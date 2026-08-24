---
type: source
title: DTC全渠道库存优化六项健康基准（Green Retail Consulting）
tags: [merchandise, inventory, otb, sell_through, wos, markdown, source]
sources: [2026-08-05_GreenRetail_DTC全渠道库存优化六项健康基准]
aliases: ["DTC全渠道库存优化六项健康基准（Green", "Retail", "Consulting）", "DTC全渠道库存优化六项健康基准（Green Retail Consulting）"]
confidence: 媒体估算
brand_specific: false
created: 2026-08-05
updated: 2026-08-05
cross_refs: [[动态OTB管理]], [[柔性供应链与商品企划]], [[sku_fine_management|服装SKU精细化管理]]
---

# DTC全渠道库存优化六项健康基准（Green Retail Consulting）

> 一句话摘要：Green Retail 为客户实现平均库存改善28%；提出六项健康基准——季末售罄率80%+、WOS 6-8周、周转4-6次/年、在库率95%+、折扣率<20%、OTB按销售预测编制；并给出六步实操（审计SKU→精简货盘→需求预测→设定OTB→每周复盘→提前规划折扣）。

> 来源：Green Retail Consulting（greenretailconsulting.com/blog/retail-inventory-optimization-the-complete-guide-for-dtc-and-omnichannel-brands）；采集 2026-08-05（Round B / L2_05 商品企划）

## 核心要点

1. **库存是最大单项资产**：2000万美元以下营收品牌多为"被动管理"而非"战略管理"。
2. **六项健康基准**（见下表）：售罄率季末80%+、WOS 6-8周、周转4-6次/年、在库率95%+、折扣率<20%、OTB按预测编制。
3. **OTB是多数品牌缺失的一环**：大型零售标准做法，1000万美元以下DTC品牌几乎完全缺失；构建基础OTB模型无需复杂软件，一张每周更新的表格即可交付企业级规划80%的纪律性。
4. **20-30% SKU贡献70-80%利润**：审计货盘时多数品牌发现少数SKU贡献绝大部分利润，其余稀释现金与注意力。

## 关键数据（六项健康基准）

| 指标 | 衡量内容 | 健康基准 |
|------|---------|---------|
| Sell-through 售罄率 | 期内已售/已收货 | 季末 80%+ |
| Weeks of supply (WOS) | 当前库存可支撑周数 | 多数品类 6–8 周 |
| Inventory turn 周转 | 年售出并补充次数 | DTC服装 4–6 次/年 |
| In-stock rate 在库率 | 可售SKU占比 | 在售货盘 95%+ |
| Markdown rate 折扣率 | 打折销售额占比 | 健康毛利品牌 <20% |
| Open-to-buy (OTB) | 周期可用采购预算 | 按销售预测编制 |

## 六步实操流程

1. 审计当前SKU表现（按售罄率与毛利贡献排序）
2. 精简货盘（退出/改造/继续低效SKU，释放OTB）
3. 按品类建立需求预测（品类级历史售罄率 + 营销/季节/趋势信号）
4. 按周期设定OTB目标（销售预测与期初库存位置 → 采买约束线）
5. 执行每周复盘（SKU级售罄率/在库率/WOS）
6. 提前规划折扣策略（季初定义售罄率触发阈值、折扣深度、执行渠道）

## 关联页面

- [[动态OTB管理]] — 六步流程第4步"设定OTB目标"与本知识库OTB体系直接对应
- [[柔性供应链与商品企划]] — 售罄率/WOS/周转基准是商品企划的健康标尺
- [[sku_fine_management|服装SKU精细化管理]] — "20-30% SKU贡献70-80%利润"与ABC分类逻辑一致

## 待办 / 待验证

- 基准源自欧美DTC/omnichannel品牌，服装零售可参照；季末售罄率80%+ 与 kb_benchmarks `lifecycle_sell_through.end_season_target=0.8` 一致 ✓。
- "20-30% SKU贡献70-80%利润"为利润口径，与 kb `sku_abc.a_class_sales_contribution=0.65`（销售贡献）口径不同，不冲突。
