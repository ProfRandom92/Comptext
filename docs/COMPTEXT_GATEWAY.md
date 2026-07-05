# COMPTEXT GATEWAY

This document defines the preparation-stage Gateway boundary for CompText.

## Current status

Gateway v0 is a deterministic local dry-run scaffold. It prepares the shape of future provider routing without starting a server, binding ports, reading secrets or environment variables, or performing live provider calls.

## Local dry-run module

The local scaffold lives in `modules/gateway/` and exposes pure helper functions:

- `get_gateway_health(...)`
- `list_gateway_models(...)`
- `normalize_gateway_request(...)`
- `dry_run_gateway_response(...)`

All functions currently support dry-run mode only. Unsupported input types are rejected before any response is produced.

## Planned local routes

Gateway v0 reports the planned local route surfaces as contract metadata only:

- `GET /health`
- `GET /v1/models`
- `POST /v1/messages`
- `POST /v1/responses`
- `POST /v1/chat/completions`

These routes are not active HTTP endpoints in v0.

## CLI commands

```bash
comptext gateway health --dry-run
comptext gateway models --dry-run
comptext gateway sample --dry-run
```

The commands output JSON and exit successfully when the dry-run result is `ok: true`.

## Model listing

`comptext gateway models --dry-run` returns safe placeholder model descriptors only. The scaffold does not call provider APIs, inspect credentials, read environment variables, or infer real availability.

Current placeholder state:

- `id`: `comptext-dry-run-model`
- `provider`: `comptext-local`
- `state`: `not_configured`
- `capabilities`: `text`, `tools_planned`

## Request normalization

The normalizer accepts a request object and returns the CompText dry-run shape:

```json
{
  "mode": "dry-run",
  "provider": "comptext-local",
  "model": "comptext-dry-run-model",
  "messages": [],
  "tools": [],
  "metadata": {}
}
```

Validation is intentionally narrow:

- request root must be an object,
- `model` must be a string when provided,
- `messages` must be a list when provided,
- `tools` must be a list when provided,
- `metadata` must be an object when provided.

## Deferred routing

Future live provider routing is deferred. Gateway v0 does not implement FastAPI, Flask, HTTP serving, healthchecks, MCP runtime startup, model calls, provider calls, or credential access.

## Safety rules

- Bind future local development servers to `127.0.0.1` by default.
- Do not expose secrets, raw provider payloads, or raw environment variables.
- Do not mark a provider as `available` without a real healthcheck.
- Do not implement live provider calls in the local dry-run MVP.
- Treat route contracts and stubs as contracts, not production functionality.

## Next safe step

Keep Gateway v0 local-only while expanding contract tests and schemas. Do not implement live routing until provider healthchecks, secrets handling, Evidence redaction, and explicit approval gates are designed and validated.
