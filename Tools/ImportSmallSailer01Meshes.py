# -*- coding: utf-8 -*-
"""
Import SmallSailer01 FBX files from Content/Ship/SmallSailer01/Mesh into UE StaticMeshes.
Run in editor:
  py "E:/newlife/Project01/Tools/ImportSmallSailer01Meshes.py"

Expected disk layout (one FBX per asset — see ship-system.mdc V0.1.1):
  Content/Ship/SmallSailer01/Mesh/SM_SmallSailer01_Hull.fbx
  Content/Ship/SmallSailer01/Mesh/SM_SmallSailer01_MastRig01_Square_Full.fbx
  ...

Destination:
  /Game/Ship/SmallSailer01/Mesh/<asset_name>
"""

from __future__ import annotations

import unreal

try:
    from EditorPyRunBanner import run_main
except ImportError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from EditorPyRunBanner import run_main

WORKFLOW = "SmallSailer01"
DISK_SUBDIR = f"Ship/{WORKFLOW}/Mesh"
UE_DEST = f"/Game/Ship/{WORKFLOW}/Mesh"

# Phase-one required + modular parts. Headsail optional (retrofit).
FBX_NAMES = [
    f"SM_{WORKFLOW}_Hull",
    *[f"SM_{WORKFLOW}_MastRig01_{Rig}_{State}" for Rig in ("Square", "Lateen") for State in ("Full", "Half", "Furled")],
    f"SM_{WORKFLOW}_Flag_Placeholder",
    f"SM_{WORKFLOW}_Figurehead_Placeholder",
    f"SM_{WORKFLOW}_Rudder",
    f"SM_{WORKFLOW}_Anchor",
    f"SM_{WORKFLOW}_MastBroken",
]

OPTIONAL_FBX_NAMES = [
    *[f"SM_{WORKFLOW}_Headsail01_{State}" for State in ("Full", "Half", "Furled")],
    "SM_Weapon_LightCannon01",
]


def import_one_fbx(asset_name: str, required: bool) -> bool:
    project_content = unreal.Paths.project_content_dir()
    fbx_disk = unreal.Paths.combine([project_content, DISK_SUBDIR, f"{asset_name}.fbx"])
    fbx_disk = unreal.Paths.convert_relative_path_to_full(fbx_disk)

    if not unreal.Paths.file_exists(fbx_disk):
        if required:
            unreal.log_error(f"Missing required FBX: {fbx_disk}")
        else:
            unreal.log(f"Optional FBX not present (skip): {fbx_disk}")
        return False

    if not unreal.EditorAssetLibrary.does_directory_exist(UE_DEST):
        unreal.EditorAssetLibrary.make_directory(UE_DEST)

    task = unreal.AssetImportTask()
    task.set_editor_property("filename", fbx_disk)
    task.set_editor_property("destination_path", UE_DEST)
    task.set_editor_property("destination_name", asset_name)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)

    options = unreal.FbxImportUI()
    options.set_editor_property("import_mesh", True)
    options.set_editor_property("import_textures", True)
    options.set_editor_property("import_materials", True)
    options.set_editor_property("import_as_skeletal", False)
    static_options = options.get_editor_property("static_mesh_import_data")
    if static_options:
        static_options.set_editor_property("combine_meshes", True)
        static_options.set_editor_property("auto_generate_collision", True)
    task.set_editor_property("options", options)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    unreal.log(f"Imported {asset_name} -> {UE_DEST}/{asset_name}")
    return True


def main() -> None:
    ok = 0
    for name in FBX_NAMES:
        if import_one_fbx(name, required=True):
            ok += 1

    opt_ok = 0
    for name in OPTIONAL_FBX_NAMES:
        if import_one_fbx(name, required=False):
            opt_ok += 1

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    unreal.log(
        f"DONE ImportSmallSailer01Meshes required={ok}/{len(FBX_NAMES)} optional={opt_ok}"
    )
    unreal.log("Next: add sockets in Static Mesh Editor, then run ValidateShipMeshes.py")


if __name__ == "__main__":
    run_main(main, "ImportSmallSailer01Meshes.py")
