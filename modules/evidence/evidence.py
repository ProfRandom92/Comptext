"""Synthetic evidence verification for local CompText dry-run commands."""

from __future__ import annotations

import hashlib
import json
from typing import Any

GENESIS_HASH = "0" * 64


def canonical_serialize(value: Any) -> str:
    """Return deterministic canonical JSON string with sorted keys and no optional whitespace."""
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def hash_event_content(event_without_hash: dict[str, Any]) -> str:
    """Compute the SHA-256 hash of the canonical serialized event content without the hash field."""
    content = {k: v for k, v in event_without_hash.items() if k != "hash"}
    return hashlib.sha256(canonical_serialize(content).encode("utf-8")).hexdigest()


def _canonical_json(value: Any) -> str:
    return canonical_serialize(value)


def _hash_event_content(event_without_hash: dict[str, Any]) -> str:
    return hash_event_content(event_without_hash)


def _validate_payload(payload: Any) -> None:
    if isinstance(payload, dict):
        for ref_field in ("workspace_before_ref", "workspace_after_ref", "workspace_delta_ref"):
            if ref_field in payload:
                val = payload[ref_field]
                if not isinstance(val, str):
                    raise ValueError(f"payload field {ref_field} must be a string ref, not {type(val).__name__}")


def _make_event(*, index: int, event_type: str, payload: dict[str, Any], previous_hash: str) -> dict[str, Any]:
    _validate_payload(payload)
    event = {
        "index": index,
        "type": event_type,
        "payload": payload,
        "previous_hash": previous_hash,
    }
    event["hash"] = _hash_event_content(event)
    return event


def build_sample_evidence() -> list[dict[str, Any]]:
    """Build a deterministic synthetic evidence chain with no secrets or external data."""
    events: list[dict[str, Any]] = []
    previous_hash = GENESIS_HASH
    sample_payloads = (
        ("run.started", {"command": "comptext evidence verify --sample", "mode": "sample"}),
        ("tool.completed", {"tool": "sample-check", "status": "ok"}),
        ("run.completed", {"status": "verified", "network": "not_called", "providers": "not_called"}),
    )

    for index, (event_type, payload) in enumerate(sample_payloads):
        event = _make_event(index=index, event_type=event_type, payload=payload, previous_hash=previous_hash)
        events.append(event)
        previous_hash = str(event["hash"])
    return events


def verify_evidence_chain(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify event indexes, previous hashes, and content hashes for an evidence chain."""
    previous_hash = GENESIS_HASH
    for expected_index, event in enumerate(events):
        if not isinstance(event, dict):
            return {"ok": False, "error": f"event at index {expected_index} must be an object"}
        if event.get("index") != expected_index:
            return {"ok": False, "error": f"event index mismatch at {expected_index}"}
        if event.get("previous_hash") != previous_hash:
            return {"ok": False, "error": f"previous hash mismatch at index {expected_index}"}
        expected_hash = event.get("hash")
        if not isinstance(expected_hash, str):
            return {"ok": False, "error": f"event hash missing at index {expected_index}"}

        payload = event.get("payload")
        try:
            _validate_payload(payload)
        except ValueError as err:
            return {"ok": False, "error": str(err)}

        event_without_hash = {key: value for key, value in event.items() if key != "hash"}
        actual_hash = _hash_event_content(event_without_hash)
        if actual_hash != expected_hash:
            return {"ok": False, "error": f"event hash mismatch at index {expected_index}"}
        previous_hash = expected_hash

    return {
        "ok": True,
        "events": len(events),
        "root_hash": previous_hash,
    }


def verify_sample_evidence(*, sample: bool = True) -> dict[str, Any]:
    """Verify the built-in sample evidence chain without file, provider, or network access."""
    if not sample:
        raise ValueError("CompText evidence verification currently supports --sample only")
    events = build_sample_evidence()
    result = verify_evidence_chain(events)
    return {
        "command": "comptext evidence verify --sample",
        "mode": "sample",
        "network": "not_called",
        "providers": "not_called",
        **result,
    }
