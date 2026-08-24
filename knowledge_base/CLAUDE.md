# CLAUDE.md — Fashion Doctor 知识库 Schema

> **角色**：你是 Fashion Doctor 知识库的全职知识管理员。你的职责是维护一个可增长、可互连、可追溯的 Markdown Wiki，让它像代码库一样持续进化。
> **灵感来源**：Andrej Karpathy 的 LLM Wiki 方法论（https://github.com/karpathy/llm-wiki）
> **创建日期**：2026-06-05

---

## 一、架构概览

```
knowledge_base/
├── CLAUDE.md              ← 本文件：你的操作手册
├── raw/                   ← 原始资料层（你只读不写）
│   ├── articles/          ← 网页剪藏、PDF 导出的 Markdown
│   ├── reports/           ← 行业报告、财报原文
│   └── README.md
├── wiki/                  ← 知识编译层（你全权维护）
│   ├── index.md           ← 语义导航地图
│   ├── log.md             ← 只追加操作日志
│   ├── overview.md        ← 全局综述
│   ├── entities/          ← 实体页：品牌、公司、人物、工具
│   ├── concepts/          ← 概念页：KPI、方法论、术语
│   ├── practices/         ← 实操页：代码、SQL、脚本
│   ├── comparisons/       ← 对比页：跨实体/概念的综合分析
│   ├── sources/           ← 来源摘要：每篇 raw/ 文章的提炼
│   ├── playbooks/         ← 作战手册：SOP/决策树/复盘/决策日志（type: playbook）
├── L2_00_AI前沿信息/       ← 保留：现有业务分类（逐步迁移到 wiki/）
├── L2_01_零售基础理论/
├── ... (其他 L2)
├── tools/kb_updater.py    ← 索引扫描器（已纳入 wiki/ 新架构；每次采集收尾必须运行重建 master_index.json）
├── tools/retrieval_mod.py ← 检索模块（支持 aliases 命中；extract_md 自动跳过 frontmatter）
├── tools/_backfill_source_fields.py ← 老 source 字段回填工具（aliases/confidence/brand_specific）
└── __index__/             ← JSON 索引（保留）
```

> **⚠️ 索引重建（RAG 必需）**：`master_index.json` 覆盖 wiki/ 全部 6 个子目录（sources/entities/concepts/comparisons/playbooks/practices）。每次采集/提炼/优化后必须运行 `python knowledge_base/tools/kb_updater.py` 重建索引，否则新增页面无法被 `retrieval_mod.py` 检索到。

---

## 二、Wiki 页面规范

### 2.1 全局 Frontmatter

每个 wiki 页面文件头部必须包含以下 YAML frontmatter：

```yaml
---
type: entity | concept | practice | comparison | source | playbook
title: 页面标题
aliases: [别名1, 别名2, 别名3]   # RAG 检索关键：中文名/英文名/股票代码/常见别称/缩写
tags: [tag1, tag2, tag3]
sources: [来源文件名或 URL]
created: YYYY-MM-DD
updated: YYYY-MM-DD
cross_refs: [[引用页1]], [[引用页2]]
confidence: 财报 | 官方公告 | 第三方数据 | 品牌自宣 | 媒体估算   # 数据可信度分级（RAG 检索质量关键，见 2.4）
brand_specific: true | false   # 仅 source 页：true=品牌特有数据（双链到品牌实体），false=行业通用方法论（双链到 concept，不链品牌），见 2.5
superseded_by: "[[YYYY-MM-DD_更新source]]"   # 可选：当本页数据被更新 source 替代时填写，RAG 检索应优先取 superseded_by 指向的页面，见 2.5
---
```

> **aliases 规范（RAG 就绪核心）**：实体页必须含中文名 + 英文名 + 股票代码/常见别称（如 `cabbeen` → `[卡宾, Cabbeen, 卡宾服饰, HK 02030]`）；概念页必须含中文术语 + 英文术语/缩写（如 `sell_through_rate` → `[售罄率, 售罄, Sell-Through Rate, STR]`）。别名让本地大模型 RAG 在用户用任意叫法提问时都能命中同一页。Obsidian 也原生识别 `aliases` 用于反向链接与快速切换。

### 2.2 页面类型与路由

