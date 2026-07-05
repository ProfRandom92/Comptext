# comptext-bootstrap

## Name
comptext-bootstrap

## Purpose
Prepare and inspect the CompText repository seed as a local dry-run-first project.

## When to use
Use when checking repository readiness, reading the first-run documents, or confirming the bootstrap baseline.

## Inputs
- Local repository files.
- Bootstrap documentation.
- Local Git status summaries.

## Outputs
- Local readiness notes.
- Documentation gaps.
- Safe next-step recommendations.

## Workflow
1. Read `AGENTS.md`, `README.md`, and `START_HERE.md`.
2. Confirm the branch and working tree state.
3. Check that MVP documentation points to local dry-run commands.
4. Report only local preparation findings.

## Safety rules
- Do not push, merge, release, or create PRs.
- Do not start servers or runtimes.
- Do not read secrets, API keys, tokens, or raw environment variables.
- Keep provider states limited to `not_configured`, `disabled`, or `experimental`.

## Validation checklist
- Product naming uses CompText, comptext, and COMPTEXT consistently.
- Documentation does not claim production readiness.
- Local dry-run commands remain the next safe step.

## Anti-patterns
- Treating bootstrap docs as a release artifact.
- Adding live provider behavior.
- Making production security, compliance, or forensic claims.
