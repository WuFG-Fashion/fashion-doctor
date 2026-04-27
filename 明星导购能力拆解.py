# -*- coding: utf-8 -*-
"""
明星导购能力分析工具 v2.0
包含决策指南和行动建议
"""

import sqlite3
import sys
from datetime import datetime, timedelta

# 配置
DB_PATH = r'C:\Users\MacBookPro\cabbeen_data\cabbeen.db'
DEFAULT_DAYS = 30

sys.stdout.reconfigure(encoding='utf-8')


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_top3_guides(conn, days=30):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    cur = conn.cursor()
    cur.execute('''
        SELECT guide_name, SUM(amount) as gmv
        FROM sales WHERE sale_date >= ? AND sale_date <= ?
        GROUP BY guide_name ORDER BY gmv DESC LIMIT 3
    ''', (start_date, end_date))
    return [r[0] for r in cur.fetchall()]


def get_all_guides_data(conn, days=30, top3=None):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    cur = conn.cursor()
    cur.execute('''
        SELECT guide_name, SUM(amount) as gmv, COUNT(DISTINCT order_no) as orders,
               SUM(qty) as total_qty, COUNT(DISTINCT member_id) as members
        FROM sales WHERE sale_date >= ? AND sale_date <= ?
        GROUP BY guide_name
    ''', (start_date, end_date))
    results = []
    for r in cur.fetchall():
        guide, gmv, orders, qty, members = r
        results.append({
            'guide': guide, 'gmv': gmv or 0, 'orders': orders or 0,
            'qty': qty or 0, 'members': members or 0,
            'is_top3': guide in top3 if top3 else False
        })
    return results


def get_dongxiao_rate(conn, guide_name, days=30):
    """正确计算动销率：导购2026夏销售SKU ÷ 店铺2026夏库存SKU"""
    cur = conn.cursor()
    
    # 获取该导购所在店铺
    cur.execute('SELECT DISTINCT shop_name FROM sales WHERE guide_name = ?', (guide_name,))
    shops = [r[0] for r in cur.fetchall()]
    if not shops:
        return 0, 0, 0
    
    # 店铺2026夏库存SKU数（用style_color去重）
    best_shop = None
    max_sku = 0
    for shop in shops:
        cur.execute('''
            SELECT COUNT(DISTINCT style_color) 
            FROM inventory WHERE year = 2026 AND season = '夏' AND shop_name = ?
        ''', (shop,))
        cnt = cur.fetchone()[0] or 0
        if cnt > max_sku:
            max_sku = cnt
            best_shop = shop
    
    if max_sku == 0:
        return 0, 0, 0
    
    # 该导购2026夏销售SKU数
    cur.execute('''
        SELECT COUNT(DISTINCT style_color)
        FROM sales WHERE guide_name = ? AND year = 2026 AND season = '夏'
    ''', (guide_name,))
    guide_sku = cur.fetchone()[0] or 0
    
    return guide_sku, max_sku, guide_sku / max_sku * 100


def get_top10_order_gmv_rate(conn, guide_name, days=30):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    cur = conn.cursor()
    cur.execute('''
        SELECT style_color FROM (
            SELECT style_color, SUM(qty) as q FROM sales
            WHERE sale_date >= ? AND sale_date <= ?
            GROUP BY style_color ORDER BY q DESC LIMIT 10
        )
    ''', (start_date, end_date))
    top10 = [r[0] for r in cur.fetchall()]
    if not top10:
        return 0, 0, 0
    placeholders = ','.join('?' * len(top10))
    cur.execute('SELECT SUM(amount) FROM sales WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ?',
                (start_date, end_date, guide_name))
    total = cur.fetchone()[0] or 0
    cur.execute(f'''
        SELECT SUM(s.amount) FROM sales s WHERE s.sale_date >= ? AND s.sale_date <= ? AND s.guide_name = ?
        AND s.order_no IN (SELECT DISTINCT order_no FROM sales WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders}))
    ''', [start_date, end_date, guide_name, start_date, end_date] + top10)
    top10_amt = cur.fetchone()[0] or 0
    return top10_amt, total, top10_amt / total * 100 if total > 0 else 0


