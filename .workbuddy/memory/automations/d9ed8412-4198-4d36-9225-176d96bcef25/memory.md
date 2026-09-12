# optimize 轮 自动化执行记忆（lint + 织网 + 索引重建）

## 执行历史

### 2026-09-06 · 首轮（11:19-11:40）— 4 commits 已推送（a22a256 → ca398cf）
- **lint 五规则终态**：断链 0 / 孤岛 0（入链 1361/1361=100%）/ 分类错 0 / 缺 updated 0 / 矛盾 0 新增。
- **断链 76 检出 → 0**：实修 35 处（raw 双 wiki 前缀 15 / 信息链占位上游 11 / 错误日期文件名 5 / 双核对照待建 1 / 品牌墙图标签 1 / 待办拟建页 1）；其余为 lint 解析误报（raw 全路径 30、index `\|` 2、log.md 豁免 5、kb_benchmarks.json 有效 3），已修解析器。
- **新建概念锚点**：`wiki/concepts/品牌联名策略.md`（lacoste 三档分层法，闭合 lacoste 实体+A290 源 2 页 3 处引用）+ index.md 概念库登记。
- **矛盾基线对账**：⚠️ 全库 57 页/66 处（=语义层 54 + raw 3）、ℹ️ 129 处 —— 与历史基线完全一致；entity↔benchmarks 数值交叉 6 hits 全为伪命中。
- **过期 54**：50 静态源页判"数据快照不判罚"；4 个 Q1 历史分析页维持不动，建议下轮评估 superseded_by。
- **产物**：master_index.json → 1361 L3（+1）；kb_benchmarks.json 元数据刷新（65 实体+113 概念/318+ 数值/未动阈值）；`_health/2026-09-06_daily_health_optimize.md`；log.md 行。
- **relations 试点**：他人 09:40 未提交工作（CLAUDE.md 2.6 + peacebird/cabbeen/dekashell relations + ontology_pilot_草案.md）已保留并单独成段提交。
- **git**：分 4 段推 main：a22a256(relations) / 37742c3(织网修复) / 6167cd2(产物) / ca398cf(规范)。
- **规范落地**：新增 `_automation_optimize.md`（口径/基线/豁免/修复模式/分段提交），下轮直接引用。

### 2026-09-12 · 第 2 轮（11:36-11:45）— 2 commits 已推送（73fe3c9 → dfd3d22）
- **lint 五规则终态**：断链 **11 → 0**（实修 11 处）/ 孤岛 0（入链 1407/1407=100%）/ 分类错 0 / 缺 updated 0 / 矛盾 0 新增（⚠️ 全库 57 页/66 处与 09-06 基线**逐字一致**）。
- **断链 11 处根因**（新类型，值得下轮预防）：①**8 处幻影链**——A1 轮对 8 品牌判「显式核验无新增、不造 source 页」，但实体页 cross_refs 写了 `[[2026-09-12_A1_<brand>_核验登记]]` 指向从未创建的页 → 删 cross_refs 条目（内容已内联各实体页 `## A1轮核验登记（2026-09-12）` 小节）；②**3 处错误日期/截断/合并源链**（dekashell 08-31→08-21 渠道下沉与门店口径 / dkny 09-04 补全「与MarcJacobs整合」/ ellesse 08-30 合并名→美国市场回归），按实际文件名重指（git 全历史核查确认 08-31 dekashell 文件名从未存在）。
- **织网升级**：孤岛 0 不代表连通性已够 → 新增**连通性分析**（区分「index.md 登记入链」vs「语义入链」）：实测 **0 页仅靠 index.md**、入链来源分布 1源16/2源77/3源166/4源163/5+源985。据此定位 6 个 `cross_refs: []` 为空的遗留页（16brands_2026q1_snapshot / ai_policy / bosideng_fy2026_deep_dive / vogue_business_ai_consumer_2026 / croquis / gxg），补 **21 条自然链接** + `## 关联页面` + 「织网说明」注语义依据。**这个「空 cross_refs 筛查」比孤岛检测更能找到真实薄弱点，建议固化为每轮动作。**
- **索引**：master_index.json → kb_version 3.1 · **1407 L3**（+46 较上轮 1361）。
- **基准受控刷新**：`scripts/update_benchmarks_controlled.py --apply`——dry-run 拟新增竞品 0 个，故为**纯元数据刷新**；补同步了上轮遗漏的 `meta.updated`（脚本只刷顶层 updated + meta.last_scan）。**验证手法（可复用）**：刷新前把文件剥除元数据键后 JSON 序列化存快照，刷新后再剥除比对 → 证明阈值区逐字节未动。
- **过期 54 → 139 属正常漂移**：90 天 cutoff 随日期前移，06-09~06-14 静态源页整批跨阈值；静态源页不判罚口径不变。**报告里必须写明这一点，否则会被误读为质量退化。**
- **矛盾口径陷阱**：全库 grep 会命中 `_health/*` 快照与 `CLAUDE.md` 里的规则文本自引用 → 统计必须**排除 _health 与 CLAUDE.md**，否则得 71/82 而非真实 57/66。
- **产物**：`_health/2026-09-12_daily_health_optimize.md` + log.md 行；分 2 段提交（无 relations 独立变更）。
- **下轮待办**：①在 `_automation_A1/A2/A3.md` 第九步加硬约束「核验登记只写实体页内联小节，禁止 cross_refs 指向独立核验登记页」；②6 个维护型过期页收口；③ℹ️ 基准核对 129→156 应定性为「自洽标注数」。

## 执行要点（可复用）
1. lint 工具 `.kbtmp/opt_lint.py`（结果 `.kbtmp/opt_lint_result.json`）——gitignored，无需入库。
2. **解析器三坑已修**：①同名文件 raw 副本遮蔽 → 语义层优先；②`wiki/raw/articles/X` 全路径被单段剥离截断 → 级联剥离；③表格 `\|` 转义目标带反斜杠 → 先归一化再分割。
3. 矛盾基线口径 = 全 wiki 含 raw 副本（57/66、129），语义层单独看是 54 页。
4. 首轮发现 raw 双树并存（KB/raw/articles vs wiki/raw/articles），建议后续统一，消除同名歧义。
5. **织网找薄弱点用「空 cross_refs 筛查」**，不要只看孤岛数——孤岛=0 时仍有 6 个 `cross_refs: []` 的空壳页（第 2 轮实测）。配合「入链来源数分布（排除 index.md）」判断真实连通性。
6. **矛盾计数必须排除 `_health/*` 与 `CLAUDE.md`**：这两处会自引用「⚠️ 数据矛盾」字样，含进去得 71 页/82 处，排除后才是真实 57 页/66 处基线。
7. **基准零改动证明手法**：刷新前剥除元数据键（updated/last_scan/files_scanned/data_points/updated）→ JSON 序列化存快照；刷新后同法再剥再比 → 逐字节一致即证明阈值未动。
8. 本机 Git Bash 下 `grep -rl` + 管道进 `python -c` 处理中文路径易触发转义报错 → 改用 heredoc 传脚本（`.kbtmp/` 或直接 `python - <<'PY'`）。
