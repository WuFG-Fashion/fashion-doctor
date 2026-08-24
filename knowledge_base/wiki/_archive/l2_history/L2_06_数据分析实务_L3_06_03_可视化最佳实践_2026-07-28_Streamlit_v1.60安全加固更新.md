# L3_06_03 可视化最佳实践 — 2026-07-28 更新纪要

> 本轮（ingestC Round 116）补充 Streamlit v1.60 安全加固，与 L2_06 可视化最佳实践直接相关。

## 新增要点

- **Streamlit v1.60（2026-07-21）安全加固**：三大 breaking 安全变更——
  - 拒绝子 iframe/注入脚本的 origin 伪造（CWE-346）
  - 客户端 query string 上限 512 KiB / 1000 字段（CWE-770）
  - `server.maxWidgetStateSize` 默认 25 MB（CWE-770）
- `client.disableDataExport` 全局隐藏 CSV 导出 + 禁用只读表剪贴板复制。
- 交互增强：`st.dataframe` 排序保留行选择、`st.tabs` 支持 `height`、`st.columns` 的 `gap` 支持像素值、`st.metric` 零值显中性灰。
- 多品牌敏感看板（销售/会员/毛利）必配导出管控 + widget 限流 + 防注入。

## 关联 wiki 页面

- 来源摘要：[[2026-07-28_Streamlit_v1.60_安全加固]]
- 概念页：[[streamlit_dashboard_2026]]（已追加"v1.60 安全加固"小节）
- 实操页：[[streamlit_production_dashboard]]（已追加"v1.60 安全加固与生产部署"小节）
