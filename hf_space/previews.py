from __future__ import annotations

import hashlib
import re
from typing import Any

from safety_checks import extract_cli_flags, extract_file_paths

_SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "huggingface-token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "openai-key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer-token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.I),
}


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def redact_secrets(text: str) -> tuple[str, bool]:
    """Redact sensitive variable assignments line-by-line.

    Returns the redacted text and a boolean indicating if any secret assignment was redacted.
    """
    if not text:
        return "", False

    sensitive_keywords = {"token", "secret", "password", "api_key", "access_key", "private_key", "credential"}
    # Matches: var_name = value  or  var_name: value
    assignment_pattern = re.compile(
        r"\b([A-Za-z_][A-Za-z0-9_]*)(\s*[:=]\s*)(\"[^\"]*\"|'[^']*'|[^\s,;]+)"
    )

    lines = text.splitlines(keepends=True)
    redacted_lines = []
    any_redacted = False

    for line in lines:
        new_line = line
        matches = list(assignment_pattern.finditer(line))
        for match in reversed(matches):
            var_name = match.group(1)
            if any(kw in var_name.lower() for kw in sensitive_keywords):
                start, end = match.span(3)
                val = match.group(3)
                if val == "<redacted>" or val == '"<redacted>"' or val == "'<redacted>'":
                    continue
                if val.startswith('"') and val.endswith('"'):
                    replacement = '"<redacted>"'
                elif val.startswith("'") and val.endswith("'"):
                    replacement = "'<redacted>'"
                else:
                    replacement = "<redacted>"
                new_line = new_line[:start] + replacement + new_line[end:]
                any_redacted = True
        redacted_lines.append(new_line)

    return "".join(redacted_lines), any_redacted


def scan_secrets(text: str) -> list[str]:
    matches = [name for name, pattern in _SECRET_PATTERNS.items() if pattern.search(text or "")]

    _, has_assignment = redact_secrets(text or "")
    if has_assignment:
        matches.append("secret-assignment")

    return sorted(matches)


def _constraints(text: str) -> list[str]:
    lower = text.lower()
    constraints: list[str] = []
    if any(term in lower for term in ("no provider", "keine provider", "keine live-provider", "without provider")):
        constraints.append("no_provider_calls")
    if "--dry-run" in text:
        constraints.append("dry_run_only")
    if any(term in lower for term in ("do not write", "nicht ändern", "nicht veraendern", "read only", "nur lesen")):
        constraints.append("no_writes")
    if any(term in lower for term in ("do not commit", "nicht commit", "no commit")):
        constraints.append("no_commits")
    return sorted(set(constraints))


def _expected_outputs(text: str) -> list[str]:
    lower = text.lower()
    outputs: list[str] = []
    if "json" in lower:
        outputs.append("json_report")
    if "markdown" in lower:
        outputs.append("markdown_report")
    if "summary" in lower or "zusammenfassung" in lower:
        outputs.append("summary")
    return outputs or ["analysis_preview"]


def build_air_preview(text: str, compression: dict[str, Any] | None = None) -> dict[str, Any]:
    clean = (text or "").strip()
    secret_matches = scan_secrets(clean)
    files = sorted(extract_file_paths(clean))
    flags = sorted(extract_cli_flags(clean))
    constraints = _constraints(clean)
    return {
        "version": "preview-1",
        "preview": True,
        "executable": False,
        "intent": "analyze_engineering_context",
        "goal": clean[:240] if clean else "No goal supplied",
        "context": {
            "source": "user_input",
            "input_hash": _sha256(clean),
            "compression": compression or {"decision": "not_run"},
            "secret_scan": {"blocked": bool(secret_matches), "matches": secret_matches},
        },
        "files": files,
        "tools": [],
        "flags": flags,
        "constraints": constraints,
        "permissions": {
            "network": False,
            "provider": False,
            "repository_write": False,
            "execute": False,
        },
        "expected_outputs": _expected_outputs(clean),
        "execution": {"enabled": False, "reason": "Hugging Face Space previews contracts only."},
    }


def build_evidence_preview(
    original: str,
    output: str,
    decision: str,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    secret_matches = scan_secrets(original)
    return {
        "schema": "simulated-evidence-preview-1",
        "simulation": True,
        "persisted": False,
        "event_type": "context_preview_completed",
        "actor": "hf-space-demo",
        "summary": f"Context preview decision: {decision}",
        "input_hash": _sha256(original),
        "output_hash": _sha256(output),
        "decision": decision,
        "metrics": metrics or {},
        "redaction": {
            "secrets_detected": bool(secret_matches),
            "matches": secret_matches,
            "raw_input_persisted": False,
        },
    }
