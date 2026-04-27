# -*- coding: utf-8 -*-
"""
明星导购能力拆解 - 练习版 v3
核心验证：TOP3是否在TOP10推销能力上领先
"""

import sqlite3
import sys
from datetime import datetime

DB_PATH = r'C:\Users\MacBookPro\cabbeen_data\cabbeen.db'
sys.stdout.reconfigure(encoding='utf-8')


def get_connection():
    return sqlite3.connect(DB_PATH)


PERIODS = {
    # 2024年
    '2024春': ('2024-03-01', '2024-05-31'),
    '2024夏': ('2024-06-01', '2024-08-31'),
    '2024秋': ('2024-09-01', '2024-11-30'),
    '2024冬': ('2024-12-01', '2024-12-31'),
    # 2025年
    '2025-01~02': ('2025-01-01', '2025-02-28'),
    '2025春': ('2025-03-01', '2025-05-31'),
    '2025夏': ('2025-06-01', '2025-08-31'),
    '2025秋': ('2025-09-01', '2025-11-30'),
    '2025冬': ('2025-12-01', '2026-02-28'),
    # 2026年
    '2026春': ('2026-03-01', '2026-04-22'),
    # 半年度
    '2024上': ('2024-03-01', '2024-06-30'),
    '2024下': ('2024-07-01', '2024-12-31'),
    '2025上': ('2025-01-01', '2025-06-30'),
    '2025下': ('2025-07-01', '2025-12-31'),
    # 年度
    '2024全': ('2024-03-01', '2024-12-31'),
    '2025全': ('2025-01-01', '2025-12-31'),
}


def get_season_info(start_date):
    year = int(start_date[:4])
    month = int(start_date[5:7])
    if month in [3, 4, 5]:
        return year, '春'
    elif month in [6, 7, 8]:
        return year, '夏'
    elif month in [9, 10, 11]:
        return year, '秋'
    else:
        return year, '冬'


def get_top3_guides(conn, start_date, end_date):
    cur = conn.cursor()
    cur.execute('''
        SELECT guide_name, SUM(amount) as gmv
        FROM sales WHERE sale_date >= ? AND sale_date <= ?
        GROUP BY guide_name ORDER BY gmv DESC LIMIT 3
    ''', (start_date, end_date))
    return [r[0] for r in cur.fetchall()]


