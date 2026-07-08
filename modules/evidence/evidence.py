"""Synthetic evidence verification for local CompText dry-run commands."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
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
        if "git_commit_ref" in payload:
            val = payload["git_commit_ref"]
            if not isinstance(val, str):
                raise ValueError(f"payload field git_commit_ref must be a string ref, not {type(val).__name__}")
            if len(val) != 40 or not all(c in "0123456789abcdefABCDEF" for c in val):
                raise ValueError("payload field git_commit_ref must be a 40-character hex string")



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


def verify_file_evidence(*, filepath: str | Path) -> dict[str, Any]:
    """Load and verify a local JSON file containing an array of evidence events."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Evidence file not found: {filepath}")

    with open(path, "r", encoding="utf-8") as f:
        events = json.load(f)

    if not isinstance(events, list):
        raise ValueError("Evidence file content must be a JSON array")

    result = verify_evidence_chain(events)
    return {
        "command": f"comptext evidence verify --file {filepath}",
        "mode": "file",
        "network": "not_called",
        "providers": "not_called",
        **result,
    }


def verify_state_log_chain(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify sequence, previous state hashes, git commit refs, and content hashes in a state log chain."""
    previous_hash = GENESIS_HASH
    for expected_sequence, entry in enumerate(entries):
        if not isinstance(entry, dict):
            return {"ok": False, "error": f"entry at sequence {expected_sequence} must be an object"}
        if entry.get("sequence") != expected_sequence:
            return {"ok": False, "error": f"entry sequence mismatch at {expected_sequence}"}
        if entry.get("previous_state_hash") != previous_hash:
            return {"ok": False, "error": f"previous state hash mismatch at sequence {expected_sequence}"}
        expected_hash = entry.get("state_hash")
        if not isinstance(expected_hash, str):
            return {"ok": False, "error": f"entry state hash missing at sequence {expected_sequence}"}

        # Validate git_commit_ref format
        git_ref = entry.get("git_commit_ref")
        if not isinstance(git_ref, str):
            return {"ok": False, "error": f"git_commit_ref at sequence {expected_sequence} must be a string"}
        if len(git_ref) != 40 or not all(c in "0123456789abcdefABCDEF" for c in git_ref):
            return {"ok": False, "error": f"git_commit_ref at sequence {expected_sequence} must be a 40-character hex string"}

        # Validate evidence_event_hash format
        event_hash = entry.get("evidence_event_hash")
        if not isinstance(event_hash, str):
            return {"ok": False, "error": f"evidence_event_hash at sequence {expected_sequence} must be a string"}
        if len(event_hash) != 64 or not all(c in "0123456789abcdefABCDEF" for c in event_hash):
            return {"ok": False, "error": f"evidence_event_hash at sequence {expected_sequence} must be a 64-character hex string"}

        # Compute hash of state log entry content (excluding state_hash itself)
        entry_without_hash = {k: v for k, v in entry.items() if k != "state_hash"}
        actual_hash = hashlib.sha256(canonical_serialize(entry_without_hash).encode("utf-8")).hexdigest()
        if actual_hash != expected_hash:
            return {"ok": False, "error": f"entry state hash mismatch at sequence {expected_sequence}"}
        previous_hash = expected_hash

    return {
        "ok": True,
        "entries": len(entries),
        "root_hash": previous_hash,
    }


def verify_file_state_log(*, filepath: str | Path) -> dict[str, Any]:
    """Load and verify a local JSON file containing an array of state log entries."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"State log file not found: {filepath}")

    with open(path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    if not isinstance(entries, list):
        raise ValueError("State log file content must be a JSON array")

    result = verify_state_log_chain(entries)
    return {
        "command": f"comptext evidence verify-state-log --file {filepath}",
        "mode": "state-log",
        "network": "not_called",
        "providers": "not_called",
        **result,
    }
