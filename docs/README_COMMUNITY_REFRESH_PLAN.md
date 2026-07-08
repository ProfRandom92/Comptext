# README Community Refresh Plan

> [!NOTE]
> This is a local planning reference note for a potential future community README refresh. It is not part of the active workspace setup and does not require downloading or installing any external packages or packs to run the local dry-run MVP.

## Source Pack Reference

- Local draft pack (optional reference): `comptext_readme_community_pack.zip`
- Recommended branch from pack: `docs/community-readme`
- Pack status notes:
  - Figma links are available as optional references.
  - Ace Knowledge Graph timed out; use `ace-knowledge-graph.json` only as a local draft/source.
  - GitHub was not updated directly.

## Available Inputs

- `README.community-draft.md`
- `mermaid/architecture.mmd`
- `mermaid/cryptographic-evidence-chain.mmd`
- `mermaid/plugin-handoff-flow.mmd`
- `mermaid/roadmap-matrix.mmd`
- `mermaid/readme-structure.mmd`
- `mermaid/safety-contract-matrix.mmd`
- `mermaid/capability-matrix.mmd`
- `figma-links.md`
- `ace-knowledge-graph.json`
- `codex-local-readme-prompt.txt`

## Proposed Scope

- Update `README.md` only unless a small docs index link is necessary.
- Add or tighten community-facing sections for:
  - What CompText is.
  - Architecture.
  - Cryptographic evidence model.
  - Capability matrix.
  - Safety contract.
  - PR Review Memory.
  - Local dry-run commands.
  - Roadmap.
- Use Mermaid diagrams only when they remain readable in GitHub Markdown.
- Use Figma links only as optional reference links if they fit naturally.

## Guardrails

- Do not claim releases, production readiness, live provider routing, live MCP runtime, automatic GitHub behavior, compliance, legal proof, or forensic certainty.
- Do not push, open PRs, merge, enable auto-merge, call GitHub APIs, perform provider calls, or read secrets.
- Stop before `git fetch` unless explicitly approved.
- Keep the README refresh scoped and reviewable.

## Validation

Run:

```bash
python -m pytest
git diff --check
```

Also run markdownlint if available.

## Suggested Next Batch

Start from a clean branch named `docs/community-readme`, inspect the pack locally, draft the README changes, validate, and make one local commit only.
