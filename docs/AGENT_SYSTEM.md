# CompText Agent System

CompText agents are workers on an Agent Bus, not chat personas. They receive scoped work, operate within explicit permissions, emit evidence, and return structured results for review.

## Lifecycle

```text
Task -> Context -> Plan -> Execution -> Evidence -> Review -> Result
```

- Task: define the requested outcome, boundaries, and approval needs.
- Context: gather the minimum relevant project state, memory, files, policies, and recent run data.
- Plan: describe the intended steps, tools, risks, validation, and evidence outputs.
- Execution: perform only approved local actions inside the assigned scope.
- Evidence: record redacted summaries, hashes, diffs, checks, and blockers.
- Review: inspect outputs, uncertainty, failures, and policy compliance.
- Result: return a concise status with changed files, validation, risks, and next steps.

## Agent types

- Architect: shapes system boundaries, interfaces, and design decisions.
- Runtime Engineer: works on local runtime, command flow, scheduling, and dry-run behavior.
- Provider Engineer: works on provider registry and gateway contracts without live calls by default.
- Evidence Engineer: maintains evidence schemas, verification, redaction, and replay contracts.
- Security Reviewer: reviews safety rules, secret handling, approvals, and risky flows.
- Tester: adds and runs relevant local checks, fixtures, and regression tests.
- Release Coordinator: prepares release plans and readiness checklists without publishing by default.
- Documentation Maintainer: keeps operational and architecture docs current.

## Boundaries

- Agents do not bypass approvals.
- Agents do not directly access secrets.
- Agents must produce evidence for meaningful actions and decisions.
- Agents must summarize uncertainty, blockers, skipped checks, and unresolved review comments.
- Agents must not claim hooks, plugins, subagents, providers, or MCP tools are implemented unless the repository contains working implementation and validation.
