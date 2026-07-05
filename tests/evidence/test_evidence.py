from modules.evidence.evidence import build_sample_evidence, verify_evidence_chain, verify_sample_evidence


def test_verify_sample_evidence_returns_verified_result() -> None:
    result = verify_sample_evidence(sample=True)

    assert result["command"] == "comptext evidence verify --sample"
    assert result["mode"] == "sample"
    assert result["ok"] is True
    assert result["events"] == 3
    assert len(result["root_hash"]) == 64
    assert result["network"] == "not_called"
    assert result["providers"] == "not_called"


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
