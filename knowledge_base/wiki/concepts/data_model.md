---
type: concept
title: 数据模型规范
aliases: [data_model]
tags: [data, model]
sources: []
created: 2026-06-05
updated: 2026-08-26
cross_refs: []
---

# 数据模型规范

> **分类**: L2_01 零售基础理论 > L3_01_03 数据模型规范
> **状态**: 🔄 持续迭代中
> **适用项目**: cabbeen_data / PEACEBIRD / Fashion Doctor

---

## 1. 核心表结构

### sales（销售表）

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INTEGER | 主键 | PK AUTOINCREMENT |
| date | TEXT | 销售日期 | 格式 YYYY-MM-DD |
| shop_name | TEXT | 店铺名称 | 与shops表关联 |
| sku_code | TEXT | 款号 | NOT NULL |
| color | TEXT | 颜色 | - |
| size | TEXT | 尺码 | - |
| quantity | INTEGER | 数量 | ≥0 |
| amount | REAL | 销售金额 | ≥0 |
| tag_price | REAL | 吊牌金额 | ≥0 |
| year | TEXT | 年份季 | 如 "2026夏" |
| season | TEXT | 季节 | 如 "夏" |

### inventory（库存表）

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| date | TEXT | 库存日期 | PK之一, YYYY-MM-DD |
| shop_name | TEXT | 店铺名称 | 与shops表关联 |
| sku_code | TEXT | 款号 | NOT NULL |
| qty | INTEGER | 库存数量 | ≥0 |
| tag_amount | REAL | 吊牌额合计 | ≥0 |

### arrival（到货表）

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| date | TEXT | 到货日期 | YYYY-MM-DD |
| shop_name | TEXT | 店铺名称 | - |
| sku_code | TEXT | 款号 | NOT NULL |
| qty | INTEGER | 到货数量 | ≥0 |
| arrival_type | TEXT | 到货类型 | 补货/首单/调拨 |

### shops（店铺表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| shop_id | TEXT | 店铺ID |
| short_name | TEXT | 简称（系统内使用） |
| full_name | TEXT | 全称（数据源中使用） |
| company | TEXT | 公司/品牌 |
| region | TEXT | 区域 |
| city | TEXT | 城市 |
| channel | TEXT | 渠道类型 |

---

## 2. 字段命名规范

| 规范项 | 规则 | 示例 |
|--------|------|------|
| 日期格式 | 统一 YYYY-MM-DD | 2026-05-11 |
| 金额单位 | 元（保留2位小数） | 1299.00 |
| 数量 | 整数 | 5 |
| 店铺匹配 | sales.shop_name = shops.full_name | JOIN用全称 |
| NULL处理 | 缺失值留空字符串或0 | 不用NULL |

---

## 3. 数据质量红线

- ❌ 日期字段禁止非标准格式（如 2026/5/11）
- ❌ 金额字段禁止负数（退货单独处理）
- ❌ SKU禁止空值
- ✅ 导入后必须抽样验证
- ✅ 关键指标必须与源数据交叉核对

---

## 4. 跨品牌扩展设计

当系统从单一品牌扩展到多品牌时：

```sql
-- 方案A：加brand字段（推荐，改动最小）
ALTER TABLE sales ADD COLUMN brand TEXT;
ALTER TABLE inventory ADD COLUMN brand TEXT;
ALTER TABLE arrival ADD COLUMN brand TEXT;

-- 方案B：独立schema（适合品牌间差异大的场景）
CREATE TABLE brand_sales (...);
```

## 关联知识

- [[kpi_benchmark]]
- [[terminology]]
- [[system_architecture]]
- [[brand_config]]
