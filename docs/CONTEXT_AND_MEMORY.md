# CompText Context and Memory

CompText should gather compact project state before broad reads. Context is an operating input, not a transcript dump.

## Context order

1. Read compact project state first when available.
2. Use codebase memory before broad file reads.
3. Inspect current git state.
4. Load targeted docs, schemas, files, and recent run evidence.
5. Summarize relevant uncertainty and known failures before execution.

## Context packs

Context packs are bounded bundles of relevant project information for a run or subagent task.

A context pack may include:

- task goal
- workspace path
- relevant files
- policies
- related docs
- recent runs
- git state
- known failures
- user preferences
- evidence references

Context packs should avoid secrets, raw environment variables, hidden chain-of-thought, and unredacted provider payloads.

## Workspace memory

Workspace memory should capture stable project facts:

- product naming
- architecture boundaries
- common commands
- validation expectations
- known constraints
- recurring review feedback

Workspace memory should be concise, updateable, and auditable.

## Recent runs and failures

Recent run data should help agents avoid repeated mistakes. It may include:

- failed commands
- skipped validation
- broken assumptions
- resolved review comments
- unresolved blockers

Store summaries and hashes where possible. Do not store secrets or raw payloads.

## PR review memory

The local [`comptext-pr-review-memory`](../plugins/pr-review-memory/README.md) scaffold defines compact PR review-memory formats for token-saving workflows. It is a companion to CompText Token Saver, not a replacement, and does not assume the external token-saving plugin is installed.

Use [`plugins/pr-review-memory/SKILL.md`](../plugins/pr-review-memory/SKILL.md) when preserving review state before or after long PR work. The memory block should keep only decisions, blockers, file paths, thread state, validation, merge readiness, risks, and next action. It must not perform GitHub actions, make network or provider calls, read secrets, or claim mergeability without a current check.

The repo-side bridge at [`.agents/skills/pr-review-memory/SKILL.md`](../.agents/skills/pr-review-memory/SKILL.md) makes this workflow discoverable to Codex while keeping `[@comptext-token-saver](plugin://comptext-token-saver@personal)` as the first prompt header. The bridge is dry-run/static instruction context only; renderer output generation, runtime GitHub integration, and MCP runtime behavior remain deferred.

## Knowledge graph direction

The long-term direction is a workspace knowledge graph that connects files, functions, types, tests, runs, evidence, docs, decisions, and failures. The graph should improve context selection without replacing explicit approvals or validation.
