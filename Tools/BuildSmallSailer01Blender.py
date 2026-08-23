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

Locked (design.md 0.1.6+ / integration.yaml):
  length 15 m, main mast 18 m (step to truck), single-level stern,
  four equal top-deck gunports, one compact hatch, one in-hull stair.
Stair side is starboard (LOCKED in this update).
Beam / draft stay UNSET — WORKING values only.
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

# Locked design facts.
LOA_M = 15.0
MAST_LENGTH_M = 18.0

# UNSET in integration.yaml — working only, not a formal lock.
BEAM_M = 5.6
DRAFT_M = 2.15
DECK_Z = 1.45
BULWARK_H = 0.95

# Midship slightly aft of x=0. Hatch stays compact and fully aft of the mast.
MAST_X = -0.55
HATCH_X = -2.10
HATCH_LEN = 1.30
HATCH_WID = 1.15

# Stern cabin: X0 = aft wall, X1 = bow-facing front wall.
STERN_CABIN_X0 = -6.90
STERN_CABIN_X1 = -4.15
STERN_CABIN_HEIGHT = 2.18
STAIR_Y = -1.95

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
    skip = {"ReviewWaterPlane", "ReviewBackdrop"}
    return [obj for obj in bpy.data.objects if obj.type == "MESH" and obj.name not in skip]


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


def hull_stations() -> list[dict[str, float]]:
    xs = (
        -7.50, -7.25, -6.85, -6.30, -5.55, -4.50, -3.20, -1.70,
        0.00, 1.60, 3.10, 4.40, 5.40, 6.15, 6.75, 7.20, 7.50,
    )
    out: list[dict[str, float]] = []
    for x in xs:
        u = x / 7.50
        abs_u = abs(u)
        hy = BEAM_M * 0.5
        if abs_u > 0.20:
            s = (abs_u - 0.20) / 0.80
            hy *= 1.0 - (s ** 1.45) * 0.88
        if u > 0.52:
            hy *= max(0.07, 1.0 - ((u - 0.52) / 0.48) ** 1.55 * 0.82)
        if u < -0.50:
            hy *= max(0.16, 1.0 - ((-u - 0.50) / 0.50) ** 1.25 * 0.62)
        keel = -DRAFT_M + 0.85 * (u ** 2) + 1.55 * max(u, 0.0) ** 2.15
        deck = DECK_Z + 0.48 * (u ** 2) + 0.32 * max(u, 0.0) ** 2
        out.append({"x": x, "hy": max(hy, 0.07), "keel": keel, "deck": deck})
    return out


def half_beam_at(x: float) -> float:
    stations = hull_stations()
    if x <= stations[0]["x"]:
        return stations[0]["hy"]
    if x >= stations[-1]["x"]:
        return stations[-1]["hy"]
    for i in range(len(stations) - 1):
        a, b = stations[i], stations[i + 1]
        if a["x"] <= x <= b["x"]:
            t = (x - a["x"]) / (b["x"] - a["x"])
            return a["hy"] + t * (b["hy"] - a["hy"])
    return stations[-1]["hy"]


def deck_z_at(x: float) -> float:
    stations = hull_stations()
    if x <= stations[0]["x"]:
        return stations[0]["deck"]
    if x >= stations[-1]["x"]:
        return stations[-1]["deck"]
    for i in range(len(stations) - 1):
        a, b = stations[i], stations[i + 1]
        if a["x"] <= x <= b["x"]:
            t = (x - a["x"]) / (b["x"] - a["x"])
            return a["deck"] + t * (b["deck"] - a["deck"])
    return DECK_Z


def section_ring(x: float, hy: float, keel: float, deck: float) -> list[tuple[float, float, float]]:
    # Rounded cog section: full belly, soft bilge, slight tumblehome. Not a box.
    profile = (
        (0.00, 0.00),
        (0.18, 0.06),
        (0.42, 0.16),
        (0.68, 0.30),
        (0.88, 0.48),
        (0.99, 0.68),
        (1.00, 0.84),
        (0.96, 1.00),
    )
    span = deck - keel
    starboard = [(x, -hy * yf, keel + span * zf) for yf, zf in profile]
    port = [(x, hy * yf, keel + span * zf) for yf, zf in reversed(profile) if yf > 0.0]
    return starboard + [(x, 0.0, deck + 0.03)] + port


def loft_from_rings(name: str, rings: list[list[tuple[float, float, float]]], collection, color) -> bpy.types.Object:
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
    return new_mesh_object(name, verts, faces, collection, color)


