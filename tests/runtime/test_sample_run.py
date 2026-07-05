import pytest

from modules.runtime.sample_run import build_sample_run_events, run_sample
from modules.evidence.evidence import verify_evidence_chain


def test_run_sample_dry_run_returns_local_only_summary() -> None:
    result = run_sample(dry_run=True)

    assert result["command"] == "comptext run sample --dry-run"
    assert result["mode"] == "dry-run"
    assert result["ok"] is True
    assert result["run"]["status"] == "completed"
    assert len(result["plan"]["steps"]) == 3
    assert result["execution"]["provider_calls"] == 0
    assert result["execution"]["network"] == "not_called"
    assert result["execution"]["providers"] == "not_called"
    assert result["execution"]["secrets"] == "not_read"
    assert result["execution"]["file_writes"] == 0
    assert result["evidence"]["verified"] is True
    assert len(result["evidence"]["root_hash"]) == 64


def test_build_sample_run_events_are_verifiable() -> None:
    events = build_sample_run_events()
    result = verify_evidence_chain(events)

    assert result["ok"] is True
    assert result["events"] == 3


def test_run_sample_rejects_non_dry_run() -> None:
    with pytest.raises(ValueError, match="--dry-run only"):
        run_sample(dry_run=False)
