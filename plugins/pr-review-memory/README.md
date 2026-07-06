# CompText PR Review Memory

`comptext-pr-review-memory` is a documentation-first, dry-run-only plugin scaffold for preserving compact pull request review state.

It exists to support the recurring CompText workflow where a PR is opened, Gemini or reviewer comments are found, actionable comments are fixed, review threads are resolved, merge readiness is checked, the work is merged to `main`, and the next task prompt is prepared.

This plugin complements CompText Token Saver by defining compact PR review memory blocks that a token-saving workflow can consume. It does not replace CompText Token Saver and does not assume that an external Token Saver plugin is installed.

## Codex skill bridge

The repo-side bridge at `.agents/skills/pr-review-memory/SKILL.md` makes this scaffold discoverable as static Codex instruction context. Prompts should still start with the personal Token Saver plugin reference:

```text
[@comptext-token-saver](plugin://comptext-token-saver@personal)
```

The bridge connects that token-saving workflow to this scaffold. It does not add runtime behavior, GitHub integration, provider calls, MCP runtime behavior, automatic review resolution, auto-merge, or production behavior. A renderer that converts review-memory JSON into handoff markdown remains deferred.

## Expected workflow

1. Capture the current PR review state before long work.
2. Summarize only decisions, blockers, file paths, thread state, validation, and next action.
3. Fix actionable comments in the repository workflow.
4. Recheck unresolved threads and validation.
5. Emit a compact handoff block for token-saving context.

## Status and boundaries

- Dry-run-only scaffold.
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
