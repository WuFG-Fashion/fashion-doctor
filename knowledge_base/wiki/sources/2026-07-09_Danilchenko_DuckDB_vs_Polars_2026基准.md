---
type: source
title: Danilchenko DuckDB vs Polars 2026基准评测
tags: [duckdb, polars, benchmark, python, olap, data_engineering]
sources: [https://www.danilchenko.dev/posts/duckdb-vs-polars/]
aliases: ["Danilchenko", "DuckDB", "vs", "Polars", "Danilchenko DuckDB vs Polars 2026基准评测"]
confidence: 第三方数据
brand_specific: false
created: 2026-07-09
updated: 2026-07-09
cross_refs: [[duckdb_olap_engine_2026]], [[polars_vs_pandas_2026]], [[python_data_stack_decision_2026]], [[data_library_selection_guide_2026]]
---

# Danilchenko DuckDB vs Polars 2026基准评测

> **一句话摘要**：2026年7月最新DuckDB 1.5.4 vs Polars 1.42.1深度对比——2TB Parquet扫描、12GB订单实测、内存模型剖析，结论：差异在舍入误差级别，文件分区比引擎选择对性能影响更大。

> **来源**：https://www.danilchenko.dev/posts/duckdb-vs-polars/
> **最后更新**：2026-07-09

## 核心要点

1. **性能差距极小**：大多数工作负载下DuckDB和Polars完成时间在舍入误差级别
2. **操作各有胜负**：DuckDB窗口函数领先/Polars CSV读取和Join更快/分组聚合平手
3. **内存是真正的分水岭**：DuckDB自动溢出开箱即用，Polars异步读取内存更优（750MB vs 1.3GB）
4. **文件布局＞引擎选择**：分区可将内存降低4-8倍
5. **最佳实践**：组合使用——DuckDB负责SQL聚合→Polars负责ETL管道→Arrow零拷贝串联

## 关键基准数据

| 测试 | DuckDB | Polars | 结论 |
|------|--------|--------|------|
| 2TB Parquet扫描 | **~45秒** | ~60秒 | DuckDB领先25% |
| 5GB数据集聚合 | **2.3秒** | 3.3秒 | DuckDB领先30% |
| 12GB订单分组聚合 | 秒级 | 秒级 | 平手 |
| 140GB文件峰值内存 | **1.3GB**(自动溢出) | 750MB(异步) | Polars内存更优 |
| 窗口函数 | 持续领先 | — | DuckDB优势场景 |
| CSV读取 | — | 持续领先 | Polars优势场景 |
| Join | — | 持续领先 | Polars优势场景 |

## 服装零售启示

- 多品牌SQL分析→**DuckDB**（联邦查询/自动溢出）
- 销售流水ETL管道→**Polars**（流式引擎/惰性求值）
- 两者协同：DuckDB粗粒度聚合→Polars精粒度转换→Arrow零拷贝

## 关联页面

- [[duckdb_olap_engine_2026]] — DuckDB嵌入式OLAP引擎
- [[polars_vs_pandas_2026]] — Polars vs Pandas选型指南
- [[python_data_stack_decision_2026]] — Python数据栈边界决策框架
- [[data_library_selection_guide_2026]] — 数据分析库选型决策指南
- [[arrow_zero_copy_interop_2026]] — Arrow零拷贝互操作

## 待办 / 待验证

- 无矛盾：PDS-H 94x、Arrow零拷贝、DuckDB 10x窗口函数等已有基准一致
