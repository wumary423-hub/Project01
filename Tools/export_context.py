#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fenced_yaml(data) -> str:
    return "```yaml\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip() + "\n```"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export tool-specific context from canonical specs.")
    parser.add_argument("asset_id", help="Example: ShipType_SmallSailer01")
    parser.add_argument(
        "--target",
        required=True,
        choices=["chatgpt", "cursor", "meshy", "blender", "ue5"],
    )
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    manifest = load_yaml(ROOT / "spec-manifest.yaml")
    asset = next((item for item in manifest["assets"] if item["asset_id"] == args.asset_id), None)
    if asset is None:
        raise SystemExit(f"Unknown asset_id: {args.asset_id}")

    system = manifest["systems"][0]
    governance = read(ROOT / manifest["authority"]["policy"])
    system_spec = read(ROOT / system["canonical_spec"])
    design = read(ROOT / asset["design_spec"])
    integration = load_yaml(ROOT / asset["integration_contract"])

    if args.target == "ue5":
        output_text = json.dumps(integration, ensure_ascii=False, indent=2) + "\n"
        default_suffix = "json"
    else:
        parts = [
            f"# Context Bundle — {args.asset_id} — {args.target}",
            "",
            "Generated from canonical repository specifications. This export is not itself authoritative.",
            "",
        ]

        if args.target in {"chatgpt", "cursor"}:
            parts += ["## Source-of-Truth Policy", governance, ""]
        if args.target in {"chatgpt", "cursor", "blender"}:
            parts += ["## Ship System", system_spec, ""]
        if args.target in {"chatgpt", "meshy", "blender"}:
            parts += ["## Asset Design", design, ""]
        parts += ["## Integration Contract", fenced_yaml(integration), ""]
        output_text = "\n".join(parts)
        default_suffix = "md"

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
    else:
        output_path = ROOT / f"exports/context/{args.asset_id}_{args.target}_context.{default_suffix}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_text, encoding="utf-8")
    print(output_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
