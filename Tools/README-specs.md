# 规范工具

## 安装

```bash
python -m pip install -r tools/requirements-specs.txt
```

## 校验

```bash
python tools/validate_specs.py
```

真实仓库合并完成后可使用严格模式：

```bash
python tools/validate_specs.py --strict
```

迁移前，严格模式会因为旧 `.cursor/rules/ship-system.mdc` 在启动包中不存在而提示。

## 导出上下文

```bash
python tools/export_context.py ShipType_SmallSailer01 --target chatgpt
python tools/export_context.py ShipType_SmallSailer01 --target google-ai-studio
python tools/export_context.py ShipType_SmallSailer01 --target cursor
python tools/export_context.py ShipType_SmallSailer01 --target meshy
python tools/export_context.py ShipType_SmallSailer01 --target blender
python tools/export_context.py ShipType_SmallSailer01 --target ue5
```

导出文件位于 `exports/context/`。导出物是工具输入快照，不是权威源。  
`--target google-ai-studio` / `chatgpt` 会附带本船 `material_card`（当前 MAT-001）正文。
