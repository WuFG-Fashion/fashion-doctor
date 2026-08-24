# Streamlit v1.59.0 发布：ButtonColumn、Skeleton、Mermaid、App.run()

> **来源**: Streamlit 官方 Changelog (docs.streamlit.io/en/stable/changelog.html)
> **日期**: 2026-07-06
> **版本**: v1.59.0

---

## 核心新特性

### 1. ButtonColumn — 在表格内放置按钮
- `st.dataframe` 和 `st.data_editor` 新增列类型 `st.column_config.ButtonColumn`
- 用户可直接在表格行内点击按钮触发操作，无需选中行后在外部按钮
- 服装零售场景：库存表格中每行一个"调拨"按钮、会员列表中每行一个"触达"按钮

### 2. st.skeleton — 加载占位动画
- 新元素 `st.skeleton`，渲染动画加载占位符
- 替代传统 `st.spinner` + 空容器的组合，视觉反馈更流畅
- 服装零售场景：Dashboard 数据加载期间展示骨架屏，提升用户体验

### 3. st.mermaid_chart — 直接在 App 中画流程图
- 渲染 Mermaid 图表（流程图、时序图、甘特图等）
- 同时支持在 `st.markdown` 中内嵌 Mermaid
- 服装零售场景：在数据看板中嵌入 ETL 流程图、会员生命周期图、组织架构图

### 4. st.chat_input 文件粘贴 + submit_mode
- 聊天输入框支持直接粘贴文件（图片、CSV 等）
- 新增 `submit_mode` 参数控制提交后行为（如显示停止按钮或禁用输入）
- 服装零售场景：导购 AI 陪练中直接粘贴销售报表截图

### 5. st.App.run() — 不再需要 streamlit run
- 支持 `python app.py` 或 `uv run app.py` 直接启动
- 无需 CLI 命令，降低部署门槛
- 支持 `st.App` 自定义脚本错误处理

### 6. st.fragment 跨容器更新
- Fragment 现在可以更新 App 中任何部分的元素（包括 Fragment 创建之前定义的元素）
- 不触发全量 rerun，性能优化显著

### 7. 其他重要更新
- **MarkdownColumn**: st.dataframe 支持在单元格内渲染 Markdown
- **st.set_page_config**: `initial_sidebar_state="locked"` 锁定侧边栏不可切换
- **Widget persist_state**: 更细粒度控制 widget 状态跨 rerun 保留
- **st.camera_input resolution**: 控制拍摄分辨率
- **VegaLite 原生 resize API**: 图表容器尺寸变化时渲染更快

## 已移除
- 弃用的 Snowpark 连接类型已移除（迁移到支持的连接类型）
- 弃用的 `st.bokeh_chart` 已移除（使用 streamlit-bokeh 组件）

## 服装零售场景价值

| 特性 | 服装零售用例 | 收益 |
|------|-------------|------|
| ButtonColumn | 库存/会员表格行内操作 | 减少 2 步点击，体验提升 |
| st.skeleton | 多品牌 Dashboard 加载 | 专业级 UI，降低感知等待 |
| st.mermaid_chart | ETL 流程图、会员分层图 | 零成本可视化文档 |
| chat_input 文件粘贴 | 导购 AI 助手传图 | 培训场景交互更自然 |
| App.run() | 一键部署到生产 | 运维简化 |
| Fragment 跨容器 | Dashboard 局部刷新 | 性能提升 |
