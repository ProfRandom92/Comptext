# comptext-schema-validation

## Name
comptext-schema-validation

## Purpose
Validate local CompText JSON schemas and example fixtures without external sources.

## When to use
Use when adding or changing schemas, local examples, or schema validation tests.

## Inputs
- Files under `schemas/`.
- Files under `examples/`.
- Local JSON Schema validation library.

## Outputs
- JSON parse results.
- Schema validity results.
- Example validation results.

## Workflow
1. Load schema files from the local repository.
2. Check each schema as valid JSON Schema.
3. Validate matching local examples.
4. Add or update focused tests.

## Safety rules
- Do not fetch schemas from remote URLs.
- Do not validate provider payloads from live services.
- Do not include secrets or raw environment data in examples.

## Validation checklist
- Schema files parse as JSON.
- Example files parse as JSON.
- Tests fail on invalid or unsafe status values.

## Anti-patterns
- Network-backed schema resolution.
- Storing provider responses as fixtures.
- Allowing plugin or provider states that imply live availability.
