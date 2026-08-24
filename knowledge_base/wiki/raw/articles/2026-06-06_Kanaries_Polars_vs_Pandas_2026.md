# Polars vs Pandas：2026年选型指南

> **来源**：Kanaries Docs，2026-02-11
> **URL**：https://docs.kanaries.net/zh/articles/polars-vs-pandas
> **采集日期**：2026-06-06

## 性能基准对比（1000万行数据集）

| 操作 | Pandas | Polars | 倍差 |
|------|--------|--------|------|
| CSV加载(1GB) | 8.2s / 1.4GB | 1.6s / 0.18GB | **5x快 / 87%**内存省 |
| GroupBy聚合 | 1.8s | 0.22s | **5-10x快** |
| 排序 | 3.4s | 0.29s | **~11x快** |
| Join(1000万×100万) | 2.1s | 0.35s | **3-8x快** |

## 选型决策矩阵

| 场景 | 推荐 | 理由 |
|------|------|------|
| <100万行/ML生态 | Pandas | scikit-learn原生支持、团队熟悉 |
| >100万行/数据流水线 | Polars | 惰性求值、pushdown优化、60-87%内存节省 |
| 内存受限(16GB以下) | Polars | 流式执行，Pandas OOM的流水线Polars 4-6GB即可 |
| 大量Parquet | Polars | predicate/projection pushdown |
| 兼顾速度与生态 | Polars→Pandas混合 | 重度处理Polars→转Pandas做ML/可视化 |

## 核心差异
- 执行模式：Polars惰性求值构建优化计划，避免中间拷贝
- 内存：Apache Arrow列式 + pushdown + 流式执行
- API哲学：Polars表达式API `pl.col()` vs Pandas方括号索引
- 生态：Pandas 17年历史45000+Stars vs Polars 5年快速增长
- 注意：Polars不原生支持Excel，需用第三方库
