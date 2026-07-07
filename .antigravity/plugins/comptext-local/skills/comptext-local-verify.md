---
name: comptext-local-verify
description: Perform offline smoke testing and verification checks on the CompText repository.
---

# CompText Local Verify Skill

Use this skill to verify that the offline containment borders and local components of the repository pass diagnostics cleanly.

## Trigger Phrases
- `/comptext-local-verify`
- `verify the local workspace`
- `check local repository status`

## Input
- Active repository root path.

## Steps
1. Execute the main local verification command:
   ```bash
   comptext verify --dry-run
   ```
2. Confirm that all check rows (Status screen, Subagent inventory, Workspace validation, and Doctor diagnostics) report `pass`.
3. Confirm that boundary values for Providers, Network, GitHub runtime, and MCP runtime are disabled or none.
4. Verify that the overall verification Result is `pass` with exit code `0`.

## Validation Commands
- `comptext verify --dry-run`
- `git diff --check`

## Boundaries
- Local-only dry-run mode.
- Do not run live network commands.
- Do not query remote LLM APIs.
- Do not execute GitHub mutations or open PRs.

## Expected Output Shape
- Verification dashboard showing status pass for status screen, subagents, and doctor.
