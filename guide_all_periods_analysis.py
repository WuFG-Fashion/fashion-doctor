#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
明星导购能力拆解 - 全时间范围测试
分析维度：近7天、近15天、近30天、近45天、近60天、2026年全年
"""
import os
from pathlib import Path

import sys
sys.stdout.reconfigure(encoding='utf-8')

import sqlite3
import json
from datetime import datetime, timedelta

DB_PATH = os.environ.get("CABBEEN_DB") or str(Path(__file__).resolve().parents[1] / "cabbeen.db")
TODAY = datetime(2026, 4, 22)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def analyze_period(start_date, end_date, period_name):
    """分析指定时间段的导购能力"""
    conn = get_db()
    cur = conn.cursor()

    sql = """
    SELECT
        s.guide_name,
        SUM(s.amount) as gmv,
        SUM(s.qty) as qty,
        COUNT(DISTINCT s.order_no) as orders,
        COUNT(DISTINCT s.member_id) as members,
        COUNT(DISTINCT s.category) as cats,
        -- 连带率 = 总件数 / 总订单数
        CAST(SUM(s.qty) AS FLOAT) / COUNT(DISTINCT s.order_no) as linkage,
        -- 客单价 = 总金额 / 总订单数
        SUM(s.amount) / COUNT(DISTINCT s.order_no) as avg_price,
        -- 折扣率
        SUM(s.amount * 10.0 / NULLIF(s.tag_amount, 0)) / COUNT(DISTINCT s.order_no) as avg_disc,
        -- VIP订单
        SUM(CASE WHEN s.is_vip = 1 OR s.member_type = 'VIP' THEN 1 ELSE 0 END) as vip_orders,
        -- VIP订单占比
        CAST(SUM(CASE WHEN s.is_vip = 1 OR s.member_type = 'VIP' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT s.order_no) * 100 as vip_rate,
        -- VIP GMV
        SUM(CASE WHEN s.is_vip = 1 OR s.member_type = 'VIP' THEN s.amount ELSE 0 END) as vip_gmv,
        -- VIP GMV占比
        SUM(CASE WHEN s.is_vip = 1 OR s.member_type = 'VIP' THEN s.amount ELSE 0 END) * 100.0 / SUM(s.amount) as vip_gmv_rate,
        -- SKU数（用style_code）
        COUNT(DISTINCT s.style_code) as sku_count,
        -- SKU分散度 = SKU数 / 订单数
        CAST(COUNT(DISTINCT s.style_code) AS FLOAT) / COUNT(DISTINCT s.order_no) as sku_disp,
        -- 高价商品（吊牌>800）
        SUM(CASE WHEN s.tag_price > 800 THEN s.amount ELSE 0 END) as high_gmv,
        SUM(CASE WHEN s.tag_price > 800 THEN s.amount ELSE 0 END) * 100.0 / SUM(s.amount) as high_price_rate,
        -- 非VIP订单
        SUM(CASE WHEN s.is_vip != 1 AND s.member_type != 'VIP' THEN 1 ELSE 0 END) as non_vip_orders,
        -- 非VIP订单占比
        CAST(SUM(CASE WHEN s.is_vip != 1 AND s.member_type != 'VIP' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT s.order_no) * 100 as non_vip_rate,
        -- 非VIP客单价
        CASE
            WHEN SUM(CASE WHEN s.is_vip != 1 AND s.member_type != 'VIP' THEN 1 ELSE 0 END) > 0
            THEN SUM(CASE WHEN s.is_vip != 1 AND s.member_type != 'VIP' THEN s.amount ELSE 0 END) /
                 SUM(CASE WHEN s.is_vip != 1 AND s.member_type != 'VIP' THEN 1 ELSE 0 END)
            ELSE 0
        END as non_vip_avg_price,
        -- VIP客单价
        SUM(CASE WHEN s.is_vip = 1 OR s.member_type = 'VIP' THEN s.amount ELSE 0 END) /
        NULLIF(SUM(CASE WHEN s.is_vip = 1 OR s.member_type = 'VIP' THEN 1 ELSE 0 END), 0) as vip_avg_price
    FROM sales s
    WHERE s.sale_date BETWEEN ? AND ?
    GROUP BY s.guide_name
    HAVING SUM(s.amount) > 0
    ORDER BY gmv DESC
    """

    cur.execute(sql, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    rows = cur.fetchall()

    if not rows:
        print(f"\n{'='*60}")
        print(f"📅 {period_name} ({start_date.date()} ~ {end_date.date()})")
        print(f"❌ 无数据")
        print(f"{'='*60}")
        return None

    # 转换为字典
    data = []
    for r in rows:
        row = dict(r)
        # 计算爆款依赖度 = Top1 SKU销量 / 总销量（简化：用1 - SKU分散度/平均SKU分散度）
        # 实际爆款依赖度需要更复杂的查询，这里用 SKU分散度的倒数来近似
        row['top1_sku_rate'] = 0  # 暂时设为0，后续单独计算
        data.append(row)

    # 计算复购率（需要单独查询）
    for row in data:
        guide = row['guide_name']
        cur.execute("""
            SELECT COUNT(*) as total_members,
                   SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) as rep_members
            FROM (
                SELECT s.member_id,
                       COUNT(DISTINCT s.order_no) as order_count
                FROM sales s
                WHERE s.sale_date BETWEEN ? AND ?
                  AND s.guide_name = ?
                GROUP BY s.member_id
            )
        """, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), guide))
        rep = cur.fetchone()
        row['rep_mem'] = rep['rep_members'] if rep else 0
        row['repurchase_rate'] = (rep['rep_members'] / rep['total_members'] * 100) if rep and rep['total_members'] > 0 else 0

        # 新VIP数（近30天注册的）
        cur.execute("""
            SELECT COUNT(DISTINCT member_id) as new_vip
            FROM sales
            WHERE guide_name = ?
              AND sale_date BETWEEN ? AND ?
        """, (guide, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        new_vip = cur.fetchone()
        row['new_vip'] = new_vip['new_vip'] if new_vip else 0
        row['new_vip_rate'] = (row['new_vip'] / row['members'] * 100) if row['members'] > 0 else 0

        # VIP多件率（VIP订单中买了多件的占比）
        cur.execute("""
            SELECT COUNT(*) as total_vip_orders,
                   SUM(CASE WHEN total_qty > 1 THEN 1 ELSE 0 END) as multi_orders
            FROM (
                SELECT order_no,
                       SUM(qty) as total_qty
                FROM sales
                WHERE guide_name = ?
                  AND sale_date BETWEEN ? AND ?
                  AND (is_vip = 1 OR member_type = 'VIP')
                GROUP BY order_no
            )
        """, (guide, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        vip_multi = cur.fetchone()
        row['vip_multi'] = vip_multi['multi_orders'] if vip_multi else 0
        row['vip_multi_rate'] = (vip_multi['multi_orders'] / vip_multi['total_vip_orders'] * 100) if vip_multi and vip_multi['total_vip_orders'] > 0 else 0

        # 爆款依赖度 = Top1 SKU销量 / 总销量
        cur.execute("""
            SELECT SUM(qty) as total_qty
            FROM sales
            WHERE guide_name = ?
              AND sale_date BETWEEN ? AND ?
        """, (guide, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        total_qty = cur.fetchone()['total_qty'] or 1

        cur.execute("""
            SELECT SUM(qty) as top1_qty
            FROM (
                SELECT style_code, SUM(qty) as qty
                FROM sales
                WHERE guide_name = ?
                  AND sale_date BETWEEN ? AND ?
                GROUP BY style_code
                ORDER BY qty DESC
                LIMIT 1
            )
        """, (guide, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        top1_qty = cur.fetchone()['top1_qty'] or 0
        row['top1_sku_rate'] = (top1_qty / total_qty * 100) if total_qty > 0 else 0

    conn.close()

    return data

def print_summary(data, period_name, start_date, end_date):
    """打印分析结果"""
    if not data:
        return

    print(f"\n{'='*60}")
    print(f"📅 {period_name} ({start_date.date()} ~ {end_date.date()})")
    print(f"{'='*60}")

    # 基础统计
    total_gmv = sum(r['gmv'] for r in data)
    total_orders = sum(r['orders'] for r in data)
    total_members = sum(r['members'] for r in data)

    print(f"\n📊 基础数据:")
    print(f"  - 导购数: {len(data)}人")
    print(f"  - 总GMV: {total_gmv:,.0f}元")
    print(f"  - 总订单: {total_orders}笔")
    print(f"  - 总会员: {total_members}人")

    # TOP3
    top3 = data[:3]
    print(f"\n🏆 TOP3 GMV:")
    for i, r in enumerate(top3):
        print(f"  {i+1}. {r['guide_name']}: {r['gmv']:,.0f}元 ({r['orders']}单)")

    # 计算全员平均
    avg_vip_rate = sum(r['vip_rate'] for r in data) / len(data)
    avg_rep_rate = sum(r['repurchase_rate'] for r in data) / len(data)
    avg_sku = sum(r['sku_count'] for r in data) / len(data)
    avg_top1_rate = sum(r['top1_sku_rate'] for r in data) / len(data)
    avg_high_rate = sum(r['high_price_rate'] for r in data) / len(data)

    # TOP3平均
    top3_vip_rate = sum(r['vip_rate'] for r in top3) / 3
    top3_rep_rate = sum(r['repurchase_rate'] for r in top3) / 3
    top3_sku = sum(r['sku_count'] for r in top3) / 3
    top3_top1_rate = sum(r['top1_sku_rate'] for r in top3) / 3
    top3_high_rate = sum(r['high_price_rate'] for r in top3) / 3

    print(f"\n📈 隐藏能力对比 (TOP3 vs 全员):")
    print(f"  {'指标':<15} {'TOP3':>10} {'全员':>10} {'差距':>10}")
    print(f"  {'-'*45}")
    print(f"  {'VIP订单率':<15} {top3_vip_rate:>9.1f}% {avg_vip_rate:>9.1f}% {top3_vip_rate - avg_vip_rate:>+9.1f}pp")
    print(f"  {'复购率':<15} {top3_rep_rate:>9.1f}% {avg_rep_rate:>9.1f}% {top3_rep_rate - avg_rep_rate:>+9.1f}pp")
    print(f"  {'SKU数':<15} {top3_sku:>10.0f} {avg_sku:>10.0f} {(top3_sku/avg_sku-1)*100:>+9.0f}%")
    print(f"  {'爆款依赖度':<15} {top3_top1_rate:>9.1f}% {avg_top1_rate:>9.1f}% {top3_top1_rate-avg_top1_rate:>+9.1f}pp")
    print(f"  {'高价商品占比':<15} {top3_high_rate:>9.1f}% {avg_high_rate:>9.1f}% {top3_high_rate-avg_high_rate:>+9.1f}pp")

    # TOP3类型分析
    print(f"\n🎯 TOP3能力画像:")
    for r in top3:
        # 判断类型
        if r['sku_count'] > avg_sku * 1.5 and r['top1_sku_rate'] < avg_top1_rate:
            gtype = "推款型"
        elif r['avg_price'] > 1200:
            gtype = "高客单型"
        elif r['repurchase_rate'] > avg_rep_rate * 1.3:
            gtype = "毛利型"
        elif r['linkage'] > 2.5:
            gtype = "连带型"
        else:
            gtype = "均衡型"

        print(f"  {r['guide_name']}: {gtype}")
        print(f"    - 订单:{r['orders']} 客单:{r['avg_price']:.0f}元 连带:{r['linkage']:.2f}件")
        print(f"    - SKU:{r['sku_count']}个 爆款依赖:{r['top1_sku_rate']:.1f}% 复购:{r['repurchase_rate']:.1f}%")

    return {
        'period': period_name,
        'start': start_date.strftime('%Y-%m-%d'),
        'end': end_date.strftime('%Y-%m-%d'),
        'total_gmv': total_gmv,
        'total_orders': total_orders,
        'total_guides': len(data),
        'top3_vip_rate': top3_vip_rate,
        'avg_vip_rate': avg_vip_rate,
        'top3_rep_rate': top3_rep_rate,
        'avg_rep_rate': avg_rep_rate,
        'top3_sku': top3_sku,
        'avg_sku': avg_sku,
        'top3_top1_rate': top3_top1_rate,
        'avg_top1_rate': avg_top1_rate,
        'top3_high_rate': top3_high_rate,
        'avg_high_rate': avg_high_rate,
    }

def main():
    print("\n" + "="*60)
    print("🚀 明星导购能力拆解 - 全时间范围测试")
    print("="*60)

    results = []

    # 定义时间范围
    periods = [
        (TODAY - timedelta(days=6), TODAY, "近7天"),
        (TODAY - timedelta(days=14), TODAY, "近15天"),
        (TODAY - timedelta(days=29), TODAY, "近30天"),
        (TODAY - timedelta(days=44), TODAY, "近45天"),
        (TODAY - timedelta(days=59), TODAY, "近60天"),
        (datetime(2026, 1, 1), TODAY, "2026年全年"),
    ]

    for start_date, end_date, period_name in periods:
        data = analyze_period(start_date, end_date, period_name)
        if data:
            result = print_summary(data, period_name, start_date, end_date)
            if result:
                results.append(result)

    # 汇总对比
    print("\n\n" + "="*60)
    print("📊 全时间范围汇总对比")
    print("="*60)
    print(f"\n{'时间段':<12} {'GMV':>10} {'订单':>6} {'导购':>4} {'VIP率':>8} {'复购率':>8} {'SKU':>6} {'爆款':>8}")
    print("-"*70)
    for r in results:
        print(f"{r['period']:<12} {r['total_gmv']:>10,.0f} {r['total_orders']:>6} {r['total_guides']:>4} "
              f"{r['top3_vip_rate']:>7.1f}% {r['top3_rep_rate']:>7.1f}% {r['top3_sku']:>6.0f} {r['top3_top1_rate']:>7.1f}%")

    # 能力差距稳定性分析
    print("\n\n📈 TOP3 vs 全员 差距稳定性分析:")
    print(f"{'时间段':<12} {'VIP率差':>8} {'复购率差':>9} {'SKU差%':>8} {'爆款差':>8}")
    print("-"*50)
    for r in results:
        vip_diff = r['top3_vip_rate'] - r['avg_vip_rate']
        rep_diff = r['top3_rep_rate'] - r['avg_rep_rate']
        sku_diff = (r['top3_sku']/r['avg_sku'] - 1) * 100 if r['avg_sku'] > 0 else 0
        top1_diff = r['top3_top1_rate'] - r['avg_top1_rate']
        print(f"{r['period']:<12} {vip_diff:>+7.1f}pp {rep_diff:>+8.1f}pp {sku_diff:>+7.0f}% {top1_diff:>+7.1f}pp")

    # 保存结果
    output_path = str(Path(__file__).resolve().parent / "_guide_all_periods_result.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {output_path}")

if __name__ == '__main__':
    main()