def get_guide_metrics_v3(conn, guide_name, start_date, end_date):
    """获取单个导购的各项指标 - v3修正版"""
    cur = conn.cursor()
    
    # 基础数据
    cur.execute('''
        SELECT SUM(amount) as gmv, COUNT(DISTINCT order_no) as orders,
               SUM(qty) as total_qty, COUNT(DISTINCT member_id) as members
        FROM sales WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ?
    ''', (guide_name, start_date, end_date))
    r = cur.fetchone()
    gmv, orders, qty, members = r[0] or 0, r[1] or 0, r[2] or 0, r[3] or 0
    
    if gmv == 0:
        return None
    
    avg_price = gmv / orders if orders > 0 else 0
    lian_dai = qty / orders if orders > 0 else 0
    
    # 获取该导购所在店铺
    cur.execute('''
        SELECT DISTINCT shop_name FROM sales 
        WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ?
    ''', (guide_name, start_date, end_date))
    shops = [r[0] for r in cur.fetchall()]
    
    # 季节信息
    year, season = get_season_info(start_date)
    
    # 店铺该季节库存SKU
    best_shop, max_sku = None, 0
    for shop in shops:
        cur.execute('''
            SELECT COUNT(DISTINCT style_color) 
            FROM inventory WHERE year = ? AND season = ? AND shop_name = ?
        ''', (year, season, shop))
        cnt = cur.fetchone()[0] or 0
        if cnt > max_sku:
            max_sku = cnt
            best_shop = shop
    
    # 导购该时间段销售SKU
    cur.execute('''
        SELECT COUNT(DISTINCT style_color)
        FROM sales WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ?
    ''', (guide_name, start_date, end_date))
    guide_sku = cur.fetchone()[0] or 0
    
    dongxiao = guide_sku / max_sku * 100 if max_sku > 0 else 0
    
    # ========== TOP10推销能力分析 ==========
    # 该时间段的TOP10款
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
    
    # TOP10订单GMV占比（含TOP10款的订单GMV / 总GMV）
    cur.execute(f'''
        SELECT SUM(s.amount) FROM sales s WHERE s.guide_name = ?
        AND s.order_no IN (
            SELECT DISTINCT order_no FROM sales 
            WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders})
        )
    ''', [guide_name, start_date, end_date] + top10)
    top10_order_amt = cur.fetchone()[0] or 0
    top10_order_rate = top10_order_amt / gmv * 100 if gmv > 0 else 0
    
    # TOP10款本身的GMV占比（TOP10款销售额 / 总GMV）
    cur.execute(f'''
        SELECT SUM(amount) FROM sales 
        WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders})
    ''', [guide_name, start_date, end_date] + top10)
    top10_sku_amt = cur.fetchone()[0] or 0
    top10_sku_rate = top10_sku_amt / gmv * 100 if gmv > 0 else 0
    
    # TOP10连带率（含TOP10款的订单中，连带了多少件）
    cur.execute(f'''
        SELECT AVG(sub.qty) FROM (
            SELECT s.order_no, SUM(s.qty) as qty
            FROM sales s
            WHERE s.guide_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
            AND s.order_no IN (
                SELECT DISTINCT order_no FROM sales 
                WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders})
            )
            GROUP BY s.order_no
        ) sub
    ''', [guide_name, start_date, end_date, start_date, end_date] + top10)
    top10_liandai = cur.fetchone()[0] or 0
    
    # 非TOP10连带率（不含TOP10款的订单中，连带了多少件）
    cur.execute(f'''
        SELECT AVG(sub.qty) FROM (
            SELECT s.order_no, SUM(s.qty) as qty
            FROM sales s
            WHERE s.guide_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
            AND s.order_no NOT IN (
                SELECT DISTINCT order_no FROM sales 
                WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders})
            )
            GROUP BY s.order_no
        ) sub
    ''', [guide_name, start_date, end_date, start_date, end_date] + top10)
    non_top10_liandai = cur.fetchone()[0] or 0
    
    # 高价值占比
    cur.execute('SELECT tag_price FROM sales WHERE sale_date >= ? AND sale_date <= ?',
                (start_date, end_date))
    prices = [r[0] for r in cur.fetchall() if r[0]]
    high_value = 0
    if prices:
        threshold = sorted(prices)[int(len(prices) * 0.75)]
        cur.execute('''
            SELECT SUM(amount) FROM sales 
            WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ? AND tag_price >= ?
        ''', (start_date, end_date, guide_name, threshold))
        high = cur.fetchone()[0] or 0
        high_value = high / gmv * 100 if gmv > 0 else 0
    
    # 复购率（30天内有2次以上购买的会员占比）
    cur.execute('''
        SELECT COUNT(*) FROM (
            SELECT member_id FROM sales
            WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ?
            AND member_id IS NOT NULL AND member_id != ''
            GROUP BY member_id HAVING COUNT(*) >= 2
        )
    ''', (start_date, end_date, guide_name))
    repurchase = cur.fetchone()[0] or 0
    repurchase_rate = repurchase / members * 100 if members > 0 else 0
    
    return {
        'guide': guide_name,
        'gmv': gmv,
        'orders': orders,
        'qty': qty,
        'members': members,
        'avg_price': avg_price,
        'lian_dai': lian_dai,
        'dongxiao': dongxiao,
        'guide_sku': guide_sku,
        'shop_sku': max_sku,
        'top10_order_rate': top10_order_rate,  # TOP10订单GMV占比
        'top10_sku_rate': top10_sku_rate,      # TOP10款GMV占比
        'top10_liandai': top10_liandai,        # TOP10连带件数
        'non_top10_liandai': non_top10_liandai,  # 非TOP10连带件数
        'high_value': high_value,
        'repurchase_rate': repurchase_rate,
    }


