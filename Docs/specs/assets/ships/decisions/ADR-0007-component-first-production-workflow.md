---
document_type: ship_asset_production_decision_record
adr_id: SHIP-ASSET-ADR-0007
status: LOCKED
date: 2026-08-23
scope: all_ship_assets
supersedes: whole_ship_multiview_pipeline
---

# 船只资产改为组件优先工作流

## 决定

1. 先用一张完整效果概念图锁定整船风格。
2. 根据该图拆分需要单独建模的组件；复杂组件可以继续递归拆分。
3. 每个组件单独设计、生成、清理与验收，优先复用既有组件。
4. 在 Blender 中组装，通过后进入 UE5。
5. 旧“线稿透视图 → 线稿多视图 → 概念多视图 → 最终多视图 → 整船 AI 3D”流程退役，不得作为有效依赖。

当前验证从 Hull 开始，并配一块可手动缩放对齐的独立 Deck。炮窗属于独立逻辑模块，不做进 Hull。
