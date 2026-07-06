"""Deterministic local renderer for PR Review Memory handoffs."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any


REQUIRED_FIELDS = ("repository", "pr_number", "branch", "head_sha", "validation_summary", "next_action")
DIFF_MARKER_PREFIXES = ("diff --git", "index ", "@@", "+++", "---")
SECRET_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)"
)


def render_pr_review_memory_handoff(data: dict[str, Any]) -> str:
    """Render structured PR review memory as compact Token Saver handoff markdown."""

    if not isinstance(data, dict):
        raise TypeError("PR review memory data must be a dictionary.")

    missing = [field for field in REQUIRED_FIELDS if _is_empty(data.get(field))]
    if missing:
        raise ValueError(f"Missing required PR review memory field(s): {', '.join(missing)}")

    lines = [
        "# PR Review Memory",
        "",
        f"Repository: {_clean_text(data['repository'])}",
        f"PR: {_format_pr(data['pr_number'], data.get('pr_url'))}",
        f"Branch: {_clean_text(data['branch'])}",
        f"Head SHA: {_clean_text(data['head_sha'])}",
    ]
    if not _is_empty(data.get("status")):
        lines.append(f"Review status: {_clean_text(data['status'])}")

    _append_item_section(lines, "Actionable comments", data.get("actionable_items"))
    _append_item_section(lines, "Fixes applied", data.get("completed_fixes"))
    _append_validation(lines, data.get("validation_summary"))
    _append_item_section(lines, "Resolved threads", data.get("resolved_items"))
    _append_item_section(lines, "Unresolved threads", data.get("unresolved_items"))
    _append_merge_readiness(lines, data.get("merge_readiness"))
    lines.append(f"Next action: {_clean_text(data['next_action'])}")

    return "\n".join(lines).rstrip() + "\n"


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _clean_text(value: Any) -> str:
    text = str(value)
    kept_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if any(stripped.startswith(prefix) for prefix in DIFF_MARKER_PREFIXES):
            continue
        kept_lines.append(stripped)
    cleaned = " ".join(part for part in kept_lines if part)
    cleaned = SECRET_PATTERN.sub(lambda match: f"{match.group(1)}=<redacted>", cleaned)
    return cleaned


def _format_pr(pr_number: Any, pr_url: Any) -> str:
    number = _clean_text(pr_number)
    if not number.startswith("#"):
        number = f"#{number}"
    if _is_empty(pr_url):
        return number
    return f"{number} ({_clean_text(pr_url)})"


def _append_item_section(lines: list[str], label: str, items: Any) -> None:
    normalized = _normalize_items(items)
    if not normalized:
        return
    rendered_items = [_render_item(item) for item in normalized]
    rendered_items = [item for item in rendered_items if item]
    if not rendered_items:
        return
    lines.append(f"{label}:")
    for rendered in rendered_items:
        lines.append(f"- {rendered}")


def _normalize_items(items: Any) -> list[Any]:
    if _is_empty(items):
        return []
    if isinstance(items, Iterable) and not isinstance(items, (str, bytes, Mapping)):
        return list(items)
    return [items]


def _render_item(item: Any) -> str:
    if isinstance(item, Mapping):
        parts: list[str] = []
        thread_id = item.get("thread_id") or item.get("id")
        if not _is_empty(thread_id):
            parts.append(str(thread_id))
        file_path = item.get("file")
        if not _is_empty(file_path):
            parts.append(_clean_text(file_path))
        files = item.get("files")
        if isinstance(files, Iterable) and not isinstance(files, (str, bytes, Mapping)):
            rendered_files = ", ".join(_clean_text(file) for file in files if not _is_empty(file))
            if rendered_files:
                parts.append(rendered_files)
        summary = item.get("summary") or item.get("reason") or item.get("status")
        if not _is_empty(summary):
            parts.append(_clean_text(summary))
        return " - ".join(part for part in parts if part)
    return _clean_text(item)


def _append_validation(lines: list[str], validation: Any) -> None:
    if _is_empty(validation):
        return
    if isinstance(validation, Mapping):
        parts = [f"{_clean_text(command)}: {_clean_text(status)}" for command, status in sorted(validation.items())]
        if parts:
            lines.append(f"Validation: {'; '.join(parts)}")
        return
    if isinstance(validation, Iterable) and not isinstance(validation, (str, bytes)):
        parts = [_clean_text(item) for item in validation if not _is_empty(item)]
        if parts:
            lines.append(f"Validation: {'; '.join(parts)}")
        return
    rendered = _render_item(validation)
    if rendered:
        lines.append(f"Validation: {rendered}")


def _append_merge_readiness(lines: list[str], readiness: Any) -> None:
    if _is_empty(readiness):
        return
    if isinstance(readiness, Mapping):
        status = readiness.get("status")
        reason = readiness.get("reason")
        parts = []
        if not _is_empty(status):
            parts.append(_clean_text(status))
        if not _is_empty(reason):
            parts.append(_clean_text(reason))
        if parts:
            lines.append(f"Merge readiness: {' - '.join(parts)}")
        return
    lines.append(f"Merge readiness: {_clean_text(readiness)}")