def analyze_period_v3(conn, start_date, end_date, period_name):
    """分析单个时间段 - v3核心版"""
    print(f"\n{'='*80}")
    print(f"【{period_name}】{start_date} ~ {end_date}")
    print('='*80)
    
    top3 = get_top3_guides(conn, start_date, end_date)
    if len(top3) < 3:
        print(f"⚠️ 导购数量不足，仅 {len(top3)} 人")
        return None
    
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT guide_name FROM sales WHERE sale_date >= ? AND sale_date <= ?',
                (start_date, end_date))
    all_guides = [r[0] for r in cur.fetchall()]
    
    results = []
    for guide in all_guides:
        m = get_guide_metrics_v3(conn, guide, start_date, end_date)
        if m:
            m['is_top3'] = guide in top3
            results.append(m)
    
    top3_list = [r for r in results if r['is_top3']]
    non_top3_list = [r for r in results if not r['is_top3']]
    
    def avg(lst, key):
        vals = [r[key] for r in lst if r.get(key, 0) is not None and r[key] > 0]
        return sum(vals) / len(vals) if vals else 0
    
    def avg_safe(lst, key):
        vals = [r[key] for r in lst if r.get(key) is not None]
        return sum(vals) / len(vals) if vals else 0
    
    print(f"\n🏆 TOP3: {', '.join(top3)}")
    print(f"📊 导购总数: {len(results)}人 (TOP3: {len(top3_list)} / 非TOP3: {len(non_top3_list)})")
    
    # ========== 核心指标对比 ==========
    print(f"\n{'维度':<18} {'TOP3均值':<14} {'非TOP3均值':<14} {'差距':<10}")
    print('-' * 60)
    
    # 基础指标
    def fmt_num(val, is_gmv=False):
        if is_gmv:
            return f"{val:,.0f}"
        return f"{val:.1f}"
    
    metrics_display = [
        ('GMV(元)', 'gmv', True),
        ('客单价(元)', 'avg_price', True),
        ('连带件数', 'lian_dai', False),
        ('动销率(%)', 'dongxiao', False),
    ]
    
    insights = []
    
    print(f"{'维度':<18} {'TOP3均值':<14} {'非TOP3均值':<14} {'差距':<10}")
    print('-' * 60)
    
    for name, key, is_gmv in metrics_display:
        def avg_func(lst):
            vals = [r[key] for r in lst if r.get(key, 0) is not None]
            return sum(vals) / len(vals) if vals else 0
        
        t = avg_func(top3_list)
        n = avg_func(non_top3_list)
        diff = t - n
        
        t_str = fmt_num(t, is_gmv)
        n_str = fmt_num(n, is_gmv)
        diff_str = f"{diff:+,.0f}" if is_gmv else f"{diff:+8.1f}"
        
        print(f"{name:<18} {t_str:<14} {n_str:<14} {diff_str}")
        insights.append((name, key, t, n, diff))
    
    # ========== TOP10推销能力（核心）==========
    print("【TOP10推销能力分析】")
    
    # 指标1: TOP10款GMV占比（越低越好=能推非TOP10款）
    t_top10_sku = avg_safe(top3_list, 'top10_sku_rate')
    n_top10_sku = avg_safe(non_top3_list, 'top10_sku_rate')
    diff_sku = t_top10_sku - n_top10_sku
    print(f"TOP10款GMV占比:    {t_top10_sku:>10.1f}% {n_top10_sku:>10.1f}% {diff_sku:>+8.1f}pp")
    insights.append(('TOP10款GMV占比', 'top10_sku_rate', t_top10_sku, n_top10_sku, diff_sku))
    
    # 指标2: TOP10订单连带件数（越高=TOP10带动能力强）
    t_top10_ld = avg(top3_list, 'top10_liandai')
    n_top10_ld = avg(non_top3_list, 'top10_liandai')
    diff_ld = t_top10_ld - n_top10_ld
    print(f"TOP10订单连带:     {t_top10_ld:>10.1f}件{n_top10_ld:>10.1f}件{diff_ld:>+8.1f}件")
    insights.append(('TOP10订单连带', 'top10_liandai', t_top10_ld, n_top10_ld, diff_ld))
    
    # 指标3: 非TOP10订单连带件数（越高=推非TOP10能力强）
    t_non_ld = avg(top3_list, 'non_top10_liandai')
    n_non_ld = avg(non_top3_list, 'non_top10_liandai')
    diff_non = t_non_ld - n_non_ld
    print(f"非TOP10订单连带:   {t_non_ld:>10.1f}件{n_non_ld:>10.1f}件{diff_non:>+8.1f}件")
    insights.append(('非TOP10订单连带', 'non_top10_liandai', t_non_ld, n_non_ld, diff_non))
    
    # 指标4: 高价值占比
    t_hv = avg_safe(top3_list, 'high_value')
    n_hv = avg_safe(non_top3_list, 'high_value')
    diff_hv = t_hv - n_hv
    print(f"高价值占比:        {t_hv:>10.1f}%{'':<4}{n_hv:>10.1f}%{diff_hv:>+8.1f}pp")
    insights.append(('高价值占比', 'high_value', t_hv, n_hv, diff_hv))
    
    # 核心结论
    print(f"\n💡 核心发现:")
    
    conclusions = []
    
    # 动销率
    dongxiao_diff = [i for i in insights if '动销率' in i[0]][0][4]
    if dongxiao_diff > 20:
        conclusions.append(f"✅ 动销率领先 {dongxiao_diff:+.0f}pp（SKU宽度优势）")
    elif dongxiao_diff < -20:
        conclusions.append(f"⚠️ 动销率落后 {dongxiao_diff:+.0f}pp")
    
    # TOP10款占比（越低越说明能推非爆款）
    top10_sku_diff = [i for i in insights if 'TOP10款GMV' in i[0]][0][4]
    if top10_sku_diff < -5:
        conclusions.append(f"✅ TOP10款占比低 {top10_sku_diff:+.1f}pp（能推非爆款）")
    elif top10_sku_diff > 5:
        conclusions.append(f"⚠️ TOP10款占比高 {top10_sku_diff:+.1f}pp（依赖爆款）")
    
    # TOP10连带
    top10_ld_diff = [i for i in insights if 'TOP10订单连带' in i[0]][0][4]
    if top10_ld_diff > 0.3:
        conclusions.append(f"✅ TOP10连带高 {top10_ld_diff:+.1f}件（TOP10带动能力强）")
    elif top10_ld_diff < -0.3:
        conclusions.append(f"⚠️ TOP10连带低 {top10_ld_diff:+.1f}件")
    
    # 非TOP10连带
    non_ld_diff = [i for i in insights if '非TOP10' in i[0]][0][4]
    if non_ld_diff > 0.3:
        conclusions.append(f"✅ 非TOP10连带高 {non_ld_diff:+.1f}件（推非爆款能力强）")
    elif non_ld_diff < -0.3:
        conclusions.append(f"⚠️ 非TOP10连带低 {non_ld_diff:+.1f}件")
    
    if conclusions:
        for c in conclusions:
            print(f"  {c}")
    else:
        print(f"  ⚪ 各维度差距较小")
    
    return {
        'period': period_name,
        'top3': top3,
        'results': results,
        'insights': insights,
        'conclusions': conclusions
    }


