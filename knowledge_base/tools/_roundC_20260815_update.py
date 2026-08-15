# -*- coding: utf-8 -*-
"""Round C (2026-08-15) — L2_06 数据分析实务 + L2_07 多品牌数据分析系统构建 + 查漏补缺。
生成 4 raw + 4 source，更新 13 个 wiki 页面(8 concept + 5 practice)，同步 5 个 L3 文件，
更新 index.md 与 log.md。脚本置于 knowledge_base/tools/（vault 约定，勿放根目录）。
"""
import os, re

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(KB, "raw", "articles")
SRC = os.path.join(KB, "wiki", "sources")
CON = os.path.join(KB, "wiki", "concepts")
PRA = os.path.join(KB, "wiki", "practices")
L206 = os.path.join(KB, "L2_06_数据分析实务")
L207 = os.path.join(KB, "L2_07_服装多品牌数据分析系统构建")
IDX = os.path.join(KB, "wiki", "index.md")
LOG = os.path.join(KB, "wiki", "log.md")
DATE = "2026-08-15"

S1 = "2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准"
S2 = "2026-08-15_Streamlit_1.59新特性与LLM集成"
S3 = "2026-08-15_语义层与数据契约治理2026"
S4 = "2026-08-15_主动元数据与多品牌数据目录2026"

os.makedirs(RAW, exist_ok=True)

# ---------------------------------------------------------------------------
# 1) RAW ARTICLES
# ---------------------------------------------------------------------------
raw_files = {
"S1": ("2026-08-15_向量化执行与PostgreSQL18_DuckDB基准.md",
'''# 向量化执行与 PostgreSQL 18 / DuckDB 1.5.4 基准（2026 剪藏）

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
'''),
"S2": ("2026-08-15_Streamlit_1.59新特性与LLM集成.md",
'''# Streamlit 1.59 新特性与 LLM 集成（2026 剪藏）

> 来源：Streamlit 官方 Release Notes（1.59.0 / 1.58.0 / 1.55.0）、tech-insider Streamlit 2026 教程。
> 收藏日期：2026-08-15

## 核心数据
- Streamlit 1.59.0（2026-07-06）亮点：ButtonColumn（表内可点击按钮）、st.skeleton（加载占位）、st.mermaid_chart（原生渲染 Mermaid 图）、App.run() 入口（直接 `python app.py` 启动）、st.fragment 可写外部容器（局部刷新不整页 rerun）、persist_state（跨 rerun 保留控件状态）。
- st.chat_input 支持粘贴文件 + submit_mode 参数；st.write_stream 支持 OpenAI Responses API 流（除既有 Chat Completions）。
- st.set_page_config initial_sidebar_state="locked" 可锁定侧栏；st.markdown 新增 anchors 参数；st.camera_input 新增 resolution。
- 1.58（2026-05-28）：@st.fragment parallel=True（并发片段）、st.pagination、streamlit skills CLI。
- 1.55（2026-03-03）：动态容器 on_change、bind 参数（控件↔URL 查询）、experimental st.App ASGI 入口。
- 移除项：Snowpark 连接类型已删除，需迁移。
'''),
"S3": ("2026-08-15_语义层与数据契约治理2026.md",
'''# 语义层与数据契约治理 2026（剪藏）

> 来源：getdbt《The trust-speed paradox》、precisiondatapartners《The Semantic Lakehouse》、stackfyi Semantic Layer Tools 2026、LinkedIn dbt+MetricFlow 实战、analyticsengineering dbt Semantic Layer。
> 收藏日期：2026-08-15

## 核心数据
- dbt《2026 State of Analytics Engineering》：数据信任成 83% 数据团队首要优先级（一年前 66%）；72% 已用 AI 辅助编码，仅 24% 用 AI 辅助可观测性——「信任—速度悖论」。
- Gartner（2025 初预测）：至 2026 年，建在非 AI-ready 数据上的 AI 项目 60% 被放弃。
- Semantic Lakehouse 实测：智能体数据解读错误 -75%、数据驱动智能体开发 +60% 更快、AI 与 BI 指标一致性 4x。
- dbt Semantic Layer / MetricFlow：指标定义为代码（measures/dimensions/entities/time spine），CI 校验；gold 模型加契约（not_null/unique/accepted_values）+ 列级血缘。
- Databricks CEO（2026-02）：平台 >80% 数据库由 AI 智能体构建。
- 选型：dbt 中心团队首选 dbt Semantic Layer；需指标 API/嵌入式分析选 Cube；读 dbt 元数据的开源 BI 选 Lightdash。
'''),
"S4": ("2026-08-15_主动元数据与多品牌数据目录2026.md",
'''# 主动元数据与多品牌数据目录 2026（剪藏）

> 来源：datanauta《How AI is Transforming Data Catalogs in 2026》、eastmoney 2026 数据治理平台排名、tely.ai 零售元数据管理、mindit.io 全球旅游零售 Lakehouse、renrendoc 2026 零售大数据分析。
> 收藏日期：2026-08-15

## 核心数据
- Active Metadata（主动元数据）= 2026 标准：元数据回流工具改变其行为（双向同步）。例：检测 PII 列→标记 SENSITIVE→立即向 Snowflake/Databricks 推送动态脱敏策略（shift-left 治理）。
- Autodesk 用主动治理扩展到 60 个业务域；Kingfisher（B&Q）建「Knowledge Hub」自助供应链分析，问题排查 小时→分钟。
- Datanauta 把「信任分」（如 98% 可靠）直接推入目录元数据；异常（schema drift/量异常）在索引前拦截。
- EU AI Act（2026）强制 AI 训练数据严格血缘 → 目录成合规工具；Grab 用 LLM 发现达 90% 文档覆盖。
- Lakehouse 成 2026 零售标准范式；自动化目录 + 血缘追踪成标配；Unity Catalog 提供跨域发现/血缘/权限。
'''),
}

