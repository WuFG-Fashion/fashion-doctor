---
type: concept
title: 未动销库存量占比
aliases: [dead_stock]
tags: [inventory, kpi, dead, stock]
sources: []
created: 2026-06-05
updated: 2026-08-26
cross_refs: []
layer: T1
scope: public
volatility: evergreen
as_of: 2026-08-26
review_due_at: 2027-02-22
status: active
---
# 未动销库存量占比

## 定义

未动销库存量占比（又称滞销率、Dead Stock Rate），指在统计周期内零销售的库存占总库存的比例。

> **核心原则**：必须匹配当年当季货品，否则旧货稀释分母，未动销率永远低不下来。

## 标准公式

```
未动销率 = 当年当季统计周期内零销售的库存量 / 当年当季总库存量 × 100%
```

## 关键维度

| 维度 | 说明 |
|------|------|
| 货品范围 | 当年当季（不含跨季货品、旧年度货品） |
| 滞销判定 | 以库存快照日期为基准，向前追溯N天无销售记录 |
| N值选择 | 60天（激进）/ 90天（标准）/ 180天（保守） |

## 常见口径对比

| 口径 | 适用场景 |
|------|---------|
| 60天未动销 | 快时尚、高频上新品牌 |
| 90天未动销 | 标准服装品牌（行业通用） |
| 180天未动销 | 奢品、高客单价品牌 |

## SQL计算逻辑

```sql
-- 以90天为例，看2026年夏季货品
WITH current_stock AS (
    -- 当年当季库存快照
    SELECT i.style_color, i.shop_name, SUM(i.stock_qty) AS stock_qty
    FROM inventory i
    JOIN shops s ON i.shop_name = s.short_name
    WHERE i.year = 2026 
      AND i.season = '夏'
      AND i.snapshot_date = (SELECT MAX(snapshot_date) FROM inventory)
    GROUP BY i.style_color, i.shop_name
),
sold_items AS (
    -- 当年当季有销售的SKU
    SELECT style_color, shop_name, SUM(qty) AS sold_qty
    FROM sales
    WHERE year = 2026 AND season = '夏'
      AND sale_date >= DATE('now', '-90 days')
    GROUP BY style_color, shop_name
)
SELECT 
    COUNT(DISTINCT cs.style_color) AS total_skus,
    COUNT(DISTINCT CASE WHEN si.style_color IS NULL THEN cs.style_color END) AS dead_skus,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN si.style_color IS NULL THEN cs.style_color END) 
          / COUNT(DISTINCT cs.style_color), 2) AS dead_stock_rate
FROM current_stock cs
LEFT JOIN sold_items si ON cs.style_color = si.style_color 
                       AND cs.shop_name = si.shop_name;
```

## 与售罄率的关系

| 指标 | 公式 | 关注点 |
|------|------|-------|
| 售罄率 | 销售吊牌额 / (销售吊牌额 + 库存吊牌额) × 100% | 已卖出多少 |
| 未动销率 | 零销售库存 / 总库存 × 100% | 卖不动多少 |

两者结合看：
- 售罄率高 + 未动销率低 = 健康
- 售罄率高 + 未动销率高 = 部分SKU爆款，部分死透
- 售罄率低 + 未动销率高 = 全面滞销

## 行业基准参考

| 品牌类型 | 90天未动销率健康值 |
|---------|------------------|
| 快时尚 | < 20% |
| 大众男装 | < 30% |
| 大众女装 | < 35% |
| 奢品/高客单 | < 50% |

## 常见误区

1. **用全年份全季节做分母** → 旧货早已清掉，稀释分母，数据失真
2. **只看件数不看SKU** → 单件大库存 vs 多SKU小库存，结果完全不同
3. **不区分店铺** → 直营好店掩盖加盟滞销问题

## 来源

Fashion Doctor 实操经验，2026-04-29 确认口径。

## 关联知识

- [[kpi_benchmark]]
- [[data_quality]]
- [[sku_lifecycle]]

- [[2026-09-04_B_季末清仓分级折扣与节奏管理]]

## 结论

死库存是"沉默的成本"——它不进损益表的一次性损失，却持续占用库位、资金与陈列效率。判定死库存的关键不是"卖得慢"，而是"在剩余生命周期内以任何折扣都难以售出"，因此必须结合[[sku_lifecycle]]的剩余窗口与[[kpi_benchmark]]的周转红线共同判定，单看周转天数会误杀慢销的季节品。

## 信息链

[[2026-09-04_B_季末清仓分级折扣与节奏管理]] → 本页 → [[kpi_benchmark]] · [[data_quality]] · [[sku_lifecycle]]

## 前沿

1. 明确"死库存"与"慢销"的量化分界（建议以剩余生命周期售出概率为判据）；2. 补充分级清仓的折扣-回收率实证曲线。
