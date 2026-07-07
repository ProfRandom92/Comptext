---
name: comptext-workspace-validation
description: Validate workspace snapshot and delta files against JSON Schema schemas.
---

# CompText Workspace Validation

Validate committed WorkspaceSnapshot, WorkspaceDelta, and ReflectionGate examples against schemas.

## Trigger Phrases
- `/comptext-workspace-validation`
- `validate workspace snapshots`
- `check committed schemas`

## Purpose
Ensure all JSON example files in `examples/workspace/` adhere strictly to their validation contracts in `schemas/`, enforcing no additional properties.

## When to Use
- After changing workspace snapshot, delta, or gate JSON examples or schemas.
- Before committing workspace state updates.

## Steps
1. Run the workspace validator command:
   ```bash
   comptext validate workspace --dry-run
   ```
2. Confirm the returned status array shows `valid` for snapshot, delta, and reflection-gate items.
3. Verify that if recursive additionalProperties checks failed, the exact mismatched keys were reported.

## Allowed Local Commands
- `comptext validate workspace --dry-run`
- `python -m pytest tests/validation`

## Boundaries
- Validations only, no active generation of files.
- No network connections, database operations, or provider requests.

## Validation Commands
- `comptext validate workspace --dry-run`
- `python -m pytest tests/validation`

## Expected Final Report Shape
- JSON array of results containing schema paths, example paths, and validation status.