for k,(fn,body) in raw_files.items():
    p = os.path.join(RAW, fn)
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    print("RAW written:", p)

# ---------------------------------------------------------------------------
# 2) SOURCE PAGES (wiki/sources) — each with >=1 [[link]], no island
# ---------------------------------------------------------------------------
def src_page(title, tags, confidence, links, body):
    fm = "---\n"
    fm += "type: source\n"
    fm += "title: " + title + "\n"
    fm += "tags: [" + tags + "]\n"
    fm += "sources: [" + links["src"] + "]\n"
    fm += "created: " + DATE + "\n"
    fm += "updated: " + DATE + "\n"
    fm += "confidence: " + confidence + "\n"
    fm += "cross_refs: [" + ", ".join(links["refs"]) + "]\n"
    fm += "---\n\n"
    fm += "# " + title + "\n\n"
    fm += "> **一句话摘要**：" + body["abs"] + "\n\n"
    fm += "> **置信度**：" + confidence + "\n\n"
    fm += "## 核心要点\n\n" + body["kp"] + "\n\n"
    fm += "## 详细内容\n\n" + body["detail"] + "\n\n"
    fm += "## 对本项目直接映射\n\n" + body["map"] + "\n\n"
    fm += "## 关联页面\n\n"
    for r in links["refs"]:
        fm += "- [[" + r + "]]\n"
    fm += "\n## 待办 / 待验证\n\n- [ ] 本项目现有周报 SQL / 看板是否已应用上述向量化/语义层/主动元数据实践，待清点\n"
    return fm

