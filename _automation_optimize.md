# optimize 轮规范（知识库优化：lint 五规则 + 织网 + 索引重建 + 基准导出）

> 触发：约每 6 天一次（自动化 d9ed8412-4198-4d36-9225-176d96bcef25）。2026-09-06 首轮落地并沉淀本规范。

## 执行步骤（与自动化 prompt 对应）

1. lint 五规则（CLAUDE.md §3.4）——用 `.kbtmp/opt_lint.py` 全扫（只读，结果存 `.kbtmp/opt_lint_result.json`）。
2. 织网修复（§3.5）：断链修复目标 **断链 0**；孤岛按下方口径**报告 + 只补自然链接**（v2.1 起「孤岛 0」不再是硬目标，见 CLAUDE.md 5.1 R1-R3）。
   - **2b. 连通性筛查（2026-09-12 第 2 轮新增，必做）**：孤岛=0 不等于连通性已够。跑「入链来源数分布（排除 index.md 登记）」+「空 `cross_refs: []` 筛查」，定位真实薄弱页；据此补链（详见「织网口径」）。
3. `python knowledge_base/tools/kb_updater.py` 重建 `90_meta/__index__/master_index.json`（校验 kb_version 3.1 + 1400+ L3）。
4. 受控刷新 `kb_benchmarks.json` 元数据：跑 `python scripts/update_benchmarks_controlled.py`（dry-run 先看）→ 确认拟新增竞品后加 `--apply`；**绝不覆盖阈值键值**，且须补同步 `meta.updated`（脚本只刷顶层 `updated` + `meta.last_scan`）+ 用「剥键比对法」证明阈值零改动（见下）。
5. 统计：页面数 / [[]] 双链数 / 孤岛数。
6. log.md 追加行 + `90_meta/_health/YYYY-MM-DD_daily_health_optimize.md` 快照。
7. 分段 git commit + push（内容修复 → 产物 → log/快照 → 规范；见下）。
8. 写自动化记忆 `.workbuddy/memory/automations/d9ed8412-.../memory.md` + 当日 daily log。

## 口径约定（首轮 2026-09-06 固化，勿随意更改）

- **扫描范围**：wiki/ 语义层 6 目录（entities/concepts/sources/comparisons/practices/playbooks）+ 导航页（index/log/overview）。
- **解析规则**：
  - 链接目标须为**文件名**（非 alias）；容忍 `[[path/../file|label]]`、`#anchor`、`.md` 后缀、表格 `\|` 转义；vault 根相对路径级联剥离（wiki/、raw/、articles/ 等多段）。
  - **同名文件歧义**：语义层目录优先于 raw/_archive（KB 内 10_web/articles 与 KB/10_web/articles 双树并存，raw 副本有大量与 sources 同名文件）。
  - 非 md 目标（`[[kb_benchmarks.json]]`）按全库文件存在判定有效。
- **豁免**：log.md（操作日志正文含 [[]] 格式示例与修复说明）；_archive/L2 legacy/raw（只报告不处理，断链另计）。
- **孤岛定义**：语义层页面无任何"语义层或导航页"入链 → 孤岛；sources 只要求出链 + 尽量被 index.md/实体页登记（历史口径"孤岛 0"= hub 目录入链覆盖 100%，勿机械按 433 个无入链 source 造链）。
- **织网口径（2026-09-12 强化）**：孤岛 0 是**底线不是目标**。真正的薄弱点用两个指标找：
  1. **入链来源数分布**（排除 index.md 登记，5=5+）：1源/2源/3源/4源/5+源。09-12 实测 16/77/166/163/985，且 **0 页仅靠 index.md 登记**。
  2. **空 `cross_refs: []` 筛查**：遗留同步页常留空 cross_refs 且只有 1 条语义入链——这是最真实的补链靶点（09-12 借此定位 6 页、补 21 条自然链接）。
  补链须按「同名实体 > 共用概念 > 同标签 > 同来源」优先级，并在页内加 `## 关联页面` + 一行「织网说明」注明语义依据；**找不到自然目标就不链**。
- **矛盾基线（2026-09-06 对账，09-12 复核未变）**：全库（含 raw 副本）`⚠️ **数据矛盾**` = **57 页 / 66 处**（语义层 54 页 + 10_web 副本 3 页），`ℹ️ **基准核对**` = 129 处（09-12 已升至 156 处，+27 全部来自新页自带的「与 kb_benchmarks 一致 ✓」自洽标注，属健康增长，**应定性为「自洽标注数」而非疑似矛盾数**）。
  - ⚠️ **统计陷阱**：全库 grep 会命中 `90_meta/_health/*` 快照与 `CLAUDE.md` 规则文本里的自引用 → **必须排除 `90_meta/_health/` 与 `CLAUDE.md`**，否则得 71 页/82 处（假数）。