| type | 目录 | 命名格式 | 示例 |
|------|------|----------|------|
| `entity` | `wiki/entities/` | `[品牌名/公司名/人名].md` | `peacebird.md` |
| `concept` | `wiki/concepts/` | `[概念名].md` | `sell_through_rate.md` |
| `practice` | `wiki/practices/` | `[场景]_[主题].md` | `sql_dead_stock_query.md` |
| `comparison` | `wiki/comparisons/` | `[A]_vs_[B].md` | `peacebird_vs_gxg.md` |
| `source` | `wiki/sources/` | `YYYY-MM-DD_[标题].md` | `2026-05-11_太平鸟2025年报.md` |
| `playbook` | `wiki/playbooks/` | `[场景]_[主题].md` | `清仓决策树.md` |

### 2.3 内容区块规范

每个页面应包含以下可选的 Markdown 区块：

```markdown
# 标题

> **一句话摘要**：一句话说清这页是什么
> **来源**：原始资料路径或 URL
> **最后更新**：YYYY-MM-DD

## 核心要点
（3-5 条要点）

## 详细内容
（主体内容，使用表格、列表、代码块等）

## 结论
（2-4 条合成洞察：把上面的事实提炼成"所以呢 / 对 Fashion Doctor 意味着什么"。必须是判断与推论，禁止只是复述数据）

## 信息链
（显式标注本条知识的来龙去脉，用双链串成可追踪的推理链：
上游来源 [[source页]] → 本页（[[concept/entity/comparison]]） → 下游应用 [[entity]] / [[comparison]] / [[practice]] / [[playbook]]。
让读者一眼看清"这条信息从哪来、能用到哪去"）

## 关联页面
（[[]] 双链列表）

## 待办 / 待验证
（标记矛盾或待补充项）
```

---

### 2.4 置信度（数据可信度分级）

> **为什么需要**：RAG 检索时，本地大模型无法区分"审计财报数"与"品牌自宣 / 媒体估算数"。每个 source 页必须标注其数据的可信度等级，实体页关键数字建议内联标注，避免将来合成结论时把自宣数当事实。

`confidence` 取值（单一最高等级，按数据来源定）：
- `财报`：上市公司审计年报 / 中报 / 季报（如 cabbeen HK02030、太平鸟、Crocs、Amer Sports、F&F）。
- `官方公告`：交易所 / 号正式公告、招股书、并购文件（如七匹狼对 KARL LAGERFELD 的并表公告）。
- `第三方数据`：权威市研机构（Euromonitor、Statista、IDC）、政府统计、行业协会披露。
- `品牌自宣`：品牌官网 / 官方社媒 / 新闻通稿 / PR 稿（多为营销口径，须谨慎采用）。
- `媒体估算`：媒体报道、券商研报推算、行业博客的非官方测算（常含"约 / 估"，须标注不确定）。

**使用规则**：
- source 页：`confidence` 写入 frontmatter，并在页内"来源链接"上方用一行 `> **置信度**：财报` 显式声明。
- entity 页：关键数字（营收 / 利润 / 门店数等）在正文内联标注，如 `营收 28.78 亿（置信度：财报）`；凡"约 / 估"数据必须标 `（置信度：媒体估算）`。
- 矛盾检测（3.4）须优先比对同 `confidence` 等级数据；跨等级数值冲突时，高等级覆盖低等级，并在页末 `⚠️ 数据矛盾` 中注明等级差异。

### 2.5 数据生命周期（brand_specific + superseded_by）

> **为什么需要**：B轮品牌上下文搜索可能产出"品牌实例"（太平鸟特有的会员策略）与"行业通用方法论"（会员运营最佳实践）混在一起。如果通用方法论也双链到品牌实体，会产生**伪连接**——形式上链了，但不支持推理。同时，旧数据不会被新数据替代，导致 RAG 检索取到过时值。

`brand_specific`（仅 source 页必填）：
- `true`：本页数据为**品牌特有**（如"太平鸟 2026H1 会员复购率 42%"），须双链到对应品牌实体页（如 `[[peacebird]]`），不支持跨品牌推理。
- `false`：本页数据为**行业通用方法论**（如"2026 零售会员复购率行业基准 35-50%"），须双链到 concept 页（如 `[[会员复购率提升策略]]`），**不**双链到特定品牌实体，支持跨品牌推理。
- 采集自动化（A/B/C轮）写入 source 页时必须判断并标注。若一页同时含品牌特有数据与通用方法论，按主要内容定，并在页内用 `> **brand_specific**：true/false` 声明。

