import json
from pathlib import Path
import pytest

from modules.cli.cli_entrypoint import run


ROOT = Path(__file__).resolve().parents[2]


def test_cli_doctor_dry_run(capsys) -> None:
    assert run(["doctor", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["command"] == "comptext doctor --dry-run"
    assert output["providers"] == "not_called"


def test_cli_validate_schemas_dry_run(capsys) -> None:
    assert run(["validate", "schemas", "--dry-run"], repo_root=Path.cwd()) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert output["results"][0]["status"] == "valid"


def test_cli_validate_workspace_dry_run(capsys) -> None:
    assert run(["validate", "workspace", "--dry-run"], repo_root=ROOT) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert len(output["results"]) == 3
    for result in output["results"]:
        assert result["status"] == "valid"
        assert "schema" in result
        assert "example" in result


def test_cli_validate_workspace_returns_non_zero_when_validation_fails(tmp_path: Path, capsys) -> None:
    assert run(["validate", "workspace", "--dry-run"], repo_root=tmp_path) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert output["results"][0]["status"] == "invalid"


def test_cli_providers_list_dry_run(capsys) -> None:
    assert run(["providers", "list", "--dry-run"], repo_root=Path.cwd()) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert output["providers"]
    assert {provider["healthcheck"] for provider in output["providers"]} == {"not_run"}


def test_cli_gateway_health_dry_run(capsys) -> None:
    assert run(["gateway", "health", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True
    assert output["server"] == "not_started"
    assert output["providers"] == "not_called"


def test_cli_gateway_models_dry_run(capsys) -> None:
    assert run(["gateway", "models", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert output["models"][0]["id"] == "comptext-dry-run-model"
    assert output["models"][0]["state"] == "not_configured"


def test_cli_gateway_sample_dry_run(capsys) -> None:
    assert run(["gateway", "sample", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True
    assert output["providers"] == "not_called"
    assert output["network"] == "not_called"
    assert output["secrets"] == "not_read"
    assert output["evidence"] == {"planned": True}


def test_cli_evidence_verify_sample(capsys) -> None:
    assert run(["evidence", "verify", "--sample"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["command"] == "comptext evidence verify --sample"
    assert output["mode"] == "sample"
    assert output["ok"] is True
    assert output["events"] == 3
    assert output["network"] == "not_called"
    assert output["providers"] == "not_called"


def test_cli_run_sample_dry_run(capsys) -> None:
    assert run(["run", "sample", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["command"] == "comptext run sample --dry-run"
    assert output["mode"] == "dry-run"
    assert output["ok"] is True
    assert output["run"]["status"] == "completed"
    assert output["execution"]["provider_calls"] == 0
    assert output["execution"]["network"] == "not_called"
    assert output["execution"]["providers"] == "not_called"
    assert output["execution"]["secrets"] == "not_read"
    assert output["evidence"]["verified"] is True


def test_cli_doctor_returns_non_zero_when_doctor_fails(tmp_path: Path, capsys) -> None:
    assert run(["doctor", "--dry-run"], repo_root=tmp_path) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is False


def test_cli_expected_errors_are_json_without_traceback(tmp_path: Path, capsys) -> None:
    assert run(["providers", "list", "--dry-run"], repo_root=tmp_path) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is False
    assert output["error"]["type"] == "FileNotFoundError"


def test_start_here_local_checks_match_available_commands() -> None:
    text = (ROOT / "START_HERE.md").read_text(encoding="utf-8")

    assert "python scripts/validate_clean_repo.py ." not in text
    assert "python -m pytest" in text
    assert "git diff --check" in text


def test_cli_status_dry_run(capsys) -> None:
    assert run(["status", "--dry-run"], repo_root=ROOT) == 0
    out = capsys.readouterr().out
    assert "COMPTEXT" in out
    assert "THE OPERATING SYSTEM FOR CONTEXT" in out
    assert "local-only / dry-run" in out
    assert "Doctor" in out
    assert "Workspace validation" in out
    assert "Runtime dry-run sample" in out
    assert "Evidence chain" in out
    assert "Providers" in out
    assert "Network" in out
    assert "GitHub runtime" in out
    assert "MCP runtime" in out
    assert "AGENTS.md" in out
    assert "Antigravity plugin" in out
    assert "Local skills" in out
    assert "Local agents" in out
    assert "MCP config" in out
    assert "Hooks status" in out
    assert "comptext status --dry-run" in out
    assert "comptext validate workspace --dry-run" in out
    assert "comptext doctor" in out
    assert "python -m pytest" in out


def test_cli_status_requires_dry_run() -> None:
    with pytest.raises(SystemExit):
        run(["status"])


def test_cli_status_fails_on_empty_dir(tmp_path: Path, capsys) -> None:
    assert run(["status", "--dry-run"], repo_root=tmp_path) == 1
    out = capsys.readouterr().out
    assert "Doctor: fail" in out
    assert "Workspace validation: fail" in out
    assert "AGENTS.md: absent" in out


def test_cli_agents_dry_run(capsys) -> None:
    assert run(["agents", "--dry-run"], repo_root=ROOT) == 0
    out = capsys.readouterr().out
    assert "COMPTEXT LOCAL SUBAGENTS" in out
    assert "local-only / dry-run" in out
    assert "validation-agent" in out
    assert "evidence-agent" in out
    assert "runtime-dryrun-agent" in out
    assert "pr-memory-agent" in out
    assert "docs-agent" in out
    assert "Routing Preview" in out
    assert "Escalation" in out
    assert "comptext status --dry-run" in out
    assert "comptext validate workspace --dry-run" in out
    assert "comptext doctor --dry-run" in out


def test_cli_agents_requires_dry_run() -> None:
    with pytest.raises(SystemExit):
        run(["agents"])


def test_cli_verify_dry_run(capsys) -> None:
    assert run(["verify", "--dry-run"], repo_root=ROOT) == 0
    out = capsys.readouterr().out
    assert "COMPTEXT LOCAL VERIFY" in out
    assert "local-only / dry-run" in out
    assert "Status screen" in out
    assert "Subagent inventory" in out
    assert "Workspace validation" in out
    assert "Doctor diagnostics" in out
    assert "Provider boundary" in out
    assert "Network boundary" in out
    assert "GitHub runtime boundary" in out
    assert "MCP runtime boundary" in out
    assert "Plugin skills" in out
    assert "Plugin agents" in out
    assert "MCP config" in out
    assert "Hooks status" in out
    assert "Result: pass" in out
    assert "comptext status --dry-run" in out
    assert "comptext agents --dry-run" in out
    assert "comptext validate workspace --dry-run" in out
    assert "comptext doctor --dry-run" in out


def test_cli_verify_requires_dry_run() -> None:
    with pytest.raises(SystemExit):
        run(["verify"])


def test_cli_main_entry_point_exists_and_invokes_run(monkeypatch) -> None:
    from modules.cli.cli_entrypoint import main
    import modules.cli.cli_entrypoint
    called = False

    def mock_run(argv=None, repo_root=None):
        nonlocal called
        called = True
        return 42

    monkeypatch.setattr(modules.cli.cli_entrypoint, "run", mock_run)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 42
    assert called is True


def test_pyproject_defines_correct_entrypoint() -> None:
    import tomllib
    pyproject_path = ROOT / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    scripts = data.get("project", {}).get("scripts", {})
    assert scripts.get("comptext") == "modules.cli.cli_entrypoint:main"
