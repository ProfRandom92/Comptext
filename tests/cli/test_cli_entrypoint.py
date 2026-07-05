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


def test_cli_dispatch_evidence_verify_sample(capsys):
    assert main(["evidence", "verify", "--sample"]) == 0
    output = capsys.readouterr().out
    assert "CompText evidence verification sample" in output
    assert "final_hash:" in output


def test_cli_dispatch_run_sample_dry_run(capsys):
    assert main(["run", "sample", "--dry-run"]) == 0
    output = capsys.readouterr().out
    assert "CompText sample run dry-run" in output
    assert "run id: run-local-sample-001" in output
    assert "hash chain status: ok" in output
