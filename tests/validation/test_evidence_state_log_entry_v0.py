import json
from pathlib import Path

import pytest

from modules.validation.schema_validator import validate_json_schema_instance
from modules.validation.workspace_validation import validate_with_additional_properties

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "evidence-state-log-entry.v0.schema.json"
SAMPLE_PATH = ROOT / "examples" / "workspace" / "evidence-state-log-entry.sample.json"


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _load_sample() -> dict:
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


def test_schema_and_sample_exist() -> None:
    assert SCHEMA_PATH.exists()
    assert SAMPLE_PATH.exists()


def test_sample_validates_successfully() -> None:
    schema = _load_schema()
    sample = _load_sample()
    validate_with_additional_properties(schema, sample)


@pytest.mark.parametrize(
    "field",
    [
        "sequence",
        "evidence_event_hash",
        "git_commit_ref",
        "previous_state_hash",
        "state_hash",
    ],
)
def test_missing_required_field_fails_validation(field: str) -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample.pop(field)
    
    with pytest.raises(ValueError):
        validate_with_additional_properties(schema, sample)


def test_schema_rejects_unknown_fields() -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["extra_unsupported_key"] = "some_value"
    
    with pytest.raises(ValueError, match="has unknown extra fields"):
        validate_with_additional_properties(schema, sample)


@pytest.mark.parametrize(
    "invalid_git_ref",
    [
        12345,                  # Non-string
        "a" * 39,               # Wrong length (short)
        "a" * 41,               # Wrong length (long)
        "g" * 40,               # Non-hex characters
    ]
)
def test_schema_rejects_invalid_git_commit_ref(invalid_git_ref) -> None:
    schema = _load_schema()
    sample = _load_sample()
    sample["git_commit_ref"] = invalid_git_ref
    
    with pytest.raises(ValueError):
        validate_with_additional_properties(schema, sample)
