# 时尚零售商季节库存计划（STR/WOC/OTB/GMROI六大指标）

- 来源: https://www.easyreplenish.com/blog/seasonal-inventory-planning-fashion
- 采集日期: 2026-08-13
- 主题: 商品企划 / 季节库存 / 售罄率 / 周转 / GMROI

## 核心要点

1. **六大核心指标**
   - **Sell-Through Rate (STR)** = 售出单位 ÷ 收货单位。核心季款式健康区间 **65–85%**，限量款趋高；持续 <50% 为 overbought，第 1 周就 95%+ 为 underbought。
   - **Weeks of Cover (WOC)** = 当前库存 ÷ 周均销售；WOC 超过剩余季周数→该 SKU 将成 overstock，应在窗口关闭前促销/调拨/降价。
   - **Open-to-Buy (OTB)** = 计划销售 + 计划 markdown + 计划期末库存 − 期初库存；连接季节预测与实际采购的预算纪律。
   - **Inventory Turnover** = COGS ÷ 平均库存成本；时尚电商约 10–12x/年，实体更低。
   - **Stockout Rate**：平衡规划品牌比被动管理品牌缺货风险低至多 18%。
   - **GMROI** = 毛利 ÷ 平均库存成本；STR 高但毛利薄、周转慢仍可能是弱 GMROI。

2. **季节采购量公式**：预测需求 + 安全库存 − 现有库存 = 季节采购量（例：预测 1000 + 安全 100 − 现有 50 = 1050）。

3. **自检验收**：多数"是否做对"问题可归约为对基准的 pass/fail——STR 65–85% 趋高、WOC 贴合剩余季长、畅销款缺货率低且稳定、markdown 提前计划、库存分析工时用于例外处理、季末复盘改变下季买深。

4. **七组件缺口**：反复出错多在 allocation / replenishment 触发 / review loop，而非预测本身。

## 备注

- 时尚零售专属基准，STR 65–85% 与 kb `lifecycle_sell_through.end_season_target=0.80`、`season_end_sell_through.excellent=0.70` 一致（0.80 落在区间内）；与 [[动态OTB管理]]、[[柔性供应链与商品企划]] 互补。
