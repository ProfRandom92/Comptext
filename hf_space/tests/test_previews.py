from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from previews import build_air_preview, build_evidence_preview, scan_secrets


def test_air_preview_is_non_executable_and_extracts_contract_data():
    text = "Analysiere modules/cli/cli_entrypoint.py mit --dry-run. Keine Provider-Aufrufe. Gib JSON zurück."
    air = build_air_preview(text)
    assert air["preview"] is True
    assert air["executable"] is False
    assert air["execution"]["enabled"] is False
    assert "modules/cli/cli_entrypoint.py" in air["files"]
    assert "--dry-run" in air["flags"]
    assert "dry_run_only" in air["constraints"]
    assert "no_provider_calls" in air["constraints"]
    assert "json_report" in air["expected_outputs"]


def test_evidence_preview_is_simulated_not_persisted_and_hashes_are_stable():
    first = build_evidence_preview("alpha", "beta", "accepted", {"reduction": 20})
    second = build_evidence_preview("alpha", "beta", "accepted", {"reduction": 20})
    assert first == second
    assert first["simulation"] is True
    assert first["persisted"] is False
    assert first["input_hash"].startswith("sha256:")
    assert first["redaction"]["raw_input_persisted"] is False


def test_secret_scanner_blocks_known_token_shapes():
    assert scan_secrets("HF_TOKEN=hf_abcdefghijklmnopqrstuvwxyz") == ["huggingface-token", "secret-assignment"]
    air = build_air_preview("Use HF_TOKEN=hf_abcdefghijklmnopqrstuvwxyz")
    assert air["context"]["secret_scan"]["blocked"] is True
