# UE5 使用指南

## 输入

- Blender交付模型；
- `integration.yaml`；
- 船只系统程序合同；
- 2D岗位布局资产。

## 当前目标路径

```text
/Game/Ships/ShipType_SmallSailer01/
/Game/Ships/ShipType_SmallSailer01/Mesh/
```

磁盘 FBX 收件箱：`Content/Ships/ShipType_SmallSailer01/Mesh/`。

## 导入检查

- 单位（厘米）、朝向（+X forward）、Pivot；
- Hull 为 `AFleet` 根；MastRig 为整包三状态；
- Socket：`Pontoon_*` ×4；`Attach_MastRig_01`；`Attach_Flag` 在 MastRig 上；
- UV与材质槽、LOD、Collision；
- 3D与2D结构一致性；
- 无 Crew Socket。

## 程序合同

运行时与 Socket 以 `docs/specs` 中 LOCKED 的 `ship-program.md` 与 `integration.yaml` 为准。`.cursor/rules/ship-system.mdc` 仅为入口。
