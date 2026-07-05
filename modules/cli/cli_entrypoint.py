"""Command line entrypoint for the local CompText dry-run MVP scaffold."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from modules.doctor.doctor import run_doctor
from modules.provider_registry.provider_registry import list_providers
from modules.validation.schema_validator import validate_local_schemas


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="comptext")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor")
    doctor.add_argument("--dry-run", action="store_true", required=True)

    validate = subparsers.add_parser("validate")
    validate_subparsers = validate.add_subparsers(dest="target", required=True)
    schemas = validate_subparsers.add_parser("schemas")
    schemas.add_argument("--dry-run", action="store_true", required=True)

    providers = subparsers.add_parser("providers")
    providers_subparsers = providers.add_subparsers(dest="provider_command", required=True)
    provider_list = providers_subparsers.add_parser("list")
    provider_list.add_argument("--dry-run", action="store_true", required=True)
    return parser


def run(argv: list[str] | None = None, *, repo_root: Path | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root or Path.cwd()

    if args.command == "doctor":
        print(json.dumps(run_doctor(repo_root=root, dry_run=args.dry_run), indent=2, sort_keys=True))
        return 0
    if args.command == "validate" and args.target == "schemas":
        print(json.dumps({"mode": "dry-run", "results": validate_local_schemas(repo_root=root, dry_run=args.dry_run)}, indent=2, sort_keys=True))
        return 0
    if args.command == "providers" and args.provider_command == "list":
        print(json.dumps({"mode": "dry-run", "providers": list_providers(path=root / "examples/provider/provider-registry-sample.json", dry_run=args.dry_run)}, indent=2, sort_keys=True))
        return 0
    return 2


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
