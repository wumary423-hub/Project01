# SmallSailer01 — Canonical Ship Design

Status: **Stage 2.6.1 locked for phase-one production; program contract V0.1.1 synchronized**  
Working name: **`SmallSailer01`**  
Catalog mapping: final `ShipTypeId` to be assigned at UE hookup.

Authority order:

> `.cursor/rules/ship-system.mdc` > `Docs/Ship/ShipAssetContract.md` > `Docs/Ship/SmallSailer01.md`

This document is the art/design source for the first workflow ship. Program interfaces follow `.cursor/rules/ship-system.mdc`; shared delivery details follow `Docs/Ship/ShipAssetContract.md`.

## 1. Gameplay role

`SmallSailer01` is the game's lowest-tier formal sea-going vessel and the player fallback/starter ship.

Intended uses:

- starter / recovery vessel after total fleet loss;
- coastal trade;
- exploration;
- small-scale transport;
- symbolic/light self-defense armament;
- capable of a Channel-crossing scale voyage rather than being merely a harbor boat.

Design character:

> small, inexpensive, plain, reliable and balanced — not a wreck and not a specialized high-performance craft.

Future derivative variants may emphasize cargo, speed/exploration or armament; the base model remains deliberately balanced.

The current development context often uses the English Channel as a practical design/testing environment, but the game is not required to start there and the world is not a strict historical reconstruction. Rig availability is therefore allowed to prioritize gameplay and readable ship differentiation over strict regional chronology.

## 2. Historical / visual language

Broad reference language:

- Shallop-like and early-modern small coastal sailing craft;
- small coastal trader characteristics;
- 15th–17th century visual language, adapted for a fictional world rather than strict reconstruction.

Do not lock the vessel to a named historical type such as Cog unless later design work explicitly does so.

## 3. Reference dimensions

Concept-only targets — not program-hard-validated:

| Parameter | Target |
|---|---:|
| Length overall | ~15 m (roughly 14–16 m acceptable while refining) |
| Beam | ~4.2–4.6 m |
| Draft | ~1.6–2.0 m |
| Reference tonnage | ~25–35 ton class |
| Mast count | **1** |
| Main deck levels | **1** |

The vessel must visually read as a true small sea-going ship with meaningful underwater hull volume and limited cargo capacity, not as an enlarged lifeboat.

## 4. Strategic-view design priority

Typical gameplay view is approximately **50–200 m**. Around **10 m** is an unusually close observation distance.

Design priority:

> **mast count > deck levels > rig silhouette > hull outline > major functional parts > small decoration**

Use 50–200 m to decide **what deserves to exist**. Use 10–30 m to ensure the asset does not look obviously crude, broken or incorrectly proportioned.

## 5. Locked identity features

Primary visual identity:

- one mast;
- one main deck;
- one dominant MastRig package;
- full but not excessively bulky hull amidships;
- clearly visible underwater hull volume / draft;
- moderately raised bow;
- slightly raised stern, but **not** a complete second deck or large sterncastle;
- restrained armament;
- uncluttered silhouette.

These features must remain recognizable in both the 3D asset and the 2D outfit diagram.

## 6. Hull and deck layout

Recommended spatial logic:

```text
Bow / work area
→ mast + central structure
→ cargo-hold area
→ aft steering / command area
```

### Bow

- clean, restrained structure;
- figurehead mount at bow/stem body;
- one stowed anchor;
- one program-approved optional Headsail retrofit position at the bow;
- no over-detailed decorative clutter.

### Mast

- located approximately amidships, slightly forward of visual center;
- mast is structurally understood as continuing down into the hull toward the mast step / keel-support region;
- do not visually treat the mast as merely glued to the deck.

### Cargo hold

- one clear main cargo-hatch structure behind / near the main mast;
- the hold may be represented empty;
- no visual need to show actual inventory quantity or cargo type.

### Stern

