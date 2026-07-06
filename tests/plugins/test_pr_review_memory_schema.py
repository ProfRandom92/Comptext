import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "pr-review-memory"
SCHEMA = PLUGIN / "schema" / "pr-review-memory.v0.schema.json"
SCHEMA_README = PLUGIN / "schema" / "README.md"
SAMPLE_JSON = PLUGIN / "examples" / "pr-review-memory.sample.json"


REQUIRED_V0_FIELDS = {
    "repository",
    "pr_number",
    "branch",
    "head_sha",
    "validation_summary",
    "next_action",
}


def _load_renderer():
    spec = importlib.util.spec_from_file_location("pr_review_memory_renderer", PLUGIN / "renderer.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pr_review_memory_schema_file_exists_and_loads() -> None:
    assert SCHEMA.exists()

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert schema["title"] == "CompText PR Review Memory Renderer Input v0"
    assert set(schema["required"]) == REQUIRED_V0_FIELDS
    assert schema["type"] == "object"


def test_sample_json_contains_required_v0_fields() -> None:
    sample = json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))

    assert REQUIRED_V0_FIELDS <= set(sample)
    for field in REQUIRED_V0_FIELDS:
        assert sample[field] not in ("", [], {})


def test_sample_json_matches_documented_required_field_contract() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    sample = json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))

    for field in schema["required"]:
        assert field in sample


def test_validation_summary_schema_documents_non_empty_values() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validation = schema["properties"]["validation_summary"]

    assert validation["minProperties"] == 1
    assert validation["minItems"] == 1
    assert validation["minLength"] == 1


@pytest.mark.parametrize("empty_value", [{}, [], ""])
def test_renderer_rejects_empty_validation_summary_values(empty_value) -> None:
    renderer = _load_renderer()
    sample = json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))
    sample["validation_summary"] = empty_value

    with pytest.raises(ValueError, match="validation_summary"):
        renderer.render_pr_review_memory_handoff(sample)


def test_renderer_accepts_schema_sample_json() -> None:
    renderer = _load_renderer()
    sample = json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))

    markdown = renderer.render_pr_review_memory_handoff(sample)

    assert "Repository: ProfRandom92/Comptext" in markdown
    assert "Validation:" in markdown
    assert "Next action:" in markdown


@pytest.mark.parametrize("field", sorted(REQUIRED_V0_FIELDS))
def test_renderer_rejects_missing_required_v0_fields(field: str) -> None:
    renderer = _load_renderer()
    sample = json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))
    sample.pop(field)

    with pytest.raises(ValueError, match=field):
        renderer.render_pr_review_memory_handoff(sample)


def test_schema_docs_do_not_claim_runtime_behavior() -> None:
    text = "\n".join(
        [
            SCHEMA.read_text(encoding="utf-8"),
            SCHEMA_README.read_text(encoding="utf-8"),
        ]
    ).lower()

    forbidden_claims = (
        "provider calls",
        "mcp runtime implemented",
        "github write behavior",
        "enables auto-merge",
        "production-ready",
    )

    for claim in forbidden_claims:
        assert claim not in text
