# Private CompText Context MCP Design

## Status

Approved autonomous design for a Windows-first MVP. The first client is Codex Desktop through local `stdio`. The architecture must remain transport-neutral so a later OpenAI Secure MCP Tunnel adapter can expose the same server without changing core services.

## Objective

Build a private, local-first MCP server that lets high-reasoning Codex models work longer by reducing avoidable context, tool-output, repository-reading, and session-handover tokens without weakening correctness.

The target is not a usage-limit bypass. The target is measurable net token reduction while preserving task success and verification quality.

## Success criteria

1. The server runs locally on Windows through `stdio` and is usable by Codex Desktop.
2. It exposes no more than eight public MCP tools.
3. Raw command output and full files stay local unless explicitly expanded.
4. Test, build, lint, Git, search, and directory output are deterministically compacted.
5. Repository context is selected under an explicit token budget.
6. Decisions, constraints, verification state, and open work survive across sessions in compact local memory.
7. Every tool call records estimated raw tokens, returned tokens, reduction percentage, detail expansions, duration, and outcome.
8. A benchmark compares baseline Codex workflows with MCP-assisted workflows.
9. The MVP must demonstrate at least 50% median reduction in tool/context input on the benchmark corpus with no lower task success rate.
10. No secrets, unrestricted shell, automatic push, deployment, destructive command, or network provider call is enabled by default.

## Repository strategy

`ProfRandom92/Comptext` remains the canonical repository and runtime.

`ProfRandom92/comptext-codex` is treated as a source for a small deterministic protocol library, not as the MCP runtime. The useful protocol elements are command identifiers, batch-plan representation, deterministic parsing, and compact metrics. They should be ported into a focused package in the main repository after licensing and compatibility checks.

The existing CompText run, evidence, memory, safety, and knowledge-graph concepts remain authoritative. The new MCP integrates with those boundaries rather than creating a parallel orchestration platform.

## Selected approach

### Recommended architecture: bounded context gateway

The MCP server is an adapter over independent local services:

```text
Codex Desktop
    |
    | MCP stdio
    v
CompText MCP Adapter
    |
    +-- Context Service
    |     +-- project map
    |     +-- lexical search
    |     +-- symbol extraction
    |     +-- token-budget packet builder
    |
    +-- Compact Execution Service
    |     +-- allowlisted command runner
    |     +-- command-family parsers
    |     +-- retained raw-result store
    |
    +-- Memory Service
    |     +-- compact project facts
    |     +-- decisions and constraints
    |     +-- verification and blockers
    |
    +-- Evidence and Metrics
          +-- execution records
          +-- token estimates
          +-- expansion accounting
          +-- benchmark reports
```

This approach is preferred over a transparent shell proxy because it provides explicit security and stable output contracts. It is preferred over an LLM-based summarizer because deterministic filtering is cheaper, reproducible, and less likely to remove critical details.

## Public MCP tools

The MVP exposes exactly eight tools.

### `context_prepare`

Builds a task-specific, token-budgeted context packet. It combines project structure, lexical/symbol matches, relevant tests, current Git changes, and compact memory.

Inputs:

- `task: string`
- `workspace: string | null`
- `token_budget: integer` with default 6000 and range 1000-20000
- `include_diff: boolean` default true
- `include_memory: boolean` default true

Output includes summary, ranked excerpts, relevant paths, known constraints, omitted-item counts, estimated tokens, and an opaque `result_id`.

### `code_search`

Performs bounded local lexical and symbol search. It returns ranked matches with path, line range, symbol, reason, and estimated token cost. It never returns entire files by default.

### `code_read`

Reads exact line ranges with configurable surrounding context and optional import/type inclusion. Workspace-root containment is mandatory.

### `run_compact`

Executes only an allowlisted command family. The request identifies the command family and arguments separately; arbitrary shell strings are rejected. Raw output is retained locally and only compact structured output is returned.

Initial families:

- `pytest`
- `npm_test`
- `npm_build`
- `npm_typecheck`
- `npm_lint`
- `git_status`
- `git_diff`
- `git_log`
- `rg`
- `directory_tree`