- **数值交叉**：entity↔kb_benchmarks 正则检测（scripts/_kb_contradiction_check.py）命中须人工核验；跨行/跨周期/跨指标（如"电商+121%"被当 revenue_growth）多为伪命中，页内"与 kb_benchmarks 一致 ✓"自洽标注为准。
- **过期规则**：静态源页（2026-06 起的批量快照）= 数据快照，**不适用 90 天新鲜度判罚**（updated 即数据时点）；维护型页面（entity/concept/comparison/practice/playbook）过期才需处理。
  - ⚠️ **过期数会随日期漂移，不是质量退化**：cutoff = today-90 逐日/逐轮前移，会整批把某日期区间的静态源页纳入（09-06 报 54，09-12 报 139，cutoff 从 06-08 移到 06-14）。**报告必须写明漂移原因**，并单列「维护型过期页」清单（09-12 为 6 页：three_brands_mid2026 / china_apparel_2026q1_operations / china_apparel_industry_scale_2026 / 服装采购渠道选型2026 / 男装品牌竞争格局2026Q1 / 探马SCRM）。
- **基准零改动证明（09-12 固化手法）**：①刷新前把 `kb_benchmarks.json` **剥除元数据键**（`updated` + `meta.{last_scan,files_scanned,data_points,updated}`）→ JSON 序列化（`sort_keys=True`）存快照；②`--apply` 刷新；③同法再剥再比 → **逐字节一致 = 阈值零改动**（09-12 实测 2→3 行变更，仅日期）。
- **relations 试点**（CLAUDE.md §2.6）：仅 entity 页；目标用文件名；对称关系只写一侧；试点范围约 10-15 个核心品牌，未铺满。

## 常见修复模式（首轮实修 35 处）

| 模式 | 处理 |
|------|------|
| `[[wiki/10_web/articles/X]]` 双前缀 | → `[[10_web/articles/X]]`（按文件实际落点） |
| 信息链"上游来源 [[品牌_主题占位]]（真实描述）" | 删占位 wikilink，保留括号描述 |
| 错误日期/改名源链（08-23 实为 08-21/08-26） | 以实际文件名重指 |
| `[[gxg_muson]]`（benchmarks 键名非文件名） | → `[[muson_gxg\|GXG]]` |
| `[[品牌墙图_2026-08-14]]`（sources: 标签非页面） | 转明文 |
| 多页引用同一缺失方法论锚点（如品牌联名策略） | 可新建 concept 页闭合（须含结论+信息链+关联页面+index 登记） |
| **幻影链：实体页 cross_refs 指向"核验登记页"但未造页**（09-12 A1 批 8 处） | 采集轮判「显式核验无新增、不造 source 页」时，核验内容应**内联在实体页 `## 核验登记（日期）` 小节**，**cross_refs 不得加** `[[<日期>_<轮次>_<品牌>_核验登记]]` → 直接删该 cross_refs 条目 |
| 源链为「两页合并名」（如 `2026-08-30_ellesse_美国回归与AndrewGarfield全球战役`） | 查平行页写法取其一（09-12 参照 09-11 页写法改指 `2026-08-30_ellesse_美国市场回归`） |
| 源链文件名被截断（如 dkny `…品牌经营颗粒` 实为 `…品牌经营颗粒与MarcJacobs整合`） | 按实际文件名补全重指 |
| 源链日期错误且该名**从未存在**（如 dekashell `2026-08-31_加盟扩张与渠道下沉`） | 先 `git log --all --diff-filter=A --name-only` 核查全历史确认不存在，再按语义重指真实页 |

## 防复发硬约束（建议写入采集轮规范第九步）

> 采集轮「显式核验无新增」时：**核验登记内容只写实体页内联小节，禁止在 `cross_refs` 添加指向独立「核验登记页」的链接。**（09-12 optimize 轮 11 处断链中 8 处由此产生）

## Git 分段提交（遵循 CLAUDE.md §4.5，禁 `git add knowledge_base/` 整目录）

1. relations 试点等独立变更单独成段（保留他人未提交工作，不吞并）。
2. 织网修复段：entities/concepts/sources/index.md。
3. 产物段：`90_meta/__index__/master_index.json` + `kb_benchmarks.json` + `90_meta/log.md` + `90_meta/_health/*`。
4. 规范段（若本轮修订了 `_automation_optimize.md` / CLAUDE.md 等规范文件）：单独成段。

**执行要求**：
- **精确路径**：用 `git diff --name-only -- <子路径>` 取文件清单后逐路径 add（`git add -- <file1> <file2> ...`），**禁用 `git add knowledge_base/`**。
- **暂存区复核**（CLAUDE.md 教训：`git add` 原子失败会静默零暂存）：每次 commit 前必须 `git -c core.quotepath=false diff --cached --name-only` 核对文件数与本轮改动清单一致，不能只看 `git status`。
- **噪音排除**：`.obsidian/plugins/*` 与 `.workbuddy/`（含 memory / automations）为运行期噪音，不入段。
- push 后核对 `git rev-parse HEAD` == `git rev-parse origin/main`（若 refs 幽灵问题复发，以 `git ls-remote origin main` 为权威）。
