---
type: source
title: Streamlit 2026 H2 Starlette正式化与并行Fragment
tags: [streamlit, starlette, asgi, polars, parallel_fragment, production]
sources: [2026-06-21_Streamlit_2026_H2_Starlette正式化与并发特性.md]
created: 2026-06-21
updated: 2026-06-22
cross_refs: [[streamlit_dashboard_2026]], [[python_dashboard_ecosystem_2026]], [[multi_brand_unified_analytics]]
---

# Streamlit 2026 H2 Starlette正式化与并行Fragment

> **一句话摘要**：Streamlit v1.57正式完成Tornado→Starlette/Uvicorn迁移（默认启用），v1.58引入@st.fragment(parallel=True)并发执行和st.pagination分页，Polars Arrow零拷贝直传上线。

> **来源**：Streamlit官方Release Notes，汇总v1.53-v1.58

## 核心要点

1. **Starlette正式化（v1.57）**：Tornado→Starlette/Uvicorn，ASGI兼容，可集成FastAPI中间件
2. **Polars Arrow零拷贝（v1.57）**：Polars DataFrame直接转Arrow，绕过pandas转换层，提升类型保真度
3. **并行Fragment（v1.58）**：`@st.fragment(parallel=True)`让多个片段同时执行，多品牌看板各Tab独立刷新
4. **st.pagination（v1.58）**：原生分页组件，无需手动管理offset/limit
5. **st.App增强**：支持secrets编程式注入、自定义异常处理器、HTTP路由/中间件

## 版本时间线

| 版本 | 日期 | 旗舰特性 |
|------|------|---------|
| v1.53 | 01-14 | Starlette实验/st.App ASGI入口/会话级缓存 |
| v1.54 | 02-04 | 路径安全加固/config.toml热加载 |
| v1.55 | 03-03 | Widget bind/dynamic_container on_change |
| v1.56 | 03-31 | st.menu_button/iframe/pandas 3.x |
| **v1.57** | **04-29** | **Starlette默认/Polars零拷贝/st.bottom** |
| **v1.58** | **05-28** | **Parallel Fragment/st.pagination/skills CLI** |

## 多品牌看板实操意义

- Starlette迁移→部署时利用ASGI中间件（认证/限流/CORS）
- Polars零拷贝→品牌数据零转换开销
- Parallel Fragment→大看板各Tab独立并行刷新
- Pagination→SKU/会员列表原生分页

## 关联页面
[[streamlit_dashboard_2026]], [[python_dashboard_ecosystem_2026]], [[multi_brand_unified_analytics]], [[streamlit_production_dashboard|Streamlit生产级看板]]
