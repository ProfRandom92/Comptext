from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BRIDGE = ROOT / ".agents" / "skills" / "pr-review-memory" / "SKILL.md"


def test_pr_review_memory_skill_bridge_exists() -> None:
    assert BRIDGE.exists()


def test_pr_review_memory_skill_bridge_references_workflow() -> None:
    text = BRIDGE.read_text(encoding="utf-8")

    assert "PR Review Memory" in text
    assert "Token Saver" in text or "comptext-token-saver" in text

    for required_field in (
        "PR number",
        "Branch",
        "Head SHA",
        "Validation",
        "Next action",
    ):
        assert required_field in text


def test_pr_review_memory_skill_bridge_avoids_runtime_claims() -> None:
    text = BRIDGE.read_text(encoding="utf-8").lower()

    forbidden_claims = (
        "implements an mcp runtime",
        "makes provider calls",
        "calls provider apis",
        "writes github state",
        "github write behavior",
        "enables auto-merge",
        "production-ready",
    )

    for claim in forbidden_claims:
        assert claim not in text
