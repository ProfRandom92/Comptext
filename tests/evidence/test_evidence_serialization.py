from pathlib import Path
import json
import pytest

from modules.evidence.evidence import (
    canonical_serialize,
    hash_event_content,
    build_sample_evidence,
    verify_evidence_chain,
)
from modules.validation.workspace_validation import validate_with_additional_properties

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "evidence-event.v0.schema.json"
SAMPLE_PATH = ROOT / "examples" / "workspace" / "evidence-event.sample.json"


def test_canonical_serialize_sorts_keys_and_omits_whitespace() -> None:
    # Verify that different key orders produce identical output
    dict_a = {"z": 1, "a": 2, "m": 3}
    dict_b = {"a": 2, "m": 3, "z": 1}
    
    serialized_a = canonical_serialize(dict_a)
    serialized_b = canonical_serialize(dict_b)
    
    assert serialized_a == serialized_b
    assert serialized_a == '{"a":2,"m":3,"z":1}'  # No spaces


def test_schema_required_fields() -> None:
    assert SCHEMA_PATH.exists()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    
    required = schema.get("required", [])
    expected_required = {"index", "type", "payload", "previous_hash", "hash"}
    assert set(required) == expected_required


def test_schema_rejects_unknown_fields() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    
    # Valid first
    validate_with_additional_properties(schema, sample)
    
    # Invalid with extra key
    sample["extra_unsupported_key"] = "value"
    with pytest.raises(ValueError, match="has unknown extra fields"):
        validate_with_additional_properties(schema, sample)


def test_hash_event_content_stability() -> None:
    sample_event = {
        "index": 0,
        "type": "run.started",
        "payload": {
            "command": "comptext evidence verify --sample",
            "mode": "sample"
        },
        "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    }
    # Expected value pre-calculated for the first event in build_sample_evidence
    expected_hash = "75e38380712627db05eb0d187f9e2a7ec809c7ab3ea4255bed0c9a96f55a5aa7"
    
    computed_hash = hash_event_content(sample_event)
    assert computed_hash == expected_hash
    
    # If the hash field is present, hash_event_content should ignore it
    sample_event_with_hash = sample_event.copy()
    sample_event_with_hash["hash"] = "some_incorrect_hash_to_ignore"
    computed_hash_with_ignored = hash_event_content(sample_event_with_hash)
    assert computed_hash_with_ignored == expected_hash


def test_sample_payload_secret_guardrail() -> None:
    # A simple guardrail check for sample fixtures to verify they don't contain common secret patterns.
    # Note: This is a sample-fixture guardrail only and does not claim to be a general secret scanner.
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    payload_str = json.dumps(sample.get("payload", {}))
    
    secret_indicators = ["api_key", "password", "token", "secret", "credential", "auth_token"]
    for indicator in secret_indicators:
        assert indicator not in payload_str.lower()


def test_existing_sample_chain_verification_passes() -> None:
    events = build_sample_evidence()
    result = verify_evidence_chain(events)
    assert result["ok"] is True
