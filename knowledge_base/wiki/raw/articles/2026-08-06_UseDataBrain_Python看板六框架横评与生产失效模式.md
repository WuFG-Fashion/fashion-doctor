# Python 看板六框架横评与生产三大失效模式（2026）

**采集日期**：2026-08-06
**来源**：
- UseDataBrain《Python Dashboard: The Complete 2026 Guide (Streamlit, Dash, Gradio)》https://www.usedatabrain.com/how-to/create-python-dashboard
- UseDataBrain《Streamlit vs Dash in 2026: Which Python Dashboard Framework to Use》
- Streamlit 官网（Snowflake 托管，三种部署入口）
- dev.to《Beyond the Basics: Streamlit, Dash, and Bokeh for Interactive Dashboards》
- CSDN《Streamlit 和 Dash 都是 Python 中用于快速构建数据可视化 Web 应用的开源框架》

---

## 一、六框架横评（2026）

| 框架 | 交付周期 | 最适合 | 什么时候会崩 |
|------|---------|-------|------------|
| **Streamlit** | 1–3 天 | 内部数据科学看板、原型，速度重于控制力的场景 | 多用户状态、细粒度交互、渲染超过 5 万点 |
| **Dash (Plotly)** | 1–2 周 | 企业级分析、多页应用、精细回调控制、大表用 AG Grid | 学习曲线陡；组件超过约 30 个后回调链难以管理 |
| **Gradio** | 1–2 天 | AI/LLM 看板、模型演示、聊天 UI、Hugging Face Spaces | 任何不像"模型演示"形状的东西（无真正网格布局、图表支持稀疏） |
| **Reflex** | 2–4 周 | 纯 Python 全栈应用且想要 React 级前端 | 生态较小；SSR + 状态模型有尖角 |
| **Panel (HoloViz)** | 1–2 周 | 科学计算看板（HoloViews / Bokeh / Datashader 管道） | 不如 Streamlit/Dash 流行 → 社区小、可查答案少 |
| **NiceGUI** | 1 周 | 既要看板又要表单的内部工具 | 小众，但在成长 |

**简单规则**：默认选 Streamlit。能用 Streamlit 出货就用。撞上 Streamlit 的 rerun 模型、需要多页企业应用、或需要 AG Grid 承载数十万行表格时，再换 Dash。看板本质是 AI/LLM 演示时选 Gradio。**如果是 SaaS 产品内面向客户的多租户分析界面，就别自建**——嵌入 Databrain/Metabase 类平台 1–5 天出货，自建多租户 Python 看板要 4–8 周的管道工作。

## 二、版本与环境基线

- **Streamlit 1.55 为 2026 年 4 月当前稳定版**；在 Snowflake 主导下**每两周发一次版**；硬性最低 Python 3.10
- 推荐环境：Python 3.13 + pandas 3.x + Plotly 6.x
- **pandas 3.0 让 Copy-on-Write 成为默认且唯一模式**——静默重渲染的 CoW 收益现在无需任何 flag 即可白拿
- **Plotly 6.x（2025 年 4 月）相对 5.x 有破坏性变更**，老代码需按 v6 迁移指南改
- 安装：`pip install "streamlit>=1.55" "pandas>=2.2" "plotly>=6"`

Streamlit 官方三条入口：浏览器 Playground 试用 → Streamlit Community Cloud（仅公开应用，完全免费，只需 GitHub 账号）→ Snowflake（无限私有应用，企业级可靠性与安全）。

## 三、Streamlit vs Dash 六维对决

### 1. 表格层：Dash 胜

- Streamlit `st.dataframe` 用 Apache Arrow + glide 渲染表格，**约 1 万行表现良好，超过 5 万行崩溃**
- Dash 原生 `dash-table` 类似，1 万行以内可以，超过就吃力
- **Dash AG Grid（`pip install dash-ag-grid`）可处理 10 万行以上**，带排序/过滤/透视/分组，浏览器无压力
- 纯 Streamlit 没有等价物，最接近的 `streamlit-aggrid`（第三方）能用但维护不够活跃

**结论**：看板重心是大表 → Dash + AG Grid；重心是图表和 KPI → 两者性能相同。

### 2. 多用户会话处理：Dash 胜（生产 #1 坑）

Streamlit 的 `st.session_state` 是按会话隔离的，**但模块级全局变量（文件顶部的 `df = pd.read_csv(...)`）在同一进程内的所有会话之间共享**。改动其一，所有用户都会看到。

