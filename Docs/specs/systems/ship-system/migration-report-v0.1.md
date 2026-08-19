# Ship System V0.1 Migration Report

Status: **ROUND 1 — REVIEW only. Not submitted. Old `.mdc` still authoritative.**  
Date: 2026-08-19  
Reporter: Cursor (working tree; HEAD = `docs-sync`)

## 旧规则基本信息

| 项 | 值 |
|----|----|
| 路径 | `.cursor/rules/ship-system.mdc` |
| 本轮是否改写 | **否**（未覆盖、未删除、未改内容） |
| 工作区实际版本 | **V0.1.1**（3D asset pipeline；Stage 2.6.1 Square+Lateen；Headsail 接口已批） |
| 启动包声称版本 | V0.1 LOCKED |
| `dev/widepath-nav` 上的同路径文件 | 更短（约 16441 字符 vs 工作区 20697）；内容为 V0.1，**落后于工作区** |
| 工作区文件 hash-object | `b27794b80513e50739212f1ed56adfec357eab55` |
| 对既有程序的权威 | 迁移批准前：**旧 `.mdc` 继续 LOCKED 权威** |
| 新 `ship-system.md` | `REVIEW` / `MIGRATION_PENDING` |

启动包未包含旧 `.mdc` 原文。本报告依据**工作区完整原文**（V0.1.1），不是启动包候选稿。

## 完整条款映射

分类：P=程序运行逻辑 D=数据结构 N=命名 F=文件路径 A=美术接口 W=工作流程 X=禁止性规则 NTE=备注

