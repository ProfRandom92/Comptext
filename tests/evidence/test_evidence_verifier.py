from modules.evidence.evidence_verifier import build_sample_evidence_events, verify_evidence_chain, verify_sample_evidence


def test_verify_sample_evidence_hash_chain():
    result = verify_sample_evidence()

    assert result["ok"] is True
    assert len(result["checked"]) == 3
    assert len(result["final_hash"]) == 64


def test_evidence_chain_rejects_tampered_hash():
    events = build_sample_evidence_events()
    events[1]["summary"] = "Tampered summary."

    result = verify_evidence_chain(events)

    assert result["ok"] is False
    assert "Hash mismatch" in result["error"]
