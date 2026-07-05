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

## Knowledge graph direction

The long-term direction is a workspace knowledge graph that connects files, functions, types, tests, runs, evidence, docs, decisions, and failures. The graph should improve context selection without replacing explicit approvals or validation.
