# Pandas 3.0 正式发布 — 重大变革与生态演进

> 来源：Pandas 官方文档（pandas.pydata.org），2026-01-21 首发，最新 3.0.4（2026-06-28）
> URL: https://pandas.pydata.org/pandas-docs/stable/whatsnew/v3.0.0.html

## 概述

Pandas 3.0 于 2026 年 1 月 21 日正式发布，是 Pandas 历史上最大的一次主版本升级。截至 2026 年 7 月已迭代至 3.0.4（6月28日）。核心变化围绕 **Arrow 原生集成**、**Copy-on-Write 默认启用**、**API 现代化**三大方向。

## 版本迭代轨迹

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.0.0 | 2026-01-21 | 首发，重大 API 变更 |
| 3.0.1 | 2026-02-17 | 修复回归问题 |
| 3.0.2 | 2026-03-30 | 增强 + 修复 |
| 3.0.3 | 2026-05-11 | 增强 + 修复 |
| 3.0.4 | 2026-06-28 | 修复回归问题（当前最新） |

## 核心变化

### 1. Arrow-backed Dtypes 默认启用
- 底层存储全面转向 Apache Arrow 列式格式
- 与 Polars、DuckDB 等 Arrow 生态工具实现零拷贝互操作
- 内存占用降低，缓存友好性提升

### 2. Copy-on-Write (CoW) 默认开启
- 解决 Pandas 历史上最令人困惑的"SettingWithCopyWarning"
- 修改 DataFrame 子集时自动创建副本，避免意外修改原始数据
- 内存管理更安全、更可预测

### 3. 性能改进
- 列式存储 + Arrow 后端带来整体性能提升
- 大规模数据集（千万行级）操作显著加速
- 仍在持续优化中（相比 Polars 列式原生引擎仍有差距）

### 4. API 现代化
- 移除多个历史遗留的 deprecated API
- 简化索引操作语义
- 改进类型推断

## 与 Polars 的定位分化

| 维度 | Pandas 3.0 | Polars 1.x |
|------|-----------|------------|
| 底层 | Arrow-backed (新) | Arrow-native (原生) |
| 执行模式 | Eager 为主 | Lazy + Eager |
| 并行 | 有限 | 全自动多线程 |
| 生态 | 最丰富 | 快速增长 |
| 学习曲线 | 低（Python 风格） | 中（Rust API 风格） |
| 适用 | 探索分析、中小数据 | ETL管道、大数据 |

## 对服装零售数据分析的影响

1. **Arrow 互操作** → Pandas 3.0 处理的数据可直接传给 Polars/DuckDB/Streamlit，无需格式转换
2. **CoW 安全** → 分析销售数据时不再担心意外修改原始表
3. **迁移建议** → 存量 Pandas 代码可平滑升级；新项目建议 Polars + Pandas 3.0 混合策略
4. **生态兼容** → Streamlit 1.56 已支持 Pandas 3.x
