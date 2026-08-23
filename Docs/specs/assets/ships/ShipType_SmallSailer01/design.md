---
document_type: asset_design_spec
schema_version: 1
asset_id: ShipType_SmallSailer01
title_zh: 小型单桅沿岸商船
title_en: Small Single-Mast Coastal Trader
working_name: SmallSailer01
former_starter_id: SHIP-0001
document_version: 0.1.8
status: REVIEW
authority: canonical
last_updated: 2026-08-23
visual_master:
  revision: "0.8"
  status: LOCKED
  file: assets/ships/ShipType_SmallSailer01/concept/ShipType_SmallSailer01_concept-master_r0.8.png
  sha256: 0c848da018e5c4ebe1edc65611d9b46a2e6633a09430aba8af80ccbf01bfe44d
reference_master:
  revision: "1"
  status: LOCKED
  role: hull_deck_stern_structural_reference
  intended_file: assets/ships/ShipType_SmallSailer01/reference/ShipType_SmallSailer01_reference-master_r1.png
  source_session_filename: 木制帆船结构技术插画.png
  source_dimensions_px: [1449, 1086]
  source_sha256: 327d646918cfb43a3a8c6347151da0944e8c1187018f3090fa6279f19f44456b
  binary_repository_status: PENDING_IMPORT
  decision_record: Docs/specs/assets/ships/ShipType_SmallSailer01/decisions/ADR-0006-reference-master-r1.md
depends_on:
  - docs/specs/systems/ship-system/ship-system.md
---

# ShipType_SmallSailer01 小型单桅沿岸商船设计规范

程序目录行与规范主键均为 **`ShipType_SmallSailer01`**。工作名 `SmallSailer01` 仅用于网格文件名前缀。旧启动包 ID `SHIP-0001` 已废止，不再作主键。

## 1. 来源与边界

本规范同时维护：

- V0.8 Concept Master：已有概念视觉版本记录；
- Reference Master R1：当前批准的船体/甲板/艉部基础结构参考母版；
- 已迁入 `ship-system.md` / `integration.yaml` 的程序接口（原 `.mdc` V0.1.1）。

Reference Master R1 当前已由用户批准并以 SHA-256 锁定身份，但 PNG 二进制尚未进入 Git；在导入前不得假称仓库中已经存在该 PNG，也不得用其他图片替换。

## 2. 资产定位

### 已确认

- 单桅小型沿岸商船；
- **以 Cog (ship) 为历史原型**；允许架空化设计调整，但总体船体技术语言、商船体量与结构逻辑以 Cog 为历史原型；
- 宽体、厚实、重载倾向；
- 近海贸易、短程运输、基础探索；
- 架空的 15 至 17 世纪欧洲航海技术语言；
- 不要求一比一复原某一艘具体历史实船；
- **船长固定为 15m**；
- **主桅长度固定为 18m**，从桅脚到桅顶计。

### 尚未锁定（不得自行填进程序合同）

- 精确船宽、吃水、排水量；
- 精确船员数量、货舱容量、航速、实际安装武装数量；炮窗结构数量已锁定为 4 个，但不等同于锁定 4 门火炮；
- 首发默认主 RigType（Square vs Lateen）。

## 3. 视觉与结构参考母版

### 3.1 V0.8 Concept Master — LOCKED

```text
assets/ships/ShipType_SmallSailer01/concept/ShipType_SmallSailer01_concept-master_r0.8.png
```

SHA-256：

```text
0c848da018e5c4ebe1edc65611d9b46a2e6633a09430aba8af80ccbf01bfe44d
```

锁定内容：单桅大横帆身份；短宽厚实比例；船艏—中段与中段—船尾的个性过渡；左前 3/4；木质船体与低饱和灰白帆布材质方向。不得把船首船尾修平。

### 3.2 Reference Master R1 — LOCKED / binary PENDING_IMPORT

用户批准源图：

```text
木制帆船结构技术插画.png
```

目标仓库路径：

```text
assets/ships/ShipType_SmallSailer01/reference/ShipType_SmallSailer01_reference-master_r1.png
```

源图尺寸：`1449 x 1086`  
源 PNG SHA-256：

```text
327d646918cfb43a3a8c6347151da0944e8c1187018f3090fa6279f19f44456b
```

当前 GitHub 连接器不能直接提交 PNG 二进制，因此目标路径暂未实际存在；母版身份先由文件名、尺寸与 SHA-256 锁定。二进制导入规则见 `decisions/ADR-0006-reference-master-r1.md`。

R1 的职责是提供船体、甲板、艉楼、楼梯、主桅/帆桁/瞭望塔、炮窗与货舱口的结构参考。为了结构阅读，R1 主动省略索具和帆；该省略**不等于最终船只永久禁止索具或帆**。

后续任务是否读取 R1，服从全局 `production-rules.md` 的目标产物与上游依赖规则；如果“重新”制作的目标本身就是 R1，则不得用旧 R1 作为输入。

### 3.3 Shared Geometry Blockout — APPROVED

本机共享白模（几何与正交相机已批准；`.blend` 通常只留本机，不以二进制进 Git）：

```text
assets/ships/ShipType_SmallSailer01/blender/ShipType_SmallSailer01_blockout.blend
```

SHA-256：

```text
7ef92e5dcbf32ba4592731495ba6acb27e476b4f0011898c00f3b8fa47d113a4
```

正交相机与取景基准随 docs-sync commit `395dba69a46ac050fb2a612203e3341458b8748c` 批准：顶 / 左舷 / 右舷 / 船首 / 船尾，统一 `ortho_scale = 48.50`。不得分别缩放单视图。该白模用于结构审核与辅助作图；不是 UE mesh。

