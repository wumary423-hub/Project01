# ShipType_SmallSailer01 Changelog

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
