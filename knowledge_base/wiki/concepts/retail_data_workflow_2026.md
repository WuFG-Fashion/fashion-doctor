---
type: concept
title: 零售数据分析完整工作流(CRISP-DM)
tags: [retail, analytics, crisp_dm, eda, workflow, python, polars]
sources: [2026-06-12_CSDN_Python数据分析工作流2026, 2026-06-15_CSDN_Python数据栈边界决策框架]
created: 2026-06-12
updated: 2026-06-15
cross_refs: [[polars_vs_pandas_2026]], [[duckdb_olap_engine_2026]], [[SQL查询性能优化]], [[retail_analytics_reporting_2026]], [[python_data_stack_decision_2026]], [[data_library_selection_guide_2026]]
---

# 零售数据分析完整工作流(CRISP-DM)

> **一句话摘要**：CRISP-DM 七步数据分析工作流映射到服装零售场景，配合 Pandas/Polars/DuckDB 三引擎按数据规模选型，EDA 三类分析 + 可视化全家桶快速定位业务问题。

> **来源**：CSDN Python数据分析与可视化 2026
> **最后更新**：2026-06-12

## CRISP-DM 七步工作流 × 服装零售

| 步骤 | 通用描述 | 服装零售示例 |
|------|---------|-------------|
| 1. 定义问题 | 明确业务目标 | 提升季度销售额？哪些品类库存周转慢？ |
| 2. 数据获取 | 采集原始数据 | 销售记录/用户行为日志/库存表/广告投放 |
| 3. 数据清洗 | 处理缺失/异常/重复 | 处理退货负值/缺失尺码/重复订单 |
| 4. EDA | 探索性分析 | 按品类/季节/渠道分析销售趋势、价格段分布 |
| 5. 特征工程 | 构建特征变量 | 计算利润率/月度环比/客单价/连带率 |
| 6. 建模/可视化 | 预测/图表 | 预测下季销量/可视化区域热销品类 |
| 7. 解读与沟通 | 结论输出 | 生成管理层周报/Streamlit仪表盘 |

## 三引擎选型矩阵

| 数据规模 | 推荐引擎 | 典型场景 | 性能特征 |
|---------|---------|---------|---------|
| <10万行 | **Pandas** | 单店日销售/周报快速探索 | 易上手，生态全 |
| 10万-1000万行 | **Polars** | 全渠道月销售/RFM/用户路径 | Lazy求值，内存省87% |
| >1000万行 | **DuckDB** | 全年全品类/供应链分析/复杂SQL | 列式存储，SQL极快 |

### 混合栈最佳实践

```python
# 小数据探索 → Pandas
df_sample = pd.read_csv("daily_sales.csv")
df_sample.describe()

# 中等数据聚合 → Polars
sales_monthly = (
    pl.scan_parquet("sales/*.parquet")
    .group_by("category", "month")
    .agg(pl.sum("amount"))
    .collect()
)

# 大数据关联 → DuckDB
import duckdb
result = duckdb.sql("""
    SELECT c.region, SUM(s.amount) as total
    FROM sales_large s
    JOIN customers c ON s.customer_id = c.id
    GROUP BY c.region
""").df()
```

## EDA 三大核心分析

### 1. 单变量分析
- 直方图：客单价分布、SKU 价格分布
- 箱线图：异常值检测（异常退货/欺诈订单）
- 频数统计：品类销售件数排行

### 2. 多变量分析
- 散点图：广告投入 vs 销售额、价格 vs 销量
- 相关性热力图：各品类间的销售关联
- 成对关系图：毛利率/周转率/售罄率交叉分析

### 3. 时间序列
- 趋势分析：同比/环比销售走势
- 季节性分解：波段上货效果评估
- 异常检测：促销活动效果、突发事件影响

## 可视化工具全家桶

| 层级 | 工具 | 适用场景 | 推荐度 |
|------|------|---------|:---:|
| 基础 | Matplotlib | 精细控制图表 | ★★★★★ |
| 统计 | Seaborn | 统计图表/热力图 | ★★★★★ |
| 交互 | Plotly Express | 交互仪表盘/管理看板 | ★★★★★ |
| 现代 | Altair + Great Tables | 声明式/自动化报表 | ★★★★ |
| 自动化 | ydata-profiling | 一键数据概览报告 | ★★★★ |

### 服装零售图表推荐

| 分析需求 | 推荐图表 | 推荐工具 |
|---------|---------|---------|
| 品类销售占比 | 树状图(Treemap) | Plotly Express |
| 月度销售趋势 | 折线图 | Seaborn / Plotly |
| 用户转化路径 | 桑基图(Sankey) | Plotly |
| 区域销售分布 | 地图热力图 | Folium / Plotly |
| 价格-销量关系 | 散点图+颜色分组 | Plotly Express |
| 库存周转分析 | 热力图 | Seaborn |

## 三阶段学习路径

| 阶段 | 时间 | 内容 | 零售练习 |
|------|:---:|------|---------|
| 1 | 1-2周 | NumPy + Pandas + Matplotlib/Seaborn | 单品牌 CSV 分析 |
| 2 | 2-4周 | EDA + Plotly + Kaggle实战 | Superstore Sales 数据集 |
| 3 | 持续 | Polars + Streamlit + 统计建模 | 实时销售仪表盘 |

## Python数据栈边界速查（2026-06新增）

> 结合[[python_data_stack_decision_2026|Python数据栈边界决策框架2026]]，在CRISP-DM各阶段选择最佳引擎：

| CRISP-DM阶段 | <5GB | 5-100GB | >100GB |
|-------------|:---:|:---:|:---:|
| 数据获取 | Pandas read_csv | Polars scan_parquet | Spark read |
| 数据清洗 | Pandas | Polars Lazy | Spark DataFrame |
| EDA | Pandas + Seaborn | Polars + Plotly | DuckDB SQL |
| 特征工程 | Pandas + Sklearn | Polars + Sklearn | Spark ML |
| 建模 | Scikit-learn | Scikit-learn | Spark ML |
| 可视化 | Plotly Express | Polars→Pandas→Plotly | DuckDB→Plotly |

## 关联页面
- [[polars_vs_pandas_2026|Polars vs Pandas 2026]]
- [[duckdb_olap_engine_2026|DuckDB OLAP 引擎]]
- [[SQL查询性能优化|SQL 查询性能优化]]
- [[retail_analytics_reporting_2026|服装零售报表 2026]]
- [[data_library_selection_guide_2026|数据分析库选型指南]]
- [[python_data_stack_decision_2026|Python数据栈边界决策框架]] ⭐ NEW
- [[2026-06-12_CSDN_Python数据分析工作流2026]]

- [[2026-06-15_CSDN_Python数据栈边界决策框架]]
- [[2026-06-15_aimojo_Python_Pandas_SQL集成指南]]
- [[2026-06-24_Polars_2.0_Arrow_18.0深度协同]]
- [[2026-07-09_Nimbleway_2026零售数据分析指南]]
- [[python_dashboard_ecosystem_2026]]
- [[python_sql_integration_patterns_2026]]
- [[streamlit_dashboard_2026]]
- [[streamlit_production_dashboard]]
