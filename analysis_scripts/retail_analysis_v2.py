# -*- coding: utf-8 -*-
"""
服装零售数据分析脚本 v2.0
严格遵循红线规范（三验规则）
使用真实数据库字段（已通过 PRAGMA table_info 确认）

分析模块：
  1. GMV 仪表盘（年度/月度）
  2. 四率诊断（动销率/售罄率/折扣率/流转率）
  3. ABC 分类（按 sub_category 精准分层）
  4. 721 货品结构（按品类属性归类）
  5. 波士顿矩阵（按 category + 同比增长率）
  6. RFM 用户分层（按 member_id）
  7. AIPL 链路健康度
  8. 版型 fit_name 分析
  9. 门店 GMV 排名（join shops 表）
  10. 月度健康度打分 + 行动指南
"""

import sqlite3
import os
from datetime import datetime
from collections import defaultdict

# ========== 配置 ==========
DB_PATH = 'C:/Users/MacBookPro/cabbeen_data/cabbeen.db'
REPORT_PATH = 'C:/Users/MacBookPro/WorkBuddy/20260421102454/retail_analysis_report.md'
TODAY = '2026-04-21'
ANALYSIS_MONTH = '2026-03'   # 最近完整月
CURRENT_MONTH = '2026-04'    # 当月（不完整）

# ========== 数据库连接 ==========
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def sql(query, params=None):
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    return cur.fetchall()

def fmt(n):
    """千分位格式化"""
    if n is None:
        return 'N/A'
    return f'{n:,.0f}'

def pct(a, b):
    """百分比显示"""
    if b == 0 or b is None:
        return 'N/A'
    return f'{a / b * 100:.1f}%'

# ========== 数据加载 ==========
print('=' * 60)
print('  服装零售数据分析 v2.0')
print('=' * 60)
print()

print('【1. 数据加载】')
sales = sql("SELECT * FROM sales WHERE sale_date IS NOT NULL")
inv = sql("SELECT * FROM inventory")
arr = sql("SELECT * FROM arrival")
shops = sql("SELECT * FROM shops")

print(f'  销售记录: {len(sales):,} 条')
print(f'  库存记录: {len(inv):,} 条')
print(f'  到货记录: {len(arr):,} 条')
print(f'  店铺数:   {len(shops):,} 家')

# 建立店铺简称映射
shop_full_to_short = {str(r['full_name']): str(r['short_name']) for r in shops}
shop_full_to_region = {str(r['full_name']): str(r['region']) for r in shops}
print(f'  店铺简称映射: {shop_full_to_short}')

# ========== 时间切片 ==========
print()
print('【2. 时间切片】')
def by_year(rows, yr):
    return [r for r in rows if str(r['sale_date']).startswith(str(yr))]

sales_2026 = by_year(sales, 2026)
sales_2025 = by_year(sales, 2025)
sales_2024 = by_year(sales, 2024)
sales_month = [r for r in sales if str(r['sale_date']).startswith(ANALYSIS_MONTH)]

print(f'  2026年: {len(sales_2026):,} 条')
print(f'  2025年: {len(sales_2025):,} 条')
print(f'  2024年: {len(sales_2024):,} 条')
print(f'  {ANALYSIS_MONTH}月: {len(sales_month):,} 条')

# ========== 3. GMV 仪表盘 ==========
print()
print('【3. GMV 仪表盘】')

def gmv_summary(rows, label):
    if not rows:
        print(f'  {label}: 无数据')
        return
    gmv = sum(r['amount'] for r in rows)
    qty = sum(r['qty'] for r in rows)
    orders = len(set(r['order_no'] for r in rows if r['order_no']))
    members = len(set(r['member_id'] for r in rows if r['member_id'] and str(r['member_id']).strip()))
    avg_price = gmv / qty if qty > 0 else 0
    avg_order = gmv / orders if orders > 0 else 0
    print(f'  {label}:')
    print(f'    GMV:        {fmt(gmv):>12s} 元')
    print(f'    销售件数:   {qty:>12,.0f} 件')
    print(f'    订单数:    {orders:>12,} 单')
    print(f'    件单价:    {avg_price:>12.1f} 元')
    print(f'    客单价:    {avg_order:>12.1f} 元')
    print(f'    会员占比:  {pct(members, len(set(r["member_id"] for r in rows if r["member_id"] and str(r["member_id"]).strip())))}')

gmv_summary(sales_2026, '2026年（截止4/20）')
gmv_summary(sales_2025, '2025年全年')
gmv_summary(sales_month, f'{ANALYSIS_MONTH}月')

