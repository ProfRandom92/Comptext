import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "hf_space"))
sys.path.insert(0, str(ROOT / "plugins" / "pr-review-memory"))
