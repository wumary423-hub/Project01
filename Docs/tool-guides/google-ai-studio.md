# Google AI Studio 使用指南

单人开发：仓库 public 读/写。允许创建、修改、新增资产档案。不需要 PR、分支审批或额外 ACL。不得删除已有规范、不得覆盖 LOCKED、不得改已发布视觉母版。概念材质卡 `MAT-*` 只用于概念图，不绑定 UE 网格材质。

## 角色

Google AI Studio 是外部设计端，与 ChatGPT 同级：

- 读 Git `docs-sync` 上的权威规范；
- 按规范做概念设计/概念图（Nano Banana）；
- 产出 `DRAFT` / `REVIEW` 候选稿。

正式项目事实仍以 Git 提交为准。Playground 通常不能 `git push`；候选文件由 Cursor 代为提交 `docs-sync`。

**不要**用 AI Studio **Build → Import GitHub** 导入本仓库。那会把 UE 工程当 Web App，并可能另建仓库。只用 Playground（Chat）+ URL context / 上传快照。

## 推荐方式：直接读 Git

1. 打开 Google AI Studio Playground。
2. 文本模型选 Gemini（Pro / Flash 等能开工具的型号）。
3. Tools 打开 **URL context**（需要时也可开 Google Search）。
4. 把下面「系统说明」贴进 System instructions，或作为该对话第一条。
5. 把对应资产读取 URL 一并贴进第一条用户消息。

GitHub 仓库：`wumary423-hub/Project01`  
分支：**`docs-sync`**（不要用 `dev/widepath-nav` 做设计同步）  
Raw 根：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/
```

GitHub 树路径大小写以仓库为准（当前为 `Docs/`，不是 `docs/`）。

**不要因为最终目标是图片就一开始切图像模型。** 先用文本 Gemini 读完 Git、分析当前用户文字、判定操作模式；只有用户明确要求视觉交付时才切 Nano Banana。

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
Cursor 适配层不是权威正文：.cursor/rules/ship-system.mdc 只指向 Docs/specs。

每次新任务开始时，先做文字分析，先不要出图：
1. 实际读到的文件 URL / 文件名；
2. 规范 document_version 与 status；
3. LOCKED；
4. REVIEW / UNSET / 缺失；
5. 冲突；
6. source_commit（若未知，写“快照可能过期”）；
7. 判定当前是文字交流、直接改图，还是 clean-slate 的“重新/重出”；
8. 说明当前是否允许读取既有视觉母版。

禁止：声称读了未访问的文件；私自改 LOCKED；把猜测写成程序接口或精确尺寸；因为最终目的是图片就直接出图。
候选输出状态只能是 DRAFT 或 REVIEW，不得覆盖 LOCKED 原件。

直接改图：使用用户指定图片为编辑基准，未要求整体重设计时不要主动改其他内容。
重新/重出：只读取当前权威文字规则、目标资产文字设计、当前材质卡和本次用户要求；不得读取上一版概念图/视觉母版图片作为生成输入，不使用历史提示词、旧 brief、被否决图片或模型记忆。
只有用户明确说“基于母图修改/参考上一版/在这张图上改”时，才允许读取指定旧图。

材质卡是硬约束，不是灵感参考。材质卡没有的船只本体颜色不得自行增加；材质卡未允许的表面效果不得自行加入。
[概念图] 默认是一张定调关键图，不自动做多视图 concept sheet。
```

## 本船读取 URL（ShipType_SmallSailer01）

单次 URL context 约 20 个上限。先贴这一组：

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
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/assets/ships/ShipType_SmallSailer01/decisions/ADR-0001-concept-master-r0.8.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/assets/ships/ShipType_SmallSailer01/decisions/ADR-0002-hull-focused-workflow.md
```

**视觉母版 URL 不再默认放入首轮读取。** 只有直接改图或用户明确要求参考母版时，再追加：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/assets/ships/ShipType_SmallSailer01/concept/ShipType_SmallSailer01_concept-master_r0.8.png
```

如果用户要求“重新/重出”，不要追加该视觉母版 URL。

需要程序运行时再追加：

```text
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/systems/ship-system/ship-program.md
https://raw.githubusercontent.com/wumary423-hub/Project01/docs-sync/Docs/specs/systems/ship-system/ship-system.yaml
```

`Docs/Ship/SmallSailer01.md` 与 `Docs/Ship/ShipAssetContract.md` 为 SUPERSEDED，不要当权威正文。

## 退路：上传快照

URL 拉不到时：

```bash
python tools/export_context.py ShipType_SmallSailer01 --target google-ai-studio
```

上传上下文快照。**视觉母版是否上传仍取决于操作模式：** 直接改图/明确参考时上传；“重新/重出”时不要上传旧母版。  
上传文件是快照，不是新的权威分支；在对话里记录日期，commit 未知则写可能过期。

## 出图工作

- 文本 Gemini 先读 Git、分析文字并判定操作模式；用户未明确要求出图时不要切 Nano Banana。
- 直接改图：使用用户指定图片。
- 重新/重出：不读旧概念图/视觉母版图片，只按当前文字规则与材质卡生成。
- `[概念图]` 默认只出一张定调图，不自动扩展多视图。
- 材质卡严格执行；不得补卡外船体颜色或未授权表面效果。
- 不依据聊天中被否决的图片。
- 图片通过后，由 Cursor 更新视觉修订号、SHA-256 和 ADR。
- 未通过的图片不得进入活跃权威路径。

## 回写 Git

- 候选 Markdown / 图交给用户或 Cursor 提交 `docs-sync`。
- 改 sockets、命名、Validate、目录或 V0.x 合同后，使用 `.cursor/rules/agent-workflow.mdc` 里的同步通知块（GPT 与 Gemini 共用）。
- 不要用 Build 双向 GitHub Sync 推整个游戏工程。

本指南只做 Google AI Studio 适配；船只资产制作事实以 `Docs/specs/assets/ships/production-rules.md` 为权威，不在本文件维护第二套冲突规则。
