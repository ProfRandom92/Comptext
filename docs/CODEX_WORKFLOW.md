# COMPTEXT CODEX WORKFLOW

This workflow keeps Codex work on CompText safe, reviewable, and local-dry-run-first.

## 1. Orientation

Read `AGENTS.md`, `README.md`, `START_HERE.md`, `docs/COMPTEXT_MVP.md`, and `docs/COMPTEXT_ARCHITECTURE_v1.md` before changing files.

## 2. Scope selection

Prefer small changes that move the local dry-run MVP forward. Do not begin Gateway, live Provider, MCP runtime, or release work before the dry-run CLI is stable.

## 3. Allowed local checks

Use only non-destructive local checks:

```bash
python scripts/validate_clean_repo.py .
python scripts/validate_no_secrets.py .
python -m compileall modules apps scripts tests
PYTHONPATH=. pytest -q
```

If tests or dependencies are missing, report that exactly. Do not claim unrun checks passed.

## 4. Provider handling

Provider configuration must not contain secrets. Provider states may only be `not_configured`, `disabled`, or `experimental` unless a real healthcheck exists and has been explicitly approved. Do not call provider APIs.

## 5. Evidence handling

Evidence may include redacted metadata, hashes, tool summaries, synthetic test results, and approved diffs. Evidence must not contain secrets, raw environment variables, hidden chain-of-thought, or unredacted provider payloads.

## 6. Change reporting

Every change report should include files changed, checks run, checks not run, known limitations, and the next smallest safe step.
