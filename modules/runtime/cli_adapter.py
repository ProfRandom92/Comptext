"""Python adapter to the Rust runtime CLI for executing and validating agent contracts."""

from __future__ import annotations

import os
import shutil
import subprocess
import json
from pathlib import Path
from typing import Any

def find_ctxt_bin() -> str:
    """Locate the ctxt binary, prioritizing workspace target directories or COMPTEXT_CLI_BIN."""
    if "COMPTEXT_CLI_BIN" in os.environ:
        return os.environ["COMPTEXT_CLI_BIN"]
        
    path_bin = shutil.which("ctxt")
    if path_bin:
        return path_bin
        
    # Relative lookup inside the current _comptext-p1 structure
    # current file: worktrees/Comptext/modules/runtime/cli_adapter.py
    repo_root = Path(__file__).resolve().parent.parent.parent
    base_dir = repo_root.parent.parent
    worktree_cli = base_dir / "worktrees" / "comptext-cli"
    
    candidates = [
        worktree_cli / "target" / "debug" / "ctxt.exe",
        worktree_cli / "target" / "debug" / "ctxt",
        worktree_cli / "target" / "release" / "ctxt.exe",
        worktree_cli / "target" / "release" / "ctxt",
    ]
    for cand in candidates:
        if cand.exists() and cand.is_file():
            return str(cand)
            
    return "ctxt"

def find_config_path() -> str | None:
    """Locate the comptext.example.toml config file."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    base_dir = repo_root.parent.parent
    worktree_cli = base_dir / "worktrees" / "comptext-cli"
    config = worktree_cli / "comptext.example.toml"
    if config.exists():
        return str(config)
    return None

def run_ctxt_cmd(args: list[str]) -> dict[str, Any]:
    """Execute the ctxt CLI with --json and return parsed output or an ErrorEnvelope."""
    bin_path = find_ctxt_bin()
    config_path = find_config_path()
    if config_path:
        cmd = [bin_path, "--config", config_path, "--json"] + args
    else:
        cmd = [bin_path, "--json"] + args
    
    env = os.environ.copy()
    
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False,
            timeout=30,
            cwd=os.getcwd(),
            env=env
        )
    except subprocess.TimeoutExpired as e:
        return {
            "contract_name": "error-envelope",
            "schema_version": "v1",
            "error_code": "TIMEOUT",
            "message": f"Command timed out: {e}",
            "details": None
        }
    except Exception as e:
        return {
            "contract_name": "error-envelope",
            "schema_version": "v1",
            "error_code": "EXECUTION_FAILED",
            "message": f"Failed to execute ctxt binary: {e}",
            "details": None
        }
        
    if res.returncode == 0:
        try:
            return json.loads(res.stdout)
        except Exception as e:
            return {
                "contract_name": "error-envelope",
                "schema_version": "v1",
                "error_code": "MALFORMED_OUTPUT",
                "message": f"Stdout could not be parsed as JSON: {e}",
                "details": {"stdout": res.stdout}
            }
    else:
        # Check if stderr contains ErrorEnvelope JSON
        try:
            return json.loads(res.stderr)
        except Exception:
            return {
                "contract_name": "error-envelope",
                "schema_version": "v1",
                "error_code": "NON_ZERO_EXIT",
                "message": f"Command exited with status {res.returncode}",
                "details": {"stderr": res.stderr, "stdout": res.stdout}
            }

def validate_spec(spec_path: str) -> dict[str, Any]:
    """Validate an AgentSpec file using the Rust CLI."""
    return run_ctxt_cmd(["agent", "validate-spec", spec_path])

def dry_run(spec_path: str, out_evidence: str, out_replay: str) -> dict[str, Any]:
    """Execute an AgentSpec in dry-run mode using the Rust CLI."""
    return run_ctxt_cmd([
        "agent", "dry-run",
        "--spec", spec_path,
        "--out-evidence", out_evidence,
        "--out-replay", out_replay
    ])

def replay(replay_path: str, evidence_path: str) -> dict[str, Any]:
    """Verify logged evidence against a replay manifest using the Rust CLI."""
    return run_ctxt_cmd([
        "agent", "replay",
        "--replay", replay_path,
        "--evidence", evidence_path
    ])