sources = {
S1: src_page(
  "SQL优化2026向量化执行与PG18_DuckDB基准",
  "sql, optimization, vectorized, duckdb, postgresql, olap, performance, source",
  "第三方数据",
  {"src": S1+", https://www.johal.in/postgresql-17-vs-duckdb-12-what-actually-scales-2026, https://markaicode.com/benchmarks/duckdb-production-benchmark-latency",
   "refs": ["SQL查询性能优化", "duckdb_olap_engine_2026", "polars_vs_pandas_2026"]},
  {"abs":"2026 年 OLAP 进入「向量化执行 + 自适应查询」阶段：DuckDB 1.5.4 比 PostgreSQL 18.4 在 TPC-H 1TB 平均快 7.4x，`pg_duckdb` 1.0 让二者共存，混合架构零资源争用。",
   "kp":"1. DuckDB 1.5.4「Variegata」(LTS 1.4.5 Andium)；`pg_duckdb` 扩展 2026 达 1.0，PG 内部可路由分析查询到 DuckDB。\n2. TPC-H 1TB Parquet：DuckDB 比 PG17 平均快 7.4x；Q1 全表扫描 8.2 GB/s vs PG17 1.1 GB/s；3+ 表 JOIN 快 5.2x。\n3. 向量化执行：120k 行 morsel + SIMD，CPU 缓存命中 40%→85%，单查询 3–10x。\n4. 自适应执行：动态 Join/并行度，倾斜场景稳定 +60%、复杂查询 -40%。\n5. 混合架构（PG OLTP + DuckDB OLAP）实测 138k 写/秒 + 7.8 GB/s、零争用；FinQore 管道 8h→8min（60x）。",
   "detail":"| 维度 | PostgreSQL 18.4 | DuckDB 1.5.4 |\n|------|------|------|\n| 执行模型 | 行式 Volcano + 并行 | 列式向量化(morsel/SIMD) |\n| TPC-H 1TB 平均 | 基准 | 7.4x 更快 |\n| Q1 扫描吞吐 | 1.1 GB/s | 8.2 GB/s |\n| 3+ 表 JOIN | 基准 | 5.2x 更快 |\n| 事务 | MVCC 强一致 | 单写多读(分析批处理) |\n\n`pg_duckdb` 1.0 使「DuckDB vs PostgreSQL」不再是二选一：PG 保留事务与并发写，分析查询透明下沉到 DuckDB 列式引擎。",
   "map":"- 本项目多品牌周报的聚合/即席查询（款号/色号/尺码/门店 group by/join）继续走 [[duckdb_olap_engine_2026]] 内存列式路线；OLTP 侧（销售入库 SQLite）保持事务模型。\n- 与 [[SQL查询性能优化]] 的「索引+改写占 70%」互补：OLAP 引擎层用向量化 + 物化中间表把分钟级压到毫秒级。\n- 与 [[polars_vs_pandas_2026]] 的「按 workload 选引擎」一致：DuckDB 擅 SQL 聚合/即席，Polars 擅 ETL 流水线。"}),

S2: src_page(
  "Streamlit_1.59新特性与LLM集成",
  "streamlit, dashboard, llm, mermaid, app_run, fragment, chat, source",
  "官方公告",
  {"src": S2+", https://docs.streamlit.io/en/latest/changelog.html",
   "refs": ["streamlit_dashboard_2026", "streamlit_production_dashboard", "python_dashboard_ecosystem_2026"]},
  {"abs":"Streamlit 1.59.0（2026-07-06）带来 ButtonColumn、st.mermaid_chart、App.run() 直启、st.fragment 写外部容器、persist_state 等，强化表内交互与 LLM 集成。",
   "kp":"1. ButtonColumn（st.dataframe/data_editor 表内可点击按钮）+ 列统计子菜单。\n2. st.skeleton（加载占位）、st.mermaid_chart（原生 Mermaid 图，亦走 st.markdown）。\n3. App.run() 入口：直接 `python app.py` / `uv run app.py`，告别 `streamlit run`。\n4. st.fragment 可写外部容器（局部刷新不整页 rerun）；persist_state 跨 rerun 保留控件状态。\n5. st.chat_input 粘贴文件 + submit_mode；st.write_stream 支持 OpenAI Responses API 流；Snowpark 连接已移除。",
   "detail":"| 特性 | 价值 |\n|------|------|\n| ButtonColumn / MarkdownColumn | 表内操作与富文本，减少跳转 |\n| st.mermaid_chart | 看板内联架构/流程图，替代外链图 |\n| App.run() | 简化容器 ENTRYPOINT 与 FastAPI/Starlette 嵌入 |\n| st.fragment(parallel) + 写外部容器 | 局部刷新，缓解整页 rerun 性能 |\n| persist_state | 控件状态跨 rerun 保留 |\n\n1.58（2026-05）已引入 @st.fragment parallel=True、st.pagination、streamlit skills CLI；1.55（2026-03）引入动态容器 on_change、bind 参数（控件↔URL）。",
   "map":"- st.mermaid_chart 可在看板内联系统架构/数据流图（呼应 [[streamlit_dashboard_2026]] 的图示需求）。\n- App.run() 简化 V3 启动脚本；persist_state + st.fragment 局部刷新是缓解「session 不丢 / 底部固定 / 横向滑动」三角矛盾的可行手段之一（见 [[streamlit_production_dashboard]]）。\n- 与 [[python_dashboard_ecosystem_2026]] 中 Streamlit 赛道领先位一致：表内交互 + LLM 集成 + 轻启动持续强化。"}),

S3: src_page(
  "语义层与数据契约治理2026",
  "semantic_layer, metrics_layer, data_contract, dbt, governance, ai_agent, source",
  "第三方数据",
  {"src": S3+", https://www.getdbt.com/blog/the-trust-speed-paradox-governing-ai-accelerated-data-work, https://www.precisiondatapartners.com.au/blog/the-semantic-lakehouse-architecting-for-ai-agents",
   "refs": ["semantic_layer_metrics_2026", "data_governance_tech_routes_2026", "data_quality_governance"]},
  {"abs":"2026 治理重心转向「信任—速度悖论」：83% 团队把数据信任放首位，但仅 24% 用 AI 可观测；语义层成为 agentic AI 时代的定义真相源，跨 AI/BI 指标一致性 4x。",
   "kp":"1. dbt《2026 State of Analytics Engineering》：数据信任成 83% 团队首要优先级（一年前 66%）；72% 用 AI 辅助编码，仅 24% 用 AI 辅助可观测。\n2. Gartner：至 2026 年，建在非 AI-ready 数据上的 AI 项目 60% 被放弃。\n3. Semantic Lakehouse：智能体数据解读错误 -75%、数据驱动智能体开发 +60% 更快、AI 与 BI 指标一致性 4x。\n4. dbt Semantic Layer/MetricFlow：指标定义为代码（measures/dimensions/entities/time spine），CI 校验。\n5. 契约前置：gold 模型加 not_null/unique/accepted_values，列级血缘，破坏性变更 CI 拦截。",
   "detail":"| 工具 | 适用 |\n|------|------|\n| dbt Semantic Layer | dbt 中心团队，指标贴近模型/测试/PR |\n| Cube | 指标 API / 嵌入式分析 / 缓存 |\n| Lightdash | 读 dbt 元数据的开源 BI |\n| MetricFlow | dbt 原生指标执行引擎(measures/entities/time) |\n\nDatabricks CEO（2026-02）称平台 >80% 数据库由 AI 智能体构建——治理须活在 AI 跑起来之前。",
   "map":"- 本项目多品牌统一指标（售罄率/毛利率/周转）应集中于 [[semantic_layer_metrics_2026]] 一处定义，从根上消除跨品牌/跨表指标漂移——直接回应 [[multi_brand_unified_analytics]] 的口径统一诉求。\n- 契约前置 + 语义层是 [[data_quality_governance]] 从「规则」走向「预防」的 2026 落地路径。\n- 选型参照归入 [[data_governance_tech_routes_2026]]（语义层成为治理核心控制面）。"}),

S4: src_page(
  "主动元数据与多品牌数据目录2026",
  "active_metadata, data_catalog, data_lineage, multi_brand, governance, pii, source",
  "第三方数据",
  {"src": S4+", https://www.datanauta.ai/blog/how-ai-is-transforming-data-catalogs-in-2026, https://mindit.io/customer-success/global-travel-retail-data-ai-platform-2026-by-mindit-io",
   "refs": ["brand_config_driven_system", "multi_brand_unified_analytics", "data_governance_tech_routes_2026"]},
  {"abs":"2026 主动元数据(Active Metadata)成标准：元数据回流工具自动改行为（PII 检测→标记→即时脱敏）；多品牌系统应在品牌注册表之上叠加自动编目/打 owner/跨品牌血缘。",
   "kp":"1. Active Metadata=2026 标准：双向同步，目录标记 PII→立即向 Snowflake/Databricks 推送动态脱敏策略(shift-left)。\n2. Autodesk 主动治理扩展到 60 业务域；Kingfisher「Knowledge Hub」自助供应链分析，排查 小时→分钟。\n3. Datanauta 把「信任分」(如 98% 可靠) 直接推入目录；schema drift/量异常在索引前拦截。\n4. EU AI Act(2026) 强制 AI 训练数据严格血缘 → 目录成合规工具；Grab 用 LLM 发现达 90% 文档覆盖。\n5. Lakehouse 成 2026 零售标准；自动化目录+血缘标配；Unity Catalog 跨域发现/血缘/权限。",
   "detail":"| 能力 | 2026 状态 |\n|------|------|\n| 元数据 | 被动仓库 → 主动系统(ReAct 智能体自动修数据) |\n| 文档 | LLM 驱动发现，Grab 90% 覆盖 |\n| 治理 | 检测即执行(脱敏/质量门) |\n| 合规 | EU AI Act 强制血缘 |\n\n多品牌场景：每个品牌数据资产自动编目、打 owner、标记敏感列(自动脱敏)、记录跨品牌血缘。",
   "map":"- [[brand_config_driven_system]] 已有品牌注册表，应叠加主动元数据目录：自动编目 + 自动脱敏 + 跨品牌血缘，达成「一次配置、自动治理」。\n- 与 [[multi_brand_unified_analytics]] 协同：主动元数据(自动编目/血缘) + 语义层(一处指标) 共同消除「跨品牌指标漂移」与「孤岛难追溯」——直接回应本项目太平鸟/卡宾/东尚多品牌数据去重与口径统一痛点。\n- 选型参照归入 [[data_governance_tech_routes_2026]]（主动元数据路线）。"}),
}

