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

- **每次 A轮（Round-A）自动化任务必须覆盖全部 `focus_brands`（当前 36 个）**，不得以「已完整 / OK」为由整体跳过任何焦点品牌。
- **「只跑少源」仅为用户单次显式收窄的临时范围，不是默认行为**；若需收窄，必须由用户在当次明确指定。
- 预检缺口清单仍可做优先级排序，但**每轮每个焦点品牌都必须被检索 / 核验 / 更新**，或显式记录「无新增」后跳过造页（不得静默跳过）。
- 已由自动化 `automation-1780752607913` 的 prompt 固化此规则（顶部"硬性覆盖规则"段）。

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
