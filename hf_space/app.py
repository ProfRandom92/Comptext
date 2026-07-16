from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import gradio as gr
import pandas as pd

from compression import DEFAULT_MODEL, compress_text
from metrics import summarize_checks
from safety_checks import run_safety_checks

ROOT = Path(__file__).parent
BENCHMARK_CASES = json.loads((ROOT / "benchmark_cases.json").read_text(encoding="utf-8"))
EXAMPLE_TEXT = "Führe keine Live-Provider-Aufrufe aus. Ändere AGENTS.md nicht. Analysiere modules/cli/cli_entrypoint.py mit --dry-run und gib JSON zurück."


def compress_ui(text: str, retention_percent: int):
    result = compress_text(text, retention_rate=retention_percent / 100)
    checks = run_safety_checks(result.original_text, result.compressed_text)
    summary = summarize_checks(checks)
    metrics = {
        "Original tokens": result.origin_tokens,
        "Compressed tokens": result.compressed_tokens,
        "Token reduction": f"{result.token_reduction_percent}%",
        "Runtime": f"{result.runtime_seconds}s",
        "Safety checks": f"{summary['passed']}/{summary['total']}",
    }
    rows = [{"Check": c.name, "Passed": "Yes" if c.passed else "No", "Expected": ", ".join(c.expected), "Missing": ", ".join(c.missing)} for c in checks]
    payload = {"compression": result.to_dict(), "safety": summary}
    with NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        export_path = handle.name
    return result.compressed_text, metrics, pd.DataFrame(rows), json.dumps(payload, ensure_ascii=False, indent=2), export_path


def run_benchmark(retention_percent: int):
    rows = []
    for case in BENCHMARK_CASES:
        try:
            result = compress_text(case["text"], retention_rate=retention_percent / 100)
            checks = run_safety_checks(result.original_text, result.compressed_text)
            summary = summarize_checks(checks)
            rows.append({"Case": case["name"], "Category": case["category"], "Original tokens": result.origin_tokens, "Compressed tokens": result.compressed_tokens, "Reduction %": result.token_reduction_percent, "Runtime s": result.runtime_seconds, "Safety %": summary["score_percent"]})
        except Exception as exc:
            rows.append({"Case": case["name"], "Category": case["category"], "Error": str(exc)})
    frame = pd.DataFrame(rows)
    with NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=2)
        export_path = handle.name
    return frame, export_path


with gr.Blocks(title="CompText Prompt Compression Lab") as demo:
    gr.Markdown("# 🗜️ CompText Prompt Compression Lab\nEvaluate multilingual prompt compression with Microsoft LLMLingua-2 on free CPU hardware. The first request may take several minutes.")
    with gr.Tab("Single prompt"):
        input_text = gr.Textbox(label="Original prompt", value=EXAMPLE_TEXT, lines=14)
        retention = gr.Slider(10, 100, value=60, step=5, label="Retention rate (%)")
        button = gr.Button("Compress", variant="primary")
        compressed = gr.Textbox(label="Compressed prompt", lines=14)
        metrics = gr.JSON(label="Metrics")
        checks = gr.Dataframe(label="Safety checks", interactive=False)
        raw = gr.Code(label="Raw result", language="json")
        download = gr.File(label="Download JSON result")
        button.click(compress_ui, [input_text, retention], [compressed, metrics, checks, raw, download])
    with gr.Tab("Benchmark suite"):
        bench_rate = gr.Slider(10, 100, value=60, step=5, label="Retention rate (%)")
        bench_button = gr.Button("Run built-in benchmark", variant="primary")
        bench_table = gr.Dataframe(label="Benchmark results", interactive=False)
        bench_download = gr.File(label="Download benchmark JSON")
        bench_button.click(run_benchmark, bench_rate, [bench_table, bench_download])
    with gr.Accordion("Model and limitations", open=False):
        gr.Markdown(f"**Model:** `{DEFAULT_MODEL}`\n\nCPU inference can be slow. Free Spaces sleep after inactivity. Safety checks are heuristics, not semantic guarantees.")

demo.queue(default_concurrency_limit=1, max_size=8)

if __name__ == "__main__":
    demo.launch()
