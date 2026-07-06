import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "pr-review-memory"


def test_pr_review_memory_manifest_is_safe_dry_run() -> None:
    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))

    assert manifest["name"] == "comptext-pr-review-memory"
    assert manifest["status"] == "dry-run"

    permissions = manifest["permissions"]
    for permission in (
        "network",
        "provider_calls",
        "github_write",
        "secrets",
        "filesystem_write",
    ):
        assert permissions[permission] is False


def test_pr_review_memory_json_examples_are_valid() -> None:
    for example in (
        PLUGIN / "examples" / "pr-review-input.sample.json",
        PLUGIN / "examples" / "pr-review-memory.sample.json",
    ):
        data = json.loads(example.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
