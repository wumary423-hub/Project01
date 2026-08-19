# Blender 使用指南

## 读取

同时读取：

- 单船 `design.md`；
- `integration.yaml`；
- Meshy输入图和输出；
- 当前模块命名规则。

## 职责

- 修正结构和左右对称；
- 重建船艏、船尾、中线舵和接口；
- 清理拓扑；
- 按 **UE 模块表** 拆分：Hull、MastRig 整包、舵/旗/船首像/锚等；
- 不要把 Mast/Yard/Sail 作为一期独立 UE 网格导出；
- 设置比例、Pivot、UV和材质槽；**+X** forward；Apply Rotation + Scale；
- 准备LOD与Collision；
- 导出FBX（一资产一文件）。

## 命名

网格工作前缀：`SM_SmallSailer01_*`。资产主键：`ShipType_SmallSailer01`。

禁止：

- 自行增加船员Socket；
- 自行决定未锁定尺寸；
- 为美观改变锁定轮廓；
- 把 `Attach_Flag` 做在 Hull 上；
- 把临时Meshy错误固化成正式结构。
