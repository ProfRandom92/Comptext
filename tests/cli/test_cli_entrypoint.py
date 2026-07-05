import json

from modules.cli.cli_entrypoint import run


def test_cli_doctor_dry_run(capsys) -> None:
    assert run(["doctor", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["command"] == "comptext doctor --dry-run"
    assert output["providers"] == "not_called"


def test_cli_validate_schemas_dry_run(capsys) -> None:
    assert run(["validate", "schemas", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert output["results"][0]["status"] == "valid"


def test_cli_providers_list_dry_run(capsys) -> None:
    assert run(["providers", "list", "--dry-run"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["mode"] == "dry-run"
    assert output["providers"]
    assert {provider["healthcheck"] for provider in output["providers"]} == {"not_run"}
