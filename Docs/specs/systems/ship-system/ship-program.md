---
document_type: system_program_spec
schema_version: 1
system_id: SYS-SHIP
title_zh: 船只系统 — 程序运行时
document_version: 0.5.0
status: LOCKED
source: .cursor/rules/ship-system.mdc V0.1.1
last_updated: 2026-09-09
decision_record: docs/specs/systems/ship-system/decisions/ADR-0002-cabin-stations-and-type-groups.md
---

# 船只系统程序规范

迁自 `.cursor/rules/ship-system.mdc` 的运行时条款。3D/2D 资产接口见 `ship-system.md` 与 `ShipType_SmallSailer01/integration.yaml`。命名见 `docs/governance/naming-and-versioning.md`。

0.3.0 目录与装配合同见 **ADR-0001**。0.5.0 舱室空槽跟船体走，见 **ADR-0002**（系统规范 0.4.0 是组件优先制作，勿混）。

## 1. 角色

- 船 = `UShipObject`（`UShipManagerSubsystem`）。
- 海上存在单位永远是 Fleet。**无 `AShip`**。单船编队仍显示为舰队。
- `AFleet` 根网格 = 旗舰 **Hull**（`DT_ShipHulls.Mesh`）。旗舰记在舰队 `FlagshipShipId`，不在船上做第二真相。
- 桅与 YardSail 由**船系统**按目录 + 实例安装组装到旗舰上；`AFleet` / `BP_Fleet` **不手摆**桅帆，只读组装结果。

## 2. 架构

| 件 | 路径 / 类型 |
|----|-------------|
| Object | `UShipObject` — `Source/.../Ship/` |
| Manager | `UShipManagerSubsystem` |
| Settings | `UShipManagerSettings` |
| Types | `ShipTypes.h`（实例 `Ship_<N>`；占位类型 `ShipType_TempCog` / `TempCaravel` / `TempCarrack`；第一艘正式类型 `ShipType_SmallSailer01`） |
| Catalog | 六表，均在 `/Game/Ship/`：`DT_Ships` + `DT_ShipHulls` + `DT_ShipMasts` + `DT_ShipYardSails` + `DT_CabinTypes` + `DT_CabinTypeGroups` |
| 船网格 | `/Game/Ships/ShipType_SmallSailer01/` |
| Tools | `Tools/CreateShipsDataTable.py`（总表）；`Tools/CreateShipArtDataTables.py`（船体/桅/帆）；`Tools/CreateCabinDataTables.py`（舱室类型/组空表，不覆盖已填行）；`Tools/ImportSmallSailer01Meshes.py`；`Tools/ValidateShipMeshes.py` |
| UI | `UCityPortWidget` + `UFleetManagementWidget` + `UShipOutfitWidget` |
| Save | `FShipSaveData`（`SaveTypes.h`；schema **v8**。`InstalledCabins` 空 = 未改装空槽；旧 v8 体读入为空数组） |

## 3. Id

- 实例：`Ship_<序号>`。舰队：`Fleet_<序号>`。禁止 `Fleet_Player_*` 当 Id。
- 船种：`ShipType_<Name>`。船体种：`ShipHull_<Name>`。桅种：`ShipMast_<Name>`。桁帆种：`ShipYardSail_<Name>`。舱室类型：`CabinType_<Name>`。舱室类型组：`CabinTypeGroup_<Name>`。船体空槽：`CabinStation_<Name>`（在该 Hull 上唯一）。
- 指挥：`PlayerCommandedFleetId`。
- 公司所有：`OwnerCompanyId == Company_Player`。无公司：`OwnerCharacterId` = 玩家角色。
- 公司保留 Id：`Company_Player`。

## 4. 实例字段