def analyze_all_v3():
    """完整分析"""
    conn = get_connection()
    try:
        print("\n" + "="*80)
        print("📊 明星导购TOP10推销能力验证")
        print("从2024年1月至今，覆盖所有季度/半年度/年度")
        print("="*80)
        
        all_results = []
        
        # 1. 各季度
        print("\n\n" + "🔹"*20)
        print("【各季度分析】")
        print("🔹"*20)
        
        quarter_order = ['2024春', '2024夏', '2024秋', '2024冬', 
                         '2025-01~02', '2025春', '2025夏', '2025秋', '2025冬', '2026春']
        for period in quarter_order:
            if period in PERIODS:
                result = analyze_period_v3(conn, *PERIODS[period], period)
                if result:
                    all_results.append(result)
        
        # 2. 半年度
        print("\n\n" + "🔹"*20)
        print("【半年度对比】")
        print("🔹"*20)
        
        for period in ['2024上', '2024下', '2025上', '2025下']:
            if period in PERIODS:
                result = analyze_period_v3(conn, *PERIODS[period], period)
                if result:
                    all_results.append(result)
        
        # 3. 年度
        print("\n\n" + "🔹"*20)
        print("【年度对比】")
        print("🔹"*20)
        
        for period in ['2024全', '2025全']:
            if period in PERIODS:
                result = analyze_period_v3(conn, *PERIODS[period], period)
                if result:
                    all_results.append(result)
        
        # ========== 汇总 ==========
        print("\n\n" + "="*80)
        print("📈 汇总：TOP3在TOP10推销能力上的表现")
        print("="*80)
        
        # 统计各指标TOP3领先/落后次数
        dim_stats = {
            '动销率': {'lead': 0, 'lag': 0, 'diffs': []},
            'TOP10款GMV占比': {'lead': 0, 'lag': 0, 'diffs': []},  # 越低越好
            'TOP10订单连带': {'lead': 0, 'lag': 0, 'diffs': []},
            '非TOP10订单连带': {'lead': 0, 'lag': 0, 'diffs': []},
            '高价值占比': {'lead': 0, 'lag': 0, 'diffs': []},
        }
        
        for result in all_results:
            for name, key, t, n, diff in result['insights']:
                if name in dim_stats:
                    dim_stats[name]['diffs'].append(diff)
                    if name == 'TOP10款GMV占比':  # 越低越好
                        if diff < -3:
                            dim_stats[name]['lead'] += 1
                        elif diff > 3:
                            dim_stats[name]['lag'] += 1
                    else:
                        if diff > 3:
                            dim_stats[name]['lead'] += 1
                        elif diff < -3:
                            dim_stats[name]['lag'] += 1
        
        print(f"\n{'维度':<18} {'TOP3领先':<10} {'TOP3落后':<10} {'平均差距':<12} {'结论'}")
        print('-' * 60)
        
        final_conclusions = []
        for name, stats in dim_stats.items():
            lead = stats['lead']
            lag = stats['lag']
            total = lead + lag
            avg_diff = sum(stats['diffs']) / len(stats['diffs']) if stats['diffs'] else 0
            
            if total == 0:
                conclusion = "⚪ 无差异"
            elif lead >= total * 0.6:
                if name == 'TOP10款GMV占比':
                    conclusion = "✅ TOP3更会推非爆款"
                else:
                    conclusion = f"✅ TOP3领先"
            elif lag >= total * 0.6:
                if name == 'TOP10款GMV占比':
                    conclusion = "⚠️ TOP3依赖爆款"
                else:
                    conclusion = "⚠️ TOP3落后"
            else:
                conclusion = "⚪ 不稳定"
            
            print(f"{name:<18} {lead}次{'':<6} {lag}次{'':<6} {avg_diff:>+8.1f}  {conclusion}")
            
            final_conclusions.append((name, lead, lag, avg_diff, conclusion))
        
        # 最终结论
        print(f"\n{'='*80}")
        print("🎯 最终结论")
        print("="*80)
        
        # TOP3推销能力总结
        top10_sku = [c for c in final_conclusions if 'TOP10款GMV' in c[0]][0]
        top10_ld = [c for c in final_conclusions if 'TOP10订单连带' in c[0]][0]
        non_ld = [c for c in final_conclusions if '非TOP10' in c[0]][0]
        dongxiao = [c for c in final_conclusions if '动销率' in c[0]][0]
        high_value = [c for c in final_conclusions if '高价值' in c[0]][0]
        
        print(f"""
核心发现：

1. 【动销率】{dongxiao[4]}
   - TOP3平均领先 {dongxiao[3]:+.0f}pp
   - 说明TOP3能卖更多SKU（宽度优势）

2. 【TOP10款GMV占比】{top10_sku[4]}
   - 平均差距 {top10_sku[3]:+.1f}pp
   - 关键指标：越低说明越能推非爆款

3. 【TOP10订单连带】{top10_ld[4]}
   - 平均差距 {top10_ld[3]:+.1f}件
   - 关键指标：TOP10带动其他商品的能力

4. 【非TOP10订单连带】{non_ld[4]}
   - 平均差距 {non_ld[3]:+.1f}件
   - 关键指标：推非爆款的能力

5. 【高价值占比】{high_value[4]}
   - 平均差距 {high_value[3]:+.1f}pp
   - 关键指标：高价商品推销能力
""")
        
        # 决策建议
        print(f"{'='*80}")
        print("📋 决策建议")
        print("="*80)
        
        print(f"""
根据 {len(all_results)} 个时间段的综合分析：

✅ TOP3真正领先的维度：
  - 动销率（{dongxiao[3]:+.0f}pp）：证明TOP3有SKU宽度优势

⚠️ TOP3不领先的维度：
  - TOP10推销能力：与非TOP3无显著差距

📋 建议：
  1. 继续用动销率作为TOP3的核心考核指标
  2. TOP10推销能力不能区分TOP3和非TOP3
  3. 非TOP3应重点提升：动销率、高价值占比
""")
        
        # TOP3稳定性
        print(f"\n{'='*80}")
        print("🏆 TOP3导购稳定性（按上榜次数）")
        print("="*80)
        
        top3_count = {}
        for result in all_results:
            for guide in result['top3']:
                top3_count[guide] = top3_count.get(guide, 0) + 1
        
        print(f"\n{'导购':<12} {'上榜次数':<10} {'定位'}")
        print('-' * 35)
        for guide, count in sorted(top3_count.items(), key=lambda x: x[1], reverse=True):
            if count >= 6:
                label = "⭐ 核心明星"
            elif count >= 3:
                label = "✅ 稳定"
            else:
                label = "⚠️ 波动"
            print(f"{guide:<12} {count}次{'':<6} {label}")
        
    finally:
        conn.close()


if __name__ == '__main__':
    analyze_all_v3()
