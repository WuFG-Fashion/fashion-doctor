# -*- coding: utf-8 -*-
"""Round C 2026-08-12 — 写入 raw/articles 4篇原始剪藏（L2_06/07 + 查漏）"""
import os, pathlib

KB = pathlib.Path(__file__).resolve().parent.parent
RAW = KB / "raw" / "articles"
RAW.mkdir(parents=True, exist_ok=True)

FILES = {}

FILES["2026-08-12_DuckDB官方_查询性能调优三层级实战.md"] = """# DuckDB 查询性能调优三层级（2026-08 实战）

> 采集日期：2026-08-12
> 来源：DuckDB Lab《DuckDB Performance Tuning: 5 Tips from Slow Queries to Millisecond Response》+《DuckDB Deep Tuning: Predicate Pushdown + Filter Indexes + materialized tables for 100x Faster Queries》+ CSDN/腾讯云社区中文转述
> URL：https://duckdblab.org/en/post/duckdb-performance-tuning-5-tips ; https://duckdblab.org/en/post/duckdb-predicate-pushdown-filter-indexes ; https://www.dench.com/blog/duckdb-query-optimization

## 一、三层优化栈总览

| 层级 | 技术 | 适用场景 | 潜在加速 |
|------|------|---------|---------|
| Layer 1 · 文件级 | Hive 分区 + Glob 路径 | 可分区历史数据 | 10–365x |
| Layer 2 · 行组级 | 谓词下推 Predicate Pushdown + 行组调优 | 大单文件 / 不可分区数据 | 2–15x |
| Layer 3 · 库级 | Filter Indexes + 物化表 | 高频看板查询 | 5–100x |

很多用户以为优化止步于分区裁剪（Layer 1）。但当数据在单个大 Parquet 文件、或实时流、或第三方 API 批量导出时，分区裁剪完全失效——此时必须上 Layer 2/3。

## 二、Layer 1：Hive 分区 + Glob

把数据按 `data/YYYY/MM/region/*.parquet` 组织，查询时只扫匹配子目录：

```sql
-- 全扫：100 个 parquet 文件
SELECT region, SUM(sales) FROM read_parquet('data/*.parquet') GROUP BY region;
-- 分区裁剪：只扫 1 月对应 2-3 个文件
SELECT region, SUM(sales) FROM read_parquet('data/*/*.parquet', hive_partitioning = true)
WHERE month = '2026-01' AND region = 'APAC';
```

同一查询，前者扫 100 文件，后者只读 2-3 个。生产环境典型差异：**30 秒 vs 1 秒**。FILE_GLOB（`data/2026-{01,02,03}/*.parquet`）可做精确文件选择。

> 最高 ROI 优化：把 CSV 换成 Parquet。10 分钟投入，回报最大。

## 三、Layer 2：行组级谓词下推 + 行组调优

每个 Parquet 文件由 Row Group 组成，DuckDB 默认每个行组约 122,880 行，行组携带列级 min/max/null 统计（footer 元数据）。谓词下推利用这些统计跳过整批不匹配的行组。

- **验证**：务必用 `EXPLAIN ANALYZE` 确认下推生效——看到 `PARQUET_SCAN ... Filters: ...` 且 `[table: ~80K rows]`（仅读约 1/12 行组）即成功；若看到 `SEQ_SCAN` 或 filter 出现在 scan 之后节点，说明下推失败。
- **反模式（阻断下推）**：
  1. 列上套函数：`WHERE CAST(trans_date AS VARCHAR) LIKE '2026-06-%'`（应改 `>= '2026-06-01' AND < '2026-07-01'`）
  2. 列上算术：`WHERE trans_date + INTERVAL '1 day' > '2026-06-15'`（应改 `> '2026-06-14'`）
  3. 超大 IN 列表（>~50 元素）：改用 `WITH target AS (SELECT unnest([...]) AS city) SELECT * FROM sales SEMI JOIN target USING (city);`
- **行组大小调优**：默认 122880（中精度/低开销）；频繁按日期/范围过滤用 50000–80000（高精度/中开销）；<10000 元数据膨胀不推荐。导出时 `COPY (SELECT * FROM raw ORDER BY trans_date) TO 'opt.parquet' (FORMAT PARQUET, ROW_GROUP_SIZE 50000)`。

## 四、Layer 3：库级 Filter Indexes + 物化表

当文件级/行组级用尽、看板仍需并发响应时上 Layer 3。

- **Filter Indexes**（ART，自适应基数树，专为高频过滤列设计）：
```sql
CREATE INDEX idx_sales_date ON sales(trans_date);
CREATE INDEX idx_sales_region_date ON sales(region, trans_date);
```
  适合点查（`WHERE user_id = 42` 微秒级）、低选择性范围扫、JOIN 条件；对全表聚合、返回 >10% 行、低基数列无帮助。
- **物化表（预聚合胜过索引）**：DuckDB 列存 + 向量化引擎下，物化预聚合每次查询都优于索引。把"每天跑一遍聚合 1B 行"改为"写入时 transform-on-write 预聚到小时级"：
```sql
CREATE TABLE hourly_metrics AS
SELECT DATE_TRUNC('hour', ts) AS hour, region,
       SUM(revenue) AS total_revenue, COUNT(DISTINCT user_id) AS unique_users
FROM raw_events GROUP BY ALL;
-- 查询：扫 168 行而非 1B 行，毫秒级
```
  也可用 `CREATE MACRO` 轻量缓存。

## 五、内存管理与溢出排查

最常见隐形慢因：数据装不下内存 → 落盘 spill，慢 10–100x。

- 检测：`PRAGMA show_temporary_files;` 或 `SELECT * FROM duckdb_temporary_files();` 若运行中产生 temp 文件（默认 `/tmp/duckdb`），即发生 spill。
- 三件套：
```sql
PRAGMA memory_limit = '8GB';              -- 默认约可用 RAM 的 75%
PRAGMA temp_directory = '/mnt/ssd/duckdb_tmp';  -- 指向 SSD，别用 HDD/网络盘
PRAGMA hash_table_size_limit = '2GB';     -- 防单查询饿死其他
PRAGMA out_of_core_threshold = '2GB';
```
- 列裁剪：宽表只 `SELECT` 需要的列，Parquet 列存优势最大化。
"""

