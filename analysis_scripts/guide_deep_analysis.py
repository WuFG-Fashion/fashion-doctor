# -*- coding: utf-8 -*-
"""
明星导购深度能力拆解分析
=====================
分析维度：排名页面看不到的隐藏能力

核心逻辑：
- 不分析表面KPI（单数/客单件/客单价），那是结果不是原因
- 分析"为什么会高"的深层原因
"""

import sqlite3
import pandas as pd
from collections import defaultdict
from datetime import datetime

DB_PATH = 'C:/Users/MacBookPro/cabbeen_data/cabbeen.db'

def load_data():
    """加载销售数据"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('''
        SELECT order_no, guide_name, shop_name, category, sub_category,
               minor_category, qty, amount, tag_price, tag_amount,
               member_id, member_level, is_vip, sale_date, barcode,
               style_code, size_code, year, season
        FROM sales
        WHERE guide_name IS NOT NULL AND guide_name != ''
    ''', conn)
    conn.close()

    # 基础处理
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['month'] = df['sale_date'].dt.month
    df['real_discount'] = (df['amount'] / df['tag_amount'] * 10).clip(0, 10).round(1)
    df['price_tier'] = pd.cut(df['tag_price'], bins=[0, 299, 499, 799, 999, float('inf')],
                              labels=['<300', '300-500', '500-800', '800-1000', '>1000'])

    return df


def calc_guide_metrics(df):
    """计算每个导购的深度指标"""
    results = []

    for guide, gdf in df.groupby('guide_name'):
        if len(gdf) < 20:  # 样本太少跳过
            continue

        total_qty = gdf['qty'].sum()
        total_amount = gdf['amount'].sum()
        total_orders = gdf['order_no'].nunique()

        # === 基础指标（参考用，不做排名依据）===
        basic = {
            'guide_name': guide,
            'gmv': total_amount,
            'total_orders': total_orders,
            'avg_order_qty': total_qty / total_orders,
            'avg_order_amount': total_amount / total_orders,
        }

        # === 1. 品类宽度分析 ===
        category_count = gdf['category'].nunique()
        sub_category_count = gdf['sub_category'].nunique()
        minor_category_count = gdf['minor_category'].nunique()
        sku_count = gdf['barcode'].nunique()

        # 品类集中度（Top3品类占比，越低越均衡）
        cat_ratio = gdf.groupby('category')['amount'].sum().nlargest(3).sum() / total_amount

        metrics = {
            **basic,
            # 品类宽度
            'category_count': category_count,
            'sub_category_count': sub_category_count,
            'minor_category_count': minor_category_count,
            'sku_count': sku_count,
            'category_balance': round(cat_ratio * 100, 1),  # Top3品类占比（越低越均衡）
        }

        # === 2. 商品深度分析 ===
        # SKU分散度：有效SKU数 / 总件数，越高说明推款越广
        sku_per_qty = sku_count / total_qty if total_qty > 0 else 0

        # 爆款依赖度：单款最高销量占比，越低说明不依赖爆款
        sku_qty_dist = gdf.groupby('barcode')['qty'].sum()
        max_sku_ratio = sku_qty_dist.max() / total_qty if total_qty > 0 else 0

        # 件单价分布
        unit_price_dist = gdf.groupby('barcode')['tag_price'].first()
        high_price_ratio = (unit_price_dist > 800).sum() / sku_count if sku_count > 0 else 0

        metrics.update({
            'sku_per_qty': round(sku_per_qty, 3),  # SKU分散度
            'top_sku_dependency': round(max_sku_ratio * 100, 1),  # 爆款依赖度%
        })

        # === 3. 价格带分析 ===
        price_dist = gdf.groupby('price_tier')['amount'].sum() / total_amount * 100
        price_metrics = price_dist.to_dict() if isinstance(price_dist, pd.Series) else {}

        # 正价商品占比（折扣>9折视为接近正价）
        full_price_ratio = (gdf['real_discount'] >= 9.0).sum() / len(gdf) * 100

        # 高价商品占比（吊牌>800）
        high_price_amount_ratio = (gdf[gdf['tag_price'] > 800]['amount'].sum() / total_amount * 100) if total_amount > 0 else 0

        metrics.update({
            'full_price_ratio': round(full_price_ratio, 1),  # 正价销售占比
            'high_price_amount_ratio': round(high_price_amount_ratio, 1),  # 高价商品金额占比
            'avg_discount': round(gdf['real_discount'].mean(), 2),
        })

        # === 4. 会员质量分析 ===
        vip_orders = gdf[gdf['is_vip'] == 1]['order_no'].nunique()
        vip_ratio = vip_orders / total_orders * 100

        # 新会员占比（会员等级为新客/普通）
        new_member_ratio = gdf[gdf['member_level'].isin(['新客', '普通', None]) & (gdf['is_vip'] == 1)]['member_id'].nunique()
        total_members = gdf[gdf['is_vip'] == 1]['member_id'].nunique()
        new_vs_old_ratio = new_member_ratio / total_members * 100 if total_members > 0 else 0

        # 会员订单集中度（是否有少数会员贡献大量订单）
        member_order_dist = gdf[gdf['is_vip'] == 1].groupby('member_id')['order_no'].nunique()
        top_member_ratio = member_order_dist.nlargest(1).values[0] / total_orders * 100 if len(member_order_dist) > 0 else 0

        metrics.update({
            'vip_ratio': round(vip_ratio, 1),
            'new_vs_old_ratio': round(new_vs_old_ratio, 1),  # 新客/普通会员占比
            'member_concentration': round(top_member_ratio, 1),  # Top1会员订单集中度
        })

        # === 5. 跨品类连带分析 ===
        # 跨品类订单占比：同一订单有≥2个品类
        cross_cat_orders = gdf.groupby('order_no')['category'].nunique()
        cross_cat_ratio = (cross_cat_orders >= 2).sum() / total_orders * 100

        # 跨品类件数
        cross_cat_qty = gdf[gdf['order_no'].isin(cross_cat_orders[cross_cat_orders >= 2].index)]['qty'].sum()

        metrics.update({
            'cross_category_ratio': round(cross_cat_ratio, 1),  # 跨品类订单占比
        })

        # === 6. 销售稳定性分析 ===
        daily_sales = gdf.groupby(gdf['sale_date'].dt.date)['amount'].sum()
        if len(daily_sales) > 1:
            daily_cv = daily_sales.std() / daily_sales.mean() if daily_sales.mean() > 0 else 0
        else:
            daily_cv = 0

        # 月份集中度（是否有淡旺季）
        monthly_dist = gdf.groupby('month')['amount'].sum()
        top_month_ratio = monthly_dist.max() / total_amount * 100 if total_amount > 0 else 0

        metrics.update({
            'daily_sales_cv': round(daily_cv, 2),  # 日销售波动系数
            'top_month_concentration': round(top_month_ratio, 1),  # Top月份集中度
        })

        # === 7. 搭配合理性 ===
        # 多件订单占比
        multi_item_orders = gdf.groupby('order_no')['qty'].sum()
        multi_item_ratio = (multi_item_orders > 1).sum() / total_orders * 100

        # 多件订单中的跨品类比例
        multi_item_cross = cross_cat_orders[(cross_cat_orders >= 2) & (multi_item_orders > 1)]
        multi_item_cross_ratio = len(multi_item_cross) / (multi_item_orders > 1).sum() * 100 if (multi_item_orders > 1).sum() > 0 else 0

        metrics.update({
            'multi_item_ratio': round(multi_item_ratio, 1),  # 多件订单占比
            'multi_cross_ratio': round(multi_item_cross_ratio, 1),  # 多件订单中跨品类占比
        })

        results.append(metrics)

    return pd.DataFrame(results)


def analyze_star_guide(df, top3_names):
    """针对TOP3明星导购的深度分析"""
    analysis = {}

    for guide in top3_names:
        gdf = df[df['guide_name'] == guide]

        guide_report = {}

        # 1. 品类结构分析
        cat_sales = gdf.groupby('category')['amount'].sum().sort_values(ascending=False)
        cat_sales_pct = cat_sales / cat_sales.sum() * 100
        guide_report['top_categories'] = {k: f"{v:.1f}%" for k, v in cat_sales_pct.head(5).items()}

        # 2. 会员结构
        vip_dist = gdf[gdf['is_vip'] == 1]['member_level'].value_counts()
        guide_report['member_level_dist'] = vip_dist.to_dict() if len(vip_dist) > 0 else {}

        # 3. 价格带分布
        price_dist = gdf.groupby('price_tier')['amount'].sum() / gdf['amount'].sum() * 100
        guide_report['price_tier_dist'] = {str(k): f"{v:.1f}%" for k, v in price_dist.items()}

        # 4. 跨品类连带具体分析
        cross_cat_data = gdf.groupby('order_no').agg({
            'category': lambda x: list(x.unique()),
            'qty': 'sum',
            'amount': 'sum'
        })
        cross_cat_data['cat_count'] = cross_cat_data['category'].apply(len)
        multi_cat_orders = cross_cat_data[cross_cat_data['cat_count'] >= 2]

        if len(multi_cat_orders) > 0:
            guide_report['cross_cat_stats'] = {
                'cross_cat_order_count': len(multi_cat_orders),
                'cross_cat_avg_qty': multi_cat_orders['qty'].mean(),
                'cross_cat_avg_amount': multi_cat_orders['amount'].mean(),
                'typical_combos': [tuple(x) for x in multi_cat_orders['category'].head(5)]
            }

        # 5. SKU分布 - 爆款分析
        sku_sales = gdf.groupby('barcode')['qty'].sum().sort_values(ascending=False)
        guide_report['sku_depth'] = {
            'total_skus': len(sku_sales),
            'top10_qty_pct': sku_sales.head(10).sum() / sku_sales.sum() * 100,
            'top20_qty_pct': sku_sales.head(20).sum() / sku_sales.sum() * 100,
        }

        # 6. 关联搭配 - 最常见的品类组合
        if len(multi_cat_orders) > 0:
            combos = multi_cat_orders['category'].apply(
                lambda x: ' + '.join(sorted([str(c) for c in x if pd.notna(c)]))
            ).value_counts()
            guide_report['common_combos'] = combos.head(5).to_dict()

        # 7. 月份销售节奏
        monthly = gdf.groupby('month')['amount'].sum()
        guide_report['monthly_pattern'] = monthly.to_dict()

        analysis[guide] = guide_report

    return analysis


def compare_with_average(df, results_df):
    """对比TOP3与全员平均"""
    comparison = {}

    # 计算全员平均
    avg_all = {
        'category_count': results_df['category_count'].mean(),
        'sku_per_qty': results_df['sku_per_qty'].mean(),
        'top_sku_dependency': results_df['top_sku_dependency'].mean(),
        'full_price_ratio': results_df['full_price_ratio'].mean(),
        'high_price_amount_ratio': results_df['high_price_amount_ratio'].mean(),
        'cross_category_ratio': results_df['cross_category_ratio'].mean(),
        'multi_item_ratio': results_df['multi_item_ratio'].mean(),
        'multi_cross_ratio': results_df['multi_cross_ratio'].mean(),
        'daily_sales_cv': results_df['daily_sales_cv'].mean(),
    }

    comparison['all_avg'] = {k: round(v, 2) for k, v in avg_all.items()}

    # TOP3平均
    top3_data = results_df[results_df['guide_name'].isin(['李志婕', '吕红', '邓小莉'])]
    avg_top3 = {
        'category_count': top3_data['category_count'].mean(),
        'sku_per_qty': top3_data['sku_per_qty'].mean(),
        'top_sku_dependency': top3_data['top_sku_dependency'].mean(),
        'full_price_ratio': top3_data['full_price_ratio'].mean(),
        'high_price_amount_ratio': top3_data['high_price_amount_ratio'].mean(),
        'cross_category_ratio': top3_data['cross_category_ratio'].mean(),
        'multi_item_ratio': top3_data['multi_item_ratio'].mean(),
        'multi_cross_ratio': top3_data['multi_cross_ratio'].mean(),
        'daily_sales_cv': top3_data['daily_sales_cv'].mean(),
    }
    comparison['top3_avg'] = {k: round(v, 2) for k, v in avg_top3.items()}

    # 差距分析
    comparison['gap'] = {}
    for key in avg_all:
        gap = avg_top3[key] - avg_all[key]
        gap_pct = gap / avg_all[key] * 100 if avg_all[key] != 0 else 0
        comparison['gap'][key] = {
            'diff': round(gap, 2),
            'diff_pct': round(gap_pct, 1)
        }

    return comparison


def main():
    print("=" * 60)
    print("明星导购深度能力拆解分析")
    print("=" * 60)

    # 加载数据
    print("\n[1/4] 加载数据...")
    df = load_data()
    print(f"    销售记录: {len(df)} 条")
    print(f"    导购人数: {df['guide_name'].nunique()} 人")
    print(f"    订单数量: {df['order_no'].nunique()} 个")

    # 计算深度指标
    print("\n[2/4] 计算深度能力指标...")
    results_df = calc_guide_metrics(df)
    results_df = results_df.sort_values('gmv', ascending=False)

    # 找出TOP3
    top3_names = results_df.head(3)['guide_name'].tolist()
    print(f"    TOP3: {', '.join(top3_names)}")

    # 输出TOP3详细对比表
    print("\n" + "=" * 60)
    print("【深度能力对比表】")
    print("=" * 60)

    key_metrics = [
        ('category_count', '品类宽度', '个'),
        ('sub_category_count', '小类宽度', '个'),
        ('sku_count', 'SKU数量', '个'),
        ('sku_per_qty', 'SKU分散度', ''),
        ('top_sku_dependency', '爆款依赖', '%'),
        ('full_price_ratio', '正价占比', '%'),
        ('high_price_amount_ratio', '高价金额占比', '%'),
        ('avg_discount', '均件折扣', '折'),
        ('cross_category_ratio', '跨品类订单占比', '%'),
        ('multi_item_ratio', '多件订单占比', '%'),
        ('multi_cross_ratio', '多件跨品类率', '%'),
        ('vip_ratio', '会员订单率', '%'),
        ('daily_sales_cv', '日销售波动', ''),
    ]

    print(f"{'指标':<20} {'TOP1李志婕':<12} {'TOP2吕红':<12} {'TOP3邓小莉':<12} {'全员平均':<12} {'差距':<12}")
    print("-" * 80)

    top3_data = results_df[results_df['guide_name'].isin(['李志婕', '吕红', '邓小莉'])].set_index('guide_name')

    for metric_key, metric_name, unit in key_metrics:
        val1 = top3_data.loc['李志婕', metric_key] if '李志婕' in top3_data.index else '-'
        val2 = top3_data.loc['吕红', metric_key] if '吕红' in top3_data.index else '-'
        val3 = top3_data.loc['邓小莉', metric_key] if '邓小莉' in top3_data.index else '-'
        avg = results_df[metric_key].mean()

        # 格式化
        f1 = f"{val1:.1f}" if isinstance(val1, (int, float)) else str(val1)
        f2 = f"{val2:.1f}" if isinstance(val2, (int, float)) else str(val2)
        f3 = f"{val3:.1f}" if isinstance(val3, (int, float)) else str(val3)
        f_avg = f"{avg:.1f}"

        # 计算差距
        if isinstance(val1, (int, float)):
            gap = val1 - avg
            gap_str = f"+{gap:.1f}" if gap >= 0 else f"{gap:.1f}"
        else:
            gap_str = '-'

        print(f"{metric_name:<20} {f1:<12} {f2:<12} {f3:<12} {f_avg:<12} {gap_str:<12}")

    # 深度分析
    print("\n" + "=" * 60)
    print("【TOP3深度能力拆解】")
    print("=" * 60)

    analysis = analyze_star_guide(df, top3_names)

    for guide, report in analysis.items():
        print(f"\n▶ {guide}")
        print("-" * 40)

        # 品类结构
        if 'top_categories' in report:
            print("  【主销品类】")
            for cat, pct in report['top_categories'].items():
                print(f"    {cat}: {pct}")

        # 品类组合
        if 'common_combos' in report:
            print("\n  【常见搭配组合】")
            for combo, cnt in list(report['common_combos'].items())[:3]:
                print(f"    {combo}: {cnt}笔")

        # SKU分布
        if 'sku_depth' in report:
            sku = report['sku_depth']
            print(f"\n  【SKU分布】")
            print(f"    总SKU数: {sku['total_skus']}")
            print(f"    Top10销量占比: {sku['top10_qty_pct']:.1f}%")
            print(f"    Top20销量占比: {sku['top20_qty_pct']:.1f}%")
            if sku['top10_qty_pct'] < 50:
                print(f"    → 推款广泛，不依赖爆款")
            else:
                print(f"    → 存在爆款依赖")

        # 价格带
        if 'price_tier_dist' in report:
            print("\n  【价格带分布】")
            for tier, pct in report['price_tier_dist'].items():
                print(f"    {tier}: {pct}")

        # 会员结构
        if 'member_level_dist' in report:
            print("\n  【会员等级分布】")
            for level, cnt in report['member_level_dist'].items():
                print(f"    {level}: {cnt}人")

        # 月份节奏
        if 'monthly_pattern' in report:
            print("\n  【月份销售节奏】")
            months = sorted(report['monthly_pattern'].keys())
            print(f"    活跃月份: {', '.join(str(m) for m in months)}")

    # 差距分析
    print("\n" + "=" * 60)
    print("【TOP3 vs 全员：真正的差距】")
    print("=" * 60)

    comparison = compare_with_average(df, results_df)

    # 按差距大小排序
    gap_sorted = sorted(comparison['gap'].items(), key=lambda x: abs(x[1]['diff_pct']), reverse=True)

    print("\n差距最大的维度（排名页面看不到的能力差异）:")
    print("-" * 50)

    for key, gap_data in gap_sorted[:8]:
        metric_labels = {
            'category_count': '品类宽度',
            'sku_per_qty': 'SKU分散度',
            'top_sku_dependency': '爆款依赖度',
            'full_price_ratio': '正价销售占比',
            'high_price_amount_ratio': '高价商品占比',
            'cross_category_ratio': '跨品类连带率',
            'multi_item_ratio': '多件订单占比',
            'multi_cross_ratio': '多件跨品类率',
            'daily_sales_cv': '日销售波动',
        }

        label = metric_labels.get(key, key)
        diff_pct = gap_data['diff_pct']

        if abs(diff_pct) > 5:  # 差距超过5%才值得看
            direction = "↑" if diff_pct > 0 else "↓"
            status = "更强" if diff_pct > 0 else "更弱"
            print(f"  {label}: {direction} {abs(diff_pct):.1f}% {status}")

    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)

    return results_df, analysis, comparison


if __name__ == '__main__':
    main()
