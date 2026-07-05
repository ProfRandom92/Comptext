# comptext-security

## Name
comptext-security

## Purpose
Maintain CompText safety boundaries during local dry-run development.

## When to use
Use when reviewing changes for provider safety, evidence safety, secret handling, or dry-run boundaries.

## Inputs
- Repository diffs.
- Local schemas and examples.
- Tests for unsafe states and secret patterns.

## Outputs
- Safety review notes.
- Validation failures for unsafe manifests.
- Recommendations limited to local preparation.

## Workflow
1. Check that changes stay local and dry-run-first.
2. Scan text fixtures and manifests for obvious credential patterns.
3. Confirm provider states do not imply live availability.
4. Confirm evidence examples are synthetic or redacted.

## Safety rules
- Do not read or print secrets.
- Do not make production security, compliance, or forensic claims.
- Do not activate providers, gateways, MCP servers, or hooks.
- Do not store unredacted provider payloads.

## Validation checklist
- Forbidden plugin statuses are absent.
- Secret-like patterns are absent from docs and manifests.
- Provider activation flags are absent.

## Anti-patterns
- Claiming compliance from local tests.
- Enabling provider gateway behavior from manifests.
- Logging credentials during validation.
