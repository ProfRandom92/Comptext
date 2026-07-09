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

## Mandatory Skill-First Workflow

For every non-trivial local development task, the agent MUST use the available Comptext workspace skills before planning or editing.

Required behavior:
- Open or inspect `/skills` or the corresponding `.agents/skills/` files.
- Select the relevant Comptext skills for the task.
- Do not merely list skill names.
- Extract the actionable workflow rules from each selected skill.
- Incorporate those rules into the implementation plan.
- Map each selected skill to:
  - concrete action
  - validation command
  - safety boundary
  - expected artifact or report output

Default required skills for local autonomous development:
- `comptext-local-autonomy`
- `comptext-local-verify`
- `comptext-workspace-validation`
- `comptext-status`
- `workspace-state`

Before implementation, produce a Skill-Grounded Plan containing:

| Skill | Applied rule | Concrete action | Validation command | Safety impact |
| ----- | ------------ | --------------- | ------------------ | ------------- |

The agent MUST stop and report if:
- required skills are missing
- skills conflict with `AGENTS.md`
- a selected skill would require network/provider/secret/MCP/hook activity not explicitly approved
- the task cannot be mapped to concrete validation commands

This skill-first rule applies before:
- creating branches
- editing files
- implementing features
- running broad searches
- committing changes

Hard boundary:
Browsing `/skills` is not sufficient. A skill only counts as used when its rules are extracted and applied to the plan.

## Codex local autonomous mode

- Use local autonomous mode only when explicitly requested.
- Start with Token Saver/project state before broad repo reads.
- Do not push, open PRs, merge, enable auto-merge, call GitHub APIs, perform provider calls, or read secrets unless explicitly instructed.
- If local `main` is stale, stop and ask before `git fetch`.
- Local commits are allowed in autonomous mode.
- Required validation is `python -m pytest` and `git diff --check`.
- Keep final reports compact: branch, local commit SHA, changed files, validation, blockers, and next action.
- Detailed playbook: [`docs/CODEX_LOCAL_AUTONOMY.md`](docs/CODEX_LOCAL_AUTONOMY.md).

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
