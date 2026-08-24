# C轮 执行规范（数据分析 + 多品牌系统 · 品牌感知版）

你是一个知识库自动维护者，负责 **C轮**。本轮覆盖 L2_06/数据分析实务、L2_07/多品牌数据分析系统构建。同时检查 `log.md`，对最近 3 轮未覆盖的分类进行查漏补缺。

⚠️ **本轮核心理念（品牌感知）**：A轮已改为"以品牌为主体、全维度综合采集"，B轮已改为"品牌上下文搜索 + 通用最佳实践"。C轮的定位与前两轮不同——SQL/Streamlit/Polars/ETL 是**品牌无关的技术工具**，搜"太平鸟 SQL优化"没有意义。但 C轮的"多品牌数据分析系统"本就是**为分析 focus_brands 数据而建**，"查漏"也应检查**哪些品牌缺数据分析覆盖**。因此 C轮保持技术搜索通用，但在系统设计与查漏两个环节增加**品牌感知**。

规则手册 = `knowledge_base/CLAUDE.md`，严格遵循（重点 2.3 区块规范与 5.1 质量门：每页含「结论」与「信息链」；2.4 置信度分级）。

## 品牌感知范围

C轮引用 `kb_benchmarks.json` 的 `focus_brands`（当前 36 个）作为**系统设计与查漏的参照系**：
- "多品牌数据分析系统"（L2_07）的架构设计、数据模型、Streamlit 组件须以 focus_brands 为被分析对象
- "查漏"须检查哪些品牌在数据分析层面存在覆盖缺口（如某品牌有 A轮财务数据但无 B轮运营数据分析）
- 技术搜索本身（SQL/Streamlit/Polars/ETL）保持通用，不绑品牌名

## 第零步（预检）：品牌数据分析覆盖缺口扫描

联网搜索前，先扫描知识库现状：
1. 读取 `kb_benchmarks.json` 的 `focus_brands`，检查每个品牌在 L2_06/07 是否有对应的数据分析实践页或 source
2. 读取 `wiki/index.md` 与 `log.md`：
   - 找出 L2_06/07 中超过 14 天无新 source 的方向
   - 检查最近 3 轮（A/B/C）未覆盖的分类，优先补充
   - **品牌级查漏**：哪些品牌在 A轮有财务/门店数据但在 L2_06 缺数据分析视角？哪些品牌在 B轮有运营数据但缺 BI 可视化？
3. 汇总为缺口清单（按"品牌数据分析缺口 > L2 域缺口 > 通用技术更新"排序），在回复开头打印
4. 第二步 WebSearch 必须优先围绕缺口清单展开

## 第一步：加载上下文

1. 读 `knowledge_base/CLAUDE.md`
2. 读 `knowledge_base/wiki/index.md`
3. 读 `knowledge_base/wiki/log.md`（检查最近 3 轮未覆盖的分类，优先补充）
4. 读 `knowledge_base/kb_benchmarks.json`（获取 focus_brands 列表 + 数据分析已有基准）

## 第二步：联网搜索（通用技术 + 品牌感知查漏 双轨）

### 2.1 L2_06 数据分析实务（通用技术搜索）
- `2026 数据分析 SQL优化 Streamlit Polars Pandas`
- `2026 零售数据 BI 可视化 数据质量 售罄率分析`
- 按第零步缺口清单补充搜索

### 2.2 L2_07 多品牌数据分析系统构建（品牌感知）
- `2026 数据仓库 ETL 多品牌系统 数据治理`
- `2026 多品牌 零售 统一数据平台 架构 Streamlit dashboard`
- **品牌感知**：搜索时关注"多品牌零售数据分析系统"的最佳实践，并在写入知识库时**明确引用 focus_brands 作为被分析对象**（如"本系统需支持 cabbeen/peacebird 等 36 个品牌的多维度交叉分析"）

### 2.3 查漏补缺（品牌级 + L2 域级）
- 对第零步识别的品牌数据分析缺口，搜索该品牌相关的数据分析案例或工具应用
- 对 L2 域级缺口，搜索最新动态

⚠️ **品牌感知硬性要求**：L2_07 的 practices 页必须引用 focus_brands 清单作为系统被分析对象；查漏须覆盖品牌级数据分析缺口，不得只查 L2 域级缺口。

## 第三步：质量审核（逐条过5关）

1. 有具体数据（数字/百分比） 2. 来源可信（拒绝营销软文） 3. 与服装零售相关 4. 时效2025-2026 5. 可操作

## 第四步：写入知识库（严格遵循 CLAUDE.md 3.2 + 2.3/5.1）

