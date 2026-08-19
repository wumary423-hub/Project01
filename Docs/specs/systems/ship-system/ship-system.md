---
document_type: system_spec
schema_version: 1
system_id: SYS-SHIP
title_zh: 船只系统
document_version: 0.2.0
status: LOCKED
migration_status: MIGRATED
legacy_source:
  path: .cursor/rules/ship-system.mdc
  version: "0.1.1"
  status: ADAPTER
last_updated: 2026-08-19
---

# 船只系统规范

跨 Cursor、ChatGPT、Meshy、Blender、UE5 的船只系统规范。**状态：LOCKED。**

- 跨工具与 3D/2D 接口：本文件 + `ship-system.yaml`
- 程序运行时：`ship-program.md`
- 第一艘船：`docs/specs/assets/ships/ShipType_SmallSailer01/`
- 命名：`docs/governance/naming-and-versioning.md`
- Cursor 入口：`.cursor/rules/ship-system.mdc`（适配层，不得另写一套事实）

第一艘船主键：**`ShipType_SmallSailer01`**（废止 `SHIP-0001`）。  
UE 网格：`/Game/Ships/ShipType_SmallSailer01/`。目录表仍为 `/Game/Ship/DT_Ships`。

`Docs/Ship/*` 为 SUPERSEDED 指向。

## 2. 每艘船的必备资产

必须同时具备 3D 船资产与 2D 岗位布局，并在船体比例、船艏方向、桅数与位置、甲板层级、艉楼、货舱/主要功能区、可交互大模块上一致。

## 3. 观察距离与细节原则

两档距离，不冲突：

| 档 | 距离 | 用途 |
|----|------|------|
| 常规 | **50–200m** | 战略地图默认观察；决定什么必须做成可读几何 |
| 极限近距 | **约 10m** | 仍应能认船、比例正确；不是常规镜头 |

优先级：桅数 > 甲板层 > 帆装轮廓 > 船体轮廓 > 大件 > 小装饰。

优先：船体轮廓、艏艉、甲板、桅/桁/帆（以 MastRig 整包呈现）、艉楼、大货舱口、舵、旗与船首像接口。

避免默认：微型绳结、铆钉、小滑轮、无功能小桶杂物。

## 4. 模块化要求

### 4.1 UE 最终模块（功能导向）

- Hull（`AFleet` 根网格）
- MastRig 整包（桅+桁+帆+少量索具；换 RigType = 换整套三状态网格，不是材质开关）
- 舵、旗、船首像、锚、断桅、可选艏帆
- 艉楼 v0 焊在 Hull 上

**禁止**把一期 UE 交付拆成独立的 `Mast_Main` / `Yard_Main` / `Sail_Main` 三件网格。Meshy 可分件出毛坯；Blender 打成 MastRig 包。

一期 RigType：**Square + Lateen**（各 Full/Half/Furled）。Gaff 仅兼容、一期不产。

### 4.2 旗帜

- 必备、可更换
- Socket **`Attach_Flag` 在活动 MastRig 网格上**，不在 Hull 上
- 桅隐藏或断桅时隐藏旗

### 4.3 船首像

- Hull `Attach_Figurehead`；实际网格可占位或空

### 4.4 船员接口

- 不设置 Crew Socket
- 岗位用 2D 改装图 + 头像，不把角色网格挂到 `Attach_*`

## 5. 货舱表现

只表示舱室是否为货舱。不按货物种类或数量生成货物模型。

## 6. 2D岗位布局

有透视的侧视图；船头朝左；2048×1024；透明；8–10% 边距；无烘焙热区；槽位 `OutfitSlot_*`。不得画出 3D 没有的结构。

## 7. 标准工作流

1. Reference / Research  
2. Concept Design & Structural Lock  
2.5 Meshy Reference Pack  
3. Meshy Base Mesh  
4. Blender Reconstruction  
5. UE5 Game Asset  
6. 2D Job-layout / UI Asset  

未经用户确认不得跨越结构锁定。

## 8. 概念母版与生成输入分离

Concept Master 锁身份。Meshy 包可去掉展开帆和杂物。不得为 Meshy 改锁定船体性格。

## 9. UE5交付

单船 `integration.yaml` 记录：单位与坐标、模块、Pivot、Socket、材质槽、UV、LOD、Collision、Nanite、导出路径、2D 图路径。

程序类与存档见 `ship-program.md`。Socket 名以 `integration.yaml` 为准（来自原 `.mdc` V0.1.1）。
