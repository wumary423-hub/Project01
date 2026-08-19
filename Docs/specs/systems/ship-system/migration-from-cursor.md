# 从 `.cursor/rules/ship-system.mdc V0.1 LOCKED` 迁移

## 禁止事项

- 不覆盖现有旧文件；
- 不把本启动包中的候选规则当作旧文件原文；
- 不因字段名称相似而自动合并；
- 不解除任何旧规则的 `LOCKED` 状态；
- 不在未获批准时删除旧路径。

## Cursor 必须完成的步骤

### 1. 读取旧文件

确认实际路径、版本、状态和完整内容。

### 2. 建立逐条清单

把每一条规范分类为：

- 程序运行逻辑；
- 数据结构；
- 命名；
- 文件路径；
- 美术接口；
- 工作流程；
- 禁止性规则；
- 备注或解释。

### 3. 映射到新体系

建议映射：

- 通用船只系统事实 → `ship-system.md`
- 可机读字段 → `ship-system.yaml`
- 单船事实 → 对应 `SHIP-xxxx/design.md`
- 程序接口 → 独立程序合同或现有代码文档
- Cursor行为提示 → `.cursor/rules/ship-specs-adapter.mdc`

### 4. 冲突报告

对每一处冲突列出：

- 旧规则原文；
- 新候选规则；
- 影响文件；
- 推荐处理；
- 是否涉及 LOCKED 内容。

### 5. 生成候选差异

创建：

```text
docs/specs/systems/ship-system/migration-report-v0.1.md
```

并更新候选 `ship-system.md` 与 `ship-system.yaml`，状态仍保持 `REVIEW`。

### 6. 校验

运行：

```bash
python tools/validate_specs.py
```

### 7. 用户批准

用户批准迁移后：

- 将新系统规范标记为 `LOCKED`；
- 更新版本；
- 记录 ADR/Changelog；
- 把旧 `.mdc` 改成只读取新权威文件的适配器；
- 保留 Git 历史，禁止无记录删除。

## 迁移报告最小格式

```md
# Ship System V0.1 Migration Report

## 旧规则基本信息
## 完整条款映射
## 未迁移内容
## 冲突
## 程序影响
## 建议差异
## 验证结果
## 用户批准记录
```