FILES["2026-08-12_Streamlit_企业级架构与生产部署路线.md"] = """# Streamlit 企业级架构与生产部署路线（2026-08）

> 采集日期：2026-08-12
> 来源：tsight.io《从原型到生产：Streamlit 企业级架构深度实践与工程避坑指南》+ livemy.app《How to deploy a Streamlit app in 2026》+ CSDN《Streamlit架构深度解析：企业级数据应用构建与部署指南》+ PowerTrend《Data Dashboard with Python and Streamlit》
> URL：https://tsight.io/articles/18042473 ; https://livemy.app/blog/deploy-streamlit-app ; https://blog.csdn.net/gitblog_01177/article/details/154462267 ; https://www.powertrend.com.br/en-us/blog/data-dashboard-python-streamlit

## 一、部署方案决策矩阵

| 维度 | Streamlit Share | 私有 Docker 容器化 | 传统服务器 |
|------|----------------|-------------------|-----------|
| 安全性 | 低（公网/GitHub 绑定） | 高（私有网络隔离） | 中（OS 级防火墙） |
| 可扩展性 | 极低（单实例） | 极高（K8s 动态扩缩） | 低（手动加实例） |
| 环境一致性 | 中（requirements.txt） | 极高（镜像级封印） | 低（易环境污染） |
| 运维成本 | 极低 | 中（维护镜像仓库） | 高（手动配置） |

**生产推荐路径**：`User → Nginx(SSL/Auth) → Docker(Streamlit) → 内部 DB/LLM API`，多实例经负载均衡 + 会话亲和分发，直接暴露 8501 端口被视为"业余且危险"。

## 二、交互体验天花板：streamlit-elements

原生"从上到下"线性布局做大屏简陋。streamlit-elements 在 Streamlit 内嵌 Material UI（MUI），实现可拖拽、可缩放网格；用 `st.session_state` 持久化组件坐标与尺寸，突破线性布局限制。

## 三、安全与监控最佳实践

- **认证授权**：集成 OAuth2.0 / SAML IdP，基于角色的访问控制（RBAC）；数据加密用 TLS/SSL 传输 + AES-256 存储；严格输入校验防注入；API 防护配速率限制与请求过滤防 DDoS。
- **监控**：Prometheus 指标采集 + Grafana 面板，关键指标含请求响应时间、内存使用率、并发会话数、缓存命中率。
- **多级缓存**：内存分页加载、生成器流式处理、Parquet/Feather 压缩降低 I/O。
- **数据库连接**：SQLAlchemy / 驱动直连，配连接池与事务控制。

## 四、2026 部署选项（超越 Community Cloud）

| 选项 | 成本 | 要点 |
|------|------|------|
| Streamlit Community Cloud | 免费 | ~1GB 内存上限（pandas 负载极易触顶并被关停）；静默 12h 后休眠；仅 1 个私有应用；无自定义域名；代码在 GitHub |
| livemy.app | $10/月 扁平 | 自动探测 GitHub 仓库；自定义域名 + 自动 SSL；无 1GB 上限；含监控 |
| Railway / Render | $5–7/月起（按用量） | 适合"应用 + Postgres + 定时任务 + API"的多服务架构 |
| Docker on VPS | $5–20/月 | 完全控制；需自维护 SSL/备份/重启；反向代理后多应用共存 |

> 经验法则：面向客户（每天有人看）别用免费层休眠页；内存尖峰是常态而非异常，扁平定价更稳。

## 五、生产实战要点（PowerTrend）

- `st.cache_data` 避免重复请求；Plotly 一行出交互图；`st.metric()` 把 KPI（营收/CAC/流失/NPS）放首屏之上；`st.selectbox/date_input/slider` 做筛选；`st.secrets` + 环境变量做认证，绝不把凭证写进代码。
"""

