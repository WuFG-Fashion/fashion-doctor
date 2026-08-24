"""
明星导购能力拆解 - 核心维度分析 v2
保留维度：SKU宽度、TOP10关联率、高价值占比、VIP率/复购率、新开卡人数、客单/连带/折扣率、单款销售深度
"""
import os
from pathlib import Path

import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime, timedelta

DB_PATH = os.environ.get("CABBEEN_DB") or str(Path(__file__).resolve().parents[1] / "cabbeen.db")

def get_date_range(days):
    """获取日期范围"""
    if days == 'full':
        return '2026-01-01', '2026-04-22'
    else:
        end = '2026-04-22'
        start = (datetime(2026, 4, 22) - timedelta(days=days)).strftime('%Y-%m-%d')
        return start, end

def analyze_period(days, period_name):
    """分析指定时间段"""
    start_date, end_date = get_date_range(days)
    
    sql = f"""
        SELECT s.guide_name,
               SUM(s.amount) as gmv,
               SUM(s.qty) as qty,
               COUNT(DISTINCT s.order_no) as orders,
               COUNT(DISTINCT CASE WHEN s.is_vip = 1 THEN s.member_id END) as vip_members,
               COUNT(DISTINCT CASE WHEN s.is_vip = 1 THEN s.order_no END) as vip_orders,
               COUNT(DISTINCT s.style_code) as sku_count,
               ROUND(SUM(CASE WHEN s.is_vip = 1 THEN s.amount ELSE 0 END) / NULLIF(SUM(s.amount), 0) * 100, 1) as vip_gmv_rate,
               ROUND(SUM(s.amount) / COUNT(DISTINCT s.order_no), 0) as avg_price,
               ROUND(SUM(s.qty) / COUNT(DISTINCT s.order_no), 2) as linkage,
               ROUND(SUM(s.amount) / SUM(s.tag_amount) * 10, 1) as disc_rate,
               ROUND(SUM(CASE WHEN s.tag_price > 800 THEN s.amount ELSE 0 END) / NULLIF(SUM(s.amount), 0) * 100, 1) as high_value_rate
        FROM sales s
        WHERE s.sale_date >= '{start_date}' AND s.sale_date <= '{end_date}'
        GROUP BY s.guide_name
        HAVING orders >= 5
        ORDER BY gmv DESC
    """
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    
    all_guides = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    if not all_guides:
        return None
    
    # 计算复购率
    for g in all_guides:
        guide = g['guide_name']
        
        # 复购率：有2笔以上订单的会员比例
        repurchase_sql = f"""
            SELECT COUNT(DISTINCT member_id) as total_members,
                   SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) as repeat_members
            FROM (
                SELECT member_id, COUNT(DISTINCT order_no) as order_count
                FROM sales
                WHERE guide_name = '{guide}' AND sale_date >= '{start_date}' AND sale_date <= '{end_date}' AND is_vip = 1
                GROUP BY member_id
            )
        """
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(repurchase_sql)
        row = cur.fetchone()
        conn.close()
        
        total = row[0] or 0
        repeat = row[1] or 0
        g['repurchase_rate'] = round(repeat / total * 100, 1) if total > 0 else 0
        g['new_vip'] = total  # VIP会员数
    
    # 计算TOP10关联率
    for g in all_guides:
        guide = g['guide_name']
        
        # 找出TOP10款
        top10_sql = f"""
            SELECT style_code FROM (
                SELECT style_code, SUM(qty) as total_qty
                FROM sales
                WHERE guide_name = '{guide}' AND sale_date >= '{start_date}' AND sale_date <= '{end_date}'
                GROUP BY style_code
                ORDER BY total_qty DESC
                LIMIT 10
            )
        """
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(top10_sql)
        top10_skus = [r[0] for r in cur.fetchall()]
        conn.close()
        
        if not top10_skus:
            g['top10_order_rate'] = 0
            g['top10_order_cnt'] = 0
            g['top10_order_avg'] = 0
            g['top1_qty_rate'] = 0
            g['top3_qty_rate'] = 0
            g['top10_qty_rate'] = 0
            g['top1_qty'] = 0
            g['top1_order_avg'] = 0
            continue
        
        # 计算TOP10关联的订单
        top10_order_sql = f"""
            SELECT order_no, SUM(amount) as order_amount
            FROM sales
            WHERE guide_name = '{guide}' AND sale_date >= '{start_date}' AND sale_date <= '{end_date}'
            AND style_code IN ({','.join(repr(s) for s in top10_skus)})
            GROUP BY order_no
        """
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(top10_order_sql)
        top10_orders = cur.fetchall()
        conn.close()
        
        top10_order_ids = [r[0] for r in top10_orders]
        top10_order_gmv = sum(r[1] for r in top10_orders)
        
        g['top10_order_rate'] = round(top10_order_gmv / g['gmv'] * 100, 1) if g['gmv'] > 0 else 0
        g['top10_order_cnt'] = len(top10_order_ids)
        g['top10_order_avg'] = round(top10_order_gmv / len(top10_order_ids), 0) if top10_order_ids else 0
        
        # 单款销售深度
        sku_qty_sql = f"""
            SELECT style_code, SUM(qty) as total_qty, SUM(amount) as total_amount, COUNT(DISTINCT order_no) as order_count
            FROM sales
            WHERE guide_name = '{guide}' AND sale_date >= '{start_date}' AND sale_date <= '{end_date}'
            GROUP BY style_code
            ORDER BY total_qty DESC
        """
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(sku_qty_sql)
        sku_rows = cur.fetchall()
        conn.close()
        
        if sku_rows:
            total_qty = sum(r[1] for r in sku_rows)
            g['top1_qty_rate'] = round(sku_rows[0][1] / total_qty * 100, 1) if total_qty > 0 else 0
            g['top3_qty_rate'] = round(sum(r[1] for r in sku_rows[:3]) / total_qty * 100, 1) if total_qty > 0 else 0
            g['top10_qty_rate'] = round(sum(r[1] for r in sku_rows[:10]) / total_qty * 100, 1) if total_qty > 0 else 0
            g['top1_qty'] = sku_rows[0][1]
            g['top1_order_avg'] = round(sku_rows[0][2] / sku_rows[0][3], 0) if sku_rows[0][3] > 0 else 0
        else:
            g['top1_qty_rate'] = 0
            g['top3_qty_rate'] = 0
            g['top10_qty_rate'] = 0
            g['top1_qty'] = 0
            g['top1_order_avg'] = 0
    
    # 计算TOP3和全员平均
    top3 = all_guides[:3]
    
    avg_all = {}
    for key in ['sku_count', 'vip_gmv_rate', 'vip_orders', 'repurchase_rate', 'new_vip', 
                'avg_price', 'linkage', 'disc_rate', 'high_value_rate',
                'top10_order_rate', 'top10_qty_rate', 'top1_qty_rate']:
        if key in all_guides[0]:
            avg_all[key] = round(sum(g[key] for g in all_guides) / len(all_guides), 1)
    
    avg_top3 = {}
    for key in avg_all:
        avg_top3[key] = round(sum(g[key] for g in top3) / len(top3), 1)
    
    return {
        'period': f'{start_date} ~ {end_date}',
        'all_data': all_guides,
        'top3': top3,
        'avg_all': avg_all,
        'avg_top3': avg_top3,
        'guide_count': len(all_guides),
        'total_gmv': sum(g['gmv'] for g in all_guides),
    }

