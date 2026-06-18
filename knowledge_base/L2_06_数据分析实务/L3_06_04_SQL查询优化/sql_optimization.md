# SQL查询优化

> **分类**: L2_06 数据分析实务 > L3_06_04 SQL查询优化
> **状态**: 🔄 持续迭代中
> **数据库引擎**: SQLite（主要）/ MySQL / PostgreSQL

---

## 最新更新 (2026-06-18)

> 本页内容已迁移至 wiki/ 体系。请查阅：
> - [[SQL查询性能优化]] — SQL三维优化法（索引+改写+参数）
> - [[polars_vs_pandas_2026]] — Polars 2.0新特性（Arrow Flight SQL/谓词下推/SIMD正则）
> - [[ETL架构选型]] — ETL vs ELT双模式选型（零售企业4h→30min提速8倍）
> - [[python_sql_integration_patterns_2026|Python Pandas+SQL集成实战]] — 三模式分层集成

---

## 6. 2026年5月17日00:54更新（第十七轮采集）

### [Vanna零售业：销售分析和库存管理的SQL自动化]（来源：CSDN blog.csdn.net，日期：**2025-09-05**，可信度：中高）
- **零售业每天产生海量数据**：销售记录/库存状态/客户行为/供应链信息
- 但真正能从中提取商业洞察的团队寥寥无几
- **传统数据查询流程三大痛点**：
  1. **技术门槛高**：业务人员不会写SQL
  2. **耗时耗力**：简单查询也要等数据团队排期
  3. **结果不可复用**：每次分析从零开始
- **Vanna AI解决方案**：自然语言→SQL自动生成→可视化结果

### [用SQL分析销售问题完整实操]（来源：知乎 zhuanlan.zhihu.com，日期：**2025-08-06**，可信度：中高）
- 从业务需求到代码实现的**完整路径拆解**
- 基于真实电商数据集的全流程演示

### [MySQL数据分析提升零售效率]（来源：帆软 finebi.com，日期：**2025-09-23**，可信度：中高）
- MySQL在零售场景的**全链路应用案例**
- 覆盖：库存优化/销售预测/客户分群/促销效果评估

### [零售BI选型指南：五款可视化工具对比]（来源：协同运营平台 seeyon.com，日期：**2026-04-02**，可信度：中高）
- 零售企业BI工具选型的关键考量维度：
  - 用户行为分析能力 / 销售数据分析深度 / 系统集成难度 / TCO

---

## 1. SQLite性能要点

| 优化项 | 说明 | 示例 |
|--------|------|------|
| **索引** | WHERE/JOIN字段必须建索引 | CREATE INDEX idx_sales_date ON sales(date) |
| **避免SELECT *** | 只查需要的列 | SELECT shop, SUM(amount) FROM ... |
| **JOIN顺序** | 小表在前，结果集小的先JOIN | inventory(3万) LEFT JOIN sales(2万) |
| **子查询→CTE** | 复杂逻辑用WITH拆分 | WITH daily_sales AS (...) SELECT ... |
| **日期函数** | SQLite日期函数有限 | 用字符串比较代替 date() 函数 |

---

## 2. 常用查询模板（已优化）

### 销售汇总（按店铺+日期）
```sql
-- ✅ 优化版：索引命中，只取必要字段
SELECT s.date, s.shop_name, 
       COUNT(DISTINCT s.sku_code) AS sku_count,
       SUM(s.quantity) AS total_qty,
       ROUND(SUM(s.amount), 2) AS total_amount,
       ROUND(SUM(s.tag_price), 2) AS total_tag
FROM sales s
WHERE s.date BETWEEN ? AND ?
  AND s.shop_name IN (SELECT full_name FROM shops WHERE region = ?)
GROUP BY s.date, s.shop_name
ORDER BY s.date DESC, total_amount DESC;
```

