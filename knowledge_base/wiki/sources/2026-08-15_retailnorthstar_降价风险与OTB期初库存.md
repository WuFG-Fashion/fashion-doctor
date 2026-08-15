---
type: source
title: retailnorthstar：服装降价风险与OTB期初库存——分类正价售罄基准
aliases: [retailnorthstar 降价风险, 服装降价风险与OTB, retailnorthstar]
tags: [merchandise, otb, markdown, sell_through, inventory, source]
sources: [https://retailnorthstar.ai/resources/research/markdown-inventory-risk-apparel]
created: 2026-08-15
updated: 2026-08-15
cross_refs: [[动态OTB管理]], [[柔性供应链与商品企划]], [[sell_through_examination_standard_2026]]
confidence: 第三方数据
---

# retailnorthstar：服装降价风险与OTB期初库存——分类正价售罄基准

> **一句话摘要**：retailnorthstar：按品类正价售罄基准（核心款 80-90%/延续时尚 65-78%/新款 60-75%/季节 70-85%）；OTB 期初库存须 48-72h 内从系统直取校验；降价归因缺口是普遍盲区。
> **来源**：https://retailnorthstar.ai/resources/research/markdown-inventory-risk-apparel
> **最后更新**：2026-08-15

## 核心要点
- 正价售罄基准（按品类）：核心/补货款 80-90%、延续时尚 65-78%、新款 60-75%、季节/场景 70-85%。
- OTB 期初库存：须从系统 of record（ERP）在规划期开始 48-72h 内直取校验，否则 OTB 虚高→超买；手工 reconciled 不可靠。
- 降价归因缺口：多数品牌按品类/渠道/季度量降价，未归因到'哪次买货决策'，季末复盘应定位 over-buy 根因。
- 健康信号：延续款售罄 < 新款售罄 是企划健康领先指标（说明新货比例/款深纪律不足）。

## 详细内容
| 品类类型 | 正价售罄目标 |
|----------|--------------|
| 核心/补货基础款 | 80-90% |
| 延续时尚款 | 65-78% |
| 新款引入 | 60-75% |
| 季节/场景款 | 70-85% |

> OTB 期初库存 recency 窗口：48-72h。未校验则 OTB 模型视为不可靠，超买风险上升。

## 结论
- 正价售罄（非 blended）才是降价风险最直接指标；retailnorthstar 的'按品类正价售罄'细化了 kb 仅有的单一季末目标。
- OTB 期初库存 48-72h 校验规则是可落地的流程护栏，对 Fashion Doctor 商品企划系统有实操价值（避免手工导出失真）。
- 对 Fashion Doctor：建议把'按品类正价售罄 + 降价归因'纳入商品企划复盘 SOP，与 [[动态OTB管理]] 联动。

## 信息链
上游来源 [[2026-08-15_retailnorthstar_降价风险与OTB期初库存]]（原始剪藏）→ 本页（来源摘要）→ 下游应用 [[动态OTB管理]] / [[柔性供应链与商品企划]] / [[sell_through_examination_standard_2026]]

## 关联页面
[[动态OTB管理]] / [[柔性供应链与商品企划]] / [[sell_through_examination_standard_2026]]

## 待办 / 待验证
> ⚠️ **数据矛盾**：新款正价售罄 60-75% 在 kb `lifecycle_sell_through.normal_sale_range=[0.5,0.8]` 内、核心款 80-90% 与 kb `hot_sale_min=0.8` 一致，无硬冲突。注：retailnorthstar 提供 kb 尚未固化的'按品类正价售罄'细分基准，建议下轮补入 kb_benchmarks（markdown_inventory_risk 分组）。
