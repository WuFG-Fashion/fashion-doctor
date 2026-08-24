---
type: source
title: Polars 2.0 大规模CSV/Parquet清洗新API与旧版对比实测
tags: [polars, python, benchmark, parquet, csv, streaming]
sources: [wiki/raw/articles/2026-06-18_CSDN_Polars_2.0_大规模数据清洗优化.md]
created: 2026-06-18
updated: 2026-06-18
cross_refs: [[polars_vs_pandas_2026]], [[python_data_stack_decision_2026]], [[duckdb_olap_engine_2026]]
---

# Polars 2.0 大规模CSV/Parquet清洗新API与旧版对比实测

> **一句话摘要**：Polars 2.0引入Arrow Flight SQL Planner实现谓词下推至Parquet页级、SIMD正则引擎、流式执行，Mem峰值降49%，元数据预读加速20倍，零拷贝Join消除GC停顿。

> **来源**：wiki/raw/articles/2026-06-18_CSDN_Polars_2.0_大规模数据清洗优化.md
> **最后更新**：2026-06-18

## 核心要点

1. **Arrow Flight SQL Planner**：谓词下推至Parquet页级，10GB文件初始化从1.82s降至0.09s（**20倍**）
2. **SIMD向量化正则引擎**：字符串处理吞吐提升，UTF-8边界自动对齐
3. **流式执行streaming=True**：避免全量内存驻留，low_memory模式峰值1960MB（vs 3820MB，降**49%**）
4. **零拷贝Join**：arena allocator替代std::unordered_map，内存从2.1GB→1.3GB，GC暂停归零
5. **声明式管道**：pipe()+collect_schema()实现模式感知清洗，12TB ETL编译阶段错误检出+73%

## 关键性能基准

### 10GB Parquet读取（TPC-DS lineitem）

| 策略 | 初始化耗时 | 内存峰值 |
|------|-----------|---------|
| 默认Schema推断 | 1.82s | 426MB |
| **FileMetaData预读+列裁剪** | **0.09s** | **17MB** |

### 10M行等值Join

| 策略 | 内存峰值 | GC暂停次数 |
|------|---------|-----------|
| std::unordered_map | 2.1GB | 17 |
| **内联预分配+arena** | **1.3GB** | **0** |

### 10GB Parquet清洗参数组合

| 参数组合 | 峰值内存 | 加载耗时 |
|---------|---------|---------|
| rechunk=True | 3820MB | 42.1s |
| low_memory=True | 1960MB | 58.7s |
| chunked_buffer=128MB | 2410MB | 46.3s |

## 范式迁移：链式→声明式

Polars 2.0引入`pl.Expr.pipe()`与`pl.LazyFrame.collect_schema()`，使清洗逻辑可静态验证。12TB ETL流水线迁移后collect()前内存峰值降**41%**。

## 关联页面

- [[polars_vs_pandas_2026]] — Polars 5-11x快/内存省87%/选型矩阵
- [[python_data_stack_decision_2026]] — Python数据栈三重边界决策框架
- [[duckdb_olap_engine_2026]] — DuckDB嵌入式OLAP引擎10x窗口函数
- [[python_sql_integration_patterns_2026|Python Pandas+SQL集成实战]] — 三模式分层集成
