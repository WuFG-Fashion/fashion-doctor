---
type: concept
title: Python项目默认技术栈2026 — uv+Ruff+Ty+Polars
aliases:
  - "Python项目默认技术栈"
  - "python dev stack 2026"
tags: [python, polars, devops, toolchain, uv, ruff, streamlit]
sources: [2026-06-14_AIFutureThinkers_uv_Ruff_Ty_Polars_2026默认技术栈.md]
created: 2026-06-14
updated: 2026-08-06
cross_refs: [[polars_vs_pandas_2026]], [[streamlit_dashboard_2026]], [[streamlit_production_dashboard|Streamlit生产级多品牌看板]], [[data_library_selection_guide_2026|数据分析库选型决策指南2026]], [[2026-08-06_Pandas_3.0_CoW与Arrow字符串后端落地基准]], [[2026-08-06_Python看板六框架横评与生产三大失效模式]]
layer: T1
scope: public
volatility: evergreen
as_of: 2026-08-06
review_due_at: 2027-02-02
status: active
---
# Python项目默认技术栈2026 — uv+Ruff+Ty+Polars

> **一句话摘要**：2026年Python数据项目从传统8+工具链收敛到 uv+Ruff+Ty+Polars 四件套（同出Astral公司），所有配置集中 pyproject.toml，uv run 一站式管理从未如此简洁。

> **来源**：AI Future Thinkers / Python Project Setup 2026
> **最后更新**：2026-06-14


## 结论

1. **四件套（uv/Ruff/Ty/Polars）是新起项目默认栈，存量项目必须拆开决策**：uv 与 Ruff 渐进采用（只换包管理器与 lint）风险低收益即时；Polars 是数据层重写、Ty 取决于类型注解现状——三者迁移成本量级不同，打包决策是常见错误。
2. **工具 8 合 1 的核心价值是配置收敛**：pyenv+pip+venv+pip-tools+Poetry+Black+isort+Flake8 收敛到 4 件同源工具（Astral）+ 唯一 pyproject.toml——对 1-2 人团队的心智负担下降显著，这是比「快」更实际的收益。
3. **本系统属于「遗留仓库谨慎换工具」类别**：深度依赖 pandas 特定 API、已有成熟 venv 工作流——uv/Ruff 可在新脚本试点、Polars/Ty 暂缓；环境基线（pandas 3.0 硬性要求 Python 3.11+、Streamlit 最低 3.10）是未来升级时的前置检查项。

## 核心要点

1. **工具8合一**：uv替代pyenv+pip+venv+pip-tools+Poetry（5个），Ruff替代Black+isort+Flake8（3个），Ty替代mypy
2. **同出一家**：uv+Ruff+Ty均来自Astral公司，天然无缝集成
3. **无需预装Python**：uv独立安装器一行命令搞定
4. **uv run 永远**：永不手动激活虚拟环境，`uv run` 统管所有命令
5. **Polars惰性执行**：scan_csv → .collect() 查询优化替代急切pandas

## 技术栈对比

| 维度 | 传统方案 | 2026默认方案 |
|------|---------|-------------|
| 工具数量 | 8+ (pyenv/pip/venv/Poetry/Black/isort/Flake8/mypy/pandas) | 4 (uv/Ruff/Ty/Polars) |
| 配置文件 | 散落多个 (.flake8/setup.cfg/mypy.ini等) | 仅 pyproject.toml |
| 安装前提 | 需预装Python | 无需预装 |
| 环境管理 | 手动 `source .venv/bin/activate` | `uv run` 自动激活 |
| 依赖锁定 | pip-tools/Poetry | uv自动生成uv.lock |
| 代码质量 | Black+isort+Flake8 | Ruff一站式 |
| 类型检查 | mypy | Ty |
| 数据管道 | pandas急切执行 | Polars惰性执行+查询优化 |

## 核心命令速查

```bash
# 初始化
uv init                          # 自动创建.venv + git仓库

# 依赖管理
uv add polars                    # 生产依赖
uv add --dev ruff ty pytest      # 开发依赖

# 统一入口（永不手动激活虚拟环境）
uv run ruff check --fix .        # Lint + 自动修复
uv run ruff format .             # 格式化
uv run ty check                  # 类型检查
uv run pytest                    # 测试
uv run python -m app.main        # 运行

# CI
uv sync --frozen                 # 严格lockfile，更快更可靠

# 一次性工具
uvx black .                      # 不安装到项目
```

## Polars数据处理范式

