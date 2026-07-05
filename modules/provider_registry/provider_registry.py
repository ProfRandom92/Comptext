"""Provider registry loading for local dry-run CompText commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ALLOWED_PROVIDER_STATES = {"not_configured", "disabled", "experimental"}
DEFAULT_PROVIDER_REGISTRY = Path("examples/provider/provider-registry-sample.json")


def load_provider_registry(path: Path | str = DEFAULT_PROVIDER_REGISTRY) -> dict[str, Any]:
    """Load and validate the local provider registry sample."""
    registry_path = Path(path)
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    providers = data.get("providers")
    if not isinstance(providers, list):
        raise ValueError("provider registry must contain a providers list")

    for provider in providers:
        if not isinstance(provider, dict):
            raise ValueError("provider entries must be objects")
        state = provider.get("state")
        if state not in ALLOWED_PROVIDER_STATES:
            raise ValueError(f"provider state is not dry-run safe: {state!r}")
    return data


def list_providers(*, path: Path | str = DEFAULT_PROVIDER_REGISTRY, dry_run: bool = True) -> list[dict[str, str]]:
    """Return safe provider list rows without healthchecks or provider calls."""
    if not dry_run:
        raise ValueError("CompText provider listing currently supports --dry-run only")
    data = load_provider_registry(path)
    rows = []
    for provider in data["providers"]:
        rows.append(
            {
                "id": str(provider["id"]),
                "display_name": str(provider.get("display_name", provider["id"])),
                "state": str(provider["state"]),
                "healthcheck": "not_run",
            }
        )
    return rows
