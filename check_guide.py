"""检查李志婕的详细数据"""
import sqlite3
conn = sqlite3.connect('C:/Users/MacBookPro/cabbeen_data/cabbeen.db')
cur = conn.cursor()

# 查询李志婕的详细数据
cur.execute("""
    SELECT
        COUNT(DISTINCT order_no) as txns,
        SUM(qty) as units,
        SUM(amount) as rev,
        COUNT(*) as rows
    FROM sales
    WHERE guide_name = ? AND year = 2026
""", ('李志婕',))
r = cur.fetchone()
print(f'李志婕基础数据:')
print(f'  笔数(去重订单): {r[0]}')
print(f'  件数: {r[1]}')
print(f'  销售额: {r[2]}')
print(f'  行数: {r[3]}')
print(f'  连带率(件数/笔数): {r[1]/r[0]:.2f}' if r[0] else 'N/A')
print(f'  客单价(销售额/笔数): {r[2]/r[0]:.0f}' if r[0] else 'N/A')

# VIP相关：会员订单数 vs 非会员订单数
cur.execute("""
    SELECT
        CASE WHEN member_id IS NOT NULL AND member_id != '' THEN '会员' ELSE '非会员' END as flag,
        COUNT(DISTINCT order_no) as vip_txns,
        SUM(qty) as vip_units,
        SUM(amount) as vip_rev
    FROM sales
    WHERE guide_name = ? AND year = 2026
    GROUP BY flag
""", ('李志婕',))
print()
print(f'会员 vs 非会员:')
for r in cur.fetchall():
    print(f'  {r[0]}: 笔数={r[1]}, 件数={r[2]}, 销售额={r[3]}')

conn.close()
