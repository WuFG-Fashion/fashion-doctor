# DuckDB vs Polars 2026：从生产管道迁移实战看引擎选择

> **来源**：https://www.danilchenko.dev/posts/duckdb-vs-polars (Danilchenko 个人博客)
> **作者简介**：作者将数百 GB Parquet 数据管道从 Pandas 迁移到 DuckDB + Polars，基于实际生产经验撰写
> **发布日期**：2026-07
> **采集日期**：2026-07-15

---

## 核心摘要

作者的核心结论：**停止把 DuckDB 和 Polars 看作对手。** DuckDB 是用 SQL 查询文件的最佳工具、内存紧张时最安全；Polars 是在 Python 中编写快速、类型安全、变换密集管道的最佳方式。两者共享 Apache Arrow 内存格式，零拷贝互操作。在真实管道中，两者各司其职。

---

## 一、2TB Parquet 基准测试

引用 codecentric 权威基准，单表从 2GB 扩展到 2TB：

| 场景 | DuckDB | Polars（默认） | Polars（强制异步读） |
|------|--------|---------------|---------------------|
| 2TB Parquet 扫描 | **~45 秒** | ~60 秒 | ~100 秒 |
| 140GB 单文件 | 领先约 1 秒 | — | — |

**操作类型胜负分布**：

| 操作 | 优势方 |
|------|--------|
| CSV 读取 | **Polars** |
| Join 操作 | **Polars** |
| 窗口函数 | **DuckDB** |
| Group-by | 基本持平 |

---

## 二、内存占用——真正的分水岭

codecentric 140GB 单文件测试：

| 引擎 | 峰值内存 |
|------|----------|
| **DuckDB** | **~1.3 GB** |
| Polars（默认） | ~17 GB |
| Polars（强制异步读） | **~750 MB**（低于 DuckDB） |

> **关键发现**：分区数据使 DuckDB 峰值内存降低约 **8 倍**，Polars 降低约 **4 倍**。**文件布局比引擎选择对内存的影响更大。**

DuckDB 的持久优势：**自动溢写磁盘**（零配置）；Polars 需要手动选择 streaming engine。

---

## 三、共存模式——最佳实践

两者共享 Arrow 格式，零拷贝互传。作者的生产模式：

```python
# DuckDB 负责文件扫描和粗粒度聚合
orders = duckdb.sql("""
    SELECT customer_id, product, sum(amount) AS revenue
    FROM 'data/orders/*.parquet'
    WHERE order_date >= '2026-01-01'
    GROUP BY customer_id, product
""").pl()  # 直接转 Polars DataFrame，零序列化

# Polars 负责排名和业务逻辑
result = orders.with_columns(
    revenue_rank=pl.col("revenue").rank("dense", descending=True).over("customer_id")
).filter(pl.col("revenue_rank") <= 3)
```

**DuckDB 做聚合，Polars 做变换，Arrow 做桥梁。**

---

## 四、选择决策矩阵

| 场景 | 推荐 |
|------|------|
| 团队写 SQL，数据在 Parquet/CSV 文件中 | DuckDB |
| 临时查询、Notebook、"帮我数一下" | DuckDB |
| 超内存数据，不想操心内存管理 | DuckDB（自动溢写） |
| 变换密集的 Python 管道 | Polars |
| 需要静态类型和 IDE 自动补全 | Polars |
| 替换 Pandas ETL 脚本 | Polars |
| Sessionization、特征工程 | Polars |
| 严肃的生产管道 | **两者都用**，Arrow 互操作 |

---

## 五、版本信息（2026年6月）

- DuckDB 1.5.4（2026-06-17）
- Polars 1.42.1（2026-06-30）
- 两者均 MIT 许可，完全进程内运行

---

## 与服装零售多品牌数据场景的关联

- 多品牌销售数据 Parquet 文件 → DuckDB SQL 快速聚合（各品牌汇总） → Polars 做排名、同比环比计算
- 内存敏感环境（单机部署）下 DuckDB 自动溢写磁盘更可靠
- 分区按品牌+日期存储可大幅降低内存峰值（8x/4x）
