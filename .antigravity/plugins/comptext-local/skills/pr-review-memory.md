---
name: pr-review-memory-bridge
description: Bridge for local deterministic PR review-memory rendering in CompText.
---

# PR Review Memory Bridge

This skill bridges the repository's existing PR Review Memory companion scaffold for Antigravity-aware workflows.

## Key References

- Root Skill Bridge: [.agents/skills/pr-review-memory/SKILL.md](../../../../.agents/skills/pr-review-memory/SKILL.md)
- Plugin Directory: [plugins/pr-review-memory/](../../../../plugins/pr-review-memory/)
- Renderer Implementation: [plugins/pr-review-memory/renderer.py](../../../../plugins/pr-review-memory/renderer.py)
- Schema Definitions: [plugins/pr-review-memory/schema/](../../../../plugins/pr-review-memory/schema/)
- Examples & Fixtures: [plugins/pr-review-memory/examples/](../../../../plugins/pr-review-memory/examples/)

## Scope and Boundaries

- **Local Deterministic Renderer Only**: The bridge must only use the local renderer in `plugins/pr-review-memory/renderer.py` to parse JSON review records and generate markdown handoffs.
- **No Live GitHub / Network Actions**: Do not connect to or call the GitHub API. Do not fetch comments or PR state over the network.
- **No Auto Review Resolution**: Unresolved comments and review threads must not be automatically resolved. They require manual checking and verification.
- **No Auto Merge**: Do not attempt to merge or approve PRs automatically.
- **No MCP Runtime**: This skill acts as documentation and static guide bridge; it does not deploy or spin up an MCP runtime server.
