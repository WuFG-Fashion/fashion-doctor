---
type: source
title: DuckDB vs Polars 2026：共存模式与生产决策
tags: [duckdb, polars, benchmark, production, arrow, sql, etl, memory]
sources: [2026-07-15_Danilchenko_DuckDB_vs_Polars_2026生产实战对比.md]
created: 2026-07-15
updated: 2026-07-15
cross_refs: [[polars_vs_pandas_2026]], [[duckdb_olap_engine_2026]], [[arrow_zero_copy_interop_2026]], [[multi_brand_unified_analytics|多品牌统一数据分析架构]]
---

# DuckDB vs Polars 2026：共存模式与生产决策

> **一句话摘要**：Danilchenko 基于数百 GB Parquet 管道迁移实战，核心结论：停止对立，DuckDB 做聚合（SQL）、Polars 做变换（表达式），Arrow 做桥梁，零拷贝互操作。分区比引擎选择更影响内存（8x/4x）。

## 核心要点

1. **2TB Parquet**：DuckDB ~45s vs Polars ~60s，差距约 33%，非营销宣传的 10x
2. **操作分胜负**：CSV/Join → Polars 胜，窗口函数 → DuckDB 胜，Group-by → 持平
3. **内存才是分水岭**：DuckDB 自动溢写磁盘（零配置），Polars 需手动 streaming engine
4. **分区比引擎重要**：分区数据使 DuckDB 峰值内存降 8x，Polars 降 4x
5. **共存模式推荐**：DuckDB SQL 扫描+聚合 → `.pl()` 零拷贝转 Polars → Polars 表达式做排名/变换/特征工程

## 详细内容

### 2TB Parquet 基准 (codecentric)

| 场景 | DuckDB 1.5.4 | Polars 1.42.1（默认） | Polars（强制异步读） |
|------|-------------|---------------------|---------------------|
| 2TB扫描 | **~45s** | ~60s | ~100s |
| 140GB单文件 | 领先~1s | — | — |

### 内存对比 (140GB单文件)

| 引擎 | 峰值内存 |
|------|----------|
| DuckDB | **~1.3 GB** |
| Polars（默认mmap） | ~17 GB（页缓存膨胀，非真实工作集） |
| Polars（强制异步读） | **~750 MB**（低于DuckDB） |

### 共存代码模式

```python
# DuckDB 负责文件扫描和粗粒度聚合
orders = duckdb.sql("""
    SELECT customer_id, product, sum(amount) AS revenue
    FROM 'data/orders/*.parquet'
    WHERE order_date >= '2026-01-01'
    GROUP BY customer_id, product
""").pl()  # 零拷贝转 Polars

# Polars 负责排名和业务逻辑
result = orders.with_columns(
    revenue_rank=pl.col("revenue").rank("dense", descending=True).over("customer_id")
).filter(pl.col("revenue_rank") <= 3)
```

## 关联页面

- [[polars_vs_pandas_2026]] — Python 数据处理引擎选型基准
- [[duckdb_olap_engine_2026]] — DuckDB 嵌入式 OLAP 引擎
- [[arrow_zero_copy_interop_2026]] — Apache Arrow 零拷贝互操作
- [[multi_brand_unified_analytics|多品牌统一数据分析架构]]
- [[data_library_selection_guide_2026|数据分析库选型决策指南2026]]