### 库存健康度
```sql
-- ✅ 使用CTE清晰表达逻辑
WITH shop_inventory AS (
    SELECT shop_name, sku_code, qty, tag_amount, date
    FROM inventory
    WHERE date = ?
),
sku_sales AS (
    SELECT shop_name, sku_code, SUM(quantity) AS sold_qty
    FROM sales
    WHERE date >= ? AND date <= ?
    GROUP BY shop_name, sku_code
)
SELECT i.shop_name,
       COUNT(i.sku_code) AS total_sku,
       SUM(CASE WHEN COALESCE(s.sold_qty, 0) = 0 THEN 1 ELSE 0 END) AS dead_sku,
       ROUND(SUM(CASE WHEN COALESCE(s.sold_qty, 0) = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(i.sku_code), 2) AS dead_rate
FROM shop_inventory i
LEFT JOIN sku_sales s ON i.shop_name = s.shop_name AND i.sku_code = s.sku_code
GROUP BY i.shop_name;
```

---

## 3. 索引设计规范

### 必建索引
```sql
-- 销售表
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(date);
CREATE INDEX IF NOT EXISTS idx_sales_shop ON sales(shop_name);
CREATE INDEX IF NOT EXISTS idx_sales_sku ON sales(sku_code);
CREATE INDEX IF NOT EXISTS idx_sales_date_shop ON sales(date, shop_name);

-- 库存表
CREATE INDEX IF NOT EXISTS idx_inv_date ON inventory(date);
CREATE INDEX IF NOT EXISTS idx_inv_shop ON inventory(shop_name);

-- 到货表
CREATE INDEX IF NOT EXISTS idx_arrival_date ON arrival(date);
CREATE INDEX IF NOT EXISTS idx_arrival_shop ON arrival(shop_name);
```

---

## 4. 性能排查 checklist

| 现象 | 可能原因 | 解决方案 |
|------|----------|----------|
| 查询慢(>5s) | 缺少索引 | EXPLAIN QUERY PLAN 分析 |
| 内存占用高 | 一次取太多数据 | 加LIMIT / 分页 |
| JOIN结果不对 | 字段类型/编码不一致 | 统一字段格式 |
| 日期过滤无效 | 日期格式不统一 | 统一YYYY-MM-DD格式 |
| 聚合结果异常 | NULL未正确处理 | 使用COALESCE |

---

## 5. 数据量参考

| 表 | 单品牌日均增量 | 月增量 | 年预估量 |
|----|----------------|--------|----------|
| sales | ~500-2000行 | ~3万行 | ~36万行 |
| inventory | ~300-500行 | ~1万行 | ~12万行 |
| arrival | ~200-500行 | ~1万行 | ~12万行 |

> 注：SQLite处理百万级行没问题，注意索引即可。

---

## 7. 2026年5月20日09:11更新（第二十七轮采集）

### [Polars vs Pandas：2026年 definitive 选型指南]（来源：Kanaries docs.kanaries.net / 知乎 / CSDN / 51CTO，日期：**2026-02至05-12**，可信度：**高**）⭐⭐
- **Polars 已成为Pandas最强替代方案**（Rust构建 + Apache Arrow内存底座）
- **核心性能对比（1GB CSV / 10M行数据）**：

| 操作 | Pandas | Polars | 加速比 |
|------|--------|--------|--------|
| CSV加载(1GB) | 8.2秒 | 1.6秒 | **5倍** |
| 内存占用(1GB) | 1.4GB | 0.18GB | **少87%** |
| GroupBy聚合(10M行) | 1.8秒 | 0.22秒 | **8-10倍** |
| 排序(10M行) | 3.4秒 | 0.29秒 | **~11倍** |
| Join操作(10M+1M) | 2.1秒 | 0.35秒 | **6倍** |

- **架构差异**：

