---
document_type: tool_adapter
tool: tripo_3d
status: ACTIVE
last_updated: 2026-08-23
---

# Tripo 3D 使用指南

Tripo 3D 按组件生成，不再接收旧整船最终多视图。正式输入是目标组件当前已批准、结构一致的参考包；输出只是毛坯，必须进入 Blender 清理。

## 当前验证：Hull

- 只生成连续船身、龙骨、艏艉过渡、船腹和连续舷墙；
- 不含 Deck、炮窗、艉楼、舱口、楼梯、桅杆、帆装、舵、斜桅、锚、灯、绞盘和装饰；
- 输出到 `assets/ships/ShipType_SmallSailer01/tripo3d/hull/`；
- 参考图数量与上传限制以当时 Tripo 界面为准，不能因此改写组件合同。

Deck 首轮由 Blender 制作简单独立板，不交给 Tripo。Tripo 输出不得直接作为 UE5 最终资产，也不得反向覆盖完整效果概念或设计规范。