| 字段 | 锁定 |
|------|------|
| `ShipId` / `ShipTypeId` / `DisplayName` | 序列 Id；目录类型；占位显示名 |
| `OwnerCompanyId` / `OwnerCharacterId` | 公司 / 无公司玩家；皆空 = 待售（later） |
| `FleetId` | 空 = 未编队 |
| `HostCityId` | 未编队 → 该城港口。`Berth` 不在 v0 |
| `InstalledMasts` | 可选。每项：`StationSocket` + `MastTypeId`。缺项或 `None` = 该位 `AllowedMastTypeIds[0]` |
| `InstalledYardSails` | 过渡/美术。无对应舱室帆槽时：缺项或 `None` = 该位 `AllowedYardSailIds[0]` |
| `InstalledCabins` | 每项：`StationId` + `CabinTypeId`。缺项或 `None` = 该空槽未改装。**CreateShip 会按该槽组的 `CabinTypeIds[0]` 写一次默认** |

实例**不**存速度、强度、网格路径。Fleet **不**存桅/帆/舱室安装。

占位行：`ShipType_TempCog` / `TempCaravel` / `TempCarrack`。缺总表则内置 Cog。改船体/桅帆/舱室组改 DataTable，不改 C++。

### 4.1 目录四表

查找键一律是类型 Id，**禁止**用 mesh 软路径当主键或配置键。

| 表 | 行键 | 行结构（实现名） | 内容 |
|----|------|------------------|------|
| `/Game/Ship/DT_Ships` | `ShipTypeId` | `FShipDefinition` | `DisplayName`、`BaseSpeed`、`BaseStrength`、**`HullId`**。**不再**挂 `Mesh` |
| `/Game/Ship/DT_ShipHulls` | `HullId` | `FShipHullDefinition` | Hull 网格；`MastStations[]`；**`CabinStations[]`**（空槽：`StationId` + `LayoutPos` + 可选 `BindSocket` + **一个** `CabinTypeGroupId`） |
| `/Game/Ship/DT_ShipMasts` | `MastTypeId` | `FShipMastDefinition` | 桅网格、高度；`YardStations[]`：`SocketName` + `AllowedYardSailIds[]`（美术能接住哪些网格，**不是**玩法菜单） |
| `/Game/Ship/DT_ShipYardSails` | `YardSailId` | `FShipYardSailDefinition` | 帆+桁**一件**（`USkeletalMesh` 优先，或 `UStaticMesh`）；帆种；尺寸 |
| `/Game/Ship/DT_CabinTypes` | `CabinTypeId` | `FCabinTypeDefinition` | 显示名；`OfferedPostIds[]`；`AllowedEquipmentIds[]`（内容由玩法填） |
| `/Game/Ship/DT_CabinTypeGroups` | `CabinTypeGroupId` | `FCabinTypeGroupDefinition` | `CabinTypeIds[]`。组数量与内容由玩法确定 |

占位 Cog / Caravel / Carrack：各有 `ShipHull_Temp*` 行，桅位与舱室槽可空（只画 Hull）。

`ShipType_SmallSailer01` → `HullId` = `ShipHull_SmallSailer01`。主桅行 `ShipMast_SmallSailer01_Main`（高 18m）。默认 YardSail 在 Square vs Lateen 未定时保持 **UNSET**（表行可先空或只登记资源、不指定 `[0]` 为玩法默认）。

舱室空槽跟**船体**走：有几个槽、槽在哪、每槽选哪一个类型组，都写在该 Hull 的 `CabinStations`。可改装菜单 = 该槽 `CabinTypeGroupId` 指向的组。同一组可挂到许多槽；改组内容即改所有这些槽的菜单。程序不写死哪类槽能改成哪些类型。

可改装的**帆槽也是舱室槽**：槽在帆的位置，`BindSocket` = 桅上 `Attach_Yard_*`。能挂什么帆、挂了什么帆以舱室改装为准。四表桅/桁位只验证网格能否拼接。

### 4.2 查找链

```text
Ship instance.ShipTypeId
  → DT_Ships.HullId
      → DT_ShipHulls（Hull 网格 + 桅位 + 舱室空槽）
          各位桅：实例 InstalledMasts 或 AllowedMastTypeIds[0]
            → DT_ShipMasts（桅网格 + 桁 socket）
          各位舱室槽：实例 InstalledCabins（空=未改装）
            → 槽.CabinTypeGroupId → DT_CabinTypeGroups.CabinTypeIds
              → DT_CabinTypes（岗位/装备列表）
          帆槽（BindSocket = 桅 Yard socket）：
            有该槽 → 改装权威：空槽不挂帆；已改装则用该舱室类型 AllowedEquipmentIds[0]（若有）
            无该槽 → 过渡：InstalledYardSails 或 AllowedYardSailIds[0]（美术拼接）
              → DT_ShipYardSails
```

