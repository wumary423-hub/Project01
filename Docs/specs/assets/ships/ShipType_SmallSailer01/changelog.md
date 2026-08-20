# ShipType_SmallSailer01 Changelog

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
