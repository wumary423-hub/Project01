---
document_type: asset_design_spec
schema_version: 1
asset_id: MAT-001
title_zh: 船只概念材质卡
document_version: 0.1.0
status: REVIEW
authority: canonical
scope: concept_art_look_card
last_updated: 2026-08-20
depends_on:
  - docs/specs/assets/ships/ShipType_SmallSailer01/design.md
source_label: 游戏船只资产
---

# MAT-001 船只概念材质卡

本卡只服务**概念图**。不定义 UE Material、不定义游戏网格 PBR、不进入 `Content/Materials/`。

## 1. 材质设计方向

与 `ShipType_SmallSailer01` V0.8 Concept Master 同一套工作船气质：

- 架空的 15–17 世纪欧洲航海技术语言；
- 木质船体，旧、厚、可用，不是豪华漆面；
- 旧帆布方向（本卡不负责展开帆的结构，只负责布面读感）；
- 外侧深色带读成**木质护舷材**，不是金属框架。

不得改成：现代复合材料、高光金属船壳、塑料感、珠宝漆、科幻合金。

## 2. 视觉目标

概念图里同一艘船的木材、帆布、护舷在多张图之间可认作同一套表面，而不是每张图换一套材质世界观。

观察距离与船规范一致：常规 50–200m 可读大块材质；约 10m 仍是木头/帆布，不要靠微型铆钉撑细节。

## 3. 使用场景

| 用 | 不用 |
|----|------|
| ChatGPT / Google AI Studio（Nano Banana）概念图、Hull-Focused 修正图 | UE `M_` / MIC / 纹理导入 |
| 保持与 V0.8 母版同一材质语言 | Meshy / Blender 游戏网格材质槽 |
| 后续船只概念图若声明沿用本卡 | 程序合同、socket、DataTable |

## 4. 已确认参数

仅收录船设计里**已经写出**的定性事实。未提供的数值不编造。

| 参数 | 值 | 状态 |
|------|----|------|
| 船体主表面 | 木质 | 已确认（随 V0.8） |
| 帆面方向 | 旧帆布 | 已确认（随 V0.8） |
| 外侧深色带 | 木质护舷材，非金属 | 已确认（随 V0.8） |
| 色号 / HEX | — | `UNSET` |
| 粗糙度 / 金属度数值 | — | `UNSET` |
| 法线 / 粗糙度贴图路径 | — | `UNSET`（本卡不引用游戏贴图） |
| UE Material / MIC | 不适用 | 见 `integration.yaml` |

来源文件「游戏船只资产」未作为仓库内独立文件入库；若后续补上概念材质卡图，再写入路径、修订号和 SHA-256，状态在批准前保持 `REVIEW`。
