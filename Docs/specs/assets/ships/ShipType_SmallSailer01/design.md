---
document_type: asset_design_spec
schema_version: 1
asset_id: ShipType_SmallSailer01
title_zh: 小型单桅沿岸商船
title_en: Small Single-Mast Coastal Trader
working_name: SmallSailer01
former_starter_id: SHIP-0001
document_version: 2.0.0
status: REVIEW
authority: canonical
last_updated: 2026-09-11
material_card: MAT-001
current_stage: full_effect_concept
latest_decision_record: Docs/specs/assets/ships/ShipType_SmallSailer01/decisions/ADR-0010-cog-dimensions-and-caravel-progression.md
depends_on:
  - Docs/specs/systems/ship-system/ship-system.md
  - Docs/specs/assets/ships/production-rules.md
---

# ShipType_SmallSailer01 小型单桅沿岸商船

## 1. 整体设定

- 类型：单桅、单层甲板的小型沿岸商船；
- 历史原型：Cog，允许架空化调整，不要求复原具体实船；
- 用途：近海贸易、短程运输、基础探索；
- 气质：短、宽、厚实，重载倾向，不是细长快船；
- 船体长度：16m，按用户现有模型更新；不含上层建筑及外伸杆件；
- 最大船宽：约5.8m；
- 满载吃水：约2m，暂定，待模型校核；
- 满载排水量：约65t，暂定，待水下体积校核；
- 船员：标准14人，最多20人；
- 帆装：1面横帆、1根横桁；艏斜桅不另加帆面；
- 火炮：4门轻型火炮，每舷2门；
- 主桅长度：18m（桅脚至桅顶），`LOCKED`；
- 载货吨位和航速：`UNSET`。排水量包含船体、装备、人员、补给和货物，不等于载货量。
- 玩家定位：初始船，承担近岸贸易、基础探索和有限自卫。下一艘为 [Caravel](../ShipType_Caravel01/design.md)。
- 上述数值为游戏设定，不是历史实船测量值；本次不代表重新验收现有3D资产。

## 2. 整船结构设定

1. 单桅，主桅位于船体纵向中心线；
2. 一层连续主甲板，纵向水平，下方为货舱；
3. 一个紧凑货舱口，位于中轴线、主桅艉侧，不与桅座重叠；
4. 单层木质艉楼，地板与主甲板同层，屋顶为可上人平台；
5. 一套船内楼梯，紧靠右舷，从主甲板通往艉楼屋顶；
6. 中线舵；
7. 艏斜桅、主帆桁和瞭望塔保留在完整船只设计中；
8. 无木桶、绳圈和无功能甲板杂物；
9. 材质执行 MAT-001，表面干净、完整、不做旧。

## 3. 新工作流中的部件边界

### 3.1 Hull — 当前主要验证对象

Hull 包括外船壳、龙骨、艏柱、艉柱、船腹、首尾曲率、舷弧和连续舷墙。

Hull **不包含**：炮窗/炮窗开口、甲板、艉楼、楼梯、货舱口、主桅、帆桁、瞭望塔、艏斜桅、船帆、索具、舵、锚、灯、绞盘、装饰或松散道具。

当前目标是验证隔离船身能否通过 Tripo 3D 得到可编辑、可继续装配的核心模型。

### 3.2 Deck — 当前配套板件

Deck 是一块独立、简单、可手动缩放的甲板 Mesh。首轮不要求精确贴合船壳轮廓，不做桅杆孔、货舱口、楼梯或板缝几何。其作用是让用户能够在 Blender 中调整到合适高度并继续搭建船只。

### 3.3 Gunport — 后续独立逻辑部件

- 全船计划使用 4 个炮窗模块：左舷 2 个、右舷 2 个，尺寸一致、左右对应；
- 炮窗不预制在 Hull 上；
- 同一炮窗资产可以复用四次；
- 炮窗模块后续包含可见框/盖板、Blender 布尔 Cutter 和火炮安装锚点；
- 本次设计确定实际武装为4门轻型火炮，每舷2门。

### 3.4 其他部件

艉楼、楼梯、货舱口、桅杆系统、艏斜桅、舵及其他有意义部件在船身验证通过后制作。大型或复杂艉楼可以继续拆成主体墙体、屋顶平台、侧廊、窗户、栏杆和楼梯等子部件。制作前先检查部件库，已有资产优先复用。

## 4. 现行制作流程

1. 制作并批准一张完整效果概念图；
2. 根据概念图拆解部件、判断复用和制作方式；
3. 立即以 Hull 为主零件验证工作流，并补一块简单 Deck；
4. 制作或复用其他部件；
5. 在 Blender 中组装整船；
6. 导入 UE5。

整船线稿透视、整船线稿多视图、整船概念多视图和整船最终多视图不再属于本船现行流程，也不得作为新制作输入。

## 5. 当前阶段与验收

当前阶段：`Full-Effect Concept / PENDING`。

完整效果概念图通过后，只先拆出船身。船身参考资料应清楚表达侧面轮廓、顶部收窄、船首、船尾和船腹；实际交给 Tripo 的视图组合按工具当前能力选择。

船身通过条件：船型身份正确、左右无明显扭曲、首尾和船腹可用、可导入 Blender 清理，并能放置独立 Deck。若隔离船身仍不能得到可用结果，核心船身改用 Blender 制作，AI 仅保留给适合的其他部件。

## 6. UE与运行时边界

最终 UE 模块、Socket、Collision、LOD 和导出路径以 `integration.yaml` 为准。炮窗/火炮锚点不得因最终合并网格而丢失。无 Crew Socket；货物不按种类或数量生成网格。
