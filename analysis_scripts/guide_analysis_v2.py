# -*- coding: utf-8 -*-
"""
导购能力模型分析（基于 cabbeen_data 项目权威公式）
公式来源：query_cli.py / member_analysis.py

核心公式（已确认）：
  连带率  = SUM(qty) / COUNT(DISTINCT order_no)        [件/单]
  客单价  = SUM(amount) / COUNT(DISTINCT order_no)      [元/单]
  折扣率  = SUM(amount) / SUM(tag_amount)              [整体折扣]
  均单件折= AVG(discount_rate)                          [均值折率]
  VIP订单 = member_id IS NOT NULL AND member_id != ''
  VIP率   = COUNT(DISTINCT CASE WHEN VIP THEN order_no) / COUNT(DISTINCT order_no)
  复购率  = 有多笔订单的会员数 / 总会员数
"""
import os
from pathlib import Path
import sqlite3, os

DB = os.environ.get("CABBEEN_DB") or str(Path(__file__).resolve().parents[1] / "cabbeen.db")

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def fetchall(sql, params=()):
    cur = get_conn().cursor()
    cur.execute(sql, params)
    return cur.fetchall()

def fetchone(sql, params=()):
    cur = get_conn().cursor()
    cur.execute(sql, params)
    return cur.fetchone()

def pct(a, b):
    return round(a / b * 100, 1) if b else 0.0

# ============================================================
# 数据提取
# ============================================================

# 基础数据
base_sql = """
SELECT
    guide_name,
    SUM(qty)                              AS total_qty,
    SUM(amount)                            AS total_gmv,
    SUM(tag_amount)                        AS total_tag,
    COUNT(DISTINCT order_no)               AS total_orders,
    COUNT(DISTINCT member_id)               AS total_members,
    AVG(discount_rate)                      AS avg_disc_rate,
    COUNT(DISTINCT category)                AS cat_count,
    COUNT(DISTINCT sub_category)            AS subcat_count
FROM sales
WHERE year = 2026
GROUP BY guide_name
ORDER BY total_gmv DESC
LIMIT 15
"""
rows = fetchall(base_sql)

# VIP订单数（去重order_no）
vip_order_sql = """
SELECT guide_name, COUNT(DISTINCT order_no) AS vip_orders
FROM sales
WHERE year = 2026 AND member_id IS NOT NULL AND member_id != ''
GROUP BY guide_name
"""
vip_order_map = {r["guide_name"]: r["vip_orders"] for r in fetchall(vip_order_sql)}

# 复购会员数（有多笔订单的会员）
repurchase_sql = """
SELECT guide_name, COUNT(*) AS repurchase_members
FROM (
    SELECT guide_name, member_id
    FROM sales
    WHERE year = 2026 AND member_id IS NOT NULL AND member_id != ''
    GROUP BY guide_name, member_id
    HAVING COUNT(DISTINCT order_no) > 1
)
GROUP BY guide_name
"""
repurchase_map = {r["guide_name"]: r["repurchase_members"] for r in fetchall(repurchase_sql)}

# ============================================================
# 计算指标
# ============================================================
all_data = []
for r in rows:
    name      = r["guide_name"]
    qty       = r["total_qty"] or 0
    gmv       = r["total_gmv"] or 0
    tag       = r["total_tag"] or 0
    orders    = r["total_orders"] or 0
    members   = r["total_members"] or 0
    avg_disc  = r["avg_disc_rate"] or 0
    cats      = r["cat_count"] or 0
    subcats   = r["subcat_count"] or 0

    vip_orders = vip_order_map.get(name, 0)
    rep_mem    = repurchase_map.get(name, 0)

    # 核心指标（与 cabbeen_data 公式完全一致）
    linkage    = round(qty / orders, 2) if orders > 0 else 0       # 连带率
    avg_price  = round(gmv / orders, 0) if orders > 0 else 0       # 客单价
    overall_disc = round(gmv / tag * 10, 2) if tag > 0 else 0     # 整体折扣（折）
    vip_rate   = pct(vip_orders, orders)                             # VIP订单率
    repurchase_rate = pct(rep_mem, members)                          # 复购率

    all_data.append({
        "name": name,
        "gmv": gmv,
        "qty": qty,
        "orders": orders,
        "members": members,
        "linkage": linkage,
        "avg_price": avg_price,
        "overall_disc": overall_disc,
        "avg_disc_rate": round(avg_disc, 1),   # 均单件折（%）
        "vip_orders": vip_orders,
        "vip_rate": vip_rate,
        "rep_mem": rep_mem,
        "repurchase_rate": repurchase_rate,
        "cats": cats,
        "subcats": subcats,
    })

# ============================================================
# 打印全表
# ============================================================
print("=" * 115)
print("2026年导购能力模型（正确公式验证）")
print("=" * 115)
print(f"{'姓名':<8} {'GMV':>8} {'件数':>5} {'笔数':>5} {'连带率':>6} {'客单价':>6} {'VIP订单':>6} {'VIP率':>6} {'复购率':>6} {'折扣':>5} {'均件折':>6} {'品类':>4}")
print("-" * 115)
for d in all_data:
    print(f"{d['name']:<8} {d['gmv']:>8,.0f} {d['qty']:>5} {d['orders']:>5} "
          f"{d['linkage']:>6.2f} {d['avg_price']:>6,.0f} {d['vip_orders']:>6} "
          f"{d['vip_rate']:>6.1f}% {d['repurchase_rate']:>6.1f}% {d['overall_disc']:>5.1f}折 {d['avg_disc_rate']:>5.1f}%")

print()

# ============================================================
# TOP3 分析
# ============================================================
top3 = all_data[:3]
total_avg = {
    "gmv": sum(d["gmv"] for d in all_data) / len(all_data),
    "linkage": sum(d["linkage"] for d in all_data) / len(all_data),
    "avg_price": sum(d["avg_price"] for d in all_data) / len(all_data),
    "vip_rate": sum(d["vip_rate"] for d in all_data) / len(all_data),
    "repurchase_rate": sum(d["repurchase_rate"] for d in all_data) / len(all_data),
    "overall_disc": sum(d["overall_disc"] for d in all_data) / len(all_data),
}

print("=" * 60)
print("TOP3 vs 全员均值对比")
print("=" * 60)
print(f"{'':8} {'GMV':>8} {'连带率':>6} {'客单价':>6} {'VIP率':>6} {'复购率':>6} {'折扣':>5}")
print("-" * 60)
for i, d in enumerate(top3):
    print(f"#{i+1} {d['name']:<6} {d['gmv']:>8,.0f} {d['linkage']:>6.2f} {d['avg_price']:>6,.0f} {d['vip_rate']:>6.1f}% {d['repurchase_rate']:>6.1f}% {d['overall_disc']:>5.1f}折")
print("-" * 60)
print(f"{'全员均值':<8} {total_avg['gmv']:>8,.0f} {total_avg['linkage']:>6.2f} {total_avg['avg_price']:>6,.0f} {total_avg['vip_rate']:>6.1f}% {total_avg['repurchase_rate']:>6.1f}% {total_avg['overall_disc']:>5.1f}折")

print()
print("TOP3 冠军画像：")
for i, d in enumerate(top3):
    print(f"  #{i+1} {d['name']}: GMV={d['gmv']:,.0f} 连带={d['linkage']} VIP率={d['vip_rate']}% 复购={d['repurchase_rate']}% 折扣={d['overall_disc']}折 客单={d['avg_price']}")
