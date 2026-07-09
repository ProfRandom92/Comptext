# CompText TUI Workbench

The CompText TUI Workbench is an Ink/TypeScript terminal workbench that provides a local-only frontend for verified Python backend commands. It allows developers to run health checks, verify evidence chains, and validate workspaces in both interactive TTY mode and non-interactive slash-command mode.

> [!NOTE]
> CompText TUI is currently an offline verification workbench, not a full multi-panel terminal workspace. It does not call remote API providers, read environment secrets, start active MCP servers, or trigger background hooks.

---

## Safety Model & Repository Boundaries

The TUI workbench adheres strictly to the repository boundaries:
- **Sandbox Containment**: No network calls, GitHub API requests, or active MCP server bindings.
- **Secrets Protection**: Zero reading of `.env` files or environment variables.
- **Local Handoffs**: All state changes are stored locally in mock snapshots or verification logs.

---

## Requirements

- **Node.js**: >= 18.x
- **Python**: >= 3.10 (to execute backend CLI commands)
- **CompText CLI**: Installed and configured locally

---

## Installation

1. Navigate to the TUI directory:
   ```bash
   cd comptext-tui
   ```
2. Install local dependencies:
   ```bash
   npm install
   ```

---

## Available Scripts

- `npm run build`: Compile TypeScript files under `src/` to `dist/`.
- `npm run typecheck`: Run the compiler without emitting files to verify types.
- `npm run dev`: Build and run the interactive TUI workbench.

---

## Interactive Mode

To start the interactive key-driven command workbench, run:
```bash
npm run dev
```
Use the keyboard to trigger backend checks:
- **[S]** Status Screen
- **[D]** Doctor Diagnostics
- **[V]** Local Verify Screen
- **[W]** Workspace Validation
- **[E]** Evidence Verify (Sample)
- **[Q]** Quit TUI

---

## Non-Interactive Slash-Command Mode

Execute individual backend commands directly through slash arguments without rendering the terminal UI:
```bash
node dist/cli.js <slash-command>
```

### Supported Slash Commands
- `/help`: Print the help message guide and exit.
- `/status`: Run the `comptext status --dry-run` Python command.
- `/doctor`: Run the `comptext doctor --dry-run` Python command.
- `/validate workspace`: Validate workspace snapshots against JSON schemas.
- `/evidence verify`: Verify the cryptographic evidence log chain.
- `/gateway health`: Verify local mock gateway routes.
- `/run sample`: Execute a sample dry-run orchestration process.
- `/clear`: Clear the console window.
- `/quit`: Exit the workbench.

### Error Behavior
If an unrecognized command is entered, the workbench prints a standardized JSON error block to `stderr` and exits with status code `1`:
```json
{
  "error": {
    "message": "Unrecognized slash command: /invalid-command",
    "type": "UnrecognizedCommandError"
  },
  "ok": false
}
```

---

## References

- Backend CLI Contract: [`comptext-tui/docs/cli-contract.md`](docs/cli-contract.md)
- Live Verification Report: [`comptext-tui/docs/verification-report.md`](docs/verification-report.md)
- Modular Panel Roadmap: [`comptext-tui/docs/panel-tui-roadmap.md`](docs/panel-tui-roadmap.md)

---

## Terminal Demo Tape

The terminal demo commands and timing are specified in [`demo/comptext-tui-demo.tape`](demo/comptext-tui-demo.tape).

> [!TIP]
> **To render the demo locally as a GIF:**
> Ensure you have [VHS](https://github.com/charmbracelet/vhs) installed, then run:
> ```bash
> vhs comptext-tui/demo/comptext-tui-demo.tape
> ```
> *Note: Headless Chrome and ttyd are required by VHS to render the `.gif` asset.*

---

## Known Limitations & Future Roadmap

- **Interactive TTY Requirement**: The interactive menu requires a fully interactive raw-mode TTY process and will fail gracefully if run inside headless/CI pipelines (use slash commands instead).
- **Roadmap**: Planned enhancements include dividing the interface into modular, concurrent components (such as `ChatPanel`, `StatusDashboard`, `FileBrowser`, and `EvidenceViewer`). See the [TUI Roadmap](docs/panel-tui-roadmap.md) for future iteration plans.