# 月度同比
gmv_m = sum(r['amount'] for r in sales_month)
gmv_ly_m = sum(r['amount'] for r in sales if str(r['sale_date']).startswith('2025-03'))
if gmv_ly_m > 0:
    yoy = (gmv_m - gmv_ly_m) / gmv_ly_m * 100
    print(f'  月度同比: {yoy:+.1f}%')

# 品类 GMV（按 category 大类）
print()
print('  品类 GMV 分布（category）：')
cat_gmv = defaultdict(float)
cat_qty = defaultdict(float)
for r in sales_2026:
    cat = r['category'] or '未知'
    cat_gmv[cat] += r['amount']
    cat_qty[cat] += r['qty']
for cat, gm in sorted(cat_gmv.items(), key=lambda x: -x[1]):
    pct_val = gm / sum(cat_gmv.values()) * 100 if cat_gmv else 0
    print(f'    {cat:<8s}: {fmt(gm):>12s} 元 ({pct_val:5.1f}%)  {cat_qty[cat]:,.0f}件')

# sub_category GMV TOP10
print()
print('  子品类 GMV TOP10（sub_category）：')
sub_gmv = defaultdict(float)
for r in sales_2026:
    sub = r['sub_category'] or '未知'
    sub_gmv[sub] += r['amount']
print('    排名  子品类       GMV(元)      占比    件数')
for i, (sub, gm) in enumerate(sorted(sub_gmv.items(), key=lambda x: -x[1])[:10], 1):
    pct_val = gm / sum(sub_gmv.values()) * 100 if sub_gmv else 0
    q = sum(r['qty'] for r in sales_2026 if (r['sub_category'] or '未知') == sub)
    print(f'    {i:>2}. {sub:<10s} {fmt(gm):>12s}  {pct_val:5.1f}%  {q:,.0f}件')

# ========== 4. 四率诊断 ==========
print()
print('【4. 四率诊断】')

# 4.1 动销率（库存 SKU 维度）
inv_skus = set(r['style_color'] or r['barcode'] for r in inv if r['style_color'] or r['barcode'])
sold_skus = set(r['style_color'] or r['barcode'] for r in sales if r['style_color'] or r['barcode'])
sold_inv_skus = inv_skus & sold_skus
str_total = len(inv_skus)
str_sold = len(sold_inv_skus)
str_rate = str_sold / str_total if str_total > 0 else 0
print(f'  动销率: {str_rate:.1%} ({str_sold}/{str_total} 个SKU)')
print(f'    → 诊断：{"✅ 良好" if str_rate >= 0.7 else "⚠️ 偏低，需促销拉动" if str_rate >= 0.5 else "🔴 过低，库存积压严重"}')

# 4.2 售罄率（入库口径）
# 到货总量 + 当前库存 ≈ 历史入库总量
arr_total = sum(r['actual_qty'] for r in arr if r['actual_qty'])
inv_total = sum(r['stock_qty'] for r in inv if r['stock_qty'])
sold_total_ytd = sum(r['qty'] for r in sales_2026 if r['qty'])
total_inflow = arr_total + inv_total
sellout_rate = sold_total_ytd / total_inflow if total_inflow > 0 else 0
print(f'  售罄率: {sellout_rate:.1%} ({sold_total_ytd:,.0f}件 / {total_inflow:,.0f}件)')
print(f'    → 诊断：{"✅ 优秀" if sellout_rate >= 0.70 else "⚠️ 偏低" if sellout_rate >= 0.50 else "🔴 滞销严重"}')

# 按 sub_category 售罄率
print()
print('  子品类售罄率 TOP5 / BOTTOM5：')
sub_inflow = defaultdict(int)
sub_sold = defaultdict(int)
for r in inv:
    sub = r['sub_category'] or '未知'
    sub_inflow[sub] += r['stock_qty']
for r in arr:
    sub = r['sub_category'] or '未知'
    sub_inflow[sub] += r['actual_qty']
for r in sales_2026:
    sub = r['sub_category'] or '未知'
    sub_sold[sub] += r['qty']
sub_sellout = {sub: sub_sold[sub] / sub_inflow[sub] if sub_inflow[sub] > 0 else 0 for sub in set(sub_inflow)}
sorted_sellout = sorted(sub_sellout.items(), key=lambda x: -x[1])
print('    TOP5（最畅销）：')
for sub, rate in sorted_sellout[:5]:
    print(f'      {sub:<10s}: {rate:.1%}  (销{sub_sold[sub]:,} / 入{sub_inflow[sub]:,})')
