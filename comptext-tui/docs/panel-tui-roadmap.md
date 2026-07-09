# CompText Modular Panel TUI Roadmap

This roadmap defines the future evolutionary phases to transition the current local verification workbench into a rich, modular panel-based Ink TUI.

---

## Phase 1: Documentation & Demo Handoff (`docs/tui-readme-demo`)
- **Scope**: Create `README.md`, `comptext-tui-demo.tape`, and `panel-tui-roadmap.md` to define baseline workbench features, safety containment rules, and local development commands.
- **Files Affected**:
  - `comptext-tui/README.md`
  - `comptext-tui/demo/comptext-tui-demo.tape`
  - `comptext-tui/docs/panel-tui-roadmap.md`
  - `README.md` (root reference)
- **Validation Commands**:
  - `git diff --check`
  - `python -m pytest`
- **Safety Boundaries**: No production releases, no external PR merges, no remote pushes.
- **Explicit Non-Goals**: No code changes to `cli.tsx` or backend modules.

---

## Phase 2: Command Client Extraction (`refactor/tui-command-client`)
- **Scope**: Extract `child_process.exec` execution logic and the command list out of `src/cli.tsx` into a modular, unit-testable command runner helper (`src/commandClient.ts`).
- **Files Affected**:
  - `comptext-tui/src/cli.tsx`
  - `comptext-tui/src/commandClient.ts` (new)
  - `comptext-tui/src/commandClient.test.ts` (new)
- **Validation Commands**:
  - `npm --prefix comptext-tui run typecheck`
  - `npm --prefix comptext-tui run build`
  - `npm --prefix comptext-tui run test`
- **Safety Boundaries**: Strictly local execution only. No hardcoded backend successes, no remote provider mock calls.
- **Explicit Non-Goals**: No UI layout changes or panel divisions.

---

## Phase 3: Chat Panel (`feat/tui-chat-panel`)
- **Scope**: Design and implement an interactive `ChatPanel` component using Ink text input, displaying structured chat history and capturing input local queries.
- **Files Affected**:
  - `comptext-tui/src/components/ChatPanel.tsx` (new)
  - `comptext-tui/src/cli.tsx`
- **Validation Commands**:
  - `npm --prefix comptext-tui run typecheck`
  - `npm --prefix comptext-tui run build`
- **Safety Boundaries**: The panel is local-only. It must NOT start active LLM API provider calls or use network. It must gracefully report `experimental/not_configured` or call local mock gateways.
- **Explicit Non-Goals**: No real-time agent coordination or multi-agent orchestration.

---

## Phase 4: Status Dashboard (`feat/tui-status-dashboard`)
- **Scope**: Implement a `StatusDashboard` panel showing verified project files, environment boundaries (Providers, Network, GitHub, MCP), and running tasks.
- **Files Affected**:
  - `comptext-tui/src/components/StatusDashboard.tsx` (new)
  - `comptext-tui/src/cli.tsx`
- **Validation Commands**:
  - `npm --prefix comptext-tui run build`
- **Safety Boundaries**: Strictly read-only data rendering from the local Python doctor client. No state edits or network calls.
- **Explicit Non-Goals**: No active self-fixing or fixing doctor checks from the dashboard.

---

## Phase 5: Evidence Viewer (`feat/tui-evidence-viewer`)
- **Scope**: Implement an `EvidenceViewer` panel to explore evidence log chain root hashes, block indices, and cryptographic hashes.
- **Files Affected**:
  - `comptext-tui/src/components/EvidenceViewer.tsx` (new)
  - `comptext-tui/src/cli.tsx`
- **Validation Commands**:
  - `npm --prefix comptext-tui run build`
- **Safety Boundaries**: Local verification only. No modification of the log chain database from the UI.
- **Explicit Non-Goals**: No syncing log chains with remote servers or database writes.

---

## Phase 6: Workspace File Browser (`feat/tui-file-browser`)
- **Scope**: Implement a directory explorer panel allowing users to browse local files under the workspace root and choose contexts.
- **Files Affected**:
  - `comptext-tui/src/components/FileBrowser.tsx` (new)
  - `comptext-tui/src/cli.tsx`
- **Validation Commands**:
  - `npm --prefix comptext-tui run build`
- **Safety Boundaries**: Root containment boundary. The browser MUST NOT navigate outside the repository root.
- **Explicit Non-Goals**: No file edits, deletions, or write operations.

---

## Phase 7: Regression Testing (`test/tui-command-regressions`)
- **Scope**: Add automated integration tests that simulate keyboard inputs inside the Ink components, verifying key triggers correctly map to target backend commands.
- **Files Affected**:
  - `comptext-tui/tests/tui-regressions.test.tsx` (new)
- **Validation Commands**:
  - `npm --prefix comptext-tui run test`
- **Safety Boundaries**: Tests must run completely offline without side-effects.
- **Explicit Non-Goals**: No unit testing of the Python backend in the Node TUI tests.
