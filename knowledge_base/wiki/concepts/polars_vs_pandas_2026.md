---
type: concept
title: Polars vs Pandas vs DuckDB 2026选型指南
aliases:
  - "Polars"
  - "Pandas"
  - "DuckDB"
  - "数据框选型"
tags: [polars, duckdb, pandas, python, data_analysis, benchmark, etl, mlflow, streamlit]
sources: [https://docs.kanaries.net/zh/articles/polars-vs-pandas, https://scopir.com/zh/posts/top-python-data-analysis-libraries-2026/, 2026-06-08_Polars_DuckDB_Pandas三大引擎对比, 2026-06-09_Scopir_Python数据分析库2026横评, 2026-06-10_CSDN_Polars_MLflow_Streamlit工程化2026, 2026-06-11_chenxutan_Polars深度实战Rust架构, 2026-06-14_Scopir_Python数据分析库2026全景对比.md, 2026-06-18_CSDN_Polars_2.0_大规模清洗优化, 2026-06-27_今日头条_Polars_DuckDB_Pandas三引擎实测2026, 2026-06-27_chenxutan_Polars深层架构与生态2026, 2026-06-30_chenxutan_Polars_Pandas深度实测2026, 2026-07-03_PyTutorial_Polars_Arrow零拷贝互操作, 2026-07-03_Pandas官方_Pandas_3.0, 2026-07-06_腾讯云_Polars_Pandas千万级实测, 2026-07-06_TechInsider_Polars_Pandas企业级TCO_2026, 2026-07-15_Polars官方_polars_1.42新特性, 2026-07-15_Danilchenko_DuckDB_vs_Polars_2026生产实战对比, 2026-07-15_匡醍量化_Pandas_3.0底层架构革命, 2026-07-18_Johal_2026生产力数据分析七栈基准, 2026-07-22_Polars_1.42_分布式K8s_vs_Spark基准, 2026-07-25_Danilchenko_Polars_vs_Pandas_2026刷新基准, 2026-07-28_CSDN_Polars_2.0_清洗范式跃迁, 2026-07-31_Polars_2.0_Pandas_2.2大规模清洗基准, 2026-08-12_Polars2.1_Pandas3.0_生产级性能对比, 2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准, 2026-08-26_数据分析技术栈盘点与Polars_DuckDB性能基准]
created: 2026-06-06
updated: 2026-08-26
cross_refs: [[SQL查询性能优化]], [[ETL架构选型]], [[零售数据仓库SQL实践]], [[duckdb_olap_engine_2026]], [[2026-06-07_Polars_2.0流式ETL]], [[data_library_selection_guide_2026]], [[streamlit_dashboard_2026]], [[streamlit_production_dashboard]], [[retail_analytics_reporting_2026]], [[retail_data_workflow_2026|零售数据分析工作流]], [[2026-06-12_CSDN_Python数据分析工作流2026]], [[python_data_stack_decision_2026]], [[python_sql_integration_patterns_2026]], [[2026-06-15_CSDN_Python数据栈边界决策框架]], [[2026-06-15_aimojo_Python_Pandas_SQL集成指南]], [[2026-06-18_CSDN_Polars_2.0_大规模清洗优化]], [[2026-06-21_DuckDB_1.5_Sirius_GPU加速]], [[2026-06-24_Polars_2.0_Arrow_18.0深度协同]], [[2026-06-27_今日头条_Polars_DuckDB_Pandas三引擎实测]], [[2026-06-27_chenxutan_Polars深层架构与生态2026]], [[2026-06-30_chenxutan_Polars_Pandas深度实测2026]], [[2026-07-03_PyTutorial_Polars_Arrow零拷贝互操作]], [[2026-07-03_Pandas官方_Pandas_3.0]], [[2026-07-15_Polars_1.42自适应云IO与矛盾过滤器]], [[2026-07-15_Pandas_3.0_Arrow原生架构革命]], [[2026-07-15_DuckDB_vs_Polars_共存模式与生产决策]], [[2026-07-18_Johal_2026生产力数据分析七栈基准]], [[2026-07-22_Polars_1.42_分布式K8s_vs_Spark基准]], [[2026-07-25_Danilchenko_Polars_vs_Pandas_2026刷新基准]], [[2026-07-31_Polars_2.0_Pandas_2.2大规模清洗基准]], [[2026-08-06_Pandas_3.0_CoW与Arrow字符串后端落地基准]], [[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]], [[2026-08-26_数据分析技术栈盘点与Polars_DuckDB性能基准]], [[2026-09-06_零售数据分析技术栈按量分层选型与多品牌指标口径治理2026]]
---

# Polars vs Pandas vs DuckDB 2026选型指南

> **一句话摘要**：2026年Python数据分析选型已从"Polars vs Pandas"升级为"三引擎协同"——DuckDB做SQL聚合+窗口函数（10x）、Polars做ETL流水线（惰性+流式/分布式K8s）、Pandas做ML可视化（生态王者），通过Apache Arrow零拷贝串联。Polars 1.42 K8s 分布式单节点 vs Spark 6.4x/分布式 3.2x(1TB PDS-H基准)，575M+下载/38K+Stars。

> **来源**：Kanaries Docs 2026 + PythonDataBench 2026-02


## 结论

> ⏳ **待 AI 合成洞察**：本页结论应为「判断 / 推论」（例：行业进入 X 期、Y 是胜负手），禁止数据复述。以下为本页顶部摘要，作为合成原始素材：
>
> **一句话摘要**：2026年Python数据分析选型已从"Polars vs Pandas"升级为"三引擎协同"——DuckDB做SQL聚合+窗口函数（10x）、Polars做ETL流水线（惰性+流式/分布式K8s）、Pandas做ML可视化（生态王者），通过Apache Arrow零拷贝串联。Polars 1.42 K8s 分布式单节点 vs Spark 6.4x/分布式 3.2x(1TB PDS-H基准)，575M+下载/38K+Stars。

_（AI 将基于本页数据提炼 2–4 条结论洞察；规范见 [CLAUDE.md](../CLAUDE.md) 2.3 区块规范）_

## 性能基准（1000万行数据集）

| 操作 | Pandas | Polars | 倍差 |
|------|--------|--------|------|
| CSV加载(1GB) | 8.2s / 1.4GB | **1.6s / 0.18GB** | 5x快 / 87%内存省 |
| GroupBy聚合 | 1.8s | **0.22s** | 5-10x |
| 排序 | 3.4s | **0.29s** | ~11x（差距最大） |
| Join(1000万×100万) | 2.1s | **0.35s** | 3-8x |

> **关键结论**：<10万行几乎无差别；性能差距从100万行开始显著

### TPC-H官方基准（PDS-H测试套件，2025-05）

| 指标 | 数据 |
|------|------|
| 查询全面领先 | Polars在全部**22个**TPC-H衍生查询中均大幅领先Pandas |
| 能耗（合成数据） | Polars能耗≈Pandas的**1/8**（即Pandas的12.5%） |
| 能耗（TPC-H查询） | Polars仅消耗Pandas约**63%**的能量 |
| Modin评价 | 内存更高+API不完整+小数据更慢（**不推荐**） |

### 2026六库定位总表（Scopir横评）

| 库 | 定位 | 推荐场景 |
|------|------|----------|
| **Polars 1.x** | 性能优先标杆 | 生产数据管道/惰性求值/ETL流水线 |
| **DuckDB 1.x** | SQL聚合之王 | 多表JOIN/窗口函数/联邦查询/文件直查 |
| **Pandas 2.2** | 生态王者 | ML/scikit-learn/Excel/Jupyter探索 |
| **Modin** | ❌ 不推荐 | 两端不靠（兼容不如Pandas/性能不如Polars） |
| **Vaex** | 维护模式 | 不推荐新项目 |
| **DataFusion** | 增长中 | Rust原生项目 |

## 选型决策矩阵

| 场景 | 推荐 | 理由 |
|------|:---:|------|
| 数据<100万行 + ML生态 | **Pandas** | scikit-learn原生支持、团队熟悉、Excel支持好 |
| 数据>100万行 / 数据流水线 | **Polars** | 惰性求值、pushdown优化、显著性能优势 |
| 内存受限(<16GB) | **Polars** | 流式执行，Pandas OOM时Polars 4-6GB即可 |
| 大量Parquet格式 | **Polars** | predicate/projection pushdown |
| 新项目无历史包袱 | **Polars** | 趋势向Arrow统一内存格式 |
| 兼顾速度与生态 | **Polars→Pandas混合** | ETL用Polars→转Pandas做ML/可视化 |

## 服装零售数据场景适配

| 场景 | 典型数据量 | 推荐 |
|------|-----------|:---:|
| 单品牌日销售流水 | <10万行 | Pandas |
| 单品牌月度销售 | 10-50万行 | 均可 |
| 多品牌季度汇总 | 100-500万行 | **Polars** |
| 全渠道年度交易 | 500万+行 | **Polars** |
| VIP全量行为分析 | 1000万+行 | **Polars** |
| 实时Dashboard ETL | 持续流式 | **Polars** |

## 核心差异

| 维度 | Pandas | Polars |
|------|--------|--------|
| 执行模式 | 仅即时求值 | 即时+惰性求值 |
| 中间拷贝 | 每步可能创建新拷贝 | 惰性模式构建优化计划 |
| 内存格式 | NumPy/Python object | **Apache Arrow 列式** |
| API风格 | 方括号索引 `df["col"]` | 表达式API `pl.col("col")` |
| 生态成熟度 | 17年/45K+Stars | 5年/快速增长 |
| Excel支持 | ✅ 原生 | ❌ 需第三方库 |
| GPU加速 | ❌ | ✅ 可选NVIDIA |

## 混合方案（推荐）

```python
# Polars做重度ETL
processed = pl.scan_parquet("sales.parquet")
    .filter(pl.col("year") >= 2024)
    .group_by("brand")
    .agg(pl.col("amount").sum())
    .collect()

# 转Pandas做ML/可视化
pdf = processed.to_pandas()
```

## Polars 2.0 流式ETL引擎（2026-03更新）

Polars 2.0 引入**原生流式执行引擎**（Streaming Execution Engine），核心升级：

| 特性 | 说明 |
|------|------|
| 批次级断点续传 | 不再任务级重试，粒度更细 |
| Stream Join | 新增左流右表/双流Join，超Hash/Sort Join |
| mmap+zstd流式 | TB级Parquet：内存1.2GB(降低35x)，吞吐940MB/s(提升7x) |
| 表达式树剪枝 | 编译期冗余去除，节点从17→9，求值开销-50% |
| 分区感知Join | 预分片时网络传输O(N)→O(1) |
| Schema-drift熔断 | 连续3批类型冲突>15%自动阻断写入 |

### 企业级质量SLA（2025 Q4实测）

| 规则 | 达标率 |
|------|--------|
| 空值率≤0.001% | **99.998%** |
| 唯一键冲突≤1条/亿行 | **99.992%** |

### 2.0推荐集成

```python
# Polars 2.0 + Dagster 2.5 声明式Pipeline
@asset
def sales_summary() -> pl.DataFrame:
    return (pl.scan_parquet("data/sales.parquet")
            .group_by("region")
            .agg(pl.col("revenue").sum())
            .collect(streaming=True))  # 2.0流式消费
```

> **结论**：Polars 2.0已具备处理TB级ETL的流式能力，多品牌服装系统可选其为默认ETL引擎。

## Polars v1.26 新功能（2026年中）

| 功能 | 说明 | 零售场景 |
|------|------|---------|
| 异步执行引擎 | `collect_async()` 非阻塞 | 多品牌看板并行加载 |
| GPU加速（实验） | `read_parquet(gpu=True)` CUDA | 亿级RFM秒级计算 |
| 云原生数据源 | S3/Delta Lake/Iceberg直读 | 品牌数据湖联邦查询 |
| 流式处理增强 | `streaming=True` 100GB+恒内存 | 全年全品牌流水一次性分析 |
| 原生ML集成 | `polars.ml.train_test_split` | 需求预测建模 |
| 生态整合 | Ibis SQL前端/ConnectorX | 与现有SQL系统无缝衔接 |

### 1亿行RFM基准（16核机器，2026-06实测）

| 框架 | 内存峰值 | 耗时 | 差值 |
|------|:------:|:---:|------|
| Pandas | 32GB | 420秒 | 基线 |
| Polars | 4GB | 28秒 | **15x快 + 8x省内存** |

### 窗口函数专项测试（1亿行）

| 操作 | Pandas | Polars | 加速比 |
|------|:------:|:-----:|:-----:|
| 复杂窗口函数 | 95秒 | 8秒 | **11.9x** |

## DuckDB：第三种力量（2026-06新增）

### Polars vs DuckDB vs Pandas 基准（10M行）

| 操作 | Pandas | Polars | DuckDB | 最佳 |
|------|--------|--------|--------|:---:|
| CSV读取 | 1x | **7.7x** | 6x | Polars |
| GroupBy聚合 | 1x | 8.7x | **9.4x** | DuckDB |
| Join | 1x | **5x** | 4x | Polars |
| 窗口函数 | 1x | - | **10x** | DuckDB |
| 峰值内存 | 最高 | **低30-60%** | 中等(可溢出磁盘) | Polars |

### DuckDB独有优势

| 维度 | DuckDB优势 |
|------|-----------|
| SQL原生 | 团队会SQL→零学习成本，复杂查询比DataFrame API更易维护 |
| 文件直查 | `SELECT FROM 'data.parquet'` 无需加载到内存 |
| 磁盘溢出 | 数据超过内存自动spill，Polars惰性模式无法处理超内存操作 |
| 联邦查询 | ATTACH多数据库，跨源聚合无需ETL |

### 三引擎混合栈（2026最佳实践）

```
DuckDB → Polars → Pandas
  ↓         ↓         ↓
 SQL准备   特征工程   ML/可视化
```

| 阶段 | 工具 | 典型操作 |
|------|------|---------|
| 数据准备 | **DuckDB** | 多表JOIN、复杂聚合、窗口函数、跨源查询 |
| 特征工程 | **Polars** | 惰性求值、列变换、类型转换、流式写入 |
| ML集成 | **Pandas** | scikit-learn、XGBoost、matplotlib/seaborn |

```python
# 混合栈示例：Arrow零拷贝串联
import duckdb, polars as pl

# DuckDB做SQL聚合
result = duckdb.sql("""
    SELECT brand, category, SUM(amount) as revenue,
           COUNT(DISTINCT customer_id) as customers
    FROM 'sales_2026.parquet'
    WHERE sale_date >= '2026-01-01'
    GROUP BY brand, category
""").pl()  # → Polars (零拷贝)

# Polars做特征工程
features = result.with_columns([
    (pl.col("revenue") / pl.col("customers")).alias("arpu"),
    pl.col("revenue").rank("dense").over("brand").alias("cat_rank")
])

# → Pandas做ML
pdf = features.to_pandas()
```

### 零售场景选型速查

| 场景 | 数据量 | 推荐工具 | 原因 |
|------|--------|:---:|------|
| 临时探索性SQL | 任意 | **DuckDB** | SQL直写，无需Python脚本 |
| 多品牌跨库聚合 | 百万-千万 | **DuckDB** | ATTACH联邦查询 |
| 定时ETL流水线 | 千万-亿 | **Polars** | 惰性+流式+断点续传 |
| 实时看板数据 | 持续流式 | **Polars 2.0** | streaming=True |
| 机器学习/预测 | <百万 | **Pandas** | sklearn/LightGBM生态 |
| 销售日报PDF | 万-十万 | **DuckDB+Pandas** | SQL出数→Pandas画图 |

## 关联知识
- [[SQL查询性能优化]]
- [[ETL架构选型]]
- [[零售数据仓库SQL实践]]
- [[data_quality_governance|数据质量常态化治理]]
- [[duckdb_olap_engine_2026|DuckDB嵌入式OLAP引擎]]
- [[streamlit_dashboard_2026|Streamlit生产级实践]]
- [[data_library_selection_guide_2026|数据分析库选型决策指南]]
- [[2026-06-09_Scopir_Python数据分析库2026横评]]
- [[2026-06-09_Kanaries_Polars_vs_Pandas_2026深度评测]]
- [[2026-06-10_CSDN_Polars_MLflow_Streamlit工程化2026]]
- [[2026-06-11_chenxutan_Polars深度实战Rust架构]]
- [[retail_analytics_reporting_2026]]
- [[python_data_stack_decision_2026|Python数据栈边界决策框架]] ⭐ NEW
- [[python_sql_integration_patterns_2026|Python Pandas+SQL集成实战]] ⭐ NEW
- [[2026-08-06_Pandas_3.0_CoW与Arrow字符串后端落地基准]] — Pandas 3.0 正式版基准（影响对照组口径）⭐ NEW

## Python项目默认技术栈2026（2026-06新增）
详见 [[python_dev_stack_2026]] — uv+Ruff+Ty+Polars四件套替代传统8+工具链，统一pyproject.toml配置

## Polars Rust 架构深度解析（2026-06新增）

### 底层三大引擎

```
Rust 核心 (无GIL/内存安全/零成本抽象)
         +
  Apache Arrow 列式存储 (连续内存/SIMD/零拷贝)
         +
  Rayon 多线程引擎 (自动任务分解到多核)
```

### PDS-H 官方基准（10GB数据，Polars团队2025.05发布）

| 操作 | Polars 流式引擎 | Pandas | 差距 |
|------|---------------|--------|:---:|
| 全量处理 | 3.89秒 | 365.71秒 | **94倍** |
| 读取(240M行Parquet) | 8.7秒 | 41.2秒 | 4.7x |
| 过滤 | 0.34秒 | 3.8秒 | 11x |
| 分组聚合 | 1.8秒 | 18.4秒 | 10x |
| 排序 | 1.3秒 | 14.1秒 | 10.8x |

### Lazy Execution 四大优化详解

| 优化 | 原理 | 效果 |
|------|------|------|
| **谓词下推** | 过滤条件推至数据源层，只读需要的行 | 可能只读10GB而非1TB |
| **列裁剪** | 100列CSV只选3列时仅解析3列 | 减少90%+无用IO |
| **聚合下推** | 利用Parquet统计信息(min/max)跳过数据块 | 跳过不需要的Row Group |
| **常量折叠** | `col*2+10`编译期重写为`col*constant` | 减少运行时计算 |

### 8核CPU 1000万行实测

| 操作 | Polars | Pandas | 倍差 |
|------|--------|--------|:---:|
| 读取 | 1.14秒 | 5.23秒 | 4.6x |
| 聚合 | 0.92秒 | 8.97秒 | **9.8x** |

### 2026年生态数据

| 指标 | 数值（2026-06） |
|------|--------------|
| GitHub Stars | **80,000+** ⚠️ |
| 贡献者 | 500+ |
| 月下载量 | 500万+ ⚠️ |
| Discord成员 | 20,000+ |
| 企业采用 | Databricks(Delta Lake)/Kaggle(30%+Notebook)/金融科技 |

### 2026下半年路线图

| 特性 | 状态 | 说明 |
|------|------|------|
| GPU加速 | 🚀 实验性 | CUDA后端 |
| 分布式执行 | 🚀 计划中 | 集成Ray/Dask |
| SQL增强 | 🚀 计划中 | 完整SQL 2003兼容 |
| 文件格式 | 🚀 计划中 | Avro/Iceberg原生支持 |

### 迁移路线图

```python
# 混合策略：Polars做ETL → Pandas做ML/可视化
df_pl = pl.scan_csv("huge_file.csv").filter(...).collect()
df_pd = df_pl.to_pandas()  # 零拷贝转换
model = LinearRegression().fit(df_pd`x`, df_pd["y"])
```

## Polars + MLflow + Streamlit 工程化三件套（2026-06新增）

### 性能实测（生产环境）

| 场景 | Pandas | Polars | 倍数 |
|------|--------|--------|:---:|
| 12GB信用卡交易处理 | 187秒/内存41GB | 23秒/内存8.2GB | **8.1x** |
| 出行特征计算 | 基准线 | — | **5.3x** |
| 跨境电商ETL(12源增量) | 3小时 | 22分钟 | **8.2x** |
| 风控模型特征更新(每小时) | 45分钟 | <6分钟 | **7.5x** |
| 150GB日志处理 | 内存128GB | 内存18GB | **7.1x内存** |

### 三件套协同架构

```
数据采集(Polars)  →  模型管理(MLflow)  →  应用交付(Streamlit)
    ↓                    ↓                     ↓
 惰性求值/流式ETL    实验追踪/Registry    交互看板/业务决策
    ↓                    ↓                     ↓
 跨12源数据增量抽取  四阶段模型治理        Nginx+Gunicorn部署
```

### MLflow模型治理四阶段

```
注册模型 → Staging(测试) → Production(生产) → Archived(归档)
```

实际效果：某银行上线周期7天→4小时，故障回滚小时级→分钟级

### 渐进式引入策略

1. `memory_profiler`识别热点（read_csv/merge/groupby.agg/pivot_table）
2. 独立模块Polars重写，`to_pandas()`导出兼容下游
3. Workshop现场对比性能，建立团队共识

### 核心理念

> Polars保证**数据可信**，MLflow保证**模型可信**，Streamlit保证**交付可信**——从原始日志到业务决策的全链路可追溯体系。

## Polars 2.0 核心升级详解（2026-06新增）

### 2.0 vs 1.x 关键演进

| 特性维度 | Polars 1.x | Polars 2.0 |
|---------|-----------|-----------|
| 执行引擎 | LazyFrame基础优化 | **Arrow Flight SQL Planner**，谓词下推至Parquet页级 |
| 字符串处理 | Rust std::string，无SIMD | **SIMD向量化正则引擎**，UTF-8边界自动对齐 |
| 流式执行 | 不支持 | **streaming=True**，TB级避免全量内存驻留 |
| 物理计划剪枝 | 无 | 投影列裁剪 + 冗余Filter合并 |
| 声明式管道 | 无 | pipe()+**collect_schema()**，模式感知清洗 |

### 关键性能基准（10GB Parquet TPC-DS lineitem）

| 策略 | 初始化耗时 | 内存峰值 |
|------|-----------|---------|
| 默认Schema推断 | 1.82s | 426MB |
| **FileMetaData预读+列裁剪** | **0.09s (20x)** | **17MB** |

### 10M行等值Join

| 策略 | 内存峰值 | GC暂停次数 |
|------|---------|-----------|
| std::unordered_map | 2.1GB | 17 |
| **内联预分配+arena** | **1.3GB** | **0** |

### 10GB Parquet清洗参数实测

| 参数组合 | 峰值内存 | 加载耗时 |
|---------|---------|---------|
| rechunk=True | 3820MB | 42.1s |
| **low_memory=True** | **1960MB (降49%)** | 58.7s |
| chunked_buffer=128MB | 2410MB | 46.3s |

### 生产环境迁移效果
- 12TB ETL流水线：编译阶段错误检出率 **+73%**
- collect()前内存峰值 **-41%**
- explain(optimized=True) 可直接定位冗余cast操作

### 声明式管道范式迁移

```python
# Polars 2.0：模式感知声明式管道
lazy_df = (
    pl.scan_parquet("data.parquet")
    .pipe(lambda lf: lf.filter(pl.col("age") > 18))
    .pipe(lambda lf: lf.with_columns(
        pl.col("salary").log10().alias("log_salary")
    ))
    .collect_schema()  # 提前捕获字段类型变更，编译期校验
)
```

### 2.0与Dask/Delta Lake互操作
- Arrow IPC流式传输 + LZ4压缩：平均延迟591ms，吞吐167MB/s
- write_metadata=True减少Dask侧schema解析37%

## Polars 2.0 + Arrow 18.0 深度协同与GPU Offload（2026-06新增）⭐

### 零序列化清洗加速

Polars 2.0与Apache Arrow 18.0联合演进，通过零拷贝共享内存布局实现2-7x清洗加速：

| 操作（10GB日志） | Polars 1.x + Arrow 15.0 | Polars 2.0 + Arrow 18.0 | 提升 |
|------|-------|-------|:---:|
| 缺失值填充(forward-fill) | 420ms | 187ms | 2.25x |
| 时间窗口聚合(5min rolling) | 690ms | 312ms | 2.21x |
| 正则提取+结构化解析 | 1120ms | 495ms | 2.26x |

### 零拷贝 vs 传统Pandas（10M行混合数据）

| 操作 | Pandas | Polars+Arrow | 提升 |
|------|--------|-------------|:---:|
| Filter + Select | 482ms | 67ms | 7.2x |
| GroupBy + Agg | 1130ms | 215ms | 5.3x |

### GPU Offload预览版（A100实测）

CUDA Graph驱动的列式算子卸载模型：

| 算子组合 | 传统Stream | CUDA Graph | 提升 |
|---------|-----------|-----------|:---:|
| Filter + Join | 18.3 GB/s | 32.7 GB/s | 78.7% |
| Filter + Join + Aggregate | 11.6 GB/s | 25.9 GB/s | 123.3% |

### 金融验证：PB级日志清洗

某头部金融风控平台：端到端延迟 **8.2s→147ms**（55x提升），Flink Checkpoint对齐 **3.4s→210ms**。

### 三项企业级特性前瞻（2026 Q1）

| 特性 | 说明 |
|------|------|
| Schema Drift自愈引擎 | 基于Delta Lake 3.0元数据变更实时修复，新增非空字段自动注入默认值<200ms |
| GDPT/CCPA双模脱敏 | 零信任脱敏管道，列级访问控制策略嵌入 |
| 跨云联邦清洗 | S3/GCS/Azure Blob元数据同步 + 分布式Predicate Pushdown |

## 关联知识（续）
- [[2026-06-18_CSDN_Polars_2.0_大规模清洗优化]] — Polars 2.0新版实测来源
- [[2026-06-24_Polars_2.0_Arrow_18.0深度协同]] — Polars 2.0 + Arrow 18.0深度协同来源 ⭐ NEW
- [[2026-06-27_今日头条_Polars_DuckDB_Pandas三引擎实测]] — 1000万行/5GB三引擎实测126x DuckDB
- [[2026-06-27_chenxutan_Polars深层架构与生态2026]] — Polars深层Rust架构与2026生态全景

## Polars 2.0 大规模数据清洗范式跃迁（2026-07新增）⭐

> 来源：[[2026-07-28_CSDN_Polars_2.0_清洗范式跃迁]]

Polars 2.0 用零拷贝内存 + LazyFrame 全链路惰性执行 + 原生并行流式 I/O，把 TB 级清洗拉到单机亚秒级。CSDN 深度评测实测：

| 场景 | Pandas/Dask | Polars 2.0 | 提升 |
|------|-------------|-------------|------|
| 10M 行清洗 | 8.2s | 1.9s | 4.3× |
| 综合清洗 vs Pandas | 基线 | — | **最高 42.6×** |
| 内存 vs Dask | 基线 | — | **低 68.7%** |
| 10GB Parquet | 8.7s/4.2GB | 3.1s/1.9GB | 2.8× / 省 2.2× |

工程要点：LazyFrame 解耦（`.collect()` 才执行 + 谓词下推/投影裁剪）、Rayon 多线程 + SIMD 向量化清洗、优先 `scan_*` 避免过早物化、声明式 YAML 质量约束 + CI Schema 校验。类型系统差异（PostgreSQL 四舍五入 vs Spark 向零截断）需在跨引擎迁移时显式治理。

> 服装零售：多品牌 TB 级 ETL/清洗（POS/ERP/WMS 异构日志合并、会员行为嵌套展开、会话切分）可用 Polars 2.0 单机替代部分 Spark 任务。

## 2026年1000万行/5GB CSV三引擎实测（2026-06新增）

### 实测基准对比

2026年4月，今日头条发布三引擎1000万行CSV同机实测：

| 指标 | Pandas | Polars | DuckDB | 结论 |
|------|--------|--------|--------|------|
| 加载速度 | 8分12秒 | 9秒 | **3.8秒** | DuckDB 126x |
| 内存占用 | 5.2GB | 0.8GB | **0.3GB** | DuckDB最低 |
| 筛选速度 | 1x基准 | 5x | 视场景 | Polars最优 |
| 加速比 | 1x | 54x | **126x** | DuckDB加载领先 |

### 50GB混合流水线范式

```python
import duckdb, polars as pl, pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 阶段1: DuckDB 扛体量—从50GB磁盘预筛选
raw = duckdb.sql("""
    SELECT user_id, event_type, amount, created_at
    FROM 'data/events_*.parquet'
    WHERE created_at >= '2025-01-01' AND amount BETWEEN 10 AND 50000
""").pl()  # 零拷贝→Polars

# 阶段2: Polars 提速度—多线程特征工程
features = (
    raw.with_columns([
        pl.col("created_at").dt.hour().alias("hour"),
        (pl.col("amount") / pl.col("amount").mean().over("user_id")).alias("rel_amount"),
    ])
    .group_by("user_id").agg([
        pl.col("amount").mean().alias("avg_amount"),
        pl.col("event_type").n_unique().alias("unique_events"),
        pl.col("hour").mode().first().alias("peak_hour"),
    ]).collect()
)

# 阶段3: Pandas 连生态—ML建模
X = features.to_pandas().drop("user_id", axis=1)
model = RandomForestClassifier().fit(X, labels)
```

### 三引擎分工公式

```
DuckDB("扛体量") → Polars("提速度") → Pandas("连生态")
超内存大文件SQL       复杂多列转换           ML/可视化
126x加载              5-10x多线程           生态最全
```

> **关键结论**：Apache Arrow零拷贝串联是关键——DuckDB→`.pl()`→Polars→`.to_pandas()`，全程不额外占内存，2026年最优解是三者协同而非二选一。

## Pandas 3.0 + Arrow 零拷贝互操作（2026-07新增）⭐

### Pandas 3.0 重大变革（2026-01发布，最新3.0.4于6月28日）

> 来源：[[2026-07-03_Pandas官方_Pandas_3.0]]

| 变化 | 说明 | 对数据分析的影响 |
|------|------|-----------------|
| **Arrow-backed Dtypes** | 底层全面转向Apache Arrow列式格式 | 与Polars/DuckDB零拷贝互操作 |
| **Copy-on-Write 默认** | 修改DataFrame子集自动创建副本 | 解决"SettingWithCopyWarning"，数据更安全 |
| **API现代化** | 移除多个历史deprecated API | 需检查存量代码兼容性 |
| **Streamlit兼容** | Streamlit 1.56+支持Pandas 3.x | 无缝升级看板 |

版本迭代：3.0.0(1月)→3.0.1(2月)→3.0.2(3月)→3.0.3(5月)→**3.0.4(6月28日)**

### Polars + Arrow 零拷贝互操作实战（2026-05）

> 来源：[[2026-07-03_PyTutorial_Polars_Arrow零拷贝互操作]]

Polars 所有数据以 Apache Arrow 内存格式存储，与 Arrow 生态工具实现零拷贝共享：

**跨工具零拷贝链路**：
```
Parquet (PyArrow读取)
  → Polars (from_arrow, 零拷贝)
    → DuckDB (to_arrow → SQL查询, 共享内存)
      → Streamlit (to_arrow → 展示, 零拷贝)
```

| 互操作 | 方法 | 特性 |
|--------|------|------|
| Polars → PyArrow | `df.to_arrow()` | 零拷贝，共享内存池 |
| PyArrow → Polars | `pl.from_arrow(arrow_table)` | 零拷贝 |
| Polars → DuckDB | `to_arrow()` → `duckdb.sql().arrow()` | 双向零拷贝 |
| Polars → Pandas 3.0 | `df.to_pandas()` | Arrow-backed零拷贝 |

**服装零售实战全链路**：
```python
# 多品牌销售数据全链路零拷贝
import pyarrow.parquet as pq, polars as pl, duckdb

arrow_tbl = pq.read_table("multi_brand_sales.parquet")  # PyArrow读取
df = pl.from_arrow(arrow_tbl)  # Polars零拷贝

agg = duckdb.sql("""
    SELECT brand, category, SUM(amount) as revenue
    FROM arrow_tbl GROUP BY brand, category
""").pl()  # DuckDB SQL → Polars零拷贝

agg.write_parquet("brand_agg.parquet")  # 输出
```
全程无数据拷贝，千万级交易数据秒级完成。

### 三引擎+零拷贝定位更新（2026-07）

| 维度 | Pandas 3.0 | Polars 1.x | DuckDB 1.5 |
|------|-----------|------------|------------|
| Arrow集成 | Arrow-backed (新) | Arrow-native (原生) | Arrow读写 |
| 零拷贝互操作 | ✅ 支持 | ✅ 原生 | ✅ Arrow |
| CoW | ✅ 默认开启 | N/A | N/A |
| 适用场景 | 探索分析+ML | ETL管道+大数据 | SQL聚合+窗口函数 |

## 腾讯云千万级实测：五大操作全链路 5.9x（2026-07新增）⭐

> 来源：[[2026-07-06_腾讯云_Polars_Pandas千万级实测]]

### 测试环境

| 项目 | 配置 |
|------|------|
| 硬件 | 8核16G服务器 |
| Python | 3.12.1 / Pandas 2.2.0 / Polars 0.20.15 |
| 数据量 | 1000万行 × 12列（CSV 567MB） |

### 五大操作实测

| 操作 | Pandas | Polars Eager | Polars Lazy | 加速比 |
|------|--------|-------------|------------|:---:|
| CSV载入 | 12.40s (1.8GB) | 2.10s (0.9GB) | — | **5.9x** |
| 过滤 | 0.38s | 0.09s | 0.07s | **5.4x** |
| 分组聚合 | 1.42s | 0.31s | 0.22s | **6.5x** |
| Join合并 | 3.85s | 0.52s | — | **7.4x** |
| 排序 | 4.67s | 0.85s | — | **5.5x** |
| **全链路** | **22.72s** | **3.87s** | — | **5.9x** |

### 公平修正：Pandas+PyArrow后端

| 操作 | Pandas原生 | Pandas+PyArrow | Polars |
|------|-----------|---------------|--------|
| CSV载入 | 12.40s | 3.21s | 2.10s |
| 分组聚合 | 1.42s | 0.89s | 0.31s |
| Join合并 | 3.85s | 1.95s | 0.52s |

> PyArrow后端缩小CSV差距（12.4→3.2s），但GroupBy/Join仍3-4x差距——单线程架构的计算瓶颈无法被内存格式优化弥补。

### 迁移决策（四档数据量）

| 数据量 | 推荐方案 |
|--------|---------|
| <10万行 | Pandas，迁移无意义 |
| 10万~500万行 | Pandas+PyArrow后端 |
| 500万~5000万行 | **Polars（单机最优解）** |
| >5000万行 | Polars Lazy+DuckDB |

### 渐进迁移策略

新模块用Polars → 旧模块按需重构 → `to_pandas()`零拷贝转换毫秒级 → 不构成瓶颈。

## Tech Insider 企业级基准与TCO（2026-07新增）⭐

> 来源：[[2026-07-06_TechInsider_Polars_Pandas企业级TCO_2026]]

### H2O.ai GroupBy基准（Polars 1.24.0 vs Pandas 2.2.3 / 16核64GB）

| 任务 | Polars | Pandas | 加速比 |
|------|--------|--------|:---:|
| 100万行按ID求和 | 0.12s | 1.8s | 15x |
| 1000万行按ID求和 | 0.45s | 12.5s | 28x |
| 1亿行按ID求和 | 4.8s | 138s | 29x |
| 10亿行按ID求和(流式) | 45s | OOM崩溃 | N/A |

### TPC-H（SF=10，10GB）

| 查询 | Polars | Pandas | 加速比 |
|------|--------|--------|:---:|
| Q1 | 1.2s | 15s | 12.5x |
| Q5（5表Join） | 2.8s | 48s | 17x |
| Inner Join 1亿×1亿 | 8s | 120s | 15x |

### 五大企业案例

| 企业 | 场景 | 收益 |
|------|------|------|
| **GitHub** | 夜间ETL 400GB遥测 | 128GB/90min→32GB/11min，成本-75% |
| **JPMorgan** | 盘中VaR风险建模 | 22min→3min，满足15min SLA |
| **Cheddar** | 5000万月会话流式 | 3节点Spark→Polars单机 |
| **Netflix** | 推荐管道 | 双轨制：Polars重型+Pandas ML |
| **H2O.ai** | AutoML | 端到端6x墙钟提升 |

### 能源效率（VU Amsterdam 2026-03）

| 指标 | Polars | Pandas |
|------|--------|--------|
| 每1TB批次能耗 | 0.4 kWh | 1.6-2.0 kWh |
| 能效比 | 基准 | 3-5x更高 |

### TCO对比

| 维度 | Polars | Pandas |
|------|--------|--------|
| 1TB ETL AWS成本 | $3.40/次 | $18.60/次 (8x) |
| 年度节能(日1TB) | ~500 kWh | 基准 |

### 2026最终选择公式

- **<1GB + scikit-learn生态** → Pandas
- **>1GB + 生产ETL/实时分析/金融建模** → Polars
- **最务实** → 双轨制：Polars重型引擎+Pandas ML胶水，Arrow零拷贝串联

## TechInsider 2026-04 企业级基准与TCO更新（2026-07新增）⭐

> 来源：[[2026-07-12_TechInsider_Polars_Pandas_2026企业级基准与TCO]]

### 版本与市场（2026年4月）
- Polars 1.24.0（流式引擎正式版），Pandas 2.2.3（3.0仍Alpha）
- 周下载：Polars 280万（+250% YoY）vs Pandas 1,850万
- 职位年增：Polars +450% vs Pandas +2%；Polars数据工程师薪资$171K（溢价$14-19K）

### VU Amsterdam能源研究（2026-03，首个同行评审）
- Polars每次等效操作耗电比Pandas少 **3-5x**
- 每1TB批次：Polars **0.4kWh** vs Pandas **1.6-2.0kWh**

### 内存占用更新（10GB CSV）

| 场景 | Polars峰值 | Pandas峰值 | 缩减 |
|------|-----------|-----------|------|
| 10GB CSV解析+聚合 | 2.1GB | 18GB | **8.6x** |
| 50GB Parquet扫描(流式) | 1.8GB | 32GB | **17x** |
| 10亿行 group-by | 4.2GB | 45GB(OOM) | **10x+** |

### AWS TCO更新
- 1TB Parquet Join：Polars **$3.40/次** vs Pandas **$18.60/次**（8x大实例）
- Polars Cloud托管：**$0.05/GB** 扫描
- 日1TB管道年节省约500kWh

### Netflix双轨制确认
Netflix研究面向的推荐管道**保留Pandas**（笔记本<几GB），重聚合由Spark SQL上游处理。Polars+Pandas双轨为大规模ML特征工程标准范式。

## 关联知识（续）
- [[2026-07-06_腾讯云_Polars_Pandas千万级实测]] ⭐ NEW
- [[2026-07-06_TechInsider_Polars_Pandas企业级TCO_2026]] ⭐ NEW
- [[2026-07-06_CSDN_Apache_Arrow零拷贝2026]] ⭐ NEW
- [[2026-07-12_TechInsider_Polars_Pandas_2026企业级基准与TCO]] ⭐ NEW

## Polars 1.42 新特性（2026-07新增）⭐

> 来源：[[2026-07-15_Polars_1.42自适应云IO与矛盾过滤器]]

Polars 1.42（2026-06-29 发布）三大亮点：

| 特性 | 说明 | 实测数据 |
|------|------|---------|
| 自适应云I/O并发 | 动态调整S3/GCS/Azure并发请求数 | TPC-H SF=1000 整体2x，I/O密集最高4x |
| 矛盾过滤器消除 | 识别6类矛盾谓词，折叠为空结果，零扫描 | 程序化构建谓词自动短路 |
| is_sorted() 扩展 | DataFrame和Expr级别排序检测 | 支持descending和nulls_last |

6类矛盾检测：逻辑否定、反向比较、空成员、不相交范围、非重叠区间、范围外相等。云I/O优化零API变更，现有调用自动受益。

## Polars 1.42 分布式K8s + vs Spark基准（2026-07新增）⭐

> 来源：[[2026-07-22_Polars_1.42_分布式K8s_vs_Spark基准]]

### On-Prem K8s 部署

Polars Distributed 正式支持自有 K8s（EKS/AKS/GKE/minikube）一键 Helm 部署，无需将数据发送到托管服务。附带查询仪表板、实时性能分析、OpenLineage 数据血缘追踪。

### vs Spark 基准（PDS-H, 1TB）

| 场景 | Polars | Spark | 倍差 |
|------|--------|-------|------|
| 单节点 (128vCPU/512GB) | — | — | **6.4x 平均**（最高 38x） |
| 分布式集群 | — | — | **3.2x 平均**（1.6x-7.7x） |

### 智能优化器更新

| 版本 | 特性 | 效果 |
|------|------|------|
| 1.41 | 嵌套 CSE（公共子计划消除） | PV 设置 `POLARS_ALLOW_NESTED_CSPE=1` 启用 |
| 1.42 | 矛盾过滤器消除 | 谓词不可能满足时直接折叠为空，零扫描 |

### Parquet 性能

| 列数 | 旧解码器 | 新手写 Thrift | 加速比 |
|------|---------|-------------|--------|
| 100 | 2.12ms | 1.32ms | 1.61x |
| 1000 | 11.66ms | 4.43ms | 2.63x |
| 10000 | 117.4ms | 35.74ms | 3.29x |

### 服装零售场景价值

- 200+门店多品牌场景：单机 Polars 远超 Spark 单节点性能（6.4x），中型服装集团无需 Spark 集群即可处理全量 ETL
- K8s 部署：可与现有基础设施整合，Helm 一键部署

## Pandas 3.0 Arrow原生架构革命（2026-07新增）⭐

> 来源：[[2026-07-15_Pandas_3.0_Arrow原生架构革命]]（匡醍量化深度解读）

### Arrow String 30x 加速

| 指标 | 旧版(NumPy Object) | 3.0(Arrow String) | 提升 |
|------|-------------------|-------------------|:---:|
| 100万行6字符内存 | ~80MB | ~12MB | **6.7x** |
| str.upper() 计算 | baseline | 30x+ | **30x+** |
| CSV读取 | 需手动engine='pyarrow' | 自动最优 | 零配置 |

### Copy-on-Write 确定性语义

Pandas 3.0 默认开启 CoW：切片是引用（零开销），修改时自动创建副本。**彻底消除 SettingWithCopyWarning**。核心推动者：Patrick Hoefler（牛津→Citadel），几乎凭一己之力重构内部索引逻辑。

### Pandas 3.0 不可替代的价值

- **拥有 Index 和 MultiIndex**（Polars 没有且几乎永远不会加），支持 stack/unstack/pivot_table
- Scikit-learn / Statsmodels / 回测引擎生态血管里流淌 Pandas 格式
- 不脱离生态即可获得接近 Polars 的性能

## DuckDB vs Polars 共存生产模式（2026-07新增）⭐

> 来源：[[2026-07-15_DuckDB_vs_Polars_共存模式与生产决策]]（Danilchenko 生产实战）

### 核心公式：DuckDB做聚合，Polars做变换，Arrow做桥梁

```python
# DuckDB SQL 扫描+粗粒度聚合 → 零拷贝 → Polars 排名+业务逻辑
orders = duckdb.sql("""
    SELECT customer_id, product, sum(amount) AS revenue
    FROM 'data/orders/*.parquet'
    WHERE order_date >= '2026-01-01'
    GROUP BY customer_id, product
""").pl()  # 零拷贝转Polars

result = orders.with_columns(
    revenue_rank=pl.col("revenue").rank("dense", descending=True).over("customer_id")
).filter(pl.col("revenue_rank") <= 3)
```

### 内存抉择

140GB单文件：DuckDB 1.3GB（自动溢出）vs Polars 750MB（强制异步读）。分区使DuckDB降8x、Polars降4x——**文件布局比引擎选择更影响内存**。

### 选择快捷公式

- SQL团队/临时查询/不想配置 → DuckDB
- Python ETL管道/变换密集/静态类型 → Polars
- 严肃生产 → 两者配合，Arrow零拷贝串联

## Johal 2026生产力数据分析七栈基准（2026-07新增）⭐

> 来源：[[2026-07-18_Johal_2026生产力数据分析七栈基准]]

### 七栈全维度基准（M3 Max 36GB, 2.1M记录/1.8GB CSV）

| 工具 | 摄入 | 分组聚合 | 多表Join | 内存 |
|------|------|----------|---------|------|
| Polars 1.12 | 0.9s | **340ms** | 1.1s | 0.8GB |
| pandas 2.2 | 4.2s | 1,600ms | 8.9s | 3.1GB |
| DuckDB 1.3 | 1.4s | 520ms | **0.38s** | 0.6GB |
| SQLite 3.45 | 12.8s | 2.1s | 6.2s | 0.3GB |

### 关键倍差
- **Polars 4.7×** (340ms vs 1600ms 分组聚合) / 内存省**74%**
- **DuckDB 16×** (380ms vs 6.2s 多表Join+窗口函数)
- LazyFrame额外**40%**内存优化
- AI辅助(Cursor+Claude)：**5.7×**查询加速(8.5min→90s)/正确率85%

### Streamlit部署
- **90秒**纯Python部署(零前端代码)
- DuckDB+Streamlit 100-300ms / Polars+Streamlit 200-500ms
- **$14k-$22k/年**工具费用节省(pandas+Tableau→Polars+Streamlit)

### 决策矩阵
| 工具组合 | 单节点上限 | 仪表板延迟 | 学习曲线 |
|---------|-----------|-----------|---------|
| Polars+Streamlit | ~10GB | 200-500ms | 2-3天 |
| DuckDB+Streamlit | ~20GB | 100-300ms | 1天(SQL) |

## Danilchenko 240M行真实基准（2026-07刷新）⭐

> 来源：[[2026-07-25_Danilchenko_Polars_vs_Pandas_2026刷新基准]]、[[2026-07-28_CSDN_Polars_2.0_清洗范式跃迁]] ⭐ NEW

### 真实工作负载（240M 行点击流）

作者用真实 ETL 负载（而非玩具 CSV）刷新了结论——18 个 Parquet 文件、7 数值 + 3 字符串列、磁盘约 14GB、M2 Pro 16 核 32GB、每操作 5 次：

| 操作 | 结论 |
|------|------|
| joins / group-bys | Polars 约 **10x** 快 |
| Parquet 读取 | Polars 约 **5x** 快 |

### Pandas 3.0 GA（2026-01）缩小但未能消除差距

| 变化 | 说明 |
|------|------|
| PyArrow-backed strings 默认 | 底层字符串全面转向 Arrow 列式 |
| Copy-on-Write 默认 | 链式赋值直接报错，消除 SettingWithCopy 隐患 |
| `pd.col()` 表达式 API | 借鉴 Polars 表达式风格 |

> 引擎级差距在 Polars 1.43 / Pandas 3.0 上**保持不变**——DuckDB Labs 的 db-benchmark 在 0.5/5/50GB 三档持续追踪印证。

### 结论升级：从"二选一"到"双轨"

作者跑过两条生产管道后选**双轨**：Polars 做批量变换（bulk transforms），Pandas 做"最后一公里"（scikit-learn / matplotlib）。"该不该全面迁移？"答案仍是**否**——小交互数据集、sklearn 往返、字符串密集场景 Pandas 仍胜。

### 服装零售落地指引

- 多品牌季度汇总 / 全渠道年度交易 / VIP 全量行为分析（100 万行+）→ Polars 主场
- 探索性 Notebook（<1GB）+ ML 建模最后一公里 → 保留 Pandas
- 混合栈：`pl.scan_parquet(...).collect()` → `.to_pandas()` 零拷贝转 Pandas 做 sklearn / 可视化

## Polars 2.0 vs Pandas 2.2 大规模清洗基准（2026-07新增）⭐

> 来源：[[2026-07-31_Polars_2.0_Pandas_2.2大规模清洗基准]]

### 12 亿行 CSV 极限测试（16 核 / 64GB）

Polars 2.0 的 LazyFrame 将转换编译为逻辑计划，`.collect()` 才执行优化后的物理计划（谓词下推 / 投影裁剪）：

| 操作 | Polars 2.0 | Pandas 2.2 | 加速比 |
|------|-----------|-----------|:---:|
| 读取 + 类型推断 | 8.3s | 47.1s | **5.7×** |
| 多列条件过滤 + 字符串标准化 | 4.9s | 32.6s | **6.7×** |
| 分组填充缺失值 | 6.2s | 28.4s | **4.6×** |

### EPYC 7742 三引擎横向

| 任务 | Polars 2.0 | Pandas 2.2 | DuckDB 0.10 |
|------|-----------|-----------|------------|
| 缺失填充 + 类型校验 | 4.2s | 24.7s | 8.9s |
| 正则提取设备型号 | 3.1s | 19.3s | 6.4s |
| 条件去重（保留最新时间戳） | 2.8s | 31.5s | 7.2s |

综合：**吞吐提升 3.8×、内存下降 62%**（对比 Pandas/Dask）；启用 `streaming=True` + `low_memory=True`。

### pyinns 2026 真实基准（10M–100M 行，2026-03 刷新）

| 操作 | Polars(1.x) | Pandas(2.2+) | 倍差 |
|------|------------|-------------|:---:|
| 读 1GB CSV | ~1–3s | ~10–20s | 5–10× |
| 过滤 50M 行 | 0.2–0.8s | 3–12s | 5–20× |
| GroupBy+聚合 100M 行 | 1–5s | 15–60s | 5–30× |
| 峰值内存(100M 数值) | 0.5–2GB | 3–8GB | 3–6× 更低 |

Streaming 处理大于内存的数据集（`scan_csv().collect(streaming=True)` 自动 spill 到磁盘），Python 3.13 + uv 安装。

### 三层清洗架构

| 层 | 角色 |
|----|------|
| pandas | 交互式探索通用引擎 |
| polars | 生产级清洗重构向量化执行器（惰性+SIMD+流式） |
| 规则中枢 | 业务校验（类型/范围/唯一性） |

> 生态兼容断层：polars 对接 scikit-learn 需 `to_pandas()` 桥接。服装零售：多品牌 TB 级 ETL（POS/ERP/WMS 异构日志合并）可用 Polars 2.0 单机替代部分 Spark 任务；优先 `scan_*` + LazyFrame + `streaming=True`；缺失值按组广播填充 `fill_null(col.mean().over("category"))`。

> ⚠️ **软口径提示**：本批 5.7–6.7× 清洗加速为 1.2B 行 CSV 特定负载；与 kb_benchmarks `polars_vs_pandas_speed_multiplier=8`（通用聚合基准）口径不同（workload 不同），不构成硬矛盾。

## Pandas 3.0 正式版对基准口径的影响（2026-08-06）

pandas 3.0.0（2026-01-21 GA / 3.0.4 于 06-28）落地后，此前多数 "Polars vs Pandas" 基准的对照组（Pandas 2.x + object 字符串）已经过时，需注意三点口径变化：

1. **字符串密集型场景差距收窄**：Pandas 3.0 字符串列默认走 PyArrow 后端，`.str` 系操作快 5–10 倍、极端场景（`.str.upper()`）30 倍以上，内存最多降 50%。服装数据里款号/色号/尺码/门店编码都属此类，旧基准中 Polars 的字符串优势会被显著压缩。
2. **CoW 消除冗余拷贝**：Pandas 3.0 底层尽量用视图、仅在写入共享数据时才复制，此前为消 `SettingWithCopyWarning` 而写的防御性 `.copy()` 造成的额外开销消失。
3. **零拷贝换手不再有损耗**：双方都支持 Arrow PyCapsule 双向接口，"Polars 做清洗 → Pandas 做建模"的混合用范式换手成本趋近于零，进一步支持本库既有的"混合用而非二选一"结论。

> **结论不变但理由更新**：仍推荐 Polars 承担大体量清洗聚合、Pandas 承担生态兼容与建模；但选型理由从"Pandas 太慢"转为"分工不同"。详见 [[2026-08-06_Pandas_3.0_CoW与Arrow字符串后端落地基准]]。

## 2026-08 Polars 2.1 / Pandas 3.0 生产级基准刷新

**johal.in 50GB 实测**（32GB RAM）：Polars 2.1.0 在 CSV Join 上比 Pandas 3.0.1 快 **12.4x**、内存 **-60%**；DuckDB 1.2.3 比 Spark 4.0（100GB）延迟 **-89%**；自建 Polars+DuckDB 栈比托管(Fivetran+Snowflake) 成本 **$0.03/GB vs $0.18/GB、快 12x**；预测 2027 年 70% 生产分析用 Rust 工具（Polars/DataFusion）。

**ima.qq.com 10M 行**：过滤 6x / GroupBy 10x / Join 12x / 排序 10x / 字符串 11x / 滚动 9x；内存省 65–73%；Polars 月下载 3000 万（较 2024 初 +300%）。**itsourcecode 1M 行**：Read 9x / GroupBy 30x / Join 14x。**pyinns 10M 行**：Read 4.7x / GroupBy 5.4x；内存 ~450MB vs ~1.8GB。

**结论**：不该全面迁移，该全面评估——混合用（Polars 做 ETL/重计算，Pandas 做 ML/可视化）。12.4x Join / -60% 内存与 kb `speed_multiplier=8` 同属"数倍至十余倍"区间，口径差异（50GB join vs 千万行通用），**非硬矛盾**。

> 映射：内存实测补 [[arrow_zero_copy_interop_2026]]；混合用范式见 [[python_data_stack_decision_2026]]。

## 信息链

- **上游 · 来源支撑**：[[2026-06-07_Polars_2.0流式ETL]] · [[2026-06-12_CSDN_Python数据分析工作流2026]] · [[2026-06-15_CSDN_Python数据栈边界决策框架]] · [[2026-06-15_aimojo_Python_Pandas_SQL集成指南]] · [[2026-06-18_CSDN_Polars_2.0_大规模清洗优化]] · [[2026-06-21_DuckDB_1.5_Sirius_GPU加速]] · [[2026-06-24_Polars_2.0_Arrow_18.0深度协同]] · [[2026-06-27_今日头条_Polars_DuckDB_Pandas三引擎实测]] · [[2026-06-27_chenxutan_Polars深层架构与生态2026]] · [[2026-06-30_chenxutan_Polars_Pandas深度实测2026]] · [[2026-07-03_PyTutorial_Polars_Arrow零拷贝互操作]] · [[2026-07-03_Pandas官方_Pandas_3.0]] · [[2026-07-15_Polars_1.42自适应云IO与矛盾过滤器]] · [[2026-07-15_Pandas_3.0_Arrow原生架构革命]] · [[2026-07-15_DuckDB_vs_Polars_共存模式与生产决策]] · …(+28 更多)（本页事实来自这些原始采集）
- **本页定位**：concept —— Polars vs Pandas vs DuckDB 2026选型指南
- 关联实体：无
- 关联概念：[[SQL查询性能优化]] · [[ETL架构选型]] · [[duckdb_olap_engine_2026]] · [[streamlit_dashboard_2026]] · [[retail_analytics_reporting_2026]] · [[retail_data_workflow_2026]] · [[python_data_stack_decision_2026]] · [[data_quality_governance]] · [[python_dev_stack_2026]] · [[arrow_zero_copy_interop_2026]]
- 关联对比：无
- 关联打法：无
- ⚠️ **断点（指向未建页）**：[[零售数据仓库SQL实践]] · [[data_library_selection_guide_2026]] · [[streamlit_production_dashboard]] · [[python_sql_integration_patterns_2026]] · `x`（待补页或修正双链）

## 2026-08-15 更新（三引擎基准再校准）

- DuckDB 1.5.4 vs PostgreSQL 18.4 实测 TPC-H 1TB 平均 7.4x（扫描 7.4x、JOIN 5.2x）；与 [[SQL查询性能优化]] 的「按 workload 选引擎」一致——DuckDB 擅 SQL 聚合/即席、Polars 擅 ETL 流水线、PG/SQLite 擅事务。
- `pg_duckdb` 1.0 使 PG+DuckDB 共存成 2026 主流混合架构（PG 扛 OLTP + DuckDB 扛 OLAP = 138k 写/秒 + 7.8 GB/s）。
- 来源：[[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]]

## 关联页面
- [[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]]

- [[2026-06-06_Kanaries_Polars_vs_Pandas_2026]]
- [[2026-06-08_Polars_DuckDB_Pandas三大引擎对比]]
- [[2026-06-09_Kanaries_Streamlit_DataFrame优化2026]]
- [[2026-06-10_Streamlit官方_2026版本架构演进]]
- [[2026-06-14_AIFutureThinkers_Python默认技术栈2026]]
- [[2026-06-14_Scopir_Python数据分析库2026全景对比]]
- [[2026-06-24_DuckDB_vs_Polars_2026基准对比]]
- [[2026-06-30_Streamlit官方_2026全版本更新v1.53-v1.58]]
- [[2026-07-09_Danilchenko_DuckDB_vs_Polars_2026基准]]
- [[2026-07-22_2026现代Python数据栈]]
- [[2026-07-22_DuckDB_1.5.4_Quack_DuckLake]]
- [[arrow_zero_copy_interop_2026]]

- [[2026-08-09_DuckDB官方_v1.5系列与Python嵌入式分析范式]]

- [[2026-08-12_DuckDB官方_查询性能调优三层级实战]]
- [[2026-08-12_Polars2.1_Pandas3.0_生产级性能对比]]

## C轮更新（2026-08-26）：Johal 五引擎全谱基准（Pandas 3.0.1 / Polars 2.1.0 / DuckDB 1.2.3 / Spark 4.0.2 / DataFusion 0.12.1）

> 来源：[[2026-08-26_数据分析技术栈盘点与Polars_DuckDB性能基准]]

| 工具版本 | 10GB CSV 读取(s) | 50GB Join(s) | 100GB Groupby(s) | 内存(GB) | 每 1TB 成本($) |
|---|---|---|---|---|---|
| Pandas 3.0.1 | 42.1 | 210.5 | 380.2 | 14.2 | 0.18 |
| Polars 2.1.0 | 3.2 | 17.1 | 31.4 | 5.2 | 0.03 |
| DuckDB 1.2.3 | 2.8 | 14.5 | 27.9 | 3.8 | 0.02 |
| Spark 4.0.2 | 18.7 | 89.3 | 165.4 | 22.1 | 0.45 |
| DataFusion 0.12.1 | 2.1 | 11.2 | 20.8 | 2.9 | 0.02 |

**要点**：
- 三引擎谱系里 DuckDB/DataFusion 纯查询最快，Polars 加工+查询均衡，Pandas 生态兼容但性能垫底（比 Polars 慢 10-13x、成本 6 倍）。
- 零售迁移案例：80GB/日 parquet，Fivetran+Snowflake → 自托管 Polars+DuckDB on K8s，p99 2.4s→120ms、报表 47min→2.3min、成本 -82%（$12k→$2.1k/月）。
- 选型结论：服装零售 35 品牌明细数据量 <10GB，**Polars+DuckDB 双引擎即全场景最优**；>100GB 才考虑 Spark。
- 与既有基准关系：08-12 源（Polars Join 12.4x vs Pandas）为两引擎专项对比，本轮为五引擎全谱，口径不同非矛盾。