| # | 分类 | 旧规则（原文或可回溯摘要） | 新体系目标文件 | 本轮写入？ |
|---|------|---------------------------|----------------|------------|
| 1 | P | 船 = `UShipObject` in `UShipManagerSubsystem` | `ship-system.md` §11.1；将来程序合同 | 候选摘要，未 LOCKED |
| 2 | P | 海上存在单位永远是 Fleet；**No `AShip`** | 同上 | 候选摘要 |
| 3 | P | `AFleet` mesh = flagship catalog mesh；`FlagshipShipId` 在舰队上 | 同上 | 候选摘要 |
| 4 | D | `ShipTypes.h`：`Ship_<N>`，`ShipType_TempCog` / `TempCaravel` / `TempCarrack` | 程序规范 / `ship-system.md` §11 | 候选摘要 |
| 5 | F | Catalog `DT_Ships` / `FShipDefinition` — `Content/Ship/`；工具 `Tools/CreateShipsDataTable.py` → `/Game/Ship/DT_Ships` | 程序规范 | 仅报告 |
| 6 | P | UI：`UCityPortWidget` + `UFleetManagementWidget` + `UShipOutfitWidget` | 程序规范 | 仅报告 |
| 7 | D | Save `FShipSaveData` in `SaveTypes.h` schema **v7** | 程序规范 | 候选摘要 |
| 8 | N | Ship Id `Ship_<序号>`；Fleet Id `Fleet_<序号>`；禁止 `Fleet_Player_*` 作玩家标记 | 程序规范 | 仅报告 |
| 9 | P | `PlayerCommandedFleetId`；`OwnerCompanyId == Company_Player`；无公司时 `OwnerCharacterId` | 程序规范 | 仅报告 |
| 10 | D | 实例字段：`ShipId` / `ShipTypeId` / `DisplayName` / `OwnerCompanyId` / `OwnerCharacterId` / `FleetId` / `HostCityId`；`Berth` not in v0 | 程序规范 | 仅报告 |
| 11 | D | `FShipDefinition`：type id, display name, mesh, `BaseSpeed`, `BaseStrength`；实例不存速度/强度 | 程序规范 | 仅报告 |
| 12 | P | 未编队必须停在城市港口；解散舰队仅在港；港容无限（later cap） | 程序规范 | 仅报告 |
| 13 | P | 在港编制：旗舰+司令原子确认；每队最多 32 船（temp）；非法编队不自动修复 | 程序规范 | 仅报告 |
| 14 | P | 合法舰队恰好一艘旗舰；沉船后指定旗舰；最后一艘沉→舰队销毁 | 程序规范 | 仅报告 |
| 15 | P | 速度=最慢船 `BaseSpeed`；强度=各船 `BaseStrength` 之和 | 程序规范 | 仅报告 |
| 16 | P | 舰队司令才有指挥权；v0 旗舰舰长室占用者 **就是** 司令 | 程序规范；2D 岗位见下 | 仅报告 |
| 17 | A | 改装 UI：无角色 3D；2D schematic + avatar；`UShipOutfitWidget` | `SHIP-xxxx/design.md` + 程序规范 | 仅报告 |
| 18 | A | 2D 图：`T_<ShipType>_OutfitDiagram`；2048×1024；透明；8–10% 边距；船头朝左；侧视略俯；**无烘焙热区** | `ship-system.md` §6（部分已有）+ design | 冲突：路径 |
| 19 | D | 槽位 `OutfitSlot_CaptainCabin/Deck/GunDeck/ChartRoom/Lookout/Sails/CannonRefit` ↔ `EFleetPost` | 程序规范 + 2D | 仅报告 |
| 20 | X | **Never** attach character meshes to hull `Attach_*` | `ship-system.md` crew_sockets | 双方一致 |
| 21 | A | 3D：Hull + MastRig Furled/Half/Full + flag + figurehead + rudder + anchor + damage FX + optional weapons | design / integration | **冲突** 模块拆分 |
| 22 | W | 工作名 `SmallSailer01`；建议目录行 `ShipType_SmallSailer01` | design / catalog | **冲突** Asset ID |
| 23 | A | Stage 2.6.1：Square+Lateen 各 Full/Half/Furled；Gaff 一期不产 | design / integration | **冲突** 与 Mast_Main 拆件 |
| 24 | A | Headsail：Hull `Attach_Headsail_01`；首发不装网格 | integration | **冲突** 启动包无此 socket |
| 25 | A | Hull 根网格；`Pontoon_*` ×4 Error if missing | integration | **冲突** 启动包未列 |
| 26 | A | `Attach_MastRig_01`；`Attach_Sail_Main` deprecated | integration | **冲突** |
| 27 | A | `Attach_Flag` **on MastRig mesh, not Hull** | integration `flag_socket.name: null UNSET` | **冲突** |
| 28 | A | Hull attach：Figurehead/Rudder/Anchor/FX_Fire/Mast_Broken/Weapon×2/Headsail | integration | **冲突** 名称 UNSET |
| 29 | W | 帆视觉状态 Furled/Half/Full；无玩法读回 | ship-system.yaml / design | 部分可对齐 |
| 30 | F | UE `/Game/Ship/SmallSailer01/`；磁盘 `Content/Ship/SmallSailer01/Mesh/*.fbx` | integration `ue5.destination_path` | **冲突** `/Game/Ships/SHIP-0001/` |
| 31 | F | `Tools/ImportSmallSailer01Meshes.py`；`Tools/ValidateShipMeshes.py` | tools 适配 | 仅报告 |
| 32 | W | Socket 在 UE Static Mesh Editor 添加；Validate 读最终 UE 网格，不要求 FBX 内含 | integration / ue5 guide | 仅报告 |
| 33 | W | Blender：Apply Rotation+Scale；**+X** forward；一 FBX 一资产 | integration `coordinate_system` | 启动包 UE forward X 为 REVIEW；pivot UNSET |
| 34 | P | 新游戏无预设玩家船；伦敦港口领取；NPC 公司多种子船型 | 程序规范 | 仅报告 |
| 35 | X | 本片不做：船厂建造、船只商品交易、改造、改装数值、舱室 Facility、弃船/捕获、每船战斗 HP 等 | ship-system.md 范围 | 仅报告 |
| 36 | X | 无 Crew Socket / 3D crew；无动态货物网格 | ship-system.yaml `crew_sockets.allowed: false`；cargo | **一致** |
| 37 | NTE | 权威链（旧）：`ship-system.mdc` > `Docs/Ship/ShipAssetContract.md` > `Docs/Ship/SmallSailer01.md` | 与新体系权威链冲突 | **冲突** 见下 |
| 38 | A | 观察距离：程序写战略镜头 **50–200m**；细节优先级 mast>deck>rig>hull>parts>decor | ship-system.md §3 写 **10m** | **冲突** |

## 未迁移内容

下列旧规则**没有**写入 `SHIP-0001/integration.yaml` 或设为 LOCKED 系统规范（避免未批准综合）：

