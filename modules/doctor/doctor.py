"""Local-only doctor checks for the CompText dry-run scaffold."""

from __future__ import annotations

import platform
import sys
from pathlib import Path


REQUIRED_PROJECT_FILES = (
    "README.md",
    "AGENTS.md",
    "START_HERE.md",
    "docs/COMPTEXT_MVP.md",
)


def run_doctor(project_root: Path) -> dict[str, object]:
    checks: list[dict[str, str]] = []

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    checks.append(
        {
            "name": "python",
            "status": "ok" if sys.version_info >= (3, 11) else "fail",
            "detail": python_version,
        }
    )

    os_name = platform.system() or "unknown"
    checks.append({"name": "operating_system", "status": "ok", "detail": os_name})

    for relative_path in REQUIRED_PROJECT_FILES:
        exists = (project_root / relative_path).is_file()
        checks.append(
            {
                "name": f"file:{relative_path}",
                "status": "ok" if exists else "fail",
                "detail": "present" if exists else "missing",
            }
        )

    return {"ok": all(check["status"] == "ok" for check in checks), "checks": checks}