| 特性 | 说明 |
|------|------|
| **惰性执行** | `scan_csv()` 构建查询计划 → `.collect()` 执行 |
| **查询优化** | 自动谓词下推、列裁剪、常量折叠 |
| **表达式驱动** | 向量化+并行化，避免逐行UDF |
| **Parquet优先** | 推荐内部数据Parquet而非CSV |

> ⚠️ 避免UDF除非没有原生替代，UDF显著更慢

## 集中配置示例（pyproject.toml）

```toml
[project]
name = "fashion-doctor-analytics"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["polars>=1.39.3"]

[dependency-groups]
dev = ["pytest>=9.0.2", "ruff>=0.15.8", "ty>=0.0.26"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "I", "UP"]

[tool.ruff.format]
docstring-code-format = true
quote-style = "double"
```

## 不适用场景

- 已有成熟Poetry/mypy工作流
- 代码库深度依赖pandas特定API/生态
- 组织标准化Pyright
- 遗留仓库换工具破坏性大

## 对Fashion Doctor多品牌的意义

| 环节 | 传统 | 2026堆栈 | 收益 |
|------|------|---------|------|
| 环境管理 | pip/venv切换 | `uv run` | 零心智负担 |
| 代码质量 | Black+isort+Flake8 | Ruff | 速度快10-100x |
| 类型安全 | mypy | Ty | 更现代的错误提示 |
| 数据处理 | pandas | Polars(惰性) | 100万行+显著提速 |


## 2026-08 环境基线刷新

| 组件 | 2026-08 基线 | 说明 |
|------|-------------|------|
| Python | **≥ 3.11（pandas 3.0 硬性要求）**，推荐 3.13 | Streamlit 硬性最低 3.10 |
| pandas | **3.0.4**（2026-06-28） | CoW 默认唯一、Arrow 字符串默认、`pd.col()` |
| Streamlit | **1.55**（2026-04 稳定版） | Snowflake 主导，**每两周发一版** |
| Plotly | **6.x** | 相对 5.x 有破坏性变更，需按 v6 迁移指南改 |

升级顺序建议：先把 uv 环境的 Python 提到 3.11+，再升 pandas 2.3 消警告，最后跳 3.0。详见 [[2026-08-06_Pandas_3.0_CoW与Arrow字符串后端落地基准]] 与 [[2026-08-06_Python看板六框架横评与生产三大失效模式]]。

## 信息链

- **上游 · 来源支撑**：[[2026-08-06_Pandas_3.0_CoW与Arrow字符串后端落地基准]] · [[2026-08-06_Python看板六框架横评与生产三大失效模式]]（本页事实来自这些原始采集）
- **本页定位**：concept —— Python项目默认技术栈2026 — uv+Ruff+Ty+Polars
- 关联实体：无
- 关联概念：[[polars_vs_pandas_2026]] · [[streamlit_dashboard_2026]] · [[duckdb_olap_engine_2026]]
- 关联对比：无
- 关联打法：无
- ⚠️ **断点（指向未建页）**：[[streamlit_production_dashboard]] · [[data_library_selection_guide_2026]]（待补页或修正双链）

## 关联页面

[[polars_vs_pandas_2026]]
[[streamlit_dashboard_2026]]
[[streamlit_production_dashboard|Streamlit生产级多品牌看板]]
[[data_library_selection_guide_2026|数据分析库选型决策指南2026]]
[[duckdb_olap_engine_2026|DuckDB嵌入式OLAP引擎]]
- [[2026-08-06_Pandas_3.0_CoW与Arrow字符串后端落地基准]] — Pandas 3.0 版本与迁移基线 ⭐ NEW
- [[2026-08-06_Python看板六框架横评与生产三大失效模式]] — 看板侧版本组合基线 ⭐ NEW

## 前沿

**适用边界**：「uv + Ruff + Ty + Polars 四件套」是 2026 Python 工程化最佳实践，但其对象是**新起项目**——存量项目（如本系统）迁移收益要扣掉迁移成本：uv 可渐进采用（只换包管理器），Polars 则是数据层重写，两者应分开决策。

**可迁移性**：对本系统可直接采纳的是 uv（包管理提速）与 Ruff（lint 提速），风险低收益即时；Ty（类型检查）取决于代码库类型注解现状。

**下轮核查**：与 `python_data_stack_decision_2026`（运行时选型）、`polars_vs_pandas_2026` 的分工（本页管开发工具链，后者管数据引擎）；Astral 四件套版本号时效。
