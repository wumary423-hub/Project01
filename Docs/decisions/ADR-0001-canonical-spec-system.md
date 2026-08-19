---
document_type: architecture_decision_record
adr_id: ADR-0001
status: REVIEW
date: 2026-08-19
---

# ADR-0001：采用跨工具统一规范系统

## 背景

项目同时使用 Cursor、ChatGPT、Meshy、Blender 和 UE5。若每个工具在自己的聊天、规则或项目文件中维护独立事实，艺术与程序对接会逐渐产生冲突。

## 决策

采用以下体系：

- Git 仓库为权威中心；
- Markdown 为可读规范；
- YAML 为机器合同；
- 大型资源通过稳定 ID 和规范路径关联；
- `.cursor/rules`、ChatGPT 项目指令及其他工具提示仅作为适配层；
- 聊天结论提交 Git 后才成为跨工具正式事实。

## 后果

优点：

- 可追溯、可比较、可回滚；
- 不同工具读取同一来源；
- 艺术与程序通过 Integration Contract 对接；
- 可以建立自动校验。

代价：

- 关键决策需要更新规范和提交；
- 旧 Cursor 规则必须进行一次迁移；
- ChatGPT 项目中的上传文件需要核对 commit。