### `git_compact`

Provides compact status, diff, and recent-history views without requiring unrestricted shell execution. Diffs are grouped by file and hunk with binary, generated, and lockfile summaries.

### `memory_recall`

Returns only memory records relevant to the current task, ranked by project, path, tags, and recency. The output is budgeted and excludes conversational prose.

### `memory_commit`

Stores structured decisions, constraints, completed verification, blockers, and next actions. It rejects secrets and oversized free-form text.

### `result_expand`

Expands a prior result by opaque `result_id`, section, and optional line/range selector. This implements progressive disclosure while keeping first responses small.

## Internal modules

### MCP adapter

Responsible only for transport, schemas, error translation, and service invocation. It contains no search, execution, memory, or parsing logic.

### Workspace policy

Resolves named workspaces to approved roots. Canonicalizes paths and rejects traversal, symlink escape, UNC escape, and access outside configured roots.

### Token estimator

Uses a pluggable estimator. The MVP may use `tiktoken` when installed and a deterministic character-based fallback. Every metric records which estimator was used.

### Context index

MVP indexing uses local filesystem metadata, Ripgrep-compatible lexical search, lightweight Python/TypeScript symbol extraction, and SQLite FTS5. Embeddings are explicitly deferred until lexical and symbol retrieval benchmarks show a measurable gap.

### Compact execution

Runs subprocesses without a shell, with fixed executable mapping, argument validation, timeout, maximum captured bytes, environment allowlist, and secret redaction.

### Parser registry

Each command family has a deterministic parser implementing:

- `supports(invocation)`
- `parse(stdout, stderr, exit_code)`
- `render_compact(parsed, budget)`
- `priority_sections(parsed)`

Unknown output falls back to bounded head/tail plus error-pattern extraction; it is never silently discarded.

### Raw-result store

Raw outputs and full search/read results are retained in a local bounded cache keyed by opaque IDs. Records expire by age and total disk quota. The MCP never exposes filesystem cache paths.

### Memory store

SQLite stores structured records:

- project
- kind: decision, constraint, verification, blocker, next_action, fact
- subject
- value
- paths
- tags
- source run
- created and updated timestamps
- supersedes relation

Memory is append-oriented with explicit supersession rather than silent rewriting.

### Evidence and metrics

Each tool call records request class, workspace, duration, success, raw bytes/tokens, returned bytes/tokens, reduction, parser used, result expansions, and error category. Command text and environment values are redacted according to policy.

## CompText protocol usage

The compact protocol from `comptext-codex` is used only internally for deterministic run plans, memory tags, evidence event classes, and agent-to-agent handoffs. Human task requirements and exact technical constraints remain ordinary structured text.

The protocol must not add encode/decode MCP round trips. Its value is compact persistence and stable identifiers, not transforming every user prompt into single-character syntax.

## Data flow

1. Codex calls `context_prepare` with a task and budget.
2. Workspace policy resolves and validates the root.
3. Context service loads compact memory, Git state, project map, lexical/symbol candidates, and related tests.
4. Ranker allocates the token budget by section priority.
5. The packet and omitted candidates are stored under `result_id`.
6. Codex reads or executes only what is necessary.
7. Compact execution parses output and retains raw data locally.
8. Codex may request precise expansion through `result_expand`.
9. Important decisions and verification state are saved with `memory_commit`.
10. Evidence and metrics produce an auditable token-efficiency record.

## Ranking and budgeting

Context ranking is deterministic in the MVP. Score components:

- exact task-term match
- symbol-name match
- path proximity to current diff
- direct import/reference relation
- test-to-source relation
- memory path/tag match
- recency as a weak tie-breaker

Default budget allocation:

- 10% task and project summary
- 45% source excerpts
- 20% related tests
- 10% Git diff/status
- 10% memory
- 5% reserve and truncation notices

Unused allocation can flow to higher-ranked source excerpts. Exact errors, file paths, line numbers, identifiers, commands, and constraints are never paraphrased.

