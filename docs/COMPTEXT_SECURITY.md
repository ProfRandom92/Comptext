# COMPTEXT SECURITY

This document defines the preparation-stage security baseline for CompText.

## Scope

CompText is not a production security, compliance, or forensic product at this stage. Security work in this repository is limited to local-first guardrails, redaction rules, approval boundaries, and non-destructive validation.

## Hard rules

- Do not read, print, persist, or log secrets.
- Do not store API keys, provider tokens, credentials, raw environment variables, hidden chain-of-thought, or unredacted provider payloads in Evidence.
- Do not perform live provider calls in the local dry-run MVP.
- Do not start a gateway server as part of bootstrap work.
- Do not run destructive commands.
- Do not claim production security, compliance, certification, or forensic readiness.

## Evidence baseline

Evidence may store redacted metadata, hashes, tool summaries, synthetic test results, and approved diffs. Any future Evidence implementation must treat redaction and approval as first-class requirements.

## Provider baseline

Provider states are limited to `not_configured`, `disabled`, or `experimental` until real healthchecks and explicit approval exist.
