---
name: comptext-pr-review-memory
description: Preserve compact PR review memory for dry-run CompText token-saving workflows.
---

# CompText PR Review Memory

## Purpose

Use this skill to emit compact PR review memory blocks for recurring review workflows. The output is meant to be consumed by token-saving context workflows, including CompText Token Saver when available, without duplicating that plugin.

For local autonomous Codex batches, also follow `docs/CODEX_LOCAL_AUTONOMY.md`.

## When to use

- Before long PR review work, summarize the current review state.
- After fixing review comments, summarize what changed and what remains.
- Before merge-readiness checks, preserve known blockers and validation status.
- Before preparing the next task prompt, create a compact handoff block.

## Inputs

- Repository name.
- PR number or local PR identifier.
- Branch, base branch, and head SHA when known.
- Review threads and thread state.
- Actionable comments and decisions.
- File paths touched by fixes.
- Validation commands and results.
- Mergeability or merge-readiness evidence.

## Outputs

- PR review memory summary.
- Gemini or reviewer comment summary.
- Merge-readiness summary.
- Token Saver handoff block.
- Deterministic local renderer v0 output from `plugins/pr-review-memory/renderer.py` when structured review-memory JSON is available.
- Renderer input schema v0 contract from `plugins/pr-review-memory/schema/pr-review-memory.v0.schema.json`.

Keep output compact. Preserve only decisions, blockers, file paths, thread state, validation, and next action.

## Required checks

- Summarize review state before long work.
- Confirm whether review threads are resolved, unresolved, or out of scope.
- Confirm validation status with concrete commands or note that validation was not run.
- Confirm merge readiness only after checking the current branch, base, and review state.
- Use `render_pr_review_memory_handoff(data)` for local conversion when the review memory is already structured as a dictionary.
- Keep structured renderer input aligned with the v0 schema contract and add compatibility tests before changing required fields.
- Keep provider states and external integrations limited to documented dry-run behavior.

## Safety notes

- No network calls.
- No GitHub API calls.
- No provider calls.
- No environment-variable reads.
- No secrets, API keys, raw provider payloads, or hidden chain-of-thought.
- No MCP runtime server behavior.
- No automatic PR modification.
- No merge behavior.
- No live GitHub integration or automatic review-thread resolution.

## Anti-patterns

- Do not duplicate full diffs unless a narrow excerpt is needed to understand a blocker.
- Do not dump full review transcripts when a compact decision summary is enough.
- Do not mark unresolved work as resolved.
- Do not claim mergeability without checking.
- Do not assume CompText Token Saver is installed.
- Do not present this scaffold as production-ready.
- Do not treat renderer output as proof that review threads are resolved or that a PR is mergeable.

## Related docs

- [Plugin README](README.md)
- [Codex Local Autonomy](../../docs/CODEX_LOCAL_AUTONOMY.md)
- [CompText Plugin System](../../docs/PLUGIN_SYSTEM.md)
- [CompText Context and Memory](../../docs/CONTEXT_AND_MEMORY.md)
- [Codex Desktop Workflow](../../docs/CODEX_DESKTOP_WORKFLOW.md)