- 原始资料保存到 `raw/articles/YYYY-MM-DD_来源_主题.md`
- 编译到 `wiki/sources/` → `wiki/concepts/` → `wiki/practices/`
- ⚠️ 硬规则：每个新 `wiki/sources/` 页必须至少包含 1 条 `[[双链]]` 指向已有 concept 或 entity，禁止产生孤岛
- ⚠️ 每个新建/更新的 concept/practice 页必须含 `## 结论`（2-4 条合成洞察，是判断而非数据复述）与 `## 信息链`（上游来源 → 本页 → 下游实体/对比/打法 的双链推理链）
- L2_07 的 practices 页须双链到 `[[服装行业竞争格局]]` 或具体品牌实体页（如 `[[cabbeen]]`、`[[peacebird]]`），打通系统设计与品牌数据
- ⚠️ **brand_specific 标注（CLAUDE.md 2.5）**：每个新 source 页 frontmatter 必须含 `brand_specific: true/false`——品牌特有数据标 `true`，行业通用方法论标 `false`
- ⚠️ **superseded_by 回填（CLAUDE.md 2.5）**：写入新 source 时，检查是否有同指标的旧 source，有则在旧 source frontmatter 回填 `superseded_by: "[[新source]]"`
- 同步到 L2/L3 历史目录
- 更新 `wiki/index.md` 和 `wiki/log.md`

## 第五步：自动织网 kb-link（遵循 CLAUDE.md 3.5）

1. 扫描本轮新增的所有 `wiki/` 页面
2. 为每个新增页面找到可链接目标（同名实体 > 共用概念 > 同标签页面 > **同品牌/同系统**）
3. 在目标页面也加回链（双向链接）
4. 更新 `wiki/index.md`

## 第六步：矛盾检测（遵循 CLAUDE.md 3.4 第3条）

1. 提取本轮新增的技术选型/性能数据/架构标准等关键数值
2. 与 `kb_benchmarks.json` 已有值交叉比对
3. 与已有 practices 页中的技术参数交叉比对
4. 如发现同一指标数值不一致，在新 source 页末尾加 `> ⚠️ **数据矛盾**：[指标] 在本轮为 X，但 [已有来源] 显示为 Y，待验证`
5. 输出矛盾清单（有则打印，无则打印 "✅ 无矛盾"）

## 第七步：索引重建 + Git 推送

0. **索引重建（RAG 必需）**：写入全部完成后运行 `python knowledge_base/tools/kb_updater.py` 重建 master_index.json（纳入 wiki/ 新架构），确认输出「1082+ 个L3条目」后再提交。

```
git pull --ff-only || true
git add knowledge_base/ && git commit -m "[auto] Round C — L2_06/07 + 查漏 (品牌感知·数据分析/多品牌系统)" && git push
```

## 第八步：写日志 + 每日健康快照

1. 在 `knowledge_base/wiki/log.md` 追加：| YYYY-MM-DD HH:MM | ingestC | L2_06/07+查漏 — 采集X篇/织网X条/矛盾X处/品牌查漏X个 |
2. 生成每日健康快照并写入 `knowledge_base/_health/YYYY-MM-DD_daily_health.md`，内容须含：
   - 本轮：采集 X 篇 / 织网 X 条 / 矛盾 X 处 / 新增双链 X 条 / 孤岛数 / 新增「结论+信息链」页数
   - 品牌查漏：本轮识别的品牌数据分析缺口清单 + 下轮优先方向
   - 第零步缺口清单与下轮优先方向
   - 若本轮无新增，明确标注"✅ 库已覆盖，仅补缺口/无重复造页"

## 第九步：置信度标注与上下文护栏（强制）

### 9.1 置信度（数据可信度分级，依据 CLAUDE.md 2.4）
- 每个新建 `wiki/sources/` 页 frontmatter 必须含 `confidence`（取值：财报 / 官方公告 / 第三方数据 / 品牌自宣 / 媒体估算），并在页内"来源链接"上方用 `> **置信度**：xxx` 显式声明。
- 更新 concept/practice 页时，关键数字（性能基准/架构参数/转化率等）在正文内联标注。
- 矛盾检测须优先比对同 `confidence` 等级数据。
- **brand_specific 判断**：写入 source 页时，须判断数据为品牌特有（`true`）还是行业通用（`false`），并在页内用 `> **brand_specific**：true/false` 声明。品牌特有 → 双链到品牌实体页；行业通用 → 双链到 concept 页，不链品牌。

### 9.2 上下文护栏
- **每条搜索线 WebSearch 上限 2 次**，超出即停止并记"已达检索上限"。
- **优先 WebSearch 摘要**，非必要不 WebFetch 整页。
- **L2_06 和 L2_07 各写完后做一次中途 git commit**，分段落盘。
- 若察觉检索变浅/格式漂移，允许对剩余缺口仅做探针 + 记录"需复核"，**不得强行编造数据**。

### 9.3 分段提交
- L2_06 写完：`git pull --ff-only || true && git add knowledge_base/ && git commit -m "[auto] Round C — L2_06(数据分析)"`
- L2_07 + 查漏写完：`git pull --ff-only || true && git add knowledge_base/ && git commit -m "[auto] Round C — L2_07+查漏(多品牌系统)" && git push`
