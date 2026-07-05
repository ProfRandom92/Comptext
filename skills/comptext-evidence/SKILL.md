# comptext-evidence

## Name
comptext-evidence

## Purpose
Build and verify synthetic Evidence hash chains for local dry-runs.

## When to use
Use when changing evidence sample generation, verification, or evidence CLI output.

## Inputs
- Synthetic Evidence Events.
- Redacted metadata.
- Local hash-chain verifier.

## Outputs
- Hash-chain verification status.
- Final synthetic hash.
- Local test coverage for tamper detection.

## Workflow
1. Build deterministic synthetic events.
2. Hash redacted event payload fields.
3. Verify sequence, previous hash, and event hash values.
4. Report concise verification status.

## Safety rules
- Do not store hidden chain-of-thought.
- Do not store secrets, API keys, tokens, or raw provider payloads.
- Do not claim forensic certainty.
- Keep evidence samples synthetic or redacted.

## Validation checklist
- Hash mismatch tests fail on tampering.
- Event sequence is checked.
- Output includes no raw credentials or provider payloads.

## Anti-patterns
- Treating synthetic evidence as forensic proof.
- Hashing raw secret-bearing payloads.
- Pulling live provider data into Evidence.
