# START_HERE

This is the clean repository seed for **CompText**.

Use this package as the initial content for a new repository named:

```text
comptext
```

## What this seed is

A local, safe, preparation-only foundation for building CompText as a local AI orchestration platform for software engineering.

It contains:

- product documentation,
- schemas,
- examples,
- local dry-run modules,
- Windows preparation scripts,
- tests,
- safety policies,
- clean repository metadata.

## What this seed is not

- not a public package release (local editable install only),
- not a live provider gateway,
- not a cloud service,
- not a production security or compliance product,
- not an autonomous code-changing agent.

## First read order

1. `README.md`
2. `AGENTS.md`
3. `docs/COMPTEXT_MVP.md`
4. `docs/COMPTEXT_ARCHITECTURE_v1.md`
5. `docs/COMPTEXT_SECURITY.md`
6. `docs/COMPTEXT_GATEWAY.md`
7. `docs/REPOSITORY_STRATEGY.md`

## Workflow routes

- New contributors: start with `README.md`, then use the first read order above.
- Local autonomous Codex work: read `AGENTS.md`, then `docs/CODEX_LOCAL_AUTONOMY.md`.
- Agent, skill, plugin, and memory model: read `docs/AGENT_SYSTEM.md`, `docs/SKILLS_SYSTEM.md`, `docs/PLUGIN_SYSTEM.md`, and `docs/CONTEXT_AND_MEMORY.md`.
- PR Review Memory / Token Saver workflows: read `plugins/pr-review-memory/README.md`, `plugins/pr-review-memory/SKILL.md`, and `.agents/skills/pr-review-memory/SKILL.md`.
- Community README follow-up: read `docs/README_COMMUNITY_REFRESH_PLAN.md`.

## Local Setup and Checks

From the repository root:

```bash
python -m pip install -e ".[dev]"
comptext status --dry-run
comptext doctor --dry-run
python -m pytest
git diff --check
```

The checks must remain local-only. They must not call providers, start servers, read secrets, or modify remote Git state.

## MVP direction

The smallest useful MVP is a local dry-run CLI that can validate schemas, load a sample AIR plan, create a synthetic Run Record, create synthetic Evidence Events, verify the Evidence hash chain, and show the provider registry without live provider calls.