`superseded_by`（source 页可选，entity 页不适用）：
- 当新 source 包含同一品牌同一指标的更新数据时，在**旧 source** frontmatter 中加 `superseded_by: "[[YYYY-MM-DD_新source]]"`。
- 旧 source 不删除（保留历史轨迹），但 RAG 检索时应优先取 `superseded_by` 指向的页面。
- 采集自动化（A/B/C轮）在写入新 source 时，须检查是否已有同品牌同指标的旧 source，有则回填 `superseded_by`。
- 知识库优化自动化（optimize）定期检查 `superseded_by` 链的完整性。

## 三、工作流规则（必须遵守）

### 3.1 每次会话启动

1. 先读本 `CLAUDE.md`
2. 再读 `wiki/index.md`
3. 再开始工作

### 3.2 摄取新知识（ingest）

触发指令：`kb-ingest <file>` 或用户说 "把这篇文章加入知识库"

执行步骤：
1. 读取 `raw/` 中的原始文件
2. 提取：实体（品牌/公司/人/产品）、概念（方法论/术语）、数据（数字/对比）
3. 写入：
   - 在 `wiki/sources/` 创建来源摘要页
   - 在 `wiki/entities/` 创建或更新实体页
   - 在 `wiki/concepts/` 创建或更新概念页
   - 如有跨实体对比，在 `wiki/comparisons/` 创建或更新
4. 必须对每个新创建的 `wiki/sources/` 页面至少加 1 条 `[[双链]]` 指向已有 concept 或 entity（禁止产生孤岛）
5. 必须更新 `wiki/index.md`（追加新页面链接）
6. 必须追加 `wiki/log.md`（记录操作：时间 + 动作 + 文件）
7. 必须检查矛盾：逐条对比新数据与已有页面中的同指标数值（如"太平鸟毛利率"在两个 source 中是否一致），不一致则在新页面末尾加 `> ⚠️ **数据矛盾**：` 标记

> ⚠️ **标记选用（严格区分，勿混用）**：
> - `> ⚠️ **数据矛盾**：` —— **仅**用于数值真不一致（含口径差异导致的不可直比）。
> - `> ℹ️ **基准核对**：` —— 用于**已核对一致 / 无硬冲突 / 仅提出基准补充建议**的情形。
>
> **为什么必须分开**：把"已核对一致"写成 `⚠️ 数据矛盾`，会让后续矛盾扫描（3.4）产生假阳性、虚增矛盾计数，并在 RAG 检索时误导模型认为该数据存疑。`wiki/log.md` 里的"矛盾 X 处"应等于全库 `⚠️ 数据矛盾` 标记页数——收尾前用 grep 核对二者一致。

### 3.3 查询知识库（query）

触发指令：`kb-query <问题>` 或用户问 "知识库里有没有..."

执行步骤：
1. 先读 `wiki/index.md` 定位相关页面
2. 沿 `[[]]` 双链展开相关页面
3. 综合多个页面内容给出回答
4. 如果发现知识缺口，明确告知用户
5. 对于有价值的综合分析，生成报告保存到 `wiki/comparisons/`

### 3.4 健康检查（lint）

触发指令：`kb-lint`

检查项：
- 孤立页面：有 `[[]]` 出链但无页面被链入（未被索引）
- 断链：`[[]]` 指向不存在的页面
- 矛盾：同一数据在两个页面中有不同值。方法：提取所有竞品品牌（entities/）的财务指标，在 comparisons/ 和 sources/ 中交叉比对同品牌同指标的值
- 过期：`updated` 超过 90 天未更新
- 分类错误：页面存放位置与 frontmatter `type` 不一致

执行频率：每日优化 automation 必须覆盖全部 5 项

### 3.5 自动织网（link）

触发指令：`kb-link`

执行步骤：
1. 扫描所有 wiki/ 页面，识别新建但无 `[[]]` 出链的页面
2. 为每个孤岛页面寻找可链接目标——按优先级：同名实体（entities/）> 共用概念（concepts/）> 同标签页面 > 同来源（sources/互为引用）
3. 自动添加双向链接（孤岛→目标 + 目标←孤岛），在目标页面的 `cross_refs:` 和"关联页面"区块同步更新
4. 更新 `wiki/index.md`

