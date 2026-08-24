# 2026 现代 Python 数据栈：团队实际在用的工具全景

> **来源**: SaaS Curate "The Modern Python Data Stack Teams Are Actually Using in 2026" (saascurate.com) + Datafold "The Modern Data Stack: Open-source edition" (datafold.com) + htdocs.dev "The Modern Python Data Stack in 2026"
> **日期**: 2026-07
> **作者**: Dhruva Shah (SaaS Curate) / Gleb Mezhanskiy (Datafold)

---

## 核心趋势: 数据工程、AI 工程、ML 基础设施三线融合

2026 年的核心变化不是某个工具，而是**团队结构**：数据工程、AI 工程、ML 基础设施边界消失。高绩效团队用轻量、生产级、AI 原生的技术栈。

---

## 八层技术栈全景

### 1. 数据摄取: dlt + Airbyte 取代手写脚本
- **dlt** (data load tool): 5.2K Stars，Python 原生，类型感知、幂等管道、极简代码
- **Airbyte**: 350+ 连接器，自托管免费
- 被取代: 手写 Python 摄取脚本（脆弱、难维护）

### 2. 存储: Postgres 全面胜利
- Postgres + pgvector (向量搜索) + pg_duckdb (分析加速) + Citus (扩展)
- 一个数据库覆盖传统需多库的场景
- MongoDB → Postgres + JSONB 替代趋势明显
- 分析层: DuckDB (嵌入式高性能)、ClickHouse (大规模 OLAP)
- DuckDB v1.5.4: Quack 核心扩展（客户端-服务器协议）、VARIANT 类型、GEOMETRY 类型、v2.0 计划 2026 秋季

### 3. 转换: Polars 取代 Pandas (生产环境)
- dbt: SQL 转换工作流仍占主导
- Ibis: 跨后端可移植转换逻辑兴起
- Polars 生产 ETL → Pandas 仅保留于探索/可视化

### 4. 编排: Airflow 不再是默认选择
- **Dagster**: 15.8K Stars，资产中心模型，内置 lineage 和可观测性，dbt 一等公民集成
- **Prefect**: 灵活的命令式工作流
- **Temporal**: 长运行 AI 工作流和事件驱动系统
- **Kestra**: 26.6K Stars，$25M Series A (2026.3)，20 亿+ 工作流执行

### 5. AI / LLM 基础设施
- PyTorch (ML) + HuggingFace (模型) + vLLM (推理) + LiteLLM (提供者抽象)
- 编排: LangGraph (多步 Agent) + DSPy (Prompt 优化)
- 可观测性: LangFuse / LangSmith

### 6. MLOps
- MLflow (实验追踪) + LangFuse (可观测性) + Ray (分布式计算)
- Modal / RunPod (GPU 推理)

### 7. 笔记本: Marimo 取代 Jupyter (生产)
- Jupyter: 探索 → 玩具
- Marimo: 响应式执行、可复现工作流、可部署 notebook 应用、脚本兼容
- Positron: 数据优先 IDE，RStudio 团队打造

### 8. 看板/内部工具
- Streamlit: 内部工具首选
- Evidence: 分析即代码（SQL 驱动）
- Plotly Dash: 生产级看板
- Tableau/Looker 仍在但小型敏捷团队倾向开发者优先工具

---

## 工具链速查

| 类别 | 2026 默认 | 被取代 |
|------|----------|--------|
| 包管理 | uv (Rust 速度) | pip + venv + pyenv |
| Linting | Ruff (单工具) | flake8 + isort + black |
| 类型检查 | ty (astral 出品) | mypy |
| IDE | Positron (数据优先) | VS Code |
| 笔记本 | Marimo (响应式) | Jupyter |
| DataFrame | Polars (多核/惰性) | Pandas |
| 本地 SQL | DuckDB (嵌入式 OLAP) | SQLite |
| 文档/报告 | Quarto | MkDocs |
| 看板 | Evidence (SQL 驱动) | Power BI / Tableau |

## 开源生态关键事件 (Datafold 2026.4)

- **Snowplow**: 从 Apache 2.0 → SLULA 限制许可证（不推荐生产）
- **MinIO**: 2026.2 归档 OSS 仓库，社区 fork pgsty/minio
- **Mage**: 2.6 commits/周，实际上停更
- **Amundsen**: 0 commits/周，已弃置
- **Evidence**: 最后提交 2026.2.18，可能 pivot/收尾
- **SQLMesh**: Fivetran 收购后捐赠 Linux Foundation (2026.3)，开发降 87%

## 服装零售场景映射

| 层 | 推荐工具 | 多品牌场景 |
|----|---------|-----------|
| 摄取 | dlt | 各品牌 POS/CRM/电商 API 统一摄取 |
| 存储 | Postgres + DuckDB | 运营库 + 分析加速 |
| 转换 | Polars + dbt | 品牌级 ETL 用 Polars，全局模型用 dbt |
| 编排 | Dagster | 资产中心模型 → 品牌级数据血缘追踪 |
| 看板 | Streamlit | 多品牌 Dashboard 统一框架 |
| 笔记本 | Marimo | 数据分析师响应式探索 |
