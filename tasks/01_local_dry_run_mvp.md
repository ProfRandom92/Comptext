# Task 01: Local dry-run MVP

## Goal

Implement the smallest safe CompText MVP as local dry-run commands only.

## Commands

```bash
comptext doctor --dry-run
comptext validate schemas --dry-run
comptext providers list --dry-run
comptext evidence verify --sample
comptext run sample --dry-run
```

## Constraints

- No provider API calls.
- No gateway server startup.
- No MCP runtime startup.
- No API keys or secrets.
- No destructive commands.
- No production security, compliance, or forensic claims.

## Expected outputs

- Doctor: local repository/environment summary with redacted-safe metadata.
- Schema validation: JSON schema parse and example validation.
- Provider list: provider registry display with only safe states.
- Evidence verify: sample hash-chain verification.
- Run sample: synthetic Run -> Plan -> Execution -> Evidence -> Replay -> Verify transcript.

## Acceptance criteria

The commands run locally, are deterministic, and can be tested without network access or secrets.