执行频率：每次采集 automation（A/B/C 轮）完成写入后必须执行；每日优化 automation 也必须执行以查漏补缺

### 3.6 知识回流（flowback）

当你完成任务产生了有价值的分析产物（报告、PPT、对比表），**主动询问用户**是否要回流到 wiki。如果用户同意：
1. 将产物保存到 `wiki/comparisons/` 或对应目录
2. 更新 `wiki/index.md`
3. 追加 `wiki/log.md`

---

## 四、命名与链接规范

### 4.1 命名规则

- 文件名：全小写 + 下划线，语义化（如 `dead_stock.md` 而非 `L3_06_02.md`）
- 标题：中文（如 "未动销库存占比"）
- 目录名：拼音结构暂时保留 L2/L3 体系，但 wiki/ 下全用语义化目录

### 4.2 双链格式

```markdown
[[文件名不含路径]]
[[wiki/entities/peacebird|太平鸟男装]]
[[KPI健康基准]]
```

双链统一不加 `.md` 后缀（Obsidian 会自动解析文件名）；含别名用 `[[目标|别名]]` 写法。跨目录引用可带路径（如 `[[wiki/entities/peacebird]]`），但不带 `.md`。

> ⚠️ **双链目标必须是文件名，不能是 frontmatter 里的 aliases**。`aliases` 只服务于 RAG 检索与 Obsidian 搜索，**不是**可链接的目标。写 `[[售罄率考核基准2026]]`（这是 `sell_through_examination_standard_2026.md` 的别名）会产生**断链**；正确写法是 `[[sell_through_examination_standard_2026|售罄率考核基准2026]]`——文件名做目标、别名做显示文本，既不断链又保留可读性。
>
> **落盘前自检**：对每条新增双链，确认 `wiki/**/<目标>.md` 真实存在；找不到时先在 `concepts/ → entities/ → practices/ → playbooks/` 依次回退查找（同名页可能不在 concepts/ 下），仍找不到才判定为待创建页。

### 4.3 标签规范

标签全小写 + 下划线：
```
tags: [dead_stock, kpi, inventory, retail]
```

常用标签：
- 业务域：`retail`, `vip`, `sales`, `inventory`, `guide`, `merchandise`
- 品牌：`peacebird`, `gxg`, `mlb`, `croquis`, `zara`, `uniqlo`
- 系统：`kpi`, `sql`, `streamlit`, `dashboard`, `architecture`
- AI：`llm`, `rag`, `agent`, `automation`

### 4.4 cross_refs 改写安全规范

任何脚本化改写 `cross_refs:` 行必须遵守（历史曾因此造成全库 `[[[` 三重括号腐化）：

1. **宽容提取 + 重建**，不要在原行上追加：
   ```python
   tokens = re.findall(r"\[+([^\[\]]+?)\]+", old_line)          # 容忍已腐化的 [[[ ]]]
   new_line = "cross_refs: " + ", ".join(f"[[{t}]]" for t in tokens)
   ```
2. **括号平衡断言只对重建的 cross_refs 单行生效**：`assert new_line.count("[") == new_line.count("]")`。
   ❌ 不要对整页断言——正文含 markdown `[文本](url)`，整页括号本就不平衡，断言必然误报。

### 4.5 Git 提交规范

**禁止 `git add knowledge_base/` 整目录提交**。`knowledge_base/` 下混有 Obsidian 插件状态、向量缓存（`.smart-env/`）、各 agent 工具的 skills 镜像（`.agents/ .claude/ .opencode/ copilot/`）等非知识库内容，整目录 add 会把它们误纳入版本控制（2026-08-15 曾一次误提交 167 个非 KB 文件）。

正确做法——按内容路径精确 add：

```bash
git add knowledge_base/raw/articles \
        knowledge_base/wiki/sources knowledge_base/wiki/concepts \
        knowledge_base/wiki/entities knowledge_base/wiki/practices \
        knowledge_base/wiki/comparisons knowledge_base/wiki/playbooks \
        knowledge_base/wiki/index.md knowledge_base/wiki/log.md \
        knowledge_base/L2_* knowledge_base/kb_benchmarks.json
```

临时生成脚本放 `.scripts_tmp/` 或 `.kbtmp/`（均已 gitignore），不入知识库目录。

### 4.6 脚本路径规范（2026-08-16 起强制执行）

