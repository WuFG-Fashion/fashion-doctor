---
type: practice
title: 服装SKU进销存管理实操
aliases:
  - "sku inventory sql operations"
tags: [sku, inventory, replenishment, practice, sql]
created: 2026-06-06
updated: 2026-06-21
sources:
  - 2026-06-06_简道云_服装SKU进销存管理
cross_refs: [[sku_fine_management|服装SKU精细化管理]], [[SQL查询性能优化]], [[动态OTB管理]], [[2026-01-28_搜狐_服装库存破局双轨制与ESG合规]], [[2026-05-07_新浪财经_永辉SKU优化调改实践]], [[2026-08-03_服装零售指标口径统一与进销存SQL]]
layer: T1
scope: public
volatility: evergreen
as_of: 2026-06-21
review_due_at: 2026-12-18
status: active
---
# 服装SKU进销存管理实操

> **一句话摘要**：服装SKU进销存管理的完整实操框架——从SKU编码规范、ABC分类自动计算、安全库存公式、畅滞款SQL识别，到8维度补货决策的端到端落地指南。

## 一、SKU编码规范

```
推荐格式：品类-季节-款号-颜色-尺码
示例：TS-24SS-1023-BK-M
```

| 段位 | 含义 | 长度 | 示例 |
|------|------|------|------|
| 品类 | 产品大类 | 2-3位 | TS=T恤, JK=夹克 |
| 季节 | 上市季 | 4位 | 24SS=2024春夏 |
| 款号 | 唯一款式 | 4-6位 | 1023 |
| 颜色 | 颜色编码 | 2位 | BK=黑色 |
| 尺码 | 尺码 | 1-2位 | M=中码 |

## 二、ABC分类SQL

```sql
-- 按月计算ABC分类
WITH sku_sales AS (
    SELECT 
        sku_id,
        SUM(sales_amount) as total_sales,
        SUM(sales_amount) / SUM(SUM(sales_amount)) OVER() as sales_pct,
        SUM(SUM(sales_amount)) OVER(ORDER BY SUM(sales_amount) DESC) 
            / SUM(SUM(sales_amount)) OVER() as cumulative_pct
    FROM sales
    WHERE sale_date >= date('now', '-3 months')
    GROUP BY sku_id
)
SELECT 
    sku_id,
    total_sales,
    CASE 
        WHEN cumulative_pct <= 0.70 THEN 'A'
        WHEN cumulative_pct <= 0.90 THEN 'B'
        ELSE 'C'
    END as abc_class
FROM sku_sales;
```

## 三、安全库存计算

```python
def calc_safety_stock(max_daily_sales, max_replenish_days, 
                       avg_daily_sales, avg_replenish_days):
    """安全库存量 = 最大日销量 × 最大补货时间 - 平均日销量 × 平均补货时间"""
    return max_daily_sales * max_replenish_days - avg_daily_sales * avg_replenish_days

def calc_reorder_point(safety_stock, in_transit_consumption):
    """补货点 = 安全库存 + 预计在途消耗"""
    return safety_stock + in_transit_consumption
```

## 四、滞销款SQL识别

```sql
-- 识别滞销SKU：30天无销售 或 60天低于阈值
SELECT 
    i.sku_id,
    i.sku_name,
    i.current_stock,
    COALESCE(s.sales_30d, 0) as sales_30d,
    COALESCE(s.sales_60d, 0) as sales_60d,
    CASE 
        WHEN COALESCE(s.sales_30d, 0) = 0 THEN 'red_30day_zero'
        WHEN COALESCE(s.sales_60d, 0) < i.slow_sales_threshold THEN 'orange_60day_low'
        ELSE 'normal'
    END as status
FROM inventory i
LEFT JOIN (
    SELECT sku_id,
        SUM(CASE WHEN sale_date >= date('now', '-30 days') THEN quantity ELSE 0 END) as sales_30d,
        SUM(CASE WHEN sale_date >= date('now', '-60 days') THEN quantity ELSE 0 END) as sales_60d
    FROM sales
    GROUP BY sku_id
) s ON i.sku_id = s.sku_id
WHERE i.current_stock > 0
ORDER BY sales_30d ASC;
```

## 五、库存健康看板指标

| 指标 | SQL/公式 | 告警阈值 |
|------|----------|---------|
| 库存周转率 | 销售额/平均库存额 | <3次/年 |
| 售罄率 | 销量/备货量×100% | <30%@30天 |
| 动销率 | 有销售SKU数/总SKU数 | <60% |
| 断码率 | 尺码不完整SKU/总SKU | >15% |
| 库销比 | 库存额/月销售额 | >3:1 |

## 关联知识
- [[sku_fine_management|服装SKU精细化管理]]
- [[SQL查询性能优化]]
- [[动态OTB管理]]
- [[零售数据仓库SQL实践]]

## 关联页面

- [[2026-08-26_服装全渠道BI看板三层角色设计与零售库存分析KPI]]
- [[retail_bi_three_tier_dashboard]]
- [[2026-09-03_服装库存分析四层拆解与售罄率库龄交叉法]]
- [[cabbeen_brand_analytics_2026]]

## 结论

1. SKU 库存查询的**性能关键在于"以快照日期为锚"**：库存是时点数据，任何未固定 `snapshot_date` 的查询都会产生重复计数——这是库存类 SQL 最高频的错误来源。
2. 与 [[dead_stock]] 的口径强绑定：未动销率必须"匹配当年当季"，因此本页的 SQL 模式必须携带 `year`/`season` 过滤，否则分母被旧货稀释，指标永远偏低——**口径正确性优先于查询性能**。
3. 库龄、周转、未动销三类查询共享同一套表结构（inventory/sales/arrival/shops，见 [[data_model]]），差异只在聚合维度（店铺/品类/款色码），因此可以抽象为一组参数化模板而非各写一遍。
4. 落地纪律：库存查询必须**区分店铺**输出，汇总数会掩盖单店滞销——这一点在 [[dead_stock]] 的"常见误区"中已被明确列为错误做法。

## 信息链

- 上游来源：[[data_model]]（inventory/sales/arrival 表结构） · [[dead_stock]]（未动销率口径） · [[sku_lifecycle]] → 本页（[[sku_inventory_sql_operations]]）→ 下游应用：[[零售数据仓库SQL实践]] · [[multi_brand_unified_analytics]] · [[kpi_benchmark]]

## 前沿

1. **待补**：本页缺少**款-色-码粒度**的查询模板——SKU 在服装场景下是"款+色+码"，而本页示例多停在款号层，未覆盖最小配货单元的查询。
2. **待验证**：跨季货品（旧年度库存）在库龄计算中是否应单独成组——若与当年当季混算，库龄分布会被长尾扭曲，影响清仓决策。
