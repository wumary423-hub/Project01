---
document_type: asset_design_spec
schema_version: 1
asset_id: ShipType_SmallSailer01
title_zh: 小型单桅沿岸商船
title_en: Small Single-Mast Coastal Trader
working_name: SmallSailer01
former_starter_id: SHIP-0001
document_version: 0.1.4
status: REVIEW
authority: canonical
last_updated: 2026-08-21
visual_master:
  revision: "0.8"
  status: LOCKED
  file: assets/ships/ShipType_SmallSailer01/concept/ShipType_SmallSailer01_concept-master_r0.8.png
  sha256: 0c848da018e5c4ebe1edc65611d9b46a2e6633a09430aba8af80ccbf01bfe44d
depends_on:
  - docs/specs/systems/ship-system/ship-system.md
---

# ShipType_SmallSailer01 小型单桅沿岸商船设计规范

程序目录行与规范主键均为 **`ShipType_SmallSailer01`**。工作名 `SmallSailer01` 仅用于网格文件名前缀。旧启动包 ID `SHIP-0001` 已废止，不再作主键。

## 1. 来源与边界

本规范依据 V0.8 Concept Master，以及已迁入 `ship-system.md` / `integration.yaml` 的程序接口（原 `.mdc` V0.1.1）。

## 2. 资产定位

### 已确认

- 单桅小型沿岸商船；
- **以 Cog (ship) 为历史原型**；允许架空化设计调整，但总体船体技术语言、商船体量与结构逻辑以 Cog 为历史原型，不要求一比一复原某一艘具体历史船；
- 宽体、厚实、重载倾向；
- 近海贸易、短程运输、基础探索；
- 架空的 15 至 17 世纪欧洲航海技术语言；
- 不要求严格复原单一历史船型。

### 尚未锁定（不得自行填进程序合同）

- 精确船长、船宽、吃水、排水量（概念约 **15m**，无程序硬校验）；
- 精确船员数量、货舱容量、航速、实际安装武装数量；炮窗结构数量已锁定为 4 个，但不等同于锁定 4 门火炮；
- 首发默认主 RigType（Square vs Lateen）。

## 3. V0.8 Concept Master：LOCKED

```text
assets/ships/ShipType_SmallSailer01/concept/ShipType_SmallSailer01_concept-master_r0.8.png
```

SHA-256（文件内容，改名后不变）：

```text
0c848da018e5c4ebe1edc65611d9b46a2e6633a09430aba8af80ccbf01bfe44d
```

锁定内容：单桅大横帆身份；短宽厚实比例；船艏—中段与中段—船尾的个性过渡；左前 3/4；木质船体与低饱和灰白帆布材质方向。不得把船首船尾修平。

## 4. 观察距离（不冲突）

- **常规游戏镜头：50–200m** — 决定什么值得做成可读几何。
- **极限近距：约 10m** — 仍应能认出是同一艘船，不得明显破模或比例错误。

优先级：桅数 > 甲板层 > 帆装轮廓 > 船体轮廓 > 大件 > 小装饰。

## 5. 当前必须修正（V1 Hull-Focused Concept）

1. 主桅结构与视觉均在船体纵向中心线；
2. **主桅长度必须严格大于船长：`mast_length > ship_length`。** 这是相对尺寸硬约束；在船长绝对值尚未锁定时，不得自行把概念约 15m 转成新的绝对主桅尺寸规则；
3. 取消船尾布料顶棚；
4. 低矮明确的木质两层艉楼；
5. 主甲板到艉楼平台只设置**一套木质楼梯**；楼梯必须**靠边贴一侧船舷布置，不得居中**，具体采用左舷还是右舷尚未锁定；不得做成左右对称双楼梯；
6. 少量小型功能窗，不做豪华大窗；
7. 删除木桶、绳圈、无功能杂物；
8. **货舱口只设置 1 个**，可由多块盖板组成但必须读成一个大型货舱口；货舱口的平面位置**不得与主桅/桅座位置重叠**；
9. 船尾中线舵；
10. 外侧深色带读成木质护舷材，不是金属框架；
11. 清除艏斜桅根部的炮管/机械圆筒歧义；
12. Hull Concept 不用展开大帆；帆省略或收帆；
13. 视觉重点回到船体、甲板、艉楼和船舵；
14. 炮窗为固定的船体结构特征：全船总计 **4 个**，左舷 **2 个**、右舷 **2 个**，不得增减；
15. **炮窗以船体纵向中心线为镜像轴，两舷镜像对应分布**；
16. **炮窗位于顶层甲板对应的舷侧区域**，不得下移到其他甲板层级；
17. 炮窗数量只锁定船体结构开口，不自动锁定实际安装武器/火炮数量。

## 6. 不得改变

不得改为多桅、细长快船、豪华艉楼城堡、删除艏斜桅、改成现代小艇轮廓、用 Meshy 反向改锁定轮廓、堆装饰武器杂物、改成另一艘船。

## 7. 模块（启动包表格格式 + 程序 MastRig 整包）

**UE 最终交付（功能导向，Cursor）：**

| 模块 | 独立网格 | 说明 |
|------|----------|------|
| Hull | 是 | `AFleet` 根；`FShipDefinition.Mesh` |
| SternSuperstructure | 否 | v0 焊在 Hull 上 |
| MastRig_01 | 是，整包 | 桅+桁+帆+少量索具；**不是**独立的 Mast/Yard/Sail 三件 UE 网格 |
| Headsail_01 | 是 | 首发不装网格；Hull 保留 socket |
| Rudder / Flag / Figurehead / Anchor / MastBroken | 是 | 见 `integration.yaml` |

**Meshy 毛坯（美术导向）** 可以按船体、艉楼、桅杆体块分件生成。Blender 必须打成上表的 UE 模块，其中帆装为 MastRig 整包 × RigType × Full/Half/Furled。

一期生产：Square + Lateen 各三状态（六件）。Gaff 仅设计兼容。

旗接口 **`Attach_Flag` 在 MastRig 网格上，不在 Hull 上。**

## 8. Meshy / Blender / UE5

Meshy：Hull Base；无展开帆；简化索具；删杂物；保留 V0.8 首尾。

Blender：对称、拓扑、Pivot、UV、按上表拆模块、+X forward、Apply Rotation+Scale。

UE：`/Game/Ships/ShipType_SmallSailer01/`。Socket 在 UE Static Mesh Editor 添加。无 Crew Socket。货物不按种类/数量生成网格。

2D 改装图：船头朝左；2048×1024；透明；无烘焙热区；槽位 `OutfitSlot_*`。

## 9. V1 验收

以 Cog (ship) 为历史原型；一眼仍是 V0.8 同一艘船；首尾未修平；主桅居中且主桅长度严格大于船长；低矮两层艉楼；主甲板至艉楼平台只有一套贴一侧船舷的木质楼梯且不得居中；货舱口只有一个且不与主桅/桅座位置重叠；全船四个炮窗、每舷两个、沿纵向中心线镜像对应且位于顶层甲板对应舷侧区域；中线舵；无展开大帆；无木桶杂物；无 AI 歧义结构。
