---
type: source
title: Danilchenko Polars vs Pandas 2026 真实基准刷新
tags: [polars, pandas, python, benchmark, etl, data_analysis]
sources: [https://danilchenko.dev/posts/polars-vs-pandas/]
created: 2026-07-25
updated: 2026-07-25
cross_refs: [[polars_vs_pandas_2026]]
---

# Danilchenko：Polars vs Pandas 2026 真实基准刷新

> **一句话摘要**：2026-07 刷新实测——240M 行真实点击流负载下 Polars joins/group-bys 约 10x、Parquet 读取约 5x 快于 Pandas；Pandas 3.0 GA（PyArrow 字符串 + CoW 默认）缩小部分差距但引擎级差距未变，结论仍是"双轨混合用"。
> **来源**：Danilchenko.dev（Last updated July 2026，refreshed for Pandas 3.0）
> **最后更新**：2026-07-25

## 核心要点

1. Polars 在任何 >1GB 基准更快；240M 行实测 joins/group-bys **~10x**、Parquet 读取 **~5x**。
2. Pandas 3.0（2026-01 GA）：PyArrow 后端字符串默认、Copy-on-Write 默认、`pd.col()` 表达式 API。
3. 引擎级差距在 Polars 1.43 / Pandas 3.0 **保持不变**。
4. 作者跑过两条生产管道后选**双轨**：Polars 批量变换 + Pandas 最后一公里（sklearn/matplotlib）。
5. "该不该全面迁移？"答案仍是**否**——小交互集 / sklearn 往返 / 字符串密集场景 Pandas 仍胜。

## 详细内容

### 真实工作负载（240M 行）

| 项目 | 配置 |
|------|------|
| 数据 | 约 2.4 亿行点击流，18 个 Parquet 文件 |
| 结构 | 7 数值列 + 3 字符串列，磁盘约 14GB |
| 硬件 | M2 Pro 16 核 32GB，每操作 5 次 |
| 基准版本 | Polars 1.18 vs Pandas 2.2（差距在 1.43/3.0 不变） |

### Pandas 3.0 改了什么

| 变化 | 说明 |
|------|------|
| PyArrow-backed strings 默认 | 底层字符串全面转向 Arrow 列式 |
| Copy-on-Write 默认 | 链式赋值直接报错，消除 SettingWithCopy 隐患 |
| `pd.col()` 表达式 API | 借鉴 Polars 表达式风格 |

### 第三方验证

DuckDB Labs 的 db-benchmark 在 0.5/5/50GB 三档追踪 group-by 与 join 性能（Polars / Pandas / DuckDB 等）。

## 关联页面

- [[polars_vs_pandas_2026|Polars vs Pandas 2026 选型指南]] — 详细性能对比、三引擎协同与零售场景适配

## 待办 / 待验证

- [ ] Polars 1.43 与 Pandas 3.0 同机再测（确认 10x/5x 在新版本下稳定）
