# Ship Asset Contract — Program ↔ Art

Status: **V0.1 LOCKED for first-ship workflow**  
Authority: **program side is authoritative for sockets, naming, validation, import and catalog hookup.**  
Source of truth: `.cursor/rules/ship-system.mdc` on this branch.

## Scope

This contract defines the minimum 3D/2D asset interface required for the first workflow ship, working name **`SmallSailer01`**. The working asset name may differ from the final `ShipTypeId`; mapping is done at UE/catalog hookup.

`RigType` is the only remaining unlock in Stage 2.6.1. Until then all MastRig files use **`TBD`** in the filename triplet.

## 1. Hull root

- One **Hull StaticMesh** per ship type.
- Hull is the scene mesh used by `AFleet` via the flagship catalog mesh.
- No `AShip` and no 3D crew actors.
- Source FBX does not need sockets; for v0 they are added in the **UE Static Mesh Editor**.

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

### Hull attach sockets — Warning set for first ship

```text
Attach_MastRig_01
Attach_Figurehead
Attach_Rudder
Attach_Anchor
Attach_FX_Fire
Attach_Mast_Broken
Attach_Weapon_Port_01
Attach_Weapon_Starboard_01
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
Attach_Headsail_*
Crew Socket of any kind
```

## 2. MastRig package

First ship uses **scheme A**: one whole StaticMesh per visual sail state, containing mast + yards/spars + sail + minimal major visual rigging.

```text
SM_<ShipType>_MastRig01_<RigType>_Full
SM_<ShipType>_MastRig01_<RigType>_Half
SM_<ShipType>_MastRig01_<RigType>_Furled
```

For `SmallSailer01`, before Stage 2.6.1 is locked:

```text
SM_SmallSailer01_MastRig01_TBD_Full
SM_SmallSailer01_MastRig01_TBD_Half
SM_SmallSailer01_MastRig01_TBD_Furled
```

Rules:

- same pivot;
- same transform;
- same hang point;
- only one state visible at a time;
- changing RigType means swapping the entire three-mesh set, not changing only material or texture;
- top sails / upper sails do not create extra gameplay slots; they are part of the same MastRig package;
- `Fore` / `Main` / `Mizzen` are data roles, not socket-name variants.

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
- Each imported Full/Half/Furled MastRig mesh used by the type should contain `Attach_Flag`.
- Mast down: hide normal MastRig and flag.

## 4. Modular parts

Separate FBX / StaticMesh, not welded into Hull:

- Figurehead → `Attach_Figurehead`
- Rudder → `Attach_Rudder`
- Anchor → `Attach_Anchor`
- Weapons → `Attach_Weapon_*`
- Flag → MastRig `Attach_Flag`

First-ship weapon meshes are **not required**. The two weapon sockets are validated as warnings; a shared light-cannon mesh is added later when the cannon-refit slice opens.

Figurehead mount is on the bow/stem body, not at the bowsprit tip.

Anchor v0 is the stowed state only; no weigh/drop animation requirement.

## 5. Damage / fire

Presentation-only v0 behavior:

- Mast down → hide normal MastRig + flag; show `MastBroken` at `Attach_Mast_Broken`.
- Fire → Niagara at `Attach_FX_Fire` / optional `Attach_FX_Fire_Mast`.
- Charred appearance → material/decal.
- Structural damage → dedicated damage mesh where needed.

Not required v0:

- live fracture physics;
- cloth simulation;
- fully simulated rigging.

## 6. Rigging

Rigging is visual only for ship assets.

- Keep only major support/control lines needed for silhouette and sail readability.
- Do not reproduce full historical rigging.
- Future boarding/swing ropes are separate gameplay assets and do not share this rigging system.

## 7. Cargo

Cargo capacity is numeric gameplay data.

- 3D may show an empty cargo-hold structure / hatch.
- Do not spawn or model cargo piles based on current inventory.
- Barrels, crates and sacks are not part of the required first-ship asset contract.

## 8. 2D outfit diagram

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
- main rig silhouette;
- hull proportion;
- bow/stern identity;
- major spaces / major functional structures.

## 9. Blender / FBX v0 handoff

- Keep proportional real-world scale in Blender; exact 15 m is not program-hard-validated.
- Apply Rotation and Scale before export.
- +X = ship forward.
- One asset per FBX for the first workflow.
- Sockets may be absent from FBX; add them in UE Static Mesh Editor.
- Validate checks the final UE StaticMesh, not Blender empties.

## 10. Validation severity

**Error**

- missing any of four Hull `Pontoon_*` sockets;
- missing required flagship hull path in catalog / `DT_Ships`.

**Warning**

- missing first-ship Hull attach sockets;
- missing `Attach_Weapon_Port_01` / `Attach_Weapon_Starboard_01`;
- missing `Attach_Flag` on a MastRig triplet used by the type.

## 11. First-ship working file checklist

```text
SM_SmallSailer01_Hull.fbx
SM_SmallSailer01_MastRig01_TBD_Full.fbx
SM_SmallSailer01_MastRig01_TBD_Half.fbx
SM_SmallSailer01_MastRig01_TBD_Furled.fbx
SM_SmallSailer01_Flag_Placeholder.fbx
SM_SmallSailer01_Figurehead_Placeholder.fbx
SM_SmallSailer01_Rudder.fbx
SM_SmallSailer01_Anchor.fbx
SM_SmallSailer01_MastBroken.fbx
T_SmallSailer01_OutfitDiagram.png
```

Later, when cannon-refit workflow is opened:

```text
SM_Weapon_LightCannon01.fbx
```

## 12. Explicitly not first-ship scope

- Crew sockets / 3D crew
- StaySail
- Headsail
- MastRig_02/03
- dynamic cargo
- full historical rigging
- cloth simulation
- live mast fracture
- boarding ropes

Any interface change after first UE hookup should be proposed as **V0.2**, not silently diverge from this contract.
