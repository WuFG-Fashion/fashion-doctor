# PostgreSQL 2026 性能调优完整清单

> 来源：https://dev.to/_d7eb1c1703182e3ce1782/postgresql-performance-tuning-checklist-2026-complete-guide-65a
> 采集日期：2026-07-09
> 作者：dev.to 社区（2026年3月）

## 硬件与OS调优

| 项目 | 建议 |
|------|------|
| shared_buffers | 25% RAM（64GB→16GB） |
| effective_cache_size | 50-75% RAM（64GB→48GB） |
| 磁盘 | NVMe SSD + XFS + noatime |
| vm.swappiness | 1（让PG管理内存） |

## 核心配置（64GB RAM专用服务器）

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| work_mem | OLTP: 16-64MB, 分析型: 256MB-1GB | 每个排序/哈希操作 |
| maintenance_work_mem | 1-2GB | VACUUM/CREATE INDEX |
| random_page_cost | 1.1 (SSD) | 默认4.0=机械硬盘 |
| effective_io_concurrency | 200 (SSD) | 默认1 |
| max_parallel_workers_per_gather | 4 | 并行查询进程 |

## 索引策略

- B-tree：最常用，复合索引选择性高列在前
- 覆盖索引（INCLUDE）：实现Index-Only Scan
- 部分索引：仅索引活跃数据（跳过95%已完成订单）
- GIN索引：全文搜索、JSONB、数组
- GiST索引：几何数据、范围类型

## 五大查询反模式

| 反模式 | 正确做法 |
|--------|---------|
| WHERE EXTRACT(YEAR FROM col)=2026 | WHERE col>='2026-01-01' AND col<'2027-01-01' |
| WHERE user_id='42'（隐式类型转换） | WHERE user_id=42 |
| SELECT * | 仅取所需列 |
| WHERE id NOT IN(SELECT...) | WHERE NOT EXISTS(SELECT 1...) |
| LIMIT 20 OFFSET 100000 | WHERE id>100000 ORDER BY id LIMIT 20 |

## 连接池

- PgBouncer transaction模式：25个服务端连接→1000+客户端
- 每个PG连接消耗5-10MB RAM

## VACUUM调优

- autovacuum_vacuum_scale_factor: 0.2→0.05（更快触发）
- 高写入表单独设置scale_factor=0.01
- 使用pg_partman自动分区管理

## 监控

- pg_stat_statements（最重要）：周度审查最慢查询
- pgBadger日志分析：记录>100ms的查询
- 性能测试：pgbench最少10分钟，一次只改一个参数

## 关键数值

- shared_buffers > 40% RAM反而有害
- SSD下random_page_cost = 1.1（非默认4.0）
- 100万行表默认需200,050死元组才触发VACUUM（太晚）
- 分区表用DROP TABLE替代DELETE（避免大量WAL和死元组）
