# DuckDB vs Polars 2026 基准对比：单机分析引擎终极选型

> **来源**: https://www.pyinns.com/python/data-sciences/duckdb-vs-polars-2026-fast-analytics-benchmarks
> **发布日期**: 2026-03-12
> **采集日期**: 2026-06-24

## 核心对比

| 维度 | DuckDB (1.2+) | Polars (1.x) | 优胜 |
|------|-------------|-------------|------|
| 主要API | SQL (类PostgreSQL) | Python表达式API + Lazy DataFrame | 取决于偏好 |
| 从Pandas迁移成本 | 中等(重写SQL) | 低-中(类似DataFrame风格) | Polars |
| 10GB Parquet读取 | ~2-6s | ~1.5-5s | Polars略优 |
| 复杂SQL (Join+Window+Agg, 5亿行) | ~8-25s | ~10-35s | DuckDB略优 |
| GroupBy+FIlter 10亿行 | ~15-40s | ~12-35s | Polars略优 |
| 超内存/流式处理 | 优秀(自动溢出) | 优秀(collect(streaming=True)) | 平手 |
| 5亿行峰值内存 | ~2-6GB | ~1.5-5GB | Polars略优 |
| 多线程/并行 | 全自动 | 全自动 | 平手 |

## 使用场景决策

- **DuckDB**: 热爱SQL、BI风格分析、嵌入式应用、MotherDuck云、需要类PostgreSQL体验
- **Polars**: Python原生、Lazy DataFrame API、ETL管道、与Python生态紧密集成(Numba, uv等)
- **混合方案**: DuckDB处理SQL报表 + Polars处理Python管道(两者都基于Arrow, 零拷贝互转)

## 安装(2026现代化方式)

```bash
uv add duckdb
uv add polars pyarrow
```

## 核心代码示例

### 读取Parquet + 过滤 + 分组 (1亿行)

DuckDB (SQL):
```python
import duckdb
result = duckdb.sql("""
    SELECT year, AVG(magnitude) as avg_mag, COUNT(*) as cnt
    FROM 'large_quakes.parquet'
    WHERE magnitude >= 6.0
    GROUP BY year ORDER BY year DESC
""").df()
```

Polars (表达式API):
```python
import polars as pl
result = (
    pl.scan_parquet("large_quakes.parquet")
      .filter(pl.col("magnitude") >= 6.0)
      .group_by("year")
      .agg(avg_mag=pl.col("magnitude").mean(), cnt=pl.len())
      .sort("year", descending=True).collect()
)
```

## 关键结论

两者在单机速度上通常差距在20-50%以内。DuckDB在复杂SQL上有轻微优势，Polars在Python原生人体工学上占优。Arrow互转—2026年许多团队同时使用两者。
