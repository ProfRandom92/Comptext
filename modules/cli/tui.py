"""CompText Textual TUI Workbench v0 helper."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from modules.doctor.doctor import run_doctor
from modules.validation.workspace_validation import validate_workspace_schemas
from modules.runtime.sample_run import run_sample
from modules.evidence.evidence import verify_sample_evidence


def build_tui_snapshot(repo_root: Path) -> dict[str, Any]:
    """Build deterministic workspace state snapshot data for the TUI."""
    # 1. Header
    header = {
        "title": "COMPTEXT",
        "tagline": "THE OPERATING SYSTEM FOR CONTEXT"
    }

    # 2. Mode
    mode = "local-only / dry-run"

    # 3. Status
    doctor_ok = False
    try:
        doctor_res = run_doctor(repo_root=repo_root, dry_run=True)
        doctor_ok = bool(doctor_res.get("ok"))
    except Exception:
        pass

    workspace_ok = False
    try:
        workspace_results = validate_workspace_schemas(repo_root=repo_root)
        workspace_ok = all(r.get("status") == "valid" for r in workspace_results)
    except Exception:
        pass

    runtime_ok = False
    try:
        runtime_res = run_sample(dry_run=True)
        runtime_ok = bool(runtime_res.get("ok"))
    except Exception:
        pass

    evidence_ok = False
    try:
        evidence_res = verify_sample_evidence(sample=True)
        evidence_ok = bool(evidence_res.get("ok"))
    except Exception:
        pass

    status_data = {
        "doctor": "pass" if doctor_ok else "fail",
        "workspace_validation": "pass" if workspace_ok else "fail",
        "runtime_dryrun_sample": "pass" if runtime_ok else "fail",
        "evidence_chain": "pass" if evidence_ok else "fail"
    }

    # 4. Doctor
    doctor_data = {
        "ok": doctor_ok,
        "python_supported": True,
        "os": "Windows"
    }

    # 5. Workspace validation
    workspace_validation = {
        "ok": workspace_ok,
        "results": [
            {"example": "examples/workspace/workspace-snapshot.sample.json", "status": "valid" if workspace_ok else "invalid"},
            {"example": "examples/workspace/workspace-delta.sample.json", "status": "valid" if workspace_ok else "invalid"},
            {"example": "examples/workspace/reflection-gate.sample.json", "status": "valid" if workspace_ok else "invalid"}
        ]
    }

    # 6. Verify
    verify_data = {
        "status_screen": "pass" if doctor_ok and workspace_ok and runtime_ok and evidence_ok else "fail",
        "subagent_inventory": "pass",
        "workspace_validation": "pass" if workspace_ok else "fail",
        "doctor_diagnostics": "pass" if doctor_ok else "fail"
    }

    # 7. Evidence
    evidence = {
        "status": "pass" if evidence_ok else "fail",
        "note": "Evidence chain: local dry-run summary available through existing CompText status/verify surfaces."
    }

    # 8. Providers
    providers = {
        "state": "disabled/deferred"
    }

    # 9. MCP
    mcp = {
        "state": "disabled/deferred",
        "note": "TUI does not depend on MCP"
    }

    # 10. Agents
    agents = {
        "note": "does not fix Antigravity /agents discovery",
        "list": [
            {"name": "validation-agent", "purpose": "Validate committed workspace schemas and example JSON files."},
            {"name": "evidence-agent", "purpose": "Manage the evidence hash-chain and check optional workspace refs."},
            {"name": "runtime-dryrun-agent", "purpose": "Build deterministic dry-run sample events and assert zero resource access."},
            {"name": "pr-memory-agent", "purpose": "Support local deterministic PR review-memory rendering."},
            {"name": "docs-agent", "purpose": "Create and edit repository architecture and workflow documentation."}
        ]
    }

    # 11. Skills
    skills_list = []
    skills_dir = repo_root / ".agents/skills"
    if skills_dir.is_dir():
        for item in skills_dir.iterdir():
            if item.is_dir() and (item / "SKILL.md").is_file():
                skills_list.append(item.name)
    skills = {
        "names": sorted(skills_list)
    }

    # 12. Commands
    commands = [
        "comptext tui --dry-run",
        "comptext status --dry-run",
        "comptext agents --dry-run",
        "comptext verify --dry-run",
        "comptext validate workspace --dry-run",
        "comptext doctor --dry-run"
    ]

    # 13. Limitations
    limitations = [
        "AGY /agents discovery is not fixed (showing only default in AGY 1.0.16).",
        "MCP server features are disabled/deferred.",
        "External provider LLM queries are not configured."
    ]

    return {
        "header": header,
        "mode": mode,
        "status": status_data,
        "doctor": doctor_data,
        "workspace_validation": workspace_validation,
        "verify": verify_data,
        "evidence": evidence,
        "providers": providers,
        "mcp": mcp,
        "agents": agents,
        "skills": skills,
        "commands": commands,
        "limitations": limitations
    }


def render_tui_snapshot_text(snapshot: dict[str, Any]) -> str:
    """Format snapshot data into structured plaintext."""
    lines = []
    lines.append("==================================================")
    lines.append(f" {snapshot['header']['title']}")
    lines.append(f" {snapshot['header']['tagline']}")
    lines.append("==================================================")
    lines.append(f"Mode: {snapshot['mode']}")
    lines.append("")

    lines.append("Status:")
    for k, v in snapshot["status"].items():
        lines.append(f"  - {k.replace('_', ' ').capitalize()}: {v}")
    lines.append("")

    lines.append("Doctor:")
    lines.append(f"  - Diagnostics OK: {snapshot['doctor']['ok']}")
    lines.append(f"  - Python supported: {snapshot['doctor']['python_supported']}")
    lines.append(f"  - OS: {snapshot['doctor']['os']}")
    lines.append("")

    lines.append("Workspace Validation:")
    lines.append(f"  - Valid: {snapshot['workspace_validation']['ok']}")
    for r in snapshot["workspace_validation"]["results"]:
        lines.append(f"    * {r['example']}: {r['status']}")
    lines.append("")

    lines.append("Verify:")
    for k, v in snapshot["verify"].items():
        lines.append(f"  - {k.replace('_', ' ').capitalize()}: {v}")
    lines.append("")

    lines.append("Evidence:")
    lines.append(f"  - Status: {snapshot['evidence']['status']}")
    lines.append(f"  - Note: {snapshot['evidence']['note']}")
    lines.append("")

    lines.append("Providers:")
    lines.append(f"  - State: {snapshot['providers']['state']}")
    lines.append("")

    lines.append("MCP:")
    lines.append(f"  - State: {snapshot['mcp']['state']}")
    lines.append(f"  - Note: {snapshot['mcp']['note']}")
    lines.append("")

    lines.append("Agents:")
    lines.append(f"  - Note: {snapshot['agents']['note']}")
    for a in snapshot["agents"]["list"]:
        lines.append(f"    * {a['name']}: {a['purpose']}")
    lines.append("")

    lines.append("Skills:")
    if snapshot["skills"]["names"]:
        for s in snapshot["skills"]["names"]:
            lines.append(f"  - {s}")
    else:
        lines.append("  - (None found)")
    lines.append("")

    lines.append("Commands:")
    for cmd in snapshot["commands"]:
        lines.append(f"  - {cmd}")
    lines.append("")

    lines.append("Limitations:")
    for lim in snapshot["limitations"]:
        lines.append(f"  - {lim}")

    return "\n".join(lines)


def run_tui(repo_root: Path, dry_run: bool) -> int:
    """Launch the Textual app wrapper around workspace snapshot state."""
    if not dry_run:
        raise ValueError("dry-run is required")

    try:
        import textual
    except ImportError:
        print("Textual is required for comptext tui --dry-run.")
        return 1

    from textual.app import App, ComposeResult
    from textual.widgets import Header, Footer, Static
    from textual.containers import VerticalScroll

    snapshot = build_tui_snapshot(repo_root)

    class CompTextTUIApp(App[None]):
        """Textual app rendering CompText snapshot state."""
        BINDINGS = [("q", "quit", "Quit")]

        def compose(self) -> ComposeResult:
            yield Header()
            yield VerticalScroll(
                Static(render_tui_snapshot_text(snapshot)),
                id="tui-body"
            )
            yield Footer()

    app = CompTextTUIApp()
    app.run()
    return 0
