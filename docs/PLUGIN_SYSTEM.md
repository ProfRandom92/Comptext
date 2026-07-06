# CompText Plugin System

Plugins are planned extension packs for CompText. They may provide skills, hooks, subagents, rules, templates, checks, and MCP server configuration.

No plugin runtime is implemented in this repository yet.

## Plugin contents

A future plugin may include:

- skills
- hook contracts
- subagent definitions
- rules and policies
- templates
- local validation checks
- MCP server configs

MCP tools may or may not be exposed depending on the local environment, installed connectors, and user configuration. Documentation must not assume they are always available.

## Example plugin packs

- Python Pack: Python skills, lint/test recipes, and packaging checks.
- Git/GitHub Pack: branch, review, PR, and issue workflow helpers.
- Provider Gateway Pack: provider registry and gateway contract checks.
- Evidence Pack: evidence schema, redaction, verification, and replay helpers.
- Windows Pack: Windows-first local workflow recipes and path handling.
- Docs Pack: documentation templates, markdown checks, and navigation rules.

## Workflow integration concept

The CompText Token Saver plugin is a workflow integration concept for compact project-state-first operation and codebase-memory-assisted context gathering. It may not be installed or available in every environment.

The local [`comptext-pr-review-memory`](../plugins/pr-review-memory/README.md) scaffold is a companion for token-saving workflows. It defines compact PR review-memory formats for recurring review work, including actionable comments, resolved threads, validation, merge readiness, and next action.

This scaffold does not replace CompText Token Saver. It does not perform GitHub actions, make network calls, make provider calls, modify PRs, merge branches, read secrets, or implement an MCP runtime server. Its skill instructions are documented in [`plugins/pr-review-memory/SKILL.md`](../plugins/pr-review-memory/SKILL.md).

## Safety requirements

- Plugins must declare required tools and permissions.
- Plugins must not access secrets by default.
- Plugins must not make live provider calls by default.
- Plugins must produce auditable outputs when they affect work.
- Plugins must clearly distinguish planned contracts from implemented behavior.
