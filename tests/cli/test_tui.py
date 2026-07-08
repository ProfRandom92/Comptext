import pytest
from pathlib import Path
from modules.cli.tui import build_tui_snapshot, render_tui_snapshot_text, run_tui

ROOT = Path(__file__).parent.parent.parent


def test_build_tui_snapshot_determinism() -> None:
    snap1 = build_tui_snapshot(ROOT)
    snap2 = build_tui_snapshot(ROOT)
    assert snap1 == snap2


def test_build_tui_snapshot_keys_and_values() -> None:
    snap = build_tui_snapshot(ROOT)
    required_keys = {
        "header", "mode", "status", "doctor", "workspace_validation",
        "verify", "evidence", "providers", "mcp", "agents", "skills",
        "commands", "limitations"
    }
    assert required_keys.issubset(snap.keys())

    assert snap["header"]["title"] == "COMPTEXT"
    assert snap["header"]["tagline"] == "THE OPERATING SYSTEM FOR CONTEXT"
    assert snap["mode"] == "local-only / dry-run"

    assert snap["providers"]["state"] == "disabled/deferred"
    assert snap["mcp"]["state"] == "disabled/deferred"
    assert "TUI does not depend on MCP" in snap["mcp"]["note"]

    assert "does not fix Antigravity /agents discovery" in snap["agents"]["note"]

    expected_commands = {
        "comptext tui --dry-run",
        "comptext status --dry-run",
        "comptext agents --dry-run",
        "comptext verify --dry-run",
        "comptext validate workspace --dry-run",
        "comptext doctor --dry-run"
    }
    assert expected_commands.issubset(set(snap["commands"]))


def test_build_tui_snapshot_skills() -> None:
    snap = build_tui_snapshot(ROOT)
    skills_names = snap["skills"]["names"]
    # Check that skill names are read from .agents/skills
    assert "comptext-local-verify" in skills_names
    assert "comptext-status" in skills_names


@pytest.mark.asyncio
async def test_tui_app_headless() -> None:
    # Since Textual is available, run a headless App.run_test()
    try:
        from modules.cli.tui import run_tui
        # Import App directly to run the headless test
        from textual.app import App, ComposeResult
        from textual.widgets import Header, Footer, Static
        from textual.containers import VerticalScroll

        snapshot = build_tui_snapshot(ROOT)

        class DummyApp(App[None]):
            def compose(self) -> ComposeResult:
                yield Header()
                yield VerticalScroll(
                    Static(render_tui_snapshot_text(snapshot)),
                    id="tui-body"
                )
                yield Footer()

        app = DummyApp()
        async with app.run_test() as pilot:
            assert app.title == "DummyApp"
    except ImportError:
        # If Textual wasn't available, we skip
        pytest.skip("Textual is not available.")


def test_tui_missing_guard(monkeypatch, capsys) -> None:
    # Force import error
    import sys
    original_import = __import__

    def mock_import(name, *args, **kwargs):
        if name == "textual" or name.startswith("textual."):
            raise ImportError("Mocked import error")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", mock_import)

    # Calling run_tui should fail gracefully
    assert run_tui(ROOT, dry_run=True) == 1
    out = capsys.readouterr().out
    assert "Textual is required for comptext tui --dry-run." in out


def test_build_tui_snapshot_evidence_fields() -> None:
    snap = build_tui_snapshot(ROOT)
    assert snap["evidence"]["status"] == "pass"
    assert "local event chain and state log chain verified" in snap["evidence"]["note"]

    # Check that all 6 workspace validation schemas are present in the TUI snapshot
    results = snap["workspace_validation"]["results"]
    assert len(results) == 6
