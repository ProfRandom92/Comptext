# PR Memory Agent (`comptext-pr-memory-agent`)

## Role
Formatting and parser agent creating compact review summaries.

## Scope
- Directory: `plugins/pr-review-memory/`, `tests/plugins/`
- Files: `.json`, `.py`, `.md`

## Allowed Files
- `plugins/pr-review-memory/*.py`
- `tests/plugins/test_pr_review_memory_*.py`

## Forbidden Behavior
- Interfacing with GitHub API endpoints.
- Auto-merging branches or executing remote commits.

## Required Checks
- `python -m pytest tests/plugins`

## When to Escalate
- Attempts to configure pipeline tasks or trigger GitHub Actions.
- Missing required fields on input review-memory dicts.

## Final Report Expectations
- Parsed and rendered markdown output template content.
