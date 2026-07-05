from modules.cli.cli_entrypoint import main


def test_cli_dispatch_doctor(capsys):
    assert main(["doctor", "--dry-run"]) == 0
    output = capsys.readouterr().out
    assert "CompText doctor dry-run" in output


def test_cli_dispatch_providers_list(capsys):
    assert main(["providers", "list", "--dry-run"]) == 0
    output = capsys.readouterr().out
    assert "CompText provider registry dry-run" in output
    assert "available" not in output
