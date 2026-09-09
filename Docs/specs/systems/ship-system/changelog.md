# Ship System Changelog

## 0.5.0 — 2026-09-09 — LOCKED（舱室空槽 + 类型组）

- **ADR-0002**：舱室跟船体走。`DT_ShipHulls.CabinStations[]` 决定空槽数量、2D 位置、可选 `BindSocket`、**一个** `CabinTypeGroupId`。
- 新增 `DT_CabinTypes` / `DT_CabinTypeGroups`。组内容由玩法填；程序只读。
- 实例 `InstalledCabins`：空 = 未改装。帆槽是舱室槽；组装优先读舱室。
- 2D 改装图热区是 `CabinStation_*`；帆槽画在帆的位置。不创建 `HostKind = Ship` 的 Facility。

## 0.4.0 — 2026-08-23 — LOCKED

- 船只资产制作切换为组件优先工作流；
- 完整效果概念图锁定风格，组件独立制作/复用后在 Blender 组装；
- 首轮验证只做 Hull 与简单独立 Deck；
- 炮窗改为独立逻辑模块，不内建到 Hull；
- 旧整船线稿、多视图、共享白模和整船 AI 3D 输入流程退役。

更早的变更历史保留在 Git。