FILES["2026-08-12_阿里云_数据中台落地方法论与ETL事务管理.md"] = """# 零售数据治理与数据中台落地方法论（2026-08）

> 采集日期：2026-08-12
> 来源：阿里云开发者社区《企业如何应用数据中台？2026智能数据管理方案参考》+ 大痣者《2026年企业如何应用数据中台？从搭建到落地的实践路径》+ 帆软 FinePedia《2026年零售行业数据分析怎么做》+ FineDataLink《2026年ETL数据加载事务管理全流程解析》
> URL：http://developer.aliyun.com:443/article/1746886 ; http://cloud.dayizhe.cn?article/1707351 ; https://www.fanruan.com/finepedia/article/695a50ffe53c3f47fb1109da ; https://www.finedatalink.com/blog/article/69c5e3011916e24b22e6eac9 ; https://www.finedatalink.com/blog/article/69cc7d731916e24b22edd4f6

## 一、数据中台选型评估矩阵（阿里云）

| 评估维度 | 传统 ETL/数仓工具 | Dataphin 等智能数据平台 | 建议 |
|---------|------------------|------------------------|------|
| 数据源适配 | 结构化为主、实时弱 | 50+ 数据源、湖仓一体、实时离线一体 | 优先多云 + 实时 |
| 治理能力 | 事后治理、与研发割裂 | 治理内嵌研发全流程、质量规则自动化 | 治理"左移"到设计阶段 |
| 智能化 | 基本无 AI | AI 驱动建模/运维/取数全链路 | 评估 AI 是否真降门槛 |
| 服务化 | 仅存储/搬运 | API 服务、资产智能体、BI 联动 | 考察消费场景丰富度 |

## 二、三阶段落地路线图

| 阶段 | 周期 | 关键动作 |
|------|------|---------|
| Phase 1 试点验证 | 1–3 月 | 选 1-2 个高价值、边界清晰场景（客户画像/库存预警）；接数据源、建模型、配质量规则、发 API；验证核心指标改善 |
| Phase 2 体系搭建 | 3–6 月 | 扩到 3-5 个核心域；建企业级标准与治理制度；上资产门户与自助分析；完善权限/合规/审计 |
| Phase 3 规模运营 | 6 月+ | 全业务线推广；建资产运营机制（成本/价值/健康度）；深化 AI（智能推荐/预测性维护）；持续迭代 |

**避坑四要点**：重技术轻业务（需业务深度参与验收）、贪大求全（先高频高价值快速见效）、治理后置（质量/合规前置，后期补救极贵）、忽视运营（非"交钥匙工程"）。

**量化成效**：阿里云案例中查询效率提升 **90%**；瓴羊 Dataphin 自动生成 ETL 代码使开发效率 **+30%–50%**，异常数据自动拦截使数据质量事故 **减少 60% 以上**。

## 三、全链路 ETL 事务管理（FineDataLink）

```
需求梳理(口径先行) → 抽取(CDC+日志比对+Kafka) → 转换(多级规则校验/异常隔离表)
→ 加载(幂等写入/批量提交/可回滚) → 监控补偿(自动告警) → 血缘回溯(DAG)
```

- **抽取**：CDC + 日志比对双保险，保增量不遗漏、时序准确。
- **转换**：Python 算子多级规则校验，异常数据单独入隔离表，减少脏数据进仓。
- **加载**：所有写入带全量/增量标识，幂等 + 批量提交，失败自动回滚、支持重跑。
- **监控补偿**：调度平台自动发现异常并补偿；DAG 血缘便于溯源定责。

**零售全渠道订单集成案例**：MySQL（门店）/ Oracle（商城）/ API（第三方）/ Kafka（实时流）多源，FineDataLink 低代码 DAG 编排，异常自动补偿，实现"不丢不重"的统一数仓。

## 四、零售全链路数据集成与治理（帆软）

2026 领先企业普遍用数据中台思路：通过 ETL 自动采集（消除手工对账）、统一标准 + 主数据管理（保质量）、分钟/小时级实时同步、严格权限分级（防泄露）。帆软强调数据质量自动监控与告警、快速对接新系统。
"""

