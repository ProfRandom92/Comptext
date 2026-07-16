from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import gradio as gr
import pandas as pd
import spaces

from compression import DEFAULT_MODEL, compress_text
from metrics import summarize_checks
from safety_checks import run_safety_checks

ROOT = Path(__file__).parent
BENCHMARK_CASES = json.loads((ROOT / "benchmark_cases.json").read_text(encoding="utf-8"))
EXAMPLE_TEXT = (
    "Ändere AGENTS.md nicht und arbeite nur mit --dry-run. "
    "CompText contains a detailed orchestration layer that coordinates providers, context preparation, policy checks, and output validation. "
    "The architecture explanation is intentionally verbose so that the safe hybrid compressor has natural-language prose to reduce while preserving every technical constraint unchanged."
)


def _export(payload: object) -> str:
    with NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        return handle.name


@spaces.GPU
def compress_ui(text: str, retention_percent: int):
    result = compress_text(text, retention_rate=retention_percent / 100)
    checks = run_safety_checks(result.original_text, result.candidate_text)
    summary = summarize_checks(checks)
    metrics = {
        "Decision": "ACCEPTED" if result.accepted else "FALLBACK TO ORIGINAL",
        "Fallback reason": result.fallback_reason or "",
        "Original tokens": result.origin_tokens,
        "Output tokens": result.compressed_tokens,
        "Net token reduction": f"{result.token_reduction_percent}%",
        "Protected segments": result.protected_segments,
        "Compressed segments": result.compressed_segments,
        "Runtime": f"{result.runtime_seconds}s",
        "Candidate safety": f"{summary['passed']}/{summary['total']}",
    }
    rows = [
        {
            "Check": c.name,
            "Relevant": "Yes" if c.relevant else "No",
            "Passed": "Yes" if c.passed else "No",
            "Expected": ", ".join(c.expected),
            "Missing": ", ".join(c.missing),
        }
        for c in checks
    ]
    payload = {"compression": result.to_dict(), "candidate_safety": summary}
    return result.compressed_text, metrics, pd.DataFrame(rows), json.dumps(payload, ensure_ascii=False, indent=2), _export(payload)


@spaces.GPU
def run_benchmark(retention_percent: int):
    rows = []
    for case in BENCHMARK_CASES:
        try:
            result = compress_text(case["text"], retention_rate=retention_percent / 100)
            checks = run_safety_checks(result.original_text, result.candidate_text)
            summary = summarize_checks(checks)
            rows.append({
                "Case": case["name"],
                "Category": case["category"],
                "Decision": "accepted" if result.accepted else "fallback",
                "Original tokens": result.origin_tokens,
                "Output tokens": result.compressed_tokens,
                "Reduction %": result.token_reduction_percent,
                "Protected": result.protected_segments,
                "Compressed": result.compressed_segments,
                "Candidate safety %": summary["score_percent"],
                "Reason": result.fallback_reason or "",
                "Runtime s": result.runtime_seconds,
            })
        except Exception as exc:
            rows.append({"Case": case["name"], "Category": case["category"], "Decision": "error", "Reason": str(exc)})
    return pd.DataFrame(rows), _export(rows)


with gr.Blocks(title="CompText Prompt Compression Lab") as demo:
    gr.Markdown(
        "# 🗜️ CompText Safe Hybrid Compression Lab\n"
        "Critical instructions, flags, paths, JSON, versions, and code symbols are protected. "
        "Only natural-language segments are compressed. Unsafe or ineffective candidates automatically fall back to the original text."
    )
    with gr.Tab("Single prompt"):
        input_text = gr.Textbox(label="Original prompt", value=EXAMPLE_TEXT, lines=14)
        retention = gr.Slider(10, 100, value=60, step=5, label="Retention rate (%)")
        button = gr.Button("Compress safely", variant="primary")
        compressed = gr.Textbox(label="Safe output", lines=14)
        metrics = gr.JSON(label="Decision and metrics")
        checks = gr.Dataframe(label="Candidate safety checks", interactive=False)
        raw = gr.Code(label="Raw result", language="json")
        download = gr.File(label="Download JSON result")
        button.click(compress_ui, [input_text, retention], [compressed, metrics, checks, raw, download])
    with gr.Tab("Benchmark suite"):
        bench_rate = gr.Slider(10, 100, value=60, step=5, label="Retention rate (%)")
        bench_button = gr.Button("Run safe hybrid benchmark", variant="primary")
        bench_table = gr.Dataframe(label="Benchmark results", interactive=False)
        bench_download = gr.File(label="Download benchmark JSON")
        bench_button.click(run_benchmark, bench_rate, [bench_table, bench_download])
    with gr.Accordion("Decision policy", open=False):
        gr.Markdown(
            f"**Model:** `{DEFAULT_MODEL}`\n\n"
            "A result is accepted only when all relevant protected elements survive and net token reduction is at least 10%. "
            "Otherwise the exact original input is returned."
        )

demo.queue(default_concurrency_limit=1, max_size=8)

if __name__ == "__main__":
    demo.launch()
