# COMPTEXT Plugin System

The initial CompText plugin system is a preparation-only manifest layer. Plugin manifests describe planned local capabilities, referenced skills, schemas, checks, and safety rules.

All initial plugin manifests use status `experimental`. This status is intentionally not a provider-ready or production-ready signal.

## Current Boundaries

- No plugin starts a gateway.
- No plugin starts an MCP runtime.
- No plugin enables provider calls.
- No plugin stores secrets or credentials.
- No plugin claims production security, compliance, or forensic readiness.

## Validation

Plugin manifests are JSON files under `plugins/*/plugin.json`. They must match `schemas/plugin.schema.json`, reference existing skill files, and keep status set to `experimental`.

Run local tests from the repository root:

```powershell
$env:PYTHONPATH="."; python -m pytest -q tests
```
