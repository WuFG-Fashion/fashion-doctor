---
type: source
title: Streamlit v1.59.0 — ButtonColumn、Skeleton、Mermaid、App.run()
tags: [streamlit, dashboard, button_column, skeleton, mermaid, production, dataframe]
sources: [2026-07-22_Streamlit_v1.59.0_ButtonColumn_Skeleton_Mermaid]
aliases: ["Streamlit", "v1.59.0", "ButtonColumn、Skeleton、Mermaid、App.run()", "Streamlit v1.59.0 — ButtonColumn、Skeleton、Mermaid、App.run()"]
confidence: 第三方数据
brand_specific: false
created: 2026-07-22
updated: 2026-07-22
cross_refs: [[streamlit_dashboard_2026]], [[streamlit_production_dashboard]], [[python_dashboard_ecosystem_2026]]
---

# Streamlit v1.59.0 — ButtonColumn、Skeleton、Mermaid、App.run()

> **一句话摘要**: Streamlit v1.59.0(2026.7.6): ButtonColumn表格内按钮、st.skeleton加载骨架屏、st.mermaid_chart流程图、chat_input文件粘贴、App.run()无CLI启动。

> **来源**: [Streamlit 官方 Changelog](https://docs.streamlit.io/en/stable/changelog.html)
> **日期**: 2026-07-22

## 核心要点

1. **ButtonColumn**: st.dataframe/st.data_editor 新增列类型，表内按钮直接触发行级操作
2. **st.skeleton**: 动画加载占位符，替代 spinner+空容器的组合模式
3. **st.mermaid_chart**: 原生支持 Mermaid 图表(流程图/时序图/甘特图)，markdown 也可内嵌
4. **st.chat_input 文件粘贴**: 聊天输入框直接粘贴图片/CSV等文件
5. **st.App.run()**: 支持 `python app.py` 启动，无需 streamlit run CLI
6. **st.fragment 跨容器更新**: Fragment 可更新任意位置元素，不触发全量 rerun
7. **MarkdownColumn**: 表格单元格内渲染 Markdown 文本

## 服装零售场景

| 特性 | 用例 |
|------|------|
| ButtonColumn | 库存表每行"调拨"/会员表每行"触达"按钮 |
| st.skeleton | Dashboard 加载骨架屏，专业 UI |
| st.mermaid_chart | ETL流程图/会员分层图零成本内嵌 |
| chat_input 粘贴 | 导购 AI 助手直接贴销售截图 |
| App.run() | 一键部署到生产环境 |

## 关联页面

[[streamlit_dashboard_2026]] — 生产级最佳实践
[[streamlit_production_dashboard]] — 多品牌看板实操
[[python_dashboard_ecosystem_2026]] — 看板生态对比
