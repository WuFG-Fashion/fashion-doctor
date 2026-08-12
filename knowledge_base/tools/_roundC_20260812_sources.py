#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round C (2026-08-12) — 写入 4 篇来源摘要页，全部硬链到已有 concept（无孤岛）"""
import io, os

WIKI = os.path.join(os.path.dirname(__file__), '..', 'wiki')
SRC = os.path.join(WIKI, 'sources')

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(content)
    print('WROTE', os.path.relpath(path, os.path.join(WIKI, '..')))

# ---------- Source 1: DuckDB 查询调优三层级 ----------
s1 = """---
type: source
title: DuckDB 查询性能调优三层级实战（2026）
tags: [duckdb, sql, performance, tuning, predicate_pushdown, parquet, materialized_view, source]
sources: [2026-08-12_DuckDB官方_查询性能调优三层级实战, https://duckdblab.org/en/post/duckdb-performance-tuning-5-tips, https://duckdblab.org/en/post/duckdb-predicate-pushdown-filter-indexes, https://www.dench.com/blog/duckdb-query-optimization]
created: 2026-08-12
updated: 2026-08-12
cross_refs: [[SQL查询性能优化]], [[duckdb_olap_engine_2026]], [[polars_vs_pandas_2026]]
---

# DuckDB 查询性能调优三层级实战（2026）

> **一句话摘要**：DuckDB Labs 给出三层查询优化栈——文件级 Hive 分区+Glob（10–365x）、行组级谓词下推+行组调优（2–15x）、库级 Filter Indexes+物化表（5–100x）；1B 行聚合预聚到小时级后扫 168 行毫秒返回，内存溢出落盘会慢 10–100x。

> **来源**：DuckDB Lab 两篇官方调优文 + 中文社区转述
> **最后更新**：2026-08-12

## 核心要点

1. **三层栈**：Layer1 文件级分区（10–365x）/ Layer2 行组级谓词下推（2–15x）/ Layer3 库级 Filter Indexes+物化表（5–100x）。
2. **Layer1**：Hive 分区 + Glob 路径，100 文件→2-3 文件，典型 30s→1s；CSV 换 Parquet 是最高 ROI 优化。
3. **Layer2**：`EXPLAIN ANALYZE` 验证下推；反模式（列上 CAST/LIKE、列算术、大 IN 列表→SEMI JOIN）阻断下推；行组默认 122880，频繁日期过滤用 50000–80000。
4. **Layer3**：ART Filter Index 适高频点查；物化预聚合表胜过索引——1B 行聚合预聚到小时级后仅扫 168 行。
5. **内存**：`memory_limit='8GB'` + temp 指 SSD；`PRAGMA show_temporary_files` 检测 spill（落盘慢 10–100x）。

## 详细内容

### 三层加速对照

| 层级 | 技术 | 加速 | 关键验证 |
|------|------|------|---------|
| L1 文件级 | Hive 分区 + Glob | 10–365x | 只扫匹配子目录 |
| L2 行组级 | 谓词下推 + 行组调优 | 2–15x | `EXPLAIN ANALYZE` 见 `PARQUET_SCAN ... Filters:` |
| L3 库级 | Filter Index + 物化表 | 5–100x | 1B 行→168 行扫描 |

### 反模式（阻断下推）

- `WHERE CAST(trans_date AS VARCHAR) LIKE '2026-06-%'` → 改范围比较
- `WHERE trans_date + INTERVAL '1 day' > ...` → 改 `> '2026-06-14'`
- 大 IN 列表 → `SEMI JOIN target USING (city)`

### 物化表模板

```sql
CREATE TABLE hourly_metrics AS
SELECT DATE_TRUNC('hour', ts) AS hour, region,
       SUM(revenue) AS total_revenue, COUNT(DISTINCT user_id) AS unique_users
FROM raw_events GROUP BY ALL;
-- 查询扫 168 行而非 1B 行，毫秒级
```

## 对本项目直接映射

- 本项目多品牌分析层以**款号/色号/尺码/门店编码**做 group by/join，DuckDB 内存模式 + 物化中间表可把周报查询从分钟级压到毫秒级，与现有 [[SQL查询性能优化]] 的索引/覆盖索引路线互补（OLAP 引擎层）。
- 三层栈是 [[duckdb_olap_engine_2026]] 的"生产调优"补强；物化表思路可直接用于本项目"每日指标预计算"实践。
- 与 [[polars_vs_pandas_2026]] 的"按 workload 选引擎"一致：DuckDB 擅 SQL 聚合/即席，Polars 擅 ETL 流水线。

## 关联页面

- [[SQL查询性能优化]] — 上位概念，本源补 DuckDB 三层调优一手实现
- [[duckdb_olap_engine_2026]] — DuckDB OLAP 引擎总览
- [[polars_vs_pandas_2026]] — 三引擎选型参照基准

## 待办 / 待验证

- [ ] 本项目现有周报 SQL 是否已用物化中间表待清点
- [ ] DuckDB spill 检测（show_temporary_files）是否接入监控待评估
"""