## Output policy

Compact results use structured JSON-compatible fields and short Markdown only where it improves readability. They avoid greetings, repeated task descriptions, success narration, and generic advice.

Every truncated response states what was omitted and how to expand it. A compact response must never imply that omitted output was successful or irrelevant.

## Error handling

Errors use stable categories:

- `workspace_not_allowed`
- `path_outside_workspace`
- `command_not_allowed`
- `invalid_arguments`
- `timeout`
- `output_limit_exceeded`
- `parser_failed`
- `result_expired`
- `index_unavailable`
- `memory_validation_failed`
- `internal_error`

Parser failure returns a safe bounded fallback and marks the result degraded. It does not convert a command failure into success.

## Security model

- Local `stdio` only for MVP.
- No listening socket.
- No shell execution.
- Explicit workspace-root allowlist.
- Explicit executable and subcommand allowlist.
- Read operations are default.
- Destructive Git, package publishing, deployments, file deletion, and network tools are out of scope.
- Child-process environment is minimal and allowlisted.
- Secret patterns are redacted before persistence and response.
- `.env`, credential stores, SSH material, browser profiles, and system directories are denied by default.
- Raw-result cache has configurable age and disk limits.
- Secure MCP Tunnel support is a later transport adapter and must preserve all local policies.

## Testing strategy

### Unit tests

- path containment and symlink escape
- command argument validation
- parser fixtures for success, failure, warnings, repeated errors, malformed output, and Unicode
- token-budget allocation
- context ranking
- redaction
- memory validation and supersession
- result expiry and expansion

### Contract tests

Each MCP tool is tested against fixed request and response schemas. Error responses are tested for stable categories and absence of raw secrets or internal paths.

### Integration tests

Temporary repositories exercise:

- Python project with pytest failures
- TypeScript project with lint/typecheck/build failures
- Git status and multi-file diffs
- large logs and repeated errors
- code search and related-test selection
- memory across two sessions

### Benchmark

A fixed corpus contains at least 20 engineering tasks across Python and TypeScript. Each task runs in two modes:

1. baseline tools and raw output
2. CompText Context MCP

Metrics:

- task completion and verification success
- total tool/context tokens
- model output tokens when available
- number of tool calls
- number of expansions
- wall-clock duration
- false omission incidents

Release threshold: at least 50% median reduction in tool/context tokens, no reduction in successful task completion, and zero high-severity omission incidents.

## Delivery phases

### Phase 1: contracts and safety foundation

Schemas, workspace policy, command registry, token estimator, result store, evidence metrics, and MCP server skeleton.

### Phase 2: RTK-style compact execution

Parsers for Git, pytest, npm build/test/typecheck/lint, Ripgrep, and directory trees with progressive expansion.

### Phase 3: selective repository context

Project mapping, lexical search, Python/TypeScript symbol extraction, related-test heuristics, ranker, and `context_prepare`.

### Phase 4: compact memory

SQLite memory records, validation, supersession, task relevance, and session handoff.

### Phase 5: benchmarking and Codex integration

Codex Desktop configuration, AGENTS policy, benchmark runner, reports, installation scripts, and documentation.

### Phase 6: hardening and future transport

Only after MVP acceptance: Secure MCP Tunnel adapter, optional HTTP transport, more languages, optional embeddings, and richer TUI metrics.

## Explicit non-goals for MVP

- Bypassing OpenAI limits or account controls
- Routing model/provider requests
- Replacing Codex reasoning
- General autonomous shell access
- Editing files through MCP
- Git push, PR, merge, deployment, or publishing
- Cloud-hosted memory
- Semantic embeddings
- Multi-agent scheduling
- A graphical desktop application

## Design self-review

- No unresolved placeholders remain.
- The MVP is one coherent subsystem: a local context and compact-execution MCP.
- Transport, execution, retrieval, memory, evidence, and security boundaries are explicit.
- Token-reduction claims are benchmark gates rather than guarantees.
- `Comptext` remains canonical; `comptext-codex` is not duplicated as a second runtime.