def get_high_value_rate(conn, guide_name, days=30):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    cur = conn.cursor()
    cur.execute('SELECT tag_price FROM sales WHERE sale_date >= ? AND sale_date <= ?',
                (start_date, end_date))
    prices = [r[0] for r in cur.fetchall() if r[0]]
    if not prices:
        return 0
    threshold = sorted(prices)[int(len(prices) * 0.75)]
    cur.execute('SELECT SUM(amount) FROM sales WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ?',
                (start_date, end_date, guide_name))
    total = cur.fetchone()[0] or 0
    cur.execute('SELECT SUM(amount) FROM sales WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ? AND tag_price >= ?',
                (start_date, end_date, guide_name, threshold))
    high = cur.fetchone()[0] or 0
    return high / total * 100 if total > 0 else 0


def calculate_all_metrics(conn, days=30):
    top3 = get_top3_guides(conn, days)
    all_guides = get_all_guides_data(conn, days, top3)
    results = []
    for g in all_guides:
        guide = g['guide']
        top10_gmv, total, top10_rate = get_top10_order_gmv_rate(conn, guide, days)
        guide_sku, shop_sku, dongxiao = get_dongxiao_rate(conn, guide, days)
        high_value = get_high_value_rate(conn, guide, days)
        avg_price = g['gmv'] / g['orders'] if g['orders'] > 0 else 0
        lian_dai = g['qty'] / g['orders'] if g['orders'] > 0 else 0
        results.append({
            'guide': guide, 'gmv': g['gmv'], 'orders': g['orders'],
            'avg_price': avg_price, 'lian_dai': lian_dai,
            'dongxiao': dongxiao, 'guide_sku': guide_sku, 'shop_sku': shop_sku,
            'top10_rate': top10_rate, 'high_value': high_value, 'is_top3': g['is_top3']
        })
    return top3, results


def get_decision_guide(days):
    """根据时间维度返回决策指南"""
    guides = {
        7: {
            'name': '近7天',
            'scenario': '即时激励',
            'top3_action': '保持状态',
            'non_top3_action': '快速跟进',
            'threshold': 15,  # 宽松阈值
            'warning': '样本量小，不宜作为考核依据'
        },
        15: {
            'name': '近15天',
            'scenario': '日常参考',
            'top3_action': '巩固优势',
            'non_top3_action': '针对性提升',
            'threshold': 10,
            'warning': '可作为调整策略的参考'
        },
        30: {
            'name': '近30天',
            'scenario': '常规考核',
            'top3_action': '传授经验',
            'non_top3_action': '补齐短板',
            'threshold': 5,
            'warning': '标准考核周期'
        },
        45: {
            'name': '近45天',
            'scenario': '深度分析',
            'top3_action': '团队赋能',
            'non_top3_action': '制定计划',
            'threshold': 5,
            'warning': '深度诊断周期'
        },
        365: {
            'name': '全年',
            'scenario': '年度评优',
            'top3_action': '嘉奖激励',
            'non_top3_action': '制定提升计划',
            'threshold': 5,
            'warning': '年度评优依据'
        }
    }
    return guides.get(days, guides[30])


def generate_action_suggestions(results, top3, threshold=5):
    """生成行动建议（过滤小样本）"""
    top3_list = [r for r in results if r['is_top3']]
    non_top3_list = [r for r in results if not r['is_top3']]
    
    def avg(lst, key):
        return sum(r[key] for r in lst) / len(lst) if lst else 0
    
    suggestions = []
    
    # 计算TOP3均值
    top3_dongxiao = avg(top3_list, 'dongxiao')
    top3_high_value = avg(top3_list, 'high_value')
    top3_top10 = avg(top3_list, 'top10_rate')
    
    # 对每个非TOP3生成建议（过滤GMV<5000的小样本）
    for r in non_top3_list:
        if r['gmv'] < 5000:  # 过滤小样本
            continue
        
        gaps = []
        actions = []
        
        if r['dongxiao'] < top3_dongxiao - threshold:
            gaps.append(f"动销率低({r['dongxiao']:.1f}% vs TOP3均值{top3_dongxiao:.1f}%)")
            if r['guide_sku'] < 30:
                actions.append("✅ 主动推荐更多SKU")
        
        if r['high_value'] < top3_high_value - threshold:
            gaps.append(f"高价值占比低({r['high_value']:.1f}% vs TOP3均值{top3_high_value:.1f}%)")
            actions.append("✅ 主推高价商品")
        
        if r['top10_rate'] < top3_top10 - threshold * 2:
            gaps.append(f"TOP10关联率低({r['top10_rate']:.1f}% vs TOP3均值{top3_top10:.1f}%)")
            actions.append("✅ 用TOP10款引流连带")
        
        if gaps:
            suggestions.append({
                'guide': r['guide'],
                'gmv': r['gmv'],
                'orders': r['orders'],
                'gaps': gaps,
                'actions': actions,
                'priority': '高' if len(gaps) >= 2 else '中'
            })
    
    return suggestions


