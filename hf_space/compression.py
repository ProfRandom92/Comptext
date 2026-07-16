from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from time import perf_counter
from typing import Any

from metrics import summarize_checks
from protected_segments import split_segments
from safety_checks import run_safety_checks

DEFAULT_MODEL = "microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank"
MIN_NET_REDUCTION_PERCENT = 10.0
MIN_COMPRESSIBLE_CHARS = 80


@dataclass
class CompressionResult:
    original_text: str
    compressed_text: str
    candidate_text: str
    origin_tokens: int
    compressed_tokens: int
    reported_rate: float
    requested_retention_rate: float
    runtime_seconds: float
    model_name: str
    accepted: bool
    fallback_reason: str | None
    protected_segments: int
    compressed_segments: int

    @property
    def token_reduction_percent(self) -> float:
        if self.origin_tokens <= 0:
            return 0.0
        return round((1 - self.compressed_tokens / self.origin_tokens) * 100, 2)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["token_reduction_percent"] = self.token_reduction_percent
        return data


def _parse_reported_rate(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return 0.0
        if cleaned.endswith("%"):
            return float(cleaned[:-1].strip()) / 100.0
        number = float(cleaned)
    else:
        number = float(value)
    return number / 100.0 if number > 1.0 else number


@lru_cache(maxsize=2)
def get_compressor(model_name: str = DEFAULT_MODEL):
    try:
        from llmlingua import PromptCompressor
        return PromptCompressor(model_name=model_name, use_llmlingua2=True)
    except Exception as exc:
        raise RuntimeError(f"LLMLingua-2 could not be loaded: {exc}") from exc


@lru_cache(maxsize=2)
def get_tokenizer(model_name: str = DEFAULT_MODEL):
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(model_name)


def _token_count(text: str, model_name: str) -> int:
    return len(get_tokenizer(model_name).encode(text, add_special_tokens=False))


def _compress_segment(compressor, text: str, retention_rate: float) -> tuple[str, float]:
    raw = compressor.compress_prompt_llmlingua2(
        text,
        rate=retention_rate,
        force_tokens=["\n", ".", "!", "?", ",", ":", ";"],
        chunk_end_tokens=[".", "\n"],
        return_word_label=False,
        drop_consecutive=True,
    )
    return raw.get("compressed_prompt", text), _parse_reported_rate(raw.get("rate"))


def compress_text(
    text: str,
    retention_rate: float = 0.6,
    model_name: str = DEFAULT_MODEL,
) -> CompressionResult:
    clean_text = (text or "").strip()
    if not clean_text:
        raise ValueError("Please enter text to compress.")
    if not 0.1 <= retention_rate <= 1.0:
        raise ValueError("Retention rate must be between 0.1 and 1.0.")

    started = perf_counter()
    compressor = get_compressor(model_name)
    segments = split_segments(clean_text)
    output: list[str] = []
    rates: list[float] = []
    protected_count = 0
    compressed_count = 0

    for segment in segments:
        if segment.protected or len(segment.text.strip()) < MIN_COMPRESSIBLE_CHARS:
            output.append(segment.text)
            protected_count += 1
            continue
        try:
            compressed, rate = _compress_segment(compressor, segment.text, retention_rate)
        except Exception as exc:
            raise RuntimeError(f"Compression failed: {exc}") from exc
        output.append(compressed)
        rates.append(rate)
        compressed_count += 1

    candidate = "".join(output).strip()
    origin_tokens = _token_count(clean_text, model_name)
    candidate_tokens = _token_count(candidate, model_name)
    checks = run_safety_checks(clean_text, candidate)
    safety = summarize_checks(checks)
    reduction = (1 - candidate_tokens / origin_tokens) * 100 if origin_tokens else 0.0

    accepted = True
    fallback_reason: str | None = None
    if not safety["all_required_preserved"]:
        accepted = False
        fallback_reason = "Required protected content was lost. Original text returned."
    elif reduction < MIN_NET_REDUCTION_PERCENT:
        accepted = False
        fallback_reason = f"Net reduction {reduction:.2f}% is below {MIN_NET_REDUCTION_PERCENT:.0f}% threshold. Original text returned."

    final_text = candidate if accepted else clean_text
    final_tokens = candidate_tokens if accepted else origin_tokens
    runtime = perf_counter() - started
    return CompressionResult(
        original_text=clean_text,
        compressed_text=final_text,
        candidate_text=candidate,
        origin_tokens=origin_tokens,
        compressed_tokens=final_tokens,
        reported_rate=(sum(rates) / len(rates)) if rates else 1.0,
        requested_retention_rate=retention_rate,
        runtime_seconds=round(runtime, 4),
        model_name=model_name,
        accepted=accepted,
        fallback_reason=fallback_reason,
        protected_segments=protected_count,
        compressed_segments=compressed_count,
    )
