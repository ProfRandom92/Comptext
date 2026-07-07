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


def test_old_evidence_without_workspace_refs_remains_valid() -> None:
    # Test that existing evidence events without workspace refs validate perfectly
    events = build_sample_evidence()
    result = verify_evidence_chain(events)
    assert result["ok"] is True


def test_evidence_with_valid_workspace_refs_passes_validation() -> None:
    events = build_sample_evidence()
    # Add valid string workspace refs to one of the payloads
    events[0]["payload"]["workspace_before_ref"] = "snap_01_init"
    events[0]["payload"]["workspace_after_ref"] = "snap_02_step"
    events[0]["payload"]["workspace_delta_ref"] = "delta_01"

    # Recalculate hash for the modified event
    from modules.evidence.evidence import _hash_event_content
    events[0].pop("hash")
    events[0]["hash"] = _hash_event_content(events[0])

    # Since we changed events[0]['hash'], we must also update events[1]['previous_hash'] and recalculate its hash
    events[1]["previous_hash"] = events[0]["hash"]
    events[1].pop("hash")
    events[1]["hash"] = _hash_event_content(events[1])

    # Same for events[2]
    events[2]["previous_hash"] = events[1]["hash"]
    events[2].pop("hash")
    events[2]["hash"] = _hash_event_content(events[2])

    result = verify_evidence_chain(events)
    assert result["ok"] is True


@pytest.mark.parametrize(
    "ref_field",
    ["workspace_before_ref", "workspace_after_ref", "workspace_delta_ref"]
)
def test_evidence_rejects_embedded_workspace_payload_objects(ref_field: str) -> None:
    events = build_sample_evidence()
    # Add an embedded object (dict) instead of a string ref
    events[0]["payload"][ref_field] = {"run_id": "embedded_object_payload"}

    # Re-calculate hash for events[0]
    from modules.evidence.evidence import _hash_event_content
    events[0].pop("hash")
    events[0]["hash"] = _hash_event_content(events[0])

    result = verify_evidence_chain(events)
    assert result["ok"] is False
    assert f"payload field {ref_field} must be a string ref" in result["error"]
