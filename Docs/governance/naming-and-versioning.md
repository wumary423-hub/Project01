---
document_type: governance_policy
document_version: 0.4.0
status: LOCKED
authority: canonical
last_updated: 2026-09-09
source_program_rule: .cursor/rules/ue-naming.mdc
---

# 命名与版本规则

跨工具稳定 ID、Content 前缀与规范文件版本。内容来自已锁定的程序命名；C++ 类前缀（`A`/`U`/`F`/`E`）仍只在 Cursor 适配层 `.cursor/rules/ue-naming.mdc`。

## 1. 实体 Id（`FName`，跨系统唯一）

形式：`<System>_<Name>`，下划线后 PascalCase。

| 系统 | 形式 | 例 |
|------|------|-----|
| 船实例 | `Ship_<序号>` | `Ship_1` |
| 船类型（总表行） | `ShipType_<Name>` | `ShipType_SmallSailer01` |
| 船体种（美术表） | `ShipHull_<Name>` | `ShipHull_SmallSailer01` |
| 桅种（美术表） | `ShipMast_<Name>` | `ShipMast_SmallSailer01_Main` |
| 桁帆种（美术表） | `ShipYardSail_<Name>` | `ShipYardSail_SmallSailer01_Square_01` |
| 舱室类型 | `CabinType_<Name>` | `CabinType_CargoHold` |
| 舱室类型组 | `CabinTypeGroup_<Name>` | `CabinTypeGroup_BelowWaterline` |
| 船体舱室空槽 | `CabinStation_<Name>` | `CabinStation_Hold_01`（在该 Hull 上唯一） |
| 舰队 | `Fleet_<序号>` | `Fleet_1` |
| 商号 | `Company_<Name>` | `Company_Player` |
| 角色 | `Char_<Name>` | `Char_PlayerLeader` |
| 设施 | `Fac_<Host>_<Type>` | `Fac_London_Market` |
| 货物 | `Goods_<Name>` | `Goods_Grain` |

- 玩家指挥标记是 `PlayerCommandedFleetId`，**不是**舰队 Id。禁止 `Fleet_Player_*` 当 Id。
- 角色 Id 碰撞加后缀：`Char_Foo_2`。
- **禁止**裸 `Player` / `Default` / `Main` 当 Id。
- **禁止** `Family_*`（Family 已从设计删除）。
- **城市 / 海区遗留例外**：`London`、`EuropeNW` 等保持裸 Id。新系统必须用前缀，勿再引入会与城市撞名的裸 Id。
- 显示名称可改；稳定 Id 不随显示名变化。
- **废止**启动包主键 `SHIP-0001`。第一艘船规范主键 = 目录行 = `ShipType_SmallSailer01`。工作名 `SmallSailer01` 只用于 `SM_SmallSailer01_*` 网格前缀。

## 2. Content 资源前缀

| 资产 | 前缀 | 路径 |
|------|------|------|
| Blueprint | `BP_` | `Content/Blueprint/<System>/` |
| Widget | `WBP_` | `Content/UI/` 或 `Content/Blueprint/UI/` |
| DataTable | `DT_` | `Content/<System>/`（船总表 `/Game/Ship/DT_Ships`；美术 `DT_ShipHulls` / `DT_ShipMasts` / `DT_ShipYardSails`；舱室 `DT_CabinTypes` / `DT_CabinTypeGroups`） |
| Static mesh | `SM_` | 领域目录 |
| Skeletal mesh | `SK_` | 领域目录（YardSail 优先骨骼） |
| Material | `M_` | `Content/Materials/` |
| Texture | `T_` | 领域目录；UI 临时 `T_UI_*` 在 `Content/Temp/UI/` |
| Map | `Map_` | `Content/Maps/Map_<SeaRegion>` |

- 临时导入只进 `Content/Temp/`，不当成品。
- 第一艘船网格 UE 路径：`/Game/Ships/ShipType_SmallSailer01/`（及 `Mesh/`）。
- 已有 CityId / SeaRegionId / 货物 Id 未经迁移计划不得改名。

## 3. 规范与资产文件路径

- `Docs/specs/`、`Docs/governance/`：ASCII；可用大小写以匹配 Id（如 `ShipType_SmallSailer01`）；无空空格。
- 概念图：`assets/ships/<AssetId>/concept/<AssetId>_concept-master_r<rev>.png`
- 网格工作文件：`SM_SmallSailer01_Hull.fbx` 等（工作名前缀，不是 `SM_ShipType_...`）

## 4. 规范文档版本

```text
document_version: 0.2.0
```

- Patch：文字澄清；Minor：增加要求；Major：改锁定接口。

视觉概念修订（与规范版本分开）：`concept_revision: 0.8` → 文件名 `r0.8`。  
3D/UE 资产版本与概念图版本不得混用。

## 5. 状态词

`DRAFT` / `REVIEW` / `LOCKED` / `SUPERSEDED` / `DEPRECATED` / `UNSET` / `MIGRATION_PENDING`

## 6. Git 提交建议

```text
spec(ship): lock ShipType_SmallSailer01 concept master r0.8
spec(naming): import program entity-id and content prefixes
```
