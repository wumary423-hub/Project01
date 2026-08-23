---
document_type: system_spec
schema_version: 1
system_id: SYS-SHIP
title_zh: 船只系统
document_version: 0.4.0
status: LOCKED
migration_status: MIGRATED
last_updated: 2026-08-23
---

# 船只系统规范

跨 Cursor、ChatGPT、Tripo 3D、Blender、UE5 的船只系统规范。程序运行时见 `ship-program.md`，美术生产规则见 `Docs/specs/assets/ships/production-rules.md`。

第一艘船主键为 `ShipType_SmallSailer01`；旧 ID `SHIP-0001` 已废止。UE 目录为 `/Game/Ships/ShipType_SmallSailer01/`。

## 1. 观察距离与细节

- 常规观察距离：50–200m；极限近距约 10m。
- 优先级：船体轮廓 > 甲板与上层建筑 > 桅帆轮廓 > 主要功能部件 > 小装饰。
- 避免默认制作无逻辑意义的微型装饰和松散杂物。

## 2. 部件化资产

船只首先由独立部件制作，再在 Blender 中组装。最小体系包括：

- `Hull`：船身核心；
- `Deck`：独立甲板；
- `Gunport`：独立炮窗模块，可带布尔 Cutter 与火炮锚点；
- 艉楼/前楼及其可继续拆分的子部件；
- `MastRig`、舵及其他具有运行时逻辑的模块。

部件可以进入跨船复用库。复用前只调整尺寸、材质、Pivot、Socket 和兼容标签。

## 3. 炮窗与火炮接口

炮窗不是 Hull 的预制开口。炮窗模块在 Blender 组装时定位并切割船舷，炮窗锚点负责绑定火炮和朝向。炮窗数量与布局由单船设计锁定。

## 4. 现行工作流

1. 完整效果概念图；
2. 根据概念图拆解部件并检查复用；
3. 制作主零件并验证流程，当前首先验证船身；
4. 制作或复用其他零件；
5. Blender 组装整船；
6. 进入 UE5。

旧整船线稿和整船多视图生产链已废止。多视图仅在具体零件需要时制作。

## 5. 当前船身验证交付

`ShipType_SmallSailer01` 的首次验证只交付：

- 连续、无炮窗、无附件的 `Hull`；
- 一块可在 Blender 中手动缩放和定位的简单 `Deck`。

Tripo 3D 只生成船身核心；Deck 可以在 Blender 中直接建立。装饰、锚、灯、绞盘、艉楼、桅杆、舵和炮窗均不进入该次验证。

## 6. UE5交付

单船 `integration.yaml` 记录单位、坐标、模块、Pivot、Socket、材质槽、UV、LOD、Collision、导出路径和 2D 布局。最终是否合并网格由运行时逻辑决定，不得在制作阶段丢失炮窗、火炮等关键锚点。