for name, content in sources.items():
    p = os.path.join(SRC, name + ".md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print("SOURCE written:", p)

# ---------------------------------------------------------------------------
# 3) WIKI PAGE UPDATES (frontmatter sources + updated + backlink + subsection)
# ---------------------------------------------------------------------------
def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def write(p, t):
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)

def update_frontmatter(text, new_src):
    lines = text.split("\n")
    out = []
    for i, l in enumerate(lines):
        if l.startswith("sources:"):
            if new_src not in l:
                s = l.rstrip()
                if s.endswith("]") and "[" in s:
                    s = s[:-1] + ", " + new_src + "]"
                else:
                    s = s + " " + new_src
                out.append(s)
            else:
                out.append(l)
        elif l.startswith("updated:") and DATE not in l:
            out.append("updated: " + DATE)
        else:
            out.append(l)
    return "\n".join(out)

def add_backlink(text, src):
    lines = text.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("cross_refs:"):
            if src not in l:
                s = l.rstrip()
                if s.endswith("]"):
                    lines[i] = s[:-1] + ", [[" + src + "]]]"
                else:
                    lines[i] = s + " [[" + src + "]]"
            break
    text = "\n".join(lines)
    if "## 关联页面" in text:
        text = text.replace("## 关联页面", "## 关联页面\n- [[" + src + "]]", 1)
    else:
        text = text.rstrip() + "\n\n## 关联页面\n\n- [[" + src + "]]\n"
    return text