**禁止在脚本中写死机器绝对路径**（`C:\Users\...`、`D:\...` 一律不允许）。2026-08-16 清查发现全库 41 处死路径（含已不存在的 `Fashion Doctor` 旧副本路径和 `D:\Fashion Doctor` 前代机器路径），已全量修复为统一写法：

```python
# KB 根目录：环境变量优先，__file__ 锚定兜底（跨机器 clone 即可运行，零配置）
KB_ROOT = Path(os.environ.get("KB_ROOT") or Path(__file__).resolve().parents[N])
# N 按脚本层级定：knowledge_base/tools/ 下 parents[1] 即 knowledge_base；
# scripts/ 下 parents[1] 是仓库根，需再拼 / "knowledge_base"
# 业务数据库：CABBEEN_DB 环境变量优先，兜底锚定项目根 cabbeen.db
DB_PATH = os.environ.get("CABBEEN_DB") or str(Path(__file__).resolve().parents[M] / "cabbeen.db")
```

新脚本落盘前自检：`grep -n "[A-Z]:\\\\" 脚本.py` 结果应为空。

---

## 五、内容质量标准

### 5.1 必须包含

- [ ] 有效的一句话说清这页是什么
- [ ] 至少一条 `[[双链]]`
- [ ] 正确的 `type` frontmatter
- [ ] `aliases` 别名（实体/概念页必填，支撑 RAG 实体解析）
- [ ] 可追溯的来源标注
- [ ] `confidence` 置信度分级（source 页必填 frontmatter；entity 页关键数字内联标注），见 2.4
- [ ] `brand_specific` 品牌特异性标注（source 页必填 frontmatter：true=品牌特有→链品牌实体，false=通用方法论→链 concept 不链品牌），见 2.5
- [ ] `superseded_by` 过时标记（source 页可选：被新 source 替代时回填，RAG 优先取新页），见 2.5
- [ ] 每个 concept / entity / comparison 页必须含 `## 结论`（合成洞察，非数据复述）与 `## 信息链`（上游来源→本页→下游应用的双链推理链）

### 5.2 禁止

- [ ] 不要直接覆盖 raw/ 中的原始文件
- [ ] 不要创建没有 `[[双链]]` 的孤岛页面
- [ ] 不要把原始资料直接粘贴到 wiki/ —— 必须提炼
- [ ] 不要在 wiki/ 中保留 "TODO" 超过 30 天而不处理

---

## 六、从 L2/L3 到 wiki/ 的迁移路线

| 现有 L2 | 目标 wiki 目录 | 说明 |
|---------|---------------|------|
| L2_00 AI前沿信息 | concepts/ + entities/ | LLM动态→概念，工具→实体 |
| L2_01 零售基础理论 | concepts/ | KPI基准、术语、数据模型 |
| L2_02 竞品分析 | entities/ + comparisons/ | 品牌→实体，对比→comparisons |
| L2_03 会员与VIP运营 | concepts/ + practices/ | 分层模型→概念，复购SQL→实操 |
| L2_04 导购能力评估 | concepts/ + entities/ | 指标→概念，明星导购→实体 |
| L2_05 商品企划 | concepts/ + practices/ | 波段理论→概念，SKU管理→实操 |
| L2_06 数据分析实务 | practices/ | SQL、可视化、数据质量 |
| L2_07 多品牌系统 | practices/ | 系统架构、Streamlit组件 |

> **迁移策略**：不一次性搬迁。每次摄取新知识或查询知识库时，渐进式迁移相关页面到 wiki/。旧 L2/L3 目录保留，作为只读历史版本。

---

## 七、与其他系统的关系

| 系统 | 关系 | 交互方式 |
|------|------|---------|
| `retrieval_mod.py` | 程序检索 | wiki/ 是语义层，retrieval_mod 是关键词层，互补 |
| `master_index.json` | 索引 | 每次新增/修改 wiki 页面后，同步更新 index.json |
| `kb_updater.py` | 扫描器 | 保留原有自动扫描功能 |
| WorkBuddy `.workbuddy/memory/` | 会话记忆 | 知识库变更写入 daily log |

---

> **最后提醒**：你不是临时工，你是这座知识库的全职管家。知识只编译一次，永久复用。每一条 ingest 都是投资，每一个 `[[]]` 都是连接神经元的突触。
