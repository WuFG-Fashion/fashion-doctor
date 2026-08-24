---
title: Streamlit v1.60 安全加固与企业级部署（2026-07-21）
source: Streamlit 官方 Discuss《Version 1.60》+ Release Notes
url: https://discuss.streamlit.io/t/version-1-60/122051, https://docs.streamlit.io/en/stable/changelog.html
date: 2026-07-28
tags: [streamlit, security, production, dashboard, hardening, v1.60]
---

# Streamlit v1.60 安全加固与企业级部署

## 核心要点

1. **v1.60 发布日期 2026-07-21**，是继 v1.59(2026-07-06) 后的安全与稳定性重点版本，包含多项 breaking 安全变更。
2. **三大安全加固（breaking changes）**：
   - 拒绝来自子 iframe 或注入脚本的 host 消息，防止 origin spoofing（CWE-346）。
   - 客户端 query string 上限 **512 KiB / 1000 字段**，防止无界资源分配（CWE-770）。
   - 新增 `server.maxWidgetStateSize` 配置（默认 **25 MB**），限制每次 rerun 客户端可发送的 widget state payload，防范超大 widget / 自定义组件 payload（CWE-770）。
3. **数据导出管控**：`client.disableDataExport` 全局禁用数据导出——`st.dataframe` / `st.data_editor` 的 CSV 导出按钮隐藏，只读 dataframe 剪贴板复制被禁用。
4. **交互增强**：`st.dataframe` 排序后保留行选择；`st.tabs` 新增 `height` 参数；`st.columns` 的 `gap` 参数支持整数像素值；`st.data_editor` 在 `num_rows="fixed"` 时用 `key` 作主行标识；`st.metric` 零值显示中性灰；Vega-Lite action 按钮整合进原生 toolbar。

## 关键配置与安全数据

| 配置项 | 默认值 | 作用 |
|--------|--------|------|
| `client.disableDataExport` | false | 全局隐藏 CSV 导出 + 禁用只读表剪贴板复制 |
| `server.maxWidgetStateSize` | 25 MB | 单次 rerun widget state payload 上限 |
| query string 上限 | 512 KiB / 1000 字段 | 防无界资源分配 |
| origin 校验 | 启用 | 拒绝子 iframe/注入脚本 host 消息（CWE-346） |

## 其他修复

- 非有限浮点（NaN/Inf）query params 被拒绝；Graphviz 链接、PyDeck tooltip、link_button、image 中危险 URL 被 sanitize；`st.selectbox` 长列表虚拟化。
- `st.tabs` 面板在 widget rerun 后不再视觉堆叠；React Aria dialog 多弹窗正确堆叠；PyArrow 25 线程初始化崩溃规避。

## 服装零售多品牌看板生产启示

- 多品牌经营看板常含销售/会员/毛利敏感数据，`client.disableDataExport` + `maxWidgetStateSize` + origin 校验三者组合可满足零售数据安全合规与防注入要求。
- 部署建议：在 `config.toml` 设 `client.disableDataExport = true`；将应用置于 Nginx/Auth0/Cloudflare Access 之后；明确标注时区与生产环境只读策略。
