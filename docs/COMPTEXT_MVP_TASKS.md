# COMPTEXT MVP TASKS

The first CompText MVP is a local dry-run MVP. It is not a full agent OS, provider gateway, MCP runtime, or release package.

## MVP commands

Implemented local-only MVP command surface:

```bash
comptext doctor --dry-run
comptext validate schemas --dry-run
comptext providers list --dry-run
comptext evidence verify --sample
comptext run sample --dry-run
```

## Task 0: Bootstrap repository

See `tasks/00_bootstrap_repo.md`.

## Task 1: Local dry-run MVP

See `tasks/01_local_dry_run_mvp.md`.

## Acceptance baseline

- Commands do not call providers.
- Commands do not start servers.
- Commands do not read secrets or raw environment variables.
- Provider states are limited to `not_configured`, `disabled`, or `experimental`.
- Evidence output is synthetic or redacted.
- Local checks are documented honestly.

## Deferred work

Gateway server, live provider healthchecks, MCP runtime, desktop UI, package release, plugin marketplace, and production claims are explicitly deferred.
