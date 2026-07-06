# Polars vs Pandas：2026年15x加速+企业级案例

> 来源：Tech Insider，2026-04-22
> URL：https://tech-insider.org/polars-vs-pandas-2026/

## 测试环境

| 项目 | 详情 |
|------|------|
| Polars版本 | 1.24.0 (2026-04-16) |
| Pandas版本 | 2.2.3 (2025-01) |
| 硬件 | 16核AMD EPYC，64GB RAM |
| Pandas优化 | PyArrow后端已启用 |

## H2O.ai GroupBy基准

| 测试任务 | Polars 1.24.0 | Pandas 2.2.3 | 加速比 |
|----------|-------------|-------------|:---:|
| 100万行，按ID求和 | 0.12s | 1.8s | **15x** |
| 1000万行，按ID求和 | 0.45s | 12.5s | **28x** |
| 1亿行，按ID求和 | 4.8s | 138s | **29x** |
| 10亿行，按ID求和(流式) | 45s | OOM崩溃 | N/A |
| 1000万行，按两列求中位数 | 0.9s | 24s | **27x** |

## TPC-H基准（SF=10，10GB）

| 查询 | Polars | Pandas | 加速比 |
|------|--------|--------|:---:|
| Q1 | 1.2s | 15s | 12.5x |
| Q5（5表join） | 2.8s | 48s | 17x |
| Q7 | 3.4s | 62s | 18x |
| Inner Join 1亿×1亿 | 8s | 120s | 15x |
| 窗口函数 | 2.3s | 38s | 16x |

## I/O吞吐量

| 操作 | Polars 1.24 | Pandas 2.2.3 | 加速比 |
|------|------------|-------------|:---:|
| CSV读取1GB | 2.5s | 28s | **11x** |
| CSV写入1GB | 3.1s | 22s | **7x** |
| Parquet读取1GB | 0.8s | 3.2s | **4x** |
| JSON Lines读取500MB | 1.7s | 19s | **11x** |

## 能源效率（VU Amsterdam 2026-03）

| 指标 | Polars | Pandas |
|------|--------|--------|
| 每1TB批次能耗 | 0.4 kWh | 1.6-2.0 kWh |
| 能效比 | 基准 | 3-5x更高能耗 |

## 企业案例

| 企业 | 场景 | 迁移前(Pandas) | 迁移后(Polars) | 收益 |
|------|------|---------------|---------------|------|
| GitHub | 夜间ETL 400GB遥测 | 128GB r5.8xlarge/90min | 32GB r5.2xlarge/11min | 成本-75%/窗口8x+ |
| JPMorgan | 盘中VaR风险建模 | 22min(超15min SLA) | 3min(同硬件) | 满足SLA |
| Cheddar | 5000万月会话流式 | 需3节点Spark集群 | Polars单机90秒 | 架构简化 |
| Netflix | 推荐管道 | 重聚合Spark SQL | Polars+Spark协同 | 双轨制 |
| H2O.ai | AutoML | 基准线 | 端到端6x墙钟提升 | 6x加速 |

## TCO对比

| 维度 | Polars | Pandas |
|------|--------|--------|
| 许可证 | MIT免费 | BSD-3免费 |
| 1TB ETL AWS成本 | $3.40/次 | $18.60/次(8x实例) |
| 安装量(周) | 280万 | 1850万 |

## 2026年最终结论

- **<1GB + scikit-learn生态** → Pandas仍是最佳选择
- **>1GB + 生产ETL/实时分析/金融建模** → Polars是明确2026赢家
- **最务实策略** → 双轨制：Polars做重型引擎，Pandas做ML生态胶水，Arrow零拷贝串联