# ---------- Source 2: Streamlit 企业级架构与生产部署 ----------
s2 = """---
type: source
title: Streamlit 企业级架构与生产部署路线（2026）
tags: [streamlit, dashboard, deployment, nginx, docker, k8s, security, monitoring, source]
sources: [2026-08-12_Streamlit_企业级架构与生产部署路线, https://tsight.io/articles/18042473, https://livemy.app/blog/deploy-streamlit-app, https://blog.csdn.net/gitblog_01177/article/details/154462267, https://www.powertrend.com.br/en-us/blog/data-dashboard-python-streamlit]
created: 2026-08-12
updated: 2026-08-12
cross_refs: [[streamlit_dashboard_2026]], [[streamlit_production_dashboard]], [[multi_brand_unified_analytics]]
---

# Streamlit 企业级架构与生产部署路线（2026）

> **一句话摘要**：2026 生产部署矩阵：Streamlit Share / 私有 Docker / 传统服务器；生产推荐 Nginx(SSL/Auth)→Docker(Streamlit)→DB 拓扑 + K8s 多实例会话亲和；streamlit-elements 突破线性布局；OAuth2.0/SAML RBAC + Prometheus/Grafana 监控；Community Cloud 有 1GB 上限+12h 休眠，livemy.app $10/月、Railway/Render $5–7/月、Docker VPS $5–20/月。

> **来源**：tsight.io + livemy.app + CSDN + PowerTrend（2026 综述）
> **最后更新**：2026-08-12

## 核心要点

1. **部署矩阵**：安全性/可扩展性/环境一致性/运维成本四维对比，生产首选私有 Docker 容器化。
2. **生产拓扑**：`User → Nginx(SSL/Auth) → Docker(Streamlit) → 内部 DB/LLM API`，多实例 K8s + 会话亲和。
3. **交互升级**：streamlit-elements（MUI）实现可拖拽网格，突破原生线性布局。
4. **安全监控**：OAuth2.0/SAML RBAC、TLS/AES-256、输入校验、速率限制；Prometheus+Grafana 盯响应时间/内存/并发/缓存命中。
5. **2026 选项**：Community Cloud（~1GB 内存 / 12h 休眠 / 1 私有应用 / 无自定义域名）vs livemy $10/月 vs Railway/Render $5–7/月 vs Docker VPS $5–20/月。

## 详细内容

### 部署选项对照

| 选项 | 成本 | 痛点/要点 |
|------|------|----------|
| Community Cloud | 免费 | 1GB 内存上限（pandas 负载易触顶关停）、静默 12h 休眠、仅 1 私有应用、无自定义域名 |
| livemy.app | $10/月 扁平 | 自动探测仓库、自定义域名+SSL、无 1GB 上限、含监控 |
| Railway / Render | $5–7/月起 | 适合"应用+DB+定时任务+API"多服务架构 |
| Docker on VPS | $5–20/月 | 完全控制，需自维护 SSL/备份/重启 |

### 生产架构拓扑

```
User → Nginx(SSL/Auth) → {负载均衡·会话亲和} → Streamlit 实例1 / 实例2
                                                  ↓
                                          内部 DB / LLM API
```

## 对本项目直接映射

- 本项目多品牌看板（[[streamlit_production_dashboard]]）应走 Docker+Nginx+认证外挂；对外分享用零门槛托管；耗时 IO 必缓存。
- 多品牌切换栏/全局筛选可借 [[streamlit_dashboard_2026]] 的 `st.bottom` + streamlit-elements 做可拖拽大屏。
- 与 [[multi_brand_unified_analytics]] 的"四层架构"生产呈现层一致：Docker 化部署是跨品牌统一看板的落地底座。

## 关联页面

- [[streamlit_dashboard_2026]] — Streamlit 2026 版本与最佳实践总览
- [[streamlit_production_dashboard]] — 生产级多品牌看板实操
- [[multi_brand_unified_analytics]] — 多品牌统一分析架构（呈现层）

## 待办 / 待验证

- [ ] 本项目是否需引入 streamlit-elements 做可拖拽大屏待评估
- [ ] K8s 多实例下的 session_state 一致性方案待设计
"""

