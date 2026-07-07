"""Deterministic local-only Provider Gateway v0 helpers."""

from __future__ import annotations

import copy
from typing import Any

DRY_RUN_MODEL_ID = "comptext-dry-run-model"
LOCAL_PROVIDER_ID = "comptext-local"
PLANNED_GATEWAY_ROUTES = (
    "GET /health",
    "GET /v1/models",
    "POST /v1/messages",
    "POST /v1/responses",
    "POST /v1/chat/completions",
)


def _require_dry_run(dry_run: bool) -> None:
    if not dry_run:
        raise ValueError("CompText Gateway v0 currently supports --dry-run only")


def get_gateway_health(*, dry_run: bool = True) -> dict[str, object]:
    """Return local Gateway health metadata without starting a server."""
    _require_dry_run(dry_run)
    return {
        "ok": True,
        "mode": "dry-run",
        "bind": "127.0.0.1",
        "server": "not_started",
        "providers": "not_called",
        "secrets": "not_read",
        "routes": list(PLANNED_GATEWAY_ROUTES),
    }


def list_gateway_models(*, dry_run: bool = True) -> list[dict[str, object]]:
    """Return deterministic placeholder model descriptors without provider calls."""
    _require_dry_run(dry_run)
    return [
        {
            "id": DRY_RUN_MODEL_ID,
            "provider": LOCAL_PROVIDER_ID,
            "state": "not_configured",
            "capabilities": ["text", "tools_planned"],
        }
    ]


def normalize_gateway_request(request: dict[str, Any], *, dry_run: bool = True) -> dict[str, object]:
    """Normalize a local request into the CompText Gateway dry-run shape."""
    _require_dry_run(dry_run)
    if not isinstance(request, dict):
        raise ValueError("gateway request root must be an object")

    model = request.get("model")
    if model is None:
        model = DRY_RUN_MODEL_ID
    elif not isinstance(model, str):
        raise ValueError("gateway request model must be a string")

    messages = request.get("messages")
    if messages is None:
        messages = []
    elif not isinstance(messages, list):
        raise ValueError("gateway request messages must be a list")

    tools = request.get("tools")
    if tools is None:
        tools = []
    elif not isinstance(tools, list):
        raise ValueError("gateway request tools must be a list")

    metadata = request.get("metadata")
    if metadata is None:
        metadata = {}
    elif not isinstance(metadata, dict):
        raise ValueError("gateway request metadata must be an object")

    return {
        "mode": "dry-run",
        "provider": LOCAL_PROVIDER_ID,
        "model": model,
        "messages": copy.deepcopy(messages),
        "tools": copy.deepcopy(tools),
        "metadata": copy.deepcopy(metadata),
    }


def dry_run_gateway_response(request: dict[str, Any], *, dry_run: bool = True) -> dict[str, object]:
    """Return a deterministic Gateway response without model, provider, or network calls."""
    normalized_request = normalize_gateway_request(request, dry_run=dry_run)
    return {
        "ok": True,
        "mode": "dry-run",
        "provider": LOCAL_PROVIDER_ID,
        "model": normalized_request["model"],
        "providers": "not_called",
        "network": "not_called",
        "secrets": "not_read",
        "evidence": {"planned": True},
        "request": normalized_request,
        "response": {
            "type": "dry_run_gateway_response",
            "content": "CompText Gateway v0 dry-run response. No provider was called.",
        },
    }
