---
document_type: governance_policy
document_version: 0.1.2
status: REVIEW
authority: canonical
last_updated: 2026-08-20
---

# 项目权威来源规则

## 1. 目的

本规则用于确保 Cursor、ChatGPT、Google AI Studio、Meshy、Blender、UE5 以及未来加入的工具读取同一套项目事实，避免聊天记忆、工具私有规则和重复文件互相冲突。

## 2. 权威层级

在不存在用户当场明确覆盖指令的情况下，按以下优先级判断：

1. 当前 Git 分支中状态为 `LOCKED` 的规范及其已提交 ADR；
2. 当前 Git 分支中状态为 `REVIEW` 的规范，用于候选实现，不得覆盖 `LOCKED` 内容；
3. 被规范明确引用且状态为 `LOCKED` 的视觉母版、模型或数据文件；
4. 机器可读合同；
5. 工具适配规则；
6. ChatGPT / Google AI Studio 上传或导出的快照；
7. 聊天记录、摘要、模型记忆和临时提示词。

工具适配规则、聊天记录和模型记忆不得单独修改项目事实。

## 3. 用户的即时指令

用户在当前工作会话中的最新明确指令可以创建一个候选变更，并暂时覆盖旧要求以完成本次工作。但是，该变更只有在以下步骤完成后才成为跨工具的正式项目事实：

1. 更新相应 Markdown/YAML；
2. 记录变更原因或 ADR；
3. 通过校验；
4. 提交 Git；
5. 对 `LOCKED` 内容的修改必须获得用户明确批准。

## 4. 视觉权威

视觉资源只有在设计规范中被明确引用，并带有版本、状态、路径和校验值时，才属于正式视觉母版。

示例：

- `ShipType_SmallSailer01` 的 V0.8 Concept Master 为 `LOCKED`；
- 被否决的生成图不得放入活跃规范路径；
- 新图在用户批准前只能标记为 `DRAFT` 或 `REVIEW`。

## 5. 不可访问来源

任何工具不得声称已读取当前不可访问的文件、图片、仓库或聊天。

如果引用文件不存在、未挂载或无法读取，工具必须：

1. 明确说明无法访问；
2. 列出已实际读取的来源；
3. 不使用常识或记忆悄悄填补缺失原文；
4. 对缺失内容创建迁移或核对任务。

## 6. 冲突处理

发现冲突时不得自行“综合”成新规则。应当：

1. 指出冲突文件和具体字段；
2. 判断各自状态和版本；
3. 说明影响；
4. 提出候选解决方式；
5. 等待用户批准后再修改权威规范。

## 7. Git 读写（Single Developer Mode）

仓库默认 public 读 / public 写。规范与资产档案允许创建、修改、新增。不采用多人团队权限模型（无强制 PR、无分支审批）。

不得删除已有规范；不得覆盖 `LOCKED` 原文；不得在未要求时改已发布资产定义。

概念材质卡（`MAT-*`）只服务概念图，不是 UE 网格材质权威。

## 8. Cursor 船只规则

`.cursor/rules/ship-system.mdc` 是适配入口。权威正文：

- `docs/specs/systems/ship-system/ship-system.md`（LOCKED）
- `docs/specs/systems/ship-system/ship-program.md`（LOCKED）
- 单船 `integration.yaml` / `design.md`

旧全文保留在该 `.mdc` 的 Git 历史中。
