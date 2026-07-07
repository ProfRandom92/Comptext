---
name: comptext-status
description: View a summary of active workspace file presence and local diagnostics status.
---

# CompText Status

Query the local status screen to check file presence, Python support, and plugin staging.

## Trigger Phrases
- `/comptext-status`
- `show workspace status`
- `check project files presence`

## Purpose
View a consolidated summary of which project files exist (AGENTS.md, plugin.json, local skills, etc.) and check doctor status.

## When to Use
- On startup to check the local development environment configuration.
- To diagnose missing metadata dependencies.

## Steps
1. Run the local status checker:
   ```bash
   comptext status --dry-run
   ```
2. Verify that `AGENTS.md`, `Antigravity plugin`, and `Local skills` are marked as `present`.
3. Check status values for Doctor, Workspace validation, Runtime, and Evidence.

## Allowed Local Commands
- `comptext status --dry-run`
- `git status --short`

## Boundaries
- Offline local-only data collection.
- No network requests, secrets retrieval, or external API calls.

## Validation Commands
- `comptext status --dry-run`

## Expected Final Report Shape
- Plaintext status screen showing presence flags, python support, and local checks summary.
