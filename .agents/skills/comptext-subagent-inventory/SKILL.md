---
name: comptext-subagent-inventory
description: Inspect local subagent definitions, allowed file scopes, and routing matrix.
---

# CompText Subagent Inventory

Inspect active subagent roles, routing boundaries, checks, and offline escalation rules.

## Trigger Phrases
- `/comptext-subagent-inventory`
- `list local subagent roles`
- `show subagents escalation rules`

## Purpose
View documented subagent role metadata (validation-agent, evidence-agent, runtime-dryrun-agent, pr-memory-agent, docs-agent), allowed directories, and routing matrix.

## When to Use
- To determine which subagent has authority over a set of files or directories.
- To inspect allowed boundaries and validation commands before proposing changes.

## Steps
1. Run the subagents inventory query:
   ```bash
   comptext agents --dry-run
   ```
2. Consult the routing matrix table to map task type to preferred agent.
3. Review escalation triggers (e.g. stop on dirty working tree, stop before provider behavior).

## Allowed Local Commands
- `comptext agents --dry-run`
- `git status --short`

## Boundaries
- Subagent role definitions listing only.
- No execution of background agents.
- No task scheduler setup.

## Validation Commands
- `comptext agents --dry-run`

## Expected Final Report Shape
- Plaintext inventory list of defined roles, purpose summaries, scopes, and checks.
