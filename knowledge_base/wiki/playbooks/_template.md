---
type: playbook
title: 作战手册模板
tags: [playbook, template, sop]
sources: [CLAUDE.md]
created: 2026-08-09
updated: 2026-08-09
cross_refs: [[决策日志_模板]], [[清仓决策树]], [[导购培训SOP]]
---

# 作战手册模板（Playbook Template）

> 本文件是 `wiki/playbooks/` 下所有作战手册的写作模板。复制本文件、改名、填充内容即可新建一篇手册。
> 作战手册 = 可直接照做的 SOP / 决策树 / 复盘模板，是知识库里"怎么干"的层（区别于 `wiki/sources` 的"情报"层和 `wiki/concepts` 的"概念"层）。

## 何时写作战手册

- 某个业务流程被重复执行（订货会、清仓、导购培训、VIP 维护…）
- 某个决策反复出现且需要统一判断标准（是否清仓、是否补单…）
- 某次复盘提炼出可复用的方法论

## Frontmatter 规范（必填）

```yaml
---
type: playbook          # 固定值，CLAUDE.md §2.1 已登记
title: 手册标题
tags: [playbook, 业务域, 关键词]
sources: [引用的概念页/实体页/来源页]
created: YYYY-MM-DD
updated: YYYY-MM-DD
cross_refs: [[关联概念页]], [[关联实体页]]
---
```

## 正文区块建议

```markdown
# 标题

> 一句话说清这手册解决什么、给谁用

## 适用场景
（什么时候该掏出这本手册）

## 决策树 / 步骤（核心）
（用缩进列表或表格表达分支逻辑，避免纯散文）

## 关键指标与红线
（配套要监控的 KPI、阈值、告警线）

## 关联页面
（[[双链]] 到相关概念/实体/其他手册）

## 待办 / 待验证
（本手册待打磨的点）
```

## 写作纪律

1. **可操作优先**：每篇必须给出"下一步具体动作"，不许只讲道理。
2. **带双链**：至少链 1 个已存在的 concept/entity，绝不孤岛。
3. **接回 Home 与对应 MOC**：新建后必须在本手册 `cross_refs` 与对应 `MOC_Lxx` 中加入入口。
4. **版本化**：重大修订只更新 `updated` 字段 + 在文末记一笔变更，不覆盖历史判断。

---

*最后更新：2026-08-09 · Fashion Doctor KB*