1. 全部 C++ 类/子系统/UI widget 名称与职责（仅 §11 摘要）。
2. `FShipDefinition` / `FShipSaveData` 字段表。
3. `EFleetPost` 与 `OutfitSlot_*` 对照。
4. 编制/旗舰/司令/存档 schema v7 运行时逻辑。
5. `Pontoon_*` 与全部 `Attach_*` 正式写入合同（integration 仍 UNSET）。
6. MastRig scheme A 文件名与 Square/Lateen 清单。
7. `ShipType_SmallSailer01` 与 `SHIP-0001` 的正式对应。
8. `DT_Ships` 行、导入/校验 Python 工具路径。
9. LOD / Collision / Nanite：**旧 `.mdc` 无条款** → 保持 UNSET，**未用 UE5 常识补全**。
10. Pivot 定义：**旧 `.mdc` 无数值** → UNSET。
11. 船长/船宽/吃水：**程序写 ~15m 概念且无硬校验**；design.md 写 12–13m PROVISIONAL；integration 数值 UNSET。三者未合并。

## 冲突

### C1. Asset ID / 工作名

- 旧：`SmallSailer01` / `ShipType_SmallSailer01`
- 新：稳定 Asset ID `SHIP-0001`（必须保留）
- 建议：`SHIP-0001` = 资产主键；`SmallSailer01` = 工作名/文件夹；catalog `ShipType_SmallSailer01`。需你批准映射表。
- LOCKED：旧程序命名 + 新 SHIP-0001 ID 同时有效直到你选映射。

### C2. UE Content 路径

- 旧：`/Game/Ship/SmallSailer01/`（单数 `Ship`）
- 新 integration：`/Game/Ships/SHIP-0001/`
- 适配器 glob：`Content/Ships/**`（与现有 `Content/Ship/` 不一致）
- 建议：程序路径保持 `/Game/Ship/...`；规范层用 SHIP-0001 引用；改 adapter glob。

### C3. 模块拆分

- 旧：Hull + **MastRig 整包**（桅+桁+帆+索具）× RigType × 3 状态；旗在 MastRig 上
- 新 design：`Hull` / `Mast_Main` / `Yard_Main` / `Sail_Main` 可分件；`flag_socket` 名称 UNSET
- **不得自行综合。** 建议：生产与 UE 以 MastRig scheme A 为准（旧 LOCKED）；Meshy 毛坯可按 hull-focused 分件，Blender 再打成 MastRig 包。

### C4. Socket 名称

| 用途 | 旧 `.mdc` | 启动包 integration.yaml |
|------|-----------|-------------------------|
| 浮力 | `Pontoon_*` ×4 | 未出现 |
| 主桅挂点 | `Attach_MastRig_01` | `mast_mount` 无 name |
| 旗 | `Attach_Flag` on **MastRig** | `flag_socket.name: null` UNSET |
| 船首像 | `Attach_Figurehead` | `figurehead_socket.name: null` UNSET |
| 舵 | `Attach_Rudder` | rudder_mount 无 name |
| 艏帆 | `Attach_Headsail_01` | 无 |
| 武器 | `Attach_Weapon_Port_01` / `_Starboard_01` | 无 |

### C5. 观察距离

- 旧：典型镜头 **50–200m**
- 新：`typical_minimum_view_distance_m: 10`
- 建议：10m 作「仍应可读的最近距离」；50–200m 作战略默认。需你确认，不自动改 yaml。

### C6. 同义规范三套并存

| 位置 | 角色 |
|------|------|
| `.cursor/rules/ship-system.mdc` | 旧程序 LOCKED（本轮未改） |
| `Docs/Ship/SmallSailer01.md` + `ShipAssetContract.md` + `CHANGELOG.md` | docs-sync 设计稿；权威声明仍指向 `.mdc` |
| `Docs/specs/assets/ships/SHIP-0001/design.md` | 启动包单船设计（V0.8 母版 LOCKED） |

未删除、未覆盖 `Docs/Ship/*`。

### C7. 目录大小写（Windows）

- 启动包：`docs/`、`tools/`
- 本仓已有：`Docs/`、`Tools/`
- NTFS 不区分大小写。文件并入现有 `Docs/`、`Tools/`；清单路径仍写 `docs/`、`tools/`，校验可通过。

### C8. Git LFS 模板过宽

模板要对全部 `*.png` / `*.uasset` / `*.umap` 开 LFS。本仓已跟踪 `Docs/MapRefs/*.png` 和大量 Content。本轮 **只** 对 `assets/ships/**` 的大美术/3D 扩展名加 LFS 规则。本机 `git lfs version` 无输出，可能未装 Git LFS。

### C9. 无法快进到 `dev/widepath-nav`

工作区大量未跟踪文件与该分支已跟踪文件同路径，且部分内容更新（`ship-system.mdc` V0.1.1、`fleet-system.mdc` 等）。`git checkout` 会覆盖。本轮 **未强制切换**。HEAD 仍为 `docs-sync`；磁盘上已有完整游戏树。

