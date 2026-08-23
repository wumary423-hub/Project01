#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
GITHUB_RAW_DOCS_SYNC = "https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync"


def repo_file(rel: str) -> Path:
    rel = rel.replace("\\", "/")
    candidates = [ROOT / rel]
    if rel.startswith("Docs/"):
        candidates.append(ROOT / ("docs/" + rel[5:]))
    elif rel.startswith("docs/"):
        candidates.append(ROOT / ("Docs/" + rel[5:]))
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def raw_url(rel: str) -> str:
    rel = rel.replace("\\", "/")
    if rel.startswith("docs/"):
        rel = "Docs/" + rel[5:]
    return f"{GITHUB_RAW_DOCS_SYNC}/{rel}"


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
        choices=["chatgpt", "google-ai-studio", "cursor", "tripo3d", "meshy", "blender", "ue5"],
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
    production_rules = read(ROOT / system["asset_production_rules"])
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

        if args.target == "google-ai-studio":
            visual = asset.get("full_effect_concept") or {}
            visual_path = visual.get("path") or ""
            material_id = asset.get("material_card")
            card = next(
                (item for item in (manifest.get("material_cards") or []) if item.get("material_card_id") == material_id),
                None,
            )
            parts += [
                "## GitHub refresh (preferred over this snapshot)",
                "",
                f"Branch: `docs-sync`. Raw root: `{GITHUB_RAW_DOCS_SYNC}/`",
                "",
                f"- {raw_url('spec-manifest.yaml')}",
                f"- {raw_url('Docs/governance/source-of-truth.md')}",
                f"- {raw_url('Docs/tool-guides/google-ai-studio.md')}",
                f"- {raw_url(system['canonical_spec'])}",
                f"- {raw_url(system['asset_production_rules'])}",
                f"- {raw_url(asset['design_spec'])}",
                f"- {raw_url(asset['integration_contract'])}",
            ]
            if visual_path:
                parts.append(f"- {raw_url(visual_path)}")
            if card:
                for key in ("spec", "machine_card", "reference"):
                    if card.get(key):
                        parts.append(f"- {raw_url(card[key])}")
            parts += ["", "If URL context can fetch these, prefer them over the bundled copy below.", ""]

        if args.target in {"chatgpt", "google-ai-studio", "cursor"}:
            parts += ["## Source-of-Truth Policy", governance, ""]
        if args.target in {"chatgpt", "google-ai-studio", "cursor", "blender"}:
            parts += ["## Ship System", system_spec, ""]
            parts += ["## Ship Asset Production Rules", production_rules, ""]
        if args.target in {"chatgpt", "google-ai-studio", "tripo3d", "meshy", "blender"}:
            parts += ["## Asset Design", design, ""]
        material_id = asset.get("material_card")
        if material_id and args.target in {"chatgpt", "google-ai-studio"}:
            card = next(
                (item for item in (manifest.get("material_cards") or []) if item.get("material_card_id") == material_id),
                None,
            )
            if card and card.get("spec"):
                card_path = repo_file(card["spec"])
                if card_path.exists():
                    parts += ["## Material Card", read(card_path), ""]
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
    try:
        print(output_path.relative_to(ROOT))
    except ValueError:
        print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
