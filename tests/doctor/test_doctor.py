from pathlib import Path

from modules.doctor.doctor import REQUIRED_PROJECT_FILES, run_doctor


def test_doctor_dry_run_checks_required_files():
    report = run_doctor(Path(__file__).resolve().parents[2])

    assert report["ok"] is True
    names = {check["name"] for check in report["checks"]}
    for relative_path in REQUIRED_PROJECT_FILES:
        assert f"file:{relative_path}" in names
