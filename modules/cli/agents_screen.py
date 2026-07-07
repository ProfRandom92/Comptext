"""CompText local subagent inventory screen build helper."""

from __future__ import annotations

from pathlib import Path


def build_agents_screen(repo_root: Path) -> tuple[int, str]:
    """Build deterministic local subagent inventory screen text and return exit code."""
    lines = [
        "COMPTEXT LOCAL SUBAGENTS",
        "",
        "Mode: local-only / dry-run",
        "",
        "Subagents:",
        "  - validation-agent",
        "    Purpose: Validate committed workspace schemas and example JSON files.",
        "    Allowed Scope: schemas/, examples/workspace/, modules/validation/.",
        "    Forbidden Scope: network requests, provider APIs, Model Context Protocol (MCP).",
        "    Validation Command: python -m pytest tests/validation tests/cli",
        "",
        "  - evidence-agent",
        "    Purpose: Manage the evidence hash-chain and check optional workspace refs.",
        "    Allowed Scope: modules/evidence/ hash-chain verification and string pointer checks.",
        "    Forbidden Scope: embedding objects/payloads, network requests, provider APIs.",
        "    Validation Command: python -m pytest tests/evidence",
        "",
        "  - runtime-dryrun-agent",
        "    Purpose: Build deterministic dry-run sample events and assert zero resource access.",
        "    Allowed Scope: modules/runtime/ local sample execution summaries.",
        "    Forbidden Scope: network, LLM provider requests, binding ports.",
        "    Validation Command: python -m pytest tests/runtime",
        "",
        "  - pr-memory-agent",
        "    Purpose: Support local deterministic PR review-memory rendering.",
        "    Allowed Scope: plugins/pr-review-memory/ review markdown serialization.",
        "    Forbidden Scope: live GitHub writes/API requests.",
        "    Validation Command: python -m pytest tests/plugins",
        "",
        "  - docs-agent",
        "    Purpose: Create and edit repository architecture and workflow documentation.",
        "    Allowed Scope: docs/ markdown additions and updates.",
        "    Forbidden Scope: modifying the root README.md without approval.",
        "    Validation Command: git diff --check",
        "",
        "Routing Preview:",
        "  - validation: validation-agent (schemas/, examples/workspace/, modules/validation/)",
        "  - evidence: evidence-agent (modules/evidence/)",
        "  - runtime dry-run: runtime-dryrun-agent (modules/runtime/)",
        "  - PR memory: pr-memory-agent (plugins/pr-review-memory/)",
        "  - docs: docs-agent (docs/)",
        "",
        "Escalation:",
        "  - Stop on dirty working tree: Abort if git status is not clean before working.",
        "  - Stop on HEAD mismatch: Abort if actual HEAD commit differs from expected.",
        "  - Stop before provider/network/GitHub/MCP behavior: Block all non-local resource accesses.",
        "  - Stop before editing root README.md: Restrict changes to allowed doc paths only.",
        "",
        "Commands:",
        "  - comptext agents --dry-run",
        "  - comptext status --dry-run",
        "  - comptext validate workspace --dry-run",
        "  - comptext doctor --dry-run",
        "  - python -m pytest",
    ]

    return 0, "\n".join(lines)