> 这是一个常见的生产 bug——你写下看起来很干净的代码，部署后一个用户的筛选选择泄漏进另一个用户的视图。

Dash 的回调按设计是无状态的：每个回调只收到它声明的输入值；每用户状态放在作用域限定于用户浏览器会话的 `dcc.Store` 组件里。**若要上多用户生产流量，这是考虑 Dash 而非 Streamlit 的头号理由**。

### 3. 部署：Streamlit 胜（业余/内部），生产打平

- Streamlit：推 GitHub → Community Cloud 免费层 → 点击 Deploy；Hugging Face Spaces 同样一键。生产环境用 Docker，**注意 `streamlit run` 不是多进程的——只能横向多实例扩展**
- Dash：gunicorn + Render / Fly.io / 自建 K8s；或付费 Dash Enterprise（托管部署 + SSO + RBAC + 版本控制）。首次部署摩擦略大，但因为 Dash 就是普通 Flask 应用，生产扩展更干净

### 4. 生态与组件库

- Dash 胜在企业组件：Dash AG Grid、Dash Mantine、Dash Bootstrap、Dash Cytoscape（图可视化）、Dash Bio、Dash DAQ（仪表盘）、Dash Enterprise
- Streamlit 胜在社区与 AI 集成：streamlit-extras、streamlit-authenticator、streamlit-aggrid，以及 Hugging Face 上大量 LangChain / LLM 形状的社区组件

### 5. 动态更新机制

- Streamlit：`st.session_state` + `@st.cache_data` / `@st.cache_resource`；第三方 `st.autorefresh()` 或 `st.empty()` + 轮询（适合低频实时）。默认无原生 WebSocket，高并发/复杂状态需谨慎
- Dash：原生 `dcc.Interval` 定时轮询；可集成 Flask-SocketIO 或自定义 API 做 WebSocket 推送；`dash.long_callback` 支持异步/后台任务

### 6. 数据规模的现实主义

> 大多数教程用 3 行玩具数据演示看板，然后当用户的 5 万行生产数据卡住时表现得很吃惊。

正确做法：**一开始就生成 5 万行真实规模的 CSV**，让缓存与图表渲染行为匹配现实。参考实现含 4 个 KPI 卡片、收入折线图、区域柱状图、Top 客户表和 5 万行样本数据集。

## 四、什么时候两个都不该选

| 场景 | 该用什么 | 原因 |
|------|---------|------|
| AI/LLM 看板（聊天 UI、模型演示） | Gradio | 形状天生契合，在 HF Spaces 上渲染更好 |
| 需要 React 级前端行为的纯 Python 全栈 | Reflex | 全栈写 Python 编译成 React，社区小、边角锋利 |
| 面向客户的多租户 SaaS 分析 | 嵌入式分析平台（Databrain/Metabase/Cube） | 自建要花 4–8 周做 auth + RBAC + 多租户 + 导出 + 定时邮件层 |
| 静态报表（PDF、周报邮件） | Quarto 或 Jupyter 管道 | "渲染成 PDF 每周发邮件"用实时看板框架是杀鸡用牛刀 |

## 五、Streamlit → Dash 迁移剧本

**何时迁移**：
1. 模块级全局状态冲突已在生产咬人
2. 需要 AG Grid 处理 5 万行以上表格
3. 需要"这个筛选只更新这三张图"的细粒度控制
4. 需要在回调层强制执行按用户 RBAC

**迁移基本是机械的**：
- 组件平移：`st.selectbox` → `dcc.Dropdown`、`st.slider` → `dcc.Slider`、`st.date_input` → `dcc.DatePickerRange`、`st.metric` → 样式化 `html.Div`、`st.plotly_chart` → `dcc.Graph`
- 渲染逻辑包进 `@callback`，每个筛选一个 `Input(...)`，每张图/KPI 一个 `Output(...)`

## 六、Bokeh 的定位（第三条路）

Bokeh 专注为现代浏览器生成高性能交互可视化，强项是对每个图表元素的颗粒化控制，适合大数据集、流式数据与高度定制的可视化；弱点是构建完整看板布局时更啰嗦。

## 采集人评估

- 时效性：★★★★★（Streamlit 1.55 / 2026-04 基线，pandas 3.x / Plotly 6.x 组合）
- 可信度：★★★★☆（独立技术媒体横评 + 官方文档交叉）
- 与多品牌看板项目的相关性：★★★★★（本项目正是 Streamlit 多 Tab 看板，多用户状态泄漏与大表阈值是直接风险）
- 可操作性：★★★★★（含阈值、迁移剧本与"不该自建"边界）
