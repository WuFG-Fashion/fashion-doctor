---
type: practice
title: 零售数据仓库SQL实践
tags: [sql, optimization, retail_data, data_warehouse, practice]
sources: [2026-06-06_腾讯云社区_MySQL查询优化, 2026-06-06_百度开发者_SQL优化实战]
created: 2026-06-06
updated: 2026-06-06
cross_refs: [[SQL查询性能优化]], [[数据质量红线]], [[ETL架构选型]]
---

# 零售数据仓库SQL实践

> **一句话**：面向服装零售场景（销售/库存/会员/导购）的SQL优化实践方法论，从索引设计到查询改写，实现BI看板秒级响应。

## 核心要点

1. 销售表按(shop_id, sale_date, category)建立复合索引，日/周/月报查询提速10-40倍
2. 库存快照使用覆盖索引避免回表，SKU×门店×时间三维查询从秒级到毫秒级
3. 会员RFM计算使用窗口函数替代自连接，百万级会员计算从分钟级到秒级
4. 导购排名使用物化视图预计算，排行榜实时刷新
5. 所有聚合查询必须设置合理的WHERE过滤范围，避免全表扫描

## 详细内容

### 场景一：销售日报优化

```sql
-- ❌ 优化前：全表扫描
SELECT shop_id, SUM(amount), COUNT(DISTINCT customer_id)
FROM sales
WHERE sale_date BETWEEN '2026-06-01' AND '2026-06-06'
GROUP BY shop_id;

-- ✅ 优化后：复合索引 (shop_id, sale_date) + 覆盖索引
-- 索引：CREATE INDEX idx_shop_date_amt ON sales(shop_id, sale_date, amount, customer_id);
-- EXPLAIN type=range, rows<10000
```

### 场景二：库存快照查询

```sql
-- ❌ 优化前：多表JOIN全表扫描
SELECT i.sku_id, i.shop_id, i.stock_qty, s.shop_name
FROM inventory i
JOIN shops s ON i.shop_id = s.id
WHERE i.snapshot_date = '2026-06-06';

-- ✅ 优化后：驱动表使用索引 + 小表驱动大表
-- 索引：CREATE INDEX idx_inv_date_shop ON inventory(snapshot_date, shop_id, sku_id, stock_qty);
-- 确保 shops 表足够小，作为驱动表
```

### 场景三：会员RFM计算

```sql
-- ✅ 使用窗口函数替代自连接
SELECT customer_id,
       DATEDIFF('2026-06-06', MAX(sale_date)) AS recency,
       COUNT(DISTINCT sale_date) AS frequency,
       SUM(amount) AS monetary,
       NTILE(5) OVER (ORDER BY DATEDIFF('2026-06-06', MAX(sale_date)) DESC) AS r_score,
       NTILE(5) OVER (ORDER BY COUNT(DISTINCT sale_date)) AS f_score,
       NTILE(5) OVER (ORDER BY SUM(amount)) AS m_score
FROM sales
WHERE sale_date BETWEEN '2025-06-06' AND '2026-06-06'
GROUP BY customer_id;
```

### 场景四：数据质量监控SQL

```sql
-- 每日数据质量检查
-- 检查空值率
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) AS null_amount,
  ROUND(SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS null_rate
FROM sales
WHERE sale_date = '2026-06-06';
```

### 性能基线

| 查询场景 | 数据量 | 优化前 | 优化后 | 索引策略 |
|---------|--------|--------|--------|---------|
| 日销售汇总 | 10万行 | 0.5s | 0.05s | 复合索引(shop,date) |
| 周销售汇总 | 100万行 | 3.2s | 0.08s | 复合索引+覆盖 |
| 月销售汇总 | 500万行 | 15s | 0.5s | 分区表+复合索引 |
| 库存快照 | 200万行 | 8s | 0.2s | 覆盖索引(date,shop,sku) |
| RFM计算 | 100万会员 | 120s | 3s | 窗口函数+索引 |

## 关联知识
- [[SQL查询性能优化]]
- [[数据质量红线]]
- [[ETL架构选型]]
- [[多品牌数据系统架构]]
