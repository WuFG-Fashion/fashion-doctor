import sqlite3, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB = r"C:\Users\MacBookPro\cabbeen_data\cabbeen.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# 检查数据库日期范围
cur.execute("SELECT MIN(sale_date), MAX(sale_date), COUNT(*) FROM sales WHERE year = 2026")
result1 = cur.fetchone()
print("2026全年数据:", result1)

# 检查30天数据
cur.execute("SELECT COUNT(*) FROM sales WHERE date(sale_date) BETWEEN '2026-03-23' AND '2026-04-20'")
result2 = cur.fetchone()
print("近30天数据:", result2)

conn.close()
print("Done")
