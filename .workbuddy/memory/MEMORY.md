# Fashion Doctor 知识库 - 项目记忆

## Git 仓库信息

- **GitHub 仓库**: https://github.com/WuFG-Fashion/fashion-doctor
- **SSH 地址**: git@github.com:WuFG-Fashion/fashion-doctor.git
- **本地路径**: D:\Fashion Doctor\fashion-doctor
- **分支**: main
- **创建日期**: 2026-06-06

## 项目简介

Fashion Doctor 知识库项目，包含 wiki 双轨架构和分类体系。

## 信息搜集优先级（采集焦点）⚠️ 长期约定

用户明确：后期信息搜集以**以下品牌为主**（2026-08-14 确认）。卡宾/太平鸟为双核，品牌墙图全品牌为运营代理集合（MODING 是渠道方非品牌，不单独追踪），艾诺丝/迪卡轩为重点补充女装。

- **双核**：卡宾（cabbeen，仅次于太平鸟的核心）、太平鸟（peacebird）
- **品牌墙图集合**（用户所发图片，原 MODING 运营代理操盘的品牌，非 MODING 本体）：trussardi, mr_mrs, marcelo_burlon, karl_lagerfeld, dkny, tommy_hilfiger, lacoste, diesel, g_star_raw, levis, dickies, salomon, speedo, hoka_one_one, ellesse, mlb, nerdy, crocs, mlb_kids, adlv, chuu, no_one_else, thisisizi8, awoken_space, awoken_time, koyo, the_mr_young, two_am, king_baby, nautica, etudes
- **重点补充女装**：艾诺丝（ariose_years，ARIOSE YEARS，杭州爱唯）、迪卡轩（dekashell，DEKASHELL，杭州轻淑）

机器可读清单见 `knowledge_base/kb_benchmarks.json` 的 `focus_brands` 字段（当前 36 个，含上述双核+品牌墙+艾诺丝+迪卡轩；实际数量以 json 为准）。新增实体默认带 `sources: [用户指定-重点女装品牌]` 或 `品牌墙图_2026-08-14`。

## A轮自动化覆盖规则 ⚠️ 长期约定（2026-08-15 确立）

- **每次 A轮（Round-A）自动化必须覆盖全部 `focus_brands`（36 个）**——但为规避"单次运行上下文溢出导致后段品牌质量滑坡"，自 2026-08-15 起将单轮拆分为 **A1/A2/A3 三轮分批**（见下），全天仍覆盖全部 36，每轮上下文可控。
- **「只跑少源」仅为用户单次显式收窄的临时范围，不是默认行为**；若需收窄，必须由用户在当次明确指定。
- 预检缺口清单可做优先级排序，但**每轮每个本组品牌都必须被检索 / 核验 / 更新**，或显式记录「无新增」后跳过造页（不得静默跳过）。

### A1/A2/A3 三分架构（06:40 / 07:00 / 07:20）
- 36 品牌按 `kb_benchmarks.json` 顺序**均分 3 组各 12 个、互不重叠**，**分组仅用于把 36 拆成 3 批以控制单次运行上下文**。
- ⚠️ **采集方向（用户 2026-08-15 重申）**：以**品牌主体**为中心，对每组每个品牌做**全维度综合采集**（财务/门店渠道/联名营销/竞品/行业趋势 一律覆盖），**不得把品牌钉死在单一事件镜头上**（早期曾误按"财务/门店/联名"分镜头，导致单品牌信息残缺，已纠正）。
  - **A1（06:40）** 分组=[adlv, ariose_years, awoken_space, awoken_time, cabbeen, chuu, crocs, dekashell, dickies, diesel, dkny, ellesse]
  - **A2（07:00）** 分组=[etudes, g_star_raw, hoka_one_one, humble_humble_r, karl_lagerfeld, king_baby, koyo, lacoste, levis, marcelo_burlon, mlb, mlb_kids]
  - **A3（07:20）** 分组=[mr_mrs, nautica, nerdy, no_one_else, peacebird, salomon, speedo, the_mr_young, thisisizi8, tommy_hilfiger, trussardi, two_am]
- 各轮完整指令存于仓库根 `_automation_A1.md` / `_automation_A2.md` / `_automation_A3.md`；对应自动化：`automation-1786773584037`(A1) / `automation-1786773585569`(A2) / `automation-1786773587084`(A3)，均 ACTIVE。
- 原单轮 `automation-1780752607913` 已 **PAUSED**（保留为历史底本，避免与 A1 在 06:40 重复触发）。

### 数据可信度分级（置信度）标准（2026-08-15 新增）
- **背景**：私企/小众女装（艾诺丝/迪卡轩/CHUU 中国等）无审计披露，数据多为品牌自宣/媒体估算；Run4 部分数字带"约/估"。RAG 检索时模型无法区分"财报数"与"自宣数" → 必须分级。
- **落地**：CLAUDE.md 2.1 frontmatter 新增 `confidence` 字段（取值：财报 / 官方公告 / 第三方数据 / 品牌自宣 / 媒体估算）；新增 2.4 章节定义分级与使用规则；5.1 必含清单纳入 `confidence`。
- **强制**：三份 A轮规范 `_automation_A1/A2/A3.md` 追加「第九步：置信度标注与上下文护栏」——source 页必填 `confidence` frontmatter + 页内 `> **置信度**` 声明；entity 页关键数字内联标注（"约/估"必标 媒体估算）；矛盾检测优先比对同等级。
- **护栏同条固化**：第九步一并规定单轮 12 品牌全维度的上下文护栏——每品牌 WebSearch≤3 次、优先摘要、第 6 品牌后中途 git commit（分两段提交）、尾部降级允许仅探针不得编造，从根上防溢出/降级。
- 已回填空量 Run4 的 11 个 `2026-08-15_R4_*` 源页 `confidence`（上市品牌=财报；Trussardi/CHUU=媒体估算；2AM/艾诺丝/迪卡轩=品牌自宣）。