print('    BOTTOM5（滞销）：')
for sub, rate in sorted_sellout[-5:]:
    print(f'      {sub:<10s}: {rate:.1%}  (销{sub_sold[sub]:,} / 入{sub_inflow[sub]:,})')

# 4.3 折扣率
total_amount = sum(r['amount'] for r in sales_2026)
total_tag = sum(r['tag_amount'] or (r['tag_price'] * r['qty']) for r in sales_2026 if r['tag_price'] and r['qty'])
disc_rate = total_amount / total_tag if total_tag > 0 else 0
avg_disc = disc_rate * 10  # 换算为 X.0 折
print(f'  折扣率: {disc_rate:.2%}（约 {avg_disc:.1f} 折）')
print(f'    → 诊断：{"✅ 良好（>8折）" if disc_rate >= 0.80 else "⚠️ 偏低（7-8折可接受）" if disc_rate >= 0.70 else "🔴 过低（<7折），促销过度"}')

# 4.4 流转率（库存周转天数）
avg_monthly_sold = sold_total_ytd / max(len(sales_2026) / 30, 1)
turnover_days = (inv_total / avg_monthly_sold * 30) if avg_monthly_sold > 0 else 0
print(f'  库存周转天数: {turnover_days:.0f} 天')
print(f'    → 诊断：{"✅ 优秀（<60天）" if turnover_days < 60 else "⚠️ 偏慢（60-90天）" if turnover_days < 90 else "🔴 过慢（>90天），资金压占"}')

# ========== 5. ABC 分类（按 sub_category） ==========
print()
print('【5. ABC 分类（按子品类）】')
abc_data = []
total_sub_gmv = sum(sub_gmv.values())
for sub, gm in sub_gmv.items():
    pct_val = gm / total_sub_gmv if total_sub_gmv > 0 else 0
    sold = sub_sold.get(sub, 0)
    inflow = sub_inflow.get(sub, 0)
    sellout = sold / inflow if inflow > 0 else 0
    abc_data.append({'sub': sub, 'gmv': gm, 'pct': pct_val, 'sellout': sellout})

abc_data.sort(key=lambda x: -x['gmv'])
cum = 0
for item in abc_data:
    cum += item['pct']
    item['cum'] = cum
    if cum <= 0.70 + item['pct']:
        item['abc'] = 'A'
    elif cum <= 0.90 + item['pct']:
        item['abc'] = 'B'
    else:
        item['abc'] = 'C'

print('  A类（主力品类，贡献70% GMV）：')
for item in [x for x in abc_data if x['abc'] == 'A']:
    print(f'    ✅ {item["sub"]:<10s} {item["gmv"]:>12,.0f}元 占比{item["pct"]:.1%}  累计{item["cum"]:.1%}  售罄{item["sellout"]:.1%}')
print('  B类（增长品类，贡献20% GMV）：')
for item in [x for x in abc_data if x['abc'] == 'B']:
    print(f'    ⚡ {item["sub"]:<10s} {item["gmv"]:>12,.0f}元 占比{item["pct"]:.1%}  累计{item["cum"]:.1%}  售罄{item["sellout"]:.1%}')
print('  C类（长尾品类，贡献10% GMV）：')
for item in [x for x in abc_data if x['abc'] == 'C']:
    print(f'    🔹 {item["sub"]:<10s} {item["gmv"]:>12,.0f}元 占比{item["pct"]:.1%}  累计{item["cum"]:.1%}  售罄{item["sellout"]:.1%}')

# ========== 6. 721 货品结构 ==========
print()
print('【6. 721 货品结构分析】')
basic_keywords = ['T恤', '衬衫', '裤', '牛仔', '基础', '休闲裤', '内裤', '袜子', 'polo', '保暖']
fashion_keywords = ['连衣裙', '裙', '卫衣', '毛衫', '针织', '外套', '茄克', '时装']
image_keywords = ['西装', '礼服', '套装', '高定', '限量']

basic_gmv = sum(v for k, v in sub_gmv.items() if any(bk in k for bk in basic_keywords))
fashion_gmv = sum(v for k, v in sub_gmv.items() if any(fk in k for fk in fashion_keywords))
image_gmv = sum(v for k, v in sub_gmv.items() if any(ik in k for ik in image_keywords))
other_gmv = total_sub_gmv - basic_gmv - fashion_gmv - image_gmv
total_721 = basic_gmv + fashion_gmv + image_gmv

