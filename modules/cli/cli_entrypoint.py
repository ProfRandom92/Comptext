"""Command line entrypoint for the local CompText dry-run MVP scaffold."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from modules.doctor.doctor import run_doctor
from modules.evidence.evidence import verify_sample_evidence
from modules.gateway.gateway import (
    dry_run_gateway_response,
    get_gateway_health,
    list_gateway_models,
)
from modules.provider_registry.provider_registry import list_providers
from modules.runtime.sample_run import run_sample
from modules.validation.schema_validator import validate_local_schemas
from modules.validation.workspace_validation import validate_workspace_schemas

EXPECTED_COMMAND_ERRORS = (OSError, json.JSONDecodeError, ValueError, KeyError)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="comptext")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor")
    doctor.add_argument("--dry-run", action="store_true", required=True)

    validate = subparsers.add_parser("validate")
    validate_subparsers = validate.add_subparsers(dest="target", required=True)
    schemas = validate_subparsers.add_parser("schemas")
    schemas.add_argument("--dry-run", action="store_true", required=True)
    workspace = validate_subparsers.add_parser("workspace")
    workspace.add_argument("--dry-run", action="store_true", required=True)

    providers = subparsers.add_parser("providers")
    providers_subparsers = providers.add_subparsers(dest="provider_command", required=True)
    provider_list = providers_subparsers.add_parser("list")
    provider_list.add_argument("--dry-run", action="store_true", required=True)

    gateway = subparsers.add_parser("gateway")
    gateway_subparsers = gateway.add_subparsers(dest="gateway_command", required=True)
    gateway_health = gateway_subparsers.add_parser("health")
    gateway_health.add_argument("--dry-run", action="store_true", required=True)
    gateway_models = gateway_subparsers.add_parser("models")
    gateway_models.add_argument("--dry-run", action="store_true", required=True)
    gateway_sample = gateway_subparsers.add_parser("sample")
    gateway_sample.add_argument("--dry-run", action="store_true", required=True)

    evidence = subparsers.add_parser("evidence")
    evidence_subparsers = evidence.add_subparsers(dest="evidence_command", required=True)
    evidence_verify = evidence_subparsers.add_parser("verify")
    evidence_verify.add_argument("--sample", action="store_true", required=True)

    run_parser = subparsers.add_parser("run")
    run_subparsers = run_parser.add_subparsers(dest="run_command", required=True)
    sample_run = run_subparsers.add_parser("sample")
    sample_run.add_argument("--dry-run", action="store_true", required=True)

    status = subparsers.add_parser("status")
    status.add_argument("--dry-run", action="store_true", required=True)
    return parser


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _print_error(error: Exception) -> None:
    _print_json({"error": {"message": str(error), "type": type(error).__name__}, "ok": False})


def run(argv: list[str] | None = None, *, repo_root: Path | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root or Path.cwd()

    try:
        if args.command == "doctor":
            result = run_doctor(repo_root=root, dry_run=args.dry_run)
            _print_json(result)
            return 0 if result.get("ok") is True else 1
        if args.command == "status":
            from modules.cli.status_screen import build_status_screen
            exit_code, output_text = build_status_screen(root)
            print(output_text)
            return exit_code
        if args.command == "validate" and args.target == "schemas":
            _print_json({"mode": "dry-run", "results": validate_local_schemas(repo_root=root, dry_run=args.dry_run)})
            return 0
        if args.command == "validate" and args.target == "workspace":
            results = validate_workspace_schemas(repo_root=root)
            _print_json({"mode": "dry-run", "results": results})
            if any(r.get("status") == "invalid" for r in results):
                return 1
            return 0
        if args.command == "providers" and args.provider_command == "list":
            _print_json({"mode": "dry-run", "providers": list_providers(path=root / "examples/provider/provider-registry-sample.json", dry_run=args.dry_run)})
            return 0
        if args.command == "gateway" and args.gateway_command == "health":
            result = get_gateway_health(dry_run=args.dry_run)
            _print_json(result)
            return 0 if result.get("ok") is True else 1
        if args.command == "gateway" and args.gateway_command == "models":
            _print_json({"mode": "dry-run", "models": list_gateway_models(dry_run=args.dry_run)})
            return 0
        if args.command == "gateway" and args.gateway_command == "sample":
            result = dry_run_gateway_response(
                {
                    "model": "comptext-dry-run-model",
                    "messages": [{"role": "user", "content": "CompText Gateway dry-run sample"}],
                    "metadata": {"sample": True},
                },
                dry_run=args.dry_run,
            )
            _print_json(result)
            return 0 if result.get("ok") is True else 1
        if args.command == "evidence" and args.evidence_command == "verify":
            result = verify_sample_evidence(sample=args.sample)
            _print_json(result)
            return 0 if result.get("ok") is True else 1
        if args.command == "run" and args.run_command == "sample":
            result = run_sample(dry_run=args.dry_run)
            _print_json(result)
            return 0 if result.get("ok") is True else 1
    except EXPECTED_COMMAND_ERRORS as error:
        _print_error(error)
        return 1
    return 2


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
