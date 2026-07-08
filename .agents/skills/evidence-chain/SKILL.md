---
name: evidence-chain
description: Design evidence schemas, validate serialization, and plan hash chains.
---

# Evidence Chain Skill

Draft and validate evidence event models, hash-chain sequences, and state log chains.

## Use when
- Designing JSON schemas for evidence events and run records (e.g. `schemas/`).
- Refining event serialization modules and formatting sample evidence logs.
- Implementing or validating local hash-chain verification routines.
- Planning local state log chains to link git commit hashes into the evidence chain.

## Do not use when
- Implementing live provider attestation or hosted cryptographic verification.
- Reading secrets or environment variables.
- Running live production executions beyond local dry-run samples.
- Making official compliance, legal, forensic, or certification claims.

## Inputs
- JSON Schema contracts: `schemas/evidence.v0.schema.json`.
- Sample run logs and state snapshots: `examples/`.
- Hashing and sequence libraries: `modules/evidence/`.

## Safety boundaries
- Bounded to offline dry-run verification and schema validation.
- No network connections or provider gateway calls.
- No compliance, legal, or forensic readiness claims.
- No auto-merge, pushes, or pull request creation.

## Workflow
1. Draft or refine evidence serialization schemas.
2. Validate mock workspace snapshot or run records against schema definitions.
3. Verify sequential hashing integrity of evidence logs.
4. Draft next-stage designs for linking git commit hashes directly to evidence blocks.

## Validation
- `comptext validate workspace --dry-run`
- `comptext validate schemas --dry-run`
- `python -m pytest tests/evidence`

## Final report
- Verification status (pass/fail), count of validated evidence events, sequence index state, and hash-chain integrity results.
