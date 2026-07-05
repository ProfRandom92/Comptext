import json
from pathlib import Path

import pytest

from modules.provider_registry.provider_registry import ALLOWED_PROVIDER_STATES, list_providers, load_provider_registry


def test_load_provider_registry_allows_only_safe_states() -> None:
    registry = load_provider_registry(Path("examples/provider/provider-registry-sample.json"))

    states = {provider["state"] for provider in registry["providers"]}
    assert states <= ALLOWED_PROVIDER_STATES


def test_list_providers_never_runs_healthchecks() -> None:
    rows = list_providers(path=Path("examples/provider/provider-registry-sample.json"), dry_run=True)

    assert rows
    assert {row["healthcheck"] for row in rows} == {"not_run"}


def test_load_provider_registry_rejects_unsafe_state(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_text(
        json.dumps({"providers": [{"id": "unsafe", "display_name": "Unsafe", "state": "configured"}]}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="not dry-run safe"):
        load_provider_registry(registry)


def test_load_provider_registry_rejects_non_object_root(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps([]), encoding="utf-8")

    with pytest.raises(ValueError, match="root must be an object"):
        load_provider_registry(registry)


def test_load_provider_registry_requires_provider_id(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_text(
        json.dumps({"providers": [{"display_name": "Missing id", "state": "disabled"}]}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="must contain 'id'"):
        load_provider_registry(registry)
