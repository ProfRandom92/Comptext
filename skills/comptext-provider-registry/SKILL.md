# comptext-provider-registry

## Name
comptext-provider-registry

## Purpose
Maintain the local provider registry sample with safe, non-live provider states.

## When to use
Use when adding provider registry examples, status validation, or provider list CLI output.

## Inputs
- `examples/provider/provider-registry-sample.json`.
- Provider registry schema.
- Local validation tests.

## Outputs
- Safe provider status display.
- Validation errors for forbidden states.
- Local-only registry examples.

## Workflow
1. Load the local provider registry example.
2. Validate provider entries and states.
3. Display provider names and safe states only.
4. Reject `available` and other live-ready states.

## Safety rules
- Allowed provider states are `not_configured`, `disabled`, and `experimental`.
- Do not run provider healthchecks.
- Do not read or print API keys.
- Do not imply provider readiness.

## Validation checklist
- `available` is rejected.
- Every provider entry has a name and safe state.
- CLI output does not include secrets or live status.

## Anti-patterns
- Adding mock providers as finished integrations.
- Treating `experimental` as enabled.
- Performing background healthchecks during list commands.
