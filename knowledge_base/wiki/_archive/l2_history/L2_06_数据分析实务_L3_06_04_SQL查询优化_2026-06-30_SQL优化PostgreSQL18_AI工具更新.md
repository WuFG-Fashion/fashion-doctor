# SQL优化更新：PostgreSQL 18 + AI工具 + 十大实践（2026-06-30 C轮）

> 本轮更新来自4篇新采集，同步到 wiki/concepts/SQL查询性能优化.md 和 wiki/practices/零售数据仓库SQL实践.md

## 新增内容

### PostgreSQL 18 三大变革（2025-09发布）
- 多列B-tree跳过扫描：索引(A,B)可被仅B的WHERE高效使用
- 异步I/O子系统：分析型大表扫描读性能最高3x
- 并行GIN索引构建：JSONB全文搜索索引并行化

### AI SQL优化工具（2026成熟）
- EverSQL：10万+用户，AI自动建议索引+查询重写
- pgMustard：$79/月 EXPLAIN可视化→可执行建议
- pgai (Timescale)：开源库内AI扩展

### 五步诊断工作流（80%问题解决率）
1. 识别慢查询（pg_stat_statements）
2. EXPLAIN ANALYZE BUFFERS（实际I/O）
3. 找最昂贵操作
4. 添加/修改索引
5. 重新EXPLAIN验证

### 五大SQL反模式
1. SELECT * → 指定列名
2. OR跨列 → UNION ALL
3. WHERE列函数 → 表达式索引
4. N+1 → 单次JOIN
5. JOIN隐式类型转换

### 服装零售对照
| 实践 | 零售SQL场景 | 提升 |
|------|-----------|------|
| FK索引 | 订单表JOIN全表扫描 | 100-1000x |
| 避免列函数 | `WHERE YEAR(sale_date)=2026` | 10-100x |
| EXPLAIN | POS流水表验证执行计划 | 秒→毫秒 |

→ 关联 wiki：[[SQL查询性能优化]]、[[零售数据仓库SQL实践]]
