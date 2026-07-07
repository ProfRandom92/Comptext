"""Local helper to validate WorkspaceSnapshot, WorkspaceDelta, and ReflectionGate examples."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from modules.validation.schema_validator import validate_json_schema_instance

WORKSPACE_SCHEMA_EXAMPLE_PAIRS = (
    (
        Path("schemas/workspace-snapshot.v0.schema.json"),
        Path("examples/workspace/workspace-snapshot.sample.json"),
    ),
    (
        Path("schemas/workspace-delta.v0.schema.json"),
        Path("examples/workspace/workspace-delta.sample.json"),
    ),
    (
        Path("schemas/reflection-gate.v0.schema.json"),
        Path("examples/workspace/reflection-gate.sample.json"),
    ),
)


def validate_with_additional_properties(schema: dict[str, Any], instance: Any, location: str = "$") -> None:
    """Validate schema instance and enforce additionalProperties: false recursively."""
    validate_json_schema_instance(schema, instance, location)

    if isinstance(instance, dict) and isinstance(schema, dict):
        if schema.get("additionalProperties") is False:
            allowed_properties = set(schema.get("properties", {}).keys())
            extra_keys = set(instance.keys()) - allowed_properties
            if extra_keys:
                raise ValueError(f"{location} has unknown extra fields: {extra_keys}")

        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in instance:
                validate_with_additional_properties(subschema, instance[key], f"{location}.{key}")

    elif isinstance(instance, list) and isinstance(schema, dict) and "items" in schema:
        for index, item in enumerate(instance):
            validate_with_additional_properties(schema["items"], item, f"{location}[{index}]")


def validate_workspace_schemas(*, repo_root: Path | None = None) -> list[dict[str, str]]:
    """Validate all workspace schemas and examples, returning structured results."""
    root = repo_root or Path.cwd()
    results = []
    for schema_rel, example_rel in WORKSPACE_SCHEMA_EXAMPLE_PAIRS:
        schema_path = root / schema_rel
        example_path = root / example_rel
        
        status = "invalid"
        error_msg = ""
        
        try:
            if not schema_path.exists():
                raise FileNotFoundError(f"Schema not found: {schema_rel}")
            if not example_path.exists():
                raise FileNotFoundError(f"Example not found: {example_rel}")
                
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            example = json.loads(example_path.read_text(encoding="utf-8"))
            
            validate_with_additional_properties(schema, example)
            status = "valid"
        except Exception as err:
            error_msg = str(err)
            
        result = {
            "schema": str(schema_rel),
            "example": str(example_rel),
            "status": status,
        }
        if error_msg:
            result["error"] = error_msg
            
        results.append(result)
        
    return results
