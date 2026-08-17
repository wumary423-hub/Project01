# Ship Asset Contract — Program ↔ Art

Status: **V0.1.1 LOCKED for first-ship workflow**  
Authority order: **`.cursor/rules/ship-system.mdc` > `Docs/Ship/ShipAssetContract.md` > `Docs/Ship/SmallSailer01.md`**  
Program side is authoritative for sockets, naming, validation, import and catalog hookup.

## Scope

This contract defines the minimum 3D/2D asset interface required for the first workflow ship, working name **`SmallSailer01`**. The working asset name may differ from the final `ShipTypeId`; mapping is done at UE/catalog hookup.

Program V0.1.1 locks phase-one main-rig production to **Square + Lateen**, each with `Full / Half / Furled`. `Gaff` remains design-compatible but is not produced in phase one. `Attach_Headsail_01` is now part of the Hull interface; the starter/fallback ship is delivered with that slot empty.

## 1. Hull root

- One **Hull StaticMesh** per ship type.
- Hull is the scene mesh used by `AFleet` via the flagship catalog mesh.
- No `AShip` and no 3D crew actors.
- Source FBX does not need sockets; for v0.1.1 they are added in the **UE Static Mesh Editor**.

### Required float sockets — Error if missing

```text
Pontoon_Bow
Pontoon_Stern
Pontoon_Port
Pontoon_Starboard
```

Placement intent:

- Bow/Stern: centerline near design waterline.
- Port/Starboard: midships near design waterline.
- Rotation is not authoritative for float points.

### Hull attach sockets — Warning set for SmallSailer01

```text
Attach_MastRig_01
Attach_Figurehead
Attach_Rudder
Attach_Anchor
Attach_FX_Fire
Attach_Mast_Broken
Attach_Weapon_Port_01
Attach_Weapon_Starboard_01
Attach_Headsail_01
```

Optional:

```text
Attach_FX_Fire_Mast
```

Deprecated:

```text
Attach_Sail_Main
```

Not used on first ship:

```text
Attach_MastRig_02
Attach_MastRig_03
Attach_StaySail_*
Crew Socket of any kind
```

## 2. MastRig package — phase-one production

First ship uses **scheme A**: one whole StaticMesh per visual sail state, containing mast + yards/spars + sail + minimal major visual rigging.

Generic naming:

```text
SM_<ShipType>_MastRig01_<RigType>_Full
SM_<ShipType>_MastRig01_<RigType>_Half
SM_<ShipType>_MastRig01_<RigType>_Furled
```

For `SmallSailer01`, phase one produces **six** MastRig StaticMeshes:

```text
SM_SmallSailer01_MastRig01_Square_Full
SM_SmallSailer01_MastRig01_Square_Half
SM_SmallSailer01_MastRig01_Square_Furled

SM_SmallSailer01_MastRig01_Lateen_Full
SM_SmallSailer01_MastRig01_Lateen_Half
SM_SmallSailer01_MastRig01_Lateen_Furled
```

`MastRig01_TBD_*` is deprecated for production; it may exist only as an intermediate working/export name before final rename.

Rules:

- same pivot, transform and hang point within each RigType triplet;
- only one state visible at a time;
- changing RigType means swapping the entire active rig set, not changing only material or texture;
- upper sails / topsails do not create extra gameplay slots; they are part of the same MastRig package;
- `Fore` / `Main` / `Mizzen` are data roles, not socket-name variants;
- starter default main RigType (`Square` vs `Lateen`) remains a gameplay/catalog choice and does not block producing both sets;
- `Gaff` is design-compatible but **not phase-one production**.

## 3. Flag

`Attach_Flag` belongs to the **active MastRig StaticMesh**, not Hull.

Hierarchy:

```text
Hull
└─ Attach_MastRig_01
   └─ MastRig
      └─ Attach_Flag
         └─ Flag mesh
```

- Flag is an independent replaceable mesh.
- First ship has one flag position at the mast top.
- Every imported Square/Lateen Full/Half/Furled MastRig mesh used by the type should contain `Attach_Flag`.
- Mast down: hide normal MastRig and flag.

## 4. Headsail retrofit

`SmallSailer01` supports one optional bow Headsail/Jib retrofit through:

```text
Attach_Headsail_01
```

Rules:

- socket host: **Hull**;
- starter/fallback loadout: **no Headsail mesh equipped**;
- Headsail is independent of `MastRig_01`, so it can be installed/uninstalled without swapping the main-rig triplet;
- intended early-game pacing is roughly the first ~20 minutes, but availability/timing is gameplay/data logic, not an art contract;
- this slice is visual + refit-workflow testing only; no Headsail performance Modifier is required;
- when the asset is built, naming follows:

```text
SM_SmallSailer01_Headsail01_Full
SM_SmallSailer01_Headsail01_Half
SM_SmallSailer01_Headsail01_Furled
```

