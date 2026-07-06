# Codex Local Autonomy

Local playbook for explicitly requested Codex autonomous batches in CompText.

## Purpose

Provide durable local rules for longer Codex work without turning `AGENTS.md` into a large prompt. This playbook governs local planning, edits, validation, and handoff reports only.

## When to use

Use this playbook only when the user explicitly requests local autonomous mode, an autonomous batch, or similar local Codex execution. Ordinary interactive work continues to follow `AGENTS.md`.

## Required first step

Start with CompText Token Saver/project state. Load compact repository state before broad reads, then use Codebase Memory before opening noisy files or scanning large surfaces.

If the requested base is `main`, confirm local `main` is current before editing. If it is stale, stop and ask before running `git fetch`.

## Allowed local actions

- Read and edit repository files needed for the requested task.
- Create local branches from synced `main`.
- Run local tests, format checks, and documentation checks.
- Make local commits when requested by the autonomous task.
- Summarize decisions, blockers, file paths, validation results, local commit SHAs, and next actions.

## Forbidden actions

- Do not push.
- Do not open pull requests.
- Do not merge branches.
- Do not enable auto-merge.
- Do not call GitHub APIs.
- Do not perform provider calls.
- Do not read secrets or raw environment variables unless explicitly required.
- Do not run MCP runtime behavior.
- Do not resolve review threads automatically.
- Do not make production, security, compliance, legal, forensic, or official compatibility claims.

## Stop conditions

Stop and ask before continuing when:

- Local `main` is stale and syncing was not explicitly approved.
- A network action is needed.
- A destructive command is needed.
- The task requires provider, GitHub API, MCP runtime, or secret access.
- The requested work conflicts with existing local changes.
- Validation reveals a failure outside the requested scope.

## Commit policy

Use one local commit per autonomous batch unless the user asks otherwise. Keep the commit scoped to the requested task. Do not push the commit.

Before committing, confirm the branch, inspect the changed files, and run required validation.

## Validation policy

Required validation for autonomous batches:

```bash
python -m pytest
git diff --check
```

For documentation-only batches, also run available markdown checks when present. If markdownlint is unavailable, report that plainly.

## Default PR Review Memory local work queue

When the batch is related to review memory or review follow-up, keep a compact local queue:

1. Capture repository, branch, head SHA, PR number or local task name, validation, blockers, and next action.
2. Inspect review and Gemini context only when provided locally or explicitly authorized.
3. Fix actionable local comments.
4. Leave ambiguous, unfixed, or out-of-scope comments unresolved.
5. Use the PR Review Memory scaffold only for compact local handoff formatting.

## Final report format

End each autonomous batch with:

- Branch name.
- Local commit SHA, when a commit was made.
- Changed files.
- Validation result.
- Confirmation that nothing was pushed.
- Next recommended local task.

## Evening GitHub update rule

Do not perform evening GitHub updates automatically. If the user asks for one, prepare a compact local summary first and wait for explicit approval before any network, GitHub API, push, PR, merge, or auto-merge action.