def print_full_report(top3, results, days=30):
    guide = get_decision_guide(days)
    
    print(f"\n{'='*70}")
    print(f"【明星导购能力分析】{guide['name']}")
    print(f"{'='*70}")
    print(f"场景: {guide['scenario']} | 阈值: ±{guide['threshold']}pp | {guide['warning']}")
    
    top3_list = [r for r in results if r['is_top3']]
    non_top3_list = [r for r in results if not r['is_top3']]
    
    def avg(lst, key):
        return sum(r[key] for r in lst) / len(lst) if lst else 0
    
    print(f"\nTOP3: {', '.join(top3)}")
    print(f"\n{'='*70}")
    print("【TOP3 vs 非TOP3 核心指标对比】")
    print(f"{'='*70}")
    
    metrics = [
        ('动销率', 'dongxiao', '%', 20),
        ('客单价', 'avg_price', '元', 200),
        ('连带件数', 'lian_dai', '件', 0.5),
        ('TOP10关联率', 'top10_rate', '%', 15),
        ('高价值占比', 'high_value', '%', 10),
    ]
    
    print(f"\n{'维度':<12} {'TOP3':<12} {'非TOP3':<12} {'差距':<12}")
    print("-" * 50)
    
    for name, key, unit, _ in metrics:
        t = avg(top3_list, key)
        n = avg(non_top3_list, key)
        diff = t - n
        if unit == '元':
            print(f"{name:<12} {t:>8.0f}{unit:<4} {n:>8.0f}{unit:<4} {diff:+.0f}元")
        elif name == '动销率':
            # 动销率特殊显示：显示为 XX%(XX/XX)
            t_sku = avg(top3_list, 'guide_sku')
            t_total = avg(top3_list, 'shop_sku')
            n_sku = avg(non_top3_list, 'guide_sku')
            n_total = avg(non_top3_list, 'shop_sku')
            print(f"{name:<12} {t:>6.1f}%{'':<2}({t_sku:.0f}/{t_total:.0f}) {n:>6.1f}%{'':<2}({n_sku:.0f}/{n_total:.0f}) {diff:+.1f}pp")
        else:
            print(f"{name:<12} {t:>8.1f}{unit:<4} {n:>8.1f}{unit:<4} {diff:+.1f}pp")
    
    # 行动建议
    print(f"\n{'='*70}")
    print("【行动建议】")
    print(f"{'='*70}")
    print(f"\n▶ {guide['name']} {guide['scenario']}建议:")
    print(f"  TOP3: {guide['top3_action']}")
    print(f"  非TOP3: {guide['non_top3_action']}")
    
    suggestions = generate_action_suggestions(results, top3, guide['threshold'])
    if suggestions:
        print(f"\n▶ 非TOP3待改进导购 ({len(suggestions)}人，GMV≥5000过滤小样本):")
        for s in sorted(suggestions, key=lambda x: x['gmv'], reverse=True):
            print(f"\n  【{s['priority']}】{s['guide']}")
            print(f"      GMV: {s['gmv']:,.0f}元 | 订单: {s['orders']}笔")
            for g in s['gaps']:
                print(f"      - {g}")
            if s['actions']:
                print(f"      → 建议: {' / '.join(s['actions'])}")
    else:
        print("\n✅ 非TOP3表现良好，无明显短板")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='明星导购能力分析工具')
    parser.add_argument('--days', type=int, default=DEFAULT_DAYS, help='分析时间范围（天）')
    args = parser.parse_args()
    
    conn = get_connection()
    try:
        top3, results = calculate_all_metrics(conn, args.days)
        print_full_report(top3, results, args.days)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
