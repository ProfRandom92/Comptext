# CompText

CompText is a local AI orchestration platform for software engineering.

It is designed as a Windows-first, local-first engineering runtime that coordinates plans, runs, evidence, provider configuration, skills, hooks, subagents, and validation without requiring cloud execution by default.

## Current status

This repository seed is not a release. It is a clean starting point for a new repository named `comptext`.

Prepared surfaces:

- architecture and safety documentation,
- JSON schemas for AIR, Evidence, Run, Run Bundle, Context Pack, plugins, MCP tools, hooks, subagents, approvals, and CLI commands,
- synthetic examples and fixtures,
- local dry-run CLI scaffolding,
- local doctor and validation helpers,
- provider registry loading with safe states only,
- deterministic sample evidence hash-chain verification,
- deterministic sample run dry-run runtime,
- approval-gate and scheduler dry-run contracts,
- Windows dry-run scripts,
- unit tests for the prepared contracts.

Not implemented yet:

- no live provider calls,
- no gateway server,
- no real MCP runtime,
- no production scheduler,
- no desktop app,
- no package release,
- no automatic file modification without approval.

## Product model

CompText replaces the simple pattern:

```text
Prompt -> Answer
```

with a controllable workflow:

```text
Run -> Plan -> Execution -> Evidence -> Replay -> Verify
```

The main layers are:

1. Terminal OS / UI
2. Runtime
3. Gateway
4. Agent Bus
5. AIR
6. Evidence
7. Memory / Knowledge Graph

## Safety baseline

- Keep provider status as `not_configured`, `disabled`, or `experimental` until a real healthcheck exists.
- Do not log API keys, secrets, tokens, or credentials.
- Do not store secrets in Evidence.
- Bind any future local gateway to `127.0.0.1` by default.
- Do not auto-apply, auto-push, auto-merge, or execute destructive commands.
- Do not make production security, compliance, or forensic claims.

## Start here

Read `START_HERE.md`, then `docs/COMPTEXT_MVP.md` and `docs/COMPTEXT_ARCHITECTURE_v1.md`.

For a future repository publication plan, read `docs/REPOSITORY_STRATEGY.md`.

For Codex Desktop workflow guidance, read `docs/CODEX_DESKTOP_WORKFLOW.md` and `docs/CODEX_DESKTOP_PROMPTS.md`.

## Agent workflow docs

- `AGENTS.md`
- `docs/AGENT_SYSTEM.md`
- `docs/SKILLS_SYSTEM.md`
- `docs/HOOKS_SYSTEM.md`
- `docs/SUBAGENTS_SYSTEM.md`
- `docs/PLUGIN_SYSTEM.md`
- `docs/CONTEXT_AND_MEMORY.md`
