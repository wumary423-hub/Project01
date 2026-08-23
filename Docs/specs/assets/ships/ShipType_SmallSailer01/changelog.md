# ShipType_SmallSailer01 Changelog

## Design Spec 0.1.7 — 2026-08-23 — REVIEW

- 艉楼楼梯侧别由 UNSET 锁定为**右舷**；楼梯在船体内部、艉楼前方，不得居中、不得埋入实体艉楼。
- `integration.yaml` 同步至 0.1.6：`stairs_to_stern_platform.side = starboard` / `LOCKED`。

## Design Spec 0.1.6 — 2026-08-22 — REVIEW

- 用户批准 `木制帆船结构技术插画.png` 作为 **Reference Master R1**；源图 `1449×1086`，原始 PNG SHA-256：`327d646918cfb43a3a8c6347151da0944e8c1187018f3090fa6279f19f44456b`。
- 目标仓库路径登记为 `assets/ships/ShipType_SmallSailer01/reference/ShipType_SmallSailer01_reference-master_r1.png`；由于当前 GitHub 连接器不能直接上传 PNG 二进制，二进制状态为 `PENDING_IMPORT`，不得假称已上传或用其他图替代。
- 艉楼改为单层木质艉楼；艉楼地板与主甲板同层，屋顶为可上人平台并设栏杆。
- 艉楼楼梯锁定为船体内部单楼梯：贴一侧船舷，下端在主甲板，上端到艉楼屋顶平台；不得放到船体外侧或中轴线上。
- 货舱口仍只允许 1 个，并缩小为紧凑尺度，不得占满/主导主甲板，且不得与主桅/桅座重叠。
- 四个炮窗保持每舷两个、沿纵向中心线镜像，并新增**尺寸统一**约束。
- 艉楼木材与船体使用同一材质/色彩体系。
- Reference Master R1 为结构阅读省略索具与帆，保留主桅、帆桁与瞭望塔；该省略不等于最终资产禁止索具/帆。
- `integration.yaml` 同步升级至 0.1.5。
- 决策记录于 `decisions/ADR-0006-reference-master-r1.md`。

## Design Spec 0.1.5 — 2026-08-21 — REVIEW

- 船长由概念暂定值正式锁定为 **15m**。
- 主桅长度由相对约束 `mast_length > ship_length` 改为固定 **18m**（桅脚至桅顶）。
- `18m / 15m = 1.2` 仅作为派生比例，不再替代绝对尺寸规则。
- `integration.yaml` 同步升级至 0.1.4，并将船长与主桅长度标记为 `LOCKED`。
- 决策记录于 `decisions/ADR-0005-fixed-length-and-main-mast.md`。

## Design Spec 0.1.4 — 2026-08-21 — REVIEW

- 历史原型锁定为 **Cog (ship)**；允许架空化调整，不要求一比一复原具体历史实船。
- 艉楼楼梯仍为单楼梯，并新增位置约束：必须靠边贴一侧船舷、不得居中；具体左/右舷保持 UNSET。
- 炮窗仍为全船 4 个、每舷 2 个；新增沿船体纵向中心线两舷镜像分布约束，并锁定在顶层甲板对应的舷侧区域。
- 主桅新增相对尺寸约束：`mast_length > ship_length`；不由当前约 15m 的概念船长推导绝对主桅长度。
- 货舱口明确只允许 1 个，且不得与主桅/桅座位置重叠。
- `integration.yaml` 同步升级至 0.1.3。
- 决策记录于 `decisions/ADR-0004-cog-and-layout-constraints.md`。

## Design Spec 0.1.3 — 2026-08-21 — REVIEW

- 主甲板至艉楼平台的楼梯锁定为一套木质楼梯；禁止左右对称双楼梯。
- 炮窗锁定为船体结构特征：全船 4 个，左舷 2 个、右舷 2 个，两舷保持对应关系。
- 炮窗结构数量不等同于实际安装武装数量；武装数量仍未锁定。
- `integration.yaml` 同步记录楼梯数量 `1` 与四炮窗结构开口。
- 结构决定记录于 `decisions/ADR-0003-stair-and-gunports.md`。

## Design Spec 0.1.2 — 2026-08-20 — REVIEW

- 按 MAT-001 v0.2.0 / MAT-001-ADR-0001，同步删除会触发视觉做旧的“旧帆布”措辞。
- 材质方向改为“木质船体与低饱和灰白帆布”，不改变船体结构、比例、帆装身份或程序合同。

## 2026-08-19 — archive entry

- 增加本船 `README.md` 与 `references/` 索引；不改设计事实，不复制概念图。

## Design Spec 0.1.1 — 2026-08-19 — REVIEW

- 主键由启动包 `SHIP-0001` 改为程序目录行 `ShipType_SmallSailer01`；
- V0.8 母版改名但 SHA-256 不变；
- 模块表改为 MastRig 整包（Cursor 内容 + 启动包格式）；
- Socket 写入旧锁定名；UE 路径 `/Game/Ships/ShipType_SmallSailer01/`。

## Design Spec 0.1.0 — 2026-08-19 — REVIEW

- 建立稳定资产 ID（当时为 `SHIP-0001`，现已 SUPERSEDED）；
- 纳入 V0.8 Concept Master，并标记为 `LOCKED`。
