import json
from pathlib import Path

import pytest

from modules.validation.workspace_validation import (
    validate_workspace_schemas,
    validate_with_additional_properties,
    WORKSPACE_SCHEMA_EXAMPLE_PAIRS,
)

ROOT = Path(__file__).resolve().parents[2]


def test_validate_all_current_workspace_examples_successfully() -> None:
    results = validate_workspace_schemas(repo_root=ROOT)
    assert len(results) == len(WORKSPACE_SCHEMA_EXAMPLE_PAIRS)
    for result in results:
        assert result["status"] == "valid", f"Validation failed for schema {result['schema']}: {result.get('error')}"
        assert "error" not in result


def test_validation_fails_on_invalid_example_with_extra_properties() -> None:
    # Use one of the schemas with an invalid temp instance containing extra property
    schema_rel, _ = WORKSPACE_SCHEMA_EXAMPLE_PAIRS[0]
    schema_path = ROOT / schema_rel
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    
    # Create invalid instance with an extra key
    invalid_instance = {
        "run_id": "run_01",
        "goal": "Test goal",
        "active_concepts": ["concept"],
        "constraints": ["constraint"],
        "next_allowed_actions": ["action"],
        "forbidden_actions": ["forbidden"],
        "invalid_extra_field": "not allowed"
    }
    
    with pytest.raises(ValueError, match="has unknown extra fields:.*invalid_extra_field"):
        validate_with_additional_properties(schema, invalid_instance)


def test_validation_fails_on_missing_required_property() -> None:
    schema_rel, _ = WORKSPACE_SCHEMA_EXAMPLE_PAIRS[0]
    schema_path = ROOT / schema_rel
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    
    # Missing forbidden_actions
    invalid_instance = {
        "run_id": "run_01",
        "goal": "Test goal",
        "active_concepts": ["concept"],
        "constraints": ["constraint"],
        "next_allowed_actions": ["action"],
    }
    
    with pytest.raises(ValueError, match="forbidden_actions is required"):
        validate_with_additional_properties(schema, invalid_instance)


def test_validate_workspace_schemas_fails_on_missing_files(tmp_path: Path) -> None:
    results = validate_workspace_schemas(repo_root=tmp_path)
    assert len(results) == len(WORKSPACE_SCHEMA_EXAMPLE_PAIRS)
    for result in results:
        assert result["status"] == "invalid"
        assert "error" in result
        assert "Schema not found" in result["error"] or "Example not found" in result["error"]
