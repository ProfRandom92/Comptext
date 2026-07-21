# Private CompText Context MCP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Windows-first private local MCP server that reduces avoidable Codex context and tool-output tokens through deterministic compaction, selective repository retrieval, compact memory, progressive disclosure, and measurable evidence.

**Architecture:** Add a transport-thin MCP adapter over isolated local services for workspace policy, compact command execution, repository context retrieval, memory, result expansion, and metrics. `ProfRandom92/Comptext` remains the runtime; selected deterministic protocol concepts from `comptext-codex` are ported only as an internal library.

**Tech Stack:** Python 3.10+, `mcp`, Pydantic v2, SQLite/FTS5, `tiktoken` optional, pytest, Ruff, mypy, standard-library subprocess/pathlib/sqlite3, Codex Desktop MCP `stdio` configuration.

## Global Constraints

- MVP transport is local `stdio`; do not open a listening socket.
- The public MCP surface is limited to exactly eight tools: `context_prepare`, `code_search`, `code_read`, `run_compact`, `git_compact`, `memory_recall`, `memory_commit`, and `result_expand`.
- No arbitrary shell strings; subprocesses use executable and argument arrays with `shell=False`.
- All paths are contained under explicitly configured workspace roots.
- No provider routing, API-key reads, deployment, Git push, PR creation, publishing, file deletion, or destructive command execution.
- Raw output remains local and is exposed only through bounded `result_expand` requests.
- Exact errors, paths, line numbers, identifiers, commands, and constraints are preserved.
- Every tool call records raw/returned token estimates, reduction, duration, parser, expansions, and outcome.
- Release benchmark requires at least 50% median tool/context token reduction, no lower task-success rate, and zero high-severity omission incidents.
- Implement using TDD and commit after every independently testable task.

---

## Planned File Structure

```text
src/comptext/
  mcp/
    __init__.py
    server.py                 # MCP transport and eight tool registrations only
    schemas.py                # Public request/response Pydantic contracts
    errors.py                 # Stable public error categories
  context/
    __init__.py
    project_map.py            # Bounded project inventory and ignore rules
    search.py                 # Lexical/FTS search and ranked matches
    symbols.py                # Python/TypeScript lightweight symbol extraction
    ranker.py                 # Deterministic relevance and token allocation
    packets.py                # context_prepare orchestration
  execution/
    __init__.py
    policy.py                 # Allowed executable/subcommand/argument contracts
    runner.py                 # shell=False subprocess runner and limits
    parsers/
      __init__.py
      base.py                 # Parser protocol and compact result model
      fallback.py             # Safe bounded fallback
      git.py                  # status/diff/log compaction
      pytest.py               # pytest result compaction
      npm.py                  # test/build/typecheck/lint compaction
      search.py               # rg/tree compaction
  memory/
    __init__.py
    models.py                 # Structured memory records
    store.py                  # SQLite persistence and supersession
    retrieval.py              # Task-relevant budgeted recall
  protocol/
    __init__.py
    codes.py                  # Internal compact identifiers ported from comptext-codex
    plans.py                  # Deterministic compact run-plan serialization
  safety/
    workspace.py              # Root resolution, canonicalization, escape prevention
    redaction.py              # Secret/path redaction
  telemetry/
    tokens.py                 # Token estimator abstraction
    results.py                # Raw-result cache and progressive disclosure
    evidence.py               # Tool-call metrics and JSONL/SQLite records
  cli/
    mcp.py                    # `comptext mcp serve --stdio`

config/
  mcp.example.toml            # Safe example workspace and limits
schemas/
  mcp-tool-call.v0.schema.json
  mcp-memory-record.v0.schema.json
  mcp-evidence.v0.schema.json

tests/
  mcp/
  context/
  execution/
    fixtures/
  memory/
  safety/
  telemetry/
  integration/
  benchmark/

benchmarks/private-context-mcp/
  corpus.json
  run_benchmark.py
  README.md

docs/
  PRIVATE_CONTEXT_MCP.md
  CODEX_DESKTOP_MCP_SETUP.md
  SECURITY_PRIVATE_CONTEXT_MCP.md
```

---

### Task 1: Establish MCP contracts, dependencies, and error model

**Files:**
- Modify: `pyproject.toml`
- Create: `src/comptext/mcp/__init__.py`
- Create: `src/comptext/mcp/schemas.py`
- Create: `src/comptext/mcp/errors.py`
- Create: `schemas/mcp-tool-call.v0.schema.json`
- Create: `tests/mcp/test_schemas.py`
- Create: `tests/mcp/test_errors.py`

