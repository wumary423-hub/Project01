# ShipType_SmallSailer01

小型单桅沿岸商船。规范主键 = 目录行 = **`ShipType_SmallSailer01`**。  
不要用 `SHIP-0001`（仅历史 alias / `former_starter_id`）。

工作名 `SmallSailer01` 只用于网格前缀 `SM_SmallSailer01_*`。

## 阶段

| 项 | 状态 |
|----|------|
| V0.8 Concept Master | LOCKED |
| Reference Master R1 | LOCKED identity / PNG `PENDING_IMPORT` |
| Shared Geometry Blockout | APPROVED |
| 正交相机与取景 | APPROVED（commit `395dba6`） |
| `[线稿多视图]` Work R1 | REJECTED |
| `[线稿多视图]` Work R2 | APPROVED |
| `[概念多视图]` | NOT STARTED |
| `design.md` | REVIEW 0.1.9 |
| 当前阶段 | Concept Multiview（待出候选） |
| 下一阶段 | `[概念多视图]`；不要导出 Tripo / UE |

## 当前 Reference Master R1

目标路径：

```text
assets/ships/ShipType_SmallSailer01/reference/ShipType_SmallSailer01_reference-master_r1.png
```

源 PNG SHA-256：

```text
327d646918cfb43a3a8c6347151da0944e8c1187018f3090fa6279f19f44456b
```

当前连接器不能直接上传 PNG，因此二进制仍为 `PENDING_IMPORT`。正式身份与结构范围见 `references/README.md` 和 `decisions/ADR-0006-reference-master-r1.md`。

## 先读这些（本船）

| 文件 | 用途 |
|------|------|
| `design.md` | 设计意图、当前结构约束、参考母版 |
| `integration.yaml` | UE 路径、模块、socket、结构机器合同 |
| `changelog.md` | 本船变更 |
| `references/` | Concept Master / Reference Master 索引 |
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
