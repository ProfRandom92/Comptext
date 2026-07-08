---
name: comptext-local-boundaries
description: Verify strict dry-run boundaries and local doctor configurations.
---

# CompText Local Boundaries Skill

Use this skill to audit project doctor files and verify the sandbox/offline setup of the local workspace.

## Trigger Phrases
- `/comptext-local-boundaries`
- `check dry run boundaries`
- `verify offline settings`

## Input
- Project manifest files and settings configurations.

## Steps
1. Execute the doctor diagnostic command:
   ```bash
   comptext doctor --dry-run
   ```
2. Confirm `ok` is `true`.
3. Verify that network, providers, and absolute filesystem accesses are flagged as blocked or not called.

## Validation Commands
- `comptext doctor --dry-run`

## Boundaries
- Do not make HTTP/HTTPS connections.
- Do not write to host-wide paths outside the repository workspace.

## Expected Output Shape
- Doctor diagnostics JSON report detailing supporting versions and system parameters.
