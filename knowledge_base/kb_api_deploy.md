# Fashion Doctor 知识库 API — 专机部署报告

> **目标机器**：专机（24小时不关机，已安装 WorkBuddy）
> **日期**：2026-06-06
> **前置条件**：已 clone `https://github.com/WuFG-Fashion/fashion-doctor.git`

---

## 专机 WorkBuddy 执行指令

```
请按顺序逐条执行以下命令。遇到错误立即停止并报告。
每完成一步，用 automation_update 模式确认状态。

## 第0步：拉取最新代码

cd C:\Users\MacBookPro\Fashion Doctor
git pull origin main

然后验证关键文件存在：
knowledge_base\kb_api.py
knowledge_base\kb_benchmarks.json
knowledge_base\brand_configs\peacebird.toml

三个文件都存在才能继续。

## 第1步：安装 Python 依赖

用 managed Python 安装依赖，使用项目自带的环境隔离：

C:\Users\MacBookPro\.workbuddy\binaries\python\versions\3.13.12\python.exe -m venv C:\Users\MacBookPro\.workbuddy\binaries\python\envs\kb-api
C:\Users\MacBookPro\.workbuddy\binaries\python\envs\kb-api\Scripts\pip.exe install fastapi uvicorn toml

验证安装成功：
C:\Users\MacBookPro\.workbuddy\binaries\python\envs\kb-api\Scripts\python.exe -c "import fastapi; import uvicorn; import toml; print('依赖安装成功')"

## 第2步：测试 API 启动

先手动启动一次，确认没有报错：

cd C:\Users\MacBookPro\Fashion Doctor\knowledge_base
C:\Users\MacBookPro\.workbuddy\binaries\python\envs\kb-api\Scripts\python.exe kb_api.py --prod

看到 "Fashion Doctor 知识库 API 启动" 日志后，新开一个终端测试：

curl http://localhost:8899/v1/health?api_key=kb_readonly_2026

返回 {"ok": true, "data": {"status": "ok"}} 即成功。

然后 Ctrl+C 停掉。

## 第3步：安装 NSSM（Windows 服务管理器）

NSSM 把 Python 进程注册为 Windows 服务，崩了自动重启，开机自启。

先从官网下载：
https://nssm.cc/download

解压后把 nssm.exe 放到 C:\Windows\System32\ 下（PATH 可访问）。

然后以管理员身份打开终端（必须管理员！），执行：

nssm install FashionDoctorKB

在弹出的 GUI 中填写：
- Application Path: C:\Users\MacBookPro\.workbuddy\binaries\python\envs\kb-api\Scripts\python.exe
- Startup directory: C:\Users\MacBookPro\Fashion Doctor\knowledge_base
- Arguments: kb_api.py --prod
- Service name: FashionDoctorKB

Details 选项卡：
- Display name: Fashion Doctor 知识库 API
- Startup type: Automatic

Exit actions 选项卡（崩溃自动重启的关键！）：
- On exit: Restart
- Restart delay: 5000 ms (5秒)

I/O 选项卡（日志）：
- Redirect stdout: C:\Users\MacBookPro\Fashion Doctor\.workbuddy\logs\kb_api_stdout.log
- Redirect stderr: C:\Users\MacBookPro\Fashion Doctor\.workbuddy\logs\kb_api_stderr.log

点击 Install service。

## 第4步：启动服务并验证

nssm start FashionDoctorKB
nssm status FashionDoctorKB     # 应该显示 SERVICE_RUNNING

等待 5 秒后测试：
curl http://localhost:8899/v1/health?api_key=kb_readonly_2026

应返回 200 OK。

再测试几个核心接口：
curl "http://localhost:8899/v1/thresholds/monthly_turnover?api_key=kb_readonly_2026"
curl "http://localhost:8899/v1/competitors/peacebird?api_key=kb_readonly_2026"
curl "http://localhost:8899/v1/competitors/peacebird/gross_margin_q1_2026?api_key=kb_readonly_2026"
curl "http://localhost:8899/v1/guides/benchmarks?api_key=kb_readonly_2026"
curl "http://localhost:8899/v1/abc/benchmarks?api_key=kb_readonly_2026"
curl "http://localhost:8899/v1/vip/benchmarks?api_key=kb_readonly_2026"
curl "http://localhost:8899/v1/knowledge/search?q=沉睡唤醒&api_key=kb_readonly_2026"
curl "http://localhost:8899/v1/knowledge/sql/滞销?api_key=kb_readonly_2026"

全部返回 200 即可。

## 第5步：模拟崩溃恢复

看门狗验证——手动杀掉进程，看 NSSM 是否自动拉起来：

nssm stop FashionDoctorKB
# 等 5 秒
nssm status FashionDoctorKB     # 应该变 SERVICE_STOPPED

nssm start FashionDoctorKB
curl http://localhost:8899/v1/health?api_key=kb_readonly_2026  # 应该正常

再暴力测试：找到 python.exe 进程 PID，taskkill 杀掉
nssm status FashionDoctorKB     # 5 秒后应该自动变 SERVICE_RUNNING

## 第6步：写入 .workbuddy/memory/ 记录

在 .workbuddy/memory/YYYY-MM-DD.md 中记录：
- NSSM 服务名：FashionDoctorKB
- 端口：8899
- API Key：kb_readonly_2026（生产环境改环境变量 KB_API_KEY）
- Python 路径：...
- 日志路径：.workbuddy/logs/kb_api_*.log

## 第7步：Git 推送所有新增文件

将新增的 kb_api.py、kb_benchmarks.json、brand_configs/ 全部提交：

cd C:\Users\MacBookPro\Fashion Doctor
git add knowledge_base/kb_api.py knowledge_base/kb_benchmarks.json knowledge_base/brand_configs/ .workbuddy/logs/
git commit -m "知识库API服务部署完成 — FastAPI + NSSM + 品牌配置"
git push
```

