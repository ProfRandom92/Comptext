# CompText

<p align="center">
  <b>Local AI orchestration for software engineering.</b><br/>
  A Windows-first, local-first runtime for plans, evidence, provider configuration, skills, hooks, subagents, and deterministic validation.
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-local%20dry--run%20MVP-blue">
  <img alt="Mode" src="https://img.shields.io/badge/mode-local--first-black">
  <img alt="Safety" src="https://img.shields.io/badge/safety-dry--run%20default-green">
  <img alt="Providers" src="https://img.shields.io/badge/providers-disabled%20or%20experimental-orange">
  <img alt="PR Review Memory" src="https://img.shields.io/badge/PR%20Review%20Memory-local%20v0-purple">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows--first-informational">
</p>

CompText is a local AI orchestration platform for software engineering. It is not a package release, hosted service, desktop app, live provider router, or production-ready system. This repository is a local dry-run MVP seed for the `comptext` CLI and surrounding contracts.

## What CompText Changes

CompText replaces the simple pattern:

```text
Prompt -> Answer
```

with a bounded engineering workflow:

```text
Run -> Plan -> Execution -> Evidence -> Replay -> Verify
```

The goal is to make AI-assisted engineering work structured, reviewable, replayable, and constrained by explicit local safety rules.

## Architecture

```mermaid
flowchart LR
  subgraph client ["Client Interfaces"]
    user["Developer"]
    terminal["CompText Terminal OS"]
    desktop["Future Desktop UI"]
  end

  subgraph gateway ["Gateway Layer"]
    cli["CLI Entry Points"]
    providerGateway["Provider Gateway Dry Run"]
  end

  subgraph service ["Core Services"]
    runtime["Run Runtime"]
    agentBus["Agent Bus"]
    air["AIR Plans"]
    evidence["Evidence Service"]
    memory["Memory Service"]
    plugins["Plugin System"]
  end

  subgraph datastore ["Local State"]
    schemas["Schema Contracts"]
    fixtures["Examples and Fixtures"]
    hashChain["Evidence Hash Chain"]
    knowledgeGraph["Knowledge Graph"]
  end

  subgraph external ["Deferred Integrations"]
    providers["Provider APIs Disabled"]
    github["GitHub Actions Deferred"]
    mcp["MCP Runtime Deferred"]
  end

  user -->|"Runs local commands"| terminal
  terminal -->|"Invokes scoped commands"| cli
  desktop -->|"Future local UI route"| cli
  cli -->|"Starts deterministic runs"| runtime
  cli -->|"Queries safe provider state"| providerGateway
  providerGateway -->|"Normalizes dry-run responses"| runtime
  runtime -->|"Executes structured plans"| air
  runtime -->|"Dispatches tasks"| agentBus
  agentBus -->|"Uses scoped skills"| plugins
  runtime -->|"Records verifiable events"| evidence
  runtime -->|"Loads compact context"| memory
  evidence -->|"Writes event contracts"| schemas
  evidence -->|"Maintains deterministic chain"| hashChain
  memory -->|"Indexes project context"| knowledgeGraph
  plugins -->|"Validates examples"| fixtures
  runtime -.->|"Provider calls deferred"| providers
  plugins -.->|"GitHub behavior deferred"| github
  plugins -.->|"MCP runtime deferred"| mcp
```

## Evidence Chain

CompText treats evidence as a first-class runtime primitive. The current repository includes deterministic sample evidence verification, not live attestation.

```mermaid
flowchart LR
  developer["Developer"] --> cli["CompText CLI"]
  cli --> run["Run"]
  run --> plan["Plan"]
  plan --> execution["Execution"]
  execution --> eventA["Evidence Event A"]
  eventA --> hashA["Hash A"]
  hashA --> eventB["Evidence Event B"]
  eventB --> hashB["Hash B"]
  hashB --> bundle["Run Bundle"]
  bundle --> replay["Replay"]
  replay --> verify["Verify"]
  validation["Validation"] --> bundle
  execution -.-> approval["Human Approval Gate"]
  verify -.-> provider["Provider Attestation Deferred"]
  verify -.-> github["GitHub Checks Deferred"]
```

Every future live execution path should answer:

| Question | CompText answer |
|---|---|
| What happened? | Evidence events |
| In what order? | Ordered run records |
| Was it modified? | Hash-chain verification |
| Can it be replayed? | Run bundle |
| Can it be reviewed? | Compact handoff |
| Can it be trusted blindly? | No. Verify first. |

## Capability Matrix