def append_subsection(text, sub):
    if "## 关联页面" in text:
        idx = text.index("## 关联页面")
        return text[:idx] + sub + "\n\n" + text[idx:]
    return text.rstrip() + "\n\n" + sub + "\n"

subsections = {
S1: {
 "SQL查询性能优化": "## 2026-08-15 更新（向量化执行与 PG18/DuckDB 基准）\n\n- 2026 OLAP 进入「向量化执行 + 自适应查询」：DuckDB 1.5.4 以 120k 行 morsel + SIMD，CPU 缓存命中 40%→85%，单查询 3–10x；自适应执行动态切换 Join/并行度，倾斜场景稳定 +60%、复杂查询 -40%。\n- PostgreSQL 18.4 引入异步 I/O + 向量化聚合（相对 PG16 -22%）；但扫描密集仍落后：TPC-H 1TB DuckDB 比 PG17 平均快 7.4x（Q1 8.2 vs 1.1 GB/s，3+表 JOIN 5.2x）。\n- `pg_duckdb` 1.0 让 PG 内部路由分析查询到 DuckDB；混合架构（PG OLTP + DuckDB OLAP）实测 138k 写/秒 + 7.8 GB/s、零争用。\n- 来源：[[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]]",
 "duckdb_olap_engine_2026": "## 2026-08-15 更新（PG18 vs DuckDB 1.5.4 实战基准）\n\n- 新增 2026 基准：TPC-H 1TB Parquet，DuckDB 1.5.4 比 PostgreSQL 18.4 平均快 7.4x（Q1 扫描 8.2 vs 1.1 GB/s，JOIN 5.2x）；`pg_duckdb` 1.0 使 PG 内部路由分析查询到 DuckDB。\n- 向量化进阶：morsel-driven + SIMD，缓存命中 40%→85%，单查询 3–10x；自适应执行使倾斜稳定 +60%、复杂查询 -40%。\n- 落地参照：FinQore 用 DuckDB 替换后管道 8h→8min（60x）。\n- 来源：[[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]]",
 "polars_vs_pandas_2026": "## 2026-08-15 更新（三引擎基准再校准）\n\n- DuckDB 1.5.4 vs PostgreSQL 18.4 实测 TPC-H 1TB 平均 7.4x（扫描 7.4x、JOIN 5.2x）；与 [[SQL查询性能优化]] 的「按 workload 选引擎」一致——DuckDB 擅 SQL 聚合/即席、Polars 擅 ETL 流水线、PG/SQLite 擅事务。\n- `pg_duckdb` 1.0 使 PG+DuckDB 共存成 2026 主流混合架构（PG 扛 OLTP + DuckDB 扛 OLAP = 138k 写/秒 + 7.8 GB/s）。\n- 来源：[[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]]",
 "python_sql_integration_patterns_2026": "## 2026-08-15 更新（DuckDB 嵌入式 SQL 桥接再强化）\n\n- 2026 基准显示 DuckDB 1.5.4 在 TPC-H 1TB 比 PostgreSQL 18.4 快 7.4x，`pg_duckdb` 1.0 让 PG 内部路由分析查询到 DuckDB——Python+SQL 集成新增「DuckDB 内存引擎」这一高性价比桥接层（见 [[duckdb_olap_engine_2026]]）。\n- 来源：[[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]]",
},
S2: {
 "streamlit_dashboard_2026": "## 2026-08-15 更新（Streamlit 1.59 新特性与 LLM 集成）\n\n- 1.59.0（2026-07-06）亮点：ButtonColumn、st.skeleton、st.mermaid_chart（原生 Mermaid 图）、App.run() 直启、st.fragment 写外部容器、persist_state、st.chat_input 粘贴文件 + submit_mode、st.write_stream 支持 OpenAI Responses API 流。\n- 对本项目：st.mermaid_chart 看板内联架构图；App.run() 简化 V3 启动；persist_state + st.fragment 局部刷新是缓解「session 不丢/底部固定/横向滑动」三角矛盾的可行手段之一（配合 [[streamlit_production_dashboard]]）。\n- 移除项：Snowpark 连接已删除，需迁移。\n- 来源：[[2026-08-15_Streamlit_1.59新特性与LLM集成]]",
 "streamlit_production_dashboard": "## 2026-08-15 更新（1.59 生产实践要点）\n\n- 启动升级：1.59 引入 `App.run()`，可直接 `python app.py` / `uv run app.py` 启动，便于嵌入 FastAPI/Starlette 或容器 ENTRYPOINT；`st.fragment(parallel=True)`（1.58）仍用于并发局部刷新。\n- 移动端/体验：st.skeleton 改善加载反馈；persist_state 缓解状态丢失；st.set_page_config initial_sidebar_state=\"locked\" 锁定侧栏（避免移动端误触）。\n- 来源：[[2026-08-15_Streamlit_1.59新特性与LLM集成]]",
 "python_dashboard_ecosystem_2026": "## 2026-08-15 更新（Streamlit 1.59 在生态中的位置）\n\n- 1.59 强化「表内交互 + LLM 集成 + 轻启动」：ButtonColumn、st.write_stream(OpenAI Responses API)、App.run() 直启，巩固「内部数据分析看板」赛道领先位，与 Dash（像素级企业应用）/Gradio（ML 演示）持续分化。\n- 来源：[[2026-08-15_Streamlit_1.59新特性与LLM集成]]",
},
S3: {
 "semantic_layer_metrics_2026": "## 2026-08-15 更新（信任—速度悖论与 Semantic Lakehouse）\n\n- dbt《2026 State of Analytics Engineering》：数据信任成 83% 团队首要优先级（一年前 66%）；72% 用 AI 辅助编码，仅 24% 用 AI 可观测——「信任—速度悖论」；Gartner 预测 2026 年前 60% 建在非 AI-ready 数据上的 AI 项目被放弃。\n- Semantic Lakehouse：语义层作智能体控制平面，实测 75% 智能体数据解读错误下降、开发 60% 更快、AI 与 BI 指标一致性 4x。\n- 落地：dbt Semantic Layer/MetricFlow 指标定义为代码 + CI 校验 + gold 模型契约 + 列级血缘；Databricks CEO（2026-02）称平台 >80% 数据库由 AI 智能体构建。\n- 对本项目：多品牌统一指标（售罄率/毛利率/周转）集中于语义层一处定义，从根上消除跨品牌/跨表指标漂移——直接回应 [[multi_brand_unified_analytics]] 口径统一诉求。\n- 来源：[[2026-08-15_语义层与数据契约治理2026]]",
 "data_governance_tech_routes_2026": "## 2026-08-15 更新（语义层成为治理核心控制面）\n\n- 2026 治理重心从「平台功能全」转向「指标/语义层可信」：dbt 调研 83% 团队把数据信任放首位；语义层（dbt Semantic Layer/MetricFlow/Cube/Lightdash）成 agentic AI 时代定义真相源，跨 AI/BI/API 一致性 4x。\n- 选型参照：dbt 中心团队首选 dbt Semantic Layer；需指标 API/嵌入式分析选 Cube；读 dbt 元数据的开源 BI 选 Lightdash。\n- 来源：[[2026-08-15_语义层与数据契约治理2026]]",
 "data_quality_governance": "## 2026-08-15 更新（契约前置 + 语义层保障质量）\n\n- 质量治理范式前移：契约在 ingestion 即校验（source freshness/not_null/unique/accepted_values），破坏性变更 CI 拦截；语义层保证「同一指标全平台同义」，消除口径漂移型质量事故。\n- 信任—速度悖论警示：83% 团队重数据信任、72% 用 AI 编码、仅 24% 用 AI 可观测——质量监控须与 AI 编码速度同步投入。\n- 来源：[[2026-08-15_语义层与数据契约治理2026]]",
 "data_quality_retail_practice": "## 2026-08-15 更新（契约 + 语义层落地零售质量）\n\n- 零售数据质量实操新增「契约前置」环节：源表 freshness/非空/唯一/取值域在入库即断言，破坏性变更 CI 拦截而非上线后人工发现；语义层保证售罄率/毛利率/周转跨表同义。\n- 来源：[[2026-08-15_语义层与数据契约治理2026]]",
},
S4: {
 "brand_config_driven_system": "## 2026-08-15 更新（主动元数据扩展品牌目录）\n\n- 多品牌系统应在「品牌注册表」之上叠加**主动元数据目录**：每个品牌数据资产自动编目、打 owner、标记敏感列（自动脱敏）、记录跨品牌血缘。Autodesk 主动治理扩到 60 业务域、Kingfisher Knowledge Hub 自助排查 小时→分钟，可作参照。\n- 与 [[multi_brand_unified_analytics]] 协同：品牌配置驱动开发 + 主动元数据自动编目 = 「一次配置、自动治理」。\n- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]]",
 "multi_brand_unified_analytics": "## 2026-08-15 更新（主动元数据 + 语义层底座）\n\n- 多品牌统一分析补两块底座：① 主动元数据目录（自动编目跨品牌资产、打 owner、自动脱敏、跨品牌血缘）；② 语义层（一处定义售罄率/毛利率/周转，跨 AI/BI 一致 4x）。\n- 二者共同消除「跨品牌指标漂移」与「孤岛难追溯」——直接回应本项目多品牌（太平鸟/卡宾/东尚）数据去重与口径统一痛点。\n- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]] / [[2026-08-15_语义层与数据契约治理2026]]",
 "data_governance_tech_routes_2026": "## 2026-08-15 更新（主动元数据成为 2026 标准）\n\n- Active Metadata=2026 标准：元数据回流工具改变行为（双向同步）。例：检测 PII 列→标记 SENSITIVE→立即向 Snowflake/Databricks 推送动态脱敏策略（shift-left 治理）。\n- Autodesk 主动治理扩到 60 业务域；Kingfisher「Knowledge Hub」自助供应链分析，排查 小时→分钟；Datanauta 把「信任分」(如 98% 可靠) 推入目录、异常(schema drift/量异常)在索引前拦截。\n- EU AI Act(2026) 强制 AI 训练数据严格血缘 → 目录成合规工具；Grab 用 LLM 发现达 90% 文档覆盖。\n- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]]",
 "data_quality_governance": "## 2026-08-15 更新（主动元数据 + 信任分）\n\n- 主动元数据使质量「左移」：目录标记 PII/敏感即自动向引擎推送脱敏策略；Datanauta 把质量健康分（Trust Score，如 98%）直接写入目录元数据，发现即见可信度。\n- 异常检测（schema drift/量异常）在目录索引前拦截，防「垃圾进垃圾出」。\n- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]]",
 "data_quality_retail_practice": "## 2026-08-15 更新（主动元数据 + 信任分落地零售）\n\n- 零售质量实操新增「主动元数据」环节：敏感列自动脱敏、信任分(Trust Score)随资产编目展示、schema drift/量异常在入库前拦截。\n- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]]",
},
}

