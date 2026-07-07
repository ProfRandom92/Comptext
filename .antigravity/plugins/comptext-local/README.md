# CompText Local Antigravity Plugin

Local bridge plugin linking the `comptext` repository to the Google Antigravity (AGY) workspace manager.

## 1. Staged Skills
This plugin defines the following human-readable skills in `skills/` that translate to slash commands:
- `/comptext-local-verify`: Runs `comptext verify --dry-run` to test local modules.
- `/comptext-status`: Runs `comptext status --dry-run` to view file presence.
- `/comptext-subagent-inventory`: Lists active subagent roles.
- `/comptext-workspace-validation`: Runs schemas validation against committed examples.
- `/comptext-pr-review-memory`: Verifies review rendering pipelines.
- `/comptext-local-boundaries`: Runs doctor commands to verify sandbox boundaries.

## 2. Local Agent Definitions
Subagents defined in `agents/` are human-readable role configurations only. No active scheduling or autonomous background threads are executed by the plugin:
- `comptext-validation-agent`
- `comptext-evidence-agent`
- `comptext-runtime-dryrun-agent`
- `comptext-pr-memory-agent`
- `comptext-docs-agent`

## 3. MCP Configurations
Model Context Protocol configurations are empty (`"mcpServers": {}`) and deferred. No active servers are started.

## 4. Hook Event Configuration
Process hooks are disabled and documented in `hooks_plan.md` as planned reminders only.

## 5. Inspection Slash Commands
Manage components using standard TUI overlays:
- `/skills`: Browse staged skills.
- `/agents`: Inspect defined roles.
- `/mcp`: Verify disconnected/disabled server registries.
- `/hooks`: Inspect planned event hooks.
- `/permissions`: View system containment blocks.
- `/diff`: Unified diff viewer.

## 6. Local Validation
Verify the codebase by running:
```bash
comptext verify --dry-run
```
