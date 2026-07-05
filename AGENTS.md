# AGENTS.md

Operational instructions for agents working in this repository.

## Project identity

CompText is a local AI orchestration platform for software engineering.

Use these names consistently:

- Product name: `CompText`
- Repository, package, and CLI name: `comptext`
- Constants and document titles: `COMPTEXT`

## Current status

This repository is local dry-run MVP only. Do not present docs, schemas, contracts, or scaffolding as production-ready features.

## Branch policy

`main` is canonical. New work branches from latest `main`.

Branch prefixes:

- `codex/<task>`
- `fix/<bug>`
- `docs/<topic>`
- `plugin/<feature>`

## Review policy

- Inspect all review and Gemini threads.
- Fix actionable comments.
- Resolve every completed thread.
- Do not resolve ambiguous, unfixed, or out-of-scope comments.

## Safety policy

- Do not perform provider calls unless explicitly configured and requested.
- Do not store secrets, API keys, raw environment variables, hidden chain-of-thought, or unredacted provider payloads in Evidence or logs.
- Do not execute destructive commands without explicit approval.
- Do not auto-push or auto-merge unless the user explicitly asks.
- Do not create pull requests, merge, or release unless repository policy is explicitly changed.

## Validation policy

- Run relevant local tests or checks for the changed surface.
- Documentation-only PRs may use markdown checks and `git diff --check`.
- Keep provider states limited to `not_configured`, `disabled`, or `experimental`.

## Navigation

- Codex Desktop workflow: [`docs/CODEX_DESKTOP_WORKFLOW.md`](docs/CODEX_DESKTOP_WORKFLOW.md)
- Codex Desktop prompts: [`docs/CODEX_DESKTOP_PROMPTS.md`](docs/CODEX_DESKTOP_PROMPTS.md)
- Architecture: [`docs/COMPTEXT_ARCHITECTURE_v1.md`](docs/COMPTEXT_ARCHITECTURE_v1.md)
- Security: [`docs/COMPTEXT_SECURITY.md`](docs/COMPTEXT_SECURITY.md)
- MVP tasks: [`docs/COMPTEXT_MVP_TASKS.md`](docs/COMPTEXT_MVP_TASKS.md)
