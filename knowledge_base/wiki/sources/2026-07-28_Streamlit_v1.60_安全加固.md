---
type: source
title: Streamlit v1.60 安全加固与企业级部署（2026-07-21）
tags: [streamlit, security, production, dashboard, hardening]
sources: [2026-07-28_streamlit_v1.60_security_hardening.md]
created: 2026-07-28
updated: 2026-07-28
cross_refs: [[streamlit_dashboard_2026]]
---

# Streamlit v1.60 安全加固与企业级部署（2026-07-21）

> **一句话摘要**：Streamlit v1.60（2026-07-21）以安全加固为核心——拒绝子 iframe/注入脚本的 origin 伪造（CWE-346）、query string 上限 512KiB/1000 字段、widget state 上限 25MB，并新增全局数据导出禁用开关，适合多品牌敏感看板的生产部署。

> **来源**：Streamlit 官方 Discuss《Version 1.60》+ Release Notes

## 核心要点

1. v1.60 三大 breaking 安全变更：origin 校验（CWE-346）、query string 上限（CWE-770）、`server.maxWidgetStateSize=25MB`（CWE-770）。
2. `client.disableDataExport` 全局隐藏 CSV 导出按钮并禁用只读表剪贴板复制。
3. 交互增强：`st.dataframe` 排序保留行选择、`st.tabs` 支持 `height`、`st.columns` 的 `gap` 支持像素值、`st.metric` 零值显中性灰。
4. 安全修复：NaN/Inf query params 拒绝、Graphviz/PyDeck/link_button/image 危险 URL sanitize、`st.selectbox` 长列表虚拟化。

## 关键配置

| 配置项 | 默认值 | 作用 |
|--------|--------|------|
| `client.disableDataExport` | false | 全局隐藏 CSV 导出 + 禁用只读表剪贴板复制 |
| `server.maxWidgetStateSize` | 25 MB | 单次 rerun widget state payload 上限 |
| query string 上限 | 512 KiB / 1000 字段 | 防无界资源分配 |

## 关联页面
- [[streamlit_dashboard_2026]] — Streamlit 2026 生产级最佳实践（v1.59 起 ButtonColumn/Mermaid/App.run 等）
- [[streamlit_production_dashboard]] — Streamlit 生产级多品牌看板构建实操
- [[multi_brand_unified_analytics]] — 多品牌统一数据分析架构（分析呈现层）