**Interfaces:**
- Produces: `ToolErrorCode`, `ToolFailure`, `ResultEnvelope[T]`, and input/output models for all eight public tools.
- Consumes: existing project packaging and schema-validation conventions.

- [ ] **Step 1: Add the minimum runtime dependencies**

Add optional dependency group and entry point without enabling network behavior:

```toml
[project.optional-dependencies]
mcp = [
  "mcp>=1.9,<2",
  "pydantic>=2.7,<3",
  "tomli-w>=1.0,<2; python_version < '3.11'",
]

[project.scripts]
comptext = "comptext.cli:main"
comptext-mcp = "comptext.cli.mcp:main"
```

Preserve existing dependencies and scripts; merge rather than replace existing tables.

- [ ] **Step 2: Write failing schema tests**

```python
from pydantic import ValidationError
from comptext.mcp.schemas import ContextPrepareRequest, MemoryCommitRequest


def test_context_budget_bounds() -> None:
    assert ContextPrepareRequest(task="fix tests", token_budget=6000).token_budget == 6000
    for invalid in (999, 20001):
        try:
            ContextPrepareRequest(task="fix tests", token_budget=invalid)
        except ValidationError:
            pass
        else:
            raise AssertionError("invalid token budget accepted")


def test_memory_rejects_unbounded_prose() -> None:
    try:
        MemoryCommitRequest(
            workspace="demo",
            kind="decision",
            subject="storage",
            value="x" * 4001,
        )
    except ValidationError:
        return
    raise AssertionError("oversized memory value accepted")
```

Run: `python -m pytest tests/mcp/test_schemas.py -v`

Expected: FAIL because `comptext.mcp.schemas` does not exist.

- [ ] **Step 3: Implement public models and stable errors**

Define:

```python
from enum import StrEnum

class ToolErrorCode(StrEnum):
    WORKSPACE_NOT_ALLOWED = "workspace_not_allowed"
    PATH_OUTSIDE_WORKSPACE = "path_outside_workspace"
    COMMAND_NOT_ALLOWED = "command_not_allowed"
    INVALID_ARGUMENTS = "invalid_arguments"
    TIMEOUT = "timeout"
    OUTPUT_LIMIT_EXCEEDED = "output_limit_exceeded"
    PARSER_FAILED = "parser_failed"
    RESULT_EXPIRED = "result_expired"
    INDEX_UNAVAILABLE = "index_unavailable"
    MEMORY_VALIDATION_FAILED = "memory_validation_failed"
    INTERNAL_ERROR = "internal_error"
```

Use strict Pydantic models with `extra="forbid"`. Define every public request and response named in the design. `ContextPrepareRequest.token_budget` is `Field(default=6000, ge=1000, le=20000)`. `MemoryCommitRequest.value` is limited to 4000 characters and its list fields are capped at 50 entries.

- [ ] **Step 4: Export JSON schema and test it**

Generate `schemas/mcp-tool-call.v0.schema.json` from a discriminated union of the eight request models. The test loads the checked-in JSON and asserts it equals `model_json_schema()` after canonical key sorting.

Run: `python -m pytest tests/mcp/test_schemas.py tests/mcp/test_errors.py -v`

Expected: PASS.

- [ ] **Step 5: Run project validation**

Run:

```bash
python -m pytest
python -m ruff check src tests
python -m mypy src/comptext
```

