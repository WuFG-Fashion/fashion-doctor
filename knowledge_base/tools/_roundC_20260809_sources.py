#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round C (2026-08-09) — 写入新来源摘要页 + 新概念页
放 tools/ 下，保持 vault 根整洁。输出用 UTF-8 + LF。
"""
import io, os

WIKI = os.path.join(os.path.dirname(__file__), '..', 'wiki')
SRC = os.path.join(WIKI, 'sources')
CON = os.path.join(WIKI, 'concepts')

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(content)
    print('WROTE', os.path.relpath(path, os.path.join(WIKI, '..')))

# ---------- Source 1: DuckDB v1.5 + Python 嵌入式 ----------
s1 = """---
type: source
title: DuckDB v1.5 系列与 Python 嵌入式分析范式（2026）
tags: [duckdb, olap, python, embedded, adbc, sql, arrow, source]
sources: [2026-08-09_DuckDB官方_v1.5系列与Python嵌入式分析范式, https://duckdb.org/2026/03/09/announcing-duckdb-150, https://duckdblab.org/zh/post/duckdb-154-release/, http://pythondatabench.com/zh/article/duckdb-wanquan-shizhan-zhinan-python-qianrushi-fenxi-shujuku, https://juejin.cn/post/7640016020847394868]
created: 2026-08-09
updated: 2026-08-09
cross_refs: [[duckdb_olap_engine_2026]], [[arrow_zero_copy_interop_2026]], [[python_sql_integration_patterns_2026]], [[polars_vs_pandas_2026]]
---

# DuckDB v1.5 系列与 Python 嵌入式分析范式（2026）

> **一句话摘要**：DuckDB 自 v1.5 起双轨维护（v1.4 LTS + v1.5 current），v1.5.4 把 ADBC 1.1.0、Avro、Unity Catalog 纳入核心；Python 侧提供 DB-API / Relational / Spark 三套 API 且与 Pandas/Arrow 近乎零序列化换手，是"嵌入式分析数据库"范式的成熟落地。

> **来源**：DuckDB 官方 Blog + DuckDB Lab 中文站 + PythonDataBench + 掘金综述
> **最后更新**：2026-08-09

## 核心要点

1. **版本节奏**：v1.5.0 "Variegata"（2026-03-09）；双轨 LTS（v1.4）+ current（v1.5）；下一个大版本 **DuckDB 2.0 计划 9 月发布**，v1.4.5 向后兼容、升级无需手动迁移数据文件。
2. **v1.5.4 生态对接三件套**：ADBC 1.1.0 + Rich Error API、Avro 扩展正式纳入、Unity Catalog 正式纳入；MERGE INTO 语义修正；Bug 修复 30+ 项。
3. **Python 三套 API**：DB-API（标准 execute/fetch）、Relational API（链式调用，体验接近 Pandas）、Spark API（PySpark 用户近零成本）。
4. **零序列化换手**：与 Pandas/Arrow 近乎无开销来回传递；内存模式（进程级临时分析）与持久化模式（落盘文件反复查询）并存；核外（out-of-core）可直查数十 GB Parquet。
5. **扩展生态**：httpfs/spatial/full_text_search/postgres+mysql 高频四件套；DuckDB-Wasm + Iceberg 浏览器内零安装查表、Quack-Cluster（DuckDB+Ray 无服务器分布式）。

## 详细内容

### v1.5.0 命令行客户端重做

| 能力 | 说明 |
|------|------|
| 新配色 | 暗/亮双模式，关键字/字符串/错误/函数/数字五类高亮 |
| 自定义高亮 | `.highlight_colors column_name darkgreen bold_underline` |
| 动态提示符 | 默认显示 database.schema，可配置 |
| `.tables` | 一次列出 ATTACH 的 catalog / schema / 表 / 列 |
| `_` 引用上次结果 | `FROM _;` 复用上一条查询结果 |

### v1.5.4 vs v1.5.3

| 特性 | v1.5.3 | v1.5.4 |
|------|--------|--------|
| ADBC | 基础 | **1.1.0 + Rich Error API** |
| Avro / Unity Catalog | ❌ | ✅ 正式纳入 |
| 存储版本映射 | — | 新增，确保与 v1.4.5 兼容 |

### Python 三套 API 实战

```python
import duckdb
# 直接查内存中的 Pandas DataFrame，无需先建表
result = duckdb.sql("SELECT * FROM my_df WHERE value > 100").df()
# 直接读 Parquet，结果转 Arrow
arrow_table = duckdb.sql("SELECT * FROM 'data.parquet'").arrow()
```

```python
con = duckdb.connect("analytics.duckdb")
con.execute("SET memory_limit = '8GB'")
con.execute("SET temp_directory = '/tmp/duckdb_spill'")
con.execute(
    "SELECT country, AVG(amount) AS avg_amt, COUNT(*) AS cnt "
    "FROM 'transactions_full.parquet' "
    "GROUP BY country HAVING COUNT(*) > 1000"
).fetch_df()
```

### 定位与边界

- **不能全面替代 SQLite**：DuckDB 面向分析型 OLAP，SQLite 擅长事务型 OLTP。
- 单文件数十至数百 GB 常见；MIT 许可，个人与商业完全免费，可集成进闭源软件。

## 对本项目的直接映射

- 本项目多品牌分析层大量以**款号/色号/尺码/门店编码**做 group by/join，适合 DuckDB 内存模式做临时探索、持久化模式做反复查询的数据集。
- 三套 API 中 Relational API（链式）与现有 [[python_sql_integration_patterns_2026]] 的生产 SQLAlchemy 模式互补：探索用 DuckDB SQL、生产用 SQLAlchemy 原生。
- ADBC 1.1.0 + Unity Catalog 让 DuckDB 可作为多品牌统一数据层的本地查询引擎，与 [[multi_brand_unified_analytics]] 的 Iceberg/湖仓路线协同。
- 与 Polars/Arrow 零序列化换手坐实 [[arrow_zero_copy_interop_2026]] 的"Arrow 是数据栈 USB-C"判断；与 [[polars_vs_pandas_2026]] 的性能对比需按 workload 分场景。

## 关联页面

- [[duckdb_olap_engine_2026]] — 上位概念，本源补上 v1.5.x 与 Python 嵌入式一手实现
- [[arrow_zero_copy_interop_2026]] — Arrow 零拷贝互操作
- [[python_sql_integration_patterns_2026]] — Python 与 SQL 集成的生产模式
- [[polars_vs_pandas_2026]] — 三引擎选型的参照基准

## 待办 / 待验证

- [ ] 本项目现有脚本是否已用 Relational API 链式写法待清点
- [ ] v1.5.4 Unity Catalog 接入多品牌统一目录的 PoC 未做
"""

# ---------- Source 2: 语义层 / 指标层 2026 ----------
s2 = """---
type: source
title: 语义层 / 指标层 2026 全景：从 BI 配角到 AI 基础设施
tags: [semantic_layer, metrics_layer, dbt, metricflow, osi, ai_agent, governance, source]
sources: [2026-08-09_Kaelio_Supaboard_dbt_语义层与指标层2026全景, https://www.kaelio.com/blog/best-semantic-layer-solutions-for-data-teams-2026-guide, https://supaboard.ai/blog/what-is-a-semantic-layer-the-2026-field-guide, https://bixtech.ai/dbt-semantic-models-metrics-layer-ai-agents, https://beefed.ai/zh/dbt-centralized-metrics-layer, https://juejin.cn/post/7628522386075992107]
created: 2026-08-09
updated: 2026-08-09
cross_refs: [[semantic_layer_metrics_2026]], [[retail_analytics_reporting_2026]], [[data_governance_tech_routes_2026]], [[multi_brand_unified_analytics]]
---

# 语义层 / 指标层 2026 全景：从 BI 配角到 AI 基础设施

> **一句话摘要**：2026 年语义层（Semantic Layer）成为 AI 时代的数据基础设施——把"已定义好的指标"而非裸 SQL 暴露给 BI 工具与 AI Agent，解决多团队对同一指标定义不一、报表口径漂移的问题；OSI 标准 1 月发布，dbt Semantic Layer 是主流实现之一。

> **来源**：Kaelio / Supaboard / bixtech / beefed / 掘金（2026 综述）
> **最后更新**：2026-08-09

## 核心要点

1. **为什么是 2026**：组织普遍管理 50+ 活跃数据源，多团队对同一指标给出不同定义；AI 就绪、多工具并存、治理强制三因素加速落地。一家大型零售商上线语义层后 **80% 查询在 1 秒内完成**。
2. **语义层里有什么**：Entities / Metrics / Dimensions / Relationships / 治理验证 / 业务规则；**不含原始数据本身、不是数据目录、不是知识图谱、本身不是 BI 工具**（headless 前提）。
3. **主流方案**：dbt Semantic Layer (MetricFlow) / AtScale / Cube Cloud / Snowflake Semantic Views / Databricks Metric Views / Power BI Semantic Model。
4. **标准化信号**：**Open Semantic Interchange（OSI）2026-01 首发**，把 datasets/metrics/dimensions/relationships/context 做成跨厂商可交换标准。
5. **给 AI Agent 的三条纪律**：不给裸 SQL 权限（走 dbt MCP server）、持续验证（CI 测试拦截破坏答案的变更）、把业务逻辑搬进版本化契约。

## 详细内容

### 2026 主流方案对照

| 方案 | 架构特点 | 适合谁 |
|------|---------|--------|
| dbt Semantic Layer (MetricFlow) | 指标与 dbt 模型同仓定义，确定性编译成 SQL | 已跑 dbt、Git 原生团队 |
| AtScale | 企业级虚拟化，就地查询不搬数 | 大型企业、多引擎 |
| Cube Cloud | headless BI，API 优先 | 多前端/嵌入式分析 |
| Snowflake Semantic Views | 仓内原生语义对象 | Snowflake 单栈 |
| Databricks Metric Views | 湖仓内原生指标视图 | Databricks 湖仓 |

**成本案例**：Bilt Rewards 集中实体关系到 dbt Semantic Layer，经 GraphQL 端点供给嵌入式分析，放弃按席位的 BI embed，**分析成本下降约 80%**。

### dbt 语义模型写法

```yaml
semantic_models:
  - name: orders
    model: ref('fct_orders')
    entities:
      - name: order
        type: primary
        expr: order_id
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: total_amount
        agg: sum
        expr: amount
```

MetricFlow 四种指标类型：Simple（聚合单 measure）/ Ratio（一 measure 除另一）/ Cumulative（按时间累计）/ Derived（由其他指标组合，如毛利=收入−成本）。

### 评估七项 + 落地四阶段

- **评估**：数据源兼容性 / BI 原生连接器 / 安全治理 / 性能 / 建模灵活性 / AI 就绪 / 弹性扩展。
- **该上语义层的三个警号**：同时用多个分析工具、持续有人抱怨数据难拿、部门报表数字对不上。
- **落地阶段**：盘点 KPI → 原子模型 `fct_*.sql` → 度量定义 `metrics/*.yml` → 血缘捕获 `manifest.json` → BI 集成 → 治理运营（PR+审查，owner 批准+CI 通过才可合并）。

## 对本项目的直接映射

- 本项目多品牌统一分析架构的"指标计算层"正是语义层的落地对象——[[multi_brand_unified_analytics]] 的"集中定义不可协商的指标"与语义层"一个指标一个口径"理念一致。
- [[retail_analytics_reporting_2026]] 的报表口径应沉淀为语义层度量定义，避免各部门各自重算售罄率/周转。
- [[data_governance_tech_routes_2026]] 的语义层能力（如腾讯云 WeData Unity Semantics）是产品化路径。
- 给本项目的 ChatBI/对话式分析入口（已在 [[multi_brand_unified_analytics]] 第三阶段规划）提供"受治理指标目录"底座，Agent 经 MCP 只读已批准指标。

## 关联页面

- [[semantic_layer_metrics_2026]] — 本源编译出的概念页
- [[retail_analytics_reporting_2026]] — 服装零售报表口径
- [[data_governance_tech_routes_2026]] — 含语义层能力的治理平台路线
- [[multi_brand_unified_analytics]] — 多品牌指标一致性架构

## 待办 / 待验证

- [ ] 本项目是否应把售罄率/周转天数做成 dbt MetricFlow 度量定义待评估
- [ ] OSI 标准与现有指标字典（业务术语库）的映射未做
"""

# ---------- Source 3: 零售数据质量 2026 可信度 ----------
s3 = """---
type: source
title: 零售数据质量 2026：从"批后清洗"到"情境可信度"
tags: [data_quality, retail, trustworthiness, dcmn, data_health, governance, source]
sources: [2026-08-09_Melissa信通院_零售数据质量2026可信度基准, https://www.cfotech.asia/story/how-data-quality-in-retail-powers-business-outcomes-in-2026, https://cloud.kd.cn/ask/110222.html, https://cloud.kd.cn/ask/110265.html, https://www.shopify.com/hk-en/enterprise/blog/data-insights-strategy, https://www.nisum.com/nisum-knows/ai-data-readiness-in-retail-commerce-how-to-stand-out-in-2026]
created: 2026-08-09
updated: 2026-08-09
cross_refs: [[data_quality_governance]], [[data_asset_management_2026]], [[retail_data_workflow_2026]], [[data_quality_retail_practice]]
---

# 零售数据质量 2026：从"批后清洗"到"情境可信度"

> **一句话摘要**：2026 零售数据质量的定义升级为 **contextual trustworthiness（情境可信度）**——可即时、自信、合规地采取行动的数据；信通院白皮书给出 DQS 四项基准（完整性≥99.5% / 准确性≥99.9% / 一致性差异≤0.1% / 及时性 T+0≥80%），考核从"技术建设完成率"转向"业务价值转化率"。

> **来源**：CFOtech Asia / Melissa + 中国信通院《数据中台发展白皮书（2026 版）》/ DCMM（GB/T 36073-2018）/ Shopify / Nisum
> **最后更新**：2026-08-09

## 核心要点

1. **定义升级**：情境可信度四要求——Proactively correct（实时持续校验）/ AI-ready / Context-aware（按用例区别解释）/ Ethically governed。
2. **信任缺口量化**：67% 数据专业人士不完全信任本组织数据；64% 把数据质量列首要挑战；全球平均数据泄露成本 $4.4M；>70% 国内企业采用"数据健康度指数"考核。
3. **四大新挑战**：AI 数据污染、全渠道数据速度、隐私优先的富化、复合身份复杂度（entity resolution）。
4. **五大支柱**：交互点智能校验 / 持续数据健康监测 / 情境化质量规则 / 隐私合规一方数据富化 / 跨系统实体解析。
5. **国内基准（信通院 + DCMM）**：DQS 四维度基准值 + 零售侧重（库存预测偏差≤10%、业务渗透率≥80%、促销秒级时效）。

## 详细内容

### 数据服务质量指标（DQS，2026 行业基准）

| 维度 | 关键指标 | 2026 基准值 |
|------|---------|------------|
| 完整性 | 核心字段非空率 | **≥ 99.5%** |
| 准确性 | 数据校验通过率 | **≥ 99.9%** |
| 一致性 | 跨系统数据差异率 | **≤ 0.1%** |
| 及时性 | 数据 T+0 更新占比 | **≥ 80%** |

另一组口径：核心业务表数据缺失率 < 0.1%、关键字段准确率 ≥ 99.9%、T+1 离线数据次日 8:00 前就绪、实时数据秒级、100% 核心链路数据血缘自动解析。

### 零售 / 电商场景侧重

| 维度 | 零售电商侧重 |
|------|-------------|
| 核心目标 | 提升转化率、降低获客成本 |
| 数据时效 | **分钟级（促销秒级）** |
| 安全合规 | 隐私计算应用率、用户授权合规 |
| 硬指标 | **库存预测偏差 ≤ 10%**；业务渗透率 ≥ 80% |

### 成熟度自评：DRI 五维（0–100）

Nisum Data Readiness Index：quality / governance / accessibility / context / operability，建议**每季度重评一次**。三阶段：打地基（统一分散数据源+指派数据所有权）→ 建信任与上下文（常态清洗+术语表+血缘）→ 规模化与优化（监控数据漂移、季度重估）。

## 对本项目的直接映射

- 本库 [[data_quality_governance]] 的四维框架与信通院 DQS 一致，可在 [[data_quality_retail_practice]] 中补入 2026 基准阈值（非空率≥99.5%、校验通过≥99.9%）。
- "情境可信度"对应 [[retail_data_workflow_2026]] 的 EDA 前的清洗环节——在采集点（POS/CRM/会员注册）即时校验优于批后清洗。
- 库存预测偏差≤10% 与本库 kb_benchmarks 的库存健康红线口径一致，可作为 [[data_asset_management_2026]] 的"面向 AI 数据供给"质量门槛。
- 复合身份（entity resolution）对应 [[multi_brand_unified_analytics]] 的跨品牌会员打通——同一客户散落数十系统需统一画像。

## 关联页面

- [[data_quality_governance]] — 数据质量常态化治理框架
- [[data_asset_management_2026]] — 数据资产管理与面向 AI 供给
- [[retail_data_workflow_2026]] — CRISP-DM 工作流中的清洗环节
- [[data_quality_retail_practice]] — 本项目数据质量实操规范

## 待办 / 待验证

- [ ] 本项目现有质量检查是否覆盖 DQS 四维度阈值待核对
- [ ] 库存预测偏差≤10% 与本库库存健康红线（库龄/断码率）的联合看板未建
"""

# ---------- Source 4: 服装五维指标体系 + 数仓分层 ----------
s4 = """---
type: source
title: 服装行业指标体系五维框架 × 电商数仓分层建设（2026）
tags: [apparel, kpi, metrics_framework, data_warehouse, dimensional_modeling, sql, source]
sources: [2026-08-09_CSDN_服装行业指标体系五维框架与电商数仓分层建设, https://blog.csdn.net/weixin_45967165/article/details/160069672, https://blog.csdn.net/xuchangwen11/article/details/156534617, https://www.jiandaoyun.com/nblog/493229/, https://beefed.ai/zh/personas/maryam-the-data-engineer-data-modeling/showcase]
created: 2026-08-09
updated: 2026-08-09
cross_refs: [[retail_analytics_reporting_2026]], [[sku_fine_management]], [[python_sql_integration_patterns_2026]], [[data_asset_management_2026]]
---

# 服装行业指标体系五维框架 × 电商数仓分层建设（2026）

> **一句话摘要**：服装行业指标体系应围绕**商品/销售/库存/渠道/用户**五维构建，配"定目标→盘数据→定指标→分场景"四步法；数仓侧用 raw→stg→mart 三层 + 星型模式 + SCD Type 2 把口径落到工程约束，进销存 SQL 六种写法覆盖约 85% 业务问题。

> **来源**：CSDN 王浩《服装行业指标体系搭建指南》+ CSDN 电商数仓实战 + 简道云进销存 + beefed 零售数仓蓝图
> **最后更新**：2026-08-09

## 核心要点

1. **五维框架**：商品（款对不对）/ 销售（卖得好不好）/ 库存（压不压货）/ 渠道（在哪卖）/ 用户（谁在买）。
2. **最致命特征**：生命周期 3–6 个月、SKU 极多、款色码维度爆炸、库存风险高（过季价值剩 30%）。
3. **四步法**：定目标找对齐（北极星指标）→ 盘数据清家底（SPU/SKU 编码统一）→ 定指标建字典（一个指标一个口径）→ 分场景做应用。
4. **数仓分层**：四大标准库（业务术语库/码值库/命名规范/指标定义规范）+ raw→stg→mart + 星型蓝图 + SCD Type 2。
5. **进销存 SQL 六种写法**：LEFT JOIN+COALESCE / 窗口函数时点库存 / CTE 分层 / 分组聚合 / 条件聚合 / 物化快照；五条性能策略综合 IO↓68%、吞吐↑2.3x。

## 详细内容

### 五维核心指标（节选）

| 维度 | 最核心指标 | 说明 |
|------|-----------|------|
| 商品 | 爆款识别 + 新品存活率（30 天动销 SKU 占比） | 萌芽期追单、选款健康度 |
| 销售 | **售罄率 = 已售/总到货** | 30 天 <30% 有问题、60 天 <50% 危险 |
| 库存 | **库龄**（>90 天基本死库存）+ **断码率** | 预警而非积压后知 |
| 渠道 | ROI / 退货率 / O2O 渗透率 | 直营/加盟/电商/直播多元 |
| 用户 | **复购率** + 风格偏好 | 选款与推荐核心依据 |

### 实战案例（女装 200 店 / 年销 8 亿）核心指标目标

| 指标 | 目标 |
|------|------|
| 售罄率（90 天） | > 70% |
| 库存周转天数 | < 90 |
| 库龄 > 90 天占比 | < 15% |
| 复购率（180 天） | > 35% |
| 会员贡献占比 | > 60% |

上线一年实绩：售罄率 58%→**73%**、周转 112→**85 天**、库龄>90 天 22%→**12%**、复购 28%→**38%**。

### 数仓分层与建模

- 四大标准库：业务术语库 / 数据字典码值库 / 命名规范（`{层}_{主题域}_{业务过程}_{描述}_{刷新周期}`）/ 指标定义规范（原子指标+修饰词+时间周期）。
- 主题域：交易/流量/用户/商品/营销。一致性维度 `dim_date/dim_product/dim_customer` 跨域分析基础。
- 星型蓝图：raw→stg→mart；`fact_sales` + 六维 `dim_*`；价格随时间变化维度用 **SCD Type 2** 保历史；度量层统一口径。

### 进销存 SQL 六种写法（覆盖率 ~85%）

LEFT JOIN + COALESCE 容错合并；窗口函数 `SUM(...) OVER(PARTITION BY ... ORDER BY ... ROWS UNBOUNDED PRECEDING)` 算时点库存；CTE 分层；分组聚合；条件聚合 `SUM(CASE WHEN move_type='IN' THEN qty ELSE 0 END)`；物化快照 `snap_inventory_daily`。五条性能策略：时间裁剪 / 覆盖索引 / 冷热分层 / 月分区+并行 / 高频指标预计算——**IO↓68%、吞吐↑2.3x**。

## 对本项目的直接映射

- 五维框架是 [[retail_analytics_reporting_2026]] 报表体系的指标骨架，可直接对齐本项目"商品/销售/库存/渠道/用户"看板。
- 款-色-码三级下钻与 [[sku_fine_management]] 的精细化 SKU 管理一致；断码率/库龄指标应纳入库存健康看板。
- SQL 六种写法可补进 [[python_sql_integration_patterns_2026]] 与零售数仓实践；SCD Type 2 对应价格历史维度。
- 标准库（术语库/码值库）是 [[data_asset_management_2026]] "数据标准管理"在服装零售的具体实现。

## 关联页面

- [[retail_analytics_reporting_2026]] — 服装零售报表与指标口径
- [[sku_fine_management]] — 精细化 SKU（款色码）管理
- [[python_sql_integration_patterns_2026]] — Python 与 SQL 集成模式
- [[data_asset_management_2026]] — 数据标准与资产管理

## 待办 / 待验证

- [ ] 本项目指标字典与五维框架的覆盖度待盘点
- [ ] SCD Type 2 在本项目价格维度是否已落地待核对
"""

# ---------- New concept: semantic_layer_metrics_2026 ----------
c1 = """---
type: concept
title: 语义层与指标层（Semantic Layer / Metrics Layer）2026
tags: [semantic_layer, metrics_layer, dbt, metricflow, osi, ai_agent, governance, headless]
sources: [2026-08-09_Kaelio_Supaboard_dbt_语义层与指标层2026全景]
created: 2026-08-09
updated: 2026-08-09
cross_refs: [[data_governance_tech_routes_2026]], [[retail_analytics_reporting_2026]], [[multi_brand_unified_analytics]], [[data_quality_governance]], [[duckdb_olap_engine_2026]]
---

# 语义层与指标层（Semantic Layer / Metrics Layer）2026

> **一句话摘要**：语义层是 2026 年成为 AI 基础设施的数据抽象层——把"已定义好的指标/维度/实体关系/业务规则"与原始数据分离，对 BI 工具与 AI Agent 统一暴露，解决多团队对同一指标定义不一、报表口径漂移的问题。

> **来源**：Kaelio / Supaboard / bixtech / beefed / 掘金 2026 综述
> **最后更新**：2026-08-09

## 它有什么、没有什么

**有**：Entities（业务名词与关系）/ Metrics（具名、已定义度量，含计算逻辑与排除项）/ Dimensions（切片方式）/ Relationships（join 逻辑）/ 治理验证（谁拥有、谁能改、如何断言正确）/ 业务规则（财年日历、汇率、自定义周期）。

**没有**：不含原始数据本身（行留仓内，AtScale 强调"就地查询"）；不是数据目录（catalog 说表存在，语义层说数字含义）；不是知识图谱（但 Looker 2026 Knowledge Catalog 让边界模糊）；本身不是 BI 工具（headless 前提：这层比任何看板活得更久）。

> Lloyd Tabb（LookML 之父）诊断："SQL 已经 50 岁了，它没有可复用性。你在一个查询里定义的计算，会在另一个查询里再定义一遍。"语义层把计算定义为持久对象。

## 为什么 2026 是规模化落地之年

- **AI 就绪**：LLM/Agent 需要结构化一致的数据才能给准答案。
- **多工具并存**：Tableau / Power BI / Excel / 自研应用同时用。
- **治理强制**：监管压力要求可审计与定义一致。
- 一家大型零售商上线后 **80% 查询在 1 秒内完成**。

## 主流方案（2026）

| 方案 | 架构特点 | 适合谁 |
|------|---------|--------|
| dbt Semantic Layer (MetricFlow) | 指标与 dbt 模型同仓定义，确定性编译 SQL | 已跑 dbt、Git 原生团队 |
| AtScale | 企业级虚拟化，就地查询不搬数 | 大型企业、多引擎 |
| Cube Cloud | headless BI，API 优先 | 多前端/嵌入式分析 |
| Snowflake Semantic Views | 仓内原生语义对象 | Snowflake 单栈 |
| Databricks Metric Views | 湖仓内原生指标视图 | Databricks 湖仓 |
| Power BI Semantic Model | 星型建模 + XMLA endpoint | 微软栈 |

**标准化信号**：**Open Semantic Interchange（OSI）2026-01 首发**，把 datasets/metrics/dimensions/relationships/context 做成跨厂商可交换标准——语义层从"产品私有模型"变成"多工具/多引擎/多 agent 可共用的契约"。

## MetricFlow 指标类型

| 类型 | 作用 | 示例 |
|------|------|------|
| Simple | 聚合单个 measure | 总收入 |
| Ratio | 一 measure 除另一 | 客单价 |
| Cumulative | 按时间累计 | 年初至今收入 |
| Derived | 由其他指标组合 | 毛利 = 收入 − 成本 |

`exposures` 把看板/应用/AI Agent 登记进依赖图，受 CI 测试保护——破坏答案的变更进生产前被拦下。

## 给 AI Agent 的三条纪律

1. **不给裸 SQL 权限**：经 dbt **MCP server** 以受治理方式发现并查询指标——Agent 只看已批准指标目录（最小权限）。
2. **持续验证**：记录 Agent 查询、与官方定义比对；指标变更在 CI 跑测试。
3. **业务逻辑进版本化契约**：Agent 请求"已定义好的指标"而非自写 SQL，降低幻觉、各工具得同一数字。

> 今天真正的问题不是"自然语言能不能翻成 SQL"，而是"自然语言能不能先落到受治理的业务语义空间，再由确定性引擎生成 SQL"。

## 评估与落地

- **七项评估**：数据源兼容 / BI 原生连接器 / 安全治理 / 性能 / 建模灵活性 / AI 就绪 / 弹性扩展。
- **三个警号**：同时用多个分析工具、持续有人抱怨数据难拿、部门报表数字对不上。
- **落地阶段**：盘点 KPI → 原子模型 `fct_*.sql` → 度量定义 `metrics/*.yml`（`dbt build`+`dbt test`）→ 血缘捕获 `manifest.json` → BI 集成 → 治理运营（PR+审查，owner 批准+CI 通过才可合并；指标注册表含 owner/SLA/消费方；测试与签字后才标 certified）。
- **成本案例**：Bilt Rewards 集中实体关系到 dbt Semantic Layer，经 GraphQL 供给嵌入式分析，放弃按席位 BI embed，**分析成本↓约 80%**。

## 服装零售映射

- 多品牌统一分析架构的"指标计算层"即语义层落地对象——集中定义不可协商的指标（售罄率/周转/复购），各品牌分布使用。
- 报表口径应沉淀为度量定义，避免各部门各自重算；ChatBI/对话式入口经 MCP 只读已批准指标。
- 库存预测偏差≤10%、T+0 更新≥80% 等质量门槛可作为语义层治理验证的断言。

## 关联页面

- [[data_governance_tech_routes_2026]] — 含语义层能力的治理平台路线
- [[retail_analytics_reporting_2026]] — 服装零售报表与指标口径
- [[multi_brand_unified_analytics]] — 多品牌指标一致性架构（指标计算层）
- [[data_quality_governance]] — 数据质量常态化治理（口径一致基础）
- [[duckdb_olap_engine_2026]] — 嵌入式查询引擎可作为语义层下游消费方
"""

for fn, content in [
    ('2026-08-09_DuckDB官方_v1.5系列与Python嵌入式分析范式.md', s1),
    ('2026-08-09_Kaelio_Supaboard_dbt_语义层与指标层2026全景.md', s2),
    ('2026-08-09_Melissa信通院_零售数据质量2026可信度基准.md', s3),
    ('2026-08-09_CSDN_服装行业指标体系五维框架与电商数仓分层建设.md', s4),
    ('semantic_layer_metrics_2026.md', c1),
]:
    p = os.path.join(SRC, fn) if fn.startswith('2026') else os.path.join(CON, fn)
    w(p, content)

print('DONE sources+concept: 5')