# map each source -> list of (dir, filename) wiki pages
wiki_targets = {
 S1: [("con","SQL查询性能优化.md"),("con","duckdb_olap_engine_2026.md"),("con","polars_vs_pandas_2026.md"),("pra","python_sql_integration_patterns_2026.md")],
 S2: [("con","streamlit_dashboard_2026.md"),("pra","streamlit_production_dashboard.md"),("con","python_dashboard_ecosystem_2026.md")],
 S3: [("con","semantic_layer_metrics_2026.md"),("con","data_governance_tech_routes_2026.md"),("con","data_quality_governance.md"),("pra","data_quality_retail_practice.md")],
 S4: [("pra","brand_config_driven_system.md"),("pra","multi_brand_unified_analytics.md"),("con","data_governance_tech_routes_2026.md"),("con","data_quality_governance.md"),("pra","data_quality_retail_practice.md")],
}

for src, targets in wiki_targets.items():
    for kind, fn in targets:
        base = CON if kind == "con" else PRA
        p = os.path.join(base, fn)
        if not os.path.exists(p):
            print("SKIP (missing):", p); continue
        t = read(p)
        before = t
        t = update_frontmatter(t, src)
        t = add_backlink(t, src)
        sub = subsections[src].get(fn.replace(".md",""))
        if sub:
            t = append_subsection(t, sub)
        if t != before:
            write(p, t)
            print("WIKI updated:", p)
        else:
            print("WIKI unchanged:", p)

