# CompText PR Review Memory

`comptext-pr-review-memory` is a documentation-first, dry-run-only plugin scaffold for preserving compact pull request review state.

It exists to support the recurring CompText workflow where a PR or local review task is summarized, reviewer comments are captured, actionable comments are fixed, review state is rechecked, merge readiness is summarized, and the next task prompt is prepared. Any actual GitHub write, review-thread resolution, merge, or push remains outside this scaffold and requires explicit approval.

This plugin complements CompText Token Saver by defining compact PR review memory blocks that a token-saving workflow can consume. It does not replace CompText Token Saver and does not assume that an external Token Saver plugin is installed.

## Codex skill bridge

The repo-side bridge at `.agents/skills/pr-review-memory/SKILL.md` makes this scaffold discoverable as static Codex instruction context. Prompts should still start with the personal Token Saver plugin reference:

```text
[@comptext-token-saver](plugin://comptext-token-saver@personal)
```

The bridge connects that token-saving workflow to this scaffold. It does not add GitHub integration, provider calls, MCP runtime behavior, automatic review resolution, auto-merge, or production behavior.

For local autonomous Codex batches, follow `docs/CODEX_LOCAL_AUTONOMY.md` and keep PR Review Memory output compact.

## Renderer v0

`renderer.py` implements deterministic local renderer v0:

```python
from renderer import render_pr_review_memory_handoff

markdown = render_pr_review_memory_handoff(review_memory)
```

The function accepts a dictionary shaped like `examples/pr-review-memory.sample.json` and returns compact Token Saver handoff markdown. It validates required fields, omits empty optional sections, redacts simple secret-like values from rendered text, removes full-diff marker lines, and keeps output stable for tests.

No CLI command is added in v0. Runtime GitHub integration, MCP runtime behavior, automatic review resolution, automatic merge behavior, and production behavior remain deferred.

## Schema v0

`schema/pr-review-memory.v0.schema.json` documents the local renderer input contract used by examples and tests. Required fields are:

- `repository`
- `pr_number`
- `branch`
- `head_sha`
- `validation_summary`
- `next_action`

The schema is intentionally simple and local. It is not live GitHub integration, not MCP runtime behavior, and not provider behavior. Future schema changes require explicit compatibility tests.

## Expected workflow

1. Capture the current PR review state before long work.
2. Summarize only decisions, blockers, file paths, thread state, validation, and next action.
3. Fix actionable comments in the repository workflow.
4. Recheck unresolved threads and validation.
5. Emit a compact handoff block for token-saving context.

## Status and boundaries

- Dry-run-only scaffold.
- Deterministic local renderer v0.
- Local renderer input schema v0.
- No GitHub writes.
- No network calls.
- No provider calls.
- No secrets or raw environment variables.
- No MCP server implementation yet.
- No automatic PR modification.
- No merge behavior.

## Recommended output shape

```markdown
# PR Review Memory

Repository:
PR:
Branch:
Base:
Head SHA:
Review status:
Threads:
Actionable comments:
Fixes applied:
Threads resolved:
Validation:
Merge readiness:
Risks:
Next action:
Token saver summary:
```
