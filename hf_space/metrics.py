from __future__ import annotations

from typing import Iterable

from safety_checks import SafetyCheck


def summarize_checks(checks: Iterable[SafetyCheck]) -> dict:
    checks = list(checks)
    passed = sum(1 for check in checks if check.passed)
    return {
        "passed": passed,
        "total": len(checks),
        "score_percent": round((passed / len(checks) * 100) if checks else 100.0, 2),
        "details": [check.to_dict() for check in checks],
    }
