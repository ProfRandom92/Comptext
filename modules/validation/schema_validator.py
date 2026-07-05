"""Local JSON schema validation for CompText dry-runs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def validate_local_schemas(project_root: Path) -> dict[str, object]:
    schema_path = project_root / "schemas" / "provider-registry.schema.json"
    example_path = project_root / "examples" / "provider" / "provider-registry-sample.json"

    items: list[dict[str, str]] = []
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    items.append({"path": str(schema_path.relative_to(project_root)), "status": "valid-json-schema"})

    example = load_json(example_path)
    Draft202012Validator(schema).validate(example)
    items.append({"path": str(example_path.relative_to(project_root)), "status": "valid-example"})

    return {"ok": True, "items": items}