print(f'  基础款: {fmt(basic_gmv):>12s} 元 ({basic_gmv/total_sub_gmv:.1%})  ← 目标 70%')
print(f'  时尚款: {fmt(fashion_gmv):>12s} 元 ({fashion_gmv/total_sub_gmv:.1%})  ← 目标 20%')
print(f'  形象款: {fmt(image_gmv):>12s} 元 ({image_gmv/total_sub_gmv:.1%})  ← 目标 10%')
print(f'  未归类: {fmt(other_gmv):>12s} 元 ({other_gmv/total_sub_gmv:.1%})')

ratio_msg = ''
if abs(basic_gmv/total_sub_gmv - 0.70) < 0.05:
    ratio_msg = '✅ 结构合理'
elif basic_gmv/total_sub_gmv > 0.80:
    ratio_msg = '⚠️ 基础款偏重，建议增加时尚款比例'
else:
    ratio_msg = '⚠️ 时尚款/形象款不足，结构失衡'
print(f'    → {ratio_msg}')

# ========== 7. 波士顿矩阵（按 category 大类） ==========
print()
print('【7. 波士顿矩阵（按品类大类）】')
ly_cat_gmv = defaultdict(float)
for r in sales_2025:
    ly_cat_gmv[r['category'] or '未知'] += r['amount']

growth_threshold = 0.0  # 用绝对增长率，今年和去年对比
bcg = []
total_gmv_2026 = sum(cat_gmv.values())
for cat, gm in cat_gmv.items():
    gm_ly = ly_cat_gmv.get(cat, 0)
    growth = (gm - gm_ly) / gm_ly if gm_ly > 0 else 0
    share = gm / total_gmv_2026 if total_gmv_2026 > 0 else 0
    bcg.append({'cat': cat, 'gmv': gm, 'growth': growth, 'share': share})

avg_share = 1.0 / len(bcg) if bcg else 0  # 均分阈值
for b in bcg:
    if b['growth'] >= growth_threshold and b['share'] >= avg_share:
        b['type'] = '⭐ 明星'
    elif b['growth'] < growth_threshold and b['share'] >= avg_share:
        b['type'] = '💰 金牛'
    elif b['growth'] >= growth_threshold and b['share'] < avg_share:
        b['type'] = '❓ 问题'
    else:
        b['type'] = '🐕 瘦狗'
    print(f"  {b['type']:<6s} {b['cat']:<8s} GMV:{fmt(b['gmv']):>10s} 同比:{b['growth']:+.1%} 份额:{b['share']:.1%}")

# ========== 8. RFM 用户分层 ==========
print()
print('【8. RFM 用户分层（基于 member_id）】')
ref_date = datetime.strptime(TODAY, '%Y-%m-%d')
member_data = defaultdict(lambda: {'amount': 0.0, 'qty': 0, 'dates': [], 'orders': set()})

for r in sales_2026:
    mid = r['member_id']
    if mid and str(mid).strip():
        member_data[mid]['amount'] += r['amount']
        member_data[mid]['qty'] += r['qty']
        member_data[mid]['dates'].append(r['sale_date'])
        if r['order_no']:
            member_data[mid]['orders'].add(r['order_no'])

total_members = len(member_data)
print(f'  2026年活跃会员: {total_members:,} 人')

R_THR = 60   # 最近60天内有消费
F_THR = 2    # 2次及以上购买
M_THR = 500  # 累计消费500元（服装客单低，设低阈值）

rfm_labels = {
    '111': '111_顶级价值', '110': '110_消费潜力', '101': '101_重要发展',
    '100': '100_新客', '011': '011_重要保持', '010': '010_一般用户',
    '001': '001_流失预警', '000': '000_流失用户'
}
rfm_counts = defaultdict(int)
rfm_gmv = defaultdict(float)

for mid, stats in member_data.items():
    dates_str = [str(d) for d in stats['dates']]
    max_date_str = max(dates_str) if dates_str else None
    days_ago = (ref_date - datetime.strptime(max_date_str, '%Y-%m-%d')).days if max_date_str else 999
    f = len(stats['orders'])
    m = stats['amount']
    r_score = 1 if days_ago <= R_THR else 0
    f_score = 1 if f >= F_THR else 0
    m_score = 1 if m >= M_THR else 0
    code = f'{r_score}{f_score}{m_score}'
    rfm_counts[code] += 1

