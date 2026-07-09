---
name: comptext-status
description: View a summary of active workspace file presence and local diagnostics status.
---

# CompText Status Skill

Use this skill to view a summary of the active project file check results, python versions, and plugin setup.

## Trigger Phrases
- `/comptext-status`
- `show comptext status`
- `inspect workspace presence`

## Input
- Active repository root path.

## Steps
1. Execute the status screen subcommand:
   ```bash
   comptext status --dry-run
   ```
2. Confirm that AGENTS.md, Antigravity plugin, and Local skills are present.
3. Review the status indicators for Doctor, Workspace validation, Runtime dry-run, and Evidence chain.

## Validation Commands
- `comptext status --dry-run`

## Boundaries
- Safe offline execution only.
- No remote model calls or server startups.
- Do not perform filesystem cleanup except python cache removal.

## Expected Output Shape
- Status screen detailing workspace presence checks and local health diagnostic pass indicators.
