import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_FILES = [
    PROJECT_ROOT / "plugins" / "comptext-core" / "plugin.json",
    PROJECT_ROOT / "plugins" / "comptext-windows" / "plugin.json",
    PROJECT_ROOT / "plugins" / "comptext-provider-gateway" / "plugin.json",
    PROJECT_ROOT / "plugins" / "comptext-evidence-replay" / "plugin.json",
    PROJECT_ROOT / "plugins" / "comptext-mcp-fabric" / "plugin.json",
]
FORBIDDEN_STATUS_VALUES = {"available", "production", "live", "provider_enabled"}
SECRET_PATTERNS = [
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"secret\s*=", re.IGNORECASE),
    re.compile(r"token\s*=", re.IGNORECASE),
]
LIVE_PROVIDER_PATTERNS = ["provider_enabled", "healthcheck_enabled", "live_provider", "start_gateway", "start_mcp"]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    assert isinstance(data, dict)
    return data


def test_plugin_manifests_are_valid_json_and_match_schema():
    schema = load_json(PROJECT_ROOT / "schemas" / "plugin.schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    for plugin_file in PLUGIN_FILES:
        manifest = load_json(plugin_file)
        validator.validate(manifest)


def test_plugin_status_is_experimental_only():
    for plugin_file in PLUGIN_FILES:
        manifest = load_json(plugin_file)
        assert manifest["status"] == "experimental"
        assert manifest["status"] not in FORBIDDEN_STATUS_VALUES


def test_plugin_skills_reference_existing_skill_files():
    for plugin_file in PLUGIN_FILES:
        manifest = load_json(plugin_file)
        for skill_path in manifest["skills"]:
            assert (PROJECT_ROOT / skill_path).is_file(), f"{plugin_file} references missing {skill_path}"


def test_plugin_files_do_not_activate_live_providers_or_contain_secrets():
    for plugin_file in PLUGIN_FILES:
        text = plugin_file.read_text(encoding="utf-8")
        lowered = text.lower()
        for pattern in LIVE_PROVIDER_PATTERNS:
            assert pattern not in lowered, f"{plugin_file} contains live activation pattern {pattern}"
        for pattern in SECRET_PATTERNS:
            assert not pattern.search(text), f"{plugin_file} contains secret-like pattern {pattern.pattern}"
