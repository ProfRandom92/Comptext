# comptext-dry-run-cli

## Name
comptext-dry-run-cli

## Purpose
Guide implementation and validation of local-only CompText CLI dry-run commands.

## When to use
Use when adding or testing `comptext doctor`, `comptext validate`, `comptext providers`, `comptext evidence`, or `comptext run` dry-run commands.

## Inputs
- CLI arguments.
- Local examples.
- Local schemas.
- Synthetic dry-run data.

## Outputs
- Deterministic terminal output.
- Exit codes for local checks.
- Unit-testable command dispatch.

## Workflow
1. Add argparse dispatch in `modules/cli/cli_entrypoint.py`.
2. Route command behavior to a local module.
3. Print concise dry-run summaries.
4. Add CLI dispatch tests.
5. Run compile and pytest locally.

## Safety rules
- Require explicit dry-run or sample flags.
- Do not call providers, gateways, MCP servers, or network endpoints.
- Do not read secrets or raw environment variables.
- Do not write runtime output outside local examples or tests.

## Validation checklist
- Command works through `python -m modules.cli.cli_entrypoint`.
- Tests cover dispatch and output markers.
- No command starts a server or performs a healthcheck.

## Anti-patterns
- Hidden network calls in command handlers.
- Treating sample output as a completed feature.
- Reading environment variables for provider credentials.
