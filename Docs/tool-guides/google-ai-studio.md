# Google AI Studio 使用指南

Google AI Studio 读取 `docs-sync` 的 Git 权威文件，只产出 `DRAFT` / `REVIEW` 候选。先用文本模型读取 `spec-manifest.yaml`、治理规则、船只系统、`production-rules.md`、目标船 `design.md`、材质卡与 `integration.yaml`，用户明确要求视觉交付后才出图。

当前流程是：完整效果概念图 → 组件拆分 → 逐组件制作/复用 → Blender 组装 → UE5。不要加载或重建已退役的整船线稿、正交五视图、共享白模或整船最终多视图。

`ShipType_SmallSailer01` 当前先等待一张完整效果概念图；随后只拆 Hull 参考，生成连续船身。简单 Deck 独立制作，炮窗及其他附件不属于 Hull。

Raw 根：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/
```

候选经用户确认后由程序侧更新路径、SHA-256、ADR 和 Git。无法访问的文件必须报告，不得用模型记忆补全。