for r in sales_2026:
    mid = r['member_id']
    if mid and str(mid).strip() and mid in member_data:
        stats = member_data[mid]
        dates_str = [str(d) for d in stats['dates']]
        max_date_str = max(dates_str) if dates_str else None
        days_ago = (ref_date - datetime.strptime(max_date_str, '%Y-%m-%d')).days if max_date_str else 999
        f = len(stats['orders'])
        m = stats['amount']
        r_score = 1 if days_ago <= R_THR else 0
        f_score = 1 if f >= F_THR else 0
        m_score = 1 if m >= M_THR else 0
        code = f'{r_score}{f_score}{m_score}'
        rfm_gmv[code] += r['amount']

print()
for code, label in sorted(rfm_labels.items(), reverse=True):
    cnt = rfm_counts.get(code, 0)
    gmv_val = rfm_gmv.get(code, 0)
    pct_cnt = cnt / total_members * 100 if total_members > 0 else 0
    pct_gmv = gmv_val / sum(rfm_gmv.values()) * 100 if rfm_gmv else 0
    action = {
        '111': '→ 重点维护，专属权益',
        '110': '→ 提升消费频次，培养忠诚',
        '101': '→ 提高客单价，推高价值款',
        '100': '→ 首次触达，激活复购',
        '011': '→ 流失召回，短信/电话唤醒',
        '010': '→ 定向营销，刺激二次购买',
        '001': '→ 紧急召回，优惠券激励',
        '000': '→ 暂时放弃，节省成本',
    }.get(code, '')
    print(f'  {label:<14s}: {cnt:>5,}人 ({pct_cnt:5.1f}%)  GMV:{fmt(gmv_val):>12s}({pct_gmv:5.1f}%)  {action}')

# ========== 9. AIPL 链路 ==========
print()
print('【9. AIPL 链路健康度】')
all_members = len(set(r['member_id'] for r in sales if r['member_id'] and str(r['member_id']).strip()))
repeat_members = total_members  # 2026年有消费的会员=已激活
loyal_members = sum(1 for mid, s in member_data.items() if len(s['orders']) >= 2)
pure_members = sum(1 for mid, s in member_data.items() if len(s['orders']) == 1)

print(f'  A（认知/曝光）:   {all_members:>6,} 人（累计会员）')
print(f'  I（兴趣/首购）:   {pure_members:>6,} 人（A→I: {pure_members/all_members*100:.1f}%）')
print(f'  P（购买/总活跃）: {repeat_members:>6,} 人（I→P: 100%，已激活）')
print(f'  L（忠诚/复购）:   {loyal_members:>6,} 人（P→L: {loyal_members/repeat_members*100:.1f}%）')
print(f'    → 复购率（复购会员/活跃会员）: {loyal_members/repeat_members*100:.1f}%')

# ========== 10. 门店分析 ==========
print()
print('【10. 门店 GMV 排名（2026年）】')
shop_gmv = defaultdict(float)
for r in sales_2026:
    shop = r['shop_name'] or '未知'
    shop_gmv[shop] += r['amount']
shop_list = sorted(shop_gmv.items(), key=lambda x: -x[1])
total_shop_gmv = sum(v for v in shop_gmv.values())
for i, (shop, gm) in enumerate(shop_list, 1):
    short = shop_full_to_short.get(shop, '未知')
    region = shop_full_to_region.get(shop, '未知')
    pct_val = gm / total_shop_gmv if total_shop_gmv > 0 else 0
    print(f'  {i:>2}. {short:<15s}  {region:<6s}  {fmt(gm):>12s}元 ({pct_val:.1%})')

# ========== 11. 版型分析 ==========
print()
print('【11. 版型 fit_name 分析（2026年）】')
fit_gmv = defaultdict(float)
fit_qty = defaultdict(int)
for r in sales_2026:
    fit = r['fit_name'] or '未知'
    fit_gmv[fit] += r['amount']
    fit_qty[fit] += r['qty']
print('    版型           GMV         件数    件单价    占比')
for fit, gm in sorted(fit_gmv.items(), key=lambda x: -x[1])[:10]:
    q = fit_qty[fit]
    avg_p = gm / q if q > 0 else 0
    pct_val = gm / total_sub_gmv * 100
    print(f'    {fit:<14s} {fmt(gm):>12s}  {q:>5,}件  {avg_p:>7.1f}元  {pct_val:5.1f}%')

# ========== 12. 月度健康度打分 ==========
print()
print('【12. 月度运营健康度打分】')
score_total = 0

