---
document_type: ship_asset_decision_record
adr_id: ShipType_SmallSailer01-ADR-0006
status: LOCKED
date: 2026-08-22
asset_id: ShipType_SmallSailer01
---

# Reference Master R1：结构参考图母版

## 用户决定

用户明确批准当前已编辑完成的结构着色图作为 `ShipType_SmallSailer01` 的**参考图母版**。

被批准的是“去除左上文字描述”之后的图像，而不是随后误触发生成的另一张图片。

源图身份：

- 当前会话源文件名：`木制帆船结构技术插画.png`
- 像素尺寸：`1449 x 1086`
- 原始 PNG SHA-256：`327d646918cfb43a3a8c6347151da0944e8c1187018f3090fa6279f19f44456b`
- 目标仓库路径：`assets/ships/ShipType_SmallSailer01/reference/ShipType_SmallSailer01_reference-master_r1.png`
- 母版修订：`R1`
- 母版状态：`LOCKED`

## 当前二进制状态

当前 GitHub 连接器只能直接创建/修改 UTF-8 文本文件，不能把本地 PNG 二进制直接提交到仓库。

因此本 ADR、`design.md`、`integration.yaml`、`spec-manifest.yaml` 与 `references/README.md` 先锁定**母版身份、目标路径和原始 SHA-256**；PNG 二进制本体标记为 `PENDING_IMPORT`。

在 PNG 实际进入仓库前：

- 不得声称仓库中已经存在该 PNG；
- 不得用另一张图替代它；
- 后续导入到目标路径的文件必须与上述源图一致，优先要求 SHA-256 完全匹配；
- 如果因格式转换无法保持 PNG 字节完全一致，必须创建新的修订和新 SHA，不得静默替换 R1。

## Reference Master R1 的职责

R1 是**船体/甲板/艉部基础结构参考母版**，用于约束后续需要读取该上游来源的结构设计工作。

它锁定/确认以下用户已经明确指定的结构关系：

1. 艉楼为**单层木质艉楼**；艉楼地板与主甲板处于同一层级；艉楼屋顶是可上人的平台并设栏杆。
2. 艉楼楼梯只有一套，位于船体内部并靠一侧船舷；下端落在主甲板，上端到达艉楼屋顶平台；不得放在船体外侧或中轴线上。
3. 主甲板货舱口只有一个；尺寸收缩为不会占满主甲板的紧凑尺度；货舱口与主桅/桅座不得重叠。
4. 全船炮窗仍为四个、每舷两个、沿纵向中心线镜像；四个炮窗尺寸统一。
5. 艉楼木材色彩与船体木材保持同一材质体系。
6. R1 为结构阅读主动去除了索具与帆；保留主桅、帆桁与瞭望塔。**索具/帆的缺失只代表本参考母版的简化展示，不等于最终船只永久禁止索具或帆。**
7. 图内不保留标题、说明框或其他文字。

## 与旧 Concept Master 的关系

V0.8 Concept Master 继续作为已有的历史视觉版本记录，不被本 ADR 删除。

R1 是新增的结构参考母版，不等同于把 V0.8 Concept Master 直接覆盖或删除。后续任务是否读取 R1 或 V0.8，仍按全局 `production-rules.md` 的目标产物/上游依赖规则判断。

## 后果

- `design.md` 升级并同步上述结构事实；
- `integration.yaml` 同步单层艉楼、内部楼梯、紧凑货舱口与等尺寸炮窗约束；
- `spec-manifest.yaml` 登记 Reference Master R1；
- `references/README.md` 增加 R1 索引；
- PNG 二进制导入完成前保持 `PENDING_IMPORT`，不得假称已上传。