### B/C轮品牌对齐改造（2026-08-15 确立，23:49 修正为方法论为主）
- **背景**：A轮已改为"以品牌为主体、全维度综合采集"，但 B轮（会员VIP/导购/商品企划）和 C轮（数据分析/多品牌系统）的 prompt 仍是纯主题搜索，完全不提任何品牌名 → 运营知识与品牌情报割裂。
- **B轮改法（方法论为主·品牌为辅）**：每个 L2 域通用方法论搜索 2-3 次为主体，品牌上下文搜索 1-2 次为佐证（双核轮换 + 每轮轮换 2-3 个品牌），防止方法论维度坍缩为实体维度子集。source 页必标 `brand_specific` 区分通用方法论 vs 品牌特有。
- **C轮改法（品牌感知）**：技术搜索（SQL/Streamlit/Polars/ETL）保持通用，但"多品牌系统"须引用 focus_brands 清单作为被分析对象，"查漏"须检查品牌级数据分析覆盖缺口。补齐 confidence/护栏/结论信息链/git pull/健康快照/分段提交。
- 规范文件：`_automation_B.md` / `_automation_C.md`；对应自动化 `automation-1780752607954`(B) / `automation-1780752608015`(C)，均 ACTIVE。
- **A vs B vs C vs S 品牌关系定位**：A轮=品牌情报（品牌在做什么）；B轮=品牌运营方法论（怎么运营，可迁移）；C轮=品牌数据基建（用什么工具分析）；S轮=跨品牌合成（品牌放在一起说明什么）。A/B/C 是采集导向，S 是合成导向。

### S轮（合成轮）跨品牌模式识别（2026-08-15 确立）
- **背景**：A/B/C 三轮都是"采集导向"（加新节点），没有"合成导向"（从已有节点中发现跨品牌模式）。第一性原理：100 条品牌情报不如 1 条跨品牌模式有价值。
- **定位**：不采集新数据（不调用 WebSearch/WebFetch），只读已有 wiki 页面，做跨品牌模式识别。
- **合成维度**：营收规模分层 / 增长模式分类 / 门店策略对比 / 毛利率分层 / 渠道结构对比 / 国际化程度 / 品类定位 / 运营策略对比 / 数据基建适配 / 风险信号。
- **输出**：`wiki/comparisons/` 新增/更新跨品牌对比页 + 更新 `wiki/concepts/服装行业竞争格局.md` + 回填旧 source 的 `superseded_by`。
- 规范文件：`_automation_S.md`；对应自动化 `automation-1786809189350`，ACTIVE，每周日 08:00。
- **上下文护栏**：36 品牌实体页分 3 批读取（每批 12 个），每批读完即提取要点笔记。

### 数据生命周期字段（2026-08-15 新增）
- **brand_specific**（source 页必填）：`true`=品牌特有数据（双链到品牌实体页），`false`=行业通用方法论（双链到 concept，不链品牌）。防止"伪连接"——通用方法论错误链到品牌实体，形式上链了但不支持推理。
- **superseded_by**（source 页可选）：当新 source 包含同品牌同指标的更新数据时，在旧 source frontmatter 回填 `superseded_by: "[[新source]]"`。旧 source 不删除但 RAG 检索优先取新页。
- 已写入 CLAUDE.md 2.1 frontmatter schema + 2.5 章节 + 5.1 必含清单；已同步到 A1/A2/A3/B/C 五份采集规范。

## 品牌归属重要约束

- 卡宾（cabbeen）是**独立上市公司（卡宾服饰 HK 02030）**，与 MODING GROUP 是并列关系，NOT 上下级——不要把卡宾挂到任何"集团旗下"。
- MODING 只是品牌运营代理公司，不是关注品牌，知识库中**不单独建 MODING 实体**。
- 太平鸟与卡宾是**并列双核**，结构上是两份独立实体页 + 对照表，不得合并。

## RAG 就绪规划 ⚠️ 长期约定（2026-08-14 确立）

**目标**：将来 Obsidian 用本地部署大模型实现外网访问的 RAG。当下准备工作已落地（commit 33a2776）。

**RAG 四大支柱**（知识库页面必须满足）：
1. **aliases 别名必填**：实体/概念页 frontmatter 必须有中/英/股票代码/别称——这是本地 LLM 检索命中率的决定性字段。已写入 CLAUDE.md 2.1 schema + 5.1 必含清单，采集自动化须强制带别名。
2. **结论块**：每页 `## 结论` 是合成判断（非数据复述）。
3. **信息链**：每页 `## 信息链`（上游来源→本页→下游应用双链），支撑多跳推理。
4. **零孤岛**：每页至少一条入链。

**当前就绪度**：entities 61 + concepts 60 + comparisons 5 已 100% aliases/结论/信息链；内容层别名 135/147=91%；全库 0 孤岛；sources 603 全有出链。

**git 与 Obsidian 协调约定**：
- `.obsidian/` 的 volatile 状态（workspace.json / graph.json / plugins/*/data.json / cache）已移出版本控制（.gitignore + git rm --cached）；稳定设置（app/appearance/community-plugins/core-plugins.json + 插件代码）保留版本化。
- `.claudian/` 本地 AI 工具状态不入库。
- 行尾已是 index=LF + autocrlf=true，勿加 .gitattributes（避免全库重 normalize）。

**可复用技能**：`obsidian-kb-rag-readiness`（user-level），含审计→注入别名→补信息链→修孤岛→git协调 全流程。
