# Danilchenko：Polars vs Pandas 2026 真实基准刷新（2026-07）

> 来源：https://danilchenko.dev/posts/polars-vs-pandas/ （Last updated: July 2026，refreshed for Pandas 3.0）
> 类别：L2_06 数据分析实务 / 分析引擎基准

## 核心结论

- Polars 在任何 >1GB 基准上都更快；作者 240M 行实测中 joins 和 group-bys 约 **10x 快**，Parquet 读取约 **5x 快**。
- Pandas 3.0（2026 年 1 月 GA）缩小了部分差距：默认 **PyArrow 后端字符串**、**Copy-on-Write 默认开启**、新增 **`pd.col()` 表达式 API**（直接借鉴 Polars）。
- 引擎级差距在 Polars 1.43 / Pandas 3.0 上**未改变**（理由见 Pandas 3.0 章节）。
- 作者真实跑过两条生产管道后选择**双轨**：Polars 做批量变换，Pandas 做"最后一公里"（scikit-learn / matplotlib）。
- **"该不该全面迁移？" 答案仍是"否"**——小交互数据集、需经 scikit-learn / matplotlib 往返、字符串密集场景 Pandas 仍胜。

## 真实工作负载基准（240M 行）

- 数据：约 **2.4 亿行**点击流，分布在 **18 个 Parquet 文件**，含 joins / aggregations / filtering 等真实 ETL 操作。
- 硬件：M2 Pro，16 核，32GB RAM；每操作跑 5 次。
- 文件规模：7 个数值列 + 3 个字符串列，磁盘约 **14GB**。
- 基准版本：Polars **1.18** vs Pandas **2.2**（引擎级差距在 1.43 / Pandas 3.0 保持不变）。

## Pandas 3.0 改了什么（又没改什么）

| 变化 | 说明 |
|------|------|
| PyArrow-backed strings 默认 | 底层字符串全面转向 Arrow 列式 |
| Copy-on-Write 默认 | 链式赋值现在直接报错，消除 SettingWithCopy 隐患 |
| `pd.col()` 表达式 API | 借鉴 Polars 的表达式风格 |
| 仍胜出的场景 | 小交互数据集、scikit-learn / matplotlib 往返、字符串密集 |

> 第三方视角：DuckDB Labs 的 db-benchmark 在 0.5GB / 5GB / 50GB 三档追踪 group-by 与 join 性能（Polars / Pandas / DuckDB 等）。

## 对服装零售数据分析的启示

- 多品牌季度汇总 / 全渠道年度交易 / VIP 全量行为分析（100 万行+）仍是 Polars 主场。
- 探索性 Notebook（<1GB）+ ML 建模最后一公里保留 Pandas，避免无谓重写。
- 混合栈：Polars 做 ETL 批量变换 → `to_pandas()` 零拷贝转 Pandas 做 sklearn / 可视化。
