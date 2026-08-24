---
type: raw
title: retailnorthstar——分品类正价售罄率基准与期初库存校验
collected: 2026-08-01 Round B
topic: 商品企划 / 售罄率与库存风险
source_type: retailnorthstar.ai（Markdown & Inventory Risk）
tags: [sell_through, merchandise, inventory, otb, benchmark, risk]
---

# retailnorthstar——分品类正价售罄率基准与期初库存校验

> 采集：2026-08-01 Round B（商品企划主题·联网检索提炼，非原文粘贴）

## 核心事实
- **分品类正价售罄率基准（满分/优秀参考线）**：
  - Core / Replenishment（核心款/补货款）：**80%-90%**
  - Carry-over（延续款）：**65%-78%**
  - New（新品）：**60%-75%**
  - Seasonal（季节款）：**70%-85%**
- **期初库存校验窗口：48-72 小时**（收货后需在 2-3 天内完成盘点与数据校准，否则 OTB 决策失真）。
- **OTB 准确率对比**：数字化管理 **0.89** vs 传统人工 **0.68**（误差率显著下降）。

## 关键机制
- 售罄率按品类属性分别设基准，避免"一刀切"考核误导企划（如 New 款天然低于 Core 款）。
- 期初库存 48-72h 校验窗口，是把"账面库存"变成"可信 OTB 输入"的关键控制点。
- 数字化 OTB 准确率 0.89 → 直接降低过量订货与季末积压风险。

## 可复用要点
- 分品类售罄率基准与 kb_benchmarks `lifecycle_sell_through.end_season_target=0.80` 高度一致（Core/Replenishment 80-90% ≥ 0.80），可作为品类细化执行的参考。
- "期初库存 48-72h 校验"是可操作的控制点，应纳入动态 OTB 作业 SOP。

## 待验证
- retailnorthstar 基准基于其客户样本，国内服装品牌需按渠道与价格带本地化校准后再固化进 kb_benchmarks。
