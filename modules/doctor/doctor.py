"""Local dry-run doctor checks for CompText."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

from modules.validation.workspace_validation import validate_workspace_schemas

REQUIRED_PROJECT_FILES = (
    "AGENTS.md",
    "README.md",
    "START_HERE.md",
    "CODEX_START_PROMPT.md",
    "docs/COMPTEXT_MVP.md",
    "docs/COMPTEXT_MVP_TASKS.md",
    "tasks/00_bootstrap_repo.md",
    "tasks/01_local_dry_run_mvp.md",
)


def run_doctor(*, repo_root: Path | None = None, dry_run: bool = True) -> dict[str, object]:
    """Return a safe local environment summary without network or secret access."""
    if not dry_run:
        raise ValueError("CompText doctor currently supports --dry-run only")

    root = repo_root or Path.cwd()
    files = {
        relative_path: (root / relative_path).is_file()
        for relative_path in REQUIRED_PROJECT_FILES
    }

    workspace_results = validate_workspace_schemas(repo_root=root)
    workspace_ok = all(r.get("status") == "valid" for r in workspace_results)

    return {
        "command": "comptext doctor --dry-run",
        "mode": "dry-run",
        "python": {
            "version": platform.python_version(),
            "supported": sys.version_info >= (3, 10),
        },
        "os": {
            "system": platform.system() or "unknown",
            "release": platform.release() or "unknown",
        },
        "project_files": files,
        "workspace_validation": {
            "results": workspace_results,
            "ok": workspace_ok,
        },
        "ok": all(files.values()) and sys.version_info >= (3, 10) and workspace_ok,
        "network": "not_checked",
        "providers": "not_called",
    }
