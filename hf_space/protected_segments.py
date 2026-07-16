from __future__ import annotations

import re
from dataclasses import dataclass

from safety_checks import extract_required_items

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])(?=\s+)|(?<=\n)")
_CODE_FENCE = re.compile(r"```[\s\S]*?```", re.MULTILINE)
_JSON_OBJECT = re.compile(r"\{[\s\S]*?\}|\[[\s\S]*?\]", re.MULTILINE)


@dataclass(frozen=True)
class Segment:
    text: str
    protected: bool
    reasons: tuple[str, ...]


def _reasons(text: str) -> tuple[str, ...]:
    reasons: list[str] = []
    required = extract_required_items(text)
    reasons.extend(name for name, items in required.items() if items)
    stripped = text.strip()
    if stripped.startswith(("```", "{", "[")):
        reasons.append("structured-block")
    if re.search(r"(^|\s)(git|python|node|npm|npx|pip|curl|docker)\s+", text, re.I):
        reasons.append("command")
    if "=" in text and re.search(r"\b[A-Z_][A-Z0-9_]*=", text):
        reasons.append("environment")
    return tuple(sorted(set(reasons)))


def split_segments(text: str) -> list[Segment]:
    if not text:
        return []

    protected_spans: list[tuple[int, int]] = []
    for pattern in (_CODE_FENCE, _JSON_OBJECT):
        protected_spans.extend((m.start(), m.end()) for m in pattern.finditer(text))
    protected_spans.sort()

    chunks: list[str] = []
    cursor = 0
    for start, end in protected_spans:
        if start > cursor:
            chunks.extend(part for part in _SENTENCE_SPLIT.split(text[cursor:start]) if part)
        chunks.append(text[start:end])
        cursor = max(cursor, end)
    if cursor < len(text):
        chunks.extend(part for part in _SENTENCE_SPLIT.split(text[cursor:]) if part)

    segments: list[Segment] = []
    for chunk in chunks:
        reasons = _reasons(chunk)
        segments.append(Segment(chunk, bool(reasons), reasons))
    return segments
