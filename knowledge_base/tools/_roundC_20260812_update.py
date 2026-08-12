#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round C (2026-08-12) — 编译知识到 concept/practice 页面 + 更新 index.md
放 tools/ 下，保持 vault 根整洁。输出 UTF-8 + LF。"""
import io, os, re

WIKI = os.path.join(os.path.dirname(__file__), '..', 'wiki')
IDX = os.path.join(WIKI, 'index.md')

def read(p):
    return io.open(p, encoding='utf-8').read()
def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('UPD', os.path.relpath(p, os.path.join(WIKI, '..')))

# ---------- 各页面新增小节（编译后的知识） ----------
SUB = {}

SUB['concepts/SQL查询性能优化.md'] = (
'2026-08-12_DuckDB官方_查询性能调优三层级实战',
"""## DuckDB 查询性能调优三层级（2026-08 新增）

DuckDB Labs 给出三层查询优化栈，与本项目"款号/色号/门店编码 group by/join"的 OLAP 分析高度契合：

| 层级 | 技术 | 加速 | 验证/注意 |
|------|------|------|----------|
| L1 文件级 | Hive 分区 + Glob | 10–365x | 100 文件→2-3；典型 30s→1s；CSV 换 Parquet 最高 ROI |
| L2 行组级 | 谓词下推 + 行组调优 | 2–15x | `EXPLAIN ANALYZE` 见 `PARQUET_SCAN ... Filters:`；反模式：列上 CAST/LIKE、列算术、大 IN 列表（→SEMI JOIN）；行组默认 122880，频繁日期过滤用 50000–80000 |
| L3 库级 | Filter Index + 物化表 | 5–100x | 1B 行聚合预聚到小时级后仅扫 168 行，毫秒返回 |

**内存**：`PRAGMA memory_limit='8GB'` + `temp_directory` 指 SSD；`PRAGMA show_temporary_files` 检测 spill（落盘慢 10–100x）。物化预聚合表胜过索引——本项目"每日指标预计算"可直接套用。

> 映射：DuckDB 三层栈补强本项目 [[duckdb_olap_engine_2026]] 的生产调优层；与 [[polars_vs_pandas_2026]] 的"按 workload 选引擎"一致（DuckDB 擅 SQL 聚合/即席，Polars 擅 ETL 流水线）。
""")

SUB['concepts/duckdb_olap_engine_2026.md'] = (
'2026-08-12_DuckDB官方_查询性能调优三层级实战',
"""## 查询性能调优三层级（2026-08 补强）

DuckDB 生产调优三层栈：**L1 文件级 Hive 分区+Glob（10–365x）/ L2 行组级谓词下推（2–15x，需 `EXPLAIN ANALYZE` 验证，避开列上 CAST/LIKE 与大 IN 列表反模式）/ L3 库级 Filter Index(ART)+物化表（5–100x，1B 行→168 行扫描）**。内存溢出落盘会慢 10–100x，用 `memory_limit` + `show_temporary_files` 监控。

> 映射：详见 [[SQL查询性能优化]] 的 2026-08 新增小节；物化表思路用于本项目每日指标预计算。
""")

SUB['concepts/streamlit_dashboard_2026.md'] = (
'2026-08-12_Streamlit_企业级架构与生产部署路线',
"""## 2026-08 企业级架构与生产部署深化

**部署决策矩阵**（安全性/可扩展性/环境一致性/运维成本）：生产首选私有 Docker 容器化。推荐拓扑 `User → Nginx(SSL/Auth) → Docker(Streamlit) → 内部 DB/LLM API`，多实例 K8s + 会话亲和。streamlit-elements（MUI）实现可拖拽网格，突破原生线性布局。

**安全监控**：OAuth2.0/SAML RBAC、TLS/AES-256、输入校验、速率限制；Prometheus+Grafana 盯响应时间/内存/并发/缓存命中；多级缓存（分页+流式+Parquet 压缩）。

**2026 部署选项**：

| 选项 | 成本 | 痛点 |
|------|------|------|
| Community Cloud | 免费 | ~1GB 内存上限、12h 休眠、仅 1 私有应用、无自定义域名 |
| livemy.app | $10/月 | 自定义域名+SSL、无 1GB 上限 |
| Railway/Render | $5–7/月起 | 多服务架构 |
| Docker VPS | $5–20/月 | 完全控制，需自维护 |

