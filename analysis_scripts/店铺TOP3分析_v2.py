"""
店铺TOP3推销能力分析 v2
目标：分析各店铺TOP3导购的推销能力（不是TOP3 vs 非TOP3）
指标：含TOP10订单GMV占比、高价值占比
"""
import os
from pathlib import Path

import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

DB_PATH = os.environ.get("CABBEEN_DB") or str(Path(__file__).resolve().parents[1] / "cabbeen.db")

# 时间段定义
TIME_PERIODS = {
    '7天': 7,
    '15天': 15,
    '30天': 30,
    '45天': 45,
    '60天': 60,
    '90天': 90,
    '180天': 180,
    '全年': 365,
}


def get_shop_guide_stats(shop_name, start_date, end_date):
    """获取店铺内各导购的推销能力指标"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取店铺GMV
    cursor.execute("""
        SELECT SUM(amount) FROM sales s
        JOIN shops sh ON s.shop_name = sh.short_name
        WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
    """, (shop_name, start_date, end_date))
    total_gmv = cursor.fetchone()[0] or 0
    
    if total_gmv == 0:
        conn.close()
        return None
    
    # 获取该店铺TOP3导购
    cursor.execute("""
        SELECT guide_name, SUM(amount) as gmv
        FROM sales s
        JOIN shops sh ON s.shop_name = sh.short_name
        WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
        GROUP BY guide_name
        ORDER BY gmv DESC
        LIMIT 3
    """, (shop_name, start_date, end_date))
    top3_list = [row[0] for row in cursor.fetchall()]
    
    # 获取店铺TOP10款
    cursor.execute("""
        SELECT style_color FROM (
            SELECT style_color, SUM(amount) as gmv
            FROM sales s
            JOIN shops sh ON s.shop_name = sh.short_name
            WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
            GROUP BY style_color
            ORDER BY gmv DESC
            LIMIT 10
        )
    """, (shop_name, start_date, end_date))
    top10_styles = [row[0] for row in cursor.fetchall()]
    
    if not top10_styles:
        conn.close()
        return {'shop': shop_name, 'guide_count': len(top3_list), 'top3_list': top3_list, 'top10_rate': 0}
    
    # 计算店铺含TOP10订单GMV占比
    placeholders10 = ','.join(['?'] * len(top10_styles))
    cursor.execute(f"""
        SELECT SUM(amount) FROM sales s
        JOIN shops sh ON s.shop_name = sh.short_name
        WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
          AND style_color IN ({placeholders10})
    """, (shop_name, start_date, end_date) + tuple(top10_styles))
    top10_gmv = cursor.fetchone()[0] or 0
    top10_rate = top10_gmv / total_gmv * 100 if total_gmv > 0 else 0
    
    # 计算TOP3的含TOP10订单GMV
    placeholders3 = ','.join(['?'] * len(top3_list)) if top3_list else 'NULL'
    if top3_list:
        cursor.execute(f"""
            SELECT SUM(amount) FROM sales s
            JOIN shops sh ON s.shop_name = sh.short_name
            WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
              AND guide_name IN ({placeholders3})
              AND style_color IN ({placeholders10})
        """, (shop_name, start_date, end_date) + tuple(top3_list) + tuple(top10_styles))
        top3_top10_gmv = cursor.fetchone()[0] or 0
    else:
        top3_top10_gmv = 0
    
    # 计算高价值商品占比（正价商品，折扣率=amount/tag_price > 0.85）
    cursor.execute("""
        SELECT SUM(CASE WHEN tag_price > 0 AND amount/tag_price > 0.85 THEN amount ELSE 0 END),
               SUM(amount)
        FROM sales s
        JOIN shops sh ON s.shop_name = sh.short_name
        WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
    """, (shop_name, start_date, end_date))
    hv_amount, total_amount = cursor.fetchone()
    hv_rate = hv_amount / total_amount * 100 if total_amount and total_amount > 0 else 0
    
    # TOP3高价值占比
    if top3_list:
        cursor.execute(f"""
            SELECT SUM(CASE WHEN tag_price > 0 AND amount/tag_price > 0.85 THEN amount ELSE 0 END),
                   SUM(amount)
            FROM sales s
            JOIN shops sh ON s.shop_name = sh.short_name
            WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
              AND guide_name IN ({placeholders3})
        """, (shop_name, start_date, end_date) + tuple(top3_list))
        hv_row = cursor.fetchone()
        top3_hv_rate = hv_row[0] / hv_row[1] * 100 if hv_row[1] and hv_row[1] > 0 else 0
    else:
        top3_hv_rate = 0
    
    conn.close()
    
    return {
        'shop': shop_name,
        'guide_count': len(top3_list),
        'top3_list': top3_list,
        'total_gmv': total_gmv,
        'top10_rate': top10_rate,  # 店铺整体含TOP10订单GMV占比
        'top3_top10_gmv': top3_top10_gmv,
        'hv_rate': hv_rate,  # 店铺整体高价值占比
        'top3_hv_rate': top3_hv_rate,  # TOP3高价值占比
    }


def get_all_shops():
    """获取所有店铺"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT short_name FROM shops ORDER BY short_name")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


