---
type: concept
title: 知识库基准文件（kb_benchmarks.json）
aliases: ["kb_benchmarks", "知识库基准", "KPI基准文件"]
tags: [benchmark, kpi, data, infrastructure]
created: 2026-08-24
updated: 2026-08-24
confidence: 官方公告
brand_specific: false
cross_refs: [[服装行业竞争格局]], [[2026-08-18_crocs_HEYDUDE困境与回购资本配置]]
layer: T1
scope: public
volatility: evergreen
as_of: 2026-08-24
review_due_at: 2027-02-20
status: active
---
# 知识库基准文件（kb_benchmarks.json）

> **一句话摘要**：`knowledge_base/kb_benchmarks.json` 是知识库的结构化基准库，集中存放行业 KPI 阈值、竞品财务、会员/导购/商品企划基准等可机读数据，供 API 与 RAG 检索引用。
> **来源**：知识库基础设施
> **最后更新**：2026-08-24

## 核心要点

- 文件路径：`knowledge_base/kb_benchmarks.json`，由采集轮次在写入新数据时同步回填。
- 顶层结构：`industry` / `kpi_health_thresholds` / `competitors` / `membership` / `guide_kpi` / `focus_brands` 等 30+ 键。
- `focus_brands`（35 个）是采集焦点品牌清单，A/B/C 轮均以此为准判断品牌相关性。
- 各采集轮次（A1/A2/A3/B/C）写入 source 时须将同品牌同指标的新数值回填到此文件，并标注 `confidence` 等级。

## 结论

- kb_benchmarks.json 是知识库的「数值事实层」，与 wiki/ 页面的「文本叙事层」互补。
- 矛盾检测（CLAUDE.md 3.4）以它为交叉比对基准：新 source 数值与基准不一致时需标注 `⚠️ 数据矛盾`。
- RAG 部署时应将本文件纳入检索源，使模型可直接引用结构化 KPI 而不依赖文本推断。

## 信息链

- 上游来源：各采集轮次 source 页（财务/门店/会员数据）→ 本文件（数值回填）
- 下游应用：[[服装行业竞争格局]]（对比基准）· API 服务（`kb_api.py` 读取阈值）· 矛盾检测（交叉比对）

## 前沿

**页面性质说明（枢纽页）**：本页是知识库与 V3 系统之间的**结构化契约**——`kb_benchmarks.json`（TTL 300s）是唯一被 API 与 RAG 直接机读的基准源，本页的前沿直接影响系统行为，措辞须谨慎。

**下轮核查（优先级高）**：① 会员复购率三档（15%/28%/12%）与 `sleeping_member_reactivation`（七匹狼 7-10% → 12-16%）、`moco_epo` 实体页（VIP 段 35-45%）的量级差异——三套数字口径不同（全行业基准 vs 单品牌唤醒实战 vs 中高端女装会员段），**须在 json 或页内显式登记适用域**，防 RAG 检索时串口径；② 导购流失率 0.15 与 `AI导购陪练` 等页的引用一致性；③ TTL 300s 的刷新机制与 json 字段 schema 版本化。
