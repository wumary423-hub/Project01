# Ship System Changelog

## 0.1.0 — 2026-08-19 — REVIEW

- 建立跨工具船只系统规范候选；
- 记录3D与2D岗位布局双资产要求；
- 记录旗帜、船首像和无船员Socket规则；
- 记录标准美术/3D/UE5工作流；
- 标记旧 `.cursor/rules/ship-system.mdc V0.1 LOCKED` 为待迁移；
- 未导入任何当前不可访问的旧程序条款。

## 0.1.1 — 2026-08-19 — REVIEW

- 主键改为 `ShipType_SmallSailer01`；废止 `SHIP-0001`；
- MastRig 整包写入启动包模块格式；socket 采用旧锁定名；
- 观察距离：常规 50–200m + 极限 10m；
- `Docs/Ship/*` 改为 SUPERSEDED 指向；旧 `.mdc` 仍未改写。

## 0.2.0 — 2026-08-19 — LOCKED

- 跨工具正文与程序运行时分别 LOCKED（`ship-system.md` / `ship-program.md`）；
- `.cursor/rules/ship-system.mdc` 改为适配入口；
- 纳入程序命名到 `naming-and-versioning.md`；
- Import/Validate 路径改为 `/Game/Ships/ShipType_SmallSailer01/`。

## 0.2.1 — 2026-08-19 — 澄清

- 将 `migration-from-cursor.md` 与 `migration-report-v0.1.md` 标为 SUPERSEDED，避免再按旧主键 `SHIP-0001` 执行迁移。



## 0.1.0+migration — 2026-08-19 — REVIEW

- Cursor 第一轮：生成 `migration-report-v0.1.md`；
- 将工作区旧文件实际版本更正为 **V0.1.1**（启动包曾写 V0.1）；
- 候选 `ship-system.md` / `ship-system.yaml` 增加从旧 `.mdc` 提取的程序事实，状态仍为 `REVIEW`；
- **未**解除旧 `.mdc` LOCKED，**未**改写 `.cursor/rules/ship-system.mdc`。