- slightly raised steering/command area;
- remains part of the single-deck identity;
- no full formal captain's cabin required for the first workflow ship;
- steering language uses a **tiller**, not a large wheel.

## 7. Armament

Intended maximum visual capacity:

- up to two light weapon positions, one port and one starboard;
- weapons are secondary visual elements, not silhouette-defining features;
- barrels should extend only modestly outside the hull;
- first workflow requires weapon sockets, not a weapon mesh.

## 8. Rigging system — visual intent

The ship asset's standing/running rigging is **visual only**.

- retain only major support lines and a small number of visually meaningful control lines;
- do not reproduce a complete historical rigging plan;
- do not spend modeling time on tiny knots, numerous blocks or dense rope networks;
- future boarding/swing ropes are a separate gameplay asset family.

## 9. Sail-slot and RigType design — Stage 2.6.1 LOCKED

### 9.1 Slot model

Current main slot:

```text
MastRig_01
```

General ship-system design separates **slot position** from **sail/rig type**:

- each mast may own one `MastRig_XX` slot;
- logical mast roles (`Fore`, `Main`, `Mizzen`) are data roles, not separate socket families;
- a mizzen is still a MastRig slot, not an independent fourth slot category;
- upper sails / topsails do not create separate gameplay slots; they are part of the same MastRig package;
- future `StaySail_*` slots live between masts;
- `Headsail_*` slots live in the bow/bowsprit region.

### 9.2 RigTypes supported by the hull design

`SmallSailer01` is designed to be compatible with:

```text
Square
Lateen
Gaff
```

These are alternate main-rig configurations for the same `MastRig_01` position. Changing RigType changes the full visible rig package, not merely a texture or numeric stat.

### 9.3 Phase-one resource production — LOCKED

Phase one produces both:

```text
Square
Lateen
```

Each requires its own complete Full / Half / Furled triplet so the first workflow can test **main-rig refit / MastRig replacement** as well as state switching.

Production names:

```text
SM_SmallSailer01_MastRig01_Square_Full
SM_SmallSailer01_MastRig01_Square_Half
SM_SmallSailer01_MastRig01_Square_Furled

SM_SmallSailer01_MastRig01_Lateen_Full
SM_SmallSailer01_MastRig01_Lateen_Half
SM_SmallSailer01_MastRig01_Lateen_Furled
```

`MastRig01_TBD_*` is no longer the production naming rule; it may appear only on intermediate work before final rename.

`Gaff` remains compatible with the hull/design system but is **not produced in phase one**.

### 9.4 Starter configuration

The fallback/starter ship does not expose every supported sail option at game start.

- exact starter main RigType (`Square` vs `Lateen`) remains a gameplay/catalog choice after both resource variants exist;
- starter/fallback configuration has **no Headsail mesh equipped**;
- supported but unequipped does not mean unsupported by the hull.

### 9.5 Headsail retrofit — PROGRAM APPROVED V0.1.1

`SmallSailer01` supports one optional Headsail/Jib retrofit through:

```text
Attach_Headsail_01
```

Design and program rules:

- `Attach_Headsail_01` lives on the Hull;
- starter/fallback configuration has no Headsail child mesh;
- intended gameplay pacing is an early visible upgrade, roughly around the first ~20 minutes of play;
- Headsail remains independent of `MastRig_01`, so installing/removing it does not require replacing the main-rig package;
- this slice tests visual/refit workflow only; no Headsail performance Modifier is required yet;
- resource side handles mesh, pivot and visual states; availability/unlock/data logic belongs to program/gameplay.

When produced, use:

```text
SM_SmallSailer01_Headsail01_Full
SM_SmallSailer01_Headsail01_Half
SM_SmallSailer01_Headsail01_Furled
```

### 9.6 Sail-state presentation

Every produced main MastRig variant uses three complete visual states:

```text
Full
Half
Furled
```

Each state is a whole MastRig package containing mast + main spars/yards + sail + minimal major rigging, with identical pivot / hang transform within that RigType triplet.