def get_db_date_range():
    """获取数据库实际日期范围"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(sale_date), MAX(sale_date) FROM sales")
    row = cursor.fetchone()
    conn.close()
    return row[0], row[1]


def main():
    db_min, db_max = get_db_date_range()
    print("数据库日期范围: {} ~ {}".format(db_min, db_max))
    
    today = db_max
    shops = get_all_shops()
    
    print("\n" + "=" * 80)
    print("店铺TOP3推销能力分析")
    print("截止日期: {}".format(today))
    print("=" * 80)
    
    all_results = []
    
    for period_name, days in TIME_PERIODS.items():
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        print("\n" + "=" * 80)
        print("时间段: {} ({} ~ {})".format(period_name, start_date, today))
        print("=" * 80)
        
        period_results = []
        
        for shop in shops:
            result = get_shop_guide_stats(shop, start_date, today)
            if result and result['guide_count'] > 0:
                period_results.append(result)
                all_results.append(result)
        
        if not period_results:
            print("  无数据")
            continue
        
        # 打印结果
        print("\n{:<10} {:<4} {:<18} {:>10} {:>10} {:>10} {:>10}".format(
            "店铺", "导购", "TOP3人员", "总GMV", "TOP10占比", "高价值", "TOP3高价值"))
        print("-" * 95)
        
        for r in period_results:
            top3_str = '/'.join(r['top3_list'][:3]) if r['top3_list'] else '-'
            if len(top3_str) > 16:
                top3_str = top3_str[:16] + '..'
            gmv_str = "{:,.0f}".format(r['total_gmv'])
            print("{:<10} {:<4} {:<18} {:>10} {:>9.1f}% {:>9.1f}% {:>9.1f}%".format(
                r['shop'], r['guide_count'], top3_str, gmv_str,
                r['top10_rate'], r['hv_rate'], r['top3_hv_rate']))
        
        # 汇总
        avg_top10 = sum(r['top10_rate'] for r in period_results) / len(period_results)
        avg_hv = sum(r['hv_rate'] for r in period_results) / len(period_results)
        avg_top3_hv = sum(r['top3_hv_rate'] for r in period_results) / len(period_results)
        
        print("\n汇总: 平均TOP10占比{:.1f}% | 平均高价值{:.1f}% | 平均TOP3高价值{:.1f}%".format(
            avg_top10, avg_hv, avg_top3_hv))
    
    # 各店铺指标稳定性
    print("\n" + "=" * 80)
    print("各店铺TOP10推销能力稳定性")
    print("=" * 80)
    
    shop_top10_rates = defaultdict(list)
    for r in all_results:
        shop_top10_rates[r['shop']].append(r['top10_rate'])
    
    for shop, rates in sorted(shop_top10_rates.items()):
        avg = sum(rates) / len(rates)
        std = (sum((x - avg) ** 2 for x in rates) / len(rates)) ** 0.5
        print("  {}: 平均{:.1f}% 标准差{:.1f}".format(shop, avg, std))


if __name__ == '__main__':
    main()
