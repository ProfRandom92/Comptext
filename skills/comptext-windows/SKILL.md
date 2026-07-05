# comptext-windows

## Name
comptext-windows

## Purpose
Capture Windows-first local dry-run expectations for CompText development and validation.

## When to use
Use when preparing Windows commands, path handling, or local developer checks.

## Inputs
- PowerShell commands.
- Windows paths.
- Local Python and pytest commands.

## Outputs
- Windows-compatible command examples.
- Local validation notes.
- Path-safe documentation.

## Workflow
1. Prefer PowerShell-compatible commands.
2. Use repository-relative paths in docs and code.
3. Validate Python commands from the repository root.
4. Avoid shell behavior that depends on Unix-only tools.

## Safety rules
- Do not run destructive commands.
- Do not inspect raw environment variables.
- Do not start gateway or MCP servers.
- Do not write outside the repository.

## Validation checklist
- Commands run from `C:\Users\contr\dev\Comptext`.
- Tests use portable `pathlib` paths.
- Documentation includes local-only examples.

## Anti-patterns
- Hardcoding machine-specific secrets paths.
- Using shell commands that delete or move repository content.
- Assuming a Unix shell runtime.
