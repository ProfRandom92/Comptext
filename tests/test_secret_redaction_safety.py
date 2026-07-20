import pytest
import sys
from pathlib import Path

# Add plugins/pr-review-memory/ and hf_space/ to path
sys.path.insert(0, str(Path(__file__).parent.parent / "hf_space"))
sys.path.insert(0, str(Path(__file__).parent.parent / "plugins" / "pr-review-memory"))

from previews import scan_secrets
from renderer import _clean_text

def test_secret_scan_previews_matrix():
    assert "secret-assignment" in scan_secrets("TOKEN=value")
    assert "secret-assignment" in scan_secrets("HF_TOKEN=value")
    assert "secret-assignment" in scan_secrets("_HF_TOKEN=value")
    assert "secret-assignment" in scan_secrets("MY_TOKEN_1=value")
    assert "secret-assignment" in scan_secrets("api_key=value")
    assert "secret-assignment" in scan_secrets("SERVICE_API_KEY=value")
    assert "secret-assignment" in scan_secrets("TOKEN  =  value")
    assert "secret-assignment" in scan_secrets('TOKEN="value"')
    assert "secret-assignment" in scan_secrets("TOKEN='value'")
    assert "secret-assignment" in scan_secrets("export HF_TOKEN=value")
    
    assert "secret-assignment" not in scan_secrets("HF_TOKEN=\n'value'")
    assert "secret-assignment" not in scan_secrets("NORMAL_VAR=value")

def test_secret_redaction_renderer_matrix():
    assert _clean_text("TOKEN=value") == "TOKEN=<redacted>"
    assert _clean_text("HF_TOKEN=value") == "HF_TOKEN=<redacted>"
    assert _clean_text("_HF_TOKEN=value") == "_HF_TOKEN=<redacted>"
    assert _clean_text("MY_TOKEN_1=value") == "MY_TOKEN_1=<redacted>"
    assert _clean_text("api_key=value") == "api_key=<redacted>"
    assert _clean_text("SERVICE_API_KEY=value") == "SERVICE_API_KEY=<redacted>"
    assert _clean_text("TOKEN  =  value") == "TOKEN  =  <redacted>"
    assert _clean_text('TOKEN="value"') == 'TOKEN="<redacted>"'
    assert _clean_text("TOKEN='value'") == "TOKEN='<redacted>'"
    
    assert _clean_text("NORMAL_VAR=value") == "NORMAL_VAR=value"
