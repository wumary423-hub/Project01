# ChatGPT 项目使用指南

与 Google AI Studio 共用 Git 分支 `docs-sync`。Studio 适配见 `docs/tool-guides/google-ai-studio.md`。

## 推荐方式

优先通过 GitHub连接读取指定仓库和 commit。

若使用项目上传文件：

- 上传 `spec-manifest.yaml`；
- 上传相关 Markdown/YAML；
- 上传被规范引用的视觉母版；
- 在项目说明中记录来源 commit；
- 上传文件视为快照，不是新的权威分支。

## 每次新对话

先要求模型：

1. 列出实际可访问文件；
2. 报告规范版本、状态和 commit；
3. 列出 LOCKED、REVIEW、UNSET；
4. 不可访问的文件必须明确说明；
5. 不得假称读取了不存在的独立文件。

## 出图工作

- 以 `design.md` 中引用的视觉母版为唯一编辑母版；
- 不依据聊天中被否决的图片；
- 图片通过后更新视觉修订号、SHA-256 和 ADR；
- 未通过的图片不得进入活跃权威路径。
