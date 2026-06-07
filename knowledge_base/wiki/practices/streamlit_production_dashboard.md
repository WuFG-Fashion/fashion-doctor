---
type: practice
title: Streamlit生产级多品牌看板构建
tags: [streamlit, dashboard, multi_brand, production, code]
sources: [2026-06-07_Python看板框架对比2026, streamlit_multitab (L3_07_04)]
created: 2026-06-07
updated: 2026-06-07
cross_refs: [[streamlit_dashboard_2026]], [[multi_brand_unified_analytics]], [[python_dashboard_ecosystem_2026]], [[polars_vs_pandas_2026]]
---

# Streamlit生产级多品牌看板构建

> **一句话摘要**：从原型到生产的Streamlit多品牌看板完整实操——基于pages/模块化架构、缓存体系、品牌配置驱动、7项生产检查。

> **来源**：UseDataBrain 2026 + L3_07_04 Streamlit多Tab组件

## 项目结构

```
dashboard/
├── main.py                 # 入口：品牌选择+导航
├── pages/
│   ├── 01_经营概览.py       # 多品牌KPI对比
│   ├── 02_销售趋势.py       # 销售时间序列分析
│   ├── 03_商品分析.py       # SKU/品类/售罄
│   ├── 04_VIP分析.py        # 会员/复购/RFM
│   └── 05_导购分析.py       # 导购业绩/排行
├── config/
│   ├── brands.py           # 品牌配置
│   └── category_map.py     # 品类映射表
├── data/
│   ├── loader.py           # 数据加载+缓存
│   └── queries.py          # SQL查询模板
├── components/
│   ├── kpi_cards.py        # 通用KPI卡片组件
│   ├── brand_selector.py   # 品牌选择器
│   └── charts.py           # 通用图表组件
└── utils/
    ├── cache.py            # 缓存策略
    └── theme.py            # 主题/配色
```

## 品牌配置驱动

```python
# config/brands.py
BRANDS = {
    "cabbeen": {
        "name": "卡宾",
        "color": "#000000",
        "db_table": "cabbeen_sales",
        "date_field": "sale_date",
        "amount_field": "sale_amount",
        "active_shops": 50,
    },
    "peacebird": {
        "name": "太平鸟男装",
        "color": "#E60012",
        "db_table": "peacebird_sales",
        "date_field": "transaction_date",
        "amount_field": "net_amount",
        "active_shops": 200,
    }
}
```

## 缓存体系

```python
# utils/cache.py
import streamlit as st
from datetime import timedelta

# 日级数据：天级刷新
@st.cache_data(ttl=timedelta(hours=6).total_seconds())
def load_daily_sales(brand: str, date_range: tuple):
    return query_sales(brand, date_range)

# 月度汇总：小时级刷新
@st.cache_data(ttl=3600)
def load_monthly_kpi(brand: str):
    return query_monthly_kpi(brand)

# 静态配置：持久化
@st.cache_data(persist=True)
def load_brand_config():
    return BRANDS
```

## 多品牌KPI卡片组件

```python
# components/kpi_cards.py
def render_kpi_row(brand: str, metrics: dict):
    """渲染单品牌KPI行"""
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[0]:
        st.metric("销售额", f"¥{metrics['sales']/10000:.0f}万",
                  delta=f"{metrics['sales_yoy']:+.1f}%")
    with cols[1]:
        st.metric("售罄率", f"{metrics['sell_through']:.1f}%")
    with cols[2]:
        st.metric("连带率", f"{metrics['upt']:.2f}")
    with cols[3]:
        st.metric("客单价", f"¥{metrics['avg_basket']:.0f}")
    with cols[4]:
        st.metric("周转天数", f"{metrics['turnover_days']:.0f}天")

def render_brand_comparison(brands: list, metric: str):
    """跨品牌KPI横向对比（使用相对指标）"""
    data = {b: get_normalized_kpi(b, metric) for b in brands}
    # 用倍率/百分比而非绝对值对比
    ...
```

## 7项生产检查（每条必须完成）

```python
# ✅ 1. 固定依赖版本
# requirements.txt:
# streamlit>=1.55
# plotly>=6.0
# pandas>=2.2
# polars>=2.0

# ✅ 2. 真实数据源
# ❌ df = pd.read_csv("sample.csv")
# ✅ df = load_from_warehouse(query)

# ✅ 3. 缓存所有昂贵操作
@st.cache_data(ttl=3600)
def expensive_query():
    ...

# ✅ 4. 图表固定高度
fig.update_layout(height=400)  # 非width

# ✅ 5. 10x数据量测试
# 开发用10万行 → 上线前用100万行+测试

# ✅ 6. 时区显式标注
st.caption("⏰ 所有时间均为北京时间 (UTC+8)")

# ✅ 7. 认证外挂
# Nginx/Auth0/Cloudflare Access → upstream to Streamlit
```

## 多品牌实时指标架构（进阶）

```
┌──────────────────────────────────────┐
│        Streamlit Dashboard           │
│  @st.cache_data + st.experimental_   │
│  fragment (v1.40+) 增量刷新          │
├──────────────┬───────────────────────┤
│  品牌A看板    │   品牌B看板            │
│  实时销售     │   实时销售             │
├──────────────┴───────────────────────┤
│     统一指标层 (Redis/内存缓存)       │
├──────────────────────────────────────┤
│  Polars/SQL 引擎 (流式ETL)           │
├──────────┬──────────┬───────────────┤
│ 品牌A DB  │ 品牌B DB  │ 行业基准API    │
└──────────┴──────────┴───────────────┘
```

## 关联知识
- [[streamlit_dashboard_2026]]
- [[multi_brand_unified_analytics]]
- [[python_dashboard_ecosystem_2026]]
- [[零售数据仓库SQL实践]]
- [[polars_vs_pandas_2026]]
