# PR Review Memory Schema

`pr-review-memory.v0.schema.json` is the local v0 renderer input contract for `plugins/pr-review-memory/renderer.py`.

The schema documents the JSON shape used by `plugins/pr-review-memory/examples/pr-review-memory.sample.json` and covered by local tests. It is for examples, tests, and documentation. It is not live GitHub integration, not MCP runtime behavior, and not provider behavior.

Renderer v0 remains deterministic local behavior: it accepts structured review-memory dictionaries and returns compact Token Saver handoff markdown. Future schema changes require explicit compatibility tests so renderer input shape drift is visible during local validation.

Deferred behavior:

- live GitHub integration
- MCP runtime behavior
- automatic review resolution
- automatic merge behavior
- production behavior
