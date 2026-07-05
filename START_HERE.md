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

- not a release,
- not an installable package yet,
- not a live provider gateway,
- not a cloud service,
- not a production security or compliance product,
- not an autonomous code-changing agent.

## First read order

1. `README.md`
2. `docs/COMPTEXT_MVP.md`
3. `docs/COMPTEXT_ARCHITECTURE_v1.md`
4. `docs/COMPTEXT_SECURITY.md`
5. `docs/COMPTEXT_GATEWAY.md`
6. `docs/REPOSITORY_STRATEGY.md`

## Local checks

From the repository root:

```bash
python scripts/validate_clean_repo.py .
python -m pytest -q
```

The checks must remain local-only. They must not call providers, start servers, read secrets, or modify remote Git state.

## MVP direction

The smallest useful MVP is a local dry-run CLI that can validate schemas, load a sample AIR plan, create a synthetic Run Record, create synthetic Evidence Events, verify the Evidence hash chain, and show the provider registry without live provider calls.
