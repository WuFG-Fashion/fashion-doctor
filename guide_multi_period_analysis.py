# -*- coding: utf-8 -*-
"""
明星导购多时间段深度分析
分析近7天、近15天、近30天、近45天、近60天、2026年全年
"""
import sqlite3
import sys
import json
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r'C:\Users\MacBookPro\cabbeen_data\cabbeen.db'
TODAY = '2026-04-22'

def get_conn():
    return sqlite3.connect(DB_PATH)

def analyze_period(start_date, end_date, period_name):
    """分析指定时间段"""
    print(f"\n{'='*60}")
    print(f"📊 {period_name} ({start_date} ~ {end_date})")
    print('='*60)
    
    conn = get_conn()
    cursor = conn.cursor()
    
    # 1. 基本统计
    cursor.execute("""
        SELECT COUNT(DISTINCT guide_name), COUNT(*), SUM(qty), SUM(amount)
        FROM sales 
        WHERE date >= ? AND date <= ?
    """, (start_date, end_date))
    basic = cursor.fetchone()
    guide_count, order_count, total_qty, total_gmv = basic
    print(f"导购数: {guide_count}, 订单数: {order_count}, 销量: {total_qty}, GMV: {total_gmv:,.0f}")
    
    # 2. 导购排名
    cursor.execute("""
        SELECT 
            s.guide_name,
            SUM(s.amount) as gmv,
            SUM(s.qty) as qty,
            COUNT(DISTINCT s.order_no) as orders,
            COUNT(DISTINCT s.member_id) as members,
            ROUND(SUM(s.qty) * 1.0 / COUNT(DISTINCT s.order_no), 2) as linkage,
            ROUND(SUM(s.amount) / COUNT(DISTINCT s.order_no), 0) as avg_price,
            COUNT(DISTINCT s.style_code) as sku_count,
            ROUND(COUNT(DISTINCT s.style_code) * 1.0 / COUNT(DISTINCT s.order_no), 1) as sku_per_order
        FROM sales s
        WHERE s.date >= ? AND s.date <= ?
        GROUP BY s.guide_name
        HAVING gmv > 0
        ORDER BY gmv DESC
    """, (start_date, end_date))
    
    guides = []
    for row in cursor.fetchall():
        guide_name, gmv, qty, orders, members, linkage, avg_price, sku_count, sku_per_order = row
        
        # 爆款依赖度（Top1 SKU占比）
        cursor.execute("""
            SELECT SUM(qty) as total_qty
            FROM sales
            WHERE guide_name = ? AND date >= ? AND date <= ?
        """, (guide_name, start_date, end_date))
        total_qty_guide = cursor.fetchone()[0] or 1
        
        cursor.execute("""
            SELECT style_code, SUM(qty) as qty
            FROM sales
            WHERE guide_name = ? AND date >= ? AND date <= ?
            GROUP BY style_code
            ORDER BY qty DESC
            LIMIT 1
        """, (guide_name, start_date, end_date))
        top1_sku = cursor.fetchone()
        top1_ratio = (top1_sku[1] / total_qty_guide * 100) if top1_sku else 0
        
        # VIP统计
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT order_no) as vip_orders,
                SUM(amount) as vip_gmv,
                COUNT(DISTINCT member_id) as vip_members,
                ROUND(SUM(qty) * 1.0 / COUNT(DISTINCT order_no), 2) as vip_linkage,
                ROUND(SUM(amount) / COUNT(DISTINCT order_no), 0) as vip_avg_price
            FROM sales
            WHERE guide_name = ? AND date >= ? AND date <= ? AND member_id IS NOT NULL
        """, (guide_name, start_date, end_date))
        vip_stats = cursor.fetchone()
        vip_orders, vip_gmv, vip_members, vip_linkage, vip_avg_price = vip_stats
        
        vip_rate = (vip_orders / orders * 100) if orders > 0 else 0
        vip_gmv_rate = (vip_gmv / gmv * 100) if gmv > 0 else 0
        
        # 复购会员（买了>=2次的会员）
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT member_id
                FROM sales
                WHERE guide_name = ? AND date >= ? AND date <= ? AND member_id IS NOT NULL
                GROUP BY member_id
                HAVING COUNT(DISTINCT order_no) >= 2
            )
        """, (guide_name, start_date, end_date))
        repurchase_mem = cursor.fetchone()[0]
        repurchase_rate = (repurchase_mem / vip_members * 100) if vip_members > 0 else 0
        
        # 新VIP数（只看该时间段内的首次购买）
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT member_id, MIN(date) as first_date
                FROM sales
                WHERE guide_name = ? AND member_id IS NOT NULL
                GROUP BY member_id
                HAVING first_date >= ? AND first_date <= ?
            )
        """, (guide_name, start_date, end_date))
        new_vip = cursor.fetchone()[0]
        new_vip_rate = (new_vip / vip_members * 100) if vip_members > 0 else 0
        
        # 高价商品占比（吊牌价>800）
        cursor.execute("""
            SELECT SUM(gmv)
            FROM (
                SELECT SUM(s.amount) as gmv
                FROM sales s
                JOIN goods g ON s.style_code = g.style_code
                WHERE s.guide_name = ? AND s.date >= ? AND s.date <= ? AND g.tag_price > 800
                GROUP BY s.style_code
            )
        """, (guide_name, start_date, end_date))
        high_gmv = cursor.fetchone()[0] or 0
        high_price_rate = (high_gmv / gmv * 100) if gmv > 0 else 0
        
        # 品类统计
        cursor.execute("""
            SELECT COUNT(DISTINCT category)
            FROM sales
            WHERE guide_name = ? AND date >= ? AND date <= ?
        """, (guide_name, start_date, end_date))
        cat_count = cursor.fetchone()[0]
        
        guides.append({
            'name': guide_name,
            'gmv': gmv,
            'qty': qty,
            'orders': orders,
            'members': members,
            'linkage': linkage,
            'avg_price': avg_price,
            'sku_count': sku_count,
            'sku_per_order': sku_per_order,
            'top1_ratio': round(top1_ratio, 1),
            'vip_orders': vip_orders,
            'vip_rate': round(vip_rate, 1),
            'vip_gmv_rate': round(vip_gmv_rate, 1),
            'vip_linkage': vip_linkage,
            'vip_avg_price': vip_avg_price,
            'repurchase_mem': repurchase_mem,
            'repurchase_rate': round(repurchase_rate, 1),
            'new_vip': new_vip,
            'new_vip_rate': round(new_vip_rate, 1),
            'high_gmv': high_gmv,
            'high_price_rate': round(high_price_rate, 1),
            'cat_count': cat_count
        })
    
    conn.close()
    
    # TOP3分析
    if len(guides) >= 3:
        top3 = guides[:3]
        all_avg = {
            'vip_rate': sum(g['vip_rate'] for g in guides) / len(guides),
            'new_vip_rate': sum(g['new_vip_rate'] for g in guides) / len(guides),
            'repurchase_rate': sum(g['repurchase_rate'] for g in guides) / len(guides),
            'sku_count': sum(g['sku_count'] for g in guides) / len(guides),
            'top1_ratio': sum(g['top1_ratio'] for g in guides) / len(guides),
            'high_price_rate': sum(g['high_price_rate'] for g in guides) / len(guides),
        }
        top3_avg = {
            'vip_rate': sum(g['vip_rate'] for g in top3) / 3,
            'new_vip_rate': sum(g['new_vip_rate'] for g in top3) / 3,
            'repurchase_rate': sum(g['repurchase_rate'] for g in top3) / 3,
            'sku_count': sum(g['sku_count'] for g in top3) / 3,
            'top1_ratio': sum(g['top1_ratio'] for g in top3) / 3,
            'high_price_rate': sum(g['high_price_rate'] for g in top3) / 3,
        }
        
        print(f"\n🏆 TOP3 排名:")
        for i, g in enumerate(top3, 1):
            print(f"  {i}. {g['name']}: GMV {g['gmv']:,.0f} | 客单{g['avg_price']:.0f} | 连带{g['linkage']}件 | SKU {g['sku_count']}个 | 爆款{g['top1_ratio']}%")
        
        print(f"\n📈 TOP3 vs 全员 均值对比:")
        print(f"  {'指标':<15} {'TOP3':>10} {'全员':>10} {'差距':>10}")
        print(f"  {'-'*45}")
        for key in ['vip_rate', 'new_vip_rate', 'repurchase_rate', 'sku_count', 'top1_ratio', 'high_price_rate']:
            label = {
                'vip_rate': 'VIP订单率',
                'new_vip_rate': '新VIP率',
                'repurchase_rate': '复购率',
                'sku_count': 'SKU数',
                'top1_ratio': '爆款依赖',
                'high_price_rate': '高价占比'
            }[key]
            top3_val = top3_avg[key]
            all_val = all_avg[key]
            diff = top3_val - all_val
            diff_str = f"{diff:+.1f}" if key in ['sku_count'] else f"{diff:+.1f}%"
            print(f"  {label:<15} {top3_val:>10.1f} {all_val:>10.1f} {diff_str:>10}")
    
    return guides

def main():
    # 定义时间段
    periods = [
        ('2026-04-16', '2026-04-22', '近7天'),
        ('2026-04-08', '2026-04-22', '近15天'),
        ('2026-03-23', '2026-04-22', '近30天'),
        ('2026-03-08', '2026-04-22', '近45天'),
        ('2026-02-21', '2026-04-22', '近60天'),
        ('2026-01-01', '2026-04-22', '2026年全年'),
    ]
    
    # 检查数据库数据范围
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(date), MAX(date) FROM sales")
    date_range = cursor.fetchone()
    print(f"\n📅 数据库日期范围: {date_range[0]} ~ {date_range[1]}")
    conn.close()
    
    all_results = {}
    
    for start_date, end_date, period_name in periods:
        results = analyze_period(start_date, end_date, period_name)
        all_results[period_name] = {
            'period': f"{start_date} ~ {end_date}",
            'guides': results
        }
    
    # 保存完整结果
    output_path = r'C:\Users\MacBookPro\Fashion Doctor\guide_multi_period_results.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {output_path}")
    
    # 跨时间段对比
    print(f"\n{'='*60}")
    print("📊 跨时间段对比：TOP3变化")
    print('='*60)
    
    for period_name, data in all_results.items():
        guides = data['guides']
        if len(guides) >= 3:
            top3_names = [g['name'] for g in guides[:3]]
            print(f"{period_name:<12}: {' > '.join(top3_names)}")

if __name__ == '__main__':
    main()
