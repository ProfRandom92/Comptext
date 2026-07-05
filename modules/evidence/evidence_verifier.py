"""Synthetic Evidence hash-chain verification for local dry-runs."""

from __future__ import annotations

import hashlib
import json
from typing import Any


GENESIS_HASH = "0" * 64


def _event_payload(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "sequence": event["sequence"],
        "kind": event["kind"],
        "summary": event["summary"],
        "previous_hash": event["previous_hash"],
    }


def compute_event_hash(event: dict[str, Any]) -> str:
    payload = json.dumps(_event_payload(event), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_sample_evidence_events() -> list[dict[str, Any]]:
    events = [
        {
            "sequence": 1,
            "kind": "run.created",
            "summary": "Synthetic local dry-run record created.",
            "previous_hash": GENESIS_HASH,
        },
        {
            "sequence": 2,
            "kind": "plan.accepted",
            "summary": "Synthetic plan accepted for local dry-run.",
            "previous_hash": "",
        },
        {
            "sequence": 3,
            "kind": "verification.completed",
            "summary": "Synthetic replay verification completed.",
            "previous_hash": "",
        },
    ]

    previous_hash = GENESIS_HASH
    for event in events:
        event["previous_hash"] = previous_hash
        event["hash"] = compute_event_hash(event)
        previous_hash = event["hash"]

    return events


def verify_evidence_chain(events: list[dict[str, Any]]) -> dict[str, Any]:
    previous_hash = GENESIS_HASH
    checked: list[dict[str, str]] = []

    for expected_sequence, event in enumerate(events, start=1):
        if event.get("sequence") != expected_sequence:
            return {"ok": False, "error": f"Unexpected sequence at event {expected_sequence}.", "checked": checked}
        if event.get("previous_hash") != previous_hash:
            return {"ok": False, "error": f"Previous hash mismatch at event {expected_sequence}.", "checked": checked}

        computed_hash = compute_event_hash(event)
        if event.get("hash") != computed_hash:
            return {"ok": False, "error": f"Hash mismatch at event {expected_sequence}.", "checked": checked}

        checked.append({"kind": event["kind"], "hash": computed_hash})
        previous_hash = computed_hash

    return {"ok": True, "checked": checked, "final_hash": previous_hash}


def verify_sample_evidence() -> dict[str, Any]:
    events = build_sample_evidence_events()
    result = verify_evidence_chain(events)
    result["events"] = events
    return result
