# DuckDB 1.5 + Sirius：GPU加速嵌入式分析数据库的性能革命

> 来源：chenxutan.com（程序员茄子），2026-04-08
> 摘要：DuckDB 1.5.1发布ExtensionKit（C#扩展）+存储格式升级+Parquet Bloom Filter；Sirius GPU扩展利用NVIDIA cuDF实现ClickBench性价比提升7.2x

## 一、DuckDB 1.5 核心新特性

### 1.1 ExtensionKit — C#扩展开发
- 允许用C#编写DuckDB扩展，降低开发门槛
- 复用.NET生态成熟库
- DuckDB从"工具"向"平台"演进

### 1.2 存储格式与压缩升级
- 默认兼容v1.0.x，可选新压缩算法（v1.2.0+存储格式）
- 设计哲学：默认保守，选项激进

### 1.3 Parquet Bloom Filter增强
- 自动应用Bloom Filter跳过不相关数据块
- 百万级日志表中查询性能提升10-100倍

### 1.4 多平台支持
- 新增musl C library（Alpine Linux）原生支持
- 正式支持LoongArch架构

## 二、Sirius GPU加速扩展

### 2.1 架构设计
- 最小侵入原则：不修改DuckDB核心代码
- 复用DuckDB查询解析器和优化器
- Substrait格式作为桥梁（开放标准）
- 零拷贝数据交换（Arrow ↔ cuDF）

### 2.2 执行流程
```
DuckDB解析优化 → Substrait计划 → Sirius格式转换
→ GPU内存传输 → cuDF算子执行 → 结果回传CPU
```

### 2.3 关键技术决策
- 复用DuckDB查询解析器和优化器（务实的工程选择）
- Substrait格式保证互操作性和版本稳定性
- 零拷贝：Sirius格式对齐Arrow，cuDF内部也基于Arrow

## 三、ClickBench性能实测

| 系统 | 相对执行时间 | 性价比提升 |
|------|:-----------:|:---------:|
| Sirius (GPU) | 1.0 | **7.2x** |
| Umbra | 1.3 | - |
| DuckDB (CPU) | 2.1 | - |
| ClickHouse | 2.4 | - |

- 测试平台：NVIDIA GH200 Grace Hopper
- GPU复杂查询（正则/JOIN）优势显著
- Q28正则查询：JIT编译（baseline）vs朴素实现13x slower

### 3.1 局限性
- 字符串操作效率相对较低（Q23）
- Top-N操作需全局排序（Q24/Q26）
- 超大规模聚合受限于GPU显存

## 四、未来规划
- 高级GPU内存管理（动态分区/渐进式溢出/预取优化）
- GPU原生文件读取器（GPU Parquet解码/智能预取）
- 管线化执行模型（算子融合/数据流优化）
- 多节点多GPU扩展（分布式JOIN/PB级处理）

## 五、实战使用
```sql
INSTALL sirius FROM community;
LOAD sirius;
SET sirius.enable_gpu = true;
SET sirius.gpu_device = 0;
SET sirius.cache_tables = true;  -- 重复查询缓存
```

适用场景：大规模聚合、多表JOIN、复杂表达式、重复查询
不适用：小数据集(<100MB)、简单过滤、I/O瓶颈场景