## 程序影响

| 领域 | 影响 |
|------|------|
| C++ `Source/.../Ship/` | 无代码改动。类名/字段仍以旧 `.mdc` 为准。 |
| Blueprint | 无改动。`BP_Fleet`、`WBP_ShipOutfit` 等仍按旧规则。 |
| DataAsset / `DT_Ships` | 无改动。`FShipDefinition.Mesh` 仍只挂 Hull。 |
| 保存 | 无改动。仍为 `FShipSaveData` schema v7。 |
| 目录 | 新增仓库根 `spec-manifest.yaml`、`assets/`、`Docs/specs|governance|schemas|tool-guides|decisions/`、`Tools/validate_specs.py` 等。不取代 `Content/Ship/`。 |
| 运行时 | 无。 |

## 建议差异（待你批准后第二轮才落地）

1. 锁定映射：`SHIP-0001` ↔ `SmallSailer01` ↔ `ShipType_SmallSailer01`。
2. 把 socket 名从旧 `.mdc` 写入 `integration.yaml`（结束 UNSET），**不要**改名。
3. 模块合同改为 MastRig scheme A；Meshy 分件标为中间产物。
4. `ue5.destination_path` 改为 `/Game/Ship/SmallSailer01/` 或批准新路径并做迁移计划。
5. 新 `ship-system.md` 在你批准后升为 LOCKED；旧 `.mdc` 改为只引用权威规范的适配入口。
6. `Docs/Ship/*` 改为指向 `Docs/specs/...` 的摘要，或标 SUPERSEDED。
7. 安装 Git LFS 后再把 `assets/ships/**/*.png` 真正纳入 LFS。
8. 在 `widepath-nav` 谱系建分支提交（需你处理 checkout 覆盖问题或允许我按无丢失策略合并）。

## 验证结果

**官方脚本未跑通：** 本机 `python` / `py` 不可用（仅 WindowsApps 商店占位）。已用 PowerShell 做等价路径/哈希检查。

PowerShell 结果（2026-08-19）：**23 OK, 0 error**。含 V0.8 SHA-256 一致、旧 `.mdc` hash-object 未变、仅 `SHIP-0001`。Schema 级 YAML 校验待安装 Python 后执行：

```text
python -m pip install -r Tools/requirements-specs.txt
python Tools/validate_specs.py
```

计划检查项：

- YAML 可解析
- Schema（manifest + SHIP-0001 integration）
- Manifest 引用路径
- V0.8 PNG SHA-256 = `0c848da018e5c4ebe1edc65611d9b46a2e6633a09430aba8af80ccbf01bfe44d`（复制后已核对，大小写不同但哈希一致）
- Asset ID 无重复（仅 SHIP-0001）
- 旧 `.mdc` 仍存在且本轮未改
- 旧规则与新合同冲突：**已列出，未自动消解**

## 用户批准记录

- 已批准：采用「Git 唯一权威 / MD 可读 / YAML 合同 / 工具适配层」；启动包合并到完整游戏仓（选项 A）；第一轮实现。
- **2026-08-19 第二轮（内容 Cursor / 格式 GPT）：**
  - 主键 **B**：废止 `SHIP-0001`，规范主键 = `ShipType_SmallSailer01`；
  - UE 路径 `/Game/Ships/ShipType_SmallSailer01/`；
  - MastRig 整包写入启动包模块表；Meshy 可分件；
  - Socket 写入旧锁定名；
  - 观察距离：50–200m 常规 + 10m 极限，不冲突；
  - `Docs/Ship/*` → SUPERSEDED 指向；
  - 旧 `.mdc` **仍未改写、仍未解除 LOCKED**；新 `ship-system.md` 仍为 `REVIEW`。
- **仍未批准：** 新正文 LOCKED；旧 `.mdc` 改成纯适配器；Git 提交/推送。

## 2026-08-19 第三轮（命名纳入 + 锁定 + 适配器）

用户批准：纳入程序命名；完成上一轮未做的 LOCKED、`.mdc` 改入口、Import/Validate 路径。

- 命名：`Docs/governance/naming-and-versioning.md` LOCKED
- 运行时迁入 `ship-program.md` LOCKED
- `ship-system.md` LOCKED；`.mdc` = 适配入口
- 网格路径：`/Game/Ships/ShipType_SmallSailer01/`
- **仍未提交 Git**


## 校验命令记录

```text
python -m pip install -r Tools/requirements-specs.txt
python Tools/validate_specs.py
```
