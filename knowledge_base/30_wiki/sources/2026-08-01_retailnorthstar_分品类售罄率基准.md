---
type: source
title: retailnorthstar——分品类正价售罄率基准与期初库存校验
tags: [sell_through, merchandise, inventory, otb, benchmark, risk]
sources: [2026-08-01_retailnorthstar_分品类售罄率基准]
aliases: ["retailnorthstar", "分品类正价售罄率基准与期初库存校验", "retailnorthstar——分品类正价售罄率基准与期初库存校验"]
confidence: 第三方数据
brand_specific: false
created: 2026-08-01
updated: 2026-08-01
cross_refs: [[动态OTB管理]], [[柔性供应链与商品企划]], [[服装企划趋势渠道]], [[sell_through_examination_standard_2026|售罄率考核基准2026]]
layer: T2
scope: public
volatility: fast
as_of: 2026-08-01
expires_at: 2026-10-30
status: active
---
# retailnorthstar——分品类正价售罄率基准与期初库存校验

> 一句话摘要：分品类正价售罄率基准（Core/Replenishment 80-90%/Carry-over 65-78%/New 60-75%/Seasonal 70-85%），期初库存48-72h校验窗口，数字化OTB准确率0.89 vs 传统0.68。
> 来源：retailnorthstar.ai（Markdown & Inventory Risk）
> 最后更新：2026-08-01

## 核心要点
- 分品类正价售罄率基准：Core/Replenishment 80-90%、Carry-over 65-78%、New 60-75%、Seasonal 70-85%。
- 期初库存校验窗口 48-72 小时：收货后 2-3 天内完成盘点校准，否则 OTB 决策失真。
- OTB 准确率：数字化 0.89 vs 传统人工 0.68。

## 关键数据
| 指标 | 数据 |
|------|------|
| Core/Replenishment 售罄率 | 80%-90% |
| Carry-over 售罄率 | 65%-78% |
| New 售罄率 | 60%-75% |
| Seasonal 售罄率 | 70%-85% |
| 期初库存校验窗口 | 48-72 小时 |
| OTB准确率（数字化/传统） | 0.89 / 0.68 |

## 结论

本页给出分品类正价售罄率基准：Core/Replenishment 80%–90%、Carry-over 65%–78%、New 60%–75%、Seasonal 70%–85%。其使用要点是——售罄率必须分品类设定目标，统一目标会导致补货型核心款被低估而新品类被高估。另有两个关键工程参数：期初库存校验窗口 48–72 小时（收货后 2–3 天内必须完成盘点校准，否则 OTB 决策失真）、OTB 准确率数字化 0.89 vs 传统人工 0.68。其中期初库存校验窗口是最容易被忽视的隐性风险点——若期初库存数据不准，后续所有 OTB 计算都建立在错误基数上。

## 信息链

上游来源 [[2026-08-01_retailnorthstar_分品类售罄率基准]] → 本页（分品类售罄率基准 + 期初库存校验窗口） → 下游应用 [[动态OTB管理]]、[[apparel_inventory_benchmark_2026]]

## 关联页面
- [[动态OTB管理]]（期初库存48-72h校验、OTB准确率）
- [[柔性供应链与商品企划]]（库存风险、分品类售罄基准）
- [[服装企划趋势渠道]]（品类结构规划视角）
- [[sell_through_examination_standard_2026|售罄率考核基准2026]]（基准线对齐）


- [[2026-08-07_retailnorthstar_SKU合理化五步减法与复杂度五区间]]
## 待办/待验证
- 基准基于 retailnorthstar 客户样本，国内服装品牌需按渠道/价格带本地化校准后再固化进 kb_benchmarks。

## 前沿

待校准：基准基于 retailnorthstar 客户样本，国内服装品牌需按渠道/价格带本地化校准后再固化进 kb_benchmarks。
