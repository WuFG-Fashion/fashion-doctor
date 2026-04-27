import sqlite3
conn = sqlite3.connect('C:/Users/MacBookPro/cabbeen_data/cabbeen.db')
cur = conn.cursor()

cur.execute("SELECT DISTINCT shop_name FROM sales WHERE sale_date LIKE '2026%' ORDER BY shop_name")
print('=== sales shops (2026) ===')
for row in cur.fetchall():
    print(f'  [{row[0]}]')

cur.execute('SELECT full_name, short_name, region, city, shop_attr, shop_type FROM shops')
print()
print('=== shops table ===')
for row in cur.fetchall():
    print(f'  full=[{row[0]}] short=[{row[1]}] region=[{row[2]}] city=[{row[3]}] attr=[{row[4]}] type=[{row[5]}]')

cur.execute("SELECT shop_attr, shop_type, COUNT(*) FROM sales WHERE sale_date LIKE '2026%' GROUP BY shop_attr, shop_type ORDER BY COUNT(*) DESC")
print()
print('=== shop_attr/shop_type distribution ===')
for row in cur.fetchall():
    print(f'  attr=[{row[0]}] type=[{row[1]}] count={row[2]}')

cur.execute("SELECT province, COUNT(*) FROM sales WHERE sale_date LIKE '2026%' GROUP BY province ORDER BY COUNT(*) DESC")
print()
print('=== province distribution ===')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')

cur.execute("SELECT SUBSTR(sale_date, 1, 7) as month, SUM(amount), COUNT(*) FROM sales WHERE sale_date LIKE '2026%' GROUP BY month ORDER BY month")
print()
print('=== 2026 monthly breakdown ===')
for row in cur.fetchall():
    print(f'  {row[0]}: GMV={row[1]:,.0f} 记录={row[2]}')

conn.close()
