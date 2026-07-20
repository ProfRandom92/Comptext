import pytest

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
    
    # New edge cases
    assert _clean_text('TOKEN="abc\\"def"') == 'TOKEN="<redacted>"'
    assert _clean_text('"TOKEN": "value"') == '"TOKEN": "<redacted>"'
    assert _clean_text("'API_KEY': 'value'") == "'API_KEY': '<redacted>'"
    assert _clean_text('{"api_key": "value"}') == '{"api_key": "<redacted>"}'
    assert _clean_text('{"normal": "value"}') == '{"normal": "value"}'
    assert _clean_text("TOKEN=val1 API_KEY=val2") == "TOKEN=<redacted> API_KEY=<redacted>"
    assert _clean_text('TOKEN="<redacted>"') == 'TOKEN="<redacted>"'

    # Explicit cases required by Thread C
    assert _clean_text('TOKEN="value\\"with\\"escapes"') == 'TOKEN="<redacted>"'
    assert _clean_text("TOKEN='value\\'with\\'escapes'") == "TOKEN='<redacted>'"
    assert _clean_text("HF_TOKEN=") == "HF_TOKEN="
    assert _clean_text("HF_TOKEN=\n'value'") == "HF_TOKEN= '<redacted>'"  # _clean_text collapses newlines to space first
    assert _clean_text("NORMAL_VAR=value") == "NORMAL_VAR=value"

    # Line boundary checks (no processing across lines on raw multiline text)
    from previews import redact_secrets
    assert redact_secrets("HF_TOKEN=\n'value'") == ("HF_TOKEN=\n'value'", False)
