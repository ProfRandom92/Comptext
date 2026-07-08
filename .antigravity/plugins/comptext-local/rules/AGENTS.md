# Repository Rules (comptext-local)

This file thinly mirrors the root [AGENTS.md](../../../../AGENTS.md) as Antigravity-readable repository rules. All operational rules and boundaries in the root [AGENTS.md](../../../../AGENTS.md) must be strictly followed.

## Project Identity & Status
- **Product Name**: `CompText`
- **Repository, Package, CLI Name**: `comptext`
- **Constants & Titles**: `COMPTEXT`
- **Status**: Local dry-run MVP only. Do not present docs, schemas, contracts, or scaffolding as production-ready.

## Crucial Boundaries & Safety Policy
- **No Network / Provider Calls**: Do not perform live provider calls unless explicitly configured and requested. Keep provider states limited to `not_configured`, `disabled`, or `experimental`.
- **No Secrets / Env Reads**: Do not read `.env` files, read or print environment variables, or read secrets. Never store secrets, API keys, raw environment variables, hidden chain-of-thought, or unredacted provider payloads in logs or Evidence.
- **No GitHub / PR / Push**: Do not auto-push, auto-merge, or create pull requests. Do not call GitHub APIs unless explicitly instructed.
- **No Destructive Actions**: Do not execute destructive commands without explicit approval.
- **No Server/Port Binding**: Do not start servers or bind local ports.

## Development & Branch Policy
- Canonical branch is `main`. New branches must branch from latest `main`.
- Allowed branch prefixes: `codex/<task>`, `fix/<bug>`, `docs/<topic>`, `plugin/<feature>`.
- Review comments: Inspect all review/Gemini threads. Fix comments, and resolve only completed threads.

## Validation & Autonomy
- Validation requires running local tests with `python -m pytest` and check for trailing whitespace/errors using `git diff --check`.
- In autonomous mode: Start with Token Saver/project state first. Only perform local commits.
- Refer to [docs/CODEX_LOCAL_AUTONOMY.md](../../../../docs/CODEX_LOCAL_AUTONOMY.md) for the detailed playbook.
