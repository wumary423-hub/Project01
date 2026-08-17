# Ship Asset / Pipeline Changelog

This log tracks design-contract changes between program and art/resource workflows.

## 2026-08-17 — Stage 2.6.1 rig plan update

### Main-rig production decision

- `SmallSailer01` hull design is intended to support `Square`, `Lateen`, and later `Gaff` main RigTypes.
- **Phase-one resource production will build both `Square` and `Lateen` MastRig triplets** so the first workflow can test main-rig refit as well as Full/Half/Furled state switching.
- Each RigType is a complete MastRig package set, not a material-only variation.
- `Gaff` remains a supported future RigType but is not required in the first production batch.
- Exact starter/fallback default main RigType (Square vs Lateen) remains a gameplay/catalog choice after both asset variants exist.

### Headsail design decision — pending program interface update

- Design side approves **one optional Headsail/Jib retrofit** for `SmallSailer01`.
- The free starter/fallback configuration should ship **without** the Headsail installed.
- Intended pacing: Headsail can become available as an early upgrade after roughly the first ~20 minutes of play.
- This is intended to test a visible auxiliary-sail refit path.
- **Program V0.1 currently excludes Headsail from the first ship.** Therefore `Attach_Headsail_01` and Headsail asset naming/validation are not part of the authoritative contract until `.cursor/rules/ship-system.mdc` is explicitly updated by program authority.
- Art/design documentation may describe the proposed retrofit, but resource delivery must not silently diverge from the locked program contract.

### Historical/world framing

- The English Channel is a current development/testing context, not a mandatory game-start location.
- The fictional-world design intentionally permits gameplay-driven rig availability rather than enforcing strict historical/regional chronology.

## 2026-08-17 — V0.1 first-ship contract established

### Program authority

- `.cursor/rules/ship-system.mdc` is the authoritative source for sockets, naming, validation, import behavior and catalog hookup.
- Resource/art side follows program-defined interfaces for the first workflow ship.
- Interface changes after first UE hookup should be proposed as **V0.2**, not silently diverge.

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

### RigType status

- Original V0.1 contract left Stage 2.6.1 unresolved and used `TBD` filenames.
- Candidate types were `Square`, `Lateen`, `Gaff`.
- Program contract remains authoritative for current file/catalog naming until it is updated to reflect the Stage 2.6.1 production decision.
- First-ship contract originally excluded StaySail, Headsail, MastRig_02 and MastRig_03.

### Modular parts

- Figurehead, Rudder, Anchor and Flag are separate meshes.
- Figurehead attaches at bow/stem body, not bowsprit tip.
- Weapon sockets are included; weapon mesh is optional for v0.1 and deferred until cannon-refit flow.
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

### Next milestone

- Program side to decide how/when to update the V0.1 contract for the dual `Square` + `Lateen` production set.
- Program side to approve or defer the proposed `Attach_Headsail_01` retrofit interface.
- Proceed to Stage 2.7 final Concept Design once the rig-production naming/interface delta is synchronized.
