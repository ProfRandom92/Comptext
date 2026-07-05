# CODEX_START_PROMPT

You are working in `ProfRandom92/comptext`, the clean main repository for **CompText**.

CompText is a local AI orchestration platform for software engineering. Keep all work local-first, dry-run-first, and evidence-aware.

## Read first

1. `AGENTS.md`
2. `README.md`
3. `START_HERE.md`
4. `docs/COMPTEXT_MVP.md`
5. `docs/COMPTEXT_ARCHITECTURE_v1.md`
6. `docs/CODEX_WORKFLOW.md`
7. `docs/COMPTEXT_MVP_TASKS.md`

## Hard boundaries

Do not create a PR, merge, release, start a gateway server, call providers, use API keys, read secrets, run destructive commands, or make production security/compliance/forensic claims.

## Product constraints

Use `CompText` for the product, `comptext` for repo/package/CLI, and `COMPTEXT` for constants and document titles. Avoid legacy product names and competition-era framing.

## Architecture

Use the seven-layer model: Terminal OS / UI, Runtime, Gateway, Agent Bus, AIR, Evidence, and Memory / Knowledge Graph. The core flow is:

```text
Run -> Plan -> Execution -> Evidence -> Replay -> Verify
```

## Next smallest safe step

Implement and validate the local dry-run commands only:

```bash
comptext doctor --dry-run
comptext validate schemas --dry-run
comptext providers list --dry-run
comptext evidence verify --sample
comptext run sample --dry-run
```

Provider states must remain `not_configured`, `disabled`, or `experimental` until real healthchecks are explicitly designed and approved.
