# 2026-07-25 Polars vs Pandas 基准刷新 + 混合用范式更新

> 本轮采集: Danilchenko 240M 行真实基准(Polars joins/groupby ~10x、Parquet ~5x) + 今日头条 Polars 月下载破 3000 万、1000 万行 groupby ~10x/join ~12x/内存省 65-73% + Pandas 3.0 GA(Arrow 字符串+CoW 默认)

## 核心更新

- **真实负载基准**: 240M 行点击流(18 Parquet/14GB)，Polars joins/group-bys ~10x、Parquet 读取 ~5x
- **Pandas 3.0 GA**: PyArrow 后端字符串默认、Copy-on-Write 默认、`pd.col()` 表达式 API
- **范式升级**: 从"二选一"到"双轨"——Polars 批量变换 + Pandas 最后一公里(sklearn/matplotlib)
- **混合用**: 1000 万行内存 3.2→1.1GB(65%)，50 万行以下无感差异

参考: [[polars_vs_pandas_2026]]、[[python_data_stack_decision_2026]]、[[2026-07-25_Danilchenko_Polars_vs_Pandas_2026刷新基准]]、[[2026-07-25_今日头条_Polars_Pandas_2026混合用范式]]
