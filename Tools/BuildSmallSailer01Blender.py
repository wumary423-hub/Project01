# -*- coding: utf-8 -*-
"""
ShipType_SmallSailer01 shared whitebox in Blender.

Modes are split so a later --ortho cannot wipe a hand-edited blend.

  --build
      Rebuild the generated whitebox, save
      assets/ships/ShipType_SmallSailer01/blender/ShipType_SmallSailer01_blockout.blend
      and render the perspective review PNG only.
      Never writes *_manual-*.blend.

  --ortho --input-blend <path>
      Open an existing .blend, do not rebuild geometry, do not save.
      Render five ortho views from cameras already in the file
      (or add missing cameras only).

  --perspective --input-blend <path>
      Same load rules; render perspective review only.

PowerShell:

    & "$env:BLENDER_EXE" --background --factory-startup --python `
        "E:\\newlife\\Project01\\Tools\\BuildSmallSailer01Blender.py" -- --build

    & "$env:BLENDER_EXE" --background --factory-startup --python `
        "E:\\newlife\\Project01\\Tools\\BuildSmallSailer01Blender.py" -- `
        --ortho --input-blend `
        "E:\\newlife\\Project01\\assets\\ships\\ShipType_SmallSailer01\\blender\\ShipType_SmallSailer01_blockout_manual-r1.blend"

No flag = refuse (will not reset the scene).
--build and --ortho together = refuse.

This is a structure-review blockout, not a UE FBX / socket / MastRig export.

Canonical spec still lists length 15 m as PROVISIONAL and stern as 两层.
ChatGPT brief 2026-08-23 treats LOA 15 m and mast 18 m as locked working
targets and stern as a single-level cabin with a railed roof deck.
Script uses those working numbers; it does not rewrite design.md.
Beam / draft stay UNSET — WORKING values only, not formal locks.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

try:
    import bpy
    import bmesh
    from mathutils import Vector
except ImportError as exc:
    raise SystemExit(
        "This script must be launched by Blender bpy, not by system Python.\n"
        r'& "$env:BLENDER_EXE" --background --factory-startup --python '
        r'"E:\newlife\Project01\Tools\BuildSmallSailer01Blender.py" -- --build'
    ) from exc


ASSET_ID = "ShipType_SmallSailer01"

# Blender: +X bow, +Z up, +Y port, -Y starboard (right-handed, blender_forward +X).
# Units: meters.

# Working targets from the 2026-08-23 ChatGPT brief. Canonical integration.yaml
# still has length_m PROVISIONAL and no mast-length field.
LOA_M = 15.0
MAST_LENGTH_M = 18.0

# UNSET in integration.yaml — working only, not a formal lock.
BEAM_M = 5.0
DRAFT_M = 1.32
DECK_Z = 0.96

STERN_CABIN_X0 = -6.70
STERN_CABIN_X1 = -3.55
STERN_CABIN_HEIGHT = 1.18
MAST_X = 1.55
HATCH_X = -0.85
HATCH_LEN = 1.35
HATCH_WID = 1.20

HULL_COLOR = (0.74, 0.73, 0.70, 1.0)
DECK_COLOR = (0.84, 0.82, 0.78, 1.0)
STRAKE_COLOR = (0.36, 0.34, 0.32, 1.0)
STERN_COLOR = (0.70, 0.68, 0.64, 1.0)
HATCH_COLOR = (0.30, 0.29, 0.27, 1.0)
MAST_COLOR = (0.56, 0.53, 0.48, 1.0)
RUDDER_COLOR = (0.46, 0.43, 0.39, 1.0)
WINDOW_COLOR = (0.16, 0.16, 0.15, 1.0)
WATER_COLOR = (0.62, 0.68, 0.72, 1.0)

CAMERA_NAMES = {
    "perspective": "Camera_Perspective_Review",
    "top": "Camera_Ortho_Top",
    "port": "Camera_Ortho_Port",
    "starboard": "Camera_Ortho_Starboard",
    "bow": "Camera_Ortho_Bow",
    "stern": "Camera_Ortho_Stern",
}

USAGE = """\
Usage (after Blender --python <this> --):
  --build
  --ortho --input-blend <path>
  --perspective --input-blend <path>
  optional: --skip-render
