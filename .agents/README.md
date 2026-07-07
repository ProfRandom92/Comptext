# CompText Workspace Agent Configuration

This directory contains workspace-scoped configurations, rules, and skills for Google Antigravity (AGY).

## Workspace Skills
AGY loads workspace-specific skills directly from:
```text
.agents/skills/{skill_name}/SKILL.md
```
These skills are mapped automatically to slash commands inside the active TUI session. Use the `/skills` TUI command to verify their loading and visibility.

The following workspace skills are defined:
- `comptext-local-verify`: Runs `comptext verify --dry-run`.
- `comptext-status`: Runs `comptext status --dry-run`.
- `comptext-subagent-inventory`: Runs `comptext agents --dry-run`.
- `comptext-workspace-validation`: Runs `comptext validate workspace --dry-run`.
- `comptext-pr-review-memory`: Validates local PR review rendering templates.
- `comptext-local-boundaries`: Runs `comptext doctor --dry-run`.

## Workspace Agents
AGY loads workspace-specific agent role definitions from:
```text
.agents/agents/{agent_name}/agent.json
```
These agents are role definitions for reference and delegation inside AGY, not automatic background executables. Use the `/agents` TUI command to verify their loading and visibility. Terminal-based inventory preview remains accessible via `comptext agents --dry-run`.

The following workspace agents are defined:
- `comptext-validation-agent`
- `comptext-evidence-agent`
- `comptext-runtime-dryrun-agent`
- `comptext-pr-memory-agent`
- `comptext-docs-agent`

## Plugin Source
The folder `.antigravity/plugins/comptext-local/` serves as the plugin packaging source/material. To invoke these skills and agents inside the active workspace session, they are mirrored under `.agents/skills/` and `.agents/agents/` which are the active workspace customization surfaces.
