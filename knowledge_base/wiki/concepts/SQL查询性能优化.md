---
type: concept
title: SQL查询性能优化
tags: [sql, optimization, mysql, performance, retail_data]
sources: [2026-06-06_腾讯云社区_MySQL查询优化, 2026-06-06_百度开发者_SQL优化实战]
created: 2026-06-06
updated: 2026-06-06
cross_refs: [[零售数据仓库SQL实践]], [[数据质量红线]], [[ETL架构选型]]
---

# SQL查询性能优化

> **一句话**：通过索引设计、SQL改写和参数调优三大维度，可实现零售数据查询10-40倍性能提升。

## 核心要点

1. 索引+SQL改写占优化效果的70%（IEEE研究），是第一优先级
2. 复合索引最左前缀原则是零售多维查询优化的核心规则
3. 零售BI场景：百万级销售记录查询可从3.2秒优化到0.08秒
4. EXPLAIN的type字段至少要达到range级别，Using filesort/temporary是红线
5. 分页优化（延迟关联）和大表JOIN（小表驱动大表）直接解决零售看板性能瓶颈

## 详细内容

### 优化三维度

| 维度 | 核心技术 | 零售场景 |
|------|---------|---------|
| 索引优化 | 复合索引、覆盖索引、索引选择性 | 销售表(shop_id, sale_date, category)复合索引 |
| SQL改写 | 子查询→JOIN、UNION ALL、延迟关联 | 库存快照查询、会员RFM计算 |
| 参数调优 | buffer pool、连接池、查询缓存 | 多品牌多数据库实例配置 |

### EXPLAIN关键字段

| 字段 | 优秀 | 警告 | 危险 |
|------|------|------|------|
| type | const/eq_ref/ref | range/index | ALL |
| rows | <1000 | 1000-10000 | >10000 |
| Extra | Using index | Using where | Using filesort/temporary |

### 服装零售高频查询优化模板

```sql
-- 销售日报（优化前：全表扫描）
-- 优化后：复合索引 (shop_id, sale_date)
SELECT shop_id, sale_date, SUM(amount)
FROM sales
WHERE sale_date BETWEEN '2026-06-01' AND '2026-06-06'
  AND shop_id IN (SELECT shop_id FROM shops WHERE region='华东')
GROUP BY shop_id, sale_date;
```

### 性能基准

| 数据量 | 优化前 | 优化后 | 提升 |
|--------|--------|--------|------|
| 10万行 | 0.5s | 0.05s | 10x |
| 100万行 | 3.2s | 0.08s | 40x |
| 1000万行 | 30s+ | 0.5s | 60x+ |

## 关联知识
- [[零售数据仓库SQL实践]]
- [[数据质量红线]]
- [[ETL架构选型]]
- [[多品牌数据系统架构]]
