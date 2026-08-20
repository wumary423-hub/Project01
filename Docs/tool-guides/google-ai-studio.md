# Google AI Studio 使用指南

单人开发：仓库 public 读/写。允许创建、修改、新增资产档案。不需要 PR、分支审批或额外 ACL。不得删除已有规范、不得覆盖 LOCKED、不得改已发布视觉母版。概念材质卡 `MAT-*` 只用于概念图，不绑定 UE 网格材质。

## 角色

Google AI Studio 是外部设计端，与 ChatGPT 同级：

- 读 Git `docs-sync` 上的权威规范；
- 按规范做概念设计/概念图（Nano Banana）；
- 产出 `DRAFT` / `REVIEW` 候选稿。

正式项目事实仍以 Git 提交为准。Playground 通常不能 `git push`；候选文件由 Cursor 代为提交 `docs-sync`。

**不要**用 AI Studio **Build → Import GitHub** 导入本仓库。只用 Playground（Chat）+ URL context / 上传快照。

## 推荐方式：直接读 Git

1. 打开 Google AI Studio Playground。
2. 文本模型选 Gemini（Pro / Flash 等能开工具的型号）。
3. Tools 打开 **URL context**（需要时也可开 Google Search）。
4. 把下面「系统说明」贴进 System instructions，或作为该对话第一条。
5. 把对应资产读取 URL 一并贴进第一条用户消息。

GitHub 仓库：`wumary423-hub/Project01`  
分支：**`docs-sync`**  
Raw 根：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/
```

GitHub 树路径大小写以仓库为准（当前为 `Docs/`，不是 `docs/`）。

**不要因为最终目标是图片就一开始切图像模型。** 先用文本 Gemini 读完 Git、分析用户文字、识别本次目标产物及上游依赖；只有用户明确要求视觉交付时才切 Nano Banana。

## 系统说明（每次新对话粘贴）

```text
你是 Project01 的外部设计助手，运行在 Google AI Studio。
单人项目：用户明确要求的修改可以按项目治理规则执行；不要另设多人权限门禁。

权威源只有 Git 分支 docs-sync 上的文件（或本次上传的快照）。禁止用模型记忆、历史聊天或“典型帆船常识”替换规范。

仓库：wumary423-hub/Project01
分支：docs-sync
入口：先读 spec-manifest.yaml，再按 Docs/governance/tool-context-protocol.md 的顺序读下去。
船只资产制作必须读取：Docs/specs/assets/ships/production-rules.md
适配指南：Docs/tool-guides/google-ai-studio.md

每次新任务开始时，先做文字分析，先不要出图：
1. 实际读到的文件 URL / 文件名；
2. 规范 document_version 与 status；
3. LOCKED；
4. REVIEW / UNSET / 缺失；
5. 冲突；
6. source_commit（若未知，写“快照可能过期”）；
7. 判定当前是文字交流、直接改图，还是对目标产物 T 的 target-scoped “重新/重出”；
8. 若为“重新/重出”，列出被排除的旧 T，以及仍需读取的合法上游来源。

禁止：声称读了未访问的文件；私自改 LOCKED；把猜测写成程序接口或精确尺寸；因为最终目的是图片就直接出图。
候选输出状态只能是 DRAFT 或 REVIEW，不得覆盖 LOCKED 原件。

直接改图：使用用户指定图片为编辑基准，未要求整体重设计时不要主动改其他内容。
重新/重出：只排除正在被重新制作的目标产物 T 的旧版本；必须继续读取当前权威工作流规定的 T 的上游来源。不要把“重新”理解成“排除所有既有图片”。
例如：重新概念图不看旧概念图；重新线稿多视图仍应读取规则规定的线稿透视图；重新最终多视图仍应读取规则规定的概念多视图和线稿多视图。

材质卡是硬约束，不是灵感参考。材质卡没有的船只本体颜色不得自行增加；材质卡未允许的表面效果不得自行加入。
[概念图] 默认是一张定调关键图，不自动做多视图 concept sheet。
```

## 本船基础读取 URL（ShipType_SmallSailer01）

先读文字权威：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/spec-manifest.yaml
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/governance/source-of-truth.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/governance/naming-and-versioning.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/governance/tool-context-protocol.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/tool-guides/google-ai-studio.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/systems/ship-system/ship-system.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/assets/ships/production-rules.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/assets/ships/ShipType_SmallSailer01/design.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/assets/ships/ShipType_SmallSailer01/README.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/assets/ships/ShipType_SmallSailer01/integration.yaml
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/assets/ships/material-cards/MAT-001/material-card.md
```

然后根据**本次目标产物 T 的依赖关系**追加上游视觉文件：

- 如果 T 就是 `[概念图]` 且用户说“重新/重出概念图”，不要加载旧概念图/旧 Concept Master 图片。
- 如果 T 是一个按工作流必须以当前已批准 `[概念图]` 为上游来源的后续产物，则应加载当前批准概念图。
- 如果 T 是 `[概念多视图]`、`[最终多视图]` 等，按 `production-rules.md` 和当前工作流加载它们规定的上游视觉产物。
- 如果是直接改图，加载用户指定图片。

当前已归档 Concept Master URL：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/assets/ships/ShipType_SmallSailer01/concept/ShipType_SmallSailer01_concept-master_r0.8.png
```

它是否用于本次任务，不由“它是母版”自动决定，而由**它是不是目标 T 的旧版本，或 T 的合法上游来源**决定。

需要程序运行时再追加：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/systems/ship-system/ship-program.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/systems/ship-system/ship-system.yaml
```

## 退路：上传快照

URL 拉不到时，可上传上下文快照。视觉文件同样按目标 T 的依赖关系上传：排除旧 T，保留 T 的合法上游来源。

## 出图工作

- 文本 Gemini 先读 Git、分析文字并识别目标产物与依赖；用户未明确要求出图时不要切 Nano Banana。
- 直接改图：使用用户指定图片。
- 重新/重出：只排除目标产物自身旧版本，不切断工作流上游来源。
- `[概念图]` 默认只出一张定调图，不自动扩展多视图。
- 材质卡严格执行；不得补卡外船体颜色或未授权表面效果。
- 不依据聊天中被否决的图片。
- 图片通过后，由 Cursor 更新视觉修订号、SHA-256 和 ADR。
- 未通过的图片不得进入活跃权威路径。

本指南只做 Google AI Studio 适配；船只资产制作事实以 `Docs/specs/assets/ships/production-rules.md` 为权威。
