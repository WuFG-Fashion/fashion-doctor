# v2.1 逻辑分层字段回填报告

- 日期：2026-09-12
- 模式：批量回填（只增不改，幂等）
- 改动文件数：124；已合规跳过：2190

| 目录 | 文件数 | 补字段数 |
|---|---|---|
| 10_web/articles | 124 | 857 |

## 口径

- entities T2/brand/slow+180d; concepts T1/public/evergreen+180d 复核
- sources T2，scope 取 brand_specific；confidence=财报 → slow+180d，其余 fast+90d
- comparisons T1/public/slow+180d 复核（沿 S 轮约定）; practices/playbooks T1/public/evergreen+180d 复核
- 10_web/articles T3，文件名命中 focus_brands → brand 否则 public，fast+90d
- as_of 取 文件名日期→updated→created→mtime；全部 status: active（不判过期，由 TTL 引擎后续校准）
