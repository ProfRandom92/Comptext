from pathlib import Path

from modules.runtime.sample_run import (
    build_run_evidence_events,
    build_sample_run_record,
    load_sample_air_plan,
    load_sample_run_record,
    run_sample_dry_run,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_sample_run_loads_air_plan():
    plan = load_sample_air_plan(PROJECT_ROOT)

    assert plan["plan_id"] == "air-plan-local-sample-001"
    assert plan["dry_run"] is True


def test_sample_run_builds_run_record():
    plan = load_sample_air_plan(PROJECT_ROOT)
    run_record = build_sample_run_record(plan)
    fixture = load_sample_run_record(PROJECT_ROOT)

    assert run_record == fixture


def test_sample_run_creates_evidence_events():
    plan = load_sample_air_plan(PROJECT_ROOT)
    run_record = build_sample_run_record(plan)
    events = build_run_evidence_events(plan, run_record)

    assert len(events) == 4
    assert events[0]["kind"] == "run.created"
    assert all(len(event["hash"]) == 64 for event in events)


def test_sample_run_verifies_hash_chain():
    result = run_sample_dry_run(PROJECT_ROOT)

    assert result["hash_chain"]["ok"] is True
    assert result["dry_run"] is True
