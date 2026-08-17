# -*- coding: utf-8 -*-
"""
Create /Game/Ship/DT_Ships (DataTable of FShipDefinition).
  py "E:/newlife/Project01/Tools/CreateShipsDataTable.py"
"""

import json
import unreal

try:
    from EditorPyRunBanner import run_main
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from EditorPyRunBanner import run_main

ASSET_DIR = "/Game/Ship"
ASSET_NAME = "DT_Ships"
ASSET_PATH = f"{ASSET_DIR}/{ASSET_NAME}"
ROW_STRUCT_PATH = "/Script/Project01.ShipDefinition"

# SmallSailer01 (V0.1.1): when Hull lands at /Game/Ship/SmallSailer01/Mesh/SM_SmallSailer01_Hull,
# add row ShipType_SmallSailer01 with Mesh = that Hull. MastRig Square/Lateen meshes are
# presentation/refit assets — not FShipDefinition.Mesh (see ship-system.mdc).

MESH_COG = "/Game/Temp/Ship1/Ship_1_tmp.Ship_1_tmp"
MESH_CARAVEL = "/Game/Temp/Ship2/Ship_2_tmp.Ship_2_tmp"
# No third temp mesh yet — Carrack reuses Cog hull until real art exists.
MESH_CARRACK = MESH_COG

# Row Name == ShipTypeId. Placeholder hulls; player claim stays TempCog.
SHIP_ROWS = [
    {
        "Name": "ShipType_TempCog",
        "ShipTypeId": "ShipType_TempCog",
        "DisplayName": "柯克船",
        "Mesh": MESH_COG,
        "BaseSpeed": 600.0,
        "BaseStrength": 10.0,
    },
    {
        "Name": "ShipType_TempCaravel",
        "ShipTypeId": "ShipType_TempCaravel",
        "DisplayName": "卡拉维尔",
        "Mesh": MESH_CARAVEL,
        "BaseSpeed": 720.0,
        "BaseStrength": 8.0,
    },
    {
        "Name": "ShipType_TempCarrack",
        "ShipTypeId": "ShipType_TempCarrack",
        "DisplayName": "克拉克帆船",
        "Mesh": MESH_CARRACK,
        "BaseSpeed": 480.0,
        "BaseStrength": 18.0,
    },
]


def find_row_struct():
    struct = unreal.load_object(None, ROW_STRUCT_PATH)
    if struct:
        return struct
    struct = unreal.find_object(None, ROW_STRUCT_PATH)
    if struct:
        return struct
    unreal.log_error(f"Row struct not found: {ROW_STRUCT_PATH} (compile Project01 first)")
    return None


def ensure_data_table(row_struct):
    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
        dt = unreal.EditorAssetLibrary.load_asset(ASSET_PATH)
        unreal.log(f"Using existing DataTable {ASSET_PATH}")
        return dt

    if not unreal.EditorAssetLibrary.does_directory_exist(ASSET_DIR):
        unreal.EditorAssetLibrary.make_directory(ASSET_DIR)

    factory = unreal.DataTableFactory()
    factory.set_editor_property("struct", row_struct)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    dt = asset_tools.create_asset(ASSET_NAME, ASSET_DIR, unreal.DataTable, factory)
    if not dt:
        unreal.log_error(f"Failed to create {ASSET_PATH}")
        return None
    unreal.log(f"Created DataTable {ASSET_PATH}")
    return dt


def mesh_column_values(dt):
    try:
        return [str(v) for v in unreal.DataTableFunctionLibrary.get_data_table_column_as_string(dt, "Mesh")]
    except Exception as exc:
        unreal.log_warning(f"Could not read Mesh column: {exc}")
        return []


def mesh_looks_set(values):
    expected = [row["Mesh"] for row in SHIP_ROWS]
    matched = 0
    for mesh in expected:
        token = mesh.split("/")[-1]
        if any(mesh in value or token in value for value in values):
            matched += 1
    return matched >= len(expected)


def rows_as_asset_path_json():
    rows = []
    for row in SHIP_ROWS:
        packed = dict(row)
        packed["Mesh"] = {"AssetPathName": row["Mesh"], "SubPathString": ""}
        rows.append(packed)
    return json.dumps(rows, ensure_ascii=False)


def rows_as_csv():
    lines = ["---,ShipTypeId,DisplayName,Mesh,BaseSpeed,BaseStrength"]
    for row in SHIP_ROWS:
        lines.append(
            f"{row['Name']},{row['ShipTypeId']},{row['DisplayName']},"
            f"StaticMesh'{row['Mesh']}',{row['BaseSpeed']:.6f},{row['BaseStrength']:.6f}"
        )
    return "\n".join(lines) + "\n"


def fill_table(dt):
    json_attempts = [
        json.dumps(SHIP_ROWS, ensure_ascii=False),
        rows_as_asset_path_json(),
    ]
    for json_str in json_attempts:
        ok = unreal.DataTableFunctionLibrary.fill_data_table_from_json_string(dt, json_str)
        if not ok:
            unreal.log_warning("fill_data_table_from_json_string failed for one format, trying next")
            continue
        values = mesh_column_values(dt)
        unreal.log(f"DT_Ships Mesh column: {values}")
        names = unreal.DataTableFunctionLibrary.get_data_table_row_names(dt)
        unreal.log(f"DT_Ships rows ({len(names)}): {[str(n) for n in names]}")
        if mesh_looks_set(values) and len(names) >= len(SHIP_ROWS):
            return True

    ok = unreal.DataTableFunctionLibrary.fill_data_table_from_csv_string(dt, rows_as_csv())
    if not ok:
        unreal.log_error("fill_data_table_from_csv_string failed")
        return False
    values = mesh_column_values(dt)
    unreal.log(f"DT_Ships Mesh column after CSV: {values}")
    names = unreal.DataTableFunctionLibrary.get_data_table_row_names(dt)
    unreal.log(f"DT_Ships rows ({len(names)}): {[str(n) for n in names]}")
    return mesh_looks_set(values) or len(names) >= len(SHIP_ROWS)


def main():
    row_struct = find_row_struct()
    if not row_struct:
        raise RuntimeError(f"missing row struct {ROW_STRUCT_PATH}")
    dt = ensure_data_table(row_struct)
    if not dt:
        raise RuntimeError(f"failed to create/load {ASSET_PATH}")
    current_struct = dt.get_editor_property("row_struct")
    if current_struct and current_struct.get_path_name() != row_struct.get_path_name():
        raise RuntimeError(
            f"Existing table has wrong row struct: {current_struct.get_path_name()} "
            f"(expected {row_struct.get_path_name()})"
        )
    if not fill_table(dt):
        raise RuntimeError("fill_data_table failed")
    unreal.EditorAssetLibrary.save_asset(ASSET_PATH, only_if_is_dirty=False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    unreal.log(f"DONE {ASSET_PATH}")


if __name__ == "__main__":
    run_main(main, "CreateShipsDataTable.py")
