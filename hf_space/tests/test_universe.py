from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from universe import capabilities_frame, layers_frame, load_universe, skills_frame


def test_universe_snapshot_has_required_identity_and_layers():
    data = load_universe()
    assert data["product"]["name"] == "CompText"
    assert data["product"]["status"] == "local-dry-run-mvp"
    assert len(data["layers"]) == 7
    assert data["source"]["runtime_github_access"] is False


def test_universe_frames_have_stable_columns():
    data = load_universe()
    assert list(layers_frame(data).columns) == ["name", "status", "purpose", "inputs", "outputs"]
    assert list(capabilities_frame(data).columns) == ["name", "surface", "status", "network", "provider", "mutating"]
    assert list(skills_frame(data).columns) == ["name", "purpose", "validation", "boundary"]


def test_capability_statuses_use_explicit_maturity_vocabulary():
    data = load_universe()
    allowed = {"implemented", "scaffolded", "experimental", "planned", "future", "disabled"}
    assert {item["status"] for item in data["capabilities"]} <= allowed
