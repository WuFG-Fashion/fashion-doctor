---
type: practice
title: Streamlit生产级多品牌看板构建
tags: [streamlit, dashboard, multi_brand, production, code, starlette, polars]
sources: [2026-06-07_Python看板框架对比2026, streamlit_multitab (L3_07_04), 2026-06-10_Streamlit官方_2026版本架构演进, 2026-06-12_Streamlit全版本新特性2026, 2026-06-14_Streamlit_2026v1.53-1.58全版本新特性.md, 2026-06-21_Streamlit_2026_H2_Starlette正式化与并发特性.md, 2026-06-24_Streamlit_2026全版本新特性v1.53-v1.58]
created: 2026-06-07
updated: 2026-06-27
cross_refs: [[streamlit_dashboard_2026]], [[multi_brand_unified_analytics]], [[python_dashboard_ecosystem_2026]], [[polars_vs_pandas_2026]], [[retail_analytics_reporting_2026]], [[brand_config_driven_system|品牌配置驱动多品牌系统]], [[retail_data_workflow_2026]], [[2026-06-21_Streamlit_2026_H2_Starlette正式化]], [[2026-06-24_Streamlit_2026全版本新特性v1.53-v1.58]], [[2026-06-27_chenxutan_Polars深层架构与生态2026]]
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

## v1.57 Starlette部署更新（2026-06新增）

### 架构迁移影响

Streamlit v1.57起默认使用Starlette/Uvicorn替代Tornado。对部署的影响：

| 配置项 | 旧值(Tornado) | 新值(Starlette) |
|------|------|------|
| Web服务器 | Tornado WSGI | **Starlette ASGI + Uvicorn** |
| `server._async` | 手动配置 | 自动处理（已移除） |
| WebSocket头获取 | `_get_websocket_headers()` | **`st.context.headers`** |
| 与FastAPI集成 | 需要复杂hack | **直接通过`st.App` ASGI入口** |

### Starlette部署模板

```python
# app.py — 使用st.App实现ASGI部署
import streamlit as st

app = st.App()

@app.route("/health")
async def health_check(request):
    return {"status": "ok"}

if __name__ == "__main__":
    app.run()
```

### Nginx + Uvicorn配置

```nginx
server {
    listen 80;
    server_name dashboard.example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;  # WebSocket关键
    }
}
```

### Polars Arrow零拷贝优化

v1.57支持Polars DataFrame直接传入，绕过pandas转换：

```python
# 旧写法（两次转换）
@st.cache_data
def load_sales():
    return pl.scan_parquet("sales.parquet").collect().to_pandas()

# v1.57+ 新写法（零拷贝）
@st.cache_data
def load_sales():
    return pl.scan_parquet("sales.parquet").collect()

st.dataframe(load_sales())  # 直接传Polars DataFrame
```

## v1.58 并行片段与分页实战（2026-06新增）

### Parallel Fragments — 多品牌看板并发加载

```python
# 多品牌数据并行加载，不阻塞 UI
@st.fragment(parallel=True)
def load_brand_a():
    df_a = pl.scan_parquet("brand_a/sales.parquet").collect()
    st.subheader("品牌A")
    st.dataframe(df_a)

@st.fragment(parallel=True)
def load_brand_b():
    df_b = pl.scan_parquet("brand_b/sales.parquet").collect()
    st.subheader("品牌B")
    st.dataframe(df_b)

@st.fragment(parallel=True)
def live_kpi():
    # 实时KPI轮询
    while True:
        col1, col2, col3 = st.columns(3)
        col1.metric("实时销售", fetch_live_sales())
        col2.metric("在线门店", fetch_live_shops())
        col3.metric("今日客流量", fetch_live_traffic())
        time.sleep(10)
```

### st.pagination — 海量SKU分页

```python
# config/brands.py 增加分页配置
BRANDS["peacebird"]["pagination"] = {
    "page_size": 50,  # 每页50条SKU
    "max_pages": 100,
}

# 分页组件
def render_sku_table(df, page_size=50):
    total_pages = len(df) // page_size + 1
    page = st.pagination(total_pages)
    start = page * page_size
    st.dataframe(df.iloc[start:start+page_size])
```

### v1.58 组件更新速查

| 组件 | 版本 | 多品牌看板场景 |
|------|:---:|---------------|
| `@st.fragment(parallel=True)` | v1.58 | 多品牌数据并行加载 |
| `st.pagination` | v1.58 | SKU明细/会员列表分页 |
| `st.bottom` | v1.57 | 品牌切换栏常驻底部 |
| `st.menu_button` | v1.56 | 品牌选择下拉菜单 |
| `st.iframe` | v1.56 | BI报表嵌入 |
| `AudioColumn` | v1.56 | 商品展示视频列 |
| `filter_mode` | v1.56 | selectbox搜索过滤 |
| `on_change` 容器 | v1.55 | 标签切换自动刷新 |
