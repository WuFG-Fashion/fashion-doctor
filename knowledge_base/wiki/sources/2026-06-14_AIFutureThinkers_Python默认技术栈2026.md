---
type: source
title: Python项目默认技术栈2026 — uv+Ruff+Ty+Polars
tags: [python, polars, devops, toolchain, uv, ruff]
sources: [2026-06-14_AIFutureThinkers_uv_Ruff_Ty_Polars_2026默认技术栈.md]
created: 2026-06-14
updated: 2026-06-14
cross_refs: [[polars_vs_pandas_2026]], [[streamlit_dashboard_2026]]
---

# Python项目默认技术栈2026 — uv+Ruff+Ty+Polars

> **一句话摘要**：2026年Python项目统一技术栈：uv+Ruff+Ty+Polars四件套替代传统8+工具，所有配置集中pyproject.toml，一站式管理从环境到数据管道。
> **来源**：AI Future Thinkers / Python Project Setup 2026
> **最后更新**：2026-06-14

## 核心要点

1. **工具从8合一到4**：uv替代pyenv+pip+venv+pip-tools+Poetry，Ruff替代Black+isort+Flake8，Ty替代mypy，Polars替代pandas
2. **uv+Ruff+Ty同出一家Astral**：无缝集成，统一pyproject.toml配置
3. **无需预装Python**：uv独立安装器，一行命令搞定
4. **uv run一站式**：永不手动激活虚拟环境
5. **Polars惰性执行+查询优化**：scan_csv→collect模式，避免逐行UDF

## 详细内容

### 核心命令

```bash
uv init                          # 初始化
uv add polars                    # 生产依赖
uv add --dev ruff ty pytest      # 开发依赖
uv run ruff check --fix .        # Lint+自动修复
uv run ruff format .             # 格式化
uv run ty check                  # 类型检查
uv run pytest                    # 测试
uv sync --frozen                 # CI冻结安装
```

### 不适用场景

- 已有成熟Poetry/mypy工作流
- 深度依赖pandas特定API
- 组织标准化Pyright
- 遗留仓库换工具破坏性大

## 关联页面

[[polars_vs_pandas_2026]]
[[streamlit_dashboard_2026]]
[[streamlit_production_dashboard|Streamlit生产级多品牌看板]]
[[data_library_selection_guide_2026|数据分析库选型决策指南2026]]
