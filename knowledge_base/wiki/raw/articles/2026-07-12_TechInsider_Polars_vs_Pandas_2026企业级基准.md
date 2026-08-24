# Polars vs Pandas 2026: 15x Speed Gap — Tech-Insider企业级基准测试

> 来源：https://tech-insider.org/polars-vs-pandas-2026/
> 发布日期：2026-04-22
> 采集日期：2026-07-12

## 核心数据

### 版本现状（2026年4月）
- Polars 1.24.0（2026-04-16发布），流式引擎正式版，原生Iceberg/Delta I/O
- Pandas 2.2.3（2025-01），Pandas 3.0仍处于Alpha（CoW+PyArrow默认延迟）
- Polars周下载280万（+250% YoY），Pandas 1850万
- GitHub星：Polars 32,000（2025年新增5,000），Pandas 42,000

### H2O.ai Group-By基准（16核AMD EPYC, 64GB RAM）

| 任务 | Polars | Pandas | 加速比 |
|------|--------|--------|--------|
| 100万行 group-by 求和 | 0.12s | 1.8s | **15x** |
| 1000万行 group-by 求和 | 0.45s | 12.5s | **28x** |
| 1亿行 group-by 求和 | 4.8s | 138s | **29x** |
| 10亿行 group-by 求和（流式） | 45s | OOM崩溃 | N/A |
| 1000万行 中位数 | 0.9s | 24s | **27x** |

### I/O吞吐量（1GB NYC Taxi）

| 格式 | Polars | Pandas | 加速比 |
|------|--------|--------|--------|
| CSV读取 | 2.5s | 28s | **11x** |
| CSV写入 | 3.1s | 22s | **7x** |
| Parquet读取 | 0.8s | 3.2s | **4x** |
| JSON Lines读取(500MB) | 1.7s | 19s | **11x** |

### TPC-H SF=10

| 查询 | Polars | Pandas | 加速比 |
|------|--------|--------|--------|
| Q1 | 1.2s | 15s | **12.5x** |
| Q5（5表Join） | 2.8s | 48s | **17x** |
| Q7 | 3.4s | 62s | **18x** |

SF=100时Pandas在64GB机器上无法完成；Polars流式25分钟完成全套。

### 内存占用

| 场景 | Polars峰值 | Pandas峰值 | 缩减 |
|------|-----------|-----------|------|
| 10GB CSV解析+聚合 | 2.1GB | 18GB | **8.6x** |
| 50GB Parquet扫描（流式） | 1.8GB | 32GB | **17x** |
| 10亿行 group-by | 4.2GB | 45GB(OOM) | **10x+** |

纯数值数据差距极小（1.07x），差距在字符串和嵌套结构上爆炸。

### VU Amsterdam能源研究（2026年3月，首个同行评审）
- Polars每次等效操作耗电比Pandas少 **3-5倍**
- 每1TB批次：Polars **0.4kWh** vs Pandas **1.6-2.0kWh**
- 每日1TB管道年节电约500kWh

### TCO分析

| 成本项 | Polars | Pandas |
|--------|--------|--------|
| 1TB夜间ETL（本地64GB） | ~$0（单机） | 通常需Spark集群 |
| AWS EC2 1TB Parquet Join | **$3.40/次** | **$18.60/次** |
| Polars Cloud托管 | $0.05/GB扫描 | N/A |

## 企业案例

### GitHub内部ETL
- 数据量：400GB遥测/夜
- 迁移前：r5.8xlarge(128GB)、90分钟
- 迁移后：r5.2xlarge(32GB)、11分钟
- 加速 **8x+**，云成本降 **75%**

### 摩根大通风险建模
- VaR计算：22分钟 → **3分钟**（7.3x），满足SLA(15分钟)
- 探索性研究笔记本保留Pandas

### Cheddar实时分析
- 5000万月会话，Polars流式每90秒运行
- Pandas等效方案需3节点Spark集群

### Netflix推荐管道
- **继续使用Pandas**（研究面向，笔记本<几GB）
- 重聚合由Spark SQL上游处理

### H2O.ai Driverless AI 2026
- 默认引擎改为Polars，端到端 **6x** 改善

## 职位市场（2026年4月）
- Polars职位年增 **+450%**，Pandas +2%
- Polars数据工程师平均薪资 **$171,000**（Pandas $152,000）
- Polars薪资溢价 **$14,000-19,000/年**

## 迁移六步法
1. 审计Pandas使用（分类：重型管道/研究笔记本/库集成）
2. 并行安装 `polars[all]==1.24.0`
3. 先迁移读写层（`pd.read_csv`→`pl.read_csv/scan_csv`）
4. 重写group-by和join（表达式API）
5. 替换apply模式为列表达式（`map_elements`做兜底）
6. 属性测试+基准测试，预期10-30x改善

## 五场景推荐
- <1GB探索笔记本 → Pandas
- >10GB生产ETL → Polars
- 亚分钟实时分析 → Polars
- 学术统计 → Pandas
- 大规模ML特征工程 → Polars+Pandas双轨

## 关键数值速查
- **15-30x**: group-by/join加速
- **10x**: 字符串内存缩减
- **3-5x**: 能效优势
- **75%**: GitHub云成本降幅
- **8x+**: GitHub ETL加速
- **7.3x**: JPMorgan VaR加速
- **$3.40 vs $18.60**: AWS每次TB join成本
- **250%**: Polars年下载增长
- **450%**: Polars职位年增长
