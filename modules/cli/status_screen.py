"""CompText local agent status screen build helper."""

from __future__ import annotations

from pathlib import Path
from modules.doctor.doctor import run_doctor
from modules.validation.workspace_validation import validate_workspace_schemas
from modules.runtime.sample_run import run_sample
from modules.evidence.evidence import verify_file_state_log, verify_sample_evidence


def build_status_screen(repo_root: Path) -> tuple[int, str]:
    """Build deterministic local agent status screen text and return exit code."""
    # Check project files presence
    agents_md = repo_root / "AGENTS.md"
    agents_md_status = "present" if agents_md.is_file() else "absent"

    plugin_json = repo_root / ".antigravity/plugins/comptext-local/plugin.json"
    plugin_status = "present" if plugin_json.is_file() else "absent"

    skills_dir = repo_root / ".antigravity/plugins/comptext-local/skills"
    skills_status = "present" if skills_dir.is_dir() else "absent"

    agents_dir = repo_root / ".antigravity/plugins/comptext-local/agents"
    agents_dir_status = "present" if agents_dir.is_dir() else "absent"

    mcp_config = repo_root / ".antigravity/plugins/comptext-local/mcp_config.json"
    mcp_status = "disabled/deferred" if mcp_config.is_file() else "none"

    hooks_plan = repo_root / ".antigravity/plugins/comptext-local/hooks_plan.md"
    hooks_status = "planned" if hooks_plan.is_file() else "none"

    # Run local checks
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
        state_log_path = repo_root / "examples/workspace/evidence-state-log.sample.json"
        state_log_res = verify_file_state_log(filepath=state_log_path)
        evidence_ok = bool(evidence_res.get("ok")) and bool(state_log_res.get("ok"))
    except Exception:
        pass

    doctor_status = "pass" if doctor_ok else "fail"
    workspace_status = "pass" if workspace_ok else "fail"
    runtime_status = "pass" if runtime_ok else "fail"
    evidence_status = "pass" if evidence_ok else "fail"

    exit_code = 0 if (doctor_ok and workspace_ok and runtime_ok and evidence_ok) else 1

    lines = [
        "COMPTEXT",
        "THE OPERATING SYSTEM FOR CONTEXT",
        "",
        "Mode: local-only / dry-run",
        "",
        "Status:",
        f"  Doctor: {doctor_status}",
        f"  Workspace validation: {workspace_status}",
        f"  Runtime dry-run sample: {runtime_status}",
        f"  Evidence chain: {evidence_status}",
        "  Providers: disabled",
        "  Network: none",
        "  GitHub runtime: none",
        "  MCP runtime: none",
        "",
        "Agent Workspace:",
        f"  AGENTS.md: {agents_md_status}",
        f"  Antigravity plugin: {plugin_status}",
        f"  Local skills: {skills_status}",
        f"  Local agents: {agents_dir_status}",
        f"  MCP config: {mcp_status}",
        f"  Hooks status: {hooks_status}",
        "",
        "Commands:",
        "  - comptext status --dry-run",
        "  - comptext validate workspace --dry-run",
        "  - comptext doctor",
        "  - python -m pytest",
    ]

    return exit_code, "\n".join(lines)