Expected: all configured checks pass. When Ruff or mypy is not configured in the repository, add only the minimal configuration needed for new files and document the exact version.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/comptext/mcp schemas/mcp-tool-call.v0.schema.json tests/mcp
git commit -m "feat(mcp): define private context tool contracts"
```

---

### Task 2: Implement workspace containment, redaction, token estimates, and result cache

**Files:**
- Create: `src/comptext/safety/workspace.py`
- Create: `src/comptext/safety/redaction.py`
- Create: `src/comptext/telemetry/tokens.py`
- Create: `src/comptext/telemetry/results.py`
- Create: `config/mcp.example.toml`
- Create: `tests/safety/test_workspace.py`
- Create: `tests/safety/test_redaction.py`
- Create: `tests/telemetry/test_tokens.py`
- Create: `tests/telemetry/test_results.py`

**Interfaces:**
- Produces: `WorkspaceRegistry.resolve(name) -> Workspace`, `Redactor.redact(text) -> str`, `TokenEstimator.estimate(text) -> TokenEstimate`, and `ResultStore.put/get/expand`.
- Consumes: public error types from Task 1.

- [ ] **Step 1: Write path-containment tests**

Cover normal files, `..`, absolute outside paths, symlink escape, UNC-like paths on Windows, missing workspace names, and case-insensitive Windows resolution. Use `tmp_path` and skip symlink assertions only when the OS denies symlink creation.

Run: `python -m pytest tests/safety/test_workspace.py -v`

Expected: FAIL because the implementation is absent.

- [ ] **Step 2: Implement immutable workspace registry**

```python
@dataclass(frozen=True, slots=True)
class Workspace:
    name: str
    root: Path

    def resolve_relative(self, relative: str | Path) -> Path:
        candidate = (self.root / relative).resolve(strict=False)
        if not candidate.is_relative_to(self.root):
            raise CompTextToolError(ToolErrorCode.PATH_OUTSIDE_WORKSPACE, str(relative))
        return candidate
```

On Python 3.10, provide an internal compatibility helper instead of calling `Path.is_relative_to` directly. Resolve configured roots during startup, reject duplicate names, and never accept a root from a tool request.

- [ ] **Step 3: Write and implement redaction tests**

Detect and replace:

- OpenAI-style API keys
- GitHub tokens
- bearer authorization values
- common `KEY=value` secret assignments
- Windows user-profile absolute paths when persistence policy requires anonymization

Replacement format is stable: `[REDACTED:<kind>]`. Do not redact ordinary SHA values, file names, error codes, or line numbers.

- [ ] **Step 4: Implement token estimator abstraction**

```python
@dataclass(frozen=True, slots=True)
class TokenEstimate:
    count: int
    estimator: str

class TokenEstimator(Protocol):
    def estimate(self, text: str) -> TokenEstimate: ...
