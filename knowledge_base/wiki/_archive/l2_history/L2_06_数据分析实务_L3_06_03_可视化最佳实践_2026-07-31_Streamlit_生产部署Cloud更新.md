# L3_06_03 可视化最佳实践 — 2026-07-31 更新纪要

> 本轮（ingestC Round 117）补充 Streamlit 2026 生产部署三路线，与 L2_06 数据分析实务 / 可视化最佳实践直接相关。

## 新增要点

- **Snowflake Container Runtime GA（2026-03-09）**：Snowpark Container Services 上运行，获 GPU/更广 Python 包/无休眠长时服务；`st.secrets` 安全访问、app-viewer URLs 分享。
- **Streamlit Cloud 免邀请（2026-07-07）**：邮箱验证即可建免费应用；销售漏斗监控页本地→全球可访问仅 4 分 17 秒。
- **Docker 生产部署**：python:3.11-slim 镜像 327MB、启动 3 秒；py-spy 定位 Plotly `mode='lines+markers'` 占 78% CPU，改 `mode='lines'` 后 5 倍提速。
- **运行机制**：全脚本重跑模型，耗时 IO 必 `@st.cache_data`；适合原型/内部工具，不适合海量用户商用站。

## 关联 wiki 页面

- 来源摘要：[[2026-07-31_Streamlit_2026生产部署与Cloud零门槛]]
- 概念页：[[streamlit_dashboard_2026]]（已追加"Streamlit 2026 生产部署三路线"小节）
- 实操页：[[streamlit_production_dashboard]]（已追加"2026 生产部署三路线"小节）