def build_hull(collection: bpy.types.Collection) -> bpy.types.Object:
    stations = hull_stations()
    rings = [section_ring(s["x"], s["hy"], s["keel"], s["deck"]) for s in stations]
    hull = loft_from_rings("Hull", rings, collection, HULL_COLOR)
    bpy.context.view_layer.objects.active = hull
    hull.select_set(True)
    sub = hull.modifiers.new("HullSmooth", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 1
    bpy.ops.object.modifier_apply(modifier=sub.name)
    return hull


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


def punch_gunports(targets: list[bpy.types.Object], collection: bpy.types.Collection) -> None:
    # Four equal through-holes at top-deck freeboard. No filler plates, no guns.
    port_size = (0.70, 1.40, 0.52)
    xs = (1.70, -2.55)
    z = DECK_Z + 0.32
    bpy.context.view_layer.update()
    for i, x in enumerate(xs, start=1):
        y = half_beam_at(x)
        for side, yy in (("Port", y), ("Starboard", -y)):
            for target in targets:
                cutter = add_box(
                    f"GunportCutter_{target.name}_{side}_{i:02d}",
                    port_size,
                    (x, yy, z),
                    collection,
                    WINDOW_COLOR,
                )
                apply_boolean_cut(target, cutter)


def build_deck_and_hatch(collection: bpy.types.Collection) -> None:
    stations = [s for s in hull_stations() if -6.6 <= s["x"] <= 6.4]
    verts: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    for i, s in enumerate(stations):
        inner = s["hy"] * 0.90
        z = s["deck"] + 0.03
        verts.append((s["x"], -inner, z))
        verts.append((s["x"], inner, z))
        if i > 0:
            a = (i - 1) * 2
            faces.append((a, a + 1, a + 3, a + 2))
    new_mesh_object("Deck", verts, faces, collection, DECK_COLOR)

    mast_aft = MAST_X - 0.28
    hatch_fwd = HATCH_X + HATCH_LEN * 0.5
    if hatch_fwd > mast_aft - 0.10:
        raise RuntimeError("hatch overlaps mast; adjust HATCH_X / MAST_X")
    add_box("MastStep", (0.58, 0.58, 0.16), (MAST_X, 0.0, DECK_Z + 0.10), collection, STRAKE_COLOR)
    add_box(
        "CargoHatchCoaming",
        (HATCH_LEN + 0.16, HATCH_WID + 0.16, 0.12),
        (HATCH_X, 0.0, DECK_Z + 0.10),
        collection,
        STRAKE_COLOR,
    )
    add_box("CargoHatchWell", (HATCH_LEN, HATCH_WID, 0.08), (HATCH_X, 0.0, DECK_Z + 0.03), collection, HATCH_COLOR)
    add_box(
        "CargoHatchCover",
        (HATCH_LEN - 0.08, HATCH_WID - 0.08, 0.04),
        (HATCH_X, 0.0, DECK_Z + 0.14),
        collection,
        HATCH_COLOR,
    )


def build_bulwarks(collection: bpy.types.Collection) -> bpy.types.Object:
    stations = [s for s in hull_stations() if -7.2 <= s["x"] <= 6.9]
    rings: list[list[tuple[float, float, float]]] = []
    for s in stations:
        hy = s["hy"] * 0.99
        z0 = s["deck"]
        z1 = s["deck"] + BULWARK_H
        thick = 0.10
        rings.append(
            [
                (s["x"], -hy, z0),
                (s["x"], -hy + thick, z0),
                (s["x"], -hy + thick, z1),
                (s["x"], -hy, z1),
                (s["x"], hy, z1),
                (s["x"], hy - thick, z1),
                (s["x"], hy - thick, z0),
                (s["x"], hy, z0),
            ]
        )
    return loft_from_rings("Bulwarks", rings, collection, HULL_COLOR)


def build_strakes(collection: bpy.types.Collection) -> None:
    # Mid-height wooden rubbing strakes, not at the waterline and not gunport plates.
    add_box("RubbingStrake_Port", (7.0, 0.12, 0.22), (0.10, 2.82, DECK_Z - 0.35), collection, STRAKE_COLOR)
    add_box("RubbingStrake_Starboard", (7.0, 0.12, 0.22), (0.10, -2.82, DECK_Z - 0.35), collection, STRAKE_COLOR)


def stern_roof_z() -> float:
    return DECK_Z + STERN_CABIN_HEIGHT


def stern_half_widths() -> tuple[float, float]:
    return half_beam_at(STERN_CABIN_X1) * 0.99, half_beam_at(STERN_CABIN_X0) * 0.99


def add_trapezoid_prism(
    name: str,
    x_fwd: float,
    x_aft: float,
    hy_fwd: float,
    hy_aft: float,
    z0: float,
    z1: float,
    collection: bpy.types.Collection,
    color: tuple[float, float, float, float],
) -> bpy.types.Object:
    verts = [
        (x_fwd, -hy_fwd, z0),
        (x_fwd, hy_fwd, z0),
        (x_aft, hy_aft, z0),
        (x_aft, -hy_aft, z0),
        (x_fwd, -hy_fwd, z1),
        (x_fwd, hy_fwd, z1),
        (x_aft, hy_aft, z1),
        (x_aft, -hy_aft, z1),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]
    return new_mesh_object(name, verts, faces, collection, color)


def build_open_rail(collection: bpy.types.Collection, hy_fwd: float, hy_aft: float) -> None:
    z0 = stern_roof_z() + 0.06
    z1 = z0 + 0.42
    posts = [
        (STERN_CABIN_X1, -hy_fwd),
        (STERN_CABIN_X1, hy_fwd),
        (STERN_CABIN_X0, -hy_aft),
        (STERN_CABIN_X0, hy_aft),
        ((STERN_CABIN_X0 + STERN_CABIN_X1) * 0.5, -(hy_fwd + hy_aft) * 0.5),
        ((STERN_CABIN_X0 + STERN_CABIN_X1) * 0.5, (hy_fwd + hy_aft) * 0.5),
    ]
    for i, (x, y) in enumerate(posts, start=1):
        add_box(f"SternRailPost_{i:02d}", (0.07, 0.07, z1 - z0), (x, y, (z0 + z1) * 0.5), collection, STRAKE_COLOR)
    rail_z = z1 - 0.04
    add_box("SternRail_Fwd", (0.06, hy_fwd * 2.0, 0.05), (STERN_CABIN_X1, 0.0, rail_z), collection, STRAKE_COLOR)
    add_box("SternRail_Aft", (0.06, hy_aft * 2.0, 0.05), (STERN_CABIN_X0, 0.0, rail_z), collection, STRAKE_COLOR)
    side_len = STERN_CABIN_X1 - STERN_CABIN_X0
    side_x = (STERN_CABIN_X0 + STERN_CABIN_X1) * 0.5
    add_box("SternRail_Starboard", (side_len, 0.06, 0.05), (side_x, -(hy_fwd + hy_aft) * 0.5, rail_z), collection, STRAKE_COLOR)
    add_box("SternRail_Port", (side_len, 0.06, 0.05), (side_x, (hy_fwd + hy_aft) * 0.5, rail_z), collection, STRAKE_COLOR)


def build_stern(collection: bpy.types.Collection) -> None:
    hy_fwd, hy_aft = stern_half_widths()
    add_trapezoid_prism(
        "SternCabin",
        STERN_CABIN_X1,
        STERN_CABIN_X0,
        hy_fwd,
        hy_aft,
        DECK_Z,
        stern_roof_z(),
        collection,
        STERN_COLOR,
    )
    add_trapezoid_prism(
        "SternRoof",
        STERN_CABIN_X1,
        STERN_CABIN_X0,
        hy_fwd + 0.04,
        hy_aft + 0.04,
        stern_roof_z(),
        stern_roof_z() + 0.08,
        collection,
        DECK_COLOR,
    )
    build_open_rail(collection, hy_fwd, hy_aft)

    win_z = DECK_Z + 0.62
    mid_x = (STERN_CABIN_X0 + STERN_CABIN_X1) * 0.5
    for i, x in enumerate((mid_x + 0.55, mid_x - 0.55), start=1):
        hy = half_beam_at(x) * 0.99
        add_box(f"SternWindow_Port_{i:02d}", (0.28, 0.07, 0.22), (x, hy, win_z), collection, WINDOW_COLOR)
        add_box(f"SternWindow_Starboard_{i:02d}", (0.28, 0.07, 0.22), (x, -hy, win_z), collection, WINDOW_COLOR)
    add_box("SternWindow_Front_01", (0.07, 0.30, 0.22), (STERN_CABIN_X1, 0.0, win_z), collection, WINDOW_COLOR)


def build_stairs(collection: bpy.types.Collection) -> None:
    # In-hull starboard, forward of the cabin front wall. Never inside the solid cabin.
    step_count = 10
    step_l = 0.30
    step_h = (stern_roof_z() - DECK_Z) / step_count
    step_w = 0.70
    start_x = STERN_CABIN_X1 + 2.55
    for i in range(step_count):
        z = DECK_Z + step_h * (i + 0.5)
        x = start_x - i * 0.28
        add_box(f"SternStair_{i + 1:02d}", (step_l, step_w, step_h), (x, STAIR_Y, z), collection, DECK_COLOR)
    add_box(
        "CompanionwayLanding",
        (0.55, 0.78, 0.08),
        (STERN_CABIN_X1 + 0.18, STAIR_Y, stern_roof_z() + 0.06),
        collection,
        DECK_COLOR,
    )


def build_mast(collection: bpy.types.Collection) -> None:
    mast_z = DECK_Z + MAST_LENGTH_M * 0.5
    add_cylinder("Mast_Main", 0.16, MAST_LENGTH_M, (MAST_X, 0.0, mast_z), (0.0, 0.0, 0.0), collection, MAST_COLOR, 20)
    yard_z = DECK_Z + 12.2
    add_cylinder("Yard_Main", 0.20, 12.2, (MAST_X, 0.0, yard_z), (math.pi * 0.5, 0.0, 0.0), collection, STRAKE_COLOR, 16)
    nest_z = DECK_Z + 15.5
    add_cylinder("CrowsNest", 0.72, 0.18, (MAST_X, 0.0, nest_z), (0.0, 0.0, 0.0), collection, STRAKE_COLOR, 16)
    add_cylinder("CrowsNestRail", 0.74, 0.36, (MAST_X, 0.0, nest_z + 0.24), (0.0, 0.0, 0.0), collection, HATCH_COLOR, 16)


def build_bowsprit(collection: bpy.types.Collection) -> None:
    pitch = math.radians(18.0)
    length = 5.6
    start = Vector((7.10, 0.0, 2.00))
    direction = Vector((math.cos(pitch), 0.0, math.sin(pitch)))
    center = start + direction * (length * 0.5)
    add_cylinder(
        "Bowsprit",
        0.20,
        length,
        (center.x, center.y, center.z),
        (0.0, math.pi * 0.5 - pitch, 0.0),
        collection,
        MAST_COLOR,
        16,
    )
    add_box("BowspritStep", (1.20, 0.42, 0.36), (6.85, 0.0, 1.95), collection, STRAKE_COLOR)


def build_rudder(collection: bpy.types.Collection) -> None:
    stern_gunwale_z = deck_z_at(-7.40)
    rudder_top = stern_gunwale_z - 0.08
    rudder_h = 2.55
    add_box("Rudder", (0.28, 0.10, rudder_h), (-7.72, 0.0, rudder_top - rudder_h * 0.5), collection, RUDDER_COLOR)
    add_box("RudderStock", (0.12, 0.10, rudder_top - 0.15), (-7.48, 0.0, (rudder_top - 0.15) * 0.5), collection, RUDDER_COLOR)


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
        data.lens = 32.0
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
    # Starboard-bow 3/4 from above, depression 20°. See deck + hatch + stairs + keel silhouette.
    target = Vector((-1.70, -0.55, 2.55))
    margin = 1.24
    depress = math.radians(20.0)
    horiz = Vector((0.55, -1.18, 0.0)).normalized()
    persp_dir = Vector((horiz.x, horiz.y, math.tan(depress))).normalized()
    persp_dist = max(size.length * 1.34, 28.0)
    persp_loc = target + persp_dir * persp_dist
    persp = add_camera(
        CAMERA_NAMES["perspective"],
        persp_loc,
        target,
        collection,
        ortho=False,
        ortho_scale=1.0,
    )
    _log(f"persp camera loc={tuple(round(c, 2) for c in persp_loc)} target={tuple(round(c, 2) for c in target)} dist={persp_dist:.1f}")

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
    shading.studio_light = "outdoor.sl"
    shading.show_shadows = False
    shading.show_cavity = True
    shading.cavity_type = "BOTH"
    shading.curvature_ridge_factor = 1.0
    shading.curvature_valley_factor = 1.0
    shading.show_object_outline = True
    shading.object_outline_color = (0.10, 0.10, 0.10)
    if hasattr(shading, "background_type"):
        shading.background_type = "VIEWPORT"
    if hasattr(shading, "background_color"):
        shading.background_color = (0.93, 0.93, 0.93)
    if line_style:
        shading.color_type = "SINGLE"
        shading.single_color = (0.92, 0.91, 0.88)
    else:
        shading.color_type = "OBJECT"

    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene.world = world
    bg_color = (0.94, 0.94, 0.94, 1.0)
    tree = world.node_tree
    if tree is not None:
        for node in tree.nodes:
            if node.type == "BACKGROUND" and node.inputs:
                node.inputs[0].default_value = bg_color
                if len(node.inputs) > 1:
                    node.inputs[1].default_value = 1.6
    else:
        world.color = bg_color[:3]
    scene.view_settings.exposure = 0.35


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
    set_water_visible(False)
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
    cam_col = ensure_collection("COL_Cameras", root_col)

    root = bpy.data.objects.new(ASSET_ID, None)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 1.0
    root_col.objects.link(root)

    hull = build_hull(hull_col)
    bulwarks = build_bulwarks(hull_col)
    punch_gunports([hull, bulwarks], hull_col)
    build_strakes(hull_col)
    build_deck_and_hatch(deck_col)
    build_stern(stern_col)
    build_stairs(stern_col)
    build_mast(mast_col)
    build_bowsprit(mast_col)
    build_rudder(hull_col)

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