| Capability | Status | Notes |
|---|---|---|
| Architecture and safety docs | Prepared | Local design and operating boundaries |
| JSON schema contracts | Prepared | AIR, Evidence, Run, plugins, hooks, subagents, approvals, CLI commands |
| Local dry-run CLI | Prepared | Deterministic scaffolding only |
| Provider registry | Prepared | Safe states only: `not_configured`, `disabled`, `experimental` |
| Provider Gateway v0 | Dry-run | No server, port binding, secret reads, or live routing |
| Evidence hash-chain | Prepared | Deterministic sample verification |
| Sample run runtime | Dry-run | Local sample execution only |
| PR Review Memory | Local v0 | Static scaffold, skill bridge, renderer, schema contract |
| Token Saver workflow | Companion | Uses local project state and compact handoff discipline |
| Codex local autonomy | Local guidance | Explicitly requested local batches only |
| MCP runtime | Deferred | No live MCP server behavior |
| Desktop app | Deferred | Not implemented |
| Package release | Deferred | No release claim |
| Auto-push, PR, or merge | Forbidden by default | Requires explicit instruction |

## Safety Contract

CompText defaults to local, bounded, and non-destructive behavior.

| Boundary | Current rule |
|---|---|
| Provider calls | Do not perform unless explicitly configured and requested |
| Secrets | Do not store secrets, API keys, raw environment variables, or provider payloads in Evidence or logs |
| GitHub writes | Do not push, open PRs, merge, enable auto-merge, or call GitHub APIs unless explicitly instructed |
| MCP runtime | Deferred; no live runtime behavior in this scaffold |
| Review state | Do not automatically resolve ambiguous, unfixed, or out-of-scope comments |
| Claims | Do not make production, security, compliance, legal, forensic, or official compatibility claims |
| Destructive commands | Require explicit approval |

Codex local autonomous batches are governed by [`AGENTS.md`](AGENTS.md) and [`docs/CODEX_LOCAL_AUTONOMY.md`](docs/CODEX_LOCAL_AUTONOMY.md).

## PR Review Memory

The PR Review Memory scaffold is a dry-run companion for token-saving workflows. It defines compact review-memory formats only; it does not replace CompText Token Saver, perform GitHub actions, make network or provider calls, read secrets, or implement an MCP runtime server.

Repo-side pieces:

- [`plugins/pr-review-memory/README.md`](plugins/pr-review-memory/README.md)
- [`plugins/pr-review-memory/SKILL.md`](plugins/pr-review-memory/SKILL.md)
- [`plugins/pr-review-memory/renderer.py`](plugins/pr-review-memory/renderer.py)
- [`plugins/pr-review-memory/schema/pr-review-memory.v0.schema.json`](plugins/pr-review-memory/schema/pr-review-memory.v0.schema.json)
- [`.agents/skills/pr-review-memory/SKILL.md`](.agents/skills/pr-review-memory/SKILL.md)

The local renderer converts structured review-memory dictionaries into compact Markdown. Runtime GitHub integration, MCP runtime behavior, automatic review resolution, automatic merge behavior, and production behavior remain deferred.

## Local Dry-Run Commands

```bash
comptext doctor --dry-run
comptext validate schemas --dry-run
comptext providers list --dry-run
comptext gateway health --dry-run
comptext gateway models --dry-run
comptext gateway sample --dry-run
comptext evidence verify --sample
comptext run sample --dry-run
```

Gateway v0 commands are deterministic local scaffolding only. They do not start a server, bind ports, read secrets or environment variables, call provider APIs, or infer real model availability.

## Start Here

Read:

- [`START_HERE.md`](START_HERE.md)
- [`docs/COMPTEXT_MVP.md`](docs/COMPTEXT_MVP.md)
- [`docs/COMPTEXT_ARCHITECTURE_v1.md`](docs/COMPTEXT_ARCHITECTURE_v1.md)
- [`docs/COMPTEXT_SECURITY.md`](docs/COMPTEXT_SECURITY.md)
- [`docs/CODEX_DESKTOP_WORKFLOW.md`](docs/CODEX_DESKTOP_WORKFLOW.md)
- [`docs/CODEX_DESKTOP_PROMPTS.md`](docs/CODEX_DESKTOP_PROMPTS.md)

## Contributor Orientation

Use `main` as the canonical branch. Create focused branches such as `docs/<topic>`, `plugin/<feature>`, `fix/<bug>`, or `codex/<task>`.

Before changing behavior, check the relevant schema, docs, examples, and tests together. Keep provider states limited to `not_configured`, `disabled`, or `experimental` unless a task explicitly changes that contract.

For local validation, run:

```bash
python -m pytest
git diff --check
```

## Roadmap

| Phase | Status language | Focus |
|---|---|---|
| Foundation | Prepared | Docs, schemas, examples, local dry-run CLI |
| Provider Gateway v0 | Dry-run | Deterministic local provider command scaffolding |
| PR Review Memory | Local v0 | Skill bridge, renderer, schema contract, compact handoff |
| Codex local autonomy | Local guidance | Explicitly requested local batches with no push or PR by default |
| Minimal CI gate | Deferred | Validation automation after local contracts settle |
| Evidence digest plugin | Deferred | Compact evidence summaries after renderer patterns stabilize |
| Live integrations | Deferred | Provider routing, MCP runtime, and GitHub behavior behind explicit approval gates |
