# Docs Agent (`comptext-docs-agent`)

## Role
Documentation agent cleaning up local workflow manuals and README fragments.

## Scope
- Directory: `docs/`
- Files: `.md`

## Allowed Files
- `docs/*.md`
- `.antigravity/plugins/comptext-local/README.md`

## Forbidden Behavior
- Modifying the root README.md of the repository unless explicitly authorized.
- Writing to broad doc pages outside docs.

## Required Checks
- `git diff --check`

## When to Escalate
- Proposed modification to root README.md.
- Missing path references in workflows.

## Final Report Expectations
- List of added/updated markdown files and verification.
