from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass
class SafetyCheck:
    name: str
    passed: bool
    expected: list[str]
    preserved: list[str]
    missing: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


NEGATIONS = {"not", "no", "never", "without", "don't", "do not", "must not", "kein", "keine", "keinen", "nicht", "niemals", "ohne", "darf nicht"}


def _preservation_check(name: str, items: Iterable[str], compressed: str) -> SafetyCheck:
    expected = sorted({item for item in items if item})
    lower = compressed.lower()
    preserved = [item for item in expected if item.lower() in lower]
    missing = [item for item in expected if item.lower() not in lower]
    return SafetyCheck(name, not missing, expected, preserved, missing)


def extract_negations(text: str) -> set[str]:
    lower = text.lower()
    return {term for term in NEGATIONS if term in lower}


def extract_cli_flags(text: str) -> set[str]:
    return set(re.findall(r"(?<!\w)--?[a-zA-Z0-9][\w-]*", text))


def extract_file_paths(text: str) -> set[str]:
    patterns = [r"(?:[A-Za-z]:\\(?:[^\\\s]+\\)*[^\\\s]+)", r"(?:/(?:[^/\s]+/)*[^/\s]+)", r"(?:[\w.-]+/)+[\w.-]+"]
    found: set[str] = set()
    for pattern in patterns:
        found.update(re.findall(pattern, text))
    return found


def extract_json_keys(text: str) -> set[str]:
    return set(re.findall(r'["\']([A-Za-z_][A-Za-z0-9_.-]*)["\']\s*:', text))


def extract_versions(text: str) -> set[str]:
    return set(re.findall(r"\bv?\d+(?:\.\d+){1,3}(?:[-+][A-Za-z0-9.-]+)?\b", text))


def extract_code_symbols(text: str) -> set[str]:
    candidates = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b", text)
    return {item for item in candidates if "_" in item or any(ch.isupper() for ch in item[1:])}


def run_safety_checks(original: str, compressed: str) -> list[SafetyCheck]:
    return [
        _preservation_check("Negations", extract_negations(original), compressed),
        _preservation_check("CLI flags", extract_cli_flags(original), compressed),
        _preservation_check("File paths", extract_file_paths(original), compressed),
        _preservation_check("JSON keys", extract_json_keys(original), compressed),
        _preservation_check("Versions", extract_versions(original), compressed),
        _preservation_check("Code symbols", extract_code_symbols(original), compressed),
    ]