### 3.4 `[线稿多视图]` Work R2 — DRAFT

候选路径：

```text
assets/ships/ShipType_SmallSailer01/line-multiview/candidates/work-r2/
```

五张图由同一份已批准 `.blend` 与批准正交相机机械渲染（`--line-ortho`），不是五次独立生图。Work R1 已整体 `REJECTED`，不得复用。Work R2 在用户确认前不得成为下游权威输入。

## 4. 观察距离（不冲突）

- **常规游戏镜头：50–200m** — 决定什么值得做成可读几何。
- **极限近距：约 10m** — 仍应能认出是同一艘船，不得明显破模或比例错误。

优先级：桅数 > 甲板层 > 帆装轮廓 > 船体轮廓 > 大件 > 小装饰。

## 5. 当前结构约束（V1 Hull-Focused Concept）

1. 主桅结构与视觉均在船体纵向中心线；
2. **船长固定为 15m；主桅长度固定为 18m（桅脚至桅顶）**；
3. 取消船尾布料顶棚；
4. 艉楼为**低矮明确的单层木质艉楼**；艉楼地板与主甲板处于同一层级；艉楼屋顶为可上人的平台，四周设置栏杆；
5. 主甲板到艉楼屋顶平台只设置**一套木质楼梯**；楼梯必须位于**船体内部**并靠**右舷**布置，不得居中；楼梯下端落在主甲板、艉楼前方，上端到达艉楼屋顶平台；不得做成左右对称双楼梯；不得埋入实体艉楼内部；
6. 艉楼只设置少量小型功能窗，不做豪华大窗；艉楼木材与船体木材保持同一材质/色彩体系；
7. 删除木桶、绳圈、无功能杂物；
8. **货舱口只设置 1 个**；尺寸保持紧凑，不得占满或主导主甲板；可由多块盖板组成但必须读成一个货舱口；货舱口位于主甲板且平面位置**不得与主桅/桅座重叠**；
9. 船尾中线舵；
10. 外侧深色带读成木质护舷材，不是金属框架；
11. 清除艏斜桅根部的炮管/机械圆筒歧义；
12. Hull Concept 不用展开大帆；帆可省略或收帆；Reference Master R1 为结构阅读完全省略索具和帆，但保留帆桁与瞭望塔；
13. 视觉重点回到船体、甲板、艉楼和船舵；
14. 炮窗为固定的船体结构特征：全船总计 **4 个**，左舷 **2 个**、右舷 **2 个**，不得增减；
15. **炮窗以船体纵向中心线为镜像轴，两舷镜像对应分布**；
16. **炮窗位于顶层甲板对应的舷侧区域**，不得下移到其他甲板层级；
17. **四个炮窗尺寸必须统一**；同一舷及两舷对应炮窗不得出现大小不一致；
18. 炮窗数量只锁定船体结构开口，不自动锁定实际安装武器/火炮数量。

## 6. 不得改变

不得改为多桅、细长快船、豪华艉楼城堡、删除艏斜桅、改成现代小艇轮廓、用 Meshy 反向改锁定轮廓、堆装饰武器杂物、改成另一艘船。

不得把艉楼重新变成两层结构；不得把艉楼楼梯移到船体外侧；不得把唯一货舱口放大到占据大部分主甲板；不得让四个炮窗尺寸不一致。

## 7. 模块（启动包表格格式 + 程序 MastRig 整包）

**UE 最终交付（功能导向，Cursor）：**

| 模块 | 独立网格 | 说明 |
|------|----------|------|
| Hull | 是 | `AFleet` 根；`FShipDefinition.Mesh` |
| SternSuperstructure | 否 | v0 焊在 Hull 上；单层艉楼，屋顶为可上人平台 |
| MastRig_01 | 是，整包 | 桅+桁+帆+少量索具；**不是**独立的 Mast/Yard/Sail 三件 UE 网格 |
| Headsail_01 | 是 | 首发不装网格；Hull 保留 socket |
| Rudder / Flag / Figurehead / Anchor / MastBroken | 是 | 见 `integration.yaml` |

**Meshy 毛坯（美术导向）** 可以按船体、艉楼、桅杆体块分件生成。Blender 必须打成上表的 UE 模块，其中帆装为 MastRig 整包 × RigType × Full/Half/Furled。

一期生产：Square + Lateen 各三状态（六件）。Gaff 仅设计兼容。

旗接口 **`Attach_Flag` 在 MastRig 网格上，不在 Hull 上。**

## 8. Meshy / Blender / UE5

Meshy：Hull Base；无展开帆；简化索具；删杂物；保留锁定结构关系。

Blender：对称、拓扑、Pivot、UV、按上表拆模块、+X forward、Apply Rotation+Scale。

UE：`/Game/Ships/ShipType_SmallSailer01/`。Socket 在 UE Static Mesh Editor 添加。无 Crew Socket。货物不按种类/数量生成网格。

2D 改装图：船头朝左；2048×1024；透明；无烘焙热区；槽位 `OutfitSlot_*`。

## 9. V1 验收

以 Cog (ship) 为历史原型；保持短宽厚实船体与首尾个性过渡；**船长 15m；主桅居中且长度 18m**；艉楼为单层、地板与主甲板同层、屋顶为可上人平台；楼梯只有一套、位于船体内部右舷、艉楼前方、下端在主甲板、上端到艉楼屋顶；货舱口只有一个、尺寸紧凑且不与主桅/桅座重叠；全船四个炮窗、每舷两个、沿纵向中心线镜像、位于顶层甲板对应舷侧区域且尺寸一致；中线舵；无木桶杂物；无 AI 歧义结构。
