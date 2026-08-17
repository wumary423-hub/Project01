# Ship Asset / Pipeline Changelog

This log tracks design-contract changes between program and art/resource workflows.

## 2026-08-17 — V0.1.1 program contract synchronized

### Authority order locked

- `.cursor/rules/ship-system.mdc` > `Docs/Ship/ShipAssetContract.md` > `Docs/Ship/SmallSailer01.md`.
- Program rules remain authoritative for sockets, naming, validation, import and catalog behavior.
- Shared/documentation layers were updated to match program V0.1.1 rather than preserve superseded V0.1 wording.

### Main-rig production now locked

- `SmallSailer01` phase-one production builds **Square + Lateen**.
- Each RigType has a complete `Full / Half / Furled` MastRig triplet.
- Total phase-one MastRig set: **6 StaticMeshes**.
- `MastRig01_TBD_*` is no longer the production naming rule; it may exist only as an intermediate working/export name before final rename.
- `Gaff` remains design/hull-compatible but is **not produced in phase one**.
- Starter default main RigType (`Square` vs `Lateen`) remains a gameplay/catalog decision after both sets exist.

### Headsail retrofit approved by program

- `Attach_Headsail_01` is now part of the `SmallSailer01` Hull contract and is a Validate warning if missing.
- Starter/fallback ship is delivered with the Headsail slot **empty / no child mesh equipped**.
- Headsail is independent of `MastRig_01` and can be installed/removed separately.
- Intended pacing remains an early visible refit around roughly the first ~20 minutes of play.
- This slice tests the visual/refit workflow only; no Headsail performance Modifier is required yet.
- Headsail asset naming when produced:
  - `SM_SmallSailer01_Headsail01_Full`
  - `SM_SmallSailer01_Headsail01_Half`
  - `SM_SmallSailer01_Headsail01_Furled`

### Docs synchronized

- `Docs/Ship/ShipAssetContract.md` updated from V0.1 to **V0.1.1**.
- `Docs/Ship/SmallSailer01.md` no longer marks Headsail as pending; it is **program approved**.
- Superseded statements saying “first ship does not build Headsail” or “RigType still TBD for production” were removed from current design/contract state.

### Program tooling noted

Program side reports the following tools are now part of the V0.1.1 workflow:

- `Tools/ValidateShipMeshes.py`
- `Tools/ImportSmallSailer01Meshes.py`
- `Tools/CreateShipsDataTable.py`

### Next milestone

- Proceed to **Stage 2.7 final Concept Design** for `SmallSailer01`.
- Final concept must directly support production of both Square and Lateen MastRig variants and preserve the optional Headsail retrofit position.

## 2026-08-17 — Stage 2.6.1 rig plan update

### Main-rig production decision

- `SmallSailer01` hull design is intended to support `Square`, `Lateen`, and later `Gaff` main RigTypes.
- **Phase-one resource production will build both `Square` and `Lateen` MastRig triplets** so the first workflow can test main-rig refit as well as Full/Half/Furled state switching.
- Each RigType is a complete MastRig package set, not a material-only variation.
- `Gaff` remains a supported future RigType but is not required in the first production batch.
- Exact starter/fallback default main RigType (Square vs Lateen) remains a gameplay/catalog choice after both asset variants exist.

### Headsail design decision — superseded by V0.1.1 approval above

- Design side approved one optional Headsail/Jib retrofit for `SmallSailer01`.
- The free starter/fallback configuration should ship without the Headsail installed.
- Intended pacing: Headsail can become available as an early upgrade after roughly the first ~20 minutes of play.
- This proposal was subsequently accepted by program V0.1.1; current authoritative state is recorded above.

### Historical/world framing

- The English Channel is a current development/testing context, not a mandatory game-start location.
- The fictional-world design intentionally permits gameplay-driven rig availability rather than enforcing strict historical/regional chronology.

## 2026-08-17 — V0.1 first-ship contract established

### Program authority

- `.cursor/rules/ship-system.mdc` is the authoritative source for sockets, naming, validation, import behavior and catalog hookup.
- Resource/art side follows program-defined interfaces for the first workflow ship.

### First workflow ship

- Working name: `SmallSailer01`.
- Final `ShipTypeId` mapping deferred until UE/catalog hookup.
- Concept target: ~15 m single-mast, single-main-deck, balanced small sea-going trader / fallback ship.
- Reference tonnage: ~25–35 ton class, concept only.
- Typical strategic camera: ~50–200 m; ~10 m is unusually close.

### 3D / 2D split

- Every ship type requires both a 3D ship asset set and a matching 2D outfit diagram.
- No 3D crew actors or Crew sockets.
- 2D outfit diagram: bow left, side view with slight top-side perspective, 2048×1024 transparent master, no baked hotspots.

### Hull / socket contract

- Hull StaticMesh is the `AFleet` root visual mesh.
- Required float sockets:
  - `Pontoon_Bow`
  - `Pontoon_Stern`
  - `Pontoon_Port`
  - `Pontoon_Starboard`
- `Attach_Sail_Main` deprecated.
- First-ship mast attachment renamed/locked to `Attach_MastRig_01`.
- Hull attachment set includes Figurehead, Rudder, Anchor, Fire FX, Broken Mast, and two weapon sockets.
- First workflow authors sockets in UE Static Mesh Editor; Validate checks final UE StaticMeshes.

### MastRig package

- Scheme A locked for first ship: whole-package StaticMesh triplet (`Full` / `Half` / `Furled`).
- Package includes mast + main yards/spars + sail + minimal major visual rigging.
- All three states share pivot / transform / hang point.
- Rig change swaps the complete triplet; it is not material-only.
- `Attach_Flag` is hosted on each active MastRig StaticMesh, not Hull.
- First ship has one mast-top flag position.

### RigType status at V0.1

- Original V0.1 contract left Stage 2.6.1 unresolved and used `TBD` filenames.
- Candidate types were `Square`, `Lateen`, `Gaff`.
- This state was superseded by V0.1.1.

### Modular parts

- Figurehead, Rudder, Anchor and Flag are separate meshes.
- Figurehead attaches at bow/stem body, not bowsprit tip.
- Weapon sockets are included; weapon mesh is optional and deferred until cannon-refit flow.
- Cargo is numeric gameplay data; no dynamic cargo piles are required in 3D.
- Rigging is simplified visual rigging only and is separate from future boarding/swing rope gameplay assets.

### Damage / fire

- Mast failure uses hide normal MastRig + flag, then show `MastBroken`.
- Fire uses Niagara attachment points.
- Charred appearance uses material/decal.
- No live fracture physics or cloth simulation in v0.

### Documentation created

- `Docs/Ship/ShipAssetContract.md`
- `Docs/Ship/SmallSailer01.md`
- `Docs/Ship/CHANGELOG.md`
