---
type: source
title: DuckDB vs Polars 2026基准对比
tags: [duckdb, polars, benchmark, python, sql, olap]
sources: [2026-06-24_PyInns_DuckDB vs Polars 2026基准对比.md]
created: 2026-06-24
updated: 2026-06-24
cross_refs: [[duckdb_olap_engine_2026]], [[polars_vs_pandas_2026]], [[python_data_stack_decision_2026]]
---

# DuckDB vs Polars 2026基准对比

> **一句话摘要**：PyInns 2026年3月实测 DuckDB 1.2+ vs Polars 1.x，覆盖1亿-10亿行数据集，提供SQL vs表达式API双视角选型指南。
> **来源**：wiki/raw/articles/2026-06-24_PyInns_DuckDB vs Polars 2026基准对比.md
> **最后更新**：2026-06-24

## 核心要点

1. 两者单机速度差距在20-50%以内，DuckDB复杂SQL略优，Polars Python人体工学占优
2. Polars在简单Filter/GroupBy和流式DataFrame操作上有微弱优势；DuckDB在复杂Join+Window操作上更优
3. 10GB Parquet读取：Polars ~1.5-5s vs DuckDB ~2-6s；5亿行峰值内存：Polars ~1.5-5GB vs DuckDB ~2-6GB
4. 两者都基于Apache Arrow，零拷贝互转（`duckdb.sql("...").pl()` → Polars DataFrame）
5. 2026年推荐混合方案：DuckDB处理SQL报表 + Polars处理Python管道

## 关键数据

| 操作 | DuckDB | Polars | 场景 |
|------|--------|--------|------|
| 10GB Parquet读取 | 2-6s | 1.5-5s | Polars略优 |
| 5亿行Join+Window+Agg | 8-25s | 10-35s | DuckDB略优 |
| 10亿行GroupBy+Filter | 15-40s | 12-35s | Polars略优 |
| 5亿行峰值内存 | 2-6GB | 1.5-5GB | Polars略优 |

## 选型建议

| 场景 | 推荐 | 理由 |
|------|------|------|
| BI/报表/SQL分析 | DuckDB | 类PostgreSQL体验，MotherDuck云 |
| Python ETL管道 | Polars | Lazy DataFrame，Python生态集成 |
| 两者都需要 | 混合 | Arrow零拷贝互转，uv统一安装 |

## 关联页面

- [[duckdb_olap_engine_2026]] — DuckDB 1.5+Sirius GPU完整能力
- [[polars_vs_pandas_2026]] — Polars vs Pandas选型深度对比
- [[python_data_stack_decision_2026]] — Python数据栈三重边界决策框架
