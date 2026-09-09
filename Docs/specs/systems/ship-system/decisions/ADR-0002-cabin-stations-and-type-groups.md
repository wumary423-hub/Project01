---
document_type: architecture_decision
adr_id: ADR-0002
system_id: SYS-SHIP
title_zh: 舱室空槽跟船体走，类型组决定可改装菜单
status: LOCKED
date: 2026-09-09
supersedes: OutfitSlot hardcoded hotspots as gameplay allow-list
---

# ADR-0002 — 舱室空槽与舱室类型组

## 决定

1. **舱室跟船体走。** `DT_ShipHulls.CabinStations[]` 决定：有几个空槽、槽在 2D 改装图上的位置、可选 3D `BindSocket`、每个槽选 **一个** `CabinTypeGroupId`。
2. **可改装菜单只读类型组。** `DT_CabinTypeGroups` 的 `CabinTypeIds[]` 就是该槽能改装的类型。组有哪些、里面有哪些类型，由玩法数据填写。程序不写死水线/炮窗/军官等分类。
3. **同一组可挂到许多槽。** 改组内容（例如底层组加入新货舱类型）即改所有引用该组的槽，不必逐槽改 Id。
4. **实例** `InstalledCabins`：`StationId` + `CabinTypeId`。缺项或 `None` = 未改装空槽（不回落到组的 `[0]`）。
5. **可改装帆槽都是舱室槽**，位置在帆上，`BindSocket` 对桅 `Attach_Yard_*`。能挂什么帆、挂了什么帆以改装为准。`DT_ShipMasts.YardStations.AllowedYardSailIds` 只表示该 socket **物理上**接得住哪些网格。
6. **组装过渡：** 船体上若已有绑定该 yard socket 的舱室槽，则只信舱室安装（空槽不挂帆）。若还没有这样的槽，仍用 `InstalledYardSails` / `AllowedYardSailIds[0]`，避免未填舱室数据时旗舰丢帆。
7. 舱室 **不是** `HostKind = Ship` 的 Facility。岗位占用从舱室类型派生后做。

## 原因

此前改装 UI 把 `OutfitSlot_*` 写死对照舰队四岗，桅/帆允许列表写在组装表上，是为了让已有系统与美术拼接能跑。正式改装需要：大船几十个槽只选组、改一组即改一批槽、帆的玩法权威回到改装。

## 后果

- LOCKED `ship-system.md` / `ship-program.md` / `ship-system.yaml` 升至 **0.5.0**（0.4.0 已用于组件优先制作工作流）。
- 命名增加 `CabinType_*` / `CabinTypeGroup_*` / `CabinStation_*`。
- 实现：C++ 结构 + 空 `DT_CabinTypes` / `DT_CabinTypeGroups` 壳；组内容与各船体空槽由设计在表里填。