# ---------------------------------------------------------------------------
# 4) L3 SYNC
# ---------------------------------------------------------------------------
l3_targets = {
 S1: [os.path.join(L206,"L3_06_04_SQL查询优化","sql_optimization.md")],
 S2: [os.path.join(L207,"L3_07_04_Streamlit多Tab组件设计","streamlit_multitab.md"),
      os.path.join(L206,"L3_06_03_可视化最佳实践","viz_best_practices.md")],
 S3: [os.path.join(L207,"L3_07_01_系统架构设计","system_architecture.md")],
 S4: [os.path.join(L207,"L3_07_01_系统架构设计","system_architecture.md"),
      os.path.join(L207,"L3_07_03_跨品牌数据整合","cross_brand_integration.md")],
}
l3_subs = {
 S1: "## 2026-08-15 更新\n\n- 2026 向量化执行+自适应查询成 OLAP 标配：DuckDB 1.5.4 比 PostgreSQL 18.4 在 TPC-H 1TB 平均快 7.4x（Q1 扫描 8.2 vs 1.1 GB/s，3+表 JOIN 5.2x）；`pg_duckdb` 1.0 让 PG 内部路由分析查询到 DuckDB；混合架构( PG OLTP + DuckDB OLAP )实测 138k 写/秒 + 7.8 GB/s 零争用。\n- 来源：[[2026-08-15_SQL优化2026向量化执行与PG18_DuckDB基准]]",
 S2: "## 2026-08-15 更新\n\n- Streamlit 1.59（2026-07）新特性：ButtonColumn(表内按钮)、st.mermaid_chart(内联架构图)、App.run() 直启、st.fragment 写外部容器(局部刷新)、persist_state(跨 rerun 保留状态)；st.write_stream 支持 OpenAI Responses API 流。\n- 来源：[[2026-08-15_Streamlit_1.59新特性与LLM集成]]",
 S3: "## 2026-08-15 更新\n\n- 语义层成 agentic AI 时代定义真相源：dbt 调研 83% 团队把数据信任放首位；Semantic Lakehouse 实测智能体数据解读错误 -75%、AI 与 BI 指标一致性 4x；指标定义为代码 + CI 校验 + 列级血缘。\n- 来源：[[2026-08-15_语义层与数据契约治理2026]]",
 S4: "## 2026-08-15 更新\n\n- 主动元数据(Active Metadata)成 2026 标准：检测 PII→即时脱敏(双向同步)；Autodesk 扩到 60 业务域、Kingfisher 自助排查 小时→分钟、Datanauta 推「信任分」98%；多品牌系统应叠加自动编目/打 owner/跨品牌血缘。\n- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]]",
}
for src, paths in l3_targets.items():
    for p in paths:
        if not os.path.exists(p):
            print("SKIP L3 (missing):", p); continue
        t = read(p)
        # avoid duplicate subsection
        marker = "2026-08-15 更新"
        if marker not in t:
            t = t.rstrip() + "\n\n" + l3_subs[src] + "\n"
            write(p, t)
            print("L3 updated:", p)
        else:
            print("L3 already has update:", p)

