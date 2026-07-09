# CompText CLI Contract

This document specifies the CLI interface contract between the Node/Ink TUI layer (`comptext-tui`) and the Python backend (`comptext` CLI).

## Global Rules

1. **Local and Offline Boundaries**: Every command must remain local-only. Live providers must be shown as `disabled`/`not_configured`, network calls must remain `not_called`/`none`, and secrets must remain `not_read`.
2. **Dry-Run Constraint**: Subcommands require `--dry-run` (or `--sample`/`--file` for evidence verification) as a safety flag. Running commands without these flags will raise errors or exit with a non-zero code.
3. **Output Formats**:
   - Diagnostic and verify screens (`status`, `agents`, `verify`) output formatted plaintext dashboards to `stdout`.
   - Core API operations output formatted JSON payloads to `stdout`.
   - In case of failures/expected exceptions, the CLI outputs a standard JSON error block to `stdout` (e.g. `{"ok": false, "error": {"message": "...", "type": "..."}}`).

---

## Subcommands Contract

### 1. Doctor
Runs diagnostic checks on local system, project file presence, python configuration, and workspace validation.
- **Syntax**: `python -m modules.cli.cli_entrypoint doctor --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "command": "comptext doctor --dry-run",
    "mode": "dry-run",
    "network": "not_checked",
    "ok": true,
    "os": {
      "release": "11",
      "system": "Windows"
    },
    "project_files": {
      "AGENTS.md": true,
      "CODEX_START_PROMPT.md": true,
      "README.md": true,
      "START_HERE.md": true,
      "docs/COMPTEXT_MVP.md": true,
      "docs/COMPTEXT_MVP_TASKS.md": true,
      "tasks/00_bootstrap_repo.md": true,
      "tasks/01_local_dry_run_mvp.md": true
    },
    "providers": "not_called",
    "python": {
      "supported": true,
      "version": "3.12.10"
    },
    "workspace_validation": {
      "ok": true,
      "results": [ ... ]
    }
  }
  ```
- **Exit Code**: `0` on success, `1` on failure.

### 2. Validate Schemas
Validates provider registry schemas against examples.
- **Syntax**: `python -m modules.cli.cli_entrypoint validate schemas --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "mode": "dry-run",
    "results": [
      {
        "schema": "schemas/provider-registry.schema.json",
        "example": "examples/provider/provider-registry-sample.json",
        "status": "valid"
      }
    ]
  }
  ```
- **Exit Code**: `0`.

### 3. Validate Workspace
Validates all workspace schemas and examples (e.g. snapshots, deltas, reflection gates).
- **Syntax**: `python -m modules.cli.cli_entrypoint validate workspace --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "mode": "dry-run",
    "results": [
      {
        "schema": "schemas/workspace-snapshot.v0.schema.json",
        "example": "examples/workspace/workspace-snapshot.sample.json",
        "status": "valid"
      }
    ]
  }
  ```
- **Exit Code**: `0` if all results are `valid`, `1` if any are `invalid`.

### 4. Providers List
Lists staged provider configurations.
- **Syntax**: `python -m modules.cli.cli_entrypoint providers list --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "mode": "dry-run",
    "providers": [
      {
        "id": "comptext-local",
        "name": "CompText Local Offline Provider",
        "state": "experimental"
      }
    ]
  }
  ```
- **Exit Code**: `0`.

### 5. Gateway Health
Checks the status of the local offline Gateway routing.
- **Syntax**: `python -m modules.cli.cli_entrypoint gateway health --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "bind": "127.0.0.1",
    "mode": "dry-run",
    "ok": true,
    "providers": "not_called",
    "routes": [
      "GET /health",
      "GET /v1/models",
      "POST /v1/messages",
      "POST /v1/responses",
      "POST /v1/chat/completions"
    ],
    "secrets": "not_read",
    "server": "not_started"
  }
  ```
- **Exit Code**: `0` if ok, `1` if not.

### 6. Gateway Models
Lists models registered in the Gateway.
- **Syntax**: `python -m modules.cli.cli_entrypoint gateway models --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "mode": "dry-run",
    "models": [
      {
        "capabilities": [
          "text",
          "tools_planned"
        ],
        "id": "comptext-dry-run-model",
        "provider": "comptext-local",
        "state": "not_configured"
      }
    ]
  }
  ```
- **Exit Code**: `0`.

### 7. Gateway Sample Response
Executes a dry-run chat completion request against the gateway.
- **Syntax**: `python -m modules.cli.cli_entrypoint gateway sample --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "message": {
      "content": "CompText Gateway dry-run response content.",
      "role": "assistant"
    },
    "mode": "dry-run",
    "model": "comptext-dry-run-model",
    "network": "not_called",
    "ok": true,
    "provider": "comptext-local",
    "providers": "not_called",
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 12,
      "total_tokens": 22
    }
  }
  ```
- **Exit Code**: `0` on success, `1` on failure.

### 8. Evidence Verify
Validates sequential indices, previous hashes, and SHA-256 signatures in an evidence log chain.
- **Syntax**:
  - `python -m modules.cli.cli_entrypoint evidence verify --sample`
  - `python -m modules.cli.cli_entrypoint evidence verify --file <path>`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "command": "comptext evidence verify --sample",
    "mode": "sample",
    "events": 3,
    "network": "not_called",
    "ok": true,
    "providers": "not_called",
    "root_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
  ```
- **Exit Code**: `0` if verification succeeds (`ok: true`), `1` if verification fails or files are missing/invalid.

### 9. Evidence Verify State Log
Validates sequence number, commit ref, and sequence hash chaining for state log logs.
- **Syntax**: `python -m modules.cli.cli_entrypoint evidence verify-state-log --file <path>`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "command": "comptext evidence verify-state-log --file examples/workspace/evidence-state-log.sample.json",
    "mode": "state-log",
    "entries": 2,
    "network": "not_called",
    "ok": true,
    "providers": "not_called",
    "root_hash": "a1b2c3d4..."
  }
  ```
- **Exit Code**: `0` on success, `1` on failure/error.

### 10. Run Sample
Triggers a dry-run local run process.
- **Syntax**: `python -m modules.cli.cli_entrypoint run sample --dry-run`
- **Output Format**: JSON
- **Success Response Sample**:
  ```json
  {
    "command": "comptext run sample --dry-run",
    "mode": "dry-run",
    "network": "not_called",
    "ok": true,
    "providers": "not_called",
    "result": "completed"
  }
  ```
- **Exit Code**: `0` on success, `1` on failure.

### 11. Plaintext Screens: Status / Agents / Verify
These subcommands print formatted plaintext dashboards to `stdout`.
- **Status Screen**: `python -m modules.cli.cli_entrypoint status --dry-run`
- **Subagent Inventory Screen**: `python -m modules.cli.cli_entrypoint agents --dry-run`
- **Verify Screen**: `python -m modules.cli.cli_entrypoint verify --dry-run`
- **Exit Code**: `0` if all components pass, `1` if any component reports `fail` or an error is raised.

---

## Standard Error Schema

Whenever a subcommand encounters an error (e.g. invalid JSON, missing files, signature tampering, bad command args), it returns `exit code 1` and prints:
```json
{
  "error": {
    "message": "Detailed error message describing the failure",
    "type": "NameOfExceptionRaised"
  },
  "ok": false
}
```
