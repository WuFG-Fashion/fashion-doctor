---
type: health
title: v2.1 物理改造全量验证报告
created: 2026-09-12
layer: T4
scope: public
volatility: versioned
status: active
retrieval: explicit_only
---

# v2.1 物理改造全量验证报告（2026-09-12）

## 验证结论：通过，物理搬迁零破坏

| 验证项 | 方法 | 结果 |
|---|---|---|
| 索引完整性 | 每批物理改动后重建 master_index | 稳定 1407 L3 条目（step1→step6 全程不变） |
| 断链扫描 | 全库 2023 个 md / 27136 条链接 | 122 broken（过滤 .agents 假阳性后 107） |
| 断链定性 | 逐一核查 107 条 | **全部为既有模板占位符与文档示例**（CLAUDE.md 的 引用页1/source页/{t}、log.md 的示例标题、index.md/_template.md 写作模板、README_human.md 的"你的笔记"），**非本次迁移产生，迁移引入真断链 = 0** |
| 检索冒烟 | retrieve() 实测 | confidence=high，sources/answer 正常返回 |
| Home 脚本化 | tools/build_home.py 生成 | 实时计数：sources 1183 / entities 65 / concepts 113 / comparisons 11 / practices 18 / playbooks 17 / raw 907 / inbox 9 / courseware 34 / legacy 11 |

## 物理改造六步落地清单

1. step1（694d992）逻辑分层先铺：2190 页批量回填 layer/scope/volatility/as_of/expires_at|review_due_at/status
2. step2（23b7cf2）死层退役：MOC×8 + L3×2 移入 50_legacy，标 retired/never
3. step3（7574440）raw 双入口合并为 10_web（同名交集=0，合并安全）+ 全库文本引用改写
4. step4（cc32b08）目录重构落地：00_inbox/10_web/20_personal/30_wiki/40_companies/50_legacy/90_meta + brand_wall 八分区物理成型
5. step5（94f131e）路径引用同步：tools 脚本 + 7 份自动化规范 + CLAUDE.md
6. step6（本批次）Home 脚本化 + 全量验证

## 回滚点

- tag `pre-physical-migration`（已推 origin），物理改造前工作区快照。
