# Cursor 使用指南

## 角色

Cursor负责：

- 读取权威规范；
- 维护程序接口；
- 编写校验、导入和导出脚本；
- 把艺术合同映射到 UE5 代码、DataAsset 或 Blueprint；
- 生成候选规范差异。

Cursor不是独立规范数据库。

## 读取顺序

1. `spec-manifest.yaml`
2. `docs/governance/source-of-truth.md`
3. `docs/governance/naming-and-versioning.md`
4. `docs/specs/systems/ship-system/ship-system.md`
5. `docs/specs/systems/ship-system/ship-program.md`
6. `docs/specs/systems/ship-system/ship-system.yaml`
7. 目标资产的 `design.md` 与 `integration.yaml`
8. `.cursor/rules` 适配入口

`.cursor/rules/ship-system.mdc` 已是适配层，不得在其中另写规范事实。

## 写入规则

- 程序事实写入系统规范或程序合同；
- 单船事实写入 `docs/specs/assets/ships/ShipType_*/`；
- Cursor行为提示只写入 `.cursor/rules`；
- 任何猜测字段写成 `UNSET`，不得自动决定；
- LOCKED变更必须提供 diff 和批准记录。
