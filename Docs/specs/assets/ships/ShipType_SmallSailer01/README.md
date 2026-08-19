# ShipType_SmallSailer01

小型单桅沿岸商船。规范主键 = 目录行 = **`ShipType_SmallSailer01`**。  
不要用 `SHIP-0001`（仅历史 alias / `former_starter_id`）。

工作名 `SmallSailer01` 只用于网格前缀 `SM_SmallSailer01_*`。

## 阶段

| 项 | 状态 |
|----|------|
| V0.8 Concept Master | LOCKED |
| `design.md` | REVIEW |
| 当前阶段 | Concept Design |
| 下一阶段 | V1 Hull-Focused Concept |

## 先读这些（本船）

| 文件 | 用途 |
|------|------|
| `design.md` | 设计意图、V1 要改什么 |
| `integration.yaml` | UE 路径、模块、socket、文件名 |
| `changelog.md` | 本船变更 |
| `references/` | 概念图入口（图文件不在本目录） |
| `decisions/` | 已拍板的 ADR |

系统级（LOCKED，不要在本船文件夹另写一套）：

- `Docs/specs/systems/ship-system/ship-system.md`
- `Docs/specs/systems/ship-system/ship-program.md`
- `Docs/specs/systems/ship-system/ship-system.yaml`

## UE（已确认）

- 网格：`/Game/Ships/ShipType_SmallSailer01/`
- 目录表：`/Game/Ship/DT_Ships`
- Hull：`SM_SmallSailer01_Hull`
- MastRig：`SM_SmallSailer01_MastRig01_<Rig>_<State>`（整包，不拆 Mast/Yard/Sail）
- Rudder：`SM_SmallSailer01_Rudder`

其余模块与 socket 以 `integration.yaml` 为准。
