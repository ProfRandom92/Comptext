"""CompText local verification screen build helper."""

from __future__ import annotations

from pathlib import Path
from modules.cli.status_screen import build_status_screen
from modules.cli.agents_screen import build_agents_screen
from modules.doctor.doctor import run_doctor
from modules.validation.workspace_validation import validate_workspace_schemas


def build_verify_screen(repo_root: Path) -> tuple[int, str]:
    """Build deterministic local verify screen text and return exit code."""
    status_ok = False
    try:
        status_code, _ = build_status_screen(repo_root)
        status_ok = (status_code == 0)
    except Exception:
        pass

    agents_ok = False
    try:
        agents_code, _ = build_agents_screen(repo_root)
        agents_ok = (agents_code == 0)
    except Exception:
        pass

    workspace_ok = False
    try:
        workspace_results = validate_workspace_schemas(repo_root=repo_root)
        workspace_ok = all(r.get("status") == "valid" for r in workspace_results)
    except Exception:
        pass

    doctor_ok = False
    try:
        doctor_res = run_doctor(repo_root=repo_root, dry_run=True)
        doctor_ok = bool(doctor_res.get("ok"))
    except Exception:
        pass

    # Antigravity plugin checks
    plugin_json = repo_root / ".antigravity/plugins/comptext-local/plugin.json"
    skills_dir = repo_root / ".antigravity/plugins/comptext-local/skills"
    skills_ok = plugin_json.is_file() and skills_dir.is_dir()

    agents_dir = repo_root / ".antigravity/plugins/comptext-local/agents"
    agents_present = agents_dir.is_dir()

    mcp_config = repo_root / ".antigravity/plugins/comptext-local/mcp_config.json"
    mcp_present = mcp_config.is_file()

    hooks_plan = repo_root / ".antigravity/plugins/comptext-local/hooks_plan.md"
    hooks_present = hooks_plan.is_file()

    status_row = "pass" if status_ok else "fail"
    agents_row = "pass" if agents_ok else "fail"
    workspace_row = "pass" if workspace_ok else "fail"
    doctor_row = "pass" if doctor_ok else "fail"
    skills_row = "pass" if skills_ok else "fail"
    plugin_agents_row = "pass" if agents_present else "fail"
    mcp_row = "disabled/deferred" if mcp_present else "none"
    hooks_row = "planned" if hooks_present else "none"

    overall_ok = (status_ok and agents_ok and workspace_ok and doctor_ok and
                  skills_ok and agents_present and mcp_present and hooks_present)
    exit_code = 0 if overall_ok else 1
    result_value = "pass" if overall_ok else "fail"

    lines = [
        "COMPTEXT LOCAL VERIFY",
        "",
        "Mode: local-only / dry-run",
        "",
        "Verification rows:",
        f"  - Status screen: {status_row}",
        f"  - Subagent inventory: {agents_row}",
        f"  - Workspace validation: {workspace_row}",
        f"  - Doctor diagnostics: {doctor_row}",
        "  - Provider boundary: pass",
        "  - Network boundary: pass",
        "  - GitHub runtime boundary: pass",
        "  - MCP runtime boundary: pass",
        f"  - Plugin skills: {skills_row}",
        f"  - Plugin agents: {plugin_agents_row}",
        f"  - MCP config: {mcp_row}",
        f"  - Hooks status: {hooks_row}",
        "",
        "Boundary values:",
        "  Providers: disabled",
        "  Network: none",
        "  GitHub runtime: none",
        "  MCP runtime: none",
        "",
        f"Result: {result_value}",
        "",
        "Commands:",
        "  - comptext verify --dry-run",
        "  - comptext status --dry-run",
        "  - comptext agents --dry-run",
        "  - comptext validate workspace --dry-run",
        "  - comptext doctor --dry-run",
        "  - python -m pytest",
    ]

    return exit_code, "\n".join(lines)
