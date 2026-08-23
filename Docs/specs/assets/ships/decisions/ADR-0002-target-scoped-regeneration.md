---
document_type: ship_asset_production_decision_record
adr_id: SHIP-ASSET-ADR-0002
status: LOCKED
date: 2026-08-21
scope: all_ship_assets
---

# “重新”只重置目标产物

用户要求重新制作目标产物 `T` 时，不使用 `T` 自身的旧图片、旧提示词或被否决版本；仍读取当前工作流规定的合法上游来源。

在组件优先工作流中：

- 重新做完整效果概念图：读取船型设定与材质卡，不读取旧完整效果概念图；
- 重新做船身拆图：读取已批准完整效果概念图与 Hull 合同，不读取旧船身拆图；
- 重新生成 Hull：读取已批准船身参考包，不读取旧 Hull 模型；
- 重新做某个复用部件：只重置该部件，不影响 Hull、Deck 或其他已批准部件。

用户明确要求“在上一版上改”时，按直接编辑执行。
