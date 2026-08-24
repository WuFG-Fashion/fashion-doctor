# 向量化执行与 PostgreSQL 18 / DuckDB 1.5.4 基准（2026 剪藏）

> 来源：modern-datatools PostgreSQL vs DuckDB 对比、johal.in PostgreSQL17 vs DuckDB1.2、markaicode DuckDB vs PostgreSQL Benchmark 2026、motherduck PGConfDev 2025、gitcode DuckDB 架构演进。
> 收藏日期：2026-08-15

## 核心数据
- DuckDB 1.5.4「Variegata」（LTS 1.4.5「Andium」）；`pg_duckdb` 扩展 2026 年达 1.0，PostgreSQL 可在内部把分析查询路由到 DuckDB 引擎。
- TPC-H 1TB Snappy Parquet（S3）：DuckDB 1.2 向量化执行比 PostgreSQL 17 平均快 7.4x；Q1 全表扫描 8.2 GB/s vs PG17 并行顺序扫描 1.1 GB/s；3+ 表 JOIN 快 5.2x。
- PostgreSQL 18.4（2026 中）引入异步 I/O 子系统，并新增向量化聚合（相对 PG16 常见聚合 -22%），但扫描密集型仍落后 DuckDB。
- 向量化执行：以 120k 行 morsel / 64KB 向量批次 + SIMD 处理，CPU 缓存命中率 40%→85%，单查询 3–10x。
- 自适应查询执行：动态切换 Join 算法 / 并行度，数据倾斜场景稳定性 +60%、复杂查询耗时 -40%，非索引查询相对 PG 快 2–5x。
- 混合架构（PG 扛 OLTP + DuckDB 扛 OLAP）实测 138k 写/秒 + 7.8 GB/s 分析吞吐、零资源争用。
- FinQore 用 DuckDB 替换后管道 8h→8min（60x）。
