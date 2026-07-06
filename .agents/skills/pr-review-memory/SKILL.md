---
name: pr-review-memory
description: Bridge Codex prompts to the dry-run PR Review Memory scaffold for compact Token Saver handoffs.
---

# PR Review Memory

Use this repo-side Codex skill bridge with the personal Token Saver prompt header:

`[@comptext-token-saver](plugin://comptext-token-saver@personal)`

This bridge connects Codex instructions to the scaffold in `plugins/pr-review-memory/`. It can use deterministic local renderer v0 in `plugins/pr-review-memory/renderer.py` when structured review-memory JSON is already available, and the local schema contract in `plugins/pr-review-memory/schema/pr-review-memory.v0.schema.json` documents that input shape. It does not make provider calls, call GitHub APIs, write GitHub state, run an MCP server, resolve review threads, merge branches, or enable auto-merge.

## When to use

- After PR creation.
- When Gemini or review comments appear.
- After actionable comments are fixed.
- Before merge-readiness checks.
- When preparing Token Saver handoff context.

## Compact handoff fields

Preserve only the compact state needed to continue review work:

- Repository.
- PR number.
- Branch.
- Head SHA.
- Review comments.
- Fixes.
- Validation.
- Resolved and unresolved threads.
- Merge readiness.
- Next action.

## Output rules

- Keep output compact.
- Prefer decisions, blockers, file paths, validation results, head SHA, PR URL, and next action.
- Avoid full diffs unless a narrow excerpt is required to explain a blocker.
- Avoid secret values, raw environment variables, hidden chain-of-thought, and provider payloads.
- Avoid unrelated file summaries.
- Avoid broad repo scans.
- Avoid automatic merge claims; only describe merge readiness after checking current state.
- Do not claim production behavior.
- Use renderer v0 only for local dictionary-to-markdown conversion; do not infer missing review state.
- Keep renderer input aligned with schema v0 unless a task explicitly updates the contract and tests.

## Related scaffold files

- `docs/CODEX_LOCAL_AUTONOMY.md`
- `plugins/pr-review-memory/README.md`
- `plugins/pr-review-memory/SKILL.md`
- `plugins/pr-review-memory/plugin.json`
- `plugins/pr-review-memory/renderer.py`
- `plugins/pr-review-memory/schema/pr-review-memory.v0.schema.json`
- `plugins/pr-review-memory/examples/token-saver-handoff.sample.md`
