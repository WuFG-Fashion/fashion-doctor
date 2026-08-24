# Streamlit 2026 H2 关键架构升级：Starlette正式化、Polars零拷贝、并行Fragment

> 来源：Streamlit官方Release Notes (docs.streamlit.io)，汇总v1.53-v1.58
> 摘要：2026年Streamlit完成史上最大架构升级——Tornado→Starlette/Uvicorn（v1.57正式默认），Polars Arrow零拷贝直传，@st.fragment(parallel=True)并发执行

## 一、Starlette架构迁移 — 2026年最大底层变更

### 时间线
- **v1.53 (2026-01-14)**：实验性引入`server.useStarlette`配置+`st.App` ASGI入口
- **v1.57 (2026-04-29)**：Starlette/Uvicorn正式替代Tornado成为默认Web服务器
- **v1.58 (2026-05-28)**：`st.App`支持自定义脚本错误处理

### 核心能力
- ASGI兼容性（可与FastAPI/Starlette等现代Python Web框架集成）
- 自定义HTTP路由、中间件、生命周期钩子
- `st.App`可直接在`st`命名空间使用
- `st.App`新增`secrets`参数（编程式传递，不依赖secrets.toml）

## 二、Polars Arrow零拷贝（v1.57）

- Polars DataFrame完全绕过pandas直接转换为Arrow格式
- 提升类型保真度，消除转换开销
- 与pandas 3.x ArrowStringArray原生兼容

## 三、@st.fragment(parallel=True) — 并发革命（v1.58）

```python
@st.fragment(parallel=True)
def background_analysis():
    # 多个片段可同时执行，不阻塞主UI
    heavy_computation()
    st.metric("Result", result)

@st.fragment(parallel=True)
def real_time_chart():
    # 独立的数据刷新区
    data = fetch_live_data()
    st.line_chart(data)
```

- 支持片段并发运行
- 实现响应式应用和后台工作流
- 多品牌看板中各品牌Tab可独立并行刷新

## 四、v1.58 全新组件

### st.pagination — 分页组件
```python
page = st.pagination("Select page", total=100, page_size=10)
# 返回当前页码，无需手动管理offset/limit
```

### streamlit skills CLI（v1.58）
- 捆绑AI代理开发技能到pip包中

## 五、其他关键增强

| 版本 | 特性 | 影响 |
|------|------|------|
| v1.56 | pandas 3.x正式支持 | ArrowStringArray/延迟注解(PEP 649) |
| v1.56 | st.menu_button | 导航菜单新组件 |
| v1.56 | selectbox/multiselect搜索过滤 | 长列表UX大幅改善 |
| v1.57 | st.bottom固定底部容器 | 底部状态栏/进度条 |
| v1.57 | :shimmer[]动画加载 | UI品质感提升 |
| v1.57 | CSS Color Level 4 | oklch/lab等现代色彩空间 |
| v1.55 | Widget bind参数 | 简化widget状态与查询参数同步 |
| v1.55 | dynamic_container on_change | 动态容器回调 |
| v1.53 | 会话级缓存 | st.cache_data/resource会话作用域 |

## 六、移除与弃用
- v1.54：移除experimental_get/set_query_params（→st.query_params）
- v1.57：移除plotly_chart/vega_lite_chart的spec等参数
- v1.58：移除element.add_rows、LangChain回调处理器

## 七、对多品牌看板的实操意义

1. **Starlette迁移**：部署时可充分利用ASGI中间件（认证、限流、CORS）
2. **Polars零拷贝**：品牌数据从Polars DataFrame到Streamlit展示零转换开销
3. **parallel fragment**：各品牌Tab独立并行刷新，大看板不再"一卡全卡"
4. **pagination**：SKU列表/会员分页展示，替代手动limit/offset
