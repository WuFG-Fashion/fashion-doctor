---
type: source
title: aislestock：2026售罄率公式与周度基准——服装8-12%/季末60-80%
aliases: [aislestock售罄率基准, 售罄率周度基准2026, aislestock]
tags: [merchandise, inventory, sell_through, benchmark, source]
sources: [http://aislestock.com/sell-through-rate]
created: 2026-08-15
updated: 2026-08-15
cross_refs: [[sell_through_examination_standard_2026]], [[sell_through_examination_standard_2026]], [[柔性供应链与商品企划]]
confidence: 第三方数据
---

# aislestock：2026售罄率公式与周度基准——服装8-12%/季末60-80%

> **一句话摘要**：aislestock 2026 售罄率基准：公式=售出/期初收货；服装 specialty 周度 8-12%/季末 60-80%（<8% 第4周触发降价），快时尚 15-25%/85-95%，鞋类 6-10%/55-75%。
> **来源**：http://aislestock.com/sell-through-rate
> **最后更新**：2026-08-15

## 核心要点
- 公式：售罄率 = (Units Sold ÷ Units Received) × 100，窗口按品类；服装按周度 + 收货以来累计。
- 服装 specialty：周度 8-12% / 季末 60-80%（12-16 周季）；<8% 第 4 周触发降价复核。
- 快时尚：周度 15-25% / 季末 85-95%（4-6 周 SKU 寿命）；鞋类：周度 6-10% / 季末 55-75%（按 SKU 非 style 追踪尺码矩阵）。
- 决策示例：春装连衣裙第 4 周累计 16%（周度 4%）低于计划→取消追单、第 6 周软降 15-20%、缩减陈列、下季 no-buy。

## 详细内容
| 品类 | 周度目标 | 季末目标 | 备注 |
|------|----------|----------|------|
| 服装 specialty | 8-12% | 60-80% | 12-16 周季；<8% 第4周降价 |
| 快时尚 | 15-25% | 85-95% | 4-6 周 SKU 寿命 |
| 鞋类 | 6-10% | 55-75% | 尺码矩阵，按 SKU 追踪 |
| 美妆 | 10-15% | 70-90% | 季节上新 |

> 行业参考：NRF research library + 运营商演示。第 4 周案例：1200 件春装售 192（16%），周度 4%，低于 8-12% 计划。

## 结论
- 售罄率必须按 SKU/style-color-size 层级周度跟踪， blended 口径会掩盖长尾滞销（与 [[sku_fine_management]] 一致）。
- 服装 specialty 季末 60-80% 是行业基准区间，可作为 kb 季末目标 0.8 的'行业校准锚'——kb 0.8 偏进取（区间上沿）。
- 对 Fashion Doctor：太平鸟/卡宾周度售罄看板应设'<8% 第4周预警'触发器，与现有周度售罄考核对齐。

## 信息链
上游来源 [[2026-08-15_aislestock_售罄率周度基准]]（原始剪藏）→ 本页（来源摘要）→ 下游应用 [[sell_through_examination_standard_2026]] / [[sell_through_examination_standard_2026]] / [[柔性供应链与商品企划]]

## 关联页面
[[sell_through_examination_standard_2026]] / [[sell_through_examination_standard_2026]] / [[柔性供应链与商品企划]]

## 待办 / 待验证
> ⚠️ **数据矛盾**：服装 specialty 季末售罄率 60-80%（行业基准区间，上沿 80%）vs kb_benchmarks `lifecycle_sell_through.end_season_target=0.8` / `season_end_sell_through.excellent=0.7`。0.8 为本区间上沿、kb 0.8 为进取目标，属区间 vs 目标的口径差异；待验证。
