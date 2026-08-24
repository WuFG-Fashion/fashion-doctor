# Polars 1.42 官方发布：自适应云 I/O、矛盾过滤器消除、排序检测

> **来源**：https://pola.rs/posts/polars-1-42 (Polars 官方博客)
> **发布日期**：2026-06-29
> **采集日期**：2026-07-15

---

## 核心摘要

Polars 1.42 于 2026 年 6 月 29 日发布，包含三大亮点：自适应云 I/O 并发控制器（TPC-H SF=1000 整体 2x、I/O 密集查询最高 4x）、矛盾过滤器消除（6 类矛盾自动折叠为空结果）、DataFrame/Expr 级别的 is_sorted()。

---

## 一、自适应云 I/O 并发 (PR #27924)

Polars 1.42 引入自适应并发控制器，用于从云对象存储（S3、GCS、Azure）读取 Parquet 和 IPC 文件。它根据观测到的带宽和延迟动态调整并发请求数量。

**性能数据**：
- 基准测试：TPC-H SF=1000，64 vCPU 实例
- **整体 2x 提升**，I/O 密集型单查询最高 **4x 提升**
- **无需 API 变更**，现有 `read_parquet`/`scan_parquet` 和 `read_ipc`/`scan_ipc` 从云存储调用自动受益

---

## 二、矛盾过滤器消除 (PR #27775)

查询优化器现在能检测永远不可能为真的过滤谓词，将整个查询折叠为空结果——**不扫描任何数据，不计算任何表达式**。识别 6 类矛盾：

| 类别 | 说明 | 示例 |
|------|------|------|
| 逻辑否定 | 谓词与其否定取合取 | `A AND NOT(A)` |
| 反向比较 | 两个不可能同时成立的比较 | `x > 5 AND x <= 5` |
| 空成员 | 对空集的成员检查 | `is_in([])` |
| 不相交范围 | 下界大于上界 | `a > 5 AND a < 3` |
| 非重叠区间 | 两个 never overlap 的 `is_between` | `is_between(4,6) AND is_between(0,2)` |
| 范围外相等 | 等式落在范围之外 | `a == 5 AND a > 10` |

**价值**：对程序化构建的谓词（参数化过滤器）特别有效，如 `low > high` 时自动跳过整个查询。

---

## 三、DataFrame 和 Expr 的 is_sorted() (PR #27870, #26708)

`Series.is_sorted()` 早已可用。1.42 扩展到 DataFrame 和表达式级别：

```python
df.is_sorted("a")              # DataFrame 级别
pl.col("a").is_sorted()        # Expr 级别，可用于 select/filter
```

均支持 `descending` 和 `nulls_last` 参数，当前标记为 unstable。

---

## 与服装零售数据场景的关联

- 多品牌数据管道从云存储（S3/Azure）读取每日销售 Parquet 文件，自适应 I/O 直接提升吞吐
- 矛盾过滤器消除有助于参数化报表查询（如日期范围无效时自动短路，避免无效扫描）
- is_sorted() 可用于验证 ETL 管道输出数据是否按时间/门店排序
