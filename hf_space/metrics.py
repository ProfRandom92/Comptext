from __future__ import annotations

from typing import Iterable

from safety_checks import SafetyCheck


def summarize_checks(checks: Iterable[SafetyCheck]) -> dict:
    checks = list(checks)
    relevant = [check for check in checks if check.relevant]
    passed = sum(1 for check in relevant if check.passed)
    score = (passed / len(relevant) * 100) if relevant else 100.0
    return {
        "passed": passed,
        "total": len(relevant),
        "all_required_preserved": all(check.passed for check in relevant),
        "score_percent": round(score, 2),
        "details": [check.to_dict() for check in checks],
    }
