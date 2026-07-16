from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import gradio as gr
import pandas as pd
import spaces

from compression import DEFAULT_MODEL, compress_text
from metrics import summarize_checks
from previews import build_air_preview, build_evidence_preview, scan_secrets
from safety_checks import run_safety_checks
from universe import capabilities_frame, contracts_frame, layers_frame, load_universe, overview_markdown, skills_frame

ROOT = Path(__file__).parent
BENCHMARK_CASES = json.loads((ROOT / "benchmark_cases.json").read_text(encoding="utf-8"))
UNIVERSE = load_universe()
EXAMPLE_TEXT = (
    "Führe keine Live-Provider-Aufrufe aus. Ändere AGENTS.md nicht. "
    "Analysiere ausführlich, wie CompText Context Packs für lokale Softwareentwicklung vorbereitet. "
    "Nutze modules/cli/cli_entrypoint.py nur lesend mit --dry-run und gib einen JSON-Bericht zurück."
)


def _json_export(payload: object) -> str:
    with NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        return handle.name


@spaces.GPU
def compress_ui(text: str, retention_percent: int):
    secret_matches = scan_secrets(text)
    if secret_matches:
        payload = {
            "decision": "blocked",
            "reason": "Potential secret material detected. Input was not processed.",
            "secret_matches": secret_matches,
        }
        return text, payload, pd.DataFrame(), json.dumps(payload, ensure_ascii=False, indent=2), None

    result = compress_text(text, retention_rate=retention_percent / 100)
    checks = run_safety_checks(result.original_text, result.candidate_text)
    summary = summarize_checks(checks)
    decision = "accepted" if result.accepted else "fallback"
    metrics = {
        "Decision": decision,
        "Original tokens": result.origin_tokens,
        "Output tokens": result.compressed_tokens,
        "Net reduction": f"{result.token_reduction_percent}%",
        "Protected segments": result.protected_segments,
        "Compressed segments": result.compressed_segments,
        "Candidate safety": f"{summary['score_percent']}%",
        "Runtime": f"{result.runtime_seconds}s",
        "Reason": result.fallback_reason or "",
    }
    rows = [
        {
            "Check": check.name,
            "Relevant": "Yes" if check.relevant else "No",
            "Passed": "Yes" if check.passed else "No",
            "Expected": ", ".join(check.expected),
            "Missing": ", ".join(check.missing),
        }
        for check in checks
    ]
    payload = {
        "decision": decision,
        "compression": result.to_dict(),
        "safety": summary,
        "air_preview": build_air_preview(text, {"decision": decision, "metrics": metrics}),
        "evidence_preview": build_evidence_preview(text, result.compressed_text, decision, metrics),
    }
    return result.compressed_text, metrics, pd.DataFrame(rows), json.dumps(payload, ensure_ascii=False, indent=2), _json_export(payload)


def preview_contracts(text: str):
    matches = scan_secrets(text)
    air = build_air_preview(text)
    evidence = build_evidence_preview(text, text, "preview_only", {"secret_matches": matches})
    return air, evidence


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
    return pd.DataFrame(rows), _json_export(rows)


with gr.Blocks(title="CompText Universe") as demo:
    gr.Markdown(overview_markdown(UNIVERSE))
    gr.Markdown(
        "**Experimental public showcase:** no provider calls, no repository writes, no AIR execution, "
        "no persistent prompt storage. The local CompText kernel remains the product runtime."
    )

    with gr.Tab("Overview"):
        with gr.Row():
            gr.Markdown(
                "## Context is the product\n"
                "CompText treats models as interchangeable providers while context, contracts and Evidence "
                "form the durable engineering system. This Space visualizes that model without executing it."
            )
            gr.JSON(value={
                "product_status": UNIVERSE["product"]["status"],
                "snapshot_version": UNIVERSE["snapshot_version"],
                "runtime_github_access": UNIVERSE["source"]["runtime_github_access"],
                "compression_model": DEFAULT_MODEL,
            }, label="Snapshot identity")
        gr.Dataframe(value=contracts_frame(UNIVERSE), label="Core contracts", interactive=False)

    with gr.Tab("Architecture"):
        gr.Markdown(
            "## Seven-layer model\n"
            "`User → Terminal OS / UI → Runtime / Gateway / Agent Bus → AIR / Evidence / Memory → Provider Router`"
        )
        gr.Dataframe(value=layers_frame(UNIVERSE), label="Architecture layers", interactive=False)

    with gr.Tab("Capabilities"):
        gr.Markdown("## What exists, what is experimental, and what remains future")
        gr.Dataframe(value=capabilities_frame(UNIVERSE), label="Capability matrix", interactive=False)

    with gr.Tab("Compression Lab"):
        gr.Markdown(
            "## Fail-closed hybrid compression\n"
            "Critical instructions, flags, paths, structured data and code-like symbols are protected. "
            "Unsafe or unhelpful candidates return the exact original input."
        )
        input_text = gr.Textbox(label="Engineering context", value=EXAMPLE_TEXT, lines=14)
        retention = gr.Slider(10, 100, value=60, step=5, label="Retention rate (%)")
        compress_button = gr.Button("Analyze and compress", variant="primary")
        compressed = gr.Textbox(label="Final output", lines=14)
        compression_metrics = gr.JSON(label="Decision and metrics")
        checks = gr.Dataframe(label="Relevant preservation checks", interactive=False)
        raw = gr.Code(label="Compression + AIR + Evidence payload", language="json")
        download = gr.File(label="Download JSON")
        compress_button.click(compress_ui, [input_text, retention], [compressed, compression_metrics, checks, raw, download])

    with gr.Tab("AIR & Evidence"):
        gr.Markdown(
            "## Non-executable contract previews\n"
            "AIR describes intended work. Evidence describes observed work. Here, AIR is always disabled and "
            "Evidence is always marked as simulated."
        )
        preview_text = gr.Textbox(label="Engineering task", value=EXAMPLE_TEXT, lines=10)
        preview_button = gr.Button("Build previews")
        air_output = gr.JSON(label="AIR preview")
        evidence_output = gr.JSON(label="Simulated Evidence preview")
        preview_button.click(preview_contracts, preview_text, [air_output, evidence_output])

    with gr.Tab("Skills"):
        gr.Markdown("## Skill-grounded local workflow and safety boundaries")
        gr.Dataframe(value=skills_frame(UNIVERSE), label="Workspace skills", interactive=False)

    with gr.Tab("Benchmarks"):
        gr.Markdown("## CompText-specific protected-context benchmark")
        bench_rate = gr.Slider(10, 100, value=60, step=5, label="Retention rate (%)")
        bench_button = gr.Button("Run benchmark", variant="primary")
        bench_table = gr.Dataframe(label="Benchmark results", interactive=False)
        bench_download = gr.File(label="Download benchmark JSON")
        bench_button.click(run_benchmark, bench_rate, [bench_table, bench_download])

    with gr.Accordion("Model, provenance and limitations", open=False):
        gr.JSON(value=UNIVERSE["source"], label="Static snapshot provenance")
        gr.Markdown(
            f"**Compression model:** `{DEFAULT_MODEL}`\n\n"
            "The Universe snapshot is committed data, not a live GitHub view. Safety checks are deterministic "
            "preservation heuristics, not a semantic equivalence proof."
        )


demo.queue(default_concurrency_limit=1, max_size=8)

if __name__ == "__main__":
    demo.launch(ssr_mode=False)
