# SmallSailer01 — Canonical Ship Design

Status: **Stage 2.6.1 main-rig selection substantially locked; Headsail retrofit pending program-interface approval**  
Working name: **`SmallSailer01`**  
Catalog mapping: final `ShipTypeId` to be assigned at UE hookup.

This document is the art/design source for the first workflow ship. Program interfaces are governed by `.cursor/rules/ship-system.mdc` and `Docs/Ship/ShipAssetContract.md`. Where this design proposes an interface not yet accepted by program, it is explicitly marked **pending program approval** and must not silently override the locked contract.

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

## 9. Sail-slot and RigType design — Stage 2.6.1

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
- future `Headsail_*` slots live in the bow/bowsprit region.

### 9.2 RigTypes supported by the hull design

`SmallSailer01` is designed to be compatible with:

```text
Square
Lateen
Gaff
```

These are alternate main-rig configurations for the same `MastRig_01` position. Changing RigType changes the full visible rig package, not merely a texture or numeric stat.

### 9.3 Phase-one resource production

**Phase one will produce both:**

```text
Square
Lateen
```

Each requires its own complete Full / Half / Furled triplet so the first workflow can test **sail refit / MastRig replacement** as well as state switching.

Planned naming after program/catalog paths are updated:

```text
SM_SmallSailer01_MastRig01_Square_Full
SM_SmallSailer01_MastRig01_Square_Half
SM_SmallSailer01_MastRig01_Square_Furled

SM_SmallSailer01_MastRig01_Lateen_Full
SM_SmallSailer01_MastRig01_Lateen_Half
SM_SmallSailer01_MastRig01_Lateen_Furled
```

Until the program-side V0.1 `TBD` naming/catalog rule is explicitly updated, resource working/export files may continue using the contract-approved `TBD` placeholder during intermediate production. Do not silently break the program contract.

`Gaff` remains a supported future RigType but is **not required in the first production batch**.

### 9.4 Starter configuration

The fallback/starter ship is **not required to expose every supported rig or auxiliary sail at game start**. Availability/unlock is gameplay configuration, not a hull-geometry limitation.

The exact default starter main RigType (Square vs Lateen) may be selected in gameplay/catalog configuration after both resource variants exist; it does not block production of either rig set.

### 9.5 Headsail retrofit — design-approved, program interface pending

Design decision:

- `SmallSailer01` may support **one optional Headsail/Jib retrofit**;
- the free starter/fallback configuration does **not** have the Headsail installed;
- intended gameplay pacing: player may gain/install the Headsail after roughly the first ~20 minutes of play;
- this gives the first ship an early, visible upgrade and allows testing the sail-refit workflow beyond swapping the main MastRig.

**Important:** current program V0.1 contract explicitly excludes Headsail on the first ship. Therefore the following remains a **proposal pending program-side approval/rule update**:

```text
Attach_Headsail_01
Headsail_01 visual asset/state set
```

Do not add this socket to the authoritative delivery/Validate list until `.cursor/rules/ship-system.mdc` is updated by the program side.

Recommended resource behavior if/when approved:

- one bow Headsail slot;
- Jib-style triangular auxiliary sail;
- independent of `MastRig_01` so it can be absent on the starter configuration and installed later;
- resource side handles Mesh / pivot / visual state only;
- gameplay performance modifiers, availability and unlock timing are program/data concerns.

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
- `Attach_Flag` lives on each active MastRig state mesh;
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
- currently equipped main RigType silhouette where the UI design chooses to reflect loadout;
- hull proportion and fullness;
- bow and stern character;
- cargo-hold / major-space logic.

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
→ optional Headsail retrofit after program interface approval
→ damage presentation
→ LOD / Collision / Pivot / Scale
→ FBX
→ UE5 StaticMesh import
→ socket setup / Validate
→ strategic-view test
→ matching 2D outfit diagram
```

The goal is not cinematic fidelity. The goal is a reusable, game-ready ship-production workflow for later Caravel, merchant and combat ships.
