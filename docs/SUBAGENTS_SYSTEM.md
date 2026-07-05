# CompText Subagents System

Subagents are scoped workers for bounded tasks. They may operate on isolated tasks or dedicated worktrees in the future, but this repository currently documents the model only.

## Purpose

Subagents should help split work into reviewable units while preserving approvals, evidence, and user control.

Expected uses:

- focused code review
- test writing
- documentation updates
- schema validation
- security review
- provider contract inspection

## Proposed registry fields

```yaml
id: docs-maintainer
name: Documentation Maintainer
purpose: Keep operational and architecture docs current.
allowed_tools:
  - filesystem_read
  - filesystem_write
  - local_checks
required_skills:
  - docs
approval_level: local_only
evidence_required: true
output_contract: summary_validation_risks
```

Field meanings:

- `id`: stable machine-readable identifier.
- `name`: human-readable display name.
- `purpose`: bounded responsibility.
- `allowed_tools`: tools the subagent may use.
- `required_skills`: skills the subagent should load.
- `approval_level`: approval boundary for actions.
- `evidence_required`: whether evidence must be emitted.
- `output_contract`: expected result format.

## Boundaries

- Subagents do not bypass approvals.
- Subagents do not directly access secrets.
- Subagents must report uncertainty and blockers.
- Subagents must stay inside their assigned task and workspace scope.