| 特性 | Pandas | Polars |
|------|--------|--------|
| 底层语言 | Python (C/Cython) | **Rust** |
| 内存模型 | NumPy block-manager | **Apache Arrow 原生列式** |
| 执行模式 | 仅即时求值 | **即时 + 惰性求值** |
| 多线程 | 单线程 | **自动并行所有CPU核心** |
| 查询优化器 | ❌ 无 | ✅ 有(predicate/projection pushdown) |
| GPU支持 | ❌ | ✅ NVIDIA GPU加速 |
| Index | 行索引为核心API | **无Index（纯列操作）** |

- **2026选型建议**：

| 场景 | 推荐 | 理由 |
|------|------|------|
| 数据<100万行 | **Pandas** | 足够快，生态最完整 |
| 数据经常>100万行 | **Polars** | 数量级性能提升 |
| 构建数据流水线 | **Polars** | 惰性求值+查询优化器自动优化 |
| 内存受限环境 | **Polars** | 同硬件处理更大数据集 |
| 深度ML集成 | **Pandas** | scikit-learn默认接收Pandas |
| 全新项目无遗留代码 | **Polars** | API更干净一致 |

- **混合方案最佳实践**（推荐）：
  ```python
  # 1. 用Polars处理大数据
  processed = pl.scan_parquet("large.parquet").filter(...).group_by(...).agg(...).collect()
  # 2. 转Pandas用于ML/可视化
  pandas_df = processed.to_pandas()
  ```
- **关键迁移速查表**：

| Pandas写法 | Polars等价 |
|-----------|----------|
| `df["col"]` | `df.select("col")` 或 `pl.col("col")` |
| `df[df["col"]>5]` | `df.filter(pl.col("col")>5)` |
| `df.groupby("col").sum()` | `df.group_by("col").agg(pl.all().sum())` |
| `df.sort_values("col")` | `df.sort("col")` |
| `df.merge(other, on="key")` | `df.join(other, on="key")` |
| `df.fillna(0)` | `df.fill_null(0)` |

- **对Fashion Doctor直接影响**：
  - cabbeen.db当前数据量在万级行，Pandas完全够用
  - 若未来扩展到多品牌/多年份（百万级行），应评估迁移Polars
  - 新分析脚本可优先尝试Polars，语法几乎一致但更快

---

## 8. 2026年5月27日10:24更新（第三十轮采集）⭐

### [金仓数据库零售销售分析落地案例：某连锁商超查询性能显著提升]（来源：人大金仓 kingbase.com.cn，采集日期：2026-05-27，可信度：**高**）⭐

**背景规模（全国性连锁商超）**：
- 覆盖**28省份、3200+门店、年销售额超800亿元**
- 日新增结构化数据约**8TB**、商品SKU **1200万+**
- 核心事实表2400万行×1443列，日均交易流水**12亿条**
- 并发分析会话500+，峰值连接超600

**Oracle原环境痛点**：
| 指标 | 数值 |
|------|------|
| 平均查询响应时间 | **3.8秒** |
| 高峰时段慢SQL占比 | **17%** |
| "区域热销TOP100"查询响应 | 由1.2秒恶化至**5.7秒** |
| 晚高峰行级锁等待 | 平均超**200毫秒** |

**优化措施与效果**：
| 措施 | 技术细节 | 效果 |
|------|---------|------|
| ICU中文国际化组件 | 显式 `COLLATE "zh-CN"` 重建索引 | 中文排序查询：2.1秒→**0.9秒**（降57%） |
| 自适应基数估计(ACE) | 结合KWR负载信息库采集执行计划 | "区域热销TOP100"稳定在**0.8秒以内** |
| Hash Join + 组合索引 | `idx_sales_time_sku_store` | 慢SQL占比17%→**1.2%以下** |
| 3节点读写分离 | 1主2从 + KFS同步 | P95响应稳定≤**1.3秒** |

