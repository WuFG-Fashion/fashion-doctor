# A3轮 自动化执行记忆（automation-1786773587084）

> 固定分组 12 品牌：mr_mrs / nautica / nerdy / no_one_else / peacebird / salomon / speedo / the_mr_young / thisisizi8 / tommy_hilfiger / trussardi / two_am
> 触发：每日 07:20（rrule FREQ=DAILY;BYHOUR=7;BYMINUTE=20）

## 最近执行（2026-08-17 09:23）
- **状态**：✅ 成功，已分两段 commit + push（bfd1a10 前半程品牌1-6 / 1d29235 后半程品牌7-12 + index/backlink）。
- **产出**：12 raw 剪藏 + 12 wiki source（全维度综合采集，非单一镜头）+ 12 实体页「近期动态刷新」+ index.md 末节 + 服装行业竞争格局回链。
- **采集量**：WebSearch 约 14 次（tommy×2、speedo×2，其余各1），均在每品牌≤3 次护栏内。
- **织网**：165 条 `[[`（含 12 源自引）→ 153 跨页双链，指向 15 目标页，孤岛 0。
- **矛盾**：1 处真冲突（Tommy Hilfiger Q1 两口径：PVH 官方 $10.77亿+3% vs 媒体 $8.42亿+6%，截止日不同不可直比，标 ⚠️，优先取官方值）；1 处基准核对（Salomon 中国 302 店与既有一致，标 ℹ️）。
- **置信度**：财报 4 / 品牌自宣 6 / 媒体估算 1 / 第三方数据 1。
- **第零步缺口**：本轮前 tommy/speedo/nautica/mr_mrs/nerdy/no_one_else/the_mr_young/thisisizi8 仅 1 篇（少源⚠️），trussardi/salomon 仅 2 篇（少源临界）；本轮各 +1 源后脱离少源。
- **遗留**：工作树 `practices/data_library_selection_guide_2026.md` 有未提交修改，非本论范围，未纳入 A3 提交（待单独处理）。

## 固定执行步骤（第零~八步）
0. 预检本组缺口清单（仅 12 品牌，不扩散 A1/A2）
1. 加载上下文（CLAUDE.md / index.md / log.md / kb_benchmarks.json）
2. 每品牌联网检索全维度（≤3 次/品牌）
3. 5 关质量审核（具体/可信/服装相关/时效2025-2026/可操作）
4. 写入知识库（raw→sources→entities），每页必含「结论」+「信息链」，每源必含双链，frontmatter 含 confidence/brand_specific/superseded_by
5. 自动织网（kb-link）
6. 矛盾检测（与 kb_benchmarks/comparisons 交叉比对，严格区分 ⚠️数据矛盾 vs ℹ️基准核对）
7. 9.3 分段提交（品牌1-6 commit / 品牌7-12 commit + push）
8. 写 log.md 追加行 + 生成 `_health/YYYY-MM-DD_daily_health.md`

## 注意事项
- 后半程提交曾因 `服装行业竞争格局.md` 路径误写（`wiki/entities/` 应为 `wiki/concepts/`）失败，已定位修正后提交成功——该页在 concepts 不在 entities。
- index.md 过大，禁止整读；用 Glob/Grep 扫描实体页与源文件规避 token 超限。
- git 精确 add，禁止 `git add knowledge_base/` 整目录（避免误提交 .smart-env/ 等非 KB 文件）。
- 硬性规则：必须覆盖全部 12 品牌全维度，不得只跑少源、不得以单一镜头替代、不得越界采集 A1/A2 品牌。
