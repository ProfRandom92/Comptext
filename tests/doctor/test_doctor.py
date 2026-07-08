from pathlib import Path

import pytest

from modules.doctor.doctor import REQUIRED_PROJECT_FILES, run_doctor


def test_doctor_reports_required_project_files() -> None:
    result = run_doctor(repo_root=Path.cwd(), dry_run=True)

    assert result["mode"] == "dry-run"
    assert result["network"] == "not_checked"
    assert result["providers"] == "not_called"
    assert set(result["project_files"]) == set(REQUIRED_PROJECT_FILES)
    assert all(result["project_files"].values())
    assert "workspace_validation" in result
    assert result["workspace_validation"]["ok"] is True
    assert len(result["workspace_validation"]["results"]) == 6
    assert result["ok"] is True


def test_doctor_workspace_validation_fails_on_empty_dir(tmp_path: Path) -> None:
    result = run_doctor(repo_root=tmp_path, dry_run=True)
    assert result["workspace_validation"]["ok"] is False
    assert result["ok"] is False
    for item in result["workspace_validation"]["results"]:
        assert item["status"] == "invalid"
        assert "schema" in item
        assert "example" in item


def test_doctor_rejects_non_dry_run() -> None:
    with pytest.raises(ValueError, match="--dry-run only"):
        run_doctor(dry_run=False)
