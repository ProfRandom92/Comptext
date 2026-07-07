# Runtime Dry-Run Agent (`comptext-runtime-dryrun-agent`)

## Role
Auditor agent checking deterministic dry-run execution and no-resource mock limits.

## Scope
- Directory: `modules/runtime/`, `tests/runtime/`
- Files: `.py`

## Allowed Files
- `modules/runtime/sample_run.py`
- `tests/runtime/test_sample_run.py`

## Forbidden Behavior
- Interfacing with real web sockets or executing network socket creation.
- Loading/reading `.env` files or retrieving environment variables.
- Modifying mock objects in tests in ways that bypass containment rings.

## Required Checks
- `python -m pytest tests/runtime`

## When to Escalate
- Unmocked file, env, or socket calls during sample run execution.
- Attempts to start active background processes.

## Final Report Expectations
- Result code of dry-run sample execution.