# ---------- Source 3: 零售数据治理与数据中台落地方法论 ----------
s3 = """---
type: source
title: 零售数据治理与数据中台落地方法论（2026）
tags: [data_governance, middle_platform, etl, cdc, data_quality, dataphin, retail, source]
sources: [2026-08-12_阿里云_数据中台落地方法论与ETL事务管理, http://developer.aliyun.com:443/article/1746886, http://cloud.dayizhe.cn?article/1707351, https://www.fanruan.com/finepedia/article/695a50ffe53c3f47fb1109da, https://www.finedatalink.com/blog/article/69c5e3011916e24b22e6eac9, https://www.finedatalink.com/blog/article/69cc7d731916e24b22edd4f6]
created: 2026-08-12
updated: 2026-08-12
cross_refs: [[data_governance_tech_routes_2026]], [[data_quality_governance]], [[multi_brand_unified_analytics]], [[brand_config_driven_system]]
---

# 零售数据治理与数据中台落地方法论（2026）

> **一句话摘要**：2026 数据中台落地方法论——选型评估矩阵（传统 ETL vs 智能平台：50+ 数据源/湖仓一体/治理左移/服务化）+ 三阶段路线图（试点 1–3 月/体系 3–6 月/规模 6 月+）；全链路 ETL 事务管理（CDC+日志比对/Kafka/幂等写入/自动补偿）；量化成效查询效率 +90%、质量事故 -60%、ETL 开发效率 +30–50%。

> **来源**：阿里云开发者社区 + 大痣者 + 帆软 FinePedia + FineDataLink（2026）
> **最后更新**：2026-08-12

## 核心要点

1. **选型矩阵**：传统 ETL/数仓 vs 智能数据平台——数据源 50+、湖仓一体、治理左移、AI 全链路、API 服务化。
2. **三阶段路线**：Phase1 试点（1–3 月，高价值场景）/ Phase2 体系（3–6 月，标准+自助）/ Phase3 规模（6 月+，资产运营）。
3. **避坑**：重技术轻业务 / 贪大求全 / 治理后置 / 忽视运营。
4. **ETL 事务管理**：口径先行 → CDC+日志比对+Kafka → 多级校验+异常隔离 → 幂等写入+批量提交+回滚 → 监控补偿 → DAG 血缘。
5. **量化**：查询效率 +90%；瓴羊 Dataphin 自动 ETL 开发效率 +30–50%、异常拦截使质量事故 -60% 以上。

## 详细内容

### 三阶段路线图

| 阶段 | 周期 | 关键动作 |
|------|------|---------|
| 试点验证 | 1–3 月 | 1-2 高价值场景，接数据源/建模型/配质量规则/发 API |
| 体系搭建 | 3–6 月 | 扩 3-5 核心域，建标准与治理，上资产门户与自助分析 |
| 规模运营 | 6 月+ | 全业务线，资产运营机制，深化 AI，持续迭代 |

### ETL 全链路事务管理

```
需求梳理(口径先行) → 抽取(CDC+日志比对+Kafka) → 转换(多级校验/异常隔离)
→ 加载(幂等/批量提交/回滚) → 监控补偿(自动告警) → 血缘回溯(DAG)
```

零售全渠道订单集成案例：MySQL 门店 / Oracle 商城 / API 第三方 / Kafka 实时流，FineDataLink 低代码 DAG 编排，异常自动补偿，实现"不丢不重"。

## 对本项目直接映射

- 本项目三品牌（太平鸟/卡宾/东尚）CSV→入库→飞书推送的 ETL 链路，应借鉴"幂等写入+批量提交+自动补偿"，避免重跑产生重复（历史大批量导入曾引发无 DELETE 重叠重复）。
- 多品牌主数据统一视图 + 标准字典 + 分级分类，与 [[brand_config_driven_system]] 的 RCBT 主数据映射、[[multi_brand_unified_analytics]] 的跨品牌隔离/共享一致。
- 与 [[data_governance_tech_routes_2026]] 的"治理左移 + 智能平台"路线对齐；[[data_quality_governance]] 的补强点在 ETL 事务级质量门禁。

## 关联页面

- [[data_governance_tech_routes_2026]] — 治理平台技术路线总览
- [[data_quality_governance]] — 数据质量常态化治理框架
- [[multi_brand_unified_analytics]] — 多品牌统一分析架构
- [[brand_config_driven_system]] — 品牌配置驱动与跨品牌主数据

## 待办 / 待验证

- [ ] 本项目三品牌 ETL 是否已具备幂等+回滚+补偿机制待核对
- [ ] 数据治理"左移"到 Tableau 报表筛选器配置层（曾因筛选器漏勾选致女装数据消失）的防呆机制待建
"""

