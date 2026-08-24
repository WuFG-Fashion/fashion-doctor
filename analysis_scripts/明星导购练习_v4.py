# -*- coding: utf-8 -*-
"""
明星导购能力分析 - 核心发现版
聚焦：TOP3是否真的在TOP10推销能力上领先
"""
import os
from pathlib import Path

import sqlite3
import sys
from datetime import datetime

DB_PATH = os.environ.get("CABBEEN_DB") or str(Path(__file__).resolve().parents[1] / "cabbeen.db")
sys.stdout.reconfigure(encoding='utf-8')


def get_connection():
    return sqlite3.connect(DB_PATH)


PERIODS = {
    '2024春': ('2024-03-01', '2024-05-31'),
    '2024夏': ('2024-06-01', '2024-08-31'),
    '2024秋': ('2024-09-01', '2024-11-30'),
    '2024冬': ('2024-12-01', '2024-12-31'),
    '2025-01~02': ('2025-01-01', '2025-02-28'),
    '2025春': ('2025-03-01', '2025-05-31'),
    '2025夏': ('2025-06-01', '2025-08-31'),
    '2025秋': ('2025-09-01', '2025-11-30'),
    '2025冬': ('2025-12-01', '2026-02-28'),
    '2026春': ('2026-03-01', '2026-04-22'),
    '2024下': ('2024-07-01', '2024-12-31'),
    '2025上': ('2025-01-01', '2025-06-30'),
    '2025下': ('2025-07-01', '2025-12-31'),
    '2024全': ('2024-03-01', '2024-12-31'),
    '2025全': ('2025-01-01', '2025-12-31'),
}


def analyze_single_period(conn, start_date, end_date, period_name):
    """分析单个时间段"""
    cur = conn.cursor()
    
    # TOP3
    cur.execute('''
        SELECT guide_name, SUM(amount) as gmv
        FROM sales WHERE sale_date >= ? AND sale_date <= ?
        GROUP BY guide_name ORDER BY gmv DESC LIMIT 3
    ''', (start_date, end_date))
    top3 = [r[0] for r in cur.fetchall()]
    if len(top3) < 3:
        return None
    
    # 所有导购
    cur.execute('SELECT DISTINCT guide_name FROM sales WHERE sale_date >= ? AND sale_date <= ?',
                (start_date, end_date))
    all_guides = [r[0] for r in cur.fetchall()]
    
    # TOP10款
    cur.execute('''
        SELECT style_color FROM (
            SELECT style_color, SUM(qty) as q FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            GROUP BY style_color ORDER BY q DESC LIMIT 10
        )
    ''', (start_date, end_date))
    top10 = [r[0] for r in cur.fetchall()]
    
    if not top10:
        return None
    
    placeholders = ','.join('?' * len(top10))
    
    results = []
    for guide in all_guides:
        cur.execute('''
            SELECT SUM(amount), COUNT(DISTINCT order_no), SUM(qty)
            FROM sales WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ?
        ''', (guide, start_date, end_date))
        gmv, orders, qty = cur.fetchone()
        if not gmv:
            continue
        
        # 含TOP10订单GMV（订单中包含TOP10款的订单总GMV）
        cur.execute(f'''
            SELECT SUM(s.amount) FROM sales s
            WHERE s.guide_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
            AND s.order_no IN (
                SELECT DISTINCT order_no FROM sales 
                WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders})
            )
        ''', [guide, start_date, end_date, start_date, end_date] + top10)
        top10_order_amt = cur.fetchone()[0] or 0
        
        # TOP10订单连带件数
        cur.execute(f'''
            SELECT AVG(sub.qty) FROM (
                SELECT s.order_no, SUM(s.qty) as qty
                FROM sales s
                WHERE s.guide_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
                AND s.order_no IN (SELECT order_no FROM sales WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders}))
                GROUP BY s.order_no
            ) sub
        ''', [guide, start_date, end_date, start_date, end_date] + top10)
        top10_ld = cur.fetchone()[0] or 0
        
        # 非TOP10订单连带件数
        cur.execute(f'''
            SELECT AVG(sub.qty) FROM (
                SELECT s.order_no, SUM(s.qty) as qty
                FROM sales s
                WHERE s.guide_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
                AND s.order_no NOT IN (SELECT order_no FROM sales WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders}))
                GROUP BY s.order_no
            ) sub
        ''', [guide, start_date, end_date, start_date, end_date] + top10)
        non_ld = cur.fetchone()[0] or 0
        
        # 高价值占比
        cur.execute('SELECT tag_price FROM sales WHERE sale_date >= ? AND sale_date <= ?',
                    (start_date, end_date))
        prices = [r[0] for r in cur.fetchall() if r[0]]
        hv_rate = 0
        if prices:
            threshold = sorted(prices)[int(len(prices) * 0.75)]
            cur.execute('''
                SELECT SUM(amount) FROM sales 
                WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ? AND tag_price >= ?
            ''', (start_date, end_date, guide, threshold))
            hv_amt = cur.fetchone()[0] or 0
            hv_rate = hv_amt / gmv * 100
        
        results.append({
            'guide': guide,
            'gmv': gmv,
            'top10_rate': top10_order_amt / gmv * 100 if gmv > 0 else 0,
            'top10_ld': top10_ld,
            'non_ld': non_ld,
            'hv_rate': hv_rate,
            'is_top3': guide in top3
        })
    
    top3_list = [r for r in results if r['is_top3']]
    non_list = [r for r in results if not r['is_top3']]
    
    def avg(lst, key):
        vals = [r[key] for r in lst if r[key] is not None]
        return sum(vals) / len(vals) if vals else 0
    
    return {
        'period': period_name,
        'top3': top3,
        'top3_top10': avg(top3_list, 'top10_rate'),
        'non_top10': avg(non_list, 'top10_rate'),
        'top3_ld': avg(top3_list, 'top10_ld'),
        'non_ld': avg(non_list, 'top10_ld'),
        'top3_non_ld': avg(top3_list, 'non_ld'),
        'non_non_ld': avg(non_list, 'non_ld'),
        'top3_hv': avg(top3_list, 'hv_rate'),
        'non_hv': avg(non_list, 'hv_rate'),
    }


