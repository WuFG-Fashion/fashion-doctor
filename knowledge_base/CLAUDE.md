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
│   └── sources/           ← 来源摘要：每篇 raw/ 文章的提炼
├── L2_00_AI前沿信息/       ← 保留：现有业务分类（逐步迁移到 wiki/）
├── L2_01_零售基础理论/
├── ... (其他 L2)
├── kb_updater.py          ← 索引扫描器（保留）
├── retrieval_mod.py       ← 检索模块（保留）
└── __index__/             ← JSON 索引（保留）
```

---

## 二、Wiki 页面规范

### 2.1 全局 Frontmatter

每个 wiki 页面文件头部必须包含以下 YAML frontmatter：

```yaml
---
type: entity | concept | practice | comparison | source
title: 页面标题
tags: [tag1, tag2, tag3]
sources: [来源文件名或 URL]
created: YYYY-MM-DD
updated: YYYY-MM-DD
cross_refs: [[引用页1]], [[引用页2]]
---
```

### 2.2 页面类型与路由

| type | 目录 | 命名格式 | 示例 |
|------|------|----------|------|
| `entity` | `wiki/entities/` | `[品牌名/公司名/人名].md` | `peacebird.md` |
| `concept` | `wiki/concepts/` | `[概念名].md` | `sell_through_rate.md` |
| `practice` | `wiki/practices/` | `[场景]_[主题].md` | `sql_dead_stock_query.md` |
| `comparison` | `wiki/comparisons/` | `[A]_vs_[B].md` | `peacebird_vs_gxg.md` |
| `source` | `wiki/sources/` | `YYYY-MM-DD_[标题].md` | `2026-05-11_太平鸟2025年报.md` |

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

## 关联页面
（[[]] 双链列表）

## 待办 / 待验证
（标记矛盾或待补充项）
```

---

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
4. 必须更新 `wiki/index.md`（追加新页面链接）
5. 必须追加 `wiki/log.md`（记录操作：时间 + 动作 + 文件）
6. 检查是否有矛盾（不同来源对同一数据的说法冲突），如有则标记

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
- 矛盾：同一数据在两个页面中有不同值
- 过期：`updated` 超过 90 天未更新
- 分类错误：页面存放位置与 frontmatter `type` 不一致

### 3.5 自动织网（link）

触发指令：`kb-link`

执行步骤：
1. 扫描所有 wiki/ 页面
2. 识别可建立 `[[]]` 双链的机会（同名实体、共用概念、上下游关系）
3. 自动添加双向链接
4. 更新 `wiki/index.md`

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
[[文件名不含路径.md]]
[[wiki/entities/peacebird.md|太平鸟男装]]
[[KPI健康基准]]
```

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

---

## 五、内容质量标准

### 5.1 必须包含

- [ ] 有效的一句话说清这页是什么
- [ ] 至少一条 `[[双链]]`
- [ ] 正确的 `type` frontmatter
- [ ] 可追溯的来源标注

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