> 映射：与 [[streamlit_production_dashboard]] 生产部署小节互补；可拖拽大屏借 `st.bottom` + streamlit-elements 做多品牌切换栏。
""")

SUB['concepts/data_governance_tech_routes_2026.md'] = (
'2026-08-12_阿里云_数据中台落地方法论与ETL事务管理',
"""## 2026-08 数据中台落地方法论（阿里云 Dataphin 路线）

**选型评估矩阵**：传统 ETL/数仓 vs 智能数据平台——数据源 50+、湖仓一体、治理"左移"到设计阶段、AI 全链路、API 服务化+资产智能体+BI 联动。

**三阶段路线图**：Phase1 试点（1–3 月，高价值场景）→ Phase2 体系（3–6 月，标准+自助）→ Phase3 规模（6 月+，资产运营）。避坑：重技术轻业务 / 贪大求全 / 治理后置 / 忽视运营。

**量化成效**：查询效率 **+90%**；瓴羊 Dataphin 自动 ETL 开发效率 **+30–50%**、异常拦截使质量事故 **-60% 以上**。

> 映射：本项目三品牌数据治理应借鉴"治理左移 + 三阶段"，避免一次性大而全；详见 [[data_quality_governance]] 的 ETL 事务级质量门禁补强。
""")

SUB['concepts/data_quality_governance.md'] = (
'2026-08-12_阿里云_数据中台落地方法论与ETL事务管理',
"""## ETL 事务管理与全链路防坑（2026-08 补强）

全链路事务管理把质量门禁前置到 ETL 每一步：

```
需求梳理(口径先行) → 抽取(CDC+日志比对+Kafka) → 转换(多级校验/异常隔离表)
→ 加载(幂等写入/批量提交/可回滚) → 监控补偿(自动告警) → 血缘回溯(DAG)
```

零售全渠道订单集成案例（MySQL 门店/Oracle 商城/API/第三方/Kafka）用 FineDataLink 低代码 DAG 编排，异常自动补偿，实现"不丢不重"。

> 映射：与 [[data_quality_retail_practice]] 的导入校验互补；本项目三品牌（太平鸟/卡宾/东尚）CSV→入库链路应强化幂等+回滚+补偿，避免历史大批量导入的无 DELETE 重叠重复。
""")

SUB['concepts/polars_vs_pandas_2026.md'] = (
'2026-08-12_Polars2.1_Pandas3.0_生产级性能对比',
"""## 2026-08 Polars 2.1 / Pandas 3.0 生产级基准刷新

**johal.in 50GB 实测**（32GB RAM）：Polars 2.1.0 在 CSV Join 上比 Pandas 3.0.1 快 **12.4x**、内存 **-60%**；DuckDB 1.2.3 比 Spark 4.0（100GB）延迟 **-89%**；自建 Polars+DuckDB 栈比托管(Fivetran+Snowflake) 成本 **$0.03/GB vs $0.18/GB、快 12x**；预测 2027 年 70% 生产分析用 Rust 工具（Polars/DataFusion）。

**ima.qq.com 10M 行**：过滤 6x / GroupBy 10x / Join 12x / 排序 10x / 字符串 11x / 滚动 9x；内存省 65–73%；Polars 月下载 3000 万（较 2024 初 +300%）。**itsourcecode 1M 行**：Read 9x / GroupBy 30x / Join 14x。**pyinns 10M 行**：Read 4.7x / GroupBy 5.4x；内存 ~450MB vs ~1.8GB。

**结论**：不该全面迁移，该全面评估——混合用（Polars 做 ETL/重计算，Pandas 做 ML/可视化）。12.4x Join / -60% 内存与 kb `speed_multiplier=8` 同属"数倍至十余倍"区间，口径差异（50GB join vs 千万行通用），**非硬矛盾**。

> 映射：内存实测补 [[arrow_zero_copy_interop_2026]]；混合用范式见 [[python_data_stack_decision_2026]]。
""")

SUB['concepts/python_data_stack_decision_2026.md'] = (
'2026-08-12_Polars2.1_Pandas3.0_生产级性能对比',
"""## 混合用范式成为主流（2026-08 补强）

ima.qq.com 观点：Polars 月下载 3000 万，"二选一"正在变成"混合用"。Polars 做 >50 万行/ETL 流水线，Pandas 做 ML（sklearn 原生）/matplotlib 可视化；50 万行以下两者感知不到差别。