FILES["2026-08-12_Polars2.1_Pandas3.0_生产级性能对比.md"] = """# Polars 2.1 / Pandas 3.0 生产级性能对比（2026-08）

> 采集日期：2026-08-12
> 来源：johal.in《Tested & Compared Data Analysis in 2026》+ ima.qq.com《Polars vs Pandas 2026》+ itsourcecode《Polars vs pandas (Speed Syntax Comparison 2026)》+ pyinns《Polars vs Pandas in 2026》+ danilchenko.dev（Pandas 3.0 背景）
> URL：https://www.johal.in/tested-compared-data-analysis-2026-step-by-step/ ; https://ima.qq.com/wiki/... ; https://itsourcecode.com/blogs/polars-vs-pandas-2026/ ; https://www.pyinns.com/python/data-manipulation/polars-vs-pandas-2026 ; https://danilchenko.dev/posts/polars-vs-pandas/

## 一、johal.in 50GB 实测基准（32GB RAM）

| 引擎 | Read | Join | Groupby | 内存 |
|------|------|------|---------|------|
| Polars 2.1.0 | 3.2s | 17.1s | 31.4s | 5324 MB |
| DuckDB 1.2.3 | 2.8s | 14.5s | 27.9s | 3891 MB |
| Pandas 3.0.1 | 42.1s | 210.5s | 380.2s | 14567 MB |

- **Polars 2.1.0 在 50GB CSV Join 上比 Pandas 3.0 快 12.4x，内存开销低 60%**。
- **DuckDB 1.2.3 直查 S3 Parquet 比 Spark 4.0（100GB）延迟低 89%**。
- 自建 Polars + DuckDB 栈处理 50GB/日数据：比托管（Fivetran + Snowflake）**成本低至 $0.03/GB vs $0.18/GB、快 12x**。
- 预测：**到 2027 年 70% 生产数据分析将用 Rust 编译工具（Polars / DataFusion）**替代纯 Python 解释器。

## 二、ima.qq.com 2026 观点与 10M 行基准

- Polars 月下载量突破 **3000 万**（较 2024 初 750 万涨 300%+）；Pandas 默默更新到 3.0.3，默认 PyArrow 后端 + 默认 Copy-on-Write。
- 10M 行混合数据集基准：过滤 ~6x / GroupBy ~10x / Join ~12x / 排序 ~10x / 字符串过滤 ~11x / 滚动均值(窗口30) ~9x。
- 内存：1000 万行混合 3.2GB→1.1GB（省 65%）；字符串密集 5.8→1.9GB（省 67%）；GroupBy 峰值 8.4→2.3GB（省 73%）。
- **结论：不该全面迁移，但该全面评估——"二选一"正在变成"混合用"**。sklearn 集成仍是 Polars 短板（1.4+ 已支持 `set_output(transform="polars")`）；真正该问的不是"用哪个"，而是"哪一步用哪个引擎"。

## 三、itsourcecode / pyinns 补充

- itsourcecode（1M 行）：Read 9x / Filter 10x / GroupBy 30x / Join 14x / Sort 10x。
- pyinns（10M 行）：Read 4.7x / GroupBy 5.4x；内存 ~450MB vs ~1.8GB。
- Pandas 3.0（2026-01-21 发布）最低 Python 3.11，字符串成真正 dtype（PyArrow 后端），`.str.contains()/.lower()` 快数倍、文本内存约减半；CoW 默认开启。

## 四、落地判断

- 数据 > 100MB / 生产 ETL / 新项目 / 多核 / 流式大文件 → **Polars**。
- 遗留 pandas 代码 / 团队标准化 / 重 sklearn·matplotlib / < 50 万行 → **Pandas**（50 万行以下两者感知不到差别）。
- 混合用：Polars 做重计算与 ETL，`.to_pandas()` 在 ML 边界喂 sklearn；DuckDB 做 SQL 聚合与即席查询；三者经 Apache Arrow 零拷贝串联。
"""

for name, body in FILES.items():
    p = RAW / name
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print("WROTE", p.name, len(body))

print("DONE raw:", len(FILES))
