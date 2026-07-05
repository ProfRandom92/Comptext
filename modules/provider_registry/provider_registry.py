"""Provider registry loading for local dry-runs only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ALLOWED_PROVIDER_STATES = frozenset({"not_configured", "disabled", "experimental"})


def load_provider_registry(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        registry = json.load(handle)
    validate_provider_registry(registry)
    return registry


def validate_provider_registry(registry: dict[str, Any]) -> None:
    providers = registry.get("providers")
    if not isinstance(providers, list):
        raise ValueError("Provider registry must contain a providers list.")

    for provider in providers:
        if not isinstance(provider, dict):
            raise ValueError("Each provider entry must be an object.")
        name = provider.get("name")
        state = provider.get("state")
        if not isinstance(name, str) or not name:
            raise ValueError("Each provider entry must have a non-empty name.")
        if state not in ALLOWED_PROVIDER_STATES:
            allowed = ", ".join(sorted(ALLOWED_PROVIDER_STATES))
            raise ValueError(f"Provider '{name}' uses forbidden state '{state}'. Allowed states: {allowed}.")


def format_provider_list(registry: dict[str, Any]) -> str:
    validate_provider_registry(registry)
    lines = ["CompText provider registry dry-run"]
    for provider in registry["providers"]:
        lines.append(f"- {provider['name']}: {provider['state']}")
    return "\n".join(lines)
