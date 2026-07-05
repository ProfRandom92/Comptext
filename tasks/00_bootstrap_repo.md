# Task 00: Bootstrap repository

## Goal

Initialize `ProfRandom92/comptext` as the clean main repository for CompText.

## Required files

- `AGENTS.md`
- `README.md`
- `START_HERE.md`
- `CODEX_START_PROMPT.md`
- `docs/COMPTEXT_ARCHITECTURE_v1.md`
- `docs/COMPTEXT_MVP.md`
- `docs/REPOSITORY_STRATEGY.md`
- `docs/CODEX_WORKFLOW.md`
- `docs/COMPTEXT_MVP_TASKS.md`
- `.github/copilot-instructions.md`

## Checks

Run local-only validation where possible:

```bash
python scripts/validate_clean_repo.py .
python scripts/validate_no_secrets.py .
python -m compileall modules apps scripts tests
PYTHONPATH=. pytest -q
```

## Completion criteria

The repository clearly presents CompText as a local AI orchestration platform for software engineering, contains no legacy product-core framing, and points the next step at the local dry-run MVP.