**整体性能提升汇总**：
| 指标 | Oracle | 金仓KES v8.6 | 提升 |
|------|--------|-------------|------|
| 核心看板P95响应 | 3.8秒 | **2.28秒** | 降幅**40%** |
| TOP10高频查询 | — | 缩短**42.3%** |
| TPS | 2800 | **5800** | **+107%** |
| 慢SQL占比 | 17% | **1.2%以下** |
| 存储空间 | — | 减少**22%** |
| 系统可用性 | — | 连续**180天零故障** | 故障切换<800ms |
| 迁移代码修改率 | — | **2.3%** |

**对Fashion Doctor的参考价值**：
- 中文排序字段（店铺名、商品名）可考虑类似优化
- 读写分离架构在Streamlit多品牌系统中可参考（主库写、从库读）
- 组合索引 `(date, sku_code, shop_name)` 的建立思路可直接复用
- "自适应基数估计"原理：根据负载自动调整执行计划——在SQLite中可通过 `ANALYZE` 命令近似实现

## 关联知识

- [[数据质量红线]]
- [[品牌配置管理]]
- [[系统架构设计]]

## 2026年6月14日更新（C轮 L2_06/07采集）⭐

### 2026 Python数据分析库全景对比（来源：Scopir，日期：**2026-06**，可信度：**高**）

- **六大库定位**：Polars（性能优先/Rust+惰性求值）、DuckDB（SQL聚合之王/零拷贝）、Pandas 2.2（生态王者）、Modin（❌不推荐）、Vaex（维护模式）、DataFusion（增长中）
- **快速决策树**：<100万行→Pandas(Arrow) ✓ / SQL团队→DuckDB ✓ / 管道化→Polars ✓ / >1亿行→Polars(Lazy)/DuckDB ✓
- **能耗对比**：大规模合成数据Polars≈Pandas的1/8能耗，TPC-H查询约为63%
- **Modin短板**：API不完整静默回退、小数据更慢、分布式调试难（明确不推荐）
- 详见 [[polars_vs_pandas_2026]] [[2026-06-14_Scopir_Python数据分析库2026全景对比]]

### Python默认技术栈2026：uv+Ruff+Ty+Polars（来源：AI Future Thinkers，日期：**2026-06**，可信度：**高**）

- **工具8合一**：uv替代pyenv+pip+venv+Poetry、Ruff替代Black+isort+Flake8、Ty替代mypy、Polars替代pandas
- **同出Astral**：uv+Ruff+Ty均来自Astral公司，统一pyproject.toml配置
- **uv run一站式**：永不手动激活虚拟环境，CI用`uv sync --frozen`
- 详见 [[python_dev_stack_2026]] [[2026-06-14_AIFutureThinkers_Python默认技术栈2026]]

## 2026年6月15日更新（C轮 L2_06/07采集）⭐

### Python数据栈边界决策框架2026（来源：CSDN，日期：**2026-04-10**，可信度：**高**）

- **三重边界清晰定义**：<5GB→Pandas / 5-100GB→Polars+DuckDB / >100GB→Spark
- **Benchmark实测**：Polars 6.7x(Pandas)/ClickHouse 10x(Pandas)，电商案例4h→15min(16x)
- **五步优化路径**：Python原型→Polars+DuckDB加速→Spark分布式→ClickHouse原生→Python编排
- 详见 [[python_data_stack_decision_2026]] [[2026-06-15_CSDN_Python数据栈边界决策框架]]

### Python Pandas+SQL集成实战模式（来源：aimojo，日期：**2026-06-12**，可信度：**高**）

- **三模式分层**：pandasql(快速原型)→SQLAlchemy原生(生产ETL)→管道分层(自动化)
- **效率提升**：Pandas+SQL融合可缩短分析时间50%
- **生产红线**：pandasql大数据较慢，生产环境必须用SQLAlchemy
- 详见 [[python_sql_integration_patterns_2026]] [[2026-06-15_aimojo_Python_Pandas_SQL集成指南]]
