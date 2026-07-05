# Copilot instructions for CompText

CompText is a local AI orchestration platform for software engineering. Keep suggestions aligned with the local dry-run MVP and the seven-layer architecture: Terminal OS / UI, Runtime, Gateway, Agent Bus, AIR, Evidence, and Memory / Knowledge Graph.

Use `CompText` for the product, `comptext` for repo/package/CLI, and `COMPTEXT` for constants and document titles. Avoid legacy names, competition-era framing, and production-readiness claims.

Do not suggest code that calls providers, starts a gateway server, reads secrets, logs raw environment variables, embeds API keys, performs destructive actions, or presents mock/stub providers as complete features.

Prioritize these dry-run commands:

```bash
comptext doctor --dry-run
comptext validate schemas --dry-run
comptext providers list --dry-run
comptext evidence verify --sample
comptext run sample --dry-run
```

Evidence must remain redacted and must not include secrets, hidden chain-of-thought, raw environment variables, or unredacted provider payloads.
