# optimize 轮规范（知识库优化：lint 五规则 + 织网 + 索引重建 + 基准导出）

> 触发：约每 6 天一次（自动化 d9ed8412-4198-4d36-9225-176d96bcef25）。2026-09-06 首轮落地并沉淀本规范。

## 执行步骤（与自动化 prompt 对应）

1. lint 五规则（CLAUDE.md §3.4）——用 `.kbtmp/opt_lint.py` 全扫（只读，结果存 `.kbtmp/opt_lint_result.json`）。
2. 织网修复（§3.5）：断链修复 + 孤岛补链，目标 **断链 0 / 孤岛 0**。
3. `python knowledge_base/tools/kb_updater.py` 重建 `__index__/master_index.json`。
4. 受控刷新 `kb_benchmarks.json` 元数据（updated/last_scan/files_scanned/data_points；**绝不覆盖阈值键值**）。
5. 统计：页面数 / [[]] 双链数 / 孤岛数。
6. log.md 追加行 + `_health/YYYY-MM-DD_daily_health_optimize.md` 快照。
7. 分段 git commit + push（内容修复 → 产物 → log/快照三段；见下）。
8. 写自动化记忆 `.workbuddy/memory/automations/d9ed8412-.../memory.md` + 当日 daily log。

## 口径约定（首轮 2026-09-06 固化，勿随意更改）

- **扫描范围**：wiki/ 语义层 6 目录（entities/concepts/sources/comparisons/practices/playbooks）+ 导航页（index/log/overview）。
- **解析规则**：
  - 链接目标须为**文件名**（非 alias）；容忍 `[[path/../file|label]]`、`#anchor`、`.md` 后缀、表格 `\|` 转义；vault 根相对路径级联剥离（wiki/、raw/、articles/ 等多段）。
  - **同名文件歧义**：语义层目录优先于 raw/_archive（KB 内 wiki/raw/articles 与 KB/raw/articles 双树并存，raw 副本有大量与 sources 同名文件）。
  - 非 md 目标（`[[kb_benchmarks.json]]`）按全库文件存在判定有效。
- **豁免**：log.md（操作日志正文含 [[]] 格式示例与修复说明）；_archive/L2 legacy/raw（只报告不处理，断链另计）。
- **孤岛定义**：语义层页面无任何"语义层或导航页"入链 → 孤岛；sources 只要求出链 + 尽量被 index.md/实体页登记（历史口径"孤岛 0"= hub 目录入链覆盖 100%，勿机械按 433 个无入链 source 造链）。
- **矛盾基线（2026-09-06 对账）**：全 wiki（含 raw 副本）`⚠️ **数据矛盾**` = **57 页 / 66 处**（语义层 54 页 + raw 3 页），`ℹ️ **基准核对**` = **129 处**。运行后若计数仍为基线值 → "矛盾 0 新增"。
- **数值交叉**：entity↔kb_benchmarks 正则检测（scripts/_kb_contradiction_check.py）命中须人工核验；跨行/跨周期/跨指标（如"电商+121%"被当 revenue_growth）多为伪命中，页内"与 kb_benchmarks 一致 ✓"自洽标注为准。
- **过期规则**：50+ 个 2026-06-05~07 静态源页 = 数据快照，**不适用 90 天新鲜度判罚**（updated 即数据时点）；维护型页面（entity/concept/comparison）过期才需处理（首轮 4 个 Q1 历史分析页维持不动，建议评估 superseded_by）。
- **relations 试点**（CLAUDE.md §2.6）：仅 entity 页；目标用文件名；对称关系只写一侧；试点范围约 10-15 个核心品牌，未铺满。

## 常见修复模式（首轮实修 35 处）

| 模式 | 处理 |
|------|------|
| `[[wiki/wiki/raw/articles/X]]` 双前缀 | → `[[wiki/raw/articles/X]]`（按文件实际落点） |
| 信息链"上游来源 [[品牌_主题占位]]（真实描述）" | 删占位 wikilink，保留括号描述 |
| 错误日期/改名源链（08-23 实为 08-21/08-26） | 以实际文件名重指 |
| `[[gxg_muson]]`（benchmarks 键名非文件名） | → `[[muson_gxg\|GXG]]` |
| `[[品牌墙图_2026-08-14]]`（sources: 标签非页面） | 转明文 |
| 多页引用同一缺失方法论锚点（如品牌联名策略） | 可新建 concept 页闭合（须含结论+信息链+关联页面+index 登记） |

## Git 分段提交（遵循 CLAUDE.md §4.5，禁 `git add knowledge_base/` 整目录）

1. relations 试点等独立变更单独成段（保留他人未提交工作，不吞并）。
2. 织网修复段：entities/concepts/sources/index.md。
3. 产物段：`__index__/master_index.json` + `kb_benchmarks.json` + `wiki/log.md` + `_health/*`。

`.obsidian/plugins/*` 与 `.workbuddy/` 为运行期噪音，不入段。
