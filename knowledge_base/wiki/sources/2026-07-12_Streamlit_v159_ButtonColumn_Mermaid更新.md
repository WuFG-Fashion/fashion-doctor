---
type: source
title: Streamlit v1.59.0 ButtonColumn/Mermaid/文件粘贴 + v1.58并行Fragment回顾
tags: [streamlit, dashboard, mermaid, button_column, parallel_fragment, production]
sources: [https://docs.streamlit.io/en/stable/changelog.html, https://www.change8.dev/package/streamlit]
aliases: ["Streamlit", "v1.59.0", "ButtonColumn/Mermaid/文件粘贴", "v1.58并行Fragment回顾", "Streamlit v1.59.0 ButtonColumn/Mermaid/文件粘贴 + v1.58并行Fragment回顾"]
confidence: 第三方数据
brand_specific: false
created: 2026-07-12
updated: 2026-07-12
cross_refs: [[streamlit_dashboard_2026]], [[streamlit_production_dashboard]], [[python_dashboard_ecosystem_2026]]
---

# Streamlit v1.59.0 ButtonColumn/Mermaid/文件粘贴更新

> **一句话摘要**：Streamlit v1.59.0（2026-07-06）新增ButtonColumn列类型、Mermaid图表原生渲染、chat_input文件粘贴；v1.58引入并行Fragment（parallel=True）和st.pagination；v1.57正式切换Starlette/ASGI架构。

> **来源**：Streamlit官方Changelog
> **最后更新**：2026-07-12

## 核心要点
1. **v1.59.0（2026-07-06）**：ButtonColumn（表格行内按钮）、Mermaid图表支持、chat_input文件粘贴
2. **v1.58.0（2026-05-28）**：并行Fragment（@st.fragment parallel=True）、st.pagination分页、skills CLI
3. **v1.57.0（2026-04-29）**：Starlette正式化（替换Tornado）、st.bottom固定容器、:shimmer[]动画、Polars零拷贝
4. **生产就绪**：ASGI兼容（可挂载到FastAPI）、并行Fragment支持后台类工作流
5. **AI Skills**：Streamlit开始内置AI agent开发技能（skills CLI + pip包内skill）

## 2026年版本路线（v1.53→v1.59）

| 版本 | 日期 | 标志性特性 |
|------|------|-----------|
| v1.59.0 | 07-06 | ButtonColumn、Mermaid、chat_input文件粘贴 |
| v1.58.0 | 05-28 | 并行Fragment、st.pagination、skills CLI |
| v1.57.0 | 04-29 | Starlette正式化、st.bottom、Polars零拷贝 |
| v1.56.0 | 03-31 | st.navigation增强、Python 3.14支持 |
| v1.55.0 | 03-03 | 查询参数widget绑定、动态容器on_change |
| v1.54.0 | 02-04 | widget绑定query params、动态option配置 |
| v1.53.0 | 01-14 | Markdown指标/slider、sidebar宽度配置 |

## 关联页面
- [[streamlit_dashboard_2026]] — Streamlit看板概念页（需更新至v1.59）
- [[streamlit_production_dashboard]] — 生产级多品牌看板实践
- [[python_dashboard_ecosystem_2026]] — Python看板生态概览
- [[multi_brand_unified_analytics]] — 多品牌统一分析架构
