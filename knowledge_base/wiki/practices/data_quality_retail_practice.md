---
type: practice
title: 数据质量零售实操规范
aliases:
  - "data quality retail practice"
tags: [data_quality, retail, sql, validation, anomaly_detection]
sources: [L3_06_01_数据质量红线, 2026-06-08_2026企业数据质量五阶段管控, 2026-08-15_语义层与数据契约治理2026, 2026-08-15_主动元数据与多品牌数据目录2026, 2026-08-26_多品牌零售数据中台与全域用户治理实践2026]
created: 2026-06-08
updated: 2026-08-26
cross_refs: [[data_quality_governance]], [[零售数据仓库SQL实践]], [[SQL查询性能优化]], [[ETL架构选型]], [[2026-08-03_AI驱动数据质量管理_从规则到智能预防]], [[2026-08-03_服装零售指标口径统一与进销存SQL]], [[2026-08-09_Melissa信通院_零售数据质量2026可信度基准]], [[2026-08-15_语义层与数据契约治理2026]], [[2026-08-15_主动元数据与多品牌数据目录2026]], [[2026-08-26_多品牌零售数据中台与全域用户治理实践2026]]
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

## 2026 情境可信度基准阈值（2026-08新增）⭐

> 来源：[[2026-08-09_Melissa信通院_零售数据质量2026可信度基准]]

在现有字段红线/JOIN 规范基础上，补入信通院 2026 DQS 量化阈值，作为导入后验证的合格线：

| 维度 | 校验项 | 2026 基准 |
|------|--------|----------|
| 完整性 | 核心字段（shop_name/amount/sale_date/style_color）非空率 | **≥ 99.5%** |
| 准确性 | 金额/数量校验通过率 | **≥ 99.9%** |
| 一致性 | 跨系统（POS/ERP/WMS）同指标差异率 | **≤ 0.1%** |
| 及时性 | 数据 T+0 更新占比 | **≥ 80%** |
| 零售硬指标 | 库存预测偏差 | **≤ 10%** |

**实践衔接**：把"期末库存/售罄率/断码率"等高频口径做成**只读视图 + 契约校验**（对应 [[data_quality_governance]] 的 Data Contracts 源头负责制），避免部门口径分裂；异常监控清单（库存负数/超安全库存/长期零销量）可直接转为 AI 可复用规则模板。

## 2026-08-15 更新（契约 + 语义层落地零售质量）

- 零售数据质量实操新增「契约前置」环节：源表 freshness/非空/唯一/取值域在入库即断言，破坏性变更 CI 拦截而非上线后人工发现；语义层保证售罄率/毛利率/周转跨表同义。
- 来源：[[2026-08-15_语义层与数据契约治理2026]]

## 2026-08-15 更新（主动元数据 + 信任分落地零售）

- 零售质量实操新增「主动元数据」环节：敏感列自动脱敏、信任分(Trust Score)随资产编目展示、schema drift/量异常在入库前拦截。
- 来源：[[2026-08-15_主动元数据与多品牌数据目录2026]]

## 关联页面
- [[2026-08-15_主动元数据与多品牌数据目录2026]]
- [[2026-08-15_语义层与数据契约治理2026]]

- [[2026-06-06_FineDataLink_ETL数据仓库选型]]
- [[2026-06-08_2026企业数据质量五阶段管控]]
- [[2026-06-30_GeeksForGeeks_SQL查询优化十大实践2026]]
- [[2026-07-09_DevTo_PostgreSQL_2026性能调优]]


- [[2026-08-26_服装全渠道BI看板三层角色设计与零售库存分析KPI]]
- [[2026-09-03_零售BI分角色看板与KPI基准2026]]

## C轮更新（2026-08-26）：零售全域治理四层 + 质量前置

> 来源：[[2026-08-26_多品牌零售数据中台与全域用户治理实践2026]]

### 治理四层范式（对齐 ETLCloud ODS-STG-DWS-API）

| 层 | 职责 | 质量动作 |
|---|---|---|
| ODS 原始层 | CDC binlog 无侵入增量落地 | 完整留存原始变更日志，不做加工（保溯源） |
| STG 清洗层 | 标准化/去重/补全/脱敏/ID 归一化 | 统一编码 + 脏数据过滤（手机号格式/重复测试账号/无效埋点） |
| DWS 宽表层 | OneID 聚合全维度标签 | 用户标签一致性校验（消费/浏览/互动/到访/优惠券） |
| API 输出层 | 画像/圈选/会员校验接口 | 接口级质量校验 + 血缘可追溯 |

- 案例基线：86 家门店/120 万会员的连锁集团，自研脚本需每月 3 名数据工程师清脏数据、标签延迟 24h+；四层平台化后秒级同步、自动化清洗。
- **治理左移**强化：质量动作前置到 STG 清洗层（入库前拦截），而非在 API 输出层补救——与既有"入库前拦截"主张一致。

### 与既有规范的关系

- 本页原有五模块（字段红线/JOIN 规范/日期处理/导入校验/异常检测）对应上表 **STG 清洗层 + 导入校验**；新增的 ODS 层强调"原始不加工保溯源"，DWS/API 层强调"标签一致 + 输出血缘"——补全了全链路视角。
- 多品牌场景：每品牌一条管道（品牌配置驱动），质量规则按品牌配置差异化（财报品牌严、品牌墙品牌松但标记），见 [[brand_config_driven_system]]。
