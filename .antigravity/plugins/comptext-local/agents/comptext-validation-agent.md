# Validation Agent (`comptext-validation-agent`)

## Role
Specialized agent for checking committed schemas, workspace snaps, deltas, and reflection gates against JSON validation rules.

## Scope
- Directory: `schemas/`, `examples/workspace/`, `modules/validation/`
- Files: `.json`, `.py`

## Allowed Files
- `schemas/*.schema.json`
- `examples/workspace/*.sample.json`
- `modules/validation/workspace_validation.py`
- `tests/validation/*.py`

## Forbidden Behavior
- Bypassing the additionalProperties: false check.
- Starting network servers.
- Calling LLM provider APIs.

## Required Checks
- `comptext validate workspace --dry-run`
- `python -m pytest tests/validation`

## When to Escalate
- Escalated immediately if working tree is dirty before starting.
- Mismatched expected HEAD commit hash.
- Invalid JSON schema structures.

## Final Report Expectations
- Compact validation results summary.
