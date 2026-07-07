import pytest

from modules.runtime.sample_run import build_sample_run_events, run_sample
from modules.evidence.evidence import verify_evidence_chain


def test_run_sample_dry_run_returns_local_only_summary() -> None:
    result = run_sample(dry_run=True)

    assert result["command"] == "comptext run sample --dry-run"
    assert result["mode"] == "dry-run"
    assert result["ok"] is True
    assert result["run"]["status"] == "completed"
    assert len(result["plan"]["steps"]) == 3
    assert result["execution"]["provider_calls"] == 0
    assert result["execution"]["network"] == "not_called"
    assert result["execution"]["providers"] == "not_called"
    assert result["execution"]["secrets"] == "not_read"
    assert result["execution"]["file_writes"] == 0
    assert result["evidence"]["verified"] is True
    assert len(result["evidence"]["root_hash"]) == 64


def test_build_sample_run_events_are_verifiable() -> None:
    events = build_sample_run_events()
    result = verify_evidence_chain(events)

    assert result["ok"] is True
    assert result["events"] == 3


def test_run_sample_rejects_non_dry_run() -> None:
    with pytest.raises(ValueError, match="--dry-run only"):
        run_sample(dry_run=False)


def test_run_sample_is_perfectly_deterministic() -> None:
    result1 = run_sample(dry_run=True)
    result2 = run_sample(dry_run=True)
    assert result1 == result2


def test_run_sample_performs_no_io_or_env_reads(monkeypatch) -> None:
    import builtins
    from pathlib import Path
    import os
    import socket

    def raise_io_error(*args, **kwargs):
        raise IOError("File operations are forbidden in dry-run sample runtime")

    monkeypatch.setattr(builtins, "open", raise_io_error)
    monkeypatch.setattr(Path, "write_text", raise_io_error)
    monkeypatch.setattr(Path, "write_bytes", raise_io_error)

    def raise_env_error(*args, **kwargs):
        raise KeyError("Environment variable access is forbidden in dry-run sample runtime")

    monkeypatch.setattr(os, "getenv", raise_env_error)
    monkeypatch.setattr(os.environ, "__getitem__", raise_env_error)
    monkeypatch.setattr(os.environ, "get", raise_env_error)

    def raise_socket_error(*args, **kwargs):
        raise RuntimeError("Network calls are forbidden in dry-run sample runtime")

    monkeypatch.setattr(socket, "socket", raise_socket_error)

    result = run_sample(dry_run=True)
    assert result["ok"] is True
