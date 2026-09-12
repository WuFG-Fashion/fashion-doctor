# Fashion Doctor 知识库 - 项目记忆

## 仓库
- GitHub: WuFG-Fashion/fashion-doctor（SSH git@github.com:WuFG-Fashion/fashion-doctor.git），本地 D:\Fashion Doctor\fashion-doctor，分支 main，git 身份 WorkBuddy <wb@local>。

## frontmatter 字段口径 ⚠️ 长期约定（2026-09-12）
- 标签由 AI 推断填写；确定不了→一律填「未知」，老板自行修正。
- layer：entities/sources=T2 其余=T1；scope：brand/public/company/personal；volatility：方法论=evergreen、门店/组织=slow、季度财报/行情=fast、事件/联名=perishable；as_of=文件名日期优先、未知=未知；expires_at：fast=as_of+90天、slow=+180天、evergreen 不填；confidence：财报/官方公告/第三方数据/品牌自宣/媒体估算、分不清=未知。
- 详规 `specs/存量补齐批次方案_2026-09-12.md` §2.1。

## 采集焦点（长期约定）
- 双核：卡宾 cabbeen（独立上市 HK02030，仅次于太平鸟）、太平鸟 peacebird——并列不合并。墙图集合 30 品牌（trussardi/mr_mrs/marcelo_burlon/karl_lagerfeld/dkny/tommy_hilfiger/lacoste/diesel/g_star_raw/levis/dickies/salomon/speedo/hoka_one_one/ellesse/mlb/nerdy/crocs/mlb_kids/adlv/chuu/no_one_else/thisisizi8/awoken_space/awoken_time/the_mr_young/two_am/king_baby/nautica/etudes，原 MODING 运营代理集合，MODING 本体不建实体）+ 艾诺丝 ariose_years + 迪卡轩 dekashell。机器可读清单 `knowledge_base/kb_benchmarks.json` focus_brands（koyo 已移除）。
- 品牌归属：卡宾与 MODING 并列非上下级，勿挂「集团旗下」；太平鸟与卡宾双核独立实体页。

## 自动化轮次架构（2026-08-15）
- A1/A2/A3（06:40/07:00/07:20，automation-…752372/…752688/…753030 ACTIVE）：以品牌为主体全维度采集，35 品牌按 kb_benchmarks 顺序均分 3 组防上下文溢出；不得钉死单一事件镜头。每轮每品牌必被检索/核验/更新或显式记录「无新增」。原单轮 automation-…752126 保持 PAUSED（prompt 为重建版）。指令：仓库根 `_automation_A1/A2/A3.md`。
- B 轮（…753361）：方法论为主·品牌为辅，source 页必标 brand_specific。C 轮（…753693）：技术搜索通用+品牌感知（多品牌系统引用 focus_brands）。S 轮（…754325，周日 08:00）：跨品牌合成，不采集新数据，输出 comparisons/ + 回填 superseded_by。A=品牌情报 / B=运营方法论 / C=数据基建 / S=合成。
- 置信度分级（2026-08-15）：source 页必填 confidence + 页内 `> **置信度**` 声明；entity 关键数字内联标注；矛盾比对同等级优先。A 轮护栏：每品牌 WebSearch≤3、第 6 品牌后中途分段 commit、尾部降级只探针不编造。
- 生命周期字段：brand_specific（source 必填）、superseded_by（新数据出时回填旧页，旧页不删）。已写入 CLAUDE.md 2.1/2.5/5.1 及五份采集规范。

## 三区块补齐战役（批次 1-11 收官 2026-09-13）
- 30_wiki 实审 1405 页三区块 100%、结论引导语=0（终审 PASS）。`.kbtmp/_b11_audit.py` 幂等可复跑，作常态验收工具。
- **验收铁律**：批处理验收必须「存在性+内容标记黑名单」双检，禁单存在性判定；名单驱动清理必须配全库变体宽扫；标题精确 `## 结论` 禁装饰变体。批次1 漏检根因（`1edf87b` 骨架只铺不写）已归档 `specs/批次11执行记录_2026-09-13.md` §3。
- CLAUDE.md 5.1/5.2 验收铁律已提交（批次 12）。结论区 U+0022 696 页=历史体例，已定性不回改。

## 批次 12（2026-09-13 收官）：矛盾清单回写源页
- 批次 8 §9 的 14 条矛盾全部收口：过时「待核实/须仲裁/未闭环」行 → 「跨页裁定（批次12 · 2026-09-13）」行；TH「净利 11.9 亿」笔误全库勘误为 1.19 亿美元；Marcelo 运营主体两说维持「未裁定 · 两说并列」标注。36 条 entry / 25 文件（7 实体+18 源页），实体页同步收敛消除与裁定自相矛盾的「未裁定」行。
- 裁定要点（后续引用口径）：TH Q1 收入两口径=口径边界未对齐禁跨口径换算；MLB 门店 RAG 主数 1,094（F&F DART）/1,185 对照；卡宾代销 201→202=财报口径、101→370=渠道占比；太平鸟净增长=前瞻指引 H2 需净开 ≥138 家；ARIOSE 主数 1,800+；HOKA 主数 >230（Deckers 财报）、250+ 对照、1000 作废；Crocs 破圈=曝光维度/遇冷=转化维度可并列。
- 详见 `specs/批次12执行记录_2026-09-13.md`（含与交接文档 4 处偏差记录）。

## RAG 就绪（2026-08-14，commit 33a2776）
- 四支柱：aliases 必填（中/英/代码/别称）、结论块（合成判断）、信息链、零孤岛。entities/concepts/comparisons 100% 达标；sources 全有出链。技能 `obsidian-kb-rag-readiness`。
- git 协调：.obsidian volatile 与 .claudian 不入库、稳定设置保留；行尾 index=LF+autocrlf=true，勿加 .gitattributes。

## 知识库 v2 方案（讨论稿已定 · 原 8 问 2026-09-11 拍板，v2.1 六点待批）
- `specs/知识库v2架构方案_讨论稿.md`：按「谁产生+寿命+权限」分区；重要性三维度（Tier×volatility×权限域）；TTL 到期软化不删除；双链废「零孤岛」硬门槛改 R1-R3+`## 前沿`；40_companies 语义层与 dongshang-v3 共用真源（版本指针 current，不钉死 V3）；视图一律脚本生成。
- **原 8 问已于 2026-09-11 全部拍板**（§11 记录）：TTL 分档（易腐 7-30/快变 90/慢变下期披露/常青 180 复核）、自动化永不删除、公司域=dongshang 且品牌墙非公司域、个人域不进 RAG、课件归东尚域（34 篇非 322）、感性言论=只读素材、视图按业务主体慢生成不日维护、先逻辑分层→提示词→最后物理。
- **真正待批 = §13.9 六点（2026-09-12 v2.1 修订新增）**：①保留 T0-T4 ②个人域完全独立索引 ③T4 允许显式注入 ④公司隔离仅 RAG（非文件 ACL）⑤语义层真源=「当前主版本」指针 ⑥物理迁移无限期延后。
- 旧账：MOC+L3 死层、raw 两处合并延后。

## 遗留待办
- ~~批次 12 矛盾清单回写~~ ✅ 2026-09-13 完成（36 条/25 文件，见执行记录）。
- ~~批次 12 范围外同型残留：comparisons/practices 层 6 页同步~~ ✅ 2026-09-13 完成（执行记录 §8；47.4% 归属仍标待核）。
- 编译层 aliases 覆盖审计；v2.1 §13.9 六点拍板（材料已呈，待批复）。
- trussardi 地理口径标注行（交接定性不动）。