def main():
    import json
    
    periods = [
        (7, '近7天'),
        (15, '近15天'),
        (30, '近30天'),
        (45, '近45天'),
        (60, '近60天'),
        ('full', '2026年全年'),
    ]
    
    all_results = []
    
    for days, name in periods:
        print(f'\n{"="*60}')
        print(f'【{name}】')
        print(f'{"="*60}')
        
        result = analyze_period(days, name)
        if not result:
            print('数据不足，跳过')
            continue
        
        all_results.append(result)
        
        print(f'\n[基础数据]')
        print(f'  导购数: {result["guide_count"]}人')
        print(f'  总GMV: {result["total_gmv"]:,.0f}元')
        
        print(f'\n[TOP3 GMV排名]')
        for i, g in enumerate(result['top3'], 1):
            print(f'  {i}. {g["guide_name"]}: {g["gmv"]:,.0f}元 ({g["orders"]}单)')
        
        print(f'\n[核心指标对比: TOP3 vs 全员]')
        print(f'  {"指标":<20} {"TOP3":>10} {"全员":>10} {"差距":>10}')
        print(f'  {"-"*55}')
        
        # SKU宽度
        sku_diff = (result["avg_top3"]["sku_count"]/result["avg_all"]["sku_count"]-1)*100 if result["avg_all"]["sku_count"] else 0
        print(f'  {"SKU宽度":<20} {result["avg_top3"]["sku_count"]:>10.0f} {result["avg_all"]["sku_count"]:>10.0f} {sku_diff:>+8.1f}%')
        
        # TOP10关联率(销售额)
        rate_diff = result["avg_top3"]["top10_order_rate"]-result["avg_all"]["top10_order_rate"]
        print(f'  {"TOP10关联率(销售)":<20} {result["avg_top3"]["top10_order_rate"]:>9.1f}% {result["avg_all"]["top10_order_rate"]:>9.1f}% {rate_diff:>+8.1f}pp')
        
        # TOP10关联率(销量)
        qty_diff = result["avg_top3"]["top10_qty_rate"]-result["avg_all"]["top10_qty_rate"]
        print(f'  {"TOP10关联率(销量)":<20} {result["avg_top3"]["top10_qty_rate"]:>9.1f}% {result["avg_all"]["top10_qty_rate"]:>9.1f}% {qty_diff:>+8.1f}pp')
        
        # 高价值占比
        hv_diff = result["avg_top3"]["high_value_rate"]-result["avg_all"]["high_value_rate"]
        print(f'  {"高价值占比":<20} {result["avg_top3"]["high_value_rate"]:>9.1f}% {result["avg_all"]["high_value_rate"]:>9.1f}% {hv_diff:>+8.1f}pp')
        
        # VIP率
        vip_diff = result["avg_top3"]["vip_gmv_rate"]-result["avg_all"]["vip_gmv_rate"]
        print(f'  {"VIP GMV占比":<20} {result["avg_top3"]["vip_gmv_rate"]:>9.1f}% {result["avg_all"]["vip_gmv_rate"]:>9.1f}% {vip_diff:>+8.1f}pp')
        
        # 复购率
        rr_diff = result["avg_top3"]["repurchase_rate"]-result["avg_all"]["repurchase_rate"]
        print(f'  {"复购率":<20} {result["avg_top3"]["repurchase_rate"]:>9.1f}% {result["avg_all"]["repurchase_rate"]:>9.1f}% {rr_diff:>+8.1f}pp')
        
        # 新开卡
        nv_diff = result["avg_top3"]["new_vip"]-result["avg_all"]["new_vip"]
        print(f'  {"VIP会员数":<20} {result["avg_top3"]["new_vip"]:>10.0f} {result["avg_all"]["new_vip"]:>10.0f} {nv_diff:>+10.0f}')
        
        # 客单价
        ap_diff = (result["avg_top3"]["avg_price"]/result["avg_all"]["avg_price"]-1)*100 if result["avg_all"]["avg_price"] else 0
        print(f'  {"客单价":<20} {result["avg_top3"]["avg_price"]:>10.0f} {result["avg_all"]["avg_price"]:>10.0f} {ap_diff:>+8.1f}%')
        
        # 连带率
        lg_diff = result["avg_top3"]["linkage"]-result["avg_all"]["linkage"]
        print(f'  {"连带率":<20} {result["avg_top3"]["linkage"]:>10.2f} {result["avg_all"]["linkage"]:>10.2f} {lg_diff:>+8.2f}')
        
        # 折扣率
        dc_diff = result["avg_top3"]["disc_rate"]-result["avg_all"]["disc_rate"]
        print(f'  {"折扣率":<20} {result["avg_top3"]["disc_rate"]:>9.1f}折 {result["avg_all"]["disc_rate"]:>9.1f}折 {dc_diff:>+8.1f}')
        
        print(f'\n[单款销售深度: TOP3]')
        for g in result['top3']:
            print(f'  {g["guide_name"]}:')
            print(f'    - SKU数:{g["sku_count"]}, Top1销量占比:{g["top1_qty_rate"]}%, Top3:{g["top3_qty_rate"]}%, Top10:{g["top10_qty_rate"]}%')
            print(f'    - TOP10关联订单:{g["top10_order_cnt"]}笔, 销售占比:{g["top10_order_rate"]}%, 订单均价:{g["top10_order_avg"]:,.0f}元')
    
    # 保存结果
    with open(str(Path(__file__).resolve().parent / '_guide_core_result.json'), 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f'\n\n[结果已保存: _guide_core_result.json]')

if __name__ == '__main__':
    main()