> 映射：本项目 Streamlit 看板用 Pandas/Plotly 展示、底层重计算用 Polars/DuckDB，经 [[arrow_zero_copy_interop_2026]] 零拷贝串联；边界在 50 万行。
""")

SUB['concepts/arrow_zero_copy_interop_2026.md'] = (
'2026-08-12_Polars2.1_Pandas3.0_生产级性能对比',
"""## 2026 内存实测补强（2026-08）

ima.qq.com 内存对比（Polars vs Pandas）：1000 万行混合 3.2GB→1.1GB（省 65%）、字符串密集 5.8→1.9GB（省 67%）、GroupBy 峰值 8.4→2.3GB（省 73%）。

> 与 kb `memory_saving_pct=0.87`（早期 Pandas 内部/其他 workload 口径）为口径差异，非硬矛盾；与 [[polars_vs_pandas_2026]] 的 2026-08 基准一致。
""")

SUB['practices/streamlit_production_dashboard.md'] = (
'2026-08-12_Streamlit_企业级架构与生产部署路线',
"""## 企业级部署架构（2026-08 补强）

**拓扑**：`User → Nginx(SSL/Auth) → Docker(Streamlit) → 内部 DB/LLM API`，多实例 K8s + 会话亲和。直接暴露 8501 被视为危险。

**安全**：OAuth2.0/SAML RBAC、TLS/AES-256、输入校验、速率限制/API 防护。**监控**：Prometheus+Grafana（响应时间/内存/并发会话/缓存命中率）。**缓存**：内存分页 + 流式 + Parquet 压缩。

**2026 部署选项**：Community Cloud（~1GB 上限/12h 休眠）→ livemy.app $10/月（自定义域名）→ Railway/Render $5–7/月 → Docker VPS $5–20/月（完全控制）。多品牌看板走 Docker+Nginx+认证外挂；对外分享用零门槛托管；耗时 IO 必缓存。

> 映射：与 [[streamlit_dashboard_2026]] 2026-08 企业级深化小节互补；可拖拽大屏借 streamlit-elements。
""")

SUB['practices/multi_brand_unified_analytics.md'] = (
'2026-08-12_阿里云_数据中台落地方法论与ETL事务管理',
"""## 数据中台落地与跨品牌治理（2026-08 补强）

**数据中台三阶段 + 治理左移 + 湖仓一体**：查询效率 **+90%**、质量事故 **-60%**、ETL 开发效率 **+30–50%**。跨品牌治理：主数据统一视图 + 标准字典 + 分级分类。

本项目三品牌（太平鸟/卡宾/东尚）CSV→入库→飞书推送链路应纳入**幂等写入 + 批量提交 + 自动补偿**，避免历史大批量导入的无 DELETE 重叠重复；同时把"治理左移"延伸到 Tableau 报表筛选器配置层（曾因筛选器漏勾选致女装数据消失），加防呆校验。

> 映射：与 [[brand_config_driven_system]] 的 RCBT 主数据映射、[[data_governance_tech_routes_2026]] 的智能平台路线一致。
""")

SUB['practices/brand_config_driven_system.md'] = (
'2026-08-12_阿里云_数据中台落地方法论与ETL事务管理',
"""## 数据中台主数据治理对齐（2026-08 补强）

阿里云数据中台路线强调"主数据统一视图 + 标准字典 + 分级分类"，与本项目 [[brand_config_driven_system]] 的 RCBT 主数据映射（Chantelle 9 品牌印证）一致。落地要点：治理左移（质量/合规前置到设计阶段）、三阶段渐进（先高频高价值场景）、避免一次性大而全。

