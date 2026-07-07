---
name: comptext-pr-review-memory
description: Local rendering and schema checks for PR review memory.
---

# CompText PR Review Memory Skill

Use this skill to validate that review memory payloads match expectations and can render to Markdown review summaries offline.

## Trigger Phrases
- `/comptext-pr-review-memory`
- `verify pr review memory`
- `render review summaries`

## Input
- Review memory JSON files and renderer templates.

## Steps
1. Execute tests for PR review memory parsing and rendering:
   ```bash
   python -m pytest tests/plugins/test_pr_review_memory_renderer.py
   ```
2. Confirm all templates render compact markdown blocks without error.

## Validation Commands
- `python -m pytest tests/plugins`

## Boundaries
- No GitHub writes.
- No live pull request merges or branch pushes.

## Expected Output Shape
- Pass result from review template validation tests.
