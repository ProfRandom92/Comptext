# CompText MVP

## Goal

The first MVP should prove the core local workflow without live provider calls or automatic file changes.

CompText MVP means:

```text
AIR Plan -> Run Record -> Agent Task -> Evidence Events -> Hash Verify -> Local Report
```

## Required MVP commands

```text
comptext doctor --dry-run
comptext validate schemas --dry-run
comptext providers list --dry-run
comptext evidence verify --sample
comptext run sample --dry-run
```

## MVP components

1. Local CLI entrypoint.
2. Schema validator.
3. Provider registry loader with safe states only.
4. Sample AIR plan loader.
5. Run record builder.
6. Synthetic Evidence event builder.
7. Evidence hash-chain verifier.
8. Local report output.
9. Unit tests and fixture validation.

## Explicit non-goals

- no live provider healthchecks in the MVP,
- no LLM calls,
- no real gateway server,
- no automatic edits,
- no push, merge, or release automation,
- no desktop UI,
- no cloud sync,
- no production security/compliance claims.

## Success criterion

A user can run local commands and see a complete dry-run trace that demonstrates how CompText connects AIR, Run, Evidence, Provider Registry, and Evidence concepts safely.
