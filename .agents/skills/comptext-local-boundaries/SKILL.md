---
name: comptext-local-boundaries
description: Audit project doctor files and verify the containment boundaries.
---

# CompText Local Boundaries

Verify the offline containment settings, Python specifications, and doctor project files check results.

## Trigger Phrases
- `/comptext-local-boundaries`
- `verify workspace doctor`
- `audit offline containment`

## Purpose
Confirm the environment is sandbox-compliant, network requests are disabled, secrets are not retrieved, and project file presence checks pass cleanly.

## When to Use
- Before performing code editing batches to ensure safety limits are active.
- To diagnose environment anomalies.

## Steps
1. Execute the repository doctor checks command:
   ```bash
   comptext doctor --dry-run
   ```
2. Verify `ok` is `true` and python version is supported.
3. Inspect `project_files` key to ensure `AGENTS.md`, `README.md`, etc., are present.

## Allowed Local Commands
- `comptext doctor --dry-run`
- `git status --short`

## Boundaries
- Safe diagnostic scans only.
- No network requests, provider calls, socket creation, or absolute filesystem modifications.

## Validation Commands
- `comptext doctor --dry-run`

## Expected Final Report Shape
- JSON doctor diagnostic report showing python status, file presence maps, and validation results.
