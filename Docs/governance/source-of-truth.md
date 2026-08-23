---
document_type: governance_policy
document_version: 0.2.0
status: REVIEW
authority: canonical
last_updated: 2026-08-23
---

# 项目权威来源规则

## 权威顺序

除用户当场明确覆盖外，依次读取：当前 Git 分支的 LOCKED 规范与 ADR、REVIEW 候选规范、规范登记的当前批准资产、机器合同、工具适配规则、临时快照、聊天与模型记忆。

船只资产额外服从 `Docs/specs/assets/ships/production-rules.md`。工具适配层不得建立第二套设计事实。

## 当前视觉权威

- 一张已批准的完整效果概念图负责锁定整船风格；
- 每个组件拥有自己的当前批准参考包和模型；
- 组件拆图只为目标组件服务，不自动成为整船几何权威；
- 旧整船线稿、旧五视图、旧共享白模和旧整船 AI 3D 输入均已退役，不得作为当前输入。

新图或模型在用户批准前只能是 `DRAFT` / `REVIEW`。被否决产物不得放入活跃权威路径。

## 变更与冲突

用户最新明确决定可以替换既有流程。替换时应更新 Markdown/YAML、记录 ADR、校验并提交 Git。明确被替换的旧流程文件可以从活跃树删除，其历史由 Git 保留；不得无授权删除仍有效的 LOCKED 设计事实。

发现冲突时指出文件和字段，按状态与版本裁定；不能访问的来源必须明确说明，禁止假称已读取。

## Cursor 入口

`.cursor/rules/ship-system.mdc` 仅为适配入口。权威正文位于 `Docs/specs`，单船事实位于目标船 `design.md` / `integration.yaml`。
