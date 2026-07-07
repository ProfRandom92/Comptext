import json
from pathlib import Path

import pytest

from modules.validation.schema_validator import validate_json_schema_instance

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "reflection-gate.v0.schema.json"
SAMPLE_PATH = ROOT / "examples" / "workspace" / "reflection-gate.sample.json"


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _load_sample() -> dict:
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


def _validate_with_additional_properties(schema: dict, instance: dict) -> None:
    # Validate using the existing validate_json_schema_instance helper
    validate_json_schema_instance(schema, instance)
    
    # Manually check additionalProperties since the base validator is minimal
    if schema.get("additionalProperties") is False:
        allowed_properties = set(schema.get("properties", {}).keys())
        extra_keys = set(instance.keys()) - allowed_properties
        if extra_keys:
            raise ValueError(f"additionalProperties: false violated. Extra keys: {extra_keys}")


def test_schema_and_sample_exist() -> None:
    assert SCHEMA_PATH.exists()
    assert SAMPLE_PATH.exists()


def test_sample_validates_successfully() -> None:
    schema = _load_schema()
    sample = _load_sample()
    _validate_with_additional_properties(schema, sample)


@pytest.mark.parametrize(
    "field",
    [
        "gate_id",
        "run_id",
        "workspace_ref",
        "risk",
        "principles",
        "decision",
        "allowed_next_action",
        "forbidden_actions_confirmed",
    ],
)
def test_missing_required_field_fails_validation(field: str) -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample.pop(field)
    
    with pytest.raises(ValueError, match=f"{field} is required"):
        _validate_with_additional_properties(schema, sample)


def test_unknown_extra_field_is_rejected() -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["unknown_extra_field"] = "unexpected_value"
    
    with pytest.raises(ValueError, match="additionalProperties: false violated"):
        _validate_with_additional_properties(schema, sample)


def test_invalid_risk_fails_validation() -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["risk"] = "invalid_risk_type"
    
    with pytest.raises(ValueError, match="must be one of"):
        _validate_with_additional_properties(schema, sample)


def test_invalid_decision_fails_validation() -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["decision"] = "invalid_decision"
    
    with pytest.raises(ValueError, match="must be one of"):
        _validate_with_additional_properties(schema, sample)


def test_principles_must_be_array_of_strings() -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["principles"] = "not_an_array"
    
    with pytest.raises(ValueError, match="must be array"):
        _validate_with_additional_properties(schema, sample)
        
    sample = _load_sample()
    sample["principles"] = [123, 456]
    
    with pytest.raises(ValueError, match="must be string"):
        _validate_with_additional_properties(schema, sample)


def test_forbidden_actions_confirmed_must_be_boolean() -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["forbidden_actions_confirmed"] = "not_a_boolean"
    
    with pytest.raises(ValueError, match="must be boolean"):
        _validate_with_additional_properties(schema, sample)


def test_free_text_rationale_field_is_rejected() -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["rationale"] = "my free text rationale"
    
    with pytest.raises(ValueError, match="additionalProperties: false violated"):
        _validate_with_additional_properties(schema, sample)