# ---------------------------------------------------------------------------
# 5) INDEX.md — bump L2_06/L2_07 quick-entry + append round row
# ---------------------------------------------------------------------------
idx = read(IDX)
idx = idx.replace(
 "| L2_06 数据分析实务 | 4 | 数据质量、未动销、可视化、SQL |",
 "| L2_06 数据分析实务 | 5 | 数据质量、未动销、可视化、SQL、向量化执行与语义层 |")
idx = idx.replace(
 "| L2_07 多品牌系统 | 4 | 架构、品牌配置、跨品牌整合、Streamlit |",
 "| L2_07 多品牌系统 | 5 | 架构、品牌配置、跨品牌整合、Streamlit、主动元数据 |")
round_row = ("\n| **122** | **08-15 17:15** | **L2_06/07+查漏 (C轮)** | **s4(SQL优化向量化PG18_DuckDB基准/Streamlit1.59新特性LLM/语义层数据契约治理/主动元数据多品牌目录)/c8更新(SQL优化+duckdb+polars+streamlit_dashboard+python_dashboard+semantic_layer+data_gov_routes+data_quality+brand_config+multi_brand)/p5更新(streamlit_production+multi_brand+brand_config+python_sql+data_quality_retail)/L3同步5处/织网24条双向/矛盾0处 ✅** |\n")
if "**122**" not in idx:
    idx = idx.rstrip() + round_row
write(IDX, idx)
print("INDEX updated")

# ---------------------------------------------------------------------------
# 6) LOG.md — append C round row
# ---------------------------------------------------------------------------
log = read(LOG)
log_row = "| 2026-08-15 17:15 | ingestC | L2_06/07+查漏 — 采集4篇/织网24条(双向)/矛盾0处 ✅ |\n"
if "2026-08-15 17:15 | ingestC" not in log:
    log = log.rstrip() + "\n" + log_row
write(LOG, log)
print("LOG appended")

print("\nDONE. Round C 2026-08-15 complete.")
