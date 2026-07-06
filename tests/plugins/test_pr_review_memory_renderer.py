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
                "validation_summary": {"python -m pytest": "passed"},
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
            "validation_summary": {"python -m pytest": "passed"},
            "unresolved_items": [],
            "merge_readiness": {},
            "next_action": "Wait for review.",
        }
    )

    assert "Actionable comments:" not in markdown
    assert "Fixes applied:" not in markdown
    assert "Validation:" in markdown
    assert "Unresolved threads:" not in markdown
    assert "Merge readiness:" not in markdown
    assert "Next action: Wait for review." in markdown


def test_renderer_accepts_minimal_valid_v0_input() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "validation_summary": "python -m pytest passed",
            "next_action": "Continue review.",
        }
    )

    assert "Repository: ProfRandom92/Comptext" in markdown
    assert "PR: #17" in markdown
    assert "Review status:" not in markdown
    assert "Validation: python -m pytest passed" in markdown
    assert "Next action: Continue review." in markdown


def test_renderer_accepts_full_valid_v0_input() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": "17",
            "pr_url": "https://example.invalid/pr/17",
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "status": "review_in_progress",
            "actionable_items": [{"thread_id": "thread-1", "file": "README.md", "summary": "Tighten docs."}],
            "completed_fixes": [{"files": {"b.py", "a.py"}, "summary": "Sorted files."}],
            "resolved_items": ["thread-2 resolved locally"],
            "unresolved_items": ["thread-3 requires reviewer input"],
            "validation_summary": {"git diff --check": "passed", "python -m pytest": "passed"},
            "merge_readiness": {"status": "blocked", "reason": "review pending"},
            "next_action": "Wait for review.",
        }
    )

    assert "PR: #17 (https://example.invalid/pr/17)" in markdown
    assert "Review status: review_in_progress" in markdown
    assert "Actionable comments:" in markdown
    assert "Fixes applied:" in markdown
    assert "a.py, b.py" in markdown
    assert "Resolved threads:" in markdown
    assert "Unresolved threads:" in markdown
    assert "Validation: git diff --check: passed; python -m pytest: passed" in markdown
    assert "Merge readiness: blocked - review pending" in markdown


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
                    "summary": (
                        "diff --git a/file b/file\n"
                        "index 111..222\n"
                        "--- a/file\n"
                        "+++ b/file\n"
                        "@@ hunk\n"
                        "Use token=raw-secret-value only in tests."
                    ),
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
    assert "index 111..222" not in markdown
    assert "--- a/file" not in markdown
    assert "+++ b/file" not in markdown
    assert "@@ hunk" not in markdown


def test_renderer_redacts_quoted_multi_word_secret_values() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "status": "review_in_progress",
            "actionable_items": ["Use token=\"multi word secret\" only in tests."],
            "validation_summary": {"python -m pytest": "passed"},
            "next_action": "Do not keep secret='another multi word value'.",
        }
    )

    assert "multi word secret" not in markdown
    assert "another multi word value" not in markdown
    assert "token=<redacted>" in markdown
    assert "secret=<redacted>" in markdown


def test_renderer_handles_general_iterable_items_as_bullets() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "status": "review_in_progress",
            "actionable_items": ("tuple item", "second tuple item"),
            "completed_fixes": ["list item"],
            "unresolved_items": {"set item"},
            "validation_summary": {"python -m pytest": "passed"},
            "next_action": "Continue review.",
        }
    )

    assert "- tuple item" in markdown
    assert "- second tuple item" in markdown
    assert "- list item" in markdown
    assert "- set item" in markdown


def test_renderer_sorts_unordered_set_items_for_stable_output() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "actionable_items": {"b set item", "a set item"},
            "validation_summary": {"python -m pytest": "passed"},
            "next_action": "Continue review.",
        }
    )

    assert markdown.index("- a set item") < markdown.index("- b set item")


def test_renderer_formats_iterable_validation_as_semicolon_text() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "status": "review_in_progress",
            "validation_summary": ["python -m pytest passed", "git diff --check passed"],
            "next_action": "Continue review.",
        }
    )

    assert "Validation: python -m pytest passed; git diff --check passed" in markdown


def test_renderer_handles_empty_text_after_splitlines_simplification() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "status": "review_in_progress",
            "actionable_items": [""],
            "validation_summary": {"python -m pytest": "passed"},
            "next_action": "Continue review.",
        }
    )

    assert "Actionable comments:" not in markdown
    assert "\n- \n" not in markdown
    assert "Next action: Continue review." in markdown


def test_renderer_treats_review_status_as_optional() -> None:
    renderer = _load_renderer()

    markdown = renderer.render_pr_review_memory_handoff(
        {
            "repository": "ProfRandom92/Comptext",
            "pr_number": 17,
            "branch": "plugin/pr-review-memory-renderer-v0",
            "head_sha": "abc123",
            "validation_summary": {"python -m pytest": "passed"},
            "next_action": "Continue review.",
        }
    )

    assert "Review status:" not in markdown
    assert "Validation: python -m pytest: passed" in markdown
