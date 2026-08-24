# SQL查询优化十大最佳实践（2026版）

> **来源**：GeeksforGeeks, "SQL Query Optimizations - Best Practices", 2026-06-11更新
> **URL**：https://www.geeksforgeeks.org/sql/best-practices-for-sql-query-optimizations/

## 十大最佳实践

### 1. 明智使用索引
```sql
-- 为高频过滤/连接/排序列创建索引
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```
- 主索引：主键自动创建
- 二级索引：手动创建于非主键列
- 聚簇索引：决定物理排列，每表仅一个
- 非聚簇索引：含指针指向数据，可多个
- ⚠️ 索引过多拖慢INSERT/UPDATE/DELETE，需定期审计

### 2. 避免SELECT *
```sql
-- 差
SELECT * FROM products;
-- 好
SELECT product_id, product_name, price FROM products;
```
- 减少内存和网络开销
- 允许数据库跳过不需要的列
- 更利于覆盖索引优化

### 3. WHERE + LIMIT限制行数
```sql
SELECT name FROM customers
WHERE country = 'USA'
ORDER BY signup_date DESC
LIMIT 50;
```

### 4. 高效WHERE子句——避免列上函数
```sql
-- 差：YEAR()阻止索引使用
SELECT * FROM employees WHERE YEAR(joining_date) = 2022;
-- 好：范围查询可用索引
SELECT * FROM employees
WHERE joining_date >= '2022-01-01' AND joining_date < '2023-01-01';
```

### 5. 智能JOIN——先过滤后连接
```sql
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.amount > 100;
```
- 优先INNER JOIN而非OUTER JOIN
- 连接前用WHERE过滤减少数据集

### 6. 避免N+1查询——单次JOIN替代
```sql
-- 差：列表查询+逐条详情
SELECT * FROM users;
-- For each: SELECT * FROM orders WHERE user_id = ?
-- 好：一次JOIN
SELECT u.user_id, u.name, o.order_id, o.amount
FROM users u JOIN orders o ON u.user_id = o.user_id;
```

### 7. EXISTS替代IN（大结果集子查询）
```sql
-- 差：IN需处理全部结果才比较
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);
-- 好：EXISTS找到第一个匹配即停止
SELECT name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

### 8. 避免LIKE前导通配符
```sql
-- 差：%开头禁用索引→全表扫描
SELECT * FROM users WHERE name LIKE '%john';
-- 好：前缀匹配可用索引
SELECT * FROM users WHERE name LIKE 'john%';
```

### 9. 使用EXPLAIN分析执行计划
```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 42;
```
- 识别全表扫描
- 验证索引使用情况
- 指导优化决策

### 10. UNION ALL替代UNION（不需去重时）
```sql
-- 差：UNION自动去重+排序
SELECT col FROM table1 UNION SELECT col FROM table2;
-- 好：UNION ALL跳过去重
SELECT col FROM table1 UNION ALL SELECT col FROM table2;
```

## 服装零售场景对照

| 实践 | 零售SQL场景 | 预期提升 |
|------|-----------|---------|
| FK索引 | 订单表customer_id未索引→JOIN全表扫描 | 100-1000x |
| SELECT列 | 日报只取10列却SELECT * 100列 | 50-90%内存节省 |
| 避免列函数 | `WHERE YEAR(sale_date)=2026` | 索引可用，10-100x |
| N+1消除 | 查店铺列表→逐店查销售额 | 减少N次查询 |
| LIMIT | POS流水表亿级全量→TOP 100 | 秒级→毫秒级 |