## 10. Flag

- first ship has **one** flag position;
- position is at the mast top;
- flag is a separate replaceable mesh;
- `Attach_Flag` lives on every produced active MastRig state mesh;
- mast down → hide flag.

Flag artwork itself may remain a placeholder during the first workflow.

## 11. Figurehead

- figurehead is a separate replaceable mesh;
- mount belongs on the bow/stem body, not the bowsprit tip;
- first workflow uses a simple placeholder;
- later formal figureheads may be high-value collectible/treasure items with:
  - a refined 2D item icon;
  - a matching 3D figurehead mesh preserving the same major silhouette and material identity.

Formal figureheads therefore deserve stronger silhouette and material work than ordinary micro-decoration, while still avoiding wasteful tiny geometry.

## 12. Damage / fire visual intent

First workflow should support:

- broken/down mast via separate `MastBroken` mesh;
- normal MastRig hidden when broken state is active;
- flag hidden with mast failure;
- fire via Niagara attachment points;
- charred look via material/decal;
- no real-time mast fracture or cloth simulation required.

## 13. Geometry detail budget

### Must be real geometry

- hull silhouette and underwater volume;
- deck-level changes;
- mast and main spars/yards;
- sail silhouette;
- cargo hatch major form;
- rudder and tiller;
- anchor;
- figurehead placeholder;
- flag mesh;
- broken mast;
- major railings where they materially affect silhouette;
- a small number of major ropes.

### Simplified geometry

- rail posts / rails;
- cargo-hatch framing;
- anchor details;
- gun carriage when weapons are eventually added;
- large structural trim where visible from game camera.

### Normal Map

- hull plank seams;
- deck plank seams;
- moderate joinery relief;
- sail fabric folds / stitching that do not define the overall sail shape.

### Base Color / Roughness / related material channels

- wood grain;
- wood color variation;
- waterline staining / salt / dirt;
- canvas aging and discoloration;
- metal oxidation / wear.

### Delete / do not model for first workflow

- individual nails / rivets;
- small knots;
- dense historical block-and-tackle detail;
- tiny chains;
- miniature carvings;
- interior furniture;
- invisible complete historical framing structure;
- dynamic barrels/crates/sacks tied to cargo inventory;
- crew belongings / deck clutter.

Rule of thumb:

> If it does not affect silhouette, is not readable at normal range, and has no gameplay function, do not model it.

## 14. 2D outfit diagram

Required companion asset:

```text
T_SmallSailer01_OutfitDiagram
```

Art rules:

- 2048×1024 master;
- transparent background;
- 8–10% safe margin;
- bow faces left;
- side view as the main read, with slight top-side perspective;
- no baked UI hotspots;
- WBP places slot widgets manually in v0.

The diagram is not a top view and is not a UV layout.

It must preserve the same ship identity as the 3D asset, especially:

- one mast;
- one deck level;
- the represented main RigType silhouette;
- hull proportion and fullness;
- bow and stern character;
- cargo-hold / major-space logic.

The starter diagram/loadout may omit the optional Headsail even though the hull supports the retrofit.

## 15. First-workflow success criteria

The first ship is successful when the complete pipeline is proven:

```text
Concept Design
→ multi-view modeling reference
→ 3D Mesh generation/modeling
→ Blender cleanup and asset split
→ UV
→ PBR material
→ Square MastRig Full/Half/Furled
→ Lateen MastRig Full/Half/Furled
→ main-rig refit test
→ modular attachments
→ Headsail retrofit interface / asset test
→ damage presentation
→ LOD / Collision / Pivot / Scale
→ FBX
→ UE5 StaticMesh import
→ socket setup / Validate
→ strategic-view test
→ matching 2D outfit diagram
```

The goal is not cinematic fidelity. The goal is a reusable, game-ready ship-production workflow for later Caravel, merchant and combat ships.