## 5. Modular parts

Separate FBX / StaticMesh, not welded into Hull:

- Figurehead → `Attach_Figurehead`
- Rudder → `Attach_Rudder`
- Anchor → `Attach_Anchor`
- Weapons → `Attach_Weapon_*`
- Headsail → `Attach_Headsail_01`
- Flag → MastRig `Attach_Flag`

First-ship weapon meshes are **not required**. The two weapon sockets are validated as warnings; a shared light-cannon mesh is added later when the cannon-refit slice opens.

Figurehead mount is on the bow/stem body, not at the bowsprit tip.

Anchor v0.1.1 is the stowed state only; no weigh/drop animation requirement.

## 6. Damage / fire

Presentation-only behavior:

- Mast down → hide normal MastRig + flag; show `MastBroken` at `Attach_Mast_Broken`.
- Fire → Niagara at `Attach_FX_Fire` / optional `Attach_FX_Fire_Mast`.
- Charred appearance → material/decal.
- Structural damage → dedicated damage mesh where needed.

Not required:

- live fracture physics;
- cloth simulation;
- fully simulated rigging.

## 7. Rigging

Rigging is visual only for ship assets.

- Keep only major support/control lines needed for silhouette and sail readability.
- Do not reproduce full historical rigging.
- Future boarding/swing ropes are separate gameplay assets and do not share this rigging system.

## 8. Cargo

Cargo capacity is numeric gameplay data.

- 3D may show an empty cargo-hold structure / hatch.
- Do not spawn or model cargo piles based on current inventory.
- Barrels, crates and sacks are not part of the required first-ship asset contract.

## 9. 2D outfit diagram

Required per ship type:

```text
T_<ShipType>_OutfitDiagram
```

First-ship target:

```text
T_SmallSailer01_OutfitDiagram
```

Rules:

- 2048×1024 master;
- transparent background;
- 8–10% safe margin;
- bow faces left;
- side view with slight top-side perspective;
- no baked UI hotspots;
- v0 slot positions are placed manually in `WBP_ShipOutfit`;
- art may supply reference normalized coordinates, but they are non-authoritative in v0.

3D and 2D must match on:

- mast count;
- deck levels;
- main rig silhouette / currently represented rig configuration;
- hull proportion;
- bow/stern identity;
- major spaces / major functional structures.

## 10. Blender / FBX handoff

- Keep proportional real-world scale in Blender; exact 15 m is not program-hard-validated.
- Apply Rotation and Scale before export.
- +X = ship forward.
- One asset per FBX for the first workflow.
- Sockets may be absent from FBX; add them in UE Static Mesh Editor.
- Validate checks the final UE StaticMesh, not Blender empties.

## 11. Validation severity

**Error**

- missing any of four Hull `Pontoon_*` sockets;
- missing required flagship hull path in catalog / `DT_Ships`.

**Warning**

- missing first-ship Hull attach sockets;
- missing `Attach_Weapon_Port_01` / `Attach_Weapon_Starboard_01`;
- missing `Attach_Headsail_01` on `SmallSailer01` Hull;
- missing `Attach_Flag` on any produced MastRig mesh used by the type.

## 12. First-ship phase-one working file checklist

```text
SM_SmallSailer01_Hull.fbx

SM_SmallSailer01_MastRig01_Square_Full.fbx
SM_SmallSailer01_MastRig01_Square_Half.fbx
SM_SmallSailer01_MastRig01_Square_Furled.fbx

SM_SmallSailer01_MastRig01_Lateen_Full.fbx
SM_SmallSailer01_MastRig01_Lateen_Half.fbx
SM_SmallSailer01_MastRig01_Lateen_Furled.fbx

SM_SmallSailer01_Flag_Placeholder.fbx
SM_SmallSailer01_Figurehead_Placeholder.fbx
SM_SmallSailer01_Rudder.fbx
SM_SmallSailer01_Anchor.fbx
SM_SmallSailer01_MastBroken.fbx
T_SmallSailer01_OutfitDiagram.png
```

Headsail retrofit asset when produced:

```text
SM_SmallSailer01_Headsail01_Full.fbx
SM_SmallSailer01_Headsail01_Half.fbx
SM_SmallSailer01_Headsail01_Furled.fbx
```

Later, when cannon-refit workflow is opened:

```text
SM_Weapon_LightCannon01.fbx
```

## 13. Explicitly not first-ship phase-one scope

- Crew sockets / 3D crew
- StaySail
- MastRig_02/03
- Gaff MastRig meshes
- dynamic cargo
- full historical rigging
- cloth simulation
- live mast fracture
- boarding ropes

Any future interface revision follows the authority order above and must be reflected in `Docs/Ship/CHANGELOG.md`.