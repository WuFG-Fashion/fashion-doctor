# Polars + Apache Arrow 零拷贝互操作指南 2026

> 来源：PyTutorial，2026-05-11
> URL: https://pytutorial.com/polars-arrow-interoperability-guide/

## 概述

Polars 的所有数据都以 Apache Arrow 数组形式存储在内存中。这意味着 Polars 与 Arrow 生态（PyArrow、DuckDB、cuDF、Pandas 2.x+）之间可以实现**零拷贝**数据共享——数据不移动，只传递指针。

## 核心机制

### Arrow 作为通用数据层
- Apache Arrow 是跨语言的列式内存格式标准
- 它不是数据库或查询引擎，而是标准化的数据层
- 所有 Arrow 兼容工具可以零序列化共享数据

### Polars 内部存储
- 每个 DataFrame 列都是 Arrow `ChunkedArray`
- 内存布局缓存友好（连续块存储）
- 使用 Arrow 类型系统（日期、时间、嵌套类型）

## 零拷贝转换

### Polars → Arrow（零拷贝）
```python
import polars as pl
import pyarrow as pa

df = pl.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
arrow_table = df.to_arrow()  # 零拷贝，共享内存
```

### Arrow → Polars（零拷贝）
```python
data = pa.table({"city": ["NYC", "LA"], "temp": [22, 28]})
df = pl.from_arrow(data)  # 零拷贝
```

### Parquet → Arrow → Polars（全链路零拷贝）
```python
import pyarrow.parquet as pq

arrow_table = pq.read_table("data.parquet")
df = pl.from_arrow(arrow_table)
result = df.filter(pl.col("value") > 100)  # 直接过滤，无内存复制
```

## 性能收益

1. **零内存分配**：转换时不创建新内存块，共享内存池
2. **SIMD 向量化**：Arrow 列式格式支持现代 CPU 的 SIMD 指令
3. **字典编码压缩**：重复字符串自动压缩，内存下降不降速
4. **懒求值与 Arrow**：LazyFrame 查询计划利用 Arrow schema 做谓词下推和投影下推

## 跨工具互操作

| 工具 | 互操作方式 | 场景 |
|------|-----------|------|
| **PyArrow** | `df.to_arrow()` / `pl.from_arrow()` | 零拷贝数据交换 |
| **DuckDB** | Arrow 共享内存 → DuckDB SQL 查询 | Polars 读取 → DuckDB 分析 → 回传 |
| **Pandas 2.x+** | Arrow-backed dtypes → `df.to_pandas()` | 兼容旧生态 |
| **Spark** | Arrow 序列化 → Spark DataFrame | 大数据管道 |
| **Arrow Flight** | 网络传输协议 | 跨机器高速数据传输 |

## 实战模式：Polars → DuckDB → Polars
```python
import polars as pl, duckdb

# Polars 读取数据
df = pl.scan_parquet("sales_*.parquet")

# 传给 DuckDB 做复杂 SQL（零拷贝）
arrow_table = df.collect().to_arrow()
result_arrow = duckdb.sql("""
    SELECT category, SUM(amount) as total
    FROM arrow_table
    GROUP BY category
""").arrow()

# 回传 Polars 继续处理（零拷贝）
result_df = pl.from_arrow(result_arrow)
```

## 对服装零售的价值

1. **ETL 管道零拷贝**：从数据库导出(Arrow Flight) → Polars 清洗 → DuckDB 聚合 → Streamlit 展示，全链路无序列化开销
2. **混合工作流**：Polars 做宽表处理 + DuckDB 做复杂 SQL 分析，无缝切换
3. **多品牌数据融合**：不同品牌数据统一用 Arrow 格式交互，避免格式转换瓶颈
4. **内存优化**：千万级会员/交易数据共享内存，不重复占用
