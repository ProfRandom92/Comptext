# COMPTEXT GATEWAY

This document defines the preparation-stage Gateway boundary for CompText.

## Current status

The Gateway is a design surface only. The bootstrap repository does not start a gateway server and does not perform live provider calls.

## Future local routes

Future Gateway work may define local contracts such as:

- `GET /health`
- `GET /v1/models`
- `POST /v1/messages`
- `POST /v1/responses`
- `POST /v1/chat/completions`
- `GET /admin`

These routes are not active features in the bootstrap stage.

## Safety rules

- Bind future local development servers to `127.0.0.1` by default.
- Do not expose secrets, raw provider payloads, or raw environment variables.
- Do not mark a provider as `available` without a real healthcheck.
- Do not implement live provider calls in the local dry-run MVP.
- Treat route contracts and stubs as contracts, not production functionality.

## Next safe step

Do not implement Gateway runtime yet. Complete the local dry-run CLI first: doctor, schema validation, provider registry listing, Evidence sample verification, and sample run dry-run.
