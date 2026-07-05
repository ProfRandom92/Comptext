"""Deterministic sample runtime for local CompText dry-runs."""

from __future__ import annotations

from typing import Any

from modules.evidence.evidence import GENESIS_HASH, _make_event, verify_evidence_chain


def build_sample_run_events() -> list[dict[str, Any]]:
    """Build deterministic local-only evidence events for a sample run."""
    previous_hash = GENESIS_HASH
    event_specs = (
        (
            "run.started",
            {
                "command": "comptext run sample --dry-run",
                "mode": "dry-run",
                "workspace": "synthetic-sample",
            },
        ),
        (
            "plan.created",
            {
                "steps": [
                    "collect synthetic context",
                    "execute local placeholder task",
                    "verify evidence chain",
                ],
                "provider_calls": 0,
            },
        ),
        (
            "execution.completed",
            {
                "tools": ["sample-runtime"],
                "network": "not_called",
                "providers": "not_called",
                "secrets": "not_read",
            },
        ),
    )

    events: list[dict[str, Any]] = []
    for index, (event_type, payload) in enumerate(event_specs):
        event = _make_event(index=index, event_type=event_type, payload=payload, previous_hash=previous_hash)
        events.append(event)
        previous_hash = str(event["hash"])
    return events


def run_sample(*, dry_run: bool = True) -> dict[str, Any]:
    """Run a deterministic sample workflow without providers, network, or secrets."""
    if not dry_run:
        raise ValueError("CompText sample run currently supports --dry-run only")

    evidence = build_sample_run_events()
    verification = verify_evidence_chain(evidence)
    return {
        "command": "comptext run sample --dry-run",
        "mode": "dry-run",
        "run": {
            "id": "sample-run",
            "status": "completed" if verification.get("ok") is True else "failed",
        },
        "plan": {
            "id": "sample-plan",
            "steps": [
                {"id": "collect-context", "status": "completed"},
                {"id": "execute-placeholder", "status": "completed"},
                {"id": "verify-evidence", "status": "completed" if verification.get("ok") is True else "failed"},
            ],
        },
        "execution": {
            "provider_calls": 0,
            "network": "not_called",
            "providers": "not_called",
            "secrets": "not_read",
            "file_writes": 0,
        },
        "evidence": {
            "events": len(evidence),
            "root_hash": verification.get("root_hash"),
            "verified": verification.get("ok") is True,
        },
        "ok": verification.get("ok") is True,
    }
