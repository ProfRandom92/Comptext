"""Local dry-run CLI entrypoint for CompText."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from modules.doctor.doctor import run_doctor
from modules.evidence.evidence_verifier import verify_sample_evidence
from modules.provider_registry.provider_registry import format_provider_list, load_provider_registry
from modules.validation.schema_validator import validate_local_schemas


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="comptext")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Run local dry-run environment checks.")
    doctor.add_argument("--dry-run", action="store_true", required=True)

    validate = subparsers.add_parser("validate", help="Validate local CompText artifacts.")
    validate_subparsers = validate.add_subparsers(dest="target", required=True)
    validate_schemas = validate_subparsers.add_parser("schemas", help="Validate local JSON schemas and examples.")
    validate_schemas.add_argument("--dry-run", action="store_true", required=True)

    providers = subparsers.add_parser("providers", help="Inspect local provider registry samples.")
    providers_subparsers = providers.add_subparsers(dest="action", required=True)
    providers_list = providers_subparsers.add_parser("list", help="List local provider sample states.")
    providers_list.add_argument("--dry-run", action="store_true", required=True)

    evidence = subparsers.add_parser("evidence", help="Verify local synthetic evidence samples.")
    evidence_subparsers = evidence.add_subparsers(dest="action", required=True)
    evidence_verify = evidence_subparsers.add_parser("verify", help="Verify a synthetic evidence hash chain.")
    evidence_verify.add_argument("--sample", action="store_true", required=True)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        report = run_doctor(PROJECT_ROOT)
        print("CompText doctor dry-run")
        for check in report["checks"]:
            print(f"- {check['name']}: {check['status']} ({check['detail']})")
        return 0 if report["ok"] else 1

    if args.command == "validate" and args.target == "schemas":
        result = validate_local_schemas(PROJECT_ROOT)
        print("CompText schema validation dry-run")
        for item in result["items"]:
            print(f"- {item['path']}: {item['status']}")
        return 0 if result["ok"] else 1

    if args.command == "providers" and args.action == "list":
        registry = load_provider_registry(PROJECT_ROOT / "examples" / "provider" / "provider-registry-sample.json")
        print(format_provider_list(registry))
        return 0

    if args.command == "evidence" and args.action == "verify":
        result = verify_sample_evidence()
        print("CompText evidence verification sample")
        for item in result["checked"]:
            print(f"- {item['kind']}: ok ({item['hash']})")
        print(f"final_hash: {result['final_hash']}")
        return 0 if result["ok"] else 1

    parser.error("Unsupported command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
