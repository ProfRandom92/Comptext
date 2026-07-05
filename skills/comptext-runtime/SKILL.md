# comptext-runtime

## Name
comptext-runtime

## Purpose
Guide local sample runtime flows that connect AIR Plans, Run Records, Evidence Events, Replay, and Verify.

## When to use
Use when adding or changing `comptext run sample --dry-run` or related local runtime examples.

## Inputs
- Local AIR Plan examples.
- Local Run Record examples.
- Synthetic Evidence Events.

## Outputs
- Local dry-run transcript.
- Synthetic Run Record.
- Verified synthetic hash-chain status.

## Workflow
1. Load a local AIR Plan.
2. Build an in-memory Run Record.
3. Build synthetic Evidence Events.
4. Verify the hash chain.
5. Print dry-run summary output.

## Safety rules
- Do not perform real execution or file edits.
- Do not call providers, gateways, MCP servers, or external services.
- Do not start background processes.
- Keep output deterministic.

## Validation checklist
- `run sample --dry-run` reports run id and plan id.
- Evidence event count is deterministic.
- Hash-chain status is verified locally.

## Anti-patterns
- Starting real agent execution.
- Writing runtime state outside local fixtures.
- Treating sample runs as production workflows.
