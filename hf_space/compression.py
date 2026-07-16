from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from time import perf_counter
from typing import Any

DEFAULT_MODEL = "microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank"


@dataclass
class CompressionResult:
    original_text: str
    compressed_text: str
    origin_tokens: int
    compressed_tokens: int
    reported_rate: float
    requested_retention_rate: float
    runtime_seconds: float
    model_name: str

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
    """Normalize LLMLingua rate values to a 0..1 ratio.

    LLMLingua versions may return a numeric ratio, a numeric percentage,
    or a percentage string such as ``"74.4%"``.
    """
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
    except Exception as exc:
        raise RuntimeError(
            "LLMLingua could not be imported. Check the Space build logs and pinned dependencies."
        ) from exc

    try:
        return PromptCompressor(model_name=model_name, use_llmlingua2=True)
    except Exception as exc:
        raise RuntimeError(
            "The LLMLingua-2 model could not be loaded. The first load can take several minutes."
        ) from exc


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

    compressor = get_compressor(model_name)
    started = perf_counter()
    try:
        raw = compressor.compress_prompt_llmlingua2(
            clean_text,
            rate=retention_rate,
            force_tokens=["\n", ".", "!", "?", ",", ":", ";", "{", "}", "[", "]"],
            chunk_end_tokens=[".", "\n"],
            return_word_label=True,
            drop_consecutive=True,
        )
    except Exception as exc:
        raise RuntimeError(f"Compression failed: {exc}") from exc

    runtime = perf_counter() - started
    return CompressionResult(
        original_text=clean_text,
        compressed_text=raw.get("compressed_prompt", ""),
        origin_tokens=int(raw.get("origin_tokens", 0)),
        compressed_tokens=int(raw.get("compressed_tokens", 0)),
        reported_rate=_parse_reported_rate(raw.get("rate")),
        requested_retention_rate=retention_rate,
        runtime_seconds=round(runtime, 4),
        model_name=model_name,
    )
