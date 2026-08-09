---
type: practice
title: 数据质量零售实操规范
tags: [data_quality, retail, sql, validation, anomaly_detection]
sources: [L3_06_01_数据质量红线, 2026-06-08_2026企业数据质量五阶段管控]
created: 2026-06-08
updated: 2026-06-08
cross_refs: [[data_quality_governance]], [[零售数据仓库SQL实践]], [[SQL查询性能优化]], [[ETL架构选型]], [[2026-08-03_AI驱动数据质量管理_从规则到智能预防]], [[2026-08-03_服装零售指标口径统一与进销存SQL]]
---

# 数据质量零售实操规范

> **一句话摘要**：基于Fashion Doctor项目踩坑记录总结的零售数据质量实操手册，覆盖字段红线/JOIN规范/日期处理/导入校验/异常检测五大模块，可直接复制使用。

> **来源**：Fashion Doctor项目实践 + L3_06_01数据质量红线

## 一、字段使用红线

### barcode字段

| 合法用途 | 禁止场景 |
|---------|---------|
| `SUBSTR(barcode, -2)` 提取尺码 | 款号/款色/SKU判定 |
| | JOIN条件 |
| | 过滤/分组 |

### 统一款色标识

```sql
-- ✅ 正确：使用 style_color
SELECT style_color, SUM(amount) FROM sales GROUP BY style_color;

-- ❌ 错误：使用 barcode、style_code 等
SELECT barcode, SUM(amount) FROM sales GROUP BY barcode;
```

## 二、JOIN规范

| 表 | JOIN条件 | 原因 |
|---|---------|------|
| sales | `sales.shop_name = shops.short_name` | sales存简称 |
| inventory | `inventory.shop_name = shops.short_name` | 同上 |
| arrival | `arrival.receiver_name = shops.short_name` | 接收人即店铺 |

### 字段名映射

| 实际字段 | 用途 | 常见错误 |
|---------|------|---------|
| `sales.shop_name` | 店铺简称 | 误用full_name |
| `sales.sale_date` | 销售日期 | 误用date |
| `sales.amount` | 销售金额 | 误用revenue |
| `inventory.snapshot_date` | 库存快照日期 | 误用date |

## 三、日期处理规范

```sql
-- ✅ SQLite：显式转换日期
SELECT * FROM sales 
WHERE sale_date >= '2026-01-01' AND sale_date <= '2026-04-29';
```

```python
# ✅ Python：使用 relativedelta 避免闰年问题
from dateutil.relativedelta import relativedelta
end_date = start_date + relativedelta(months=1)

# ❌ 错误：2月29日→报错
date.replace(year=year+1)
```

## 四、数据导入检查清单

### 导入前
```
□ 日期格式统一为 YYYY-MM-DD
□ 数值字段无千分位逗号
□ 无全角字符混入
□ 中文逗号检查（'，' vs ','）
□ 空值统一为 NULL
```

### 导入后验证
```sql
-- 1. 日期范围检查
SELECT MIN(sale_date), MAX(sale_date) FROM sales;

-- 2. 关键字段非空检查
SELECT COUNT(*) FROM sales WHERE shop_name IS NULL;

-- 3. 抽样对比
SELECT * FROM sales ORDER BY ROWID LIMIT 10;
```

## 五、异常数据识别

| 异常类型 | 识别方法 | 处理方式 |
|---------|---------|---------|
| 日期超出范围 | `WHERE sale_date > '2026-06-08'` | 标记待核实 |
| 负数金额 | `WHERE amount < 0` | 退货/冲销，需保留 |
| 超高单价 | `WHERE amount > 50000` | 团单/定制，需核实 |
| 重复记录 | `GROUP BY + HAVING COUNT>1` | 去重或合并 |

## 六、数据质量监控SQL模板

```sql
-- 完整性检查：核心字段空值率
SELECT 
    'shop_name' as field,
    ROUND(100.0*SUM(CASE WHEN shop_name IS NULL THEN 1 ELSE 0 END)/COUNT(*), 2) as null_pct
FROM sales
UNION ALL
SELECT 'amount', ROUND(100.0*SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)/COUNT(*), 2)
FROM sales;

-- 唯一性检查：订单号重复
SELECT order_id, COUNT(*) as cnt
FROM sales
GROUP BY order_id
HAVING cnt > 1;

-- 时效性检查：最新数据日期
SELECT MAX(sale_date) as latest_date,
       JULIANDAY('now') - JULIANDAY(MAX(sale_date)) as days_lag
FROM sales;
```

## 七、置信度评估标准

| 置信度 | 条件 | 输出标注 |
|--------|------|---------|
| **high** | 索引命中+多源验证 | ✅ |
| **medium** | 单源内容 | ⚠️ |
| **low** | 推断/估算 | 🔶 |
| **unverified** | 用户提供未核实 | ⚠️ |

## 关联知识

- [[data_quality_governance|数据质量常态化治理]]
- [[零售数据仓库SQL实践]]
- [[SQL查询性能优化]]
- [[ETL架构选型]]
- [[multi_brand_unified_analytics]]

## 关联页面

- [[2026-06-06_FineDataLink_ETL数据仓库选型]]
- [[2026-06-08_2026企业数据质量五阶段管控]]
- [[2026-06-30_GeeksForGeeks_SQL查询优化十大实践2026]]
- [[2026-07-09_DevTo_PostgreSQL_2026性能调优]]
