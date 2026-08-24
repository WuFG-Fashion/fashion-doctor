# Python项目默认技术栈2026：uv + Ruff + Ty + Polars

> 来源：AI Future Thinkers (https://aifuturethinkers.com/python-project-setup-2026-uv-ruff-ty-polars/)
> 采集日期：2026-06-14

---

## 概述

2026年Python项目的推荐默认技术栈已从传统的分散式工具链转向以 **Astral公司** 为核心的整合方案，8个工具缩减到4个，全部配置集中在 `pyproject.toml` 一个文件。

---

## 技术栈组成

| 工具 | 用途 | 替代的传统工具 | 开发商 |
|------|------|---------------|--------|
| **uv** | Python安装/环境管理/依赖管理/锁定/命令运行 | pyenv + pip + venv + pip-tools + Poetry | Astral |
| **Ruff** | 代码检查(Linting) + 格式化(Formatting) | Black + isort + Flake8 | Astral |
| **Ty** | 类型检查 | mypy / Pyright | Astral |
| **Polars** | 数据框(DataFrame)处理 | pandas | Pola.rs |

> uv + Ruff + Ty 来自同一家公司 Astral，无缝集成。

---

## 与传统方案对比

| 维度 | 传统方案 | 2026默认方案 |
|------|---------|-------------|
| **工具数量** | 8+ (pyenv+pip+venv+Poetry+Black+isort+Flake8+mypy+pandas) | 4 (uv+Ruff+Ty+Polars) |
| **配置文件** | 多个散落 (.flake8, setup.cfg, mypy.ini等) | 仅 pyproject.toml |
| **安装前提** | 需要预装Python | 无需预装Python |
| **环境管理** | 手动激活虚拟环境 | `uv run` 自动激活 |
| **依赖锁定** | pip-tools或Poetry | uv 自动生成 uv.lock |
| **代码格式化** | Black | Ruff（兼容Black风格） |
| **导入排序** | isort | Ruff（内置I规则） |
| **代码检查** | Flake8 | Ruff（更快，规则兼容） |
| **类型检查** | mypy | Ty（针对现代工作流优化） |
| **数据管道** | pandas（急切执行） | Polars（惰性执行+查询优化） |

---

## 核心命令速查

```bash
# 初始化项目（自动创建.venv和git仓库）
uv init

# 添加依赖
uv add polars
uv add --dev ruff ty pytest

# 统一命令入口：无需手动激活虚拟环境
uv run ruff check --fix .   # 代码检查+自动修复
uv run ruff format .         # 格式化
uv run ty check              # 类型检查
uv run pytest                # 测试
uv run python -m my_project.main  # 运行

# CI冻结安装
uv sync --frozen

# 一次性工具（不安装到项目）
uvx black .
```

---

## Polars 数据处理范式

| 特性 | 说明 |
|------|------|
| **惰性执行** | `scan_csv()` → `.collect()` 查询计划 |
| **查询优化** | 自动谓词下推、列裁剪 |
| **表达式驱动** | 向量化+并行化，避免逐行UDF |
| **Parquet优先** | 推荐内部数据使用Parquet而非CSV |

> **注意**：Polars expressions 让引擎实现向量化和并行化。除非没有原生替代，否则避免使用 UDF，因为 UDF 显著更慢。

---

## 不适用场景

- 团队已有成熟的 Poetry 或 mypy 工作流
- 代码库深度依赖 pandas 特定API或生态系统
- 组织标准化使用 Pyright
- 在遗留仓库中更换工具会带来更大破坏

---

## 配置统一示例

```toml
[project]
name = "fashion-doctor-analytics"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["polars>=1.39.3", "python-dotenv"]

[dependency-groups]
dev = ["pytest>=9.0.2", "ruff>=0.15.8", "ty>=0.0.26"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "B", "I", "UP"]
```
