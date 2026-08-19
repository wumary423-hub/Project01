#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.ok: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def success(self, message: str) -> None:
        self.ok.append(message)

    def print(self) -> None:
        for item in self.ok:
            print(f"[OK] {item}")
        for item in self.warnings:
            print(f"[WARN] {item}")
        for item in self.errors:
            print(f"[ERROR] {item}")


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(instance, schema_path: Path, label: str, reporter: Reporter) -> None:
    schema = load_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            location = ".".join(map(str, error.path)) or "<root>"
            reporter.error(f"{label}: {location}: {error.message}")
    else:
        reporter.success(f"{label} schema validation")


def check_path(rel_path: str, reporter: Reporter, label: str) -> Path:
    path = ROOT / rel_path
    if path.exists():
        reporter.success(f"{label}: {rel_path}")
    else:
        reporter.error(f"{label} missing: {rel_path}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical game specifications.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors.")
    args = parser.parse_args()

    reporter = Reporter()

    manifest_path = ROOT / "spec-manifest.yaml"
    if not manifest_path.exists():
        print("[ERROR] spec-manifest.yaml is missing")
        return 1

    manifest = load_yaml(manifest_path)
    validate_schema(
        manifest,
        ROOT / "docs/schemas/spec-manifest.schema.json",
        "spec-manifest.yaml",
        reporter,
    )

    policy_paths = [
        manifest["authority"]["policy"],
        manifest["governance"]["naming_and_versioning"],
        manifest["governance"]["change_control"],
        manifest["governance"]["tool_context_protocol"],
    ]
    for rel in policy_paths:
        check_path(rel, reporter, "Governance file")

    for system in manifest.get("systems", []):
        check_path(system["canonical_spec"], reporter, f"System {system['system_id']} spec")
        check_path(system["machine_contract"], reporter, f"System {system['system_id']} contract")
        migration = system.get("migration", {})
        legacy = migration.get("legacy_path")
        if legacy and not (ROOT / legacy).exists():
            reporter.warning(
                f"Legacy source not found in this package: {legacy}. "
                "This is expected until the package is merged into the real repository."
            )

    for asset in manifest.get("assets", []):
        asset_id = asset["asset_id"]
        design_path = check_path(asset["design_spec"], reporter, f"{asset_id} design")
        contract_path = check_path(asset["integration_contract"], reporter, f"{asset_id} integration")

        if contract_path.exists():
            contract = load_yaml(contract_path)
            validate_schema(
                contract,
                ROOT / "docs/schemas/ship-asset.schema.json",
                f"{asset_id} integration.yaml",
                reporter,
            )

        visual = asset.get("visual_master", {})
        visual_path = check_path(visual["path"], reporter, f"{asset_id} visual master")
        expected_hash = visual.get("sha256")
        if visual_path.exists() and expected_hash:
            actual_hash = sha256(visual_path)
            if actual_hash == expected_hash:
                reporter.success(f"{asset_id} visual master SHA-256")
            else:
                reporter.error(
                    f"{asset_id} visual master hash mismatch: expected {expected_hash}, got {actual_hash}"
                )

    reporter.print()

    error_count = len(reporter.errors)
    if args.strict:
        error_count += len(reporter.warnings)

    print(
        f"\nSummary: {len(reporter.ok)} OK, "
        f"{len(reporter.warnings)} warning(s), {len(reporter.errors)} error(s)"
    )
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
