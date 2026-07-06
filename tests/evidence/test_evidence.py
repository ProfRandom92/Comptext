import pytest

from modules.evidence.evidence import build_sample_evidence, verify_evidence_chain, verify_sample_evidence


def test_build_sample_evidence_is_deterministic() -> None:
    first = build_sample_evidence()
    second = build_sample_evidence()

    assert first == second
    assert verify_evidence_chain(first) == verify_evidence_chain(second)


def test_verify_sample_evidence_returns_verified_result() -> None:
    result = verify_sample_evidence(sample=True)

    assert result["command"] == "comptext evidence verify --sample"
    assert result["mode"] == "sample"
    assert result["ok"] is True
    assert result["events"] == 3
    assert len(result["root_hash"]) == 64
    assert result["network"] == "not_called"
    assert result["providers"] == "not_called"


def test_verify_sample_evidence_rejects_non_sample_mode() -> None:
    with pytest.raises(ValueError, match="--sample only"):
        verify_sample_evidence(sample=False)


def test_verify_evidence_chain_rejects_non_object_event() -> None:
    result = verify_evidence_chain(["not an event"])  # type: ignore[list-item]

    assert result["ok"] is False
    assert "must be an object" in result["error"]


def test_verify_evidence_chain_rejects_missing_hash() -> None:
    events = build_sample_evidence()
    events[0].pop("hash")

    result = verify_evidence_chain(events)

    assert result["ok"] is False
    assert "event hash missing" in result["error"]


def test_verify_evidence_chain_rejects_tampered_payload() -> None:
    events = build_sample_evidence()
    events[1]["payload"]["status"] = "tampered"

    result = verify_evidence_chain(events)

    assert result["ok"] is False
    assert "hash mismatch" in result["error"]


def test_verify_evidence_chain_rejects_broken_previous_hash() -> None:
    events = build_sample_evidence()
    events[2]["previous_hash"] = "bad"

    result = verify_evidence_chain(events)

    assert result["ok"] is False
    assert "previous hash mismatch" in result["error"]