"""


def _log(msg: str) -> None:
    print(f"[BuildSmallSailer01Blender] {msg}", flush=True)


def parse_script_args() -> dict:
    argv = sys.argv
    extra = argv[argv.index("--") + 1 :] if "--" in argv else []

    def value_after(flag: str) -> str | None:
        if flag not in extra:
            return None
        idx = extra.index(flag)
        if idx + 1 >= len(extra) or extra[idx + 1].startswith("--"):
            return None
        return extra[idx + 1]

    return {
        "build": "--build" in extra,
        "ortho": "--ortho" in extra,
        "perspective": "--perspective" in extra,
        "skip_render": "--skip-render" in extra,
        "input_blend": value_after("--input-blend"),
    }


def resolve_paths() -> tuple[Path, Path, Path]:
    script = None
    if "--python" in sys.argv:
        idx = sys.argv.index("--python")
        if idx + 1 < len(sys.argv):
            script = Path(sys.argv[idx + 1]).resolve()
    if script is None:
        script = Path(__file__).resolve()
    project = script.parent.parent
    blender_dir = project / "assets" / "ships" / ASSET_ID / "blender"
    review_dir = blender_dir / "review"
    generated_blend = blender_dir / f"{ASSET_ID}_blockout.blend"
    return project, generated_blend, review_dir


def is_manual_blend(path: Path) -> bool:
    return "manual" in path.stem.lower()


def reset_scene() -> None:
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)
    for cam in list(bpy.data.cameras):
        bpy.data.cameras.remove(cam)
    for col in list(bpy.data.collections):
        if col.name != "Collection":
            bpy.data.collections.remove(col)
    default = bpy.data.collections.get("Collection")
    if default is not None:
        default.name = "SceneRoot"


def ensure_collection(name: str, parent: bpy.types.Collection | None = None) -> bpy.types.Collection:
    existing = bpy.data.collections.get(name)
    if existing is not None:
        return existing
    col = bpy.data.collections.new(name)
    host = parent or bpy.context.scene.collection
    host.children.link(col)
    return col


def set_object_color(obj: bpy.types.Object, color: tuple[float, float, float, float]) -> None:
    obj.color = color


def new_mesh_object(
    name: str,
    verts: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    collection: bpy.types.Collection,
    color: tuple[float, float, float, float],
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    set_object_color(obj, color)
    return obj


def add_box(
    name: str,
    size: tuple[float, float, float],
    location: tuple[float, float, float],
    collection: bpy.types.Collection,
    color: tuple[float, float, float, float],
) -> bpy.types.Object:
    sx, sy, sz = size
    hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
    verts = [
        (-hx, -hy, -hz),
        (hx, -hy, -hz),
        (hx, hy, -hz),
        (-hx, hy, -hz),
        (-hx, -hy, hz),
        (hx, -hy, hz),
        (hx, hy, hz),
        (-hx, hy, hz),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (2, 6, 7, 3),
        (0, 3, 7, 4),
        (1, 5, 6, 2),
    ]
    obj = new_mesh_object(name, verts, faces, collection, color)
    obj.location = location
    return obj


def add_cylinder(
    name: str,
    radius: float,
    depth: float,
    location: tuple[float, float, float],
    rotation: tuple[float, float, float],
    collection: bpy.types.Collection,
    color: tuple[float, float, float, float],
    segments: int = 18,
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=segments,
        radius1=radius,
        radius2=radius,
        depth=depth,
    )
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    collection.objects.link(obj)
    set_object_color(obj, color)
    return obj


def look_at(obj: bpy.types.Object, target: Vector) -> None:
    direction = target - obj.location
    if direction.length < 1e-6:
        return
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def look_horizontal(obj: bpy.types.Object, target_xy: Vector, z: float) -> None:
    target = Vector((target_xy.x, target_xy.y, z))
    obj.location.z = z
    look_at(obj, target)


def iter_mesh_objects(collections: list[bpy.types.Collection]) -> list[bpy.types.Object]:
    out: list[bpy.types.Object] = []
    for col in collections:
        for obj in col.objects:
            if obj.type == "MESH":
                out.append(obj)
    return out


def all_mesh_objects() -> list[bpy.types.Object]:
    return [obj for obj in bpy.data.objects if obj.type == "MESH" and obj.name != "ReviewWaterPlane"]


def world_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    mins = Vector((1e9, 1e9, 1e9))
    maxs = Vector((-1e9, -1e9, -1e9))
    for obj in objects:
        for corner in obj.bound_box:
            world = obj.matrix_world @ Vector(corner)
            mins.x = min(mins.x, world.x)
            mins.y = min(mins.y, world.y)
            mins.z = min(mins.z, world.z)
            maxs.x = max(maxs.x, world.x)
            maxs.y = max(maxs.y, world.y)
            maxs.z = max(maxs.z, world.z)
    return mins, maxs


def section_ring(x: float, hy: float, keel: float, deck: float) -> list[tuple[float, float, float]]:
    mid_z = (keel + deck) * 0.42
    return [
        (x, 0.0, keel),
        (x, -hy * 0.32, keel + 0.10),
        (x, -hy * 0.78, keel + 0.48),
        (x, -hy, mid_z),
        (x, -hy * 0.97, deck),
        (x, 0.0, deck + 0.05),
        (x, hy * 0.97, deck),
        (x, hy, mid_z),
        (x, hy * 0.78, keel + 0.48),
        (x, hy * 0.32, keel + 0.10),
    ]


def build_hull(collection: bpy.types.Collection) -> bpy.types.Object:
    half_beam = BEAM_M * 0.5
    # LOA working 15 m: stem ~+7.55 to stern ~-7.45.
    stations = [
        {"x": -7.45, "hy": 0.16, "keel": -0.80, "deck": 1.32},
        {"x": -7.20, "hy": 1.48, "keel": -0.96, "deck": 1.26},
        {"x": -6.40, "hy": 2.16, "keel": -1.14, "deck": 1.16},
        {"x": -4.70, "hy": 2.42, "keel": -1.26, "deck": 1.06},
        {"x": -2.10, "hy": half_beam, "keel": -DRAFT_M, "deck": 1.00},
        {"x": 0.00, "hy": half_beam, "keel": -DRAFT_M, "deck": DECK_Z},
        {"x": 2.40, "hy": 2.38, "keel": -1.26, "deck": 0.98},
        {"x": 4.60, "hy": 2.02, "keel": -1.10, "deck": 1.08},
        {"x": 6.20, "hy": 1.18, "keel": -0.74, "deck": 1.30},
        {"x": 7.15, "hy": 0.38, "keel": -0.32, "deck": 1.58},
        {"x": 7.55, "hy": 0.07, "keel": -0.04, "deck": 1.74},
    ]
    rings = [section_ring(s["x"], s["hy"], s["keel"], s["deck"]) for s in stations]
    n_ring = len(rings[0])
    verts: list[tuple[float, float, float]] = []
    for ring in rings:
        verts.extend(ring)
    faces: list[tuple[int, ...]] = []
    for i in range(len(rings) - 1):
        for j in range(n_ring):
            j2 = (j + 1) % n_ring
            a = i * n_ring + j
            b = i * n_ring + j2
            c = (i + 1) * n_ring + j2
            d = (i + 1) * n_ring + j
            faces.append((a, b, c, d))
    stern = tuple(range(n_ring - 1, -1, -1))
    bow_start = (len(rings) - 1) * n_ring
    faces.append(stern)
    faces.append(tuple(range(bow_start, bow_start + n_ring)))
    return new_mesh_object("Hull", verts, faces, collection, HULL_COLOR)


def apply_boolean_cut(hull: bpy.types.Object, cutter: bpy.types.Object) -> None:
    mod = hull.modifiers.new(cutter.name, "BOOLEAN")
    mod.operation = "DIFFERENCE"
    if hasattr(mod, "solver"):
        mod.solver = "FLOAT"
    mod.object = cutter
    bpy.context.view_layer.objects.active = hull
    hull.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def punch_gunports(hull: bpy.types.Object, collection: bpy.types.Collection) -> None:
    # Four equal hollow ports, two per side, mirrored. No guns this stage.
    port_size = (0.62, 1.10, 0.46)
    xs = (2.20, -1.70)
    z = 0.20
    y = 2.50
    bpy.context.view_layer.update()
    for i, x in enumerate(xs, start=1):
        for side, yy in (("Port", y), ("Starboard", -y)):
            cutter = add_box(f"GunportCutter_{side}_{i:02d}", port_size, (x, yy, z), collection, WINDOW_COLOR)
            apply_boolean_cut(hull, cutter)
            add_box(
                f"Gunport_{side}_{i:02d}",
                (0.58, 0.08, 0.42),
                (x, yy * 0.97, z),
                collection,
                WINDOW_COLOR,
            )


def build_deck_and_hatch(collection: bpy.types.Collection) -> None:
    add_box("Deck", (8.0, 3.90, 0.08), (0.70, 0.0, DECK_Z + 0.02), collection, DECK_COLOR)
    mast_aft = MAST_X - 0.22
    hatch_fwd = HATCH_X + HATCH_LEN * 0.5
    if hatch_fwd > mast_aft - 0.15:
        raise RuntimeError("hatch overlaps mast; adjust HATCH_X / MAST_X")
    add_box(
        "MastStep",
        (0.55, 0.55, 0.14),
        (MAST_X, 0.0, DECK_Z + 0.10),
        collection,
        STRAKE_COLOR,
    )
    add_box(
        "CargoHatchCoaming",
        (HATCH_LEN + 0.16, HATCH_WID + 0.16, 0.12),
        (HATCH_X, 0.0, DECK_Z + 0.10),
        collection,
        STRAKE_COLOR,
    )
    add_box(
        "CargoHatchWell",
        (HATCH_LEN, HATCH_WID, 0.08),
        (HATCH_X, 0.0, DECK_Z + 0.03),
        collection,
        HATCH_COLOR,
    )
    add_box(
        "CargoHatchCover",
        (HATCH_LEN - 0.08, HATCH_WID - 0.08, 0.04),
        (HATCH_X, 0.0, DECK_Z + 0.14),
        collection,
        HATCH_COLOR,
    )


def build_strakes(collection: bpy.types.Collection) -> None:
    add_box("RubbingStrake_Port", (8.2, 0.10, 0.22), (0.20, 2.50, 0.18), collection, STRAKE_COLOR)
    add_box("RubbingStrake_Starboard", (8.2, 0.10, 0.22), (0.20, -2.50, 0.18), collection, STRAKE_COLOR)
    add_box("GunwaleRail_Port", (8.4, 0.10, 0.16), (0.25, 2.40, DECK_Z + 0.14), collection, STRAKE_COLOR)
    add_box("GunwaleRail_Starboard", (8.4, 0.10, 0.16), (0.25, -2.40, DECK_Z + 0.14), collection, STRAKE_COLOR)


def stern_roof_z() -> float:
    return DECK_Z + STERN_CABIN_HEIGHT


def build_stern(collection: bpy.types.Collection) -> None:
    # Single-level cabin: floor = main deck. Roof = railed walkable platform.
    # Side walls flush with the gunwale line (not an inset house).
    length = STERN_CABIN_X1 - STERN_CABIN_X0
    center_x = (STERN_CABIN_X0 + STERN_CABIN_X1) * 0.5
    width = 4.30
    wall_h = STERN_CABIN_HEIGHT
    cabin_z = DECK_Z + wall_h * 0.5
    add_box("SternCabin", (length, width, wall_h), (center_x, 0.0, cabin_z), collection, STERN_COLOR)
    add_box(
        "SternRoof",
        (length + 0.08, width + 0.08, 0.08),
        (center_x, 0.0, stern_roof_z() + 0.04),
        collection,
        DECK_COLOR,
    )
    rail_h = 0.32
    rail_z = stern_roof_z() + 0.20
    add_box("SternRoofRail_Port", (length + 0.08, 0.07, rail_h), (center_x, width * 0.5, rail_z), collection, STRAKE_COLOR)
    add_box("SternRoofRail_Starboard", (length + 0.08, 0.07, rail_h), (center_x, -width * 0.5, rail_z), collection, STRAKE_COLOR)
    add_box("SternRoofRail_Aft", (0.07, width + 0.08, rail_h), (STERN_CABIN_X0, 0.0, rail_z), collection, STRAKE_COLOR)
    add_box("SternRoofRail_Fwd", (0.07, width + 0.08, rail_h), (STERN_CABIN_X1, 0.0, rail_z), collection, STRAKE_COLOR)

    win_z = DECK_Z + 0.58
    add_box("SternWindow_Port_01", (0.28, 0.06, 0.22), (center_x + 0.55, width * 0.5, win_z), collection, WINDOW_COLOR)
    add_box("SternWindow_Port_02", (0.28, 0.06, 0.22), (center_x - 0.55, width * 0.5, win_z), collection, WINDOW_COLOR)
    add_box("SternWindow_Starboard_01", (0.28, 0.06, 0.22), (center_x + 0.55, -width * 0.5, win_z), collection, WINDOW_COLOR)
    add_box("SternWindow_Starboard_02", (0.28, 0.06, 0.22), (center_x - 0.55, -width * 0.5, win_z), collection, WINDOW_COLOR)
    add_box("SternWindow_Aft_01", (0.06, 0.28, 0.22), (STERN_CABIN_X0, 0.0, win_z), collection, WINDOW_COLOR)


def build_stairs(collection: bpy.types.Collection) -> None:
    # One internal starboard run: main deck -> stern roof. Not a second exterior stair.
    step_count = 7
    step_l = 0.30
    step_h = (stern_roof_z() - DECK_Z) / step_count
    step_w = 0.62
    start_x = STERN_CABIN_X1 - 0.18
    y = -1.58
    for i in range(step_count):
        z = DECK_Z + step_h * (i + 0.5)
        x = start_x - i * (step_l * 0.82)
        add_box(f"SternStair_{i + 1:02d}", (step_l, step_w, step_h), (x, y, z), collection, DECK_COLOR)
    hatch_x = start_x - (step_count - 1) * (step_l * 0.82) * 0.45
    add_box(
        "CompanionwayOpening",
        (1.15, 0.78, 0.06),
        (hatch_x, y, stern_roof_z() + 0.09),
        collection,
        HATCH_COLOR,
    )


def build_mast(collection: bpy.types.Collection) -> None:
    # Centerline Y=0. Visible spar length = working 18 m, standing on deck.
    mast_z = DECK_Z + MAST_LENGTH_M * 0.5
    add_cylinder("Mast_Main", 0.14, MAST_LENGTH_M, (MAST_X, 0.0, mast_z), (0.0, 0.0, 0.0), collection, MAST_COLOR, 20)
    yard_z = DECK_Z + 12.4
    add_cylinder("Yard_Main", 0.12, 9.2, (MAST_X, 0.0, yard_z), (math.pi * 0.5, 0.0, 0.0), collection, STRAKE_COLOR, 16)
    nest_z = DECK_Z + 15.6
    add_cylinder("CrowsNest", 0.70, 0.18, (MAST_X, 0.0, nest_z), (0.0, 0.0, 0.0), collection, STRAKE_COLOR, 16)
    add_cylinder("CrowsNestRail", 0.72, 0.36, (MAST_X, 0.0, nest_z + 0.24), (0.0, 0.0, 0.0), collection, HATCH_COLOR, 16)


def build_bowsprit(collection: bpy.types.Collection) -> None:
    # Cylinder default axis is +Z. Rotate onto +X, then pitch up ~16 deg.
    pitch_from_horizontal = math.radians(16.0)
    add_cylinder(
        "Bowsprit",
        0.10,
        3.8,
        (8.90, 0.0, 2.05),
        (0.0, math.pi * 0.5 - pitch_from_horizontal, 0.0),
        collection,
        MAST_COLOR,
        14,
    )
    add_box("BowspritStep", (0.90, 0.32, 0.28), (7.35, 0.0, 1.62), collection, STRAKE_COLOR)


def build_rudder(collection: bpy.types.Collection) -> None:
    # Centerline. Rudder top must stay at or below the stern gunwale (~1.32).
    stern_gunwale_z = 1.32
    rudder_top = stern_gunwale_z - 0.06
    rudder_h = 2.00
    rudder_z = rudder_top - rudder_h * 0.5
    add_box("Rudder", (0.22, 0.08, rudder_h), (-7.62, 0.0, rudder_z), collection, RUDDER_COLOR)
    stock_h = rudder_top - 0.10
    add_box("RudderStock", (0.10, 0.09, stock_h), (-7.40, 0.0, stock_h * 0.5), collection, RUDDER_COLOR)


def build_water(collection: bpy.types.Collection) -> bpy.types.Object:
    return add_box("ReviewWaterPlane", (40.0, 28.0, 0.04), (0.0, 0.0, -0.02), collection, WATER_COLOR)


def parent_to_root(root: bpy.types.Object, collections: list[bpy.types.Collection]) -> None:
    for obj in iter_mesh_objects(collections):
        obj.parent = root


def add_camera(
    name: str,
    location: Vector,
    target: Vector,
    collection: bpy.types.Collection | None,
    ortho: bool,
    ortho_scale: float,
) -> bpy.types.Object:
    data = bpy.data.cameras.new(name)
    data.type = "ORTHO" if ortho else "PERSP"
    data.clip_start = 0.05
    data.clip_end = 400.0
    if ortho:
        data.ortho_scale = ortho_scale
    else:
        data.lens = 28.0
    obj = bpy.data.objects.new(name, data)
    obj.location = location
    look_at(obj, target)
    host = collection or bpy.context.scene.collection
    host.objects.link(obj)
    return obj


def setup_cameras(
    ship_objects: list[bpy.types.Object],
    collection: bpy.types.Collection | None,
) -> dict[str, bpy.types.Object]:
    mins, maxs = world_bounds(ship_objects)
    size = maxs - mins
    target = Vector((0.15, 0.0, 1.20))
    margin = 1.24
    persp_dir = Vector((0.84, 1.16, 0.78)).normalized()
    persp_dist = max(size.length * 1.48, 32.0)
    persp = add_camera(
        CAMERA_NAMES["perspective"],
        target + persp_dir * persp_dist,
        target,
        collection,
        ortho=False,
        ortho_scale=1.0,
    )

    far = 48.0
    side_z = DECK_Z + 0.05
    side_scale = max(size.x, size.z) * margin
    end_scale = max(size.y, size.z) * margin
    cameras = {
        "perspective": persp,
        "top": add_camera(
            CAMERA_NAMES["top"],
            Vector((target.x, 0.0, far)),
            Vector((target.x, 0.0, 0.0)),
            collection,
            True,
            max(size.x, size.y) * margin,
        ),
        "port": add_camera(
            CAMERA_NAMES["port"],
            Vector((target.x, far, side_z)),
            Vector((target.x, 0.0, side_z)),
            collection,
            True,
            side_scale,
        ),
        "starboard": add_camera(
            CAMERA_NAMES["starboard"],
            Vector((target.x, -far, side_z)),
            Vector((target.x, 0.0, side_z)),
            collection,
            True,
            side_scale,
        ),
        "bow": add_camera(
            CAMERA_NAMES["bow"],
            Vector((far, 0.0, side_z + 2.0)),
            Vector((0.0, 0.0, side_z + 2.0)),
            collection,
            True,
            end_scale,
        ),
        "stern": add_camera(
            CAMERA_NAMES["stern"],
            Vector((-far, 0.0, side_z + 2.0)),
            Vector((0.0, 0.0, side_z + 2.0)),
            collection,
            True,
            end_scale,
        ),
    }
    return cameras


def collect_or_create_cameras() -> dict[str, bpy.types.Object]:
    found: dict[str, bpy.types.Object] = {}
    missing = False
    for key, name in CAMERA_NAMES.items():
        obj = bpy.data.objects.get(name)
        if obj is not None and obj.type == "CAMERA":
            found[key] = obj
        else:
            missing = True
    if not missing:
        return found
    _log("some review cameras missing; adding cameras only (no mesh rebuild)")
    cam_col = bpy.data.collections.get("COL_Cameras")
    created = setup_cameras(all_mesh_objects(), cam_col)
    created.update(found)
    return created


def setup_workbench(scene: bpy.types.Scene, line_style: bool) -> None:
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    shading = scene.display.shading
    shading.light = "STUDIO"
    shading.studio_light = "Default"
    shading.show_shadows = False
    shading.show_cavity = True
    shading.cavity_type = "BOTH"
    shading.curvature_ridge_factor = 1.0
    shading.curvature_valley_factor = 1.0
    shading.show_object_outline = True
    shading.object_outline_color = (0.08, 0.08, 0.08)
    if line_style:
        shading.color_type = "SINGLE"
        shading.single_color = (0.92, 0.91, 0.88)
    else:
        shading.color_type = "OBJECT"

    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene.world = world
    bg_color = (0.78, 0.80, 0.82, 1.0) if not line_style else (0.88, 0.88, 0.86, 1.0)
    tree = world.node_tree
    if tree is not None:
        background = tree.nodes.get("Background")
        if background is not None and background.inputs:
            background.inputs[0].default_value = bg_color
    else:
        world.color = bg_color[:3]


def set_water_visible(visible: bool) -> None:
    water = bpy.data.objects.get("ReviewWaterPlane")
    if water is None:
        return
    water.hide_render = not visible
    water.hide_viewport = not visible


def render_camera(scene: bpy.types.Scene, camera: bpy.types.Object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    scene.camera = camera
    scene.render.filepath = str(path)
    _log(f"render {camera.name} -> {path}")
    bpy.ops.render.render(write_still=True)


def render_perspective(scene: bpy.types.Scene, cameras: dict[str, bpy.types.Object], review_dir: Path) -> None:
    setup_workbench(scene, line_style=False)
    set_water_visible(True)
    render_camera(scene, cameras["perspective"], review_dir / f"{ASSET_ID}_blockout_perspective.png")


def render_ortho(scene: bpy.types.Scene, cameras: dict[str, bpy.types.Object], review_dir: Path) -> None:
    setup_workbench(scene, line_style=True)
    set_water_visible(False)
    for key, suffix in (
        ("top", "ortho_top"),
        ("port", "ortho_port"),
        ("starboard", "ortho_starboard"),
        ("bow", "ortho_bow"),
        ("stern", "ortho_stern"),
    ):
        render_camera(scene, cameras[key], review_dir / f"{ASSET_ID}_blockout_{suffix}.png")


def open_blend(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"blend not found: {path}")
    _log(f"open existing blend (no rebuild, no save): {path}")
    bpy.ops.wm.open_mainfile(filepath=str(path))


def build_whitebox() -> dict[str, bpy.types.Object]:
    reset_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    root_col = ensure_collection("ShipType_SmallSailer01")
    hull_col = ensure_collection("COL_Hull", root_col)
    deck_col = ensure_collection("COL_Deck", root_col)
    stern_col = ensure_collection("COL_Stern", root_col)
    mast_col = ensure_collection("COL_Mast", root_col)
    helper_col = ensure_collection("COL_ReviewHelpers", root_col)
    cam_col = ensure_collection("COL_Cameras", root_col)

    root = bpy.data.objects.new(ASSET_ID, None)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 1.0
    root_col.objects.link(root)

    hull = build_hull(hull_col)
    punch_gunports(hull, hull_col)
    build_strakes(hull_col)
    build_deck_and_hatch(deck_col)
    build_stern(stern_col)
    build_stairs(stern_col)
    build_mast(mast_col)
    build_bowsprit(mast_col)
    build_rudder(hull_col)
    build_water(helper_col)

    ship_cols = [hull_col, deck_col, stern_col, mast_col]
    parent_to_root(root, ship_cols)
    bpy.context.view_layer.update()
    for name in ("Mast_Main", "Yard_Main", "CrowsNest", "Bowsprit", "Rudder"):
        obj = bpy.data.objects.get(name)
        if obj is None:
            _log(f"missing object {name}")
        else:
            _log(f"{name} loc={tuple(round(c, 2) for c in obj.location)}")
    return setup_cameras(iter_mesh_objects(ship_cols), cam_col)


def main() -> int:
    args = parse_script_args()
    project, generated_blend, review_dir = resolve_paths()
    _log(f"project={project}")

    if args["build"] and args["ortho"]:
        _log("refuse: --build and --ortho cannot run together")
        return 2
    if not args["build"] and not args["ortho"] and not args["perspective"]:
        _log("refuse: no mode. Will not reset the scene.")
        print(USAGE)
        return 2
    if args["ortho"] and not args["input_blend"]:
        _log("refuse: --ortho requires --input-blend <path> so a hand-edited file is not rebuilt")
        return 2
    if args["perspective"] and not args["build"] and not args["input_blend"]:
        _log("refuse: --perspective without --build requires --input-blend <path>")
        return 2

    scene = bpy.context.scene

    if args["build"]:
        if is_manual_blend(generated_blend):
            _log(f"refuse: generated path looks manual: {generated_blend}")
            return 2
        _log("mode=--build (perspective review only; no ortho)")
        cameras = build_whitebox()
        scene = bpy.context.scene
        scene.camera = cameras["perspective"]
        generated_blend.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(generated_blend))
        _log(f"saved generated blend {generated_blend}")
        if not args["skip_render"]:
            render_perspective(scene, cameras, review_dir)
        bpy.ops.wm.save_mainfile()
        _log("build done; --ortho was not run")
        return 0

    input_blend = Path(args["input_blend"]).resolve()
    open_blend(input_blend)
    scene = bpy.context.scene
    cameras = collect_or_create_cameras()
    if args["perspective"] and not args["skip_render"]:
        render_perspective(scene, cameras, review_dir)
    if args["ortho"]:
        if not args["skip_render"]:
            render_ortho(scene, cameras, review_dir)
        _log("ortho done; blend was not saved (hand edits preserved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