```

Use `tiktoken` when importable. Fallback count is `max(1, ceil(len(text.encode("utf-8")) / 4))`. Tests assert determinism and estimator labeling, not exact parity between implementations.

- [ ] **Step 5: Implement bounded local result store**

`ResultStore` stores redacted raw sections under random opaque IDs. Required limits:

- default TTL: 24 hours
- default disk quota: 256 MiB
- maximum item: 32 MiB
- no cache path returned publicly
- atomic writes through temporary file plus replace
- expired, corrupt, or missing records map to `result_expired`

`expand(result_id, section, start, limit)` returns bounded text, total characters, returned range, and whether more content exists.

- [ ] **Step 6: Test and commit**

Run:

```bash
python -m pytest tests/safety tests/telemetry -v
python -m pytest
```

Expected: PASS.

```bash
git add src/comptext/safety src/comptext/telemetry config/mcp.example.toml tests/safety tests/telemetry
git commit -m "feat(mcp): enforce workspace and result safety"
```

---

### Task 3: Build the allowlisted compact execution engine

**Files:**
- Create: `src/comptext/execution/policy.py`
- Create: `src/comptext/execution/runner.py`
- Create: `src/comptext/execution/parsers/base.py`
- Create: `src/comptext/execution/parsers/fallback.py`
- Create: `src/comptext/execution/parsers/git.py`
- Create: `src/comptext/execution/parsers/pytest.py`
- Create: `src/comptext/execution/parsers/npm.py`
- Create: `src/comptext/execution/parsers/search.py`
- Create: `tests/execution/test_policy.py`
- Create: `tests/execution/test_runner.py`
- Create: `tests/execution/test_parsers.py`
- Create: `tests/execution/fixtures/*`

**Interfaces:**
- Produces: `CommandRegistry.build(family, args, workspace) -> Invocation`, `CompactRunner.run(invocation) -> CompactExecutionResult`, and parser registry.
- Consumes: workspace, redaction, token estimator, result store, and public error types.

- [ ] **Step 1: Define failing allowlist tests**

Assert permitted mappings such as:

```python
invocation = registry.build("pytest", ["tests/unit", "-q"], workspace)
assert invocation.argv == (sys.executable, "-m", "pytest", "tests/unit", "-q")
assert invocation.shell is False
```

Reject `;`, `&&`, pipes, redirection, absolute executable paths, `git push`, `git clean`, `npm publish`, lifecycle-script injection, and paths outside the workspace.

- [ ] **Step 2: Implement command registry**

Map families to fixed executable forms:

- `pytest` -> `sys.executable -m pytest`
- npm families -> detected `npm.cmd`/`npm`, fixed script names from configuration
- Git families -> `git status --short`, `git diff --no-ext-diff`, and bounded `git log`
- `rg` -> detected `rg` with fixed output flags
- `directory_tree` -> Python implementation, not `cmd /c tree`

Argument validators operate per family. Do not use a generic denylist as the primary security boundary.

- [ ] **Step 3: Write runner timeout/output-limit tests**

Use helper Python processes to emit stdout/stderr, sleep, exceed byte limits, and return nonzero exit codes. Verify:

- process-tree termination on Windows
- timeout maps to `timeout`
- truncation maps to a degraded result, not success
- exit code is preserved
- environment contains only configured keys and safe defaults

- [ ] **Step 4: Implement runner**

Use `subprocess.Popen` with `shell=False`, workspace `cwd`, captured binary pipes, timeout, bounded reads, and process-group handling appropriate for Windows and POSIX. Redact before cache persistence and public return.

- [ ] **Step 5: Add parser fixtures and failing tests**

Fixtures must include:

- passing and failing pytest output
- TypeScript compiler repeated errors
- ESLint warnings/errors
- npm build success/failure
- Git short status
- multi-file Git diff
- Ripgrep repeated matches
- malformed/unknown output
- Unicode paths and messages

Test compact output preserves exact primary errors, file paths, line numbers, counts, exit code, and omitted-section notices.

- [ ] **Step 6: Implement parsers and fallback**

Every parser returns:

```python
@dataclass(frozen=True, slots=True)
class CompactSection:
    name: str
    priority: int
    text: str

@dataclass(frozen=True, slots=True)
class ParsedCommandOutput:
    summary: str
    sections: tuple[CompactSection, ...]
    degraded: bool
    parser_name: str
```

The fallback includes exit code, extracted error-like lines, first 40 lines, last 40 lines, total line count, and an explicit truncation notice.

- [ ] **Step 7: Integrate result caching and token metrics**

`CompactExecutionResult` contains compact sections, `result_id`, raw and returned token estimates, reduction percentage, duration, exit code, degraded flag, and parser name.

- [ ] **Step 8: Test and commit**

Run:

```bash
python -m pytest tests/execution -v
python -m pytest
```

Expected: PASS.

```bash
git add src/comptext/execution tests/execution
git commit -m "feat(mcp): add deterministic compact execution"
```

---

### Task 4: Implement project mapping, bounded search, and symbol extraction

**Files:**
- Create: `src/comptext/context/project_map.py`
- Create: `src/comptext/context/search.py`
- Create: `src/comptext/context/symbols.py`
- Create: `tests/context/test_project_map.py`
- Create: `tests/context/test_search.py`
- Create: `tests/context/test_symbols.py`
- Create: `tests/context/fixtures/python_project/*`
- Create: `tests/context/fixtures/typescript_project/*`

**Interfaces:**
- Produces: `ProjectMapper.build(workspace) -> ProjectMap`, `CodeSearch.search(query, limit) -> SearchResult`, and `SymbolExtractor.extract(path, text) -> tuple[Symbol, ...]`.
- Consumes: workspace safety, token estimator, and result store.

- [ ] **Step 1: Write project-map tests**

Verify deterministic ordering, ignore handling, maximum file count, maximum file size, binary detection, generated-directory exclusion, and lockfile classification. Default ignores include `.git`, `.venv`, `venv`, `node_modules`, `dist`, `build`, `.next`, coverage output, and local CompText cache directories.

- [ ] **Step 2: Implement bounded project mapper**

Return relative POSIX-style paths, language classification, size, modified timestamp, generated/binary flags, and a compact directory summary. Never read file contents during inventory beyond bounded detection bytes.

- [ ] **Step 3: Write Python and TypeScript symbol tests**

Python extraction uses `ast` for modules, classes, functions, async functions, imports, and assignments representing constants.

TypeScript extraction uses deterministic line-oriented extraction for imports, exported functions/classes/interfaces/types, and test blocks. Do not add a Node parser dependency in the MVP.

- [ ] **Step 4: Implement symbol extraction**

Every symbol records name, kind, path, start/end line, exported flag, and parent. Syntax errors produce a degraded extraction record rather than aborting the index.

- [ ] **Step 5: Implement SQLite FTS5 lexical index**

Index bounded code chunks with path and line ranges. The index lives under the local CompText state directory, keyed by workspace fingerprint. Incremental refresh compares size and modified timestamp. Exclude denied and generated files by default.

Search results contain exact snippets, match terms, path, lines, symbol when known, score components, token estimate, and `result_id`. Limit defaults to 20 and maximum is 100.

- [ ] **Step 6: Test and commit**

Run:

```bash
python -m pytest tests/context/test_project_map.py tests/context/test_search.py tests/context/test_symbols.py -v
python -m pytest
```

Expected: PASS.

```bash
git add src/comptext/context tests/context
git commit -m "feat(mcp): index and search bounded project context"
```

---

### Task 5: Build deterministic context ranking and packets

**Files:**
- Create: `src/comptext/context/ranker.py`
- Create: `src/comptext/context/packets.py`
- Create: `tests/context/test_ranker.py`
- Create: `tests/context/test_packets.py`

**Interfaces:**
- Produces: `ContextRanker.rank(task, candidates, git_state, memory)`, `BudgetAllocator.allocate(...)`, and `ContextPacketBuilder.prepare(request)`.
- Consumes: project map/search/symbols, Git compact service, memory retrieval interface, token estimator, and result store.

- [ ] **Step 1: Write deterministic ranking tests**

Construct candidates where exact symbol matches, current-diff proximity, direct references, and related tests must outrank generic textual matches. Assert stable ordering when scores tie.

- [ ] **Step 2: Implement explicit scoring**

Use integer score components with named fields:

```python
@dataclass(frozen=True, slots=True)
class ScoreBreakdown:
    exact_term: int
    symbol_match: int
    diff_proximity: int
    direct_relation: int
    related_test: int
    memory_match: int
    recency_tiebreaker: int
```

Do not use an LLM or opaque embedding score in the MVP.

- [ ] **Step 3: Write token-allocation tests**

Verify the design allocation, flow of unused budget, hard budget ceiling, preservation of truncation notices, and minimum useful excerpt size. The packet must never exceed the requested budget by more than the estimator's documented fallback tolerance.

- [ ] **Step 4: Implement packet builder**

`prepare()` creates sections for task summary, source excerpts, related tests, Git state, memory, and omissions. It stores full candidate metadata in the result store and returns an expandable `result_id`.

When fewer than two relevant candidates are found, return `degraded=true` and explain that retrieval confidence is low; do not fabricate relevance.

- [ ] **Step 5: Test and commit**

Run:

```bash
python -m pytest tests/context/test_ranker.py tests/context/test_packets.py -v
python -m pytest
```

Expected: PASS.

```bash
git add src/comptext/context/ranker.py src/comptext/context/packets.py tests/context/test_ranker.py tests/context/test_packets.py
git commit -m "feat(mcp): build token-budgeted context packets"
```

---

### Task 6: Implement compact project memory and internal CompText protocol

**Files:**
- Create: `src/comptext/memory/models.py`
- Create: `src/comptext/memory/store.py`
- Create: `src/comptext/memory/retrieval.py`
- Create: `src/comptext/protocol/codes.py`
- Create: `src/comptext/protocol/plans.py`
- Create: `schemas/mcp-memory-record.v0.schema.json`
- Create: `tests/memory/test_store.py`
- Create: `tests/memory/test_retrieval.py`
- Create: `tests/protocol/test_plans.py`

**Interfaces:**
- Produces: `MemoryStore.commit`, `MemoryRetriever.recall`, and deterministic `CompactPlan.encode/decode`.
- Consumes: workspace identity, redaction, token estimator, and public memory contracts.

- [ ] **Step 1: Write memory validation and supersession tests**

Assert accepted kinds are exactly `decision`, `constraint`, `verification`, `blocker`, `next_action`, and `fact`. Reject probable secrets, empty subjects, oversized values, excessive paths/tags, and workspace mismatch.

Superseding a record creates a new row pointing to the old record; it does not update or delete historical content.

- [ ] **Step 2: Implement SQLite store**

Use WAL mode, foreign keys, explicit migrations, and parameterized statements. Store paths and tags in normalized child tables or canonical JSON with deterministic ordering. All public IDs are UUIDs.

- [ ] **Step 3: Implement budgeted retrieval**

Rank by exact subject/tag/path match, task-term overlap, active-not-superseded state, and recency as a weak tie-breaker. Return structured records without conversational history.

- [ ] **Step 4: Port only useful protocol primitives**

Create stable internal codes for operation, language, evidence class, and memory kind. Implement round-trip serialization for compact run plans such as analyze/fix/test/verify. Do not expose encode/decode as MCP tools.

Add a source note identifying the MIT-licensed `comptext-codex` concepts and preserve required attribution.

- [ ] **Step 5: Export schema, test, and commit**

Run:

```bash
python -m pytest tests/memory tests/protocol -v
python -m pytest
```

Expected: PASS.

```bash
git add src/comptext/memory src/comptext/protocol schemas/mcp-memory-record.v0.schema.json tests/memory tests/protocol
git commit -m "feat(mcp): add compact project memory and plans"
```

---

### Task 7: Add evidence metrics and register the eight MCP tools

**Files:**
- Create: `src/comptext/telemetry/evidence.py`
- Create: `src/comptext/mcp/server.py`
- Create: `src/comptext/cli/mcp.py`
- Modify: existing root CLI registration file
- Create: `schemas/mcp-evidence.v0.schema.json`
- Create: `tests/telemetry/test_evidence.py`
- Create: `tests/mcp/test_server.py`
- Create: `tests/integration/test_mcp_stdio.py`

**Interfaces:**
- Produces: `create_mcp_server(settings)`, `serve_stdio(settings)`, and persisted `ToolEvidence`.
- Consumes: all services from Tasks 1-6.

- [ ] **Step 1: Write evidence tests**

Assert every record includes tool, workspace alias, duration, outcome, parser, raw/returned token estimates, reduction, result ID, expansion count, and degraded state. Assert secret values and raw environment data never appear.

- [ ] **Step 2: Implement append-only evidence writer**

Persist canonical JSONL or SQLite records under the local state directory with atomic writes. Reuse the existing CompText evidence chain only through a small adapter; do not weaken or bypass its validation rules.

- [ ] **Step 3: Write MCP registration tests**

Assert the server exposes exactly this set:

```python
{
    "context_prepare",
    "code_search",
    "code_read",
    "run_compact",
    "git_compact",
    "memory_recall",
    "memory_commit",
    "result_expand",
}
```

Assert tool descriptions are concise, schemas reject extra fields, and service exceptions map to stable public errors.

- [ ] **Step 4: Implement transport-thin MCP adapter**

Each tool handler:

1. validates the request model
2. invokes one application service
3. records evidence in `finally`
4. returns a public response envelope
5. never reads files, executes subprocesses, or writes memory directly

- [ ] **Step 5: Implement CLI startup**

Supported command:

```bash
comptext mcp serve --stdio --config path/to/mcp.toml
```

Requirements:

- refuse startup without at least one valid workspace
- log only to stderr
- reserve stdout for MCP frames
- fail closed on invalid configuration
- no implicit environment-secret reads

- [ ] **Step 6: Add stdio integration test**

Start the server subprocess against a temporary workspace, perform MCP initialization, list tools, call `code_search`, call `run_compact` with a safe fixture, expand a result, and shut down. Assert no non-protocol text appears on stdout.

- [ ] **Step 7: Test and commit**

Run:

```bash
python -m pytest tests/mcp tests/telemetry tests/integration/test_mcp_stdio.py -v
python -m pytest
```

Expected: PASS.

```bash
git add src/comptext/mcp src/comptext/cli/mcp.py src/comptext/telemetry/evidence.py schemas/mcp-evidence.v0.schema.json tests/mcp tests/telemetry/test_evidence.py tests/integration/test_mcp_stdio.py
git commit -m "feat(mcp): expose private context server over stdio"
```

---

### Task 8: Integrate Codex Desktop and enforce context-efficient agent behavior

**Files:**
- Create: `docs/CODEX_DESKTOP_MCP_SETUP.md`
- Create: `docs/PRIVATE_CONTEXT_MCP.md`
- Create: `docs/SECURITY_PRIVATE_CONTEXT_MCP.md`
- Modify: `AGENTS.md`
- Create: `examples/codex/config.private-context-mcp.toml`
- Create: `scripts/install-private-context-mcp.ps1`
- Create: `scripts/check-private-context-mcp.ps1`
- Create: `tests/integration/test_example_config.py`

**Interfaces:**
- Produces: repeatable Windows installation/check flow and Codex operating policy.
- Consumes: `comptext mcp serve --stdio` from Task 7.

- [ ] **Step 1: Add failing example-config test**

Load the checked-in example, replace placeholder workspace root with `tmp_path`, and assert startup settings validate. Assert no API key, username-specific path, or public network binding exists.

- [ ] **Step 2: Add Codex configuration example**

Document the current supported Codex Desktop MCP configuration form, using an absolute executable path or `py -m` command appropriate for Windows. Keep user-specific paths as explicit placeholders in documentation only, never active defaults.

- [ ] **Step 3: Add `AGENTS.md` policy**

Insert a focused section:

```markdown
## Private Context MCP policy

1. Call `context_prepare` before broad repository reading.
2. Prefer `code_search` and `code_read` line ranges over full-file reads.
3. Prefer `run_compact` and `git_compact` over raw terminal output.
4. Use `result_expand` only for the missing section required to continue.
5. Save only durable decisions, constraints, verification, blockers, and next actions.
6. Never claim omitted output succeeded; inspect exit codes and degraded flags.
7. Do not bypass workspace or command policy.
```

- [ ] **Step 4: Implement PowerShell installer and doctor**

Installer actions:

- create a venv under a user-selected local directory
- install the repository with `[mcp]`
- copy the example config without overwriting an existing config
- print the exact Codex Desktop config snippet

Doctor checks:

- Python version
- package import
- config parsing
- workspace accessibility
- Git, npm, rg availability as optional capabilities
- MCP stdio initialize/list-tools smoke test

Scripts must use `$ErrorActionPreference = 'Stop'` and must not edit Codex configuration automatically.

- [ ] **Step 5: Document security and operations**

Include threat model, cache locations, TTL/quota settings, redaction limitations, allowed commands, workspace configuration, uninstallation, troubleshooting, and explicit statement that the tool does not bypass OpenAI limits.

- [ ] **Step 6: Test and commit**

Run:

```powershell
python -m pytest tests/integration/test_example_config.py -v
pwsh -NoProfile -File scripts/check-private-context-mcp.ps1 -Config config/mcp.example.toml
```

Expected: tests pass; doctor reports required capabilities as PASS and optional missing tools as WARN.

```bash
git add AGENTS.md docs/PRIVATE_CONTEXT_MCP.md docs/CODEX_DESKTOP_MCP_SETUP.md docs/SECURITY_PRIVATE_CONTEXT_MCP.md examples/codex scripts tests/integration/test_example_config.py
git commit -m "docs(mcp): add Codex Desktop setup and safety policy"
```

---

### Task 9: Build the comparative benchmark and release gate

**Files:**
- Create: `benchmarks/private-context-mcp/corpus.json`
- Create: `benchmarks/private-context-mcp/run_benchmark.py`
- Create: `benchmarks/private-context-mcp/README.md`
- Create: `tests/benchmark/test_corpus.py`
- Create: `tests/benchmark/test_metrics.py`
- Create: `docs/private-context-mcp-benchmark-report-template.md`

**Interfaces:**
- Produces: reproducible baseline/MCP benchmark reports and pass/fail release gate.
- Consumes: context, execution, memory, evidence, and token-estimation services.

- [ ] **Step 1: Define and validate a 20-task corpus**

Include ten Python and ten TypeScript tasks spanning:

- locate implementation and related tests
- diagnose one failing test
- diagnose repeated type errors
- inspect a multi-file diff
- summarize repository architecture under a budget
- continue from saved decision/verification state
- handle large successful test output
- handle large failed build output
- find symbol definitions/references
- determine the minimum verification command set

Every task declares fixture repository, expected relevant files, expected critical facts, verification command, and severity of omissions.

- [ ] **Step 2: Implement baseline and MCP modes**

Baseline mode captures raw file/search/command output according to a fixed transparent procedure. MCP mode uses the services exactly as public tools would. Both modes share the same task fixtures and token estimator.

- [ ] **Step 3: Implement metrics and release gate**

Report:

- raw and returned tool/context tokens
- median and percentile reduction
- tool-call count
- expansion count
- duration
- critical-fact recall
- task/verification success
- false omission incidents

Gate:

```python
passed = (
    median_reduction >= 0.50
    and mcp_success_rate >= baseline_success_rate
    and high_severity_omissions == 0
)
```

- [ ] **Step 4: Add deterministic tests**

Use fixture results to test calculations, empty sets, zero raw tokens, degraded outputs, and gate boundaries at 49.9% and 50.0%.

- [ ] **Step 5: Run benchmark and save report**

Run:

```bash
python benchmarks/private-context-mcp/run_benchmark.py \
  --corpus benchmarks/private-context-mcp/corpus.json \
  --output .comptext/reports/private-context-mcp.json
```

Expected: valid JSON report. The implementation is not release-ready until the gate passes; record failures honestly rather than adjusting the corpus after seeing results.

- [ ] **Step 6: Commit**

```bash
git add benchmarks/private-context-mcp tests/benchmark docs/private-context-mcp-benchmark-report-template.md
git commit -m "test(mcp): add token-efficiency benchmark gate"
```

---

### Task 10: Full verification, migration note, and MVP release preparation

**Files:**
- Modify: `README.md`
- Modify: `docs/COMPTEXT_ARCHITECTURE_v1.md`
- Modify: `docs/COMPTEXT_SECURITY.md`
- Create: `docs/COMPTEXT_CODEX_PROTOCOL_MIGRATION.md`
- Create: `docs/private-context-mcp-verification-report.md`

**Interfaces:**
- Produces: reviewed MVP documentation and a decision on release readiness.
- Consumes: all prior tasks and benchmark report.

- [ ] **Step 1: Document repository relationship**

State that `Comptext` is canonical and `comptext-codex` remains a protocol-history/source repository. List exact protocol concepts ported, attribution, compatibility decisions, and elements intentionally not ported, especially encode/decode MCP tools and unsupported 94% total-session claims.

- [ ] **Step 2: Update architecture and security docs**

Replace the MCP status from deferred only after the real implementation and integration tests exist. Describe `stdio`, services, caches, memory, evidence, and future Secure MCP Tunnel adapter as separate transport work.

- [ ] **Step 3: Run complete verification**

Run:

```bash
python -m pytest
python -m ruff check src tests benchmarks
python -m mypy src/comptext
python -m build
python benchmarks/private-context-mcp/run_benchmark.py --corpus benchmarks/private-context-mcp/corpus.json --output .comptext/reports/private-context-mcp.json
git diff --check
```

On Windows also run:

```powershell
pwsh -NoProfile -File scripts/check-private-context-mcp.ps1 -Config config/mcp.example.toml
```

Expected: all code checks pass and the benchmark gate reports its truthful status.

- [ ] **Step 4: Perform security regression review**

Manually verify:

- no `shell=True`
- no server socket or HTTP listener
- no automatic environment-secret reads
- no path escapes
- no destructive command family
- no secrets in evidence/cache fixtures
- no raw cache paths in MCP output
- no stdout logging outside MCP frames

Record evidence and exact commands in `docs/private-context-mcp-verification-report.md`.

- [ ] **Step 5: Decide MVP status**

Mark one state only:

- `verified-mvp` when all checks and benchmark gate pass
- `functional-preview` when correctness checks pass but benchmark gate does not
- `blocked` when safety or correctness checks fail

Do not publish production or security claims beyond the recorded evidence.

- [ ] **Step 6: Commit**

```bash
git add README.md docs/COMPTEXT_ARCHITECTURE_v1.md docs/COMPTEXT_SECURITY.md docs/COMPTEXT_CODEX_PROTOCOL_MIGRATION.md docs/private-context-mcp-verification-report.md
git commit -m "docs(mcp): record private context MVP verification"
```

---

## Deferred Follow-up Plans

These are separate specs and plans after MVP validation:

1. OpenAI Secure MCP Tunnel transport adapter and authentication operations.
2. Optional HTTP transport for non-OpenAI MCP clients.
3. Tree-sitter/LSP symbol extraction for more languages.
4. Embedding retrieval only if lexical/symbol benchmark recall is insufficient.
5. TUI panels for token savings, result expansion, memory, and evidence.
6. Controlled file-edit tools with approval gates, if still needed.
7. Multi-agent compact handoff using the internal CompText protocol.

## Plan Self-Review

- Every design requirement maps to a task.
- The plan contains no implementation placeholders.
- Public tool names and core signatures are consistent across tasks.
- Setup, safety, testing, benchmarking, documentation, and repository migration are included.
- Deferred features are explicitly separated from the MVP.
- The benchmark measures net utility rather than repeating promotional reduction claims.
