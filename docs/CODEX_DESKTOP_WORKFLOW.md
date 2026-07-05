# Codex Desktop Workflow

This is the baseline workflow for using Codex Desktop with CompText after the local dry-run MVP. It complements `docs/CODEX_WORKFLOW.md` with repository-level branch, review, and token-saving guidance.

This document does not assume Codex Desktop is fully automated. It also does not assume that MCP tools, plugins, RTK, or Codebase Memory are always available in every session.

## Branch Workflow

- `main` is the canonical branch.
- Start every task from the latest `main`.
- Create one branch per task.
- Use these branch name prefixes:
  - `codex/<task>` for Codex-assisted workflow or implementation tasks.
  - `fix/<bug>` for bug fixes.
  - `docs/<topic>` for documentation-only changes.
  - `plugin/<feature>` for plugin or tool integration work.
- Open PRs against `main`.
- Merge PRs with a merge commit unless the user explicitly requests a different strategy.
- Do not push, auto-push, merge, enable auto-merge, or change PR state unless the user explicitly asks.

Recommended start sequence:

```text
fetch latest main -> switch to main -> fast-forward or rebase to origin/main -> create task branch
```

If the local checkout is stale, sync `main` first. Do not branch new work from old task branches, stale local branches, or partially completed review branches.

## Review Handling

When addressing Gemini or other review feedback:

- Inspect all review threads before editing.
- Fix every actionable in-scope comment.
- Resolve every completed review thread after the requested change is made and verified.
- Do not resolve unresolved, ambiguous, blocked, or out-of-scope comments.
- Leave unclear comments open and ask for clarification or summarize the ambiguity.
- Summarize remaining blockers in the PR update or handoff note.

Completed review comments must be resolved. Unresolved comments must remain visible so reviewers can see what still needs a decision.

## CompText Token Saver Plugin

Use the CompText Token Saver plugin when it is available:

- Check compact project state first.
- Use Codebase Memory before broad file reads, architecture searches, call-chain analysis, or repository-wide impact checks.
- Run noisy commands through RTK when available.
- Keep command output summarized in conversation and PR notes.
- Prefer targeted file reads and focused diffs over full-file dumps.

If the plugin, Codebase Memory, MCP tools, or RTK are unavailable, continue with the smallest practical local inspection and mention the fallback.

## PR Readiness

Before opening or updating a PR:

- Confirm the branch is based on the latest practical `main`.
- Confirm the diff contains only intentional files.
- Run relevant checks, or explain why no check is needed.
- Confirm no runtime code changed for documentation-only work.
- Summarize what changed, what stayed out of scope, validation performed, risks, and follow-up.

For documentation-only changes, validation can be limited to reviewing the Markdown, checking links, and confirming that runtime files are unchanged.
