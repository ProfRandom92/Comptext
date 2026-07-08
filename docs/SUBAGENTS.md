# Local Subagent Role Definitions

This document defines the local subagent role specifications for the `comptext` repository. These definitions describe how development tasks should be divided across focused local-only agents.

> [!NOTE]
> Subagents in this repository are documentation-first role specifications meant to guide development boundaries in offline dry-runs. In active Google Antigravity (AGY) sessions, these are loaded from `.agents/agents/{agent_name}/agent.json` as role configuration templates for delegation. They are not active background runtime executors or auto-schedulers.

---

## 1. Subagent Specifications

### 1.1 Validation Agent (`validation-agent`)
- **Purpose**: Validating committed workspace schemas and example JSON files against JSON schema constraints, executing CLI validation commands, and running doctor validation checks.
- **Allowed Scope**:
  - Validating files under `schemas/` and `examples/workspace/`.
  - Calling helper functions in `modules/validation/`.
  - Executing `comptext validate workspace --dry-run` and `comptext doctor --dry-run`.
- **Forbidden Scope**:
  - Running any network requests, provider APIs, or Model Context Protocol (MCP) integrations.
  - Generating new runtime snapshots or filesystem synchronization.
- **Expected Inputs**: Workspace schemas, example JSON files, and path directories.
- **Expected Outputs**: Structured validation results (list of dicts containing schema paths, example paths, status, and errors).
- **Validation/Check Commands**:
  - `python -m pytest tests/validation`
  - `python -m pytest tests/cli`

### 1.2 Evidence Agent (`evidence-agent`)
- **Purpose**: Managing the evidence hash-chain, enforcing optional workspace references, and generating dry-run sample evidence events.
- **Allowed Scope**:
  - Appending or validating optional string reference fields (`workspace_before_ref`, `workspace_after_ref`, `workspace_delta_ref`).
  - Calculating event and previous block hashes using `modules/evidence/evidence.py`.
- **Forbidden Scope**:
  - Embedding full WorkspaceSnapshot or WorkspaceDelta JSON objects inside Evidence payloads.
  - Making security/cryptographic compliance claims beyond deterministic local hash-linking.
  - Executing network or external provider API calls.
- **Expected Inputs**: Raw event payload dicts and previous hash strings.
- **Expected Outputs**: Staged/serialized hash-chain events.
- **Validation/Check Commands**:
  - `python -m pytest tests/evidence`

### 1.3 Runtime Dry-Run Agent (`runtime-dryrun-agent`)
- **Purpose**: Building deterministic dry-run sample events and asserting zero resource/API access.
- **Allowed Scope**:
  - Generating local sample execution summaries.
  - Enforcing and testing no-resource boundaries (mocking open, env, and socket calls).
- **Forbidden Scope**:
  - Automating active filesystem snapshots or synchronization.
  - Starting network servers or binding local ports.
  - Initiating external LLM provider API requests.
- **Expected Inputs**: Dry-run flags and sample plan steps.
- **Expected Outputs**: Local-only execution results showing completed steps.
- **Validation/Check Commands**:
  - `python -m pytest tests/runtime`

### 1.4 PR Memory Agent (`pr-memory-agent`)
- **Purpose**: Supporting local deterministic PR review-memory rendering and formatting markdown review summaries.
- **Allowed Scope**:
  - Compiling review-memory schemas and renderer templates.
  - Converting review-memory dictionaries into markdown handoffs.
- **Forbidden Scope**:
  - Accessing or modifying GitHub pull requests, issues, or branches.
  - Making live GitHub API requests.
- **Expected Inputs**: PR review-memory JSON input dictionary.
- **Expected Outputs**: Markdown handoff block.
- **Validation/Check Commands**:
  - `python -m pytest tests/plugins`

### 1.5 Docs Agent (`docs-agent`)
- **Purpose**: Creating and polishing scoped documentation files, README fragments, and workflow instructions.
- **Allowed Scope**:
  - Creating new files under `docs/`.
  - Updating CLI workflow notes and local plugins documentation.
- **Forbidden Scope**:
  - Modifying the root [README.md](../README.md) file unless explicitly requested.
  - Implementing badge or pipeline automations.
- **Expected Inputs**: Markdown documents and system updates.
- **Expected Outputs**: Standardized markdown documentation files.
- **Validation/Check Commands**:
  - `git diff --check`

---

## 2. Routing Matrix

When a task is received, it is routed to the preferred subagent based on its type and directory boundaries:

| Task Type | Preferred Subagent | Files / Directories in Scope | Validation Command |
| :--- | :--- | :--- | :--- |
| Schema / Example updates | `validation-agent` | `schemas/`, `examples/workspace/`, `modules/validation/` | `python -m pytest tests/validation` |
| Evidence chain / hashing | `evidence-agent` | `modules/evidence/`, `tests/evidence/` | `python -m pytest tests/evidence` |
| Dry-run workflow / sample execution | `runtime-dryrun-agent` | `modules/runtime/`, `tests/runtime/` | `python -m pytest tests/runtime` |
| PR memory rendering | `pr-memory-agent` | `plugins/pr-review-memory/`, `tests/plugins/` | `python -m pytest tests/plugins` |
| Documentation updates | `docs-agent` | `docs/` | `git diff --check` |

---

## 3. Escalation Rules

Subagents must abort execution and escalate to the user immediately if any of the following safety triggers occur:
1. **Dirty Working Tree**: Abort if git status shows untracked (excluding cache files) or modified tracked files prior to starting work.
2. **HEAD Mismatch**: Abort if the expected git log HEAD hash does not match the actual current commit.
3. **External Dependencies**: Stop immediately before executing any network calls, provider API requests, or Model Context Protocol (MCP) integrations.
4. **Out of Scope Modifications**: Stop before modifying files outside of the allowed directories (e.g., editing the root `README.md` or existing `AGENTS.md` rules).

---

## 4. AGY CLI Usage Guide

When inspecting or debugging active agent environments, use the following `agy` slash commands:
- `/agents`: Inspect active local agent subagent roles and configs.
- `/skills`: Inspect currently loaded skills and recipes.
- `/context`: Review the active file mentions and context window contents.
- `/diff`: Verify staged changes and diff blocks prior to final reporting.
- `/permissions`: Ensure network access, provider calls, and port binding permissions remain blocked.
