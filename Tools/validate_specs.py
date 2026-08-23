#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml
try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:  # Keep repository validation usable in minimal Python environments.
    Draft202012Validator = None


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


def validate_schema_subset(instance, schema: dict, path: list[str] | None = None) -> list[tuple[list[str], str]]:
    path = path or []
    errors: list[tuple[list[str], str]] = []
    schema_type = schema.get("type")
    type_names = schema_type if isinstance(schema_type, list) else [schema_type] if schema_type else []
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
        "null": type(None),
    }
    if type_names:
        valid_type = any(
            isinstance(instance, type_map[name]) and not (name in {"integer", "number"} and isinstance(instance, bool))
            for name in type_names
        )
        if not valid_type:
            return [(path, f"expected type {schema_type!r}")]
    if "const" in schema and instance != schema["const"]:
        errors.append((path, f"expected constant {schema['const']!r}"))
    if "enum" in schema and instance not in schema["enum"]:
        errors.append((path, f"expected one of {schema['enum']!r}"))
    if isinstance(instance, str):
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            errors.append((path, f"does not match {schema['pattern']!r}"))
        if len(instance) < schema.get("minLength", 0):
            errors.append((path, f"is shorter than {schema['minLength']}"))
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append((path + [key], "required property is missing"))
        for key, child_schema in schema.get("properties", {}).items():
            if key in instance:
                errors.extend(validate_schema_subset(instance[key], child_schema, path + [key]))
    if isinstance(instance, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(instance):
            errors.extend(validate_schema_subset(item, schema["items"], path + [str(index)]))
    return errors


def validate_schema(instance, schema_path: Path, label: str, reporter: Reporter) -> None:
    schema = load_json(schema_path)
    if Draft202012Validator is None:
        errors = validate_schema_subset(instance, schema)
        for path, message in errors:
            location = ".".join(path) or "<root>"
            reporter.error(f"{label}: {location}: {message}")
    else:
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
        for error in errors:
            location = ".".join(map(str, error.path)) or "<root>"
            reporter.error(f"{label}: {location}: {error.message}")
    if not errors:
        suffix = " (built-in subset)" if Draft202012Validator is None else ""
        reporter.success(f"{label} schema validation{suffix}")


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


def validate_component_first_contract(asset_id: str, contract: dict, reporter: Reporter) -> None:
    workflow = contract.get("production_workflow", {})
    modules = contract.get("modules", {})
    hull = modules.get("hull", {})
    deck = modules.get("deck", {})
    gunport = modules.get("gunport", {})
    ai_3d = contract.get("ai_3d", {})

    checks = {
        "component-first workflow": workflow.get("version") == "component_first_v1",
        "full-effect concept is current stage": workflow.get("current_stage") == "full_effect_concept",
        "Hull forbids built-in gunports": hull.get("built_in_gunports_allowed") is False,
        "Deck is a separate scalable board": deck.get("simple_scalable_board") is True,
        "Gunport is separate from Hull": gunport.get("built_into_hull") is False,
        "Gunport owns a Boolean cutter": gunport.get("boolean_cutter_required") is True,
        "Gunport owns a cannon anchor": gunport.get("cannon_anchor_required") is True,
        "Tripo target is Hull only": ai_3d.get("generation_target") == "hull_only",
        "whole-ship final multiview is not required": ai_3d.get("whole_ship_final_multiview_required") is False,
    }
    for label, passed in checks.items():
        if passed:
            reporter.success(f"{asset_id} {label}")
        else:
            reporter.error(f"{asset_id} {label} check failed")


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
    validate_schema(manifest, ROOT / "Docs/schemas/spec-manifest.schema.json", "spec-manifest.yaml", reporter)

    policy_paths = [
        manifest["authority"]["policy"],
        manifest["governance"]["naming_and_versioning"],
        manifest["governance"]["change_control"],
        manifest["governance"]["tool_context_protocol"],
    ]
    for rel_path in policy_paths:
        check_path(rel_path, reporter, "Governance file")

    for system in manifest.get("systems", []):
        check_path(system["canonical_spec"], reporter, f"System {system['system_id']} spec")
        check_path(system["machine_contract"], reporter, f"System {system['system_id']} contract")

    for asset in manifest.get("assets", []):
        asset_id = asset["asset_id"]
        check_path(asset["design_spec"], reporter, f"{asset_id} design")
        contract_path = check_path(asset["integration_contract"], reporter, f"{asset_id} integration")

        if contract_path.exists():
            contract = load_yaml(contract_path)
            validate_schema(contract, ROOT / "Docs/schemas/ship-asset.schema.json", f"{asset_id} integration.yaml", reporter)
            validate_component_first_contract(asset_id, contract, reporter)

        concept = asset.get("full_effect_concept", {})
        concept_path_value = concept.get("path")
        if concept_path_value:
            concept_path = check_path(concept_path_value, reporter, f"{asset_id} full-effect concept")
            expected_hash = concept.get("sha256")
            if concept_path.exists() and expected_hash:
                actual_hash = sha256(concept_path)
                if actual_hash == expected_hash:
                    reporter.success(f"{asset_id} full-effect concept SHA-256")
                else:
                    reporter.error(
                        f"{asset_id} full-effect concept hash mismatch: expected {expected_hash}, got {actual_hash}"
                    )
        elif concept.get("status") == "PENDING":
            reporter.success(f"{asset_id} full-effect concept correctly pending")
        else:
            reporter.error(f"{asset_id} full-effect concept has no path and is not PENDING")

    reporter.print()
    error_count = len(reporter.errors) + (len(reporter.warnings) if args.strict else 0)
    print(
        f"\nSummary: {len(reporter.ok)} OK, "
        f"{len(reporter.warnings)} warning(s), {len(reporter.errors)} error(s)"
    )
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
