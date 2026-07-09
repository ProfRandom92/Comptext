---
name: comptext-workspace-validation
description: Validate workspace snapshot and delta files against JSON Schema schemas.
---

# CompText Workspace Validation Skill

Use this skill to verify that the local JSON fixtures match workspace validation contracts with additional properties forbidden.

## Trigger Phrases
- `/comptext-workspace-validation`
- `validate workspace schemas`
- `run workspace validation`

## Input
- JSON Schema definition files and example fixtures in `schemas/` and `examples/workspace/`.

## Steps
1. Execute the validation runner command:
   ```bash
   comptext validate workspace --dry-run
   ```
2. Check the status key of the snapshot, delta, and reflection-gate examples is `valid`.
3. If errors are present, verify that the recursive additionalProperties check identified the unknown fields.

## Validation Commands
- `comptext validate workspace --dry-run`
- `python -m pytest tests/validation`

## Boundaries
- No mutation of schemas or example files.
- No network queries or remote connection calls.

## Expected Output Shape
- JSON results mapping schema paths, example paths, and validation status.
