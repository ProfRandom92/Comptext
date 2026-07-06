import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "pr-review-memory"
SAMPLE_JSON = PLUGIN / "examples" / "pr-review-memory.sample.json"
SAMPLE_MARKDOWN = PLUGIN / "examples" / "token-saver-handoff.sample.md"


def _load_renderer():
    spec = importlib.util.spec_from_file_location("pr_review_memory_renderer", PLUGIN / "renderer.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_renderer_converts_sample_json_to_compact_markdown() -> None:
    renderer = _load_renderer()
    data = json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))

    markdown = renderer.render_pr_review_memory_handoff(data)

    assert isinstance(markdown, str)
    assert markdown == SAMPLE_MARKDOWN.read_text(encoding="utf-8")
    assert "Repository: ProfRandom92/Comptext" in markdown
    assert "PR: #17" in markdown
    assert "Branch: plugin/pr-review-memory-renderer-v0" in markdown
    assert "Head SHA: dryrun1234567890abcdef1234567890abcdef1234" in markdown
    assert "Validation:" in markdown
    assert "Next action:" in markdown


def test_renderer_rejects_non_dict_input() -> None:
    renderer = _load_renderer()

    with pytest.raises(TypeError):
        renderer.render_pr_review_memory_handoff(["not", "a", "dict"])


def test_renderer_rejects_missing_required_fields() -> None:
    renderer = _load_renderer()

    with pytest.raises(ValueError, match="repository"):
        renderer.render_pr_review_memory_handoff(
            {
                "pr_number": 17,
                "branch": "plugin/pr-review-memory-renderer-v0",
                "head_sha": "abc123",
                "status": "review_in_progress",
                "next_action": "Continue review.",
            }
        )


def test_renderer_omits_empty_optional_sections() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "status": "ready_for_review",
            "actionable_items": [],
            "completed_fixes": [],
            "validation_summary": {},
            "unresolved_items": [],
            "merge_readiness": {},
            "next_action": "Wait for review.",
        }
    )

    assert "Actionable comments:" not in markdown
    assert "Fixes applied:" not in markdown
    assert "Validation:" not in markdown
    assert "Unresolved threads:" not in markdown
    assert "Merge readiness:" not in markdown
    assert "Next action: Wait for review." in markdown


def test_renderer_omits_diff_markers_and_redacts_secret_like_values() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "status": "review_in_progress",
            "actionable_items": [
                {
                    "thread_id": "thread-1",
                    "summary": "diff --git a/file b/file\n@@ hunk\nUse token=raw-secret-value only in tests.",
                }
            ],
            "validation_summary": {"python -m pytest": "passed"},
            "next_action": "Continue without password=raw-secret-value.",
        }
    )

    assert "raw-secret-value" not in markdown
    assert "token=<redacted>" in markdown
    assert "password=<redacted>" in markdown
    assert "diff --git" not in markdown
    assert "@@ hunk" not in markdown
