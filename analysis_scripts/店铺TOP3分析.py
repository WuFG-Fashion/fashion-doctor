"""
店铺维度TOP3导购推销能力分析 v2
以店铺为单位，分析各时间段的TOP3 vs 非TOP3表现
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

# 阈值配置（pp）
THRESHOLDS = {
    7: 15,
    15: 10,
    30: 5,
    45: 5,
    60: 5,
    90: 5,
    180: 5,
    365: 5,
}


def get_top3_by_shop(shop_name, start_date, end_date):
    """获取指定店铺的TOP3导购"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # sales.shop_name = shops.short_name（简称）
    sql = """
    SELECT s.guide_name, SUM(s.amount) as total_gmv
    FROM sales s
    JOIN shops sh ON s.shop_name = sh.short_name
    WHERE sh.short_name = ?
      AND s.sale_date >= ? AND s.sale_date <= ?
    GROUP BY s.guide_name
    HAVING total_gmv > 0
    ORDER BY total_gmv DESC
    LIMIT 3
    """
    
    cursor.execute(sql, (shop_name, start_date, end_date))
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


def analyze_shop(shop_name, start_date, end_date, days):
    """分析单个店铺"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    threshold = THRESHOLDS.get(days, 5)
    
    # 获取该店铺的TOP3
    top3_list = get_top3_by_shop(shop_name, start_date, end_date)
    
    if not top3_list:
        return None
    
    # 店铺GMV
    cursor.execute("""
        SELECT SUM(amount) FROM sales s
        JOIN shops sh ON s.shop_name = sh.short_name
        WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
    """, (shop_name, start_date, end_date))
    total_gmv = cursor.fetchone()[0] or 0
    
    # TOP3 GMV
    placeholders = ','.join(['?'] * len(top3_list))
    cursor.execute(f"""
        SELECT SUM(amount) FROM sales s
        JOIN shops sh ON s.shop_name = sh.short_name
        WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
          AND s.guide_name IN ({placeholders})
    """, (shop_name, start_date, end_date) + tuple(top3_list))
    top3_gmv = cursor.fetchone()[0] or 0
    
    non_top3_gmv = total_gmv - top3_gmv
    top3_rate = top3_gmv / total_gmv * 100 if total_gmv > 0 else 0
    non_top3_rate = 100 - top3_rate
    gap = top3_rate - non_top3_rate
    
    # 含TOP10订单GMV占比
    # 先获取该店铺TOP10款
    cursor.execute("""
        SELECT style_color, SUM(amount) as gmv
        FROM sales s
        JOIN shops sh ON s.shop_name = sh.short_name
        WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
        GROUP BY style_color
        ORDER BY gmv DESC LIMIT 10
    """, (shop_name, start_date, end_date))
    top10_styles = [row[0] for row in cursor.fetchall()]
    
    if top10_styles:
        placeholders10 = ','.join(['?'] * len(top10_styles))
        # 含TOP10订单GMV（TOP3）
        cursor.execute(f"""
            SELECT SUM(s.amount) FROM sales s
            JOIN shops sh ON s.shop_name = sh.short_name
            WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
              AND s.guide_name IN ({placeholders})
              AND s.style_color IN ({placeholders10})
        """, (shop_name, start_date, end_date) + tuple(top3_list) + tuple(top10_styles))
        top3_top10_gmv = cursor.fetchone()[0] or 0
        
        # 含TOP10订单GMV（非TOP3）
        cursor.execute(f"""
            SELECT SUM(s.amount) FROM sales s
            JOIN shops sh ON s.shop_name = sh.short_name
            WHERE sh.short_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
              AND s.guide_name NOT IN ({placeholders})
              AND s.style_color IN ({placeholders10})
        """, (shop_name, start_date, end_date) + tuple(top3_list) + tuple(top10_styles))
        non_top3_top10_gmv = cursor.fetchone()[0] or 0
        
        total_top10_gmv = top3_top10_gmv + non_top3_top10_gmv
        top3_top10_rate = top3_top10_gmv / total_top10_gmv * 100 if total_top10_gmv > 0 else 0
        non_top3_top10_rate = 100 - top3_top10_rate
        gap_top10 = top3_top10_rate - non_top3_top10_rate
    else:
        top3_top10_rate = 0
        non_top3_top10_rate = 0
        gap_top10 = 0
    
    conn.close()
    
    return {
        'shop': shop_name,
        'days': days,
        'top3_list': top3_list,
        'top3_gmv': top3_gmv,
        'non_top3_gmv': non_top3_gmv,
        'top3_rate': top3_rate,
        'non_top3_rate': non_top3_rate,
        'gap': gap,
        'threshold': threshold,
        'leading': 'TOP3' if gap > threshold else ('非TOP3' if gap < -threshold else '持平'),
        'top3_top10_rate': top3_top10_rate,
        'non_top3_top10_rate': non_top3_top10_rate,
        'gap_top10': gap_top10,
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
    
    today = db_max  # 使用数据库最新日期
    shops = get_all_shops()
    shops = get_all_shops()
    
    print("=" * 80)
    print("店铺维度TOP3导购推销能力分析")
    print("截止日期: {}".format(today))
    print("店铺数量: {}".format(len(shops)))
    print("=" * 80)
    
    all_results = []
    
    for period_name, days in TIME_PERIODS.items():
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        print("\n" + "=" * 80)
        print("时间段: {} ({} ~ {})".format(period_name, start_date, today))
        print("=" * 80)
        
        period_results = []
        
        for shop in shops:
            result = analyze_shop(shop, start_date, today, days)
            if result:
                period_results.append(result)
                all_results.append(result)
        
        if not period_results:
            print("  无数据")
            continue
        
        # 打印各店铺结果
        print("\n{:<10} {:<18} {:>8} {:>8} {:>8} {:<6}".format(
            "店铺", "TOP3人员", "TOP3占比", "非TOP3", "差距", "结论"))
        print("-" * 65)
        
        for r in period_results:
            top3_str = '/'.join(r['top3_list'][:3]) if r['top3_list'] else '-'
            if len(top3_str) > 16:
                top3_str = top3_str[:16] + '..'
            print("{:<10} {:<18} {:>7.1f}% {:>7.1f}% {:>+6.1f}pp {:<6}".format(
                r['shop'], top3_str, r['top3_rate'], r['non_top3_rate'], r['gap'], r['leading']))
        
        # 汇总
        top3_wins = sum(1 for r in period_results if r['leading'] == 'TOP3')
        non_wins = sum(1 for r in period_results if r['leading'] == '非TOP3')
        flat = len(period_results) - top3_wins - non_wins
        
        print("\n汇总: TOP3领先{}店 | 非TOP3领先{}店 | 持平{}店".format(
            top3_wins, non_wins, flat))
    
    # 打印各店铺稳定表现
    print("\n" + "=" * 80)
    print("各店铺TOP3领先次数统计")
    print("=" * 80)
    
    shop_top3_wins = defaultdict(int)
    for r in all_results:
        if r['leading'] == 'TOP3':
            shop_top3_wins[r['shop']] += 1
    
    for shop, wins in sorted(shop_top3_wins.items(), key=lambda x: -x[1]):
        stars = '*' * wins
        print("  {}: {}/8次 {}".format(shop, wins, stars))


if __name__ == '__main__':
    main()
