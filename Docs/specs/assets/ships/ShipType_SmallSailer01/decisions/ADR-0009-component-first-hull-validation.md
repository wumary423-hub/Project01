---
document_type: asset_decision_record
adr_id: ShipType_SmallSailer01-ADR-0009
asset_id: ShipType_SmallSailer01
status: LOCKED
date: 2026-08-23
---

# 首轮验证只制作 Hull 与简单 Deck

## Hull

Hull 是区分船型的主组件。首轮只制作连续船身、龙骨、艏艉过渡、船腹曲面和连续舷墙；不得包含炮窗、甲板、艉楼、桅杆、帆装、舵、斜桅、锚、灯、绞盘或装饰。

## Deck

另做一块简单、独立、可手动缩放和移动的 Deck，让用户在 Blender 中按需要对齐 Hull。首轮不要求复杂自动贴合。

炮窗和其他组件在 Hull 验证通过后再单独制作或复用。
