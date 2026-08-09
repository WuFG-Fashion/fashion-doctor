# L3_06_04 SQL查询优化 — 2026-08-09 更新纪要

> 本轮（ingestC Round 120）补充 DuckDB v1.5 嵌入式分析范式（Python 三套 API + 零序列化换手）与服装五维指标体系对应的数仓分层建设（raw→stg→mart + 星型 + SCD Type 2），进销存 SQL 六种写法覆盖约 85% 业务问题。

## 新增要点

- **DuckDB 嵌入式 SQL 桥接**：DB-API / Relational API / Spark API 三套；与 Pandas/Arrow 近乎零序列化换手；内存模式 + 持久化模式 + 核外直查数十 GB Parquet。
- **服装五维指标体系**：商品/销售/库存/渠道/用户，配套"定目标→盘数据→定指标→分场景"四步法；售罄率/库龄/断码率/复购率为核心。
- **数仓分层**：raw→stg→mart 三层 + 星型模式 + SCD Type 2（价格历史维度）；四大标准库（术语库/码值库/命名规范/指标定义规范）。
- **进销存 SQL 六种写法**：LEFT JOIN+COALESCE / 窗口函数时点库存 / CTE 分层 / 分组聚合 / 条件聚合 / 物化快照；五条性能策略综合 IO↓68%、吞吐↑2.3x。

## 关联 wiki 页面

- 来源摘要：[[2026-08-09_DuckDB官方_v1.5系列与Python嵌入式分析范式]]、[[2026-08-09_CSDN_服装行业指标体系五维框架与电商数仓分层建设]]
- 概念页：[[duckdb_olap_engine_2026]]（已追加 Python 嵌入式分析范式小节）、[[retail_data_workflow_2026]]（已追加五维框架+数仓分层小节）、[[semantic_layer_metrics_2026]]（新建）
- 实践页：[[python_sql_integration_patterns_2026]]（已追加 DuckDB 嵌入式 SQL 桥接模式）、[[零售数据仓库SQL实践]]
