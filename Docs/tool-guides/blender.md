# Blender 使用指南

Blender 负责清理 AI 组件、制作简单组件、设置比例/Pivot/UV/碰撞/LOD，并组装整船。读取目标船 `design.md`、`integration.yaml`、当前批准完整效果概念和目标组件参考包。

当前验证：

- 清理 Tripo 生成的 Hull；
- Hull 保持连续，不带炮窗或附件；
- 制作一块独立、可手动缩放和移动的简单 Deck；
- 暂不制作或组装艉楼、桅杆、舵、斜桅、锚、灯、绞盘和装饰。

以后炮窗模块包含可见部件、Boolean Cutter 和 Cannon Anchor，再由用户在 Hull 上布置。网格工作前缀为 `SM_SmallSailer01_*`，坐标采用 `+X` forward，Apply Rotation + Scale 后再导出。
