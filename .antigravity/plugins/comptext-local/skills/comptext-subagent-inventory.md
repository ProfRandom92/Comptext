---
name: comptext-subagent-inventory
description: Inspect local subagent definitions, allowed file scopes, and routing matrix.
---

# CompText Subagent Inventory Skill

Use this skill to view the definitions, purpose, scope rules, and validation checks for the five local CompText subagents.

## Trigger Phrases
- `/comptext-subagent-inventory`
- `list local subagents`
- `show agent routing matrix`

## Input
- Active repository root path.

## Steps
1. Execute the subagents query subcommand:
   ```bash
   comptext agents --dry-run
   ```
2. Confirm the subagent names: validation-agent, evidence-agent, runtime-dryrun-agent, pr-memory-agent, and docs-agent.
3. Review the task routing directories and escalation triggers (e.g. dirty working tree, HEAD mismatch).

## Validation Commands
- `comptext agents --dry-run`

## Boundaries
- Inventory listing only.
- Do not spawn active subprocesses or configure scheduling pipelines.

## Expected Output Shape
- Subagent inventory list with purposes, scopes, and checks.
