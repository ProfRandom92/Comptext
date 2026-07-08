# Antigravity CLI Workflow

This document explains how to set up and use the repo-local Antigravity bridge plugin with the `agy` CLI for local development in `comptext`.

## Installation

To install the local bridge plugin in your Antigravity environment, run the following command:

```bash
agy plugin install <repo-root>\.antigravity\plugins\comptext-local
```

## Safe Offline Development Workflow

When executing local development tasks via the Antigravity CLI:

1. **Run One Unit at a Time**: Break down your tasks into small, self-contained development units.
2. **Approve Tool Permissions Responsibly**:
   - Always choose "Approve only this time" for any tool permissions requested.
   - **Never** select "Always allow" or use flags that bypass security approvals.
3. **Validate**: Run focused tests, then complete full verification before proposing commits:
   - `python -m pytest`
   - `git diff --check`
4. **Commit Locally**: Once validation passes, make a clean git commit locally with a descriptive message.
5. **Stop**: Report completion status, list changed files, and exit.

## Subagent Roles

Refer to [docs/SUBAGENTS.md](SUBAGENTS.md) for the local subagent role specifications, task routing matrix, and safe offline escalation boundaries.

## Workspace Skills & Agents

Google Antigravity loads workspace-specific customization surfaces directly from:
- Skills: `.agents/skills/{skill_name}/SKILL.md` (exposed via TUI `/skills`)
- Agents: `.agents/agents/{agent_name}/agent.json` (exposed via TUI `/agents`)

The directory `.antigravity/plugins/comptext-local/` serves as the plugin packaging source. The registered workspace agents are role definitions only for task delegation within AGY, not active runtime background schedulers. Verify their visibility by running `/skills` and `/agents` inside the active TUI session.

## Textual Workbench v0

The local CLI includes a Textual-based status and agent inventory workbench:
```bash
comptext tui --dry-run
```
- **Dry-run enforcement**: Missing the `--dry-run` flag causes the command to fail using standard `argparse` behavior.
- **Strict offline boundaries**: It does not make provider queries, network requests, GitHub API calls, start subagents, use MCP runtime, or fix TUI `/agents` discovery.
- **Dependency Guard**: In environments where `textual` is not installed, it exits with exit code 1 and prints `Textual is required for comptext tui --dry-run.`

## Next Implementation Unit

The next planned unit of work is:
- **Offline state log chain validation**: Building the local validation tools to link sequential git commit hashes directly into the evidence chain.
