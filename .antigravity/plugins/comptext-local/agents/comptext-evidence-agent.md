# Evidence Agent (`comptext-evidence-agent`)

## Role
Confined agent verifying hash-chain links, hashing algorithms, and string workspace pointers.

## Scope
- Directory: `modules/evidence/`, `tests/evidence/`
- Files: `.py`

## Allowed Files
- `modules/evidence/evidence.py`
- `tests/evidence/test_evidence.py`

## Forbidden Behavior
- Embedding raw WorkspaceSnapshot or WorkspaceDelta objects inside evidence payload blocks.
- Bypassing string-ref checks on evidence validations.
- Bypassing block hashing verifications.

## Required Checks
- `python -m pytest tests/evidence`

## When to Escalate
- Verification hash mismatches.
- Non-string workspace reference payloads.
- Intended modifications to gateway files.

## Final Report Expectations
- Hash-chain status showing all events verified cleanly.
