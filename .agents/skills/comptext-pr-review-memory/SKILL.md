---
name: comptext-pr-review-memory
description: Local checks and markdown rendering for pull request review summaries.
---

# CompText PR Review Memory

Validate review memory schemas and render markdown review handoffs offline.

## Trigger Phrases
- `/comptext-pr-review-memory`
- `check pr review summaries`
- `render review handoffs`

## Purpose
Confirm that compact PR review memory formats parse correctly and can translate to markdown blocks without network or GitHub API access.

## When to Use
- After fixing Gemini or review comments on a branch.
- When preparing handoff tokens.

## Steps
1. Run local plugins tests to verify schema parsing and rendering:
   ```bash
   python -m pytest tests/plugins
   ```
2. Inspect rendered markdown templates for conventional commit messages and resolutions.

## Allowed Local Commands
- `python -m pytest tests/plugins`
- `git diff --check`

## Boundaries
- Local template rendering only.
- Do not interface with GitHub repositories, pull requests, or issue boards.
- Do not make provider API calls.

## Validation Commands
- `python -m pytest tests/plugins`

## Expected Final Report Shape
- Compact markdown review handoff summarization block.
