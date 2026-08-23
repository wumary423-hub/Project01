# ShipType_SmallSailer01 参考图

本目录只放索引，**不存放概念图/参考图副本**。母版图像文件统一放在仓库 `assets/ships/ShipType_SmallSailer01/` 下，避免重复副本导致 SHA 对不上。

## V0.8 Concept Master — LOCKED

路径（仓库根起）：

```text
assets/ships/ShipType_SmallSailer01/concept/ShipType_SmallSailer01_concept-master_r0.8.png
```

SHA-256：

```text
0c848da018e5c4ebe1edc65611d9b46a2e6633a09430aba8af80ccbf01bfe44d
```

被引用处：`design.md`、`integration.yaml`、`spec-manifest.yaml`。

## Reference Master R1 — LOCKED identity / binary PENDING_IMPORT

用户批准源图：

```text
木制帆船结构技术插画.png
```

尺寸：`1449 x 1086`

源 PNG SHA-256：

```text
327d646918cfb43a3a8c6347151da0944e8c1187018f3090fa6279f19f44456b
```

目标仓库路径：

```text
assets/ships/ShipType_SmallSailer01/reference/ShipType_SmallSailer01_reference-master_r1.png
```

当前 GitHub 连接器不能直接上传 PNG 二进制，因此该目标路径当前为 `PENDING_IMPORT`。在实际导入前，不得声称 PNG 已在仓库中，也不得用其他图片替代 R1。

R1 的使用范围：船体、主甲板、单层艉楼、内部楼梯、紧凑货舱口、炮窗、主桅/帆桁/瞭望塔等基础结构参考。R1 为结构阅读省略索具和帆；这不等于最终资产禁止索具/帆。

被引用处：`design.md`、`integration.yaml`、`spec-manifest.yaml`、`decisions/ADR-0006-reference-master-r1.md`。

## Shared Geometry Blockout — APPROVED

```text
assets/ships/ShipType_SmallSailer01/blender/ShipType_SmallSailer01_blockout.blend
```

SHA-256：`7ef92e5dcbf32ba4592731495ba6acb27e476b4f0011898c00f3b8fa47d113a4`  
正交取景批准 commit：`395dba69a46ac050fb2a612203e3341458b8748c`

## `[线稿多视图]`

- Work R1：`REJECTED`
- Work R2：`APPROVED`（`assets/ships/ShipType_SmallSailer01/line-multiview/candidates/work-r2/`）

五张线稿是 `[概念多视图]` 的结构上游权威输入。不得修改。

## `[概念多视图]`

- 状态：`NOT STARTED`
- 上游：V0.8 Concept Master + Work R2 + `MAT-001`

## 归档约束

否决图、试画、Meshy 中间图不要放进上述母版路径。工作文件使用 `assets/ships/ShipType_SmallSailer01/meshy/` 等对应工作目录。