> 映射：三品牌 ETL 链路（CSV→入库）应强化幂等+回滚+补偿，参见 [[multi_brand_unified_analytics]] 的 2026-08 补强。
""")

# ---------- 执行页面更新 ----------
for rel, (srcfn, sub) in SUB.items():
    p = os.path.join(WIKI, rel)
    if not os.path.exists(p):
        print('SKIP(not found):', rel); continue
    s = read(p)
    # 更新 updated 日期
    s = re.sub(r'^updated:.*$', 'updated: 2026-08-12', s, count=1, flags=re.M)
    # 追加 source 到 sources 列表（单行情形）
    m = re.search(r'^sources:\s*\[([^\]]*)\]\s*$', s, re.M)
    if m and srcfn not in m.group(1):
        inner = m.group(1).strip()
        newinner = (inner.rstrip(',') + ', ' + srcfn) if inner else srcfn
        s = s[:m.start()] + 'sources: [' + newinner + ']' + s[m.end():]
    # 插入小节（置于首个"关联"区块之前，保持链接在末）
    idx = s.find('\n## 关联页面')
    if idx == -1:
        idx = s.find('\n## 关联')
    if idx == -1:
        s = s.rstrip('\n') + '\n\n' + sub.rstrip('\n') + '\n'
    else:
        s = s[:idx] + '\n' + sub.rstrip('\n') + '\n' + s[idx:]
    write(p, s)

# ---------- 更新 index.md ----------
idx = read(IDX)
# 1) frontmatter updated 日期
idx = re.sub(r'^updated:.*$', 'updated: 2026-08-12', idx, count=1, flags=re.M)

# 2) 插入 4 条 source 行（wiki/sources/ 表头后）
SRC_ROWS = """| [[2026-08-12_DuckDB官方_查询性能调优三层级实战]] ⭐ NEW | DuckDB 查询调优三层级：L1分区10-365x/L2谓词下推2-15x/L3物化表5-100x·1B行→168行·落盘慢10-100x | duckdb, sql, tuning, parquet, source |
| [[2026-08-12_Streamlit_企业级架构与生产部署路线]] ⭐ NEW | Streamlit 企业级：Docker+Nginx+Auth+K8s·streamlit-elements·OAuth2/SAML·Prometheus·Community Cloud 1GB/12h休眠 vs livemy $10 vs Docker VPS | streamlit, deployment, security, source |
| [[2026-08-12_阿里云_数据中台落地方法论与ETL事务管理]] ⭐ NEW | 数据中台三阶段+治理左移：查询效率+90%/质量事故-60%/ETL开发+30-50%·ETL事务管理(CDC+幂等+补偿) | data_governance, middle_platform, etl, source |
| [[2026-08-12_Polars2.1_Pandas3.0_生产级性能对比]] ⭐ NEW | Polars2.1 vs Pandas3.0 50GB Join 12.4x/内存-60%·DuckDB vs Spark 100GB -89%·$0.03 vs $0.18/GB·混合用范式 | polars, pandas, benchmark, source |
"""
mm = re.search(r'(### wiki/sources/ — 来源摘要库\s*\n\| 页面 \| 说明 \| 标签 \|\n\|------\|------\|------\|\n)', idx)
if mm:
    idx = idx[:mm.end()] + SRC_ROWS + idx[mm.end():]
else:
    print('WARN: sources header not found, skip source rows')

# 3) 标记 UPDATED（概念+实践）
UPD_NAMES = [
    'SQL查询性能优化', 'duckdb_olap_engine_2026', 'streamlit_dashboard_2026',
    'data_governance_tech_routes_2026', 'data_quality_governance', 'polars_vs_pandas_2026',
    'python_data_stack_decision_2026', 'arrow_zero_copy_interop_2026',
    'streamlit_production_dashboard', 'multi_brand_unified_analytics', 'brand_config_driven_system',
]
for nm in UPD_NAMES:
    pat = re.compile(r'(\| \[\[' + re.escape(nm) + r'(?:\|[^\]]*)?\]\])')
    def repl(m):
        tok = m.group(1)
        line = m.group(0)
        if 'UPDATED' in line:
            return m.group(0)
        return tok + ' ⭐ UPDATED'
    idx = pat.sub(lambda m: (m.group(1) + ' ⭐ UPDATED') if 'UPDATED' not in m.group(0) else m.group(0), idx)

# 4) 追加 round 历史行
ROUND_ROW = ("\n| **121** | **08-12 17:06** | **L2_06/07+查漏 (C轮)** | "
             "**s4(DuckDB三层调优/Streamlit企业级部署/数据中台落地+ETL事务/Polars2.1 Pandas3.0基准)"
             "/c8更新(SQL优化+duckdb+streamlit_dashboard+data_gov_routes+data_quality+polars+python_stack+arrow)"
             "/p3更新(streamlit_production+multi_brand+brand_config)/L3同步(wiki页)3处/织网双向/矛盾0处 ✅** |")
# 找到最后一个 round 行（| **数字** | ...）后插入
last = None
for mm2 in re.finditer(r'^\| \*\*\d+\*\* \|', idx, re.M):
    last = mm2
if last:
    pos = last.start()
    # 插入到该行之前（保持表格顺序，置于末尾）
    idx = idx[:pos] + ROUND_ROW + '\n' + idx[pos:]
else:
    idx = idx.rstrip('\n') + '\n' + ROUND_ROW + '\n'

write(IDX, idx)
print('DONE update: pages=%d + index' % len(SUB))
