---
document_type: architecture_decision
adr_id: ADR-0001
system_id: SYS-SHIP
title_zh: 四表目录与桅/桁帆分件
status: LOCKED
date: 2026-09-08
supersedes: MastRig scheme A whole_package
---

# ADR-0001 — 四表目录与桅 / YardSail 分件

## 决定

1. **`DT_Ships` 只做船种总表**（身份 + 玩法数 + `HullId`）。船体网格、桅位、桅种、桁位、YardSail 不进总表。
2. 美术分三张可复用表：`DT_ShipHulls` / `DT_ShipMasts` / `DT_ShipYardSails`。查找键是类型 Id，不是 mesh 路径。
3. **废止 MastRig 整包**（桅+桁+帆一件 × RigType × Full/Half/Furled）。UE 装配为：

```text
Hull（AFleet 根）
  └─ Hull socket → 独立桅网格
       └─ 桅 socket → YardSail（帆+桁一件；骨骼优先）
```

4. **仍禁止**把桁与帆拆成两件 UE 网格。
5. `Attach_Flag` 在**桅**网格上。Hull 挂桅 socket 正名为 `Attach_Mast_01`；`Attach_MastRig_01` 为旧名别名。
6. 实例可存实际安装的 `MastTypeId` / `YardSailId`；空则回退该位 `Allowed*Ids[0]`。Fleet 不存帆装。
7. 船系统组装旗舰外观；`AFleet` 只读组装结果。无 `AShip`。

## 原因

总表若同时挂玩法与全部挂点/允许列表，行会膨胀且桅种无法跨船复用。帆测试转入需要独立桅与可动画的 YardSail，MastRig 整包无法表达。

## 后果

- LOCKED `ship-system.md` / `ship-program.md` / `ship-system.yaml` 升至 0.3.0。
- `ShipType_SmallSailer01` 模块合同改分件；旧 `SM_*_MastRig01_<Rig>_<State>` 文件名作废。
- 实现另开；本 ADR 不授权改 C++。