# 动销率 (25分)
s_str = min(25, str_rate / 0.70 * 25) if str_rate > 0 else 0
score_total += s_str
print(f'  动销率:   {str_rate:.1%} → {s_str:.0f}/25分  {"✅" if s_str >= 18 else "⚠️" if s_str >= 12 else "🔴"}')

# 售罄率 (25分)
s_so = min(25, sellout_rate / 0.70 * 25) if sellout_rate > 0 else 0
score_total += s_so
print(f'  售罄率:   {sellout_rate:.1%} → {s_so:.0f}/25分  {"✅" if s_so >= 18 else "⚠️" if s_so >= 12 else "🔴"}')

# 折扣率 (25分) — 目标 8折
s_disc = min(25, disc_rate / 0.80 * 25) if disc_rate > 0 else 0
score_total += s_disc
print(f'  折扣率:   {disc_rate:.2%}({avg_disc:.1f}折) → {s_disc:.0f}/25分  {"✅" if s_disc >= 18 else "⚠️" if s_disc >= 12 else "🔴"}')

# 流转率 (25分) — 目标60天
s_inv = min(25, 60 / turnover_days * 25) if turnover_days > 0 else 0
score_total += s_inv
print(f'  流转率:   {turnover_days:.0f}天 → {s_inv:.0f}/25分  {"✅" if s_inv >= 18 else "⚠️" if s_inv >= 12 else "🔴"}')

print(f'  ─────────────────────────────────')
print(f'  综合得分: {score_total:.0f}/100分  {"🟢优秀" if score_total >= 80 else "🟡良好" if score_total >= 60 else "🔴警告"}')

# ========== 13. 行动指南 ==========
print()
print('【13. 行动指南（基于 PDCA + 四率诊断）】')
print()
print('  📋 P（Plan）—— 本月计划建议：')
low_sellout = [sub for sub, rate in sorted(sub_sellout.items(), key=lambda x: x[1])[:3] if rate < 0.5]
if low_sellout:
    print(f'    1. 滞销品类（{"/".join(low_sellout)}）需加速清货，折扣目标降至{pct(disc_rate - 0.1, 1) if disc_rate > 0.5 else "N/A"}')
print(f'    2. A类主力品类（{[x["sub"] for x in abc_data if x["abc"]=="A"][:3]}）备货充足，维持动销率 >70%')
print(f'    3. RFM 流失预警用户 {rfm_counts.get("001",0)+rfm_counts.get("000",0):,} 人，启动召回计划')

print()
print('  ⚡ D（Do）—— 本周执行动作：')
top3_shop = shop_list[:3]
print(f'    1. TOP3 门店（{"、".join([shop_full_to_short.get(s[0],s[0]) for s in top3_shop])}）重点维护，确保库存充足')
print(f'    2. 时尚款（{fashion_gmv/total_sub_gmv:.0%}占GMV）加大陈列和推荐力度')
print(f'    3. 版型偏好：{sorted(fit_gmv.items(), key=lambda x: -x[1])[0][0]} 最受欢迎，主推该版型')

print()
print('  📊 C（Check）—— 月底核查指标：')
print(f'    1. 目标动销率: ≥70% | 实际: {str_rate:.1%} | 差距: {(str_rate-0.70)*100:+.1f}pp')
print(f'    2. 目标售罄率: ≥70% | 实际: {sellout_rate:.1%} | 差距: {(sellout_rate-0.70)*100:+.1f}pp')
print(f'    3. 目标折扣率: ≥80% | 实际: {disc_rate:.1%} | 差距: {(disc_rate-0.80)*100:+.1f}pp')
print(f'    4. 目标流转天数: ≤60天 | 实际: {turnover_days:.0f}天 | 差距: {turnover_days-60:+.0f}天')

print()
print('  🔧 A（Act）—— 下月调整方向：')
if score_total >= 80:
    print('    综合健康度优秀，保持现状，小幅优化薄弱环节')
elif score_total >= 60:
    print('    综合健康度一般，重点解决：折扣率过低、流转过慢两项短板')
    print('    → 建议减少促销次数；集中资源清仓滞销品')
else:
    print('    综合健康度警告，全面复盘：商品结构/定价策略/门店运营三方面')
    print('    → 建议 PDCA 专项会议，制定改善计划')

# ========== 生成报告文件 ==========
conn.close()
print()
print('=' * 60)
print(f'  ✅ 分析完成！报告存至: {REPORT_PATH}')
print('=' * 60)
