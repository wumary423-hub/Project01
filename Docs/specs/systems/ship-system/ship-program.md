---
document_type: system_program_spec
schema_version: 1
system_id: SYS-SHIP
title_zh: 船只系统 — 程序运行时
document_version: 0.2.0
status: LOCKED
source: .cursor/rules/ship-system.mdc V0.1.1
last_updated: 2026-08-19
---

# 船只系统程序规范

迁自 `.cursor/rules/ship-system.mdc` 的运行时条款。3D/2D 资产接口见 `ship-system.md` 与 `ShipType_SmallSailer01/integration.yaml`。命名见 `docs/governance/naming-and-versioning.md`。

## 1. 角色

- 船 = `UShipObject`（`UShipManagerSubsystem`）。
- 海上存在单位永远是 Fleet。**无 `AShip`**。单船编队仍显示为舰队。
- `AFleet` 网格 = 旗舰目录网格。旗舰记在舰队 `FlagshipShipId`，不在船上做第二真相。

## 2. 架构

| 件 | 路径 / 类型 |
|----|-------------|
| Object | `UShipObject` — `Source/.../Ship/` |
| Manager | `UShipManagerSubsystem` |
| Settings | `UShipManagerSettings` |
| Types | `ShipTypes.h`（实例 `Ship_<N>`；占位类型 `ShipType_TempCog` / `TempCaravel` / `TempCarrack`；第一艘正式类型 `ShipType_SmallSailer01`） |
| Catalog | `DT_Ships` / `FShipDefinition` — `/Game/Ship/DT_Ships` |
| 船网格 | `/Game/Ships/ShipType_SmallSailer01/` |
| Tools | `Tools/CreateShipsDataTable.py`；`Tools/ImportSmallSailer01Meshes.py`；`Tools/ValidateShipMeshes.py` |
| UI | `UCityPortWidget` + `UFleetManagementWidget` + `UShipOutfitWidget` |
| Save | `FShipSaveData`（`SaveTypes.h`，schema **v7**） |

## 3. Id

- 实例：`Ship_<序号>`。舰队：`Fleet_<序号>`。禁止 `Fleet_Player_*` 当 Id。
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

`FShipDefinition`：type id、display name、mesh、`BaseSpeed`、`BaseStrength`。实例不存速度/强度。占位行：`ShipType_TempCog` / `TempCaravel` / `TempCarrack`。缺表则内置 Cog。改船体改 DataTable，不改 C++。

## 5. 未编队 / 所有权

未编队必须停在城市港口。公司建造归公司（建造 later）。领取船归玩家角色；成立公司后转入 `Company_Player`。仅在港解散舰队。港容 later（现无限）。

## 6. 在港编制

城市面板 → 港口 → 舰队管理。两列（船 | 人员）。旗舰与司令置顶。`[+]` 创建；Cancel = 不创建。最多 32 艘（临时）。确认必须有旗舰和司令，否则整单拒绝。第一成功编制写入 `PlayerCommandedFleetId`。从己方其他舰队抽走船/司令/旗舰会使那队在港非法：不自动修；不能离港、不能 MoveTo、NpcAi 不调度。海上可在本队内改旗舰。不可加减船（减 = 弃船，later）。

## 7. 旗舰

合法舰队恰好一艘旗舰。场景网格跟合法旗舰。沉余船须立刻指定旗舰。最后一艘沉：舰队销毁；人员回 HQ 或最近港，否则伦敦。玩家零船时可港口领取（与开局领取相同）。

## 8. 派生属性（v0）

速度 = 最慢船 `BaseSpeed`。强度 = 各船 `BaseStrength` 之和。

## 9. 岗位

指挥权只在舰队司令。v0 旗舰舰长室占用者 **就是** 司令。其他船本片不派岗位。

## 10. 改装 UI（在港）

`UShipOutfitWidget`。无角色 3D。2D 图 + 头像。舰长室=司令（高亮）；甲板=水手长；炮位=炮长；制图室=领航员。司令只能替换不能卸任。瞭望塔/船帆/火炮配置锁定占位。不创建 `HostKind = Ship` 的 Facility。

槽位 Id：`OutfitSlot_CaptainCabin` / `Deck` / `GunDeck` / `ChartRoom` / `Lookout` / `Sails` / `CannonRefit`。布局规则见系统规范 §6。

## 11. 新游戏

玩家无预设船队。家乡暂 **London**。港口领取一艘占位类型船后编制。NPC 公司各种子一队+旗舰；船体来自 `StarterShipTypeId`。不进 `PlayerCommandedFleetId`。

## 12. 本片明确不做

船厂建造、船只商品交易、改造、改装数值、舱室 Facility、弃船/捕获、多舰队指挥切换、每船战斗 HP。
