# AGENTS.md

This repository is the clean main project for **CompText**, a local AI orchestration platform for software engineering.

## Product naming

Use these names consistently:

- Product name: `CompText`
- Repository, package, and CLI name: `comptext`
- Constants and document titles: `COMPTEXT`

Do not use legacy product-core names or framing or migration-era names/competition positioning.

## Current operating mode

The repository is preparation-only and local-dry-run-first. Do not present stubs or contracts as production-ready features.

## Architecture baseline

CompText is organized as a seven-layer system:

1. Terminal OS / UI
2. Runtime
3. Gateway
4. Agent Bus
5. AIR
6. Evidence
7. Memory / Knowledge Graph

Core flow:

```text
Run -> Plan -> Execution -> Evidence -> Replay -> Verify
```

## Allowed work

- Create and update documentation, schemas, examples, tests, and dry-run scaffolding.
- Run local-only checks that parse files, validate schemas, scan for obvious secret patterns, compile Python files, or execute unit tests.
- Keep provider states limited to `not_configured`, `disabled`, or `experimental`.

## Forbidden work

- Do not create pull requests, merge, or release.
- Do not perform live provider calls, real healthchecks, gateway startup, or MCP runtime startup.
- Do not read, use, print, or log secrets, API keys, tokens, raw environment variables, or provider payloads.
- Do not execute destructive commands.
- Do not claim production security, compliance, forensic, or provider readiness.
- Do not store hidden chain-of-thought or unredacted payloads in Evidence.

## Evidence rules

Evidence may store redacted metadata, hashes, tool summaries, synthetic test results, and approved diffs. Evidence must not store secrets, API keys, raw environment variables, hidden chain-of-thought, or unredacted provider payloads.

## MVP focus

The next safe implementation step is a local dry-run MVP:

```bash
comptext doctor --dry-run
comptext validate schemas --dry-run
comptext providers list --dry-run
comptext evidence verify --sample
comptext run sample --dry-run
```
