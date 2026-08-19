---
document_type: asset_decision_record
adr_id: ShipType_SmallSailer01-ADR-0002
asset_id: ShipType_SmallSailer01
status: LOCKED
date: 2026-08-19
---

# 船体设计与帆装展示分离

## 背景

展开大帆遮挡主桅根部、主甲板、货舱口和艉楼关系，同时增加AI生成歧义。

## 决策

下一阶段采用 Hull-Focused Concept：

- 不使用展开大帆；
- 帆省略或收帆；
- 简化索具；
- 删除木桶和甲板杂物；
- 先锁定船体、甲板、艉楼、舵和接口；
- 帆装身份在船体锁定后单独设计。

UE 最终帆装模块仍是 **MastRig 整包**（scheme A），不是独立的 Mast/Yard/Sail 三件网格。

## 后果

Concept Master继续保留完整视觉身份；Meshy输入不再承担帆装展示任务。
