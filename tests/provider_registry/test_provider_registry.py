import json
from pathlib import Path

import pytest

from modules.provider_registry.provider_registry import load_provider_registry, validate_provider_registry

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_provider_registry_accepts_safe_states():
    registry = {
        "providers": [
            {"name": "one", "state": "not_configured"},
            {"name": "two", "state": "disabled"},
            {"name": "three", "state": "experimental"},
        ]
    }

    validate_provider_registry(registry)


def test_provider_registry_rejects_available_state():
    registry = {"providers": [{"name": "provider", "state": "available"}]}

    with pytest.raises(ValueError, match="forbidden state"):
        validate_provider_registry(registry)


def test_provider_registry_sample_loads():
    registry = load_provider_registry(PROJECT_ROOT / "examples" / "provider" / "provider-registry-sample.json")

    assert len(registry["providers"]) == 3


def test_provider_registry_schema_is_valid_json():
    schema_path = PROJECT_ROOT / "schemas" / "provider-registry.schema.json"

    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)

    assert schema["title"] == "COMPTEXT Provider Registry"
