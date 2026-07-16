from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).parent
SNAPSHOT_PATH = ROOT / "data" / "universe_snapshot.json"


@lru_cache(maxsize=1)
def load_universe() -> dict[str, Any]:
    data = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    required = {"snapshot_version", "product", "source", "layers", "capabilities", "skills", "contracts"}
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError(f"Universe snapshot is missing required keys: {', '.join(missing)}")
    if data["product"].get("status") != "local-dry-run-mvp":
        raise ValueError("Universe snapshot must identify the product as local-dry-run-mvp.")
    return data


def layers_frame(data: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(data["layers"], columns=["name", "status", "purpose", "inputs", "outputs"])


def capabilities_frame(data: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        data["capabilities"],
        columns=["name", "surface", "status", "network", "provider", "mutating"],
    )


def skills_frame(data: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(data["skills"], columns=["name", "purpose", "validation", "boundary"])


def contracts_frame(data: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(data["contracts"], columns=["name", "kind", "fields", "execution"])


def overview_markdown(data: dict[str, Any]) -> str:
    product = data["product"]
    boundaries = "\n".join(f"- {item}" for item in data["boundaries"])
    return (
        f"# 🧭 {product['name']} Universe\n\n"
        f"> {product['claim']}\n\n"
        f"**Status:** `{product['status']}` · **Snapshot:** `{data['snapshot_version']}`\n\n"
        f"{product['description']}\n\n"
        "## Hard boundaries\n"
        f"{boundaries}"
    )
