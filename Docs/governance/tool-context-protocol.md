---
document_type: governance_policy
document_version: 0.1.3
status: REVIEW
authority: canonical
last_updated: 2026-08-20
---

# 工具上下文协议

## 1. 所有工具的读取入口

开始任务时按顺序读取：

1. `spec-manifest.yaml`
2. `docs/governance/source-of-truth.md`
3. 对应系统规范
4. 对应资产类型的全局制作规则（船只资产：`Docs/specs/assets/ships/production-rules.md`）
5. 对应资产 `design.md`
6. 当前任务需要的材质卡（若指定/绑定）
7. 对应 `integration.yaml`
8. 规范中引用的视觉、模型或数据文件——**仅在当前操作模式允许时读取**
9. 工具自己的适配指南

船只资产任务在读取视觉文件前，必须先根据 `production-rules.md` 判定是：文字交流、直接改图，还是 clean-slate 的“重新/重出”。

## 2. 任务开始时的最小报告

工具应简要说明：

- 实际读取的文件；
- 当前规范版本与状态；
- 当前视觉/资产版本；
- `LOCKED` 内容；
- `UNSET` 或迁移未完成内容；
- 是否检测到冲突或缺失；
- 当前操作模式，以及是否允许读取既有视觉母版。

对多数文字讨论，不要求为了报告而加载图片，也不得自动出图。

## 3. 上下文快照

ChatGPT、Google AI Studio 或其他外部工具使用上传文件时，应记录：

```yaml
source_repository: wumary423-hub/Project01
source_branch: docs-sync
source_commit: <commit>
snapshot_date: YYYY-MM-DD
```

如果 commit 无法确认，必须说明该快照可能过期。

## 4. 输出要求

每项工具输出至少携带：

- `asset_id` 或 `system_id`；
- 来源规范版本；
- 来源 commit（可用时）；
- 输出版本；
- 状态；
- 与规范的偏差列表。

视觉生成前还必须确认：

- 用户是否真的要求生成图片；
- 是直接改图还是重新生成；
- 当前材质卡是否已实际读取；
- 是否存在材质卡外颜色或其他模型自行补充项。

## 5. 禁止行为

- 以模型记忆替代文件；
- 声称读取未访问的文件；
- 私自修改 LOCKED 内容；
- 删除已有规范；
- 在工具私有规则中复制并长期维护第二套权威事实；
- 通过“看起来合理”填补程序接口或尺寸字段；
- 因为最终目标是视觉资产就跳过文字分析直接出图；
- 在“重新/重出”任务中读取上一版概念图/视觉母版图片作为生成输入；
- 把历史提示词、被否决图片或助手旧描述当作制作规则；
- 把材质卡当作可自由偏离的灵感参考。

## 6. Git 档案写入（Single Developer Mode）

默认允许：创建文件、修改非 LOCKED 文件、新增资产档案。  
不需要 PR、分支审批或额外 ACL。  
改 `LOCKED` 或已发布视觉母版仍须用户明确批准。
