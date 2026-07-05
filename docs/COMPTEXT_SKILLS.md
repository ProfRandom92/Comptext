# COMPTEXT Skills

CompText skills are local guidance documents for dry-run development. They describe when to use a workflow, the expected inputs and outputs, safety rules, validation checks, and anti-patterns.

The initial skills cover bootstrap, dry-run CLI work, schema validation, provider registry safety, synthetic Evidence, runtime samples, Windows usage, and safety review.

These skills do not activate providers, start gateways, start MCP runtimes, read secrets, or claim production readiness.

## Validation

Skill files must include these headings:

- Name
- Purpose
- When to use
- Inputs
- Outputs
- Workflow
- Safety rules
- Validation checklist
- Anti-patterns

Run local tests from the repository root:

```powershell
$env:PYTHONPATH="."; python -m pytest -q tests
```