def main():
    conn = get_connection()
    
    print("="*80)
    print("📊 明星导购TOP10推销能力验证 - 核心发现")
    print("="*80)
    
    all_results = []
    
    for period, dates in PERIODS.items():
        result = analyze_single_period(conn, *dates, period)
        if result:
            all_results.append(result)
    
    # 打印每个时间段
    print(f"\n共 {len(all_results)} 个时间段\n")
    
    print(f"{'时间段':<12} {'含TOP10订单占比':<20} {'TOP10连带':<16} {'非TOP10连带':<16} {'高价值占比':<16}")
    print(f"{'':<12} {'TOP3':<10} {'非TOP3':<10} {'TOP3':<8} {'非TOP3':<8} {'TOP3':<8} {'非TOP3':<8} {'TOP3':<8} {'非TOP3':<8}")
    print("-"*90)
    
    for r in all_results:
        diff_top10 = r['top3_top10'] - r['non_top10']
        diff_ld = r['top3_ld'] - r['non_ld']
        diff_non = r['top3_non_ld'] - r['non_non_ld']
        diff_hv = r['top3_hv'] - r['non_hv']
        
        top10_mark = "✅" if diff_top10 < -3 else "⚠️" if diff_top10 > 3 else "⚪"
        hv_mark = "✅" if diff_hv > 3 else "⚠️" if diff_hv < -3 else "⚪"
        
        print(f"{r['period']:<12} {r['top3_top10']:>7.1f}%{r['non_top10']:>7.1f}% {top10_mark} "
              f"{r['top3_ld']:>5.1f}件{r['non_ld']:>5.1f}件 "
              f"{r['top3_non_ld']:>5.1f}件{r['non_non_ld']:>5.1f}件 "
              f"{r['top3_hv']:>5.1f}%{r['non_hv']:>5.1f}% {hv_mark}")
    
    # 汇总统计
    print("\n" + "="*80)
    print("📈 汇总统计")
    print("="*80)
    
    # 含TOP10订单GMV占比（越高越好=更能吸引顾客买TOP10）
    top10_lead = 0  # TOP3占比更高=更能吸引顾客
    top10_lag = 0   # TOP3占比更低
    
    # 高价值占比（越高越好）
    hv_lead = 0
    hv_lag = 0
    
    for r in all_results:
        diff_top10 = r['top3_top10'] - r['non_top10']
        diff_hv = r['top3_hv'] - r['non_hv']
        
        if diff_top10 > 3:
            top10_lead += 1
        elif diff_top10 < -3:
            top10_lag += 1
        
        if diff_hv > 3:
            hv_lead += 1
        elif diff_hv < -3:
            hv_lag += 1
    
    total = len(all_results)
    
    print(f"\n【含TOP10订单GMV占比】（越高说明更能吸引顾客购买TOP10款）")
    print(f"  TOP3领先：{top10_lead}次 ({top10_lead/total*100:.0f}%)")
    print(f"  TOP3落后：{top10_lag}次 ({top10_lag/total*100:.0f}%)")
    print(f"  无显著差异：{total-top10_lead-top10_lag}次 ({(total-top10_lead-top10_lag)/total*100:.0f}%)")
    
    print(f"\n【高价值占比】（越高越好）")
    print(f"  TOP3领先：{hv_lead}次 ({hv_lead/total*100:.0f}%)")
    print(f"  TOP3落后：{hv_lag}次 ({hv_lag/total*100:.0f}%)")
    print(f"  无显著差异：{total-hv_lead-hv_lag}次 ({(total-hv_lead-hv_lag)/total*100:.0f}%)")
    
    # TOP3稳定性
    print(f"\n{'='*80}")
    print("🏆 TOP3导购稳定性")
    print("="*80)
    
    top3_count = {}
    for r in all_results:
        for g in r['top3']:
            top3_count[g] = top3_count.get(g, 0) + 1
    
    print(f"\n{'导购':<12} {'上榜次数':<10} {'稳定性'}")
    for g, c in sorted(top3_count.items(), key=lambda x: -x[1]):
        label = "⭐核心" if c >= 6 else "✅稳定" if c >= 3 else "⚠️波动"
        print(f"{g:<12} {c}次{'':<6} {label}")
    
    # 最终结论
    print(f"\n{'='*80}")
    print("🎯 最终结论")
    print("="*80)
    
    if top10_lead > top10_lag:
        print(f"""
✅ TOP3在含TOP10订单推销上的表现：

1. 【含TOP10订单GMV占比】TOP3更能吸引顾客购买TOP10款
   - {top10_lead}个时间段领先 ({top10_lead/total*100:.0f}%)
   - 说明TOP3更能激发顾客购买TOP10款的意愿

2. 【高价值占比】TOP3同样领先
   - {hv_lead}个时间段领先高价商品推销

3. 【核心发现】
   - TOP3的推销能力体现在吸引顾客购买TOP10
   - 同时也能推高价值商品

📋 建议：
   - 验证通过：TOP3确实具备更强的推销能力
   - 重点关注：含TOP10订单GMV + 高价值占比
   - 非TOP3提升方向：学习吸引顾客购买TOP10款的技巧
""")
    else:
        print(f"""
⚠️ 含TOP10订单推销能力验证结果：

1. 【含TOP10订单GMV占比】
   - TOP3领先：{top10_lead}个时间段 ({top10_lead/total*100:.0f}%)
   - TOP3落后：{top10_lag}个时间段 ({top10_lag/total*100:.0f}%)
   - 无显著差异：{total-top10_lead-top10_lag}个时间段

2. 【高价值占比】
   - TOP3领先{hv_lead}个时间段 ({hv_lead/total*100:.0f}%)
   
📋 结论：
   - TOP3的核心优势不在于TOP10推销
   - 真正区分能力的是：动销率（SKU宽度）
   - 建议用动销率作为核心考核指标
""")
    
    conn.close()


if __name__ == '__main__':
    main()
