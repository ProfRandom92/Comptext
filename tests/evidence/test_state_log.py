import json
from pathlib import Path
import pytest

from modules.evidence.evidence import (
    verify_state_log_chain,
    verify_file_state_log,
)
from modules.cli.cli_entrypoint import run

ROOT = Path(__file__).resolve().parents[2]


def _get_valid_entries() -> list[dict]:
    sample_file = ROOT / "examples" / "workspace" / "evidence-state-log.sample.json"
    return json.loads(sample_file.read_text(encoding="utf-8"))


def test_verify_state_log_chain_valid() -> None:
    entries = _get_valid_entries()
    result = verify_state_log_chain(entries)
    assert result["ok"] is True
    assert result["entries"] == 2
    assert len(result["root_hash"]) == 64


def test_verify_state_log_chain_empty() -> None:
    result = verify_state_log_chain([])
    assert result["ok"] is False
    assert "at least 1 entry" in result["error"]


def test_verify_file_state_log_valid() -> None:
    sample_file = ROOT / "examples" / "workspace" / "evidence-state-log.sample.json"
    result = verify_file_state_log(filepath=sample_file)
    assert result["ok"] is True
    assert result["mode"] == "state-log"
    assert result["entries"] == 2
    assert len(result["root_hash"]) == 64


def test_verify_state_log_chain_invalid_sequence() -> None:
    entries = _get_valid_entries()
    entries[1]["sequence"] = 99  # Should be 1
    result = verify_state_log_chain(entries)
    assert result["ok"] is False
    assert "entry sequence mismatch" in result["error"]


def test_verify_state_log_chain_invalid_previous_state_hash() -> None:
    entries = _get_valid_entries()
    entries[1]["previous_state_hash"] = "bad_hash"
    result = verify_state_log_chain(entries)
    assert result["ok"] is False
    assert "previous state hash mismatch" in result["error"]


def test_verify_state_log_chain_tampered_state_hash() -> None:
    entries = _get_valid_entries()
    entries[0]["evidence_event_hash"] = "0" * 64  # Tamper content
    result = verify_state_log_chain(entries)
    assert result["ok"] is False
    assert "entry state hash mismatch" in result["error"]


def test_verify_file_state_log_missing() -> None:
    with pytest.raises(FileNotFoundError, match="State log file not found"):
        verify_file_state_log(filepath="does_not_exist.json")


def test_verify_file_state_log_invalid_json(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{bad json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        verify_file_state_log(filepath=bad_file)


def test_verify_file_state_log_non_array(tmp_path: Path) -> None:
    bad_file = tmp_path / "non_array.json"
    bad_file.write_text('{"sequence": 0}', encoding="utf-8")
    with pytest.raises(ValueError, match="must be a JSON array"):
        verify_file_state_log(filepath=bad_file)


# CLI Tests
def test_cli_verify_state_log_valid(capsys) -> None:
    sample_file = "examples/workspace/evidence-state-log.sample.json"
    assert run(["evidence", "verify-state-log", "--file", sample_file]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True
    assert output["mode"] == "state-log"
    assert output["entries"] == 2


def test_cli_verify_state_log_missing(capsys) -> None:
    assert run(["evidence", "verify-state-log", "--file", "does_not_exist.json"]) == 1
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is False
    assert output["error"]["type"] == "FileNotFoundError"