---

## API 使用手册（发给调用方）

### 快速上手

```python
import requests

BASE = "http://专机IP:8899"
KEY = "kb_readonly_2026"

# 查行业基准
r = requests.get(f"{BASE}/v1/benchmarks/2026q1", params={"api_key": KEY})
print(r.json())

# 查太平鸟毛利率
r = requests.get(f"{BASE}/v1/competitors/peacebird/gross_margin_q1_2026", params={"api_key": KEY})
print(r.json())  # → 0.6287

# 查月周转优秀线（带品牌覆盖）
r = requests.get(f"{BASE}/v1/thresholds/monthly_turnover", params={"api_key": KEY, "brand": "peacebird"})
print(r.json())  # → excellent: 1.3（太平鸟自定义），而非 1.5（通用）

# 搜知识库
r = requests.get(f"{BASE}/v1/knowledge/search", params={"q": "沉睡唤醒", "api_key": KEY})
print(r.json())
```

### 所有端点速查

| 端点 | 用途 |
|------|------|
| `/v1/health` | 健康检查 |
| `/v1/thresholds` | 全部阈值 |
| `/v1/thresholds/{name}?brand=xxx` | 指定阈值 |
| `/v1/benchmarks` | 行业基准 |
| `/v1/benchmarks/{name}` | 指定基准 |
| `/v1/competitors` | 竞品列表 |
| `/v1/competitors/{brand}` | 竞品完整数据 |
| `/v1/competitors/{brand}/{metric}` | 竞品特定指标 |
| `/v1/guides/benchmarks` | 导购分析基准 |
| `/v1/abc/benchmarks` | ABC分析基准 |
| `/v1/vip/benchmarks` | VIP分析基准 |
| `/v1/knowledge/search?q=xxx` | 知识搜索 |
| `/v1/knowledge/sql/{template}` | SQL模板 |
| `/v1/categories` | 品类列表 |
| `/v1/brands` | 品牌列表 |

### 添加新品牌

在 `knowledge_base/brand_configs/` 下新建 `品牌名.toml`，参考 `peacebird.toml` 格式。

API 会自动识别，无需重启服务（懒加载）。
```

## 运维命令速查

```bash
# 查看服务状态
nssm status FashionDoctorKB

# 启动
nssm start FashionDoctorKB

# 停止
nssm stop FashionDoctorKB

# 重启
nssm restart FashionDoctorKB

# 查看日志
tail -f .workbuddy/logs/kb_api_stdout.log

# 更新代码后重启（知识库更新会自动热加载 kb_benchmarks.json）
git pull && nssm restart FashionDoctorKB

# 卸载服务（需要时）
nssm remove FashionDoctorKB confirm
```