# ---------- Source 4: Polars 2.1 / Pandas 3.0 生产级性能对比 ----------
s4 = """---
type: source
title: Polars 2.1 / Pandas 3.0 生产级性能对比（2026）
tags: [polars, pandas, duckdb, python, benchmark, rust, data_analysis, source]
sources: [2026-08-12_Polars2.1_Pandas3.0_生产级性能对比, https://www.johal.in/tested-compared-data-analysis-2026-step-by-step/, https://ima.qq.com/wiki/, https://itsourcecode.com/blogs/polars-vs-pandas-2026/, https://www.pyinns.com/python/data-manipulation/polars-vs-pandas-2026, https://danilchenko.dev/posts/polars-vs-pandas/]
created: 2026-08-12
updated: 2026-08-12
cross_refs: [[polars_vs_pandas_2026]], [[arrow_zero_copy_interop_2026]], [[python_data_stack_decision_2026]]
---

# Polars 2.1 / Pandas 3.0 生产级性能对比（2026）

> **一句话摘要**：johal.in 50GB 实测——Polars 2.1.0 在 CSV Join 上比 Pandas 3.0 快 12.4x、内存低 60%；DuckDB 1.2.3 比 Spark 4.0（100GB）延迟低 89%；自建 Polars+DuckDB 栈比托管(Fivetran+Snowflake) 成本 $0.03/GB vs $0.18/GB、快 12x；预测 2027 年 70% 生产分析用 Rust 工具。ima：Polars 月下载 3000 万，"二选一"→"混合用"。

> **来源**：johal.in + ima.qq.com + itsourcecode + pyinns + danilchenko（2026）
> **最后更新**：2026-08-12

## 核心要点

1. **johal 50GB**：Polars 2.1.0 Join 比 Pandas 3.0.1 快 **12.4x**、内存 **-60%**；DuckDB 1.2.3 比 Spark 4.0（100GB）延迟 **-89%**。
2. **成本**：自建 Polars+DuckDB 处理 50GB/日，$0.03/GB vs 托管 $0.18/GB、快 12x；2027 年 70% 生产分析用 Rust 工具（Polars/DataFusion）。
3. **ima 10M 行**：过滤 6x / GroupBy 10x / Join 12x / 排序 10x / 字符串 11x / 滚动 9x；内存省 65–73%。
4. **itsourcecode 1M 行**：Read 9x / Filter 10x / GroupBy 30x / Join 14x / Sort 10x。
5. **结论**：不该全面迁移，该全面评估——混合用（Polars 做 ETL/重计算，Pandas 做 ML/可视化）。

## 详细内容

### 50GB 实测基准（32GB RAM）

| 引擎 | Read | Join | Groupby | 内存 |
|------|------|------|---------|------|
| Polars 2.1.0 | 3.2s | 17.1s | 31.4s | 5324 MB |
| DuckDB 1.2.3 | 2.8s | 14.5s | 27.9s | 3891 MB |
| Pandas 3.0.1 | 42.1s | 210.5s | 380.2s | 14567 MB |

### 内存实测（Polars vs Pandas）

| 场景 | Pandas | Polars | 节省 |
|------|--------|--------|------|
| 1000 万行混合 | 3.2 GB | 1.1 GB | 65% |
| 字符串密集 | 5.8 GB | 1.9 GB | 67% |
| GroupBy 峰值 | 8.4 GB | 2.3 GB | 73% |

### 落地判断

- 数据 > 100MB / ETL / 新项目 / 多核 / 流式 → Polars
- 遗留 pandas / 重 sklearn·matplotlib / < 50 万行 → Pandas
- 混合：Polars 重计算 `.to_pandas()` 喂 sklearn；DuckDB 做 SQL 聚合；三者经 Arrow 零拷贝串联

## 对本项目直接映射

- 本项目 Streamlit 看板用 Pandas/Plotly 展示、底层重计算用 Polars/DuckDB，经 [[arrow_zero_copy_interop_2026]] 零拷贝串联，与 [[python_data_stack_decision_2026]] 的"混合用"范式一致。
- 12.4x Join / -60% 内存与 [[polars_vs_pandas_2026]] 既有基准（kb `speed_multiplier=8`）同属"数倍至十余倍"区间，口径差异（50GB join vs 千万行通用），非硬矛盾。

## 关联页面

- [[polars_vs_pandas_2026]] — 三引擎选型总览（本源刷新 2026-08 基准）
- [[arrow_zero_copy_interop_2026]] — Arrow 零拷贝互操作（本源补内存实测）
- [[python_data_stack_decision_2026]] — Python 数据栈决策（混合用范式）

## 待办 / 待验证

- [ ] 本项目是否将 >50 万行重计算从 Pandas 迁移到 Polars 待评估
- [ ] 三品牌入库后分析是否引入 DuckDB 直查 Parquet 待 PoC
"""

for fn, content in [
    ('2026-08-12_DuckDB官方_查询性能调优三层级实战.md', s1),
    ('2026-08-12_Streamlit_企业级架构与生产部署路线.md', s2),
    ('2026-08-12_阿里云_数据中台落地方法论与ETL事务管理.md', s3),
    ('2026-08-12_Polars2.1_Pandas3.0_生产级性能对比.md', s4),
]:
    w(os.path.join(SRC, fn), content)

print('DONE sources: 4')
