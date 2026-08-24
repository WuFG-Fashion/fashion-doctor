# Streamlit v1.59.0 发布：ButtonColumn、Mermaid、文件粘贴

> 来源：https://docs.streamlit.io/en/stable/changelog.html + https://www.change8.dev/package/streamlit
> 发布日期：2026-07-06 (v1.59.0), 2026-07-08 (v1.59.1)
> 采集日期：2026-07-12

## v1.59.0 核心新特性（2026-07-06）

### ButtonColumn（column_config新增）
- 在st.dataframe中新增 `ButtonColumn` 列类型
- 支持在表格行内嵌入操作按钮，实现行级交互

### 文件粘贴到chat_input
- `st.chat_input` 新增支持直接粘贴文件（图片/文档）
- 用户可以Ctrl+V粘贴文件到聊天输入框

### Mermaid图表支持
- `st.markdown` 新增原生Mermaid图表渲染
- 无需第三方组件即可在Streamlit中绘制流程图、架构图

## v1.59.1 修复（2026-07-08）
- 修复查询参数在空query string时的崩溃问题

## v1.58.0 回顾（2026-05-28）

### 核心新特性
- **并行Fragment**: `@st.fragment(parallel=True)`，Fragment并发运行，支持后台类工作流
- **st.pagination**: 原生分页组件，用于DataFrame等分页界面
- **streamlit skills CLI**: 新的CLI命令，用于安装AI agent技能

### 重要变更
- `st.App` 自定义脚本错误处理
- `st.expander`/`st.status` 新增 `type` 参数（紧凑样式）
- 移除LangChain回调处理集成
- OAuth PKCE恢复、30天cookie持久化恢复

## v1.57.0 里程碑（2026-04-29）
- **Starlette正式化**: 默认服务器从Tornado切换到Starlette/Uvicorn
- **st.bottom**: 底部固定容器，适合聊天输入、工具栏
- **:shimmer[]** 动画加载文本
- **Polars零拷贝**: 直接Polars→Arrow转换，绕过Pandas
- **st.App ASGI入口**: 可挂载到FastAPI/Starlette

## 版本路线（2026年至今）

| 版本 | 日期 | 关键特性 |
|------|------|----------|
| v1.59.0 | 07-06 | ButtonColumn、Mermaid、文件粘贴到chat_input |
| v1.58.0 | 05-28 | 并行Fragment、st.pagination、skills CLI |
| v1.57.0 | 04-29 | Starlette正式化、st.bottom、Polars零拷贝、:shimmer[] |
| v1.56.0 | 03-31 | st.navigation增强、Python 3.14支持 |
| v1.55.0 | 03-03 | 查询参数widget绑定、动态容器on_change |
| v1.54.0 | 02-04 | widget绑定query params、动态option配置 |
| v1.53.0 | 01-14 | Markdown指标/slider、sidebar宽度配置 |

## 生产部署要点
- Starlette/ASGI架构（v1.57+）：更好性能、支持FastAPI挂载
- 并行Fragment（v1.58+）：独立并发渲染，适合后台任务
- Polars零拷贝（v1.57+）：大数据场景性能提升
- Mermaid图表（v1.59+）：无需第三方组件做架构图
