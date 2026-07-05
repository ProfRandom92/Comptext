# CompText Architecture v1

## Product Vision

CompText is a local AI orchestration platform for software engineering. It is not only a CLI, not only a chat interface, and not only a model wrapper. It is intended to become a local engineering operating system that coordinates agentic tools, model providers, context, evidence, replay, and developer workflows.

Core claim:

> Models are providers. Context is the product. Evidence is the trust layer. CompText is the kernel.

## Non-Goals

- No fake provider availability.
- No hidden credential manipulation.
- No automatic PR, push, merge, or release.
- No unsupported compliance, forensic, or certification claims.
- No hidden chain-of-thought capture.
- No cloud dependency for the core runtime.
- No WSL-only Windows strategy.

## Seven-Layer Architecture

```text
User
  │
CompText Terminal OS / Desktop UI
  │
Runtime ─ Gateway ─ MCP Fabric ─ Agent Bus
  │
AIR ─ Evidence ─ Memory / Knowledge Graph
  │
Provider Router
  │
OpenAI / Anthropic / Gemini / Ollama / OpenRouter / NVIDIA / xAI / Mistral / LM Studio
```

### 1. Terminal OS / UI

Terminal-first workbench with:

- Session Manager
- Workspace Manager
- Command Palette
- Notification Center
- Provider Switcher
- Evidence Viewer
- Run Queue
- CompText Logo / Splash
- later Desktop UI

### 2. Runtime

The Runtime manages:

- Runs
- Plans
- Execution
- Evidence capture
- Replay
- Verification
- Queueing
- Dependencies
- Retry
- Timeout
- Resume

### 3. Gateway

The Gateway normalizes provider traffic and exposes local routes:

- `GET /health`
- `GET /v1/models`
- `POST /v1/messages`
- `POST /v1/responses`
- `POST /v1/chat/completions`
- `GET /admin`

Default bind: `127.0.0.1` only.

### 4. Agent Bus

The Agent Bus coordinates specialized agents as tasks, not as chat noise.

- Tasks enter a queue.
- Subagents work with explicit roles.
- Results become Evidence events.
- Human approval gates high-risk transitions.

### 5. AIR

AIR is the Agent Intermediate Representation. It describes what should happen before execution.

AIR should include:

- Intent
- Goal
- Context
- Files
- Tools
- Constraints
- Permissions
- Expected Output
- Review
- Approval
- Evidence links

### 6. Evidence

Evidence describes what actually happened.

Every relevant action becomes an event:

- run started/completed
- plan created
- context pack built
- tool used
- file changed
- diff created
- tests executed
- approval requested/granted/denied
- provider selected
- model changed

### 7. Memory / Knowledge Graph

Memory is not chat history. It is structured workspace knowledge:

- Workspace memory
- Semantic context
- Recent runs
- Git state
- Failures
- Learned preferences
- Workspace graph
- File/function/type/test/run/evidence relationships

## Kernel Services

- Context Service
- Evidence Service
- Provider Service
- Model Service
- Secrets Service
- Workspace Service
- Git Service
- Filesystem Service
- Task Scheduler
- Plugin Service
- Security Service

## Repository Strategy

`comptext` is the clean main product repository. Other repositories may remain sources, archives, or migration inputs, but they must not define the public product name or the core architecture.

## First Implementation Principle

Prepare before implementing. Architecture, contracts, schemas, docs, and stubs should be coherent before risky refactors or provider integrations are attempted.

## Interface Overview

CompText defines clear interfaces between layers. These interfaces are described with JSON Schemas in `schemas/` and supporting documents in `docs/`.

| Interface | Key fields |
| --- | --- |
| **AIR Plan** | version, intent, goal, context, files, tools, permissions, expected_outputs, metadata |
| **Evidence Event** | event_id, run_id, type, actor, tool, summary, input_hash, output_hash, timestamp, redaction |
| **Run Record** | run_id, air_hash, status, start_time, end_time, event_hashes, metrics |
| **Provider Registry Entry** | state, api_key_env, base_url, models |
| **MCP Tool Descriptor** | name, version, description, inputs, outputs, tags, requires_approval |
| **Plugin Manifest** | name, version, description, entry, hooks, dependencies, permissions, allowed_tools |
| **Hook Event** | hook_id, type, command, redactions, status, timestamp, actor |
| **Subagent Manifest** | name, role, responsibilities, allowed_tools, forbidden_actions, inputs, outputs, escalation_rules, version |

The AIR Plan describes intended behavior. Evidence Events document what actually happened. The Run Record connects both with status and timestamps. Further detail belongs in the dedicated specifications such as `docs/COMPTEXT_AIR_SPEC.md`, `docs/COMPTEXT_EVIDENCE.md`, and `docs/COMPTEXT_RUNTIME.md`.
