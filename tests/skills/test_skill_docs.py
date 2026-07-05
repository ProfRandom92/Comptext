from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_FILES = [
    PROJECT_ROOT / "skills" / "comptext-bootstrap" / "SKILL.md",
    PROJECT_ROOT / "skills" / "comptext-dry-run-cli" / "SKILL.md",
    PROJECT_ROOT / "skills" / "comptext-schema-validation" / "SKILL.md",
    PROJECT_ROOT / "skills" / "comptext-provider-registry" / "SKILL.md",
    PROJECT_ROOT / "skills" / "comptext-evidence" / "SKILL.md",
    PROJECT_ROOT / "skills" / "comptext-runtime" / "SKILL.md",
    PROJECT_ROOT / "skills" / "comptext-windows" / "SKILL.md",
    PROJECT_ROOT / "skills" / "comptext-security" / "SKILL.md",
]
REQUIRED_HEADINGS = [
    "## Name",
    "## Purpose",
    "## When to use",
    "## Inputs",
    "## Outputs",
    "## Workflow",
    "## Safety rules",
    "## Validation checklist",
    "## Anti-patterns",
]
SECRET_PATTERNS = ["api_key", "apikey", "secret=", "token="]


def test_skill_docs_exist_and_have_required_headings():
    for skill_file in SKILL_FILES:
        text = skill_file.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            assert heading in text, f"{skill_file} missing {heading}"


def test_skill_docs_do_not_contain_secret_patterns():
    for skill_file in SKILL_FILES:
        text = skill_file.read_text(encoding="utf-8").lower()
        for pattern in SECRET_PATTERNS:
            assert pattern not in text, f"{skill_file} contains forbidden pattern {pattern}"
