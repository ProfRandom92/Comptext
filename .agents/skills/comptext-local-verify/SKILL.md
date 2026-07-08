---
name: comptext-local-verify
description: Perform offline verify checks on status, subagents, workspace validation, and doctor diagnostics.
---

# CompText Local Verify

Perform local dry-run verification checks on status, subagents, workspace validation, and doctor diagnostics.

## Trigger Phrases
- `/comptext-local-verify`
- `verify local comptext`
- `run local verification`

## Purpose
Ensure all local repository validation modules, metadata presence rules, and boundary configurations pass offline diagnostics cleanly.

## When to Use
- Before staging or proposing a new commit.
- After implementing repository modifications.
- To verify sandbox containment rules.

## Steps
1. Run the local verification suite:
   ```bash
   comptext verify --dry-run
   ```
2. Confirm the verification status rows for Status screen, Subagent inventory, Workspace validation, and Doctor diagnostics report `pass`.
3. Confirm that boundary indicators for Providers, Network, GitHub, and MCP show expected disabled/none states.
4. Verify that the Result value reports `pass`.

## Allowed Local Commands
- `comptext verify --dry-run`
- `git status --short`
- `git diff --check`

## Boundaries
- Safe offline dry-run checks only.
- No remote LLM model queries or API calls.
- No network connections or server startups.
- No GitHub write operations.

## Validation Commands
- `comptext verify --dry-run`

## Expected Final Report Shape
- Plaintext dashboard summarizing the pass/fail state of each local check component and final pass confirmation.
