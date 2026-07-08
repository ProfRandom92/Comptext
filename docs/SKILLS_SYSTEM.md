# CompText Skills System

Skills are capability packs, not random prompts. A skill should package repeatable operating knowledge for a bounded kind of work.

## Skill contents

Each skill may include:

- `SKILL.md`
- checklists
- command recipes
- templates
- validation rules
- anti-patterns

## Proposed directory shape

```text
skills/
  python/
    SKILL.md
  git/
    SKILL.md
  github/
    SKILL.md
  docs/
    SKILL.md
  evidence/
    SKILL.md
  provider-gateway/
    SKILL.md
```

This repository does not implement a full skill marketplace yet. Skill files are documentation-first operating guides until a runtime loader exists.

## Baseline Repository Skills

The following baseline workspace skills are defined under `.agents/skills/` and `.antigravity/plugins/comptext-local/skills/`:

- **`comptext-status`**: View a summary of active workspace file presence and local diagnostics status.
- **`comptext-local-boundaries`**: Audit project doctor files and verify dry-run sandbox boundaries.
- **`comptext-local-verify`**: Perform offline verify checks on workspace status, subagents, and doctor diagnostics.
- **`comptext-subagent-inventory`**: Inspect local subagent definitions, allowed file scopes, and routing.
- **`comptext-workspace-validation`**: Validate workspace snapshot and delta files against JSON Schema contracts.
- **`pr-review-memory`**: Bridges Codex prompts to the dry-run PR Review Memory scaffold.
- **`repo-hygiene`**: Manage stale path cleanup, metadata alignment, and file exclusions.
- **`ci-validation`**: Manage GitHub Actions validation workflows and Python version compatibility.
- **`evidence-chain`**: Design evidence event models, serialization, and sequence logs.

## Skill requirements

- Keep each skill scoped to one capability area.
- Include trigger conditions, inputs, outputs, when to use it, and when not to use it.
- List required local checks and safety notes.
- List forbidden behavior explicitly, especially provider calls, GitHub writes, MCP runtime behavior, secret reads, auto-merge, and production claims.
- Link to related CompText docs instead of duplicating architecture.
- Avoid provider calls, network assumptions, and secret access unless an explicit future policy permits them.
