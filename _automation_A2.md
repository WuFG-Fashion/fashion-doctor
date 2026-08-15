# A轮 第2轮（A2）执行规范

你是一个知识库自动维护者，负责 **A轮第2轮（A2）**。本轮覆盖 L2_00/AI前沿、L2_01/零售基础理论、L2_02/竞品分析 中 **固定分组 A2** 的品牌，事件镜头聚焦门店零售/渠道/线下事件。

规则手册 = `knowledge_base/CLAUDE.md`，严格遵循（重点 2.3 区块规范与 5.1 质量门：每页含「结论」与「信息链」）。

## 本论固定分组（必须全覆盖，不得只跑少源）
A2 负责以下 **12 个焦点品牌（固定，不与 A1/A3 重叠）**：
etudes, g_star_raw, hoka_one_one, humble_humble_r, karl_lagerfeld, king_baby, koyo, lacoste, levis, marcelo_burlon, mlb, mlb_kids

**本论事件镜头**：门店零售 / 渠道 / 线下事件 —— 开店/关店、渠道结构、线下快闪/门店活动、区域拓展、加盟/直营、奥莱/电商渠道。深查以该镜头为主，但凡命中 2025-2026 重大信号也须收录。

⚠️ 硬性分组覆盖规则（最高优先级）：A2 必须覆盖上述 **本组全部 12 个焦点品牌**，不得以「已完整 / OK」为由整体跳过任何本组品牌。「只跑少源」仅为用户单次显式收窄的临时范围，不是默认行为。预检缺口清单可做优先级排序，但每轮每个本组品牌都必须被检索/核验/更新，或显式记录「无新增」后跳过造页（不得静默跳过）。**A1/A3 负责的品牌不在本论范围，不要越界采集。**

## 第零步（预检）：生成缺口清单（仅本组 12 品牌）
联网搜索前，先扫描知识库现状，产出「本轮优先缺口」，让后续搜索有的放矢：
1. 读取 `kb_benchmarks.json` 的 `focus_brands`，取出本组 12 个 key，解析到 `wiki/entities/` 页（别名映射：uniqlo_fast_retailing→fast_retailing、gxg_muson→muson_gxg、zara_inditex→inditex_zara；其余同名）。检查每个是否有实体页 + 至少 3 篇 `wiki/sources/`；标注「缺实体 / 少源 / OK」——**此标注仅用于排序优先级，不影响覆盖**，OK 品牌仍须检索核验。⚠️ 缺口清单**仅围绕本组 12 品牌**，不得扩散到 A1/A3 品牌或非焦点竞品。
2. 读取 `wiki/index.md` 与 `log.md`，找出 L2_00/01/02 中超过 14 天无新 source 且属本组的方向。
3. 汇总为缺口清单，在回复开头打印。
4. 第二步 WebSearch 必须优先围绕缺口清单展开；若某次搜索结果均为已入库内容，记录「无新增」并跳过造页，不得强行重复。

## 第一步：加载上下文
1. 读 `knowledge_base/CLAUDE.md`
2. 读 `knowledge_base/wiki/index.md`
3. 读 `knowledge_base/wiki/log.md`
4. 读 `knowledge_base/kb_benchmarks.json`

## 第二步：联网搜索（本组 12 品牌 × 镜头=门店零售/渠道/线下事件）
用 WebSearch 对每个本组品牌检索 2 次（优先命中第零步缺口清单；镜头聚焦门店/渠道/线下，再辐射本组其余）：
- 各品牌 2025-2026 开店/关店 / 渠道结构 / 线下快闪 / 门店活动 / 区域拓展 / 加盟直营 / 奥莱电商渠道
- 品牌墙品牌（lacoste/levis/marcelo_burlon/mlb/mlb_kids 等）与 karl_lagerfeld 的门店与渠道动态
⚠️ **覆盖硬性要求**：每个本组品牌本轮至少检索 1 次；OK 品牌也须核验是否有 2025-2026 新增，有则更新实体页 + 加 source，无则记录「无新增」。不得因品牌已完整而静默跳过检索。

## 第三步：质量审核（逐条过5关）
1. 有具体数据（数字/百分比） 2. 来源可信（拒绝营销软文） 3. 与服装零售相关 4. 时效2025-2026 5. 可操作

## 第四步：写入知识库（严格遵循 CLAUDE.md 3.2 + 2.3/5.1）
- 原始资料保存到 `raw/articles/YYYY-MM-DD_来源_主题.md`
- 编译到 `wiki/sources/` → `wiki/entities/` → `wiki/concepts/` → `wiki/comparisons/`
- ⚠️ 硬规则：每个新 `wiki/sources/` 页必须至少包含 1 条 `[[双链]]` 指向已有 concept 或 entity，禁止产生孤岛
- ⚠️ 每个新建/更新的 concept/entity/comparison 页必须含 `## 结论`（2-4 条合成洞察，是判断而非数据复述）与 `## 信息链`（上游来源 → 本页 → 下游实体/对比/打法 的双链推理链），遵循 CLAUDE.md 2.3/5.1
- 同步到 L2/L3 历史目录
- 更新 `wiki/index.md` 和 `wiki/log.md`

## 第五步：自动织网 kb-link（遵循 CLAUDE.md 3.5）
1. 扫描本轮新增的所有 `wiki/` 页面
2. 为每个新增页面找到可链接目标（同名实体 > 共用概念 > 同标签页面），优先补「信息链」所需的下游打法/对比页
3. 在目标页面也加回链（双向链接）
4. 更新 `wiki/index.md`

## 第六步：矛盾检测（遵循 CLAUDE.md 3.4 第3条）
1. 提取本轮新增的竞品门店/渠道数据
2. 与 `kb_benchmarks.json` 已有值交叉比对
3. 与 `comparisons/` 下的对比表交叉比对
4. 如发现同一品牌同一指标数值不一致，在新 source 页末尾加 `> ⚠️ **数据矛盾**：[指标] 在本轮为 X，但 [已有来源] 显示为 Y，待验证`
5. 输出矛盾清单（有则打印，无则打印 "✅ 无矛盾"）

## 第七步：Git 推送
```
git pull --ff-only || true
git add knowledge_base/ && git commit -m "[auto] Round A2 — L2_00/01/02 (分组A2·门店渠道镜头)" && git push
```

## 第八步：写日志 + 每日健康快照
1. 在 `knowledge_base/wiki/log.md` 追加：| YYYY-MM-DD HH:MM | ingestA2 | L2_00/01/02 — 采集X篇/织网X条/矛盾X处 |
2. 生成每日健康快照并写入 `knowledge_base/_health/YYYY-MM-DD_daily_health.md`（Obsidian 可读仪表盘），内容须含：
   - 本轮：采集 X 篇 / 织网 X 条 / 矛盾 X 处 / 新增双链 X 条 / 孤岛数 / 新增「结论+信息链」页数
   - 第零步缺口清单与下轮优先方向（**仅限本组 12 品牌**）
   - 引用 `log.md` 中最近一次 optimize 的 lint 结论（断链/孤岛/矛盾）作为健康基线
   - 若本轮无新增，明确标注「✅ 库已覆盖，仅补缺口/无重复造页」
