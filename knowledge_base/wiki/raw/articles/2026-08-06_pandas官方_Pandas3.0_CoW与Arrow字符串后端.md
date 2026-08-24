# Pandas 3.0 — Copy-on-Write、PyArrow 字符串后端与 pd.col() 表达式

**采集日期**：2026-08-06
**来源**：
- pandas 官方 What's new in 3.0.0（2026-01-21）https://pandas.pydata.org/docs/whatsnew/v3.0.0.html
- pandas 官网首页（最新版 3.0.4，发布日 2026-06-28）https://pandas.pydata.org/
- PythonDataBench《Pandas 3.0: Complete Guide to Copy-on-Write, String Dtype, and pd.col() Expressions》
- SharpSkill《Pandas 3.0 in 2026: New APIs, Breaking Changes and Interview Questions》
- Quantide 博客《量化新基建(四)：Pandas 3.0》

---

## 版本时间线

| 版本 | 发布日 |
|------|--------|
| pandas 3.0.0 | 2026-01-21 |
| pandas 3.0.4（当前稳定） | 2026-06-28 |
| pandas 2.3.3 | 2025-09-29 |

官方建议：先升级到 2.3 消除全部 deprecation warning，再升 3.0。

## 三大头条特性

### 1. Copy-on-Write（CoW）成为默认且唯一模式

- 规则简化为一句话：**任何索引操作或返回 DataFrame/Series 的方法，在用户 API 层面一律表现为副本**。
- 后果：链式赋值 `df[df['A'] > 0]['B'] = 1` 从"有时生效"变成**抛出 `ChainedAssignmentError`**。
- `SettingWithCopyWarning` 被彻底移除，为消警告加的防御性 `.copy()` 不再需要。
- 底层仍尽量用视图，只在真正写入共享数据时才复制 → 性能是副产品，语义一致性才是主目标。
- `mode.copy_on_write` 选项失效并弃用，将在 4.0 删除。
- 所有方法的 `copy=` 关键字参数不再有任何作用，可安全删除。
- `inplace=True` 的方法（`replace()`/`fillna()`/`ffill()`/`bfill()`/`clip()`）现在返回 `self` 而不是 `None`，可以链式调用。

正确迁移写法：

```python
# 3.0 之前（现在报 ChainedAssignmentError）
# df[df["category"] == "A"]["price"] = 150

# 3.0 正确写法
df.loc[df["category"] == "A", "price"] = 150

# CoW 内存共享演示
df2 = df[["price"]]          # 与 df 共享内存
df2["price"] = df2["price"] * 2   # 此刻才触发复制
# df 保持不变，无副作用
```

### 2. 专用字符串 dtype（默认 PyArrow 后端）

- 历史上字符串列用 NumPy `object` dtype 存储：既不特定于字符串，性能与内存都差。
- 3.0 起，字符串数据默认推断为专用 `str` dtype，**底层由 PyArrow 支撑**（未装 PyArrow 时回退 NumPy object）。
- `str` dtype 只能存字符串或缺失值（setitem 非字符串会失败）；缺失值哨兵统一为 `NaN`，与其他默认 dtype 语义一致。

实测数据：

| 项目 | 旧（object） | 新（Arrow string） |
|------|------------|------------------|
| 100 万个 6 字符编码列内存 | 约 80 MB | 约 12 MB |
| `df['symbol'].str.upper()` | 基准 | **提速 30 倍以上** |
| `.str.contains()` / `.str.lower()` 等 | 基准 | **快 5–10 倍** |
| 文本密集列内存 | 基准 | **最多降低 50%** |

原理：旧版存的是 100 万个 Python String 对象的指针（每个都是堆内存独立对象）；3.0 把所有字符串内容紧凑放进一个连续大缓冲区 + 一个偏移量数组，在 C 层直接扫描连续内存，而不是在 Python 虚拟机里逐对象处理。

附带收益：`read_csv` 不再需要手动指定 `engine='pyarrow'`，系统自动选择最优后端。

**迁移警告**：用 `df['col'].dtype == object` 判断字符串列的代码会失效，应改为 `pd.api.types.is_string_dtype(df['col'])`。另外 PyArrow 数组不可变，转可写 NumPy 需显式 `.to_numpy(copy=True)`。

### 3. pd.col() 表达式构建器

灵感来自 PySpark 与 Polars，解决 lambda 的作用域与不透明问题。

```python
# 旧写法
df.assign(c = lambda df: df['a'] + df['b'])

# 3.0 新写法
df.assign(c = pd.col('a') + pd.col('b'))
```

`col()` 返回的表达式对象支持全部标准运算符与全部 Series 方法/命名空间（`pd.col("name").sum()`、`pd.col("name").str.upper()`）。当前可用于 `DataFrame.assign()`、`DataFrame.loc()`、getitem/setitem，后续版本会扩展。

### 4. Arrow PyCapsule 接口支持

DataFrame 与 Series 现在同时支持 Arrow PyCapsule 协议的**导出与导入**（GH 56587 / GH 63208）。Arrow C data interface 让数据在不同 DataFrame 库之间以 Arrow 格式移动，设计上尽可能零拷贝。

实际意义（Quantide 视角）：2026 年若用 Rust 写了高频计算引擎，可以直接把 pandas 3.0 的内存地址传给 Rust，中间无需任何数据拷贝——这种"原地共享"能力终结了 Python 在数据密集型任务中的性能瓶颈。

```python
import duckdb
# 与 DuckDB 零拷贝互操作
result = duckdb.sql("SELECT name FROM df WHERE name LIKE '%li%'").df()
```

## 硬性环境要求

- **Python 3.11+**（3.0 起最低要求提升）
- 3.0 移除了大量此前版本已弃用的功能

## 采集人评估

- 时效性：★★★★★（3.0.0 半年内，3.0.4 为 6 月末最新补丁）
- 可信度：★★★★★（pandas 官方文档一手）
- 与服装零售数据分析的相关性：★★★★☆（本项目多品牌分析层直接依赖 pandas/Polars/DuckDB 三方互操作）
- 可操作性：★★★★★（含明确迁移清单与断裂点）
