---
type: source
title: Streamlit DataFrame 显示与优化2026（Kanaries）
tags: [streamlit, dataframe, visualization, optimization, pandas, polars]
aliases: ["Streamlit", "DataFrame", "显示与优化2026（Kanaries）", "Streamlit DataFrame 显示与优化2026（Kanaries）"]
confidence: 第三方数据
brand_specific: false
source_url: https://docs.kanaries.net/zh/topics/Streamlit/streamlit-dataframe
created: 2026-06-09
updated: 2026-06-09
cross_refs: [[streamlit_dashboard_2026]], [[polars_vs_pandas_2026]], [[python_dashboard_ecosystem_2026]]
---

# Streamlit DataFrame 显示与优化2026

> **来源**：Kanaries Docs（2026-05-29更新）
> **覆盖**：Streamlit中DataFrame的显示、样式化与性能优化

## 三种显示方法对比

| 方法 | 适用场景 | 性能 | 交互 |
|------|---------|:---:|:---:|
| `st.dataframe()` | **生产主力**，大数据集首选 | 高（虚拟滚动） | 排序/过滤/搜索 |
| `st.table()` | 小数据集（<1000行）静态展示 | 中（全量渲染） | 无 |
| `st.data_editor()` | **编辑场景**，用户可修改数据 | 中 | 编辑/复制行/添加行 |

## 性能优化要点

| 策略 | 方法 | 效果 |
|------|------|------|
| 限制行数 | `df.head(10000)` 或服务端预聚合 | 避免5万行+直接渲染 |
| 缩小列宽 | `column_config` 指定像素宽度 | 减少DOM节点 |
| 缓存数据 | `@st.cache_data` 缓存加载函数 | 避免每次交互重载 |
| 列投影 | 查询时只SELECT需要展示的列 | 减少数据传输 |
| Arrow互通 | `pl.DataFrame` 直接传给Streamlit | v1.30+原生支持Polars零拷贝 |

## Column Config 高级配置

```python
st.dataframe(
    df,
    column_config={
        "revenue": st.column_config.NumberColumn(
            "营收", format="¥%.0f", width="medium"
        ),
        "growth": st.column_config.ProgressColumn(
            "增长率", format="%.1f%%", min_value=-50, max_value=100
        ),
        "date": st.column_config.DateColumn("日期", format="YYYY-MM-DD"),
    },
    hide_index=True,
    use_container_width=True,
)
```

## Polars 原生支持（v1.30+）

Streamlit v1.30起原生支持 `pl.DataFrame`，无需 `to_pandas()` 转换，结合 `@st.cache_data` 可获得零拷贝性能：

```python
import polars as pl

@st.cache_data
def load_brand_sales(brand: str) -> pl.DataFrame:
    return pl.scan_parquet(f"data/{brand}_sales.parquet")
        .group_by("month").agg(pl.col("amount").sum())
        .collect()

st.dataframe(load_brand_sales("peacebird"))
```

## 服装零售看板场景适配

| 场景 | 推荐组件 | 说明 |
|------|---------|------|
| 销售流水明细 | `st.dataframe()` + 虚拟滚动 | 百万行级别可平滑滚动 |
| KPI卡片 | `st.metric()` | 带delta对比 |
| 品牌对比表 | `st.dataframe()` + column_config | 条件高亮/进度条 |
| 排行榜 | `st.dataframe()` + 预排序+head(20) | Top N展示 |
| 数据编辑 | `st.data_editor()` | 预算调整/参数配置 |

## 关联页面
- [[streamlit_dashboard_2026]] — Streamlit生产级实践
- [[streamlit_production_dashboard]] — 多品牌看板实操
- [[polars_vs_pandas_2026]] — 数据分析引擎选型
- [[python_dashboard_ecosystem_2026]] — 2026看板生态全景
