---
name: repo-hygiene
description: Clean stale local paths, align metadata, and verify gitignore.
---

# Repository Hygiene Skill

Maintain clean repository metadata and verify that absolute/private paths are not committed.

## Use when
- Cleaning stale local/private absolute paths (such as `C:\Users\...\` or `file:///C:/...`).
- Aligning public-facing package metadata in `pyproject.toml` (version, description, keywords).
- Verifying `.gitignore` patterns to prevent caching issues.
- Ensuring wording consistency across `README.md`, `START_HERE.md`, and `CONTRIBUTING.md`.

## Do not use when
- Adding new runtime code features or CLI commands.
- Modifying GitHub Actions CI workflows.
- Editing evidence-chain schemas or verification logic.
- Automating hosted release packaging or public package publishing.

## Inputs
- Project documentation files: `README.md`, `START_HERE.md`, `CONTRIBUTING.md`.
- Project configuration: `pyproject.toml`, `.gitignore`.

## Safety boundaries
- Bounded to repository metadata and documentation.
- No LLM provider calls or routing.
- No network connections or GitHub API calls.
- No secrets or environment-variable access.
- No live MCP runtime, push, PR creation, or branch merging.

## Workflow
1. Scan repository files for absolute system paths or machine-specific environment variables.
2. Replace machine-specific references with relative paths or generic placeholders (e.g. `<repo-root>`).
3. Inspect `pyproject.toml` parameters to confirm the version matches the current local developer preview status.
4. Check that cached Python binaries and logs are correctly ignored by `.gitignore`.

## Validation
- `comptext status --dry-run`
- `comptext doctor --dry-run`
- `git diff --check`

## Final report
- Summary of files scanned, details of metadata/version modifications, list of generalized paths, and formatting validation results.
