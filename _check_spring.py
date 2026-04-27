# -*- coding: utf-8 -*-
import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r'C:\Users\MacBookPro\cabbeen_data\cabbeen.db'

def analyze_period(start_date, end_date, period_name):
    print(f"\n{'='*60}")
    print(f"【{period_name}】分析")
    print(f"时间范围: {start_date} ~ {end_date}")
    print('='*60)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. 先计算全局TOP10款（按销量）
    cur.execute("""
        SELECT style_code, SUM(qty) as total_qty
        FROM sales
        WHERE sale_date >= ? AND sale_date <= ?
        GROUP BY style_code
        ORDER BY total_qty DESC
        LIMIT 10
    """, (start_date, end_date))
    global_top10 = [r[0] for r in cur.fetchall()]
    print(f"\n全局TOP10款: {global_top10[:3]}... (共{len(global_top10)}个)")

    if not global_top10:
        print("无数据")
        conn.close()
        return

    # 2. 计算每个导购的GMV和TOP3
    cur.execute("""
        SELECT
            s.guide_name,
            SUM(s.amount) as total_gmv,
            SUM(s.qty) as total_qty,
            COUNT(DISTINCT s.member_id) as member_count,
            COUNT(DISTINCT s.order_no) as order_count
        FROM sales s
        WHERE s.sale_date >= ? AND s.sale_date <= ?
        GROUP BY s.guide_name
        ORDER BY total_gmv DESC
    """, (start_date, end_date))
    guides = cur.fetchall()
    print(f"导购数量: {len(guides)}")

    if len(guides) < 3:
        print("导购数量不足")
        conn.close()
        return

    top3_names = [g[0] for g in guides[:3]]
    print(f"TOP3: {top3_names}")

    # 3. 计算各维度指标
    results = []
    for guide in guides:
        name = guide[0]
        gmv = guide[1]
        qty = guide[2]
        member_count = guide[3]
        order_count = guide[4]

        # SKU宽度（不同style_code数量）
        cur.execute("""
            SELECT COUNT(DISTINCT style_code)
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ?
        """, (start_date, end_date, name))
        sku_width = cur.fetchone()[0]

        # TOP10关联率（销售额）
        placeholders = ",".join("?" * len(global_top10))
        cur.execute(f"""
            SELECT COALESCE(SUM(amount), 0)
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            AND guide_name = ?
            AND style_code IN ({placeholders})
        """, (start_date, end_date, name) + tuple(global_top10))
        top10_amt = cur.fetchone()[0]
        top10_rate = (top10_amt / gmv * 100) if gmv > 0 else 0

        # 高价值占比（吊牌价前25%的SKU销售占比）
        # 先算全局吊牌价的75分位数
        cur.execute(f"""
            SELECT tag_price FROM sales
            WHERE sale_date >= ? AND sale_date <= ? AND tag_price > 0
        """, (start_date, end_date))
        all_prices = [r[0] for r in cur.fetchall()]
        if all_prices:
            all_prices.sort()
            p75 = all_prices[int(len(all_prices) * 0.75)]
        else:
            p75 = 0

        cur.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            AND guide_name = ?
            AND tag_price >= ?
        """, (start_date, end_date, name, p75))
        hv_amt = cur.fetchone()[0]
        hv_rate = (hv_amt / gmv * 100) if gmv > 0 else 0

        # VIP订单率
        cur.execute("""
            SELECT COUNT(*), COUNT(CASE WHEN is_vip = '1' OR is_vip = 'Y' THEN 1 END)
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            AND guide_name = ?
        """, (start_date, end_date, name))
        total_orders, vip_orders = cur.fetchone()
        vip_rate = (vip_orders / total_orders * 100) if total_orders > 0 else 0

        # 复购率
        cur.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN repeat_count > 1 THEN 1 ELSE 0 END) as repeat
            FROM (
                SELECT member_id, COUNT(DISTINCT order_no) as repeat_count
                FROM sales
                WHERE sale_date >= ? AND sale_date <= ?
                AND guide_name = ?
                GROUP BY member_id
            )
        """, (start_date, end_date, name))
        total_mem, repeat_mem = cur.fetchone()
        repurchase_rate = (repeat_mem / total_mem * 100) if total_mem > 0 else 0

        # 新开卡人数（该导购的新会员）
        cur.execute("""
            SELECT COUNT(DISTINCT member_id)
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            AND guide_name = ?
            AND member_type = '新卡'
        """, (start_date, end_date, name))
        new_vip = cur.fetchone()[0]

        # 客单价
        avg_price = gmv / order_count if order_count > 0 else 0

        # 连带件数
        avg_qty = qty / order_count if order_count > 0 else 0

        # 折扣率（用平均折扣）
        cur.execute("""
            SELECT AVG(discount_rate)
            FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            AND guide_name = ?
        """, (start_date, end_date, name))
        avg_discount = cur.fetchone()[0] or 0

        results.append({
            'name': name,
            'gmv': gmv,
            'sku_width': sku_width,
            'top10_rate': top10_rate,
            'hv_rate': hv_rate,
            'vip_rate': vip_rate,
            'repurchase_rate': repurchase_rate,
            'new_vip': new_vip,
            'avg_price': avg_price,
            'avg_qty': avg_qty,
            'avg_discount': avg_discount
        })

    conn.close()

    # 4. 汇总TOP3和全员
    top3 = [r for r in results if r['name'] in top3_names]
    all_data = results

    def avg(lst, key):
        vals = [r[key] for r in lst if r[key] is not None]
        return sum(vals) / len(vals) if vals else 0

    def sumv(lst, key):
        vals = [r[key] for r in lst if r[key] is not None]
        return sum(vals) if vals else 0

    print(f"\n{'指标':<15} {'TOP3':<12} {'全员':<12} {'差距':<10}")
    print('-' * 50)

    metrics = [
        ('GMV', 'gmv', lambda v: f'{v:,.0f}元'),
        ('SKU宽度', 'sku_width', lambda v: f'{v:.0f}个'),
        ('TOP10关联率', 'top10_rate', lambda v: f'{v:.1f}%'),
        ('高价值占比', 'hv_rate', lambda v: f'{v:.1f}%'),
        ('VIP订单率', 'vip_rate', lambda v: f'{v:.1f}%'),
        ('复购率', 'repurchase_rate', lambda v: f'{v:.1f}%'),
        ('新开卡', 'new_vip', lambda v: f'{v:.0f}人'),
        ('客单价', 'avg_price', lambda v: f'{v:.0f}元'),
        ('连带件数', 'avg_qty', lambda v: f'{v:.2f}件'),
        ('折扣率', 'avg_discount', lambda v: f'{v:.2f}'),
    ]

    for label, key, fmt in metrics:
        t3_val = avg(top3, key)
        all_val = avg(all_data, key)
        if all_val > 0:
            diff = (t3_val - all_val) / all_val * 100
            diff_str = f'{diff:+.1f}%'
        else:
            diff_str = '-'
        print(f"{label:<15} {fmt(t3_val):<12} {fmt(all_val):<12} {diff_str:<10}")

    # 5. TOP3详情
    print(f"\n【TOP3详细】")
    for g in sorted(top3, key=lambda x: -x['gmv']):
        print(f"  {g['name']}: GMV={g['gmv']:,.0f}, SKU={g['sku_width']}, TOP10={g['top10_rate']:.1f}%, 高价值={g['hv_rate']:.1f}%, 复购={g['repurchase_rate']:.1f}%")

    return results

# 过年前7天：2026年春节是2月17日，前7天是2月10日-2月16日
print("\n" + "="*60)
print("【过年前7天】2026-02-10 ~ 2026-02-16")
print("="*60)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT COUNT(*), SUM(amount) FROM sales WHERE sale_date BETWEEN '2026-02-10' AND '2026-02-16'")
cnt, amt = cur.fetchone()
print(f"销售笔数: {cnt}, GMV: {amt:,.0f}元" if cnt else "无数据")
conn.close()

analyze_period('2026-02-10', '2026-02-16', '过年前7天')
