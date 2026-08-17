# -*- coding: utf-8 -*-
"""
Validate SmallSailer01 (and DT_Ships hull) StaticMesh sockets + expected mesh paths.
Run in editor:
  py "E:/newlife/Project01/Tools/ValidateShipMeshes.py"

Authority: .cursor/rules/ship-system.mdc V0.1.1
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
MESH_ROOT = "/Game/Ship/SmallSailer01/Mesh"
HULL_ASSET = f"{MESH_ROOT}/SM_{WORKFLOW}_Hull"
DT_SHIPS = "/Game/Ship/DT_Ships"
CATALOG_TYPE_ID = "ShipType_SmallSailer01"

PHASE1_RIG_TYPES = ("Square", "Lateen")
SAIL_STATES = ("Full", "Half", "Furled")
DEFERRED_RIG_TYPES = ("Gaff",)

PONTOON_SOCKETS = (
    "Pontoon_Bow",
    "Pontoon_Stern",
    "Pontoon_Port",
    "Pontoon_Starboard",
)

HULL_WARN_SOCKETS = (
    "Attach_MastRig_01",
    "Attach_Figurehead",
    "Attach_Rudder",
    "Attach_Anchor",
    "Attach_FX_Fire",
    "Attach_Mast_Broken",
    "Attach_Headsail_01",
    "Attach_Weapon_Port_01",
    "Attach_Weapon_Starboard_01",
)

MASTRIG_FLAG_SOCKET = "Attach_Flag"

HEADSAIL_MESHES = tuple(
    f"{MESH_ROOT}/SM_{WORKFLOW}_Headsail01_{State}" for State in SAIL_STATES
)


def _log_ok(msg: str) -> None:
    unreal.log(f"[ValidateShipMeshes] OK  {msg}")


def _log_warn(msg: str) -> None:
    unreal.log_warning(f"[ValidateShipMeshes] WARN {msg}")


def _log_error(msg: str) -> None:
    unreal.log_error(f"[ValidateShipMeshes] ERR {msg}")


def _load_static_mesh(asset_path: str) -> unreal.StaticMesh | None:
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        return None
    return unreal.EditorAssetLibrary.load_asset(asset_path)


def _socket_names(mesh: unreal.StaticMesh) -> set[str]:
    names: set[str] = set()
    for idx in range(mesh.get_num_sockets()):
        sock = mesh.get_socket_by_index(idx)
        if sock:
            names.add(str(sock.socket_name))
    return names


def _check_sockets(mesh: unreal.StaticMesh, label: str, required: tuple[str, ...], severity_error: bool) -> int:
    issues = 0
    present = _socket_names(mesh)
    for name in required:
        if name in present:
            _log_ok(f"{label}: socket {name}")
        else:
            issues += 1
            msg = f"{label}: missing socket {name}"
            if severity_error:
                _log_error(msg)
            else:
                _log_warn(msg)
    return issues


def _mast_rig_asset_name(rig_type: str, state: str) -> str:
    return f"{MESH_ROOT}/SM_{WORKFLOW}_MastRig01_{rig_type}_{state}"


def validate_hull() -> tuple[int, int]:
    errors = 0
    warnings = 0
    mesh = _load_static_mesh(HULL_ASSET)
    if not mesh:
        _log_error(f"Hull asset missing: {HULL_ASSET}")
        return 1, 0

    errors += _check_sockets(mesh, "Hull", PONTOON_SOCKETS, severity_error=True)
    warnings += _check_sockets(mesh, "Hull", HULL_WARN_SOCKETS, severity_error=False)
    return errors, warnings


def validate_mast_rigs() -> tuple[int, int]:
    errors = 0
    warnings = 0
    for rig_type in PHASE1_RIG_TYPES:
        for state in SAIL_STATES:
            path = _mast_rig_asset_name(rig_type, state)
            mesh = _load_static_mesh(path)
            if not mesh:
                warnings += 1
                _log_warn(f"MastRig asset missing: {path}")
                continue
            _log_ok(f"MastRig asset exists: {path}")
            warnings += _check_sockets(mesh, path, (MASTRIG_FLAG_SOCKET,), severity_error=False)

    for rig_type in DEFERRED_RIG_TYPES:
        any_found = any(
            unreal.EditorAssetLibrary.does_asset_exist(_mast_rig_asset_name(rig_type, state))
            for state in SAIL_STATES
        )
        if any_found:
            _log_warn(
                f"Deferred RigType {rig_type} meshes present — OK for future, not required phase one"
            )
    return errors, warnings


def validate_headsail_optional() -> int:
    warnings = 0
    any_found = any(unreal.EditorAssetLibrary.does_asset_exist(p) for p in HEADSAIL_MESHES)
    if any_found:
        _log_ok("Headsail retrofit meshes present (optional until refit slice)")
        for path in HEADSAIL_MESHES:
            mesh = _load_static_mesh(path)
            if mesh:
                _log_ok(f"Headsail asset: {path}")
            else:
                warnings += 1
                _log_warn(f"Headsail asset missing: {path}")
    else:
        _log_ok("Headsail meshes not imported yet — expected for starter loadout")
    return warnings


def validate_dt_ships_hull() -> int:
    if not unreal.EditorAssetLibrary.does_asset_exist(DT_SHIPS):
        _log_warn(f"DataTable missing: {DT_SHIPS}")
        return 0

    dt = unreal.EditorAssetLibrary.load_asset(DT_SHIPS)
    if not dt:
        _log_warn(f"Could not load: {DT_SHIPS}")
        return 0

    try:
        row_names = unreal.DataTableFunctionLibrary.get_data_table_row_names(dt)
    except Exception as exc:
        _log_warn(f"DT_Ships row scan failed: {exc}")
        return 0

    names = {str(n) for n in row_names}
    if CATALOG_TYPE_ID not in names:
        _log_warn(
            f"DT_Ships has no row {CATALOG_TYPE_ID} yet — add when Hull lands (see ship-system.mdc)"
        )
        return 0

    # Mesh column string check (best-effort)
    try:
        mesh_values = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(dt, "Mesh")
        row_index = list(names).index(CATALOG_TYPE_ID) if CATALOG_TYPE_ID in names else -1
        unreal.log(f"[ValidateShipMeshes] DT row {CATALOG_TYPE_ID} present; Mesh column rows={len(mesh_values)}")
    except Exception:
        pass

    return 0


def main() -> None:
    total_errors = 0
    total_warnings = 0

    unreal.log("[ValidateShipMeshes] --- SmallSailer01 V0.1.1 ---")

    e, w = validate_hull()
    total_errors += e
    total_warnings += w

    e, w = validate_mast_rigs()
    total_errors += e
    total_warnings += w

    total_warnings += validate_headsail_optional()
    total_warnings += validate_dt_ships_hull()

    unreal.log(
        f"[ValidateShipMeshes] DONE errors={total_errors} warnings={total_warnings}"
    )
    if total_errors > 0:
        raise RuntimeError(f"ValidateShipMeshes: {total_errors} error(s)")


if __name__ == "__main__":
    run_main(main, "ValidateShipMeshes.py")
