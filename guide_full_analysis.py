# -*- coding: utf-8 -*-
"""
明星导购能力拆解 - 全维度版本
每个时间段的TOP3独立计算，每个时间段的TOP10也独立计算
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import sqlite3
from datetime import datetime, timedelta

DB_PATH = r'C:\Users\MacBookPro\cabbeen_data\cabbeen.db'
today = datetime(2026, 4, 22)

# 时间范围定义
periods = [
    ("近7天", 7),
    ("近15天", 15),
    ("近30天", 30),
    ("近45天", 45),
    ("近60天", 60),
    ("全年", None),  # None表示全年
]

def get_period_range(days):
    """计算时间范围"""
    if days is None:
        return "2026-01-01", "2026-04-22"
    end_date = today.strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=days-1)).strftime("%Y-%m-%d")
    return start_date, end_date

def analyze_period(cursor, period_name, days):
    """分析单个时间段"""
    start_date, end_date = get_period_range(days)
    
    # 1. 计算每个导购的GMV，确定TOP3
    guide_gmv_sql = """
    SELECT
        s.guide_name,
        SUM(s.amount) as total_gmv,
        SUM(s.qty) as total_qty,
        COUNT(DISTINCT s.member_id) as member_count,
        COUNT(DISTINCT s.style_code) as sku_count,
        COUNT(DISTINCT s.order_no) as order_count
    FROM sales s
    WHERE s.sale_date >= ? AND s.sale_date <= ?
    GROUP BY s.guide_name
    ORDER BY total_gmv DESC
    """
    
    cursor.execute(guide_gmv_sql, (start_date, end_date))
    all_guides = cursor.fetchall()
    
    if not all_guides:
        return None
    
    # 取TOP3
    top3_names = [g[0] for g in all_guides[:3]]
    
    # 2. 计算全员指标
    total_gmv = sum(g[1] for g in all_guides)
    total_qty = sum(g[2] for g in all_guides)
    total_members = sum(g[3] for g in all_guides)
    total_skus = sum(g[4] for g in all_guides)
    total_orders = sum(g[5] for g in all_guides)
    
    avg_sku = total_skus / len(all_guides)
    avg_qty_per_order = total_qty / total_orders if total_orders > 0 else 0
    avg_gmv_per_order = total_gmv / total_orders if total_orders > 0 else 0
    
    # 3. 计算全员VIP率、新开卡、复购率
    # VIP率（按订单数计算，每笔订单只要有VIP商品就算VIP订单）
    vip_sql = """
    SELECT COUNT(DISTINCT order_no) FROM sales
    WHERE sale_date >= ? AND sale_date <= ? AND is_vip = 1
    """
    cursor.execute(vip_sql, (start_date, end_date))
    vip_count = cursor.fetchone()[0] or 0
    
    # 新开卡（member_id在周期内首次出现）
    # 先找所有会员的最早购买日期
    new_card_sql = """
    SELECT COUNT(*) FROM (
        SELECT member_id FROM (
            SELECT member_id, MIN(sale_date) as first_date
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            AND member_id IS NOT NULL AND member_id != ''
            GROUP BY member_id
        )
        WHERE first_date >= ?
    )
    """
    cursor.execute(new_card_sql, (start_date, end_date, start_date))
    new_card_count = cursor.fetchone()[0] or 0
    
    # 复购率（购买2次以上的会员/总会员数）
    repeat_sql = """
    SELECT COUNT(*) FROM (
        SELECT member_id FROM sales
        WHERE sale_date >= ? AND sale_date <= ?
        GROUP BY member_id
        HAVING COUNT(DISTINCT order_no) > 1
    )
    """
    cursor.execute(repeat_sql, (start_date, end_date))
    repeat_count = cursor.fetchone()[0] or 0
    repeat_rate = repeat_count / total_members if total_members > 0 else 0
    
    # 4. 计算全员TOP10关联率（基于销售额）
    # 先找全员TOP10款
    top10_sql = """
    SELECT style_code, SUM(amount) as total_amount
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ?
    GROUP BY style_code
    ORDER BY total_amount DESC
    LIMIT 10
    """
    cursor.execute(top10_sql, (start_date, end_date))
    top10_codes = [r[0] for r in cursor.fetchall()]
    
    # 计算全员TOP10关联率
    top10_amount_sql = f"""
    SELECT COALESCE(SUM(amount), 0)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ?
    AND style_code IN ({','.join('?' * len(top10_codes))})
    """
    cursor.execute(top10_amount_sql, (start_date, end_date) + tuple(top10_codes))
    top10_amount = cursor.fetchone()[0] or 0
    top10_rate = top10_amount / total_gmv if total_gmv > 0 else 0
    
    # 5. 高价值占比（正价商品，discount_rate=0表示有折扣）
    high_value_sql = """
    SELECT COALESCE(SUM(amount), 0), COALESCE(SUM(qty), 0)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ? AND discount_rate != 0
    """
    cursor.execute(high_value_sql, (start_date, end_date))
    hv = cursor.fetchone()
    high_value_amount = hv[0]
    high_value_qty = hv[1]
    high_value_rate = high_value_amount / total_gmv if total_gmv > 0 else 0
    
    # 6. 计算折扣率
    disc_sql = """
    SELECT COALESCE(AVG(discount_rate), 1)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ? AND discount_rate IS NOT NULL
    """
    cursor.execute(disc_sql, (start_date, end_date))
    avg_discount = cursor.fetchone()[0] or 1.0
    
    # 7. 计算TOP3的指标
    top3_gmv = sum(g[1] for g in all_guides[:3])
    top3_qty = sum(g[2] for g in all_guides[:3])
    top3_orders = sum(g[5] for g in all_guides[:3])
    
    # TOP3 VIP率（按订单数计算）
    top3_placeholders = ','.join('?' * len(top3_names))
    top3_vip_sql = f"""
    SELECT COUNT(DISTINCT order_no)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ?
    AND guide_name IN ({top3_placeholders})
    AND is_vip = 1
    """
    cursor.execute(top3_vip_sql, (start_date, end_date) + tuple(top3_names))
    top3_vip = cursor.fetchone()[0] or 0
    
    # TOP3新开卡（member_id在该导购周期内首次出现）
    top3_new_card_sql = f"""
    SELECT COUNT(*) FROM (
        SELECT member_id FROM (
            SELECT member_id, MIN(sale_date) as first_date, guide_name
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            AND member_id IS NOT NULL AND member_id != ''
            GROUP BY member_id
        )
        WHERE guide_name IN ({top3_placeholders})
        AND first_date >= ?
    )
    """
    cursor.execute(top3_new_card_sql, (start_date, end_date) + tuple(top3_names) + (start_date,))
    top3_new_card = cursor.fetchone()[0] or 0
    
    # TOP3复购率
    top3_members_sql = f"""
    SELECT COUNT(DISTINCT member_id)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ?
    AND guide_name IN ({top3_placeholders})
    """
    cursor.execute(top3_members_sql, (start_date, end_date) + tuple(top3_names))
    top3_total_members = cursor.fetchone()[0] or 0
    
    top3_repeat_sql = f"""
    SELECT COUNT(*) FROM (
        SELECT member_id FROM sales
        WHERE sale_date >= ? AND sale_date <= ?
        AND guide_name IN ({top3_placeholders})
        GROUP BY member_id
        HAVING COUNT(DISTINCT order_no) > 1
    )
    """
    cursor.execute(top3_repeat_sql, (start_date, end_date) + tuple(top3_names))
    top3_repeat = cursor.fetchone()[0] or 0
    top3_repeat_rate = top3_repeat / top3_total_members if top3_total_members > 0 else 0
    
    # TOP3 TOP10关联率
    top10_placeholders = ','.join('?' * len(top10_codes))
    top3_top10_sql = f"""
    SELECT COALESCE(SUM(amount), 0)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ?
    AND guide_name IN ({top3_placeholders})
    AND style_code IN ({top10_placeholders})
    """
    cursor.execute(top3_top10_sql, (start_date, end_date) + tuple(top3_names) + tuple(top10_codes))
    top3_top10_amount = cursor.fetchone()[0] or 0
    top3_top10_rate = top3_top10_amount / top3_gmv if top3_gmv > 0 else 0
    
    # TOP3高价值占比（正价商品，discount_rate=0表示有折扣）
    top3_hv_sql = f"""
    SELECT COALESCE(SUM(amount), 0)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ?
    AND guide_name IN ({top3_placeholders})
    AND discount_rate != 0
    """
    cursor.execute(top3_hv_sql, (start_date, end_date) + tuple(top3_names))
    top3_hv = cursor.fetchone()[0] or 0
    top3_hv_rate = top3_hv / top3_gmv if top3_gmv > 0 else 0
    
    # TOP3折扣率
    top3_disc_sql = f"""
    SELECT COALESCE(AVG(discount_rate), 1)
    FROM sales
    WHERE sale_date >= ? AND sale_date <= ?
    AND guide_name IN ({top3_placeholders})
    AND discount_rate IS NOT NULL
    """
    cursor.execute(top3_disc_sql, (start_date, end_date) + tuple(top3_names))
    top3_avg_disc = cursor.fetchone()[0] or 1.0
    
    return {
        "period": period_name,
        "date_range": f"{start_date} ~ {end_date}",
        "top3_names": top3_names,
        "top3": {
            "gmv": top3_gmv,
            "qty": top3_qty,
            "orders": top3_orders,
            "vip_rate": top3_vip / top3_orders if top3_orders > 0 else 0,
            "new_card": top3_new_card,
            "repeat_rate": top3_repeat_rate,
            "top10_rate": top3_top10_rate,
            "high_value_rate": top3_hv_rate,
            "avg_discount": top3_avg_disc,
            "qty_per_order": top3_qty / top3_orders if top3_orders > 0 else 0,
            "gmv_per_order": top3_gmv / top3_orders if top3_orders > 0 else 0,
        },
        "all": {
            "gmv": total_gmv,
            "qty": total_qty,
            "orders": total_orders,
            "guides": len(all_guides),
            "vip_rate": vip_count / total_orders if total_orders > 0 else 0,
            "new_card": new_card_count,
            "repeat_rate": repeat_rate,
            "top10_rate": top10_rate,
            "high_value_rate": high_value_rate,
            "avg_discount": avg_discount,
            "qty_per_order": avg_qty_per_order,
            "gmv_per_order": avg_gmv_per_order,
        }
    }

# 执行分析
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

results = []
for period_name, days in periods:
    result = analyze_period(cursor, period_name, days)
    if result:
        results.append(result)

conn.close()

# 打印结果
print("=" * 80)
print("【明星导购能力拆解 - 各时间段TOP3独立计算】")
print("=" * 80)

for r in results:
    print(f"\n{'='*60}")
    print(f"【{r['period']}】{r['date_range']}")
    print(f"TOP3: {' / '.join(r['top3_names'])}")
    print("-" * 60)
    
    t = r['top3']
    a = r['all']
    
    # 计算差距
    def gap(top3_val, all_val, higher_better=True):
        if all_val == 0:
            return "N/A"
        diff = top3_val - all_val
        pct = diff / all_val * 100
        if higher_better:
            return f"{pct:+.1f}%"
        else:
            return f"{pct:.1f}pp"
    
    print(f"{'指标':<20} {'TOP3':>12} {'全员':>12} {'差距':>12}")
    print("-" * 60)
    print(f"{'TOP10关联率(销额)':<20} {t['top10_rate']*100:>11.1f}% {a['top10_rate']*100:>11.1f}% {gap(t['top10_rate'], a['top10_rate'], higher_better=False):>12}")
    print(f"{'高价值占比':<20} {t['high_value_rate']*100:>11.1f}% {a['high_value_rate']*100:>11.1f}% {gap(t['high_value_rate'], a['high_value_rate']):>12}")
    print(f"{'VIP订单率':<20} {t['vip_rate']*100:>11.1f}% {a['vip_rate']*100:>11.1f}% {gap(t['vip_rate'], a['vip_rate']):>12}")
    print(f"{'复购率':<20} {t['repeat_rate']*100:>11.1f}% {a['repeat_rate']*100:>11.1f}% {gap(t['repeat_rate'], a['repeat_rate']):>12}")
    print(f"{'新开卡人数':<20} {t['new_card']:>12} {a['new_card']:>12} {gap(t['new_card'], a['new_card']):>12}")
    print(f"{'客单价':<20} {t['gmv_per_order']:>11.0f}元 {a['gmv_per_order']:>10.0f}元 {gap(t['gmv_per_order'], a['gmv_per_order']):>12}")
    print(f"{'连带件数':<20} {t['qty_per_order']:>11.2f}件 {a['qty_per_order']:>10.2f}件 {gap(t['qty_per_order'], a['qty_per_order']):>12}")
    print(f"{'平均折扣率':<20} {t['avg_discount']:>11.2f} {a['avg_discount']:>11.2f} {'越低越好':>12}")

# 汇总表格
print("\n" + "=" * 80)
print("【汇总对比表】")
print("=" * 80)
print(f"{'时间段':<8} {'TOP3':<20} {'TOP10关联率':>10} {'高价值':>8} {'VIP率':>8} {'复购率':>8} {'新开卡':>8} {'客单价':>10} {'连带':>8}")
print("-" * 80)

for r in results:
    t = r['top3']
    a = r['all']
    top3_short = '/'.join([n[0] for n in r['top3_names']])
    print(f"{r['period']:<8} {top3_short:<20} {t['top10_rate']*100:>9.1f}% {t['high_value_rate']*100:>7.1f}% {t['vip_rate']*100:>7.1f}% {t['repeat_rate']*100:>7.1f}% {t['new_card']:>8} {t['gmv_per_order']:>9.0f} {t['qty_per_order']:>7.2f}")

print()
print(f"{'全员':<8} {'':<20} {a['top10_rate']*100:>9.1f}% {a['high_value_rate']*100:>7.1f}% {a['vip_rate']*100:>7.1f}% {a['repeat_rate']*100:>7.1f}% {a['new_card']:>8} {a['gmv_per_order']:>9.0f} {a['qty_per_order']:>7.2f}")
