"""Local synthetic sample run for the CompText dry-run MVP."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from modules.evidence.evidence_verifier import GENESIS_HASH, compute_event_hash, verify_evidence_chain


SAMPLE_PLAN_PATH = Path("examples") / "air" / "sample-air-plan.json"
SAMPLE_RUN_RECORD_PATH = Path("examples") / "run" / "sample-run-record.json"


def load_sample_air_plan(project_root: Path) -> dict[str, Any]:
    with (project_root / SAMPLE_PLAN_PATH).open("r", encoding="utf-8") as handle:
        plan = json.load(handle)
    if not isinstance(plan, dict):
        raise ValueError("Sample AIR plan must be a JSON object.")
    if not isinstance(plan.get("plan_id"), str) or not plan["plan_id"]:
        raise ValueError("Sample AIR plan must include a plan_id.")
    return plan


def build_sample_run_record(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": "run-local-sample-001",
        "plan_id": plan["plan_id"],
        "dry_run": True,
        "status": "verified",
        "flow": ["Run", "Plan", "Execution", "Evidence", "Replay", "Verify"],
        "task_count": len(plan.get("tasks", [])),
    }


def load_sample_run_record(project_root: Path) -> dict[str, Any]:
    with (project_root / SAMPLE_RUN_RECORD_PATH).open("r", encoding="utf-8") as handle:
        run_record = json.load(handle)
    if not isinstance(run_record, dict):
        raise ValueError("Sample Run Record must be a JSON object.")
    return run_record


def build_run_evidence_events(plan: dict[str, Any], run_record: dict[str, Any]) -> list[dict[str, Any]]:
    events = [
        {
            "sequence": 1,
            "kind": "run.created",
            "summary": f"Synthetic dry-run {run_record['run_id']} created for plan {plan['plan_id']}.",
            "previous_hash": GENESIS_HASH,
        },
        {
            "sequence": 2,
            "kind": "plan.loaded",
            "summary": f"Synthetic AIR plan {plan['plan_id']} loaded from local examples.",
            "previous_hash": "",
        },
        {
            "sequence": 3,
            "kind": "execution.simulated",
            "summary": "Synthetic local execution completed without providers, gateway, MCP, or servers.",
            "previous_hash": "",
        },
        {
            "sequence": 4,
            "kind": "verification.completed",
            "summary": "Synthetic evidence hash chain verified for local dry-run.",
            "previous_hash": "",
        },
    ]

    previous_hash = GENESIS_HASH
    for event in events:
        event["previous_hash"] = previous_hash
        event["hash"] = compute_event_hash(event)
        previous_hash = event["hash"]

    return events


def run_sample_dry_run(project_root: Path) -> dict[str, Any]:
    plan = load_sample_air_plan(project_root)
    run_record = build_sample_run_record(plan)
    evidence_events = build_run_evidence_events(plan, run_record)
    hash_chain = verify_evidence_chain(evidence_events)

    return {
        "plan": plan,
        "run_record": run_record,
        "evidence_events": evidence_events,
        "hash_chain": hash_chain,
        "dry_run": True,
    }
