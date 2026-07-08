"""Local JSON schema validation helpers for CompText dry-runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_EXAMPLE_PAIRS = (
    (Path("schemas/provider-registry.schema.json"), Path("examples/provider/provider-registry-sample.json")),
)


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValueError(f"unsupported schema type: {expected}")


def _require_type(value: Any, expected: str, location: str) -> None:
    if not _matches_type(value, expected):
        raise ValueError(f"{location} must be {expected}")


def validate_json_schema_instance(schema: dict[str, Any], instance: Any, location: str = "$") -> None:
    """Validate the small schema subset used by the local dry-run samples."""
    expected_type = schema.get("type")
    if isinstance(expected_type, str):
        _require_type(instance, expected_type, location)

    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError(f"{location} must be one of {schema['enum']}")

    if "pattern" in schema and isinstance(instance, str):
        import re
        if not re.match(schema["pattern"], instance):
            raise ValueError(f"{location} does not match pattern {schema['pattern']}")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                raise ValueError(f"{location}.{key} is required")
        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in instance:
                validate_json_schema_instance(subschema, instance[key], f"{location}.{key}")

    if isinstance(instance, list) and "items" in schema:
        for index, item in enumerate(instance):
            validate_json_schema_instance(schema["items"], item, f"{location}[{index}]")


def validate_local_schemas(*, repo_root: Path | None = None, dry_run: bool = True) -> list[dict[str, str]]:
    """Load local schemas and validate local examples without external sources."""
    if not dry_run:
        raise ValueError("CompText schema validation currently supports --dry-run only")
    root = repo_root or Path.cwd()
    results = []
    for schema_rel, example_rel in SCHEMA_EXAMPLE_PAIRS:
        schema = json.loads((root / schema_rel).read_text(encoding="utf-8"))
        example = json.loads((root / example_rel).read_text(encoding="utf-8"))
        validate_json_schema_instance(schema, example)
        results.append({"schema": str(schema_rel), "example": str(example_rel), "status": "valid"})
    return results