### 4.3 旗舰组装与 v0 显示

- 船系统解析上链，把桅挂到 Hull socket，把 YardSail 挂到桅 socket。
- Socket 正名：Hull `Attach_Mast_01`（旧名 `Attach_MastRig_01` 作别名）；桅 `Attach_Yard_01`…；`Attach_Flag` 在**桅**上。
- **v0 显示（临时）**：在港 → YardSail 骨骼最后一帧（收帆）；出海 → 第 0 帧（满帆）。无风。不做半帆独立 SM。Half 状态 SM 不在本片。
- 无 YardSail / 桅位为空 → 只显示 Hull，不报组装失败为 Error（占位船合法）。
- 船体尚未写帆舱室槽时，组装仍走美术 `AllowedYardSailIds[0]`，避免未填舱室数据时旗舰丢帆。

## 5. 未编队 / 所有权

未编队必须停在城市港口。公司建造归公司（建造 later）。领取船归玩家角色；成立公司后转入 `Company_Player`。仅在港解散舰队。港容 later（现无限）。

## 6. 在港编制

城市面板 → 港口 → 舰队管理。两列（船 | 人员）。旗舰与司令置顶。`[+]` 创建；Cancel = 不创建。最多 32 艘（临时）。确认必须有旗舰和司令，否则整单拒绝。第一成功编制写入 `PlayerCommandedFleetId`。从己方其他舰队抽走船/司令/旗舰会使那队在港非法：不自动修；不能离港、不能 MoveTo、NpcAi 不调度。海上可在本队内改旗舰。不可加减船（减 = 弃船，later）。

## 7. 旗舰

合法舰队恰好一艘旗舰。场景根网格跟合法旗舰 Hull；桅/YardSail 随该旗舰实例组装。沉余船须立刻指定旗舰。最后一艘沉：舰队销毁；人员回 HQ 或最近港，否则伦敦。玩家零船时可港口领取（与开局领取相同）。

## 8. 派生属性（v0）

速度 = 最慢船 `BaseSpeed`。强度 = 各船 `BaseStrength` 之和。

## 9. 岗位

指挥权只在舰队司令。v0 旗舰舰长室占用者 **就是** 司令。其他船本片不派岗位。

## 10. 改装 UI（在港）

`UShipOutfitWidget`。无角色 3D。2D 图 + 头像。舱室槽来自旗舰 Hull `CabinStations`（不是写死的 `OutfitSlot_*` 菜单）。组内容由 `DT_CabinTypeGroups` 提供。

岗位对照（哪类舱挂司令/水手长等）在舱室开发中后续匹配；本片数据层不改舰队四岗合法性。司令只能替换不能卸任（岗位规则仍有效）。不创建 `HostKind = Ship` 的 Facility。

2D 布局规则见系统规范 §6。槽位 Id 用 `CabinStation_<Name>`。

改舱类型 API：`TrySetInstalledCabin`（类型必须属于该槽的组；`None` = 清空空槽）。改桅网格仍走组装表。帆的玩法安装走帆位舱室槽。

## 11. 新游戏

玩家无预设船队。家乡暂 **London**。港口领取一艘占位类型船后编制。NPC 公司各种子一队+旗舰；船体来自 `StarterShipTypeId`。不进 `PlayerCommandedFleetId`。

## 12. 本片明确不做

船厂建造、船只商品交易、改造、改装数值、**舱室 Facility**（舱室是 Hull 空槽 + 类型组，不是 `HostKind = Ship`）、弃船/捕获、多舰队指挥切换、每船战斗 HP、风场、半帆独立网格、`AShip`、岗位占用从舱室自动派生（后续匹配）。
