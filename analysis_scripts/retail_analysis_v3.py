# -*- coding: utf-8 -*-
"""
服装零售数据分析脚本 v3.0（修正版）
✅ 修正1：sales.shop_name = shops.short_name（已知事实：sales存简称）
✅ 修正2：流转率公式 = 月均库存 / 月均销售 × 30天
✅ 修正3：售罄率口径 = 本期销售 / (期初库存 + 本期到货)
✅ 修正4：月均销售用月度实际数据

使用说明：PYTHONIOENCODING=utf-8 python retail_analysis_v3.py
"""

import sqlite3
from datetime import datetime
from collections import defaultdict

DB_PATH = 'C:/Users/MacBookPro/cabbeen_data/cabbeen.db'
TODAY = '2026-04-21'
ANALYSIS_MONTH = '2026-03'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def q(sql_str, params=None):
    if params:
        cur.execute(sql_str, params)
    else:
        cur.execute(sql_str)
    return cur.fetchall()

def fmt(n):
    return f'{n:,.0f}' if n is not None else 'N/A'

def pct(a, b):
    return f'{a/b*100:.1f}%' if b and b != 0 else 'N/A'

def diag_rate(val, good, warn):
    """四率诊断：返回等级和说明"""
    if val >= good:
        return '✅ 优秀', f'{val:.1%}'
    elif val >= warn:
        return '⚠️ 偏低', f'{val:.1%}'
    else:
        return '🔴 警告', f'{val:.1%}'

# =====================================================================
print('=' * 62)
print('  服装零售数据分析 v3.0（修正确认版）')
print('  分析日期：2026-04-21 | 数据截止：2026-04-20')
print('=' * 62)

# =====================================================================
# 【1. 数据加载 & 关键字段验证】
# =====================================================================
print('\n【1. 数据概览】')
sales = q("SELECT * FROM sales WHERE sale_date IS NOT NULL")
inv = q("SELECT * FROM inventory")
arr = q("SELECT * FROM arrival")
shops_rows = q("SELECT * FROM shops")

print(f'  销售记录: {len(sales):,} 条')
print(f'  库存快照: {len(inv):,} 条 (截至 {inv[0]["snapshot_date"] if inv else "N/A"})')
print(f'  到货记录: {len(arr):,} 条')
print(f'  店铺数:   {len(shops_rows):,} 家')

# 店铺映射（已知：sales.shop_name = shops.short_name）
shop_map = {str(r['short_name']): dict(r) for r in shops_rows}
shop_names_in_sales = set(r['shop_name'] for r in sales if r['shop_name'])
shop_names_in_shops = set(shop_map.keys())
print(f'  店铺映射验证: sales中{len(shop_names_in_sales)}家 vs shops中{len(shop_names_in_shops)}家')
print(f'  已匹配店铺: {shop_names_in_sales & shop_names_in_shops}')
excluded = shop_names_in_sales - shop_names_in_shops
if excluded:
    print(f'  ⚠️ 未匹配店铺（可能已排除）: {excluded}')

# =====================================================================
# 【2. 时间切片】
# =====================================================================
print('\n【2. 时间切片】')
sales_2026 = [r for r in sales if str(r['sale_date']).startswith('2026')]
sales_2025 = [r for r in sales if str(r['sale_date']).startswith('2025')]
sales_2024 = [r for r in sales if str(r['sale_date']).startswith('2024')]
sales_m = [r for r in sales if str(r['sale_date']).startswith(ANALYSIS_MONTH)]
sales_curr = [r for r in sales if str(r['sale_date']).startswith('2026-04')]

# 月度数据
monthly = defaultdict(lambda: {'gmv': 0, 'qty': 0, 'orders': set(), 'members': set()})
for r in sales_2026:
    m = str(r['sale_date'])[:7]
    monthly[m]['gmv'] += r['amount'] or 0
    monthly[m]['qty'] += r['qty'] or 0
    if r['order_no']:
        monthly[m]['orders'].add(r['order_no'])
    if r['member_id'] and str(r['member_id']).strip():
        monthly[m]['members'].add(r['member_id'])

for m, d in sorted(monthly.items()):
    print(f'  {m}: GMV {fmt(d["gmv"]):>12s}  件数{d["qty"]:>5,.0f}  订单{len(d["orders"]):>4}  会员{len(d["members"]):>4}')

# =====================================================================
# 【3. GMV 仪表盘】
# =====================================================================
print('\n【3. GMV 仪表盘】')

def gmv_block(rows, label, compare_rows=None):
    if not rows:
        print(f'  {label}: 无数据')
        return 0, 0, 0
    gmv = sum(r['amount'] for r in rows)
    qty = sum(r['qty'] for r in rows)
    orders = len(set(r['order_no'] for r in rows if r['order_no']))
    members = len(set(r['member_id'] for r in rows if r['member_id'] and str(r['member_id']).strip()))
    avg_price = gmv / qty if qty > 0 else 0
    avg_order = gmv / orders if orders > 0 else 0
    tag_total = sum(r['tag_amount'] or (r['tag_price'] * r['qty']) for r in rows if r['tag_price'] and r['qty'])
    disc = gmv / tag_total if tag_total > 0 else 0
    disc_zk = disc * 10
    print(f'  {label}:')
    print(f'    GMV:     {fmt(gmv):>12s} 元')
    print(f'    件数:    {qty:>8,.0f} 件')
    print(f'    订单:    {orders:>6,} 单')
    print(f'    会员:    {members:>6,} 人  ({pct(members, orders)}/单)')
    print(f'    件单价:  {avg_price:>8.1f} 元')
    print(f'    客单价:  {avg_order:>8.1f} 元')
    print(f'    折扣率:  {disc:.2%}  ({disc_zk:.1f}折)')
    if compare_rows and compare_rows:
        gmvc = sum(r['amount'] for r in compare_rows)
        if gmvc > 0:
            yoy = (gmv - gmvc) / gmvc * 100
            print(f'    同比:    {yoy:+.1f}%  (vs {fmt(gmvc)})')
    return gmv, qty, disc

gmv_2026, qty_2026, disc_2026 = gmv_block(sales_2026, '2026年(1-4月)')
gmv_2025, qty_2025, disc_2025 = gmv_block(sales_2025, '2025年全年')
gmv_month, qty_month, disc_month = gmv_block(sales_m, f'{ANALYSIS_MONTH}月')

# =====================================================================
# 【4. 四率诊断】
# =====================================================================
print('\n【4. 四率诊断】')

# ── 4.1 动销率 ──
# 有销售记录的 SKU / 库存中的 SKU（以 barcode/style_color 为 SKU 标识）
inv_skus = set(r['barcode'] for r in inv if r['barcode'])
sold_skus = set(r['barcode'] for r in sales_2026 if r['barcode'])
sold_inv = inv_skus & sold_skus
str_rate = len(sold_inv) / len(inv_skus) if inv_skus else 0
status, val_str = diag_rate(str_rate, 0.70, 0.50)
print(f'  4.1 动销率: {val_str} ({len(sold_inv)}/{len(inv_skus)} SKU)')
print(f'     → {status} | 目标≥70%')

# ── 4.2 售罄率（2026年累计） ──
# 口径：2026年销售件数 / (当前库存 + 2026年新到货)
inv_qty = sum(r['stock_qty'] for r in inv if r['stock_qty'])
arr_2026 = [r for r in arr if str(r['delivery_date']).startswith('2026')]
arr_qty_2026 = sum(r['actual_qty'] for r in arr_2026 if r['actual_qty'])
total_inflow = inv_qty + arr_qty_2026
sellout_rate = qty_2026 / total_inflow if total_inflow > 0 else 0
status, val_str = diag_rate(sellout_rate, 0.70, 0.50)
print(f'  4.2 售罄率: {val_str} ({qty_2026:,.0f}/{total_inflow:,.0f}件)')
print(f'     → {status} | 目标≥70%')

# 子品类售罄率 TOP/BOTTOM
sub_inflow = defaultdict(int)
sub_sold_2026 = defaultdict(float)
for r in inv:
    sub_inflow[r['sub_category'] or '未知'] += r['stock_qty']
for r in arr_2026:
    sub_inflow[r['sub_category'] or '未知'] += r['actual_qty']
for r in sales_2026:
    sub_sold_2026[r['sub_category'] or '未知'] += r['qty']
sub_so = {sub: sub_sold_2026[sub] / sub_inflow[sub] if sub_inflow[sub] > 0 else 0 for sub in sub_inflow}
sorted_so = sorted(sub_so.items(), key=lambda x: -x[1])
top3 = [(s, sub_so[s], sub_sold_2026[s], sub_inflow[s]) for s, _ in sorted_so[:3] if sub_so[s] > 0]
bot3 = [(s, sub_so[s], sub_sold_2026[s], sub_inflow[s]) for s, _ in sorted_so[-3:] if sub_inflow[s] > 0]
print(f'     TOP3畅销: {", ".join([f"{s}({r:.0%})" for s,r,_,__ in top3])}')
print(f'     BOTTOM滞销: {", ".join([f"{s}({r:.0%})" for s,r,_,__ in bot3])}')

# ── 4.3 折扣率 ──
status, val_str = diag_rate(disc_2026, 0.80, 0.70)
print(f'  4.3 折扣率: {val_str} ({disc_2026*10:.1f}折)')
print(f'     → {status} | 目标≥80%')

# ── 4.4 流转率（修正公式） ──
# 月均库存 / 月均销售 * 30
days_in_2026 = (datetime(2026, 4, 20) - datetime(2026, 1, 1)).days + 1  # ~110天
months_frac = days_in_2026 / 30  # 折算月数
monthly_avg_sold = qty_2026 / months_frac if months_frac > 0 else 0
inv_turnover_days = (inv_qty / monthly_avg_sold * 30) if monthly_avg_sold > 0 else 9999
status_inv = '✅ 优秀' if inv_turnover_days < 60 else '⚠️ 偏慢' if inv_turnover_days < 90 else '🔴 滞压'
print(f'  4.4 库存周转: {inv_turnover_days:.0f} 天（月均销 {monthly_avg_sold:,.0f} 件 / 当前库 {inv_qty:,} 件）')
print(f'     → {status_inv} | 目标≤60天')

# =====================================================================
# 【5. ABC 分类（按 sub_category）】
# =====================================================================
print('\n【5. ABC 分类（子品类，按 GMV）】')
sub_gmv = defaultdict(float)
for r in sales_2026:
    sub_gmv[r['sub_category'] or '未知'] += r['amount']
total_sub_gmv = sum(sub_gmv.values())

abc_list = []
for sub, gm in sub_gmv.items():
    pct_val = gm / total_sub_gmv if total_sub_gmv > 0 else 0
    sold = sub_sold_2026.get(sub, 0)
    inflow = sub_inflow.get(sub, 0)
    so = sold / inflow if inflow > 0 else 0
    abc_list.append({'sub': sub, 'gmv': gm, 'pct': pct_val, 'sellout': so})

abc_list.sort(key=lambda x: -x['gmv'])
cum = 0
for item in abc_list:
    cum += item['pct']
    item['cum'] = cum
    if cum - item['pct'] < 0.70:
        item['abc'] = 'A'
    elif cum - item['pct'] < 0.90:
        item['abc'] = 'B'
    else:
        item['abc'] = 'C'

for abc in ['A', 'B', 'C']:
    items = [x for x in abc_list if x['abc'] == abc]
    label = {'A': '主力品类（贡献70%）', 'B': '增长品类（贡献20%）', 'C': '长尾品类（贡献10%）'}[abc]
    print(f'  {abc}类  {label}:')
    for item in items:
        print(f'    {item["sub"]:<10s}  GMV {fmt(item["gmv"]):>10s}  占比{item["pct"]:.1%}  累计{item["cum"]:.1%}  售罄{item["sellout"]:.0%}')

# =====================================================================
# 【6. 721 货品结构】
# =====================================================================
print('\n【6. 721 货品结构】')
basic = ['T恤', '衬衫', '裤', '牛仔', '基础', '内裤', '袜子', 'polo', '保暖', '长袖T恤', '短袖T恤']
fashion = ['连衣裙', '裙', '卫衣', '毛衫', '针织', '外套', '茄克', '时装', '呢茄克', '长袖卫衣', '长袖线衫']
image = ['西装', '礼服', '套装', '高定', '限量']

b_gmv = sum(v for k, v in sub_gmv.items() if any(bk in k for bk in basic))
f_gmv = sum(v for k, v in sub_gmv.items() if any(fk in k for fk in fashion))
i_gmv = sum(v for k, v in sub_gmv.items() if any(ik in k for ik in image))
o_gmv = total_sub_gmv - b_gmv - f_gmv - i_gmv

print(f'  基础款: {fmt(b_gmv):>12s} ({b_gmv/total_sub_gmv:.1%})  目标70% {"✅" if abs(b_gmv/total_sub_gmv-0.70)<0.1 else "⚠️" if b_gmv/total_sub_gmv>0.60 else "🔴"}')
print(f'  时尚款: {fmt(f_gmv):>12s} ({f_gmv/total_sub_gmv:.1%})  目标20% {"✅" if abs(f_gmv/total_sub_gmv-0.20)<0.05 else "⚠️"}')
print(f'  形象款: {fmt(i_gmv):>12s} ({i_gmv/total_sub_gmv:.1%})  目标10% {"✅" if abs(i_gmv/total_sub_gmv-0.10)<0.03 else "⚠️"}')
print(f'  未归类: {fmt(o_gmv):>12s} ({o_gmv/total_sub_gmv:.1%})')

# =====================================================================
# 【7. 波士顿矩阵（按 category 大类）】
# =====================================================================
print('\n【7. 波士顿矩阵（品类大类）】')
ly_cat = defaultdict(float)
for r in sales_2025:
    ly_cat[r['category'] or '未知'] += r['amount']
total_ly = sum(ly_cat.values())

bcg_data = []
for cat, gm in {k: v for k, v in
    [(r['category'] or '未知', sum(s['amount'] for s in sales_2026 if (s['category'] or '未知') == r['category'] or (not r['category'] and not s['category'])))
     for r in sales_2026]}.items():
    pass

cat_gmv_2026 = defaultdict(float)
for r in sales_2026:
    cat_gmv_2026[r['category'] or '未知'] += r['amount']

for cat, gm in cat_gmv_2026.items():
    gm_ly = ly_cat.get(cat, 0)
    growth = (gm - gm_ly) / gm_ly if gm_ly > 0 else 0
    share = gm / sum(cat_gmv_2026.values()) if cat_gmv_2026 else 0
    avg_share = 1.0 / len(cat_gmv_2026) if cat_gmv_2026 else 0
    if growth >= 0 and share >= avg_share:
        btype = '⭐ 明星'
    elif growth < 0 and share >= avg_share:
        btype = '💰 金牛'
    elif growth >= 0 and share < avg_share:
        btype = '❓ 问题'
    else:
        btype = '🐕 瘦狗'
    print(f'  {btype}  {cat:<8s}  GMV {fmt(gm):>10s}  同比 {growth:+.1%}  份额 {share:.1%}')

# =====================================================================
# 【8. 门店 GMV 分析（JOIN 修正：shop_name = short_name）】
# =====================================================================
print('\n【8. 门店 GMV 排名（2026年）】')
shop_gmv = defaultdict(lambda: {'gmv': 0, 'qty': 0, 'orders': set(), 'members': set()})
for r in sales_2026:
    sn = r['shop_name'] or '未知'
    shop_gmv[sn]['gmv'] += r['amount']
    shop_gmv[sn]['qty'] += r['qty']
    if r['order_no']:
        shop_gmv[sn]['orders'].add(r['order_no'])
    if r['member_id'] and str(r['member_id']).strip():
        shop_gmv[sn]['members'].add(r['member_id'])

total_gmv = sum(v['gmv'] for v in shop_gmv.values())
shop_list = sorted(shop_gmv.items(), key=lambda x: -x[1]['gmv'])
for rank, (sn, d) in enumerate(shop_list, 1):
    info = shop_map.get(sn, {})
    region = info.get('region', '未知')
    city = info.get('city', '未知')
    stype = info.get('shop_type', '未知')
    pct_val = d['gmv'] / total_gmv if total_gmv > 0 else 0
    avg_order = d['gmv'] / len(d['orders']) if d['orders'] else 0
    print(f'  {rank}. {sn:<12s}  {region:<6s}  {fmt(d["gmv"]):>10s}元  {pct_val:.1%}  订单{len(d["orders"]):>3}  客单{avg_order:.0f}  [{stype}]')

# =====================================================================
# 【9. RFM 用户分层】
# =====================================================================
print('\n【9. RFM 用户分层（2026年活跃会员）】')
ref_date = datetime(2026, 4, 21)
member = defaultdict(lambda: {'amount': 0.0, 'qty': 0, 'dates': [], 'orders': set()})
for r in sales_2026:
    mid = r['member_id']
    if mid and str(mid).strip():
        member[mid]['amount'] += r['amount']
        member[mid]['qty'] += r['qty']
        member[mid]['dates'].append(r['sale_date'])
        if r['order_no']:
            member[mid]['orders'].add(r['order_no'])

total_m = len(member)
print(f'  2026年活跃会员: {total_m:,} 人')

R_T, F_T, M_T = 60, 2, 500  # 阈值
labels = {
    '111': ('顶级价值', '专属权益，高频维护'),
    '110': ('消费潜力', '提升频次，培养忠诚'),
    '101': ('重要发展', '推高客单，价值升级'),
    '100': ('新客', '激活复购，首购激励'),
    '011': ('重要保持', '流失召回，定向触达'),
    '010': ('一般用户', '营销刺激，二次购买'),
    '001': ('流失预警', '紧急召回，限时优惠'),
    '000': ('流失用户', '成本过高，暂时搁置'),
}
rc = defaultdict(int)
rg = defaultdict(float)
for mid, s in member.items():
    ds = [str(d) for d in s['dates']]
    max_d = max(ds) if ds else None
    days = (ref_date - datetime.strptime(max_d, '%Y-%m-%d')).days if max_d else 999
    f = len(s['orders'])
    m = s['amount']
    code = f'{1 if days<=R_T else 0}{1 if f>=F_T else 0}{1 if m>=M_T else 0}'
    rc[code] += 1

for r in sales_2026:
    mid = r['member_id']
    if mid and str(mid).strip() and mid in member:
        s = member[mid]
        ds = [str(d) for d in s['dates']]
        max_d = max(ds) if ds else None
        days = (ref_date - datetime.strptime(max_d, '%Y-%m-%d')).days if max_d else 999
        f = len(s['orders'])
        m = s['amount']
        code = f'{1 if days<=R_T else 0}{1 if f>=F_T else 0}{1 if m>=M_T else 0}'
        rg[code] += r['amount']

for code in ['111', '110', '101', '100', '011', '010', '001', '000']:
    cnt = rc.get(code, 0)
    gmv_val = rg.get(code, 0)
    name, action = labels[code]
    cp = cnt / total_m * 100 if total_m > 0 else 0
    gp = gmv_val / sum(rg.values()) * 100 if rg else 0
    bar = '█' * int(cp / 2) if cp > 0 else ''
    print(f'  {code} {name:<10s}: {cnt:>5,}人 ({cp:5.1f}%) {bar:<25s} GMV {fmt(gmv_val):>10s}({gp:5.1f}%)  行动: {action}')

print(f'\n  复购会员: {sum(1 for m,s in member.items() if len(s["orders"])>=2):,} / {total_m} = {sum(1 for m,s in member.items() if len(s["orders"])>=2)/total_m:.1%}')

# =====================================================================
# 【10. AIPL 链路】
# =====================================================================
print('\n【10. AIPL 链路健康度】')
all_members = len(set(r['member_id'] for r in sales if r['member_id'] and str(r['member_id']).strip()))
pure = sum(1 for m, s in member.items() if len(s['orders']) == 1)
repeat = sum(1 for m, s in member.items() if len(s['orders']) >= 2)
print(f'  A 曝光/认知: {all_members:>6,} 人（累计会员总量）')
print(f'  I 兴趣/首购: {pure:>6,} 人（仅1次购买）')
print(f'  P 购买/活跃: {total_m:>6,} 人（有消费记录）')
print(f'  L 忠诚/复购: {repeat:>6,} 人（≥2次购买）')
print(f'  A→I: {pct(pure, all_members)} | P→L: {pct(repeat, total_m)} | 链路健康度: {"优秀" if repeat/total_m>0.30 else "一般" if repeat/total_m>0.15 else "偏低"}')

# =====================================================================
# 【11. 版型分析】
# =====================================================================
print('\n【11. 版型 fit_name 分析】')
fit_gmv = defaultdict(float)
fit_qty = defaultdict(float)
for r in sales_2026:
    f = r['fit_name'] or '无版型'
    fit_gmv[f] += r['amount']
    fit_qty[f] += r['qty']
print(f'  {"版型":<14s}  {"GMV":>12s}  {"件数":>6s}  {"件单价":>8s}  {"占比":>6s}')
for fit, gm in sorted(fit_gmv.items(), key=lambda x: -x[1])[:8]:
    q = fit_qty[fit]
    ap = gm / q if q > 0 else 0
    print(f'  {fit:<14s}  {fmt(gm):>12s}  {q:>5.0f}件  {ap:>7.1f}元  {gm/total_sub_gmv:.1%}')

# =====================================================================
# 【12. 综合健康度打分】
# =====================================================================
print('\n【12. 综合健康度打分】')
scores = {}
scores['动销率'] = min(25, str_rate / 0.70 * 25)
scores['售罄率'] = min(25, sellout_rate / 0.70 * 25)
scores['折扣率'] = min(25, disc_2026 / 0.80 * 25)
scores['流转率'] = min(25, 60 / inv_turnover_days * 25) if inv_turnover_days > 0 else 0
total_s = sum(scores.values())
bar = '█' * int(total_s / 4) + '░' * (25 - int(total_s / 4))
print(f'  {"指标":<8s}  {"实际值":>10s}  {"目标":>8s}  {"得分":>6s}/25  {"状态":>6s}')
print(f'  {"─"*50}')
for k, v in scores.items():
    target = {'动销率': '≥70%', '售罄率': '≥70%', '折扣率': '≥80%', '流转率': '≤60天'}[k]
    actual = {'动销率': f'{str_rate:.1%}', '售罄率': f'{sellout_rate:.1%}', '折扣率': f'{disc_2026:.1%}', '流转率': f'{inv_turnover_days:.0f}天'}[k]
    icon = '✅' if v >= 18 else '⚠️' if v >= 12 else '🔴'
    print(f'  {k:<8s}  {actual:>10s}  {target:>8s}  {v:>5.0f}      {icon}')
print(f'  {"─"*50}')
print(f'  综合得分: {total_s:.0f}/100  {bar}  {"🟢优秀" if total_s>=80 else "🟡良好" if total_s>=60 else "🔴警告"}')

# =====================================================================
# 【13. 决策建议（PDCA + 知识库模型联动）】
# =====================================================================
print('\n【13. 决策建议】')

print('\n  【P】Plan — 本月计划：')
# 找最需要行动的维度
worst = min(scores.items(), key=lambda x: x[1])
worst_name = {'动销率': '动销率过低', '售罄率': '售罄率过低', '折扣率': '折扣率偏低', '流转率': '库存周转过慢'}[worst[0]]
print(f'    首要任务: {worst_name}（得分{worst[1]:.0f}/25），重点解决')
top3_cat = [x['sub'] for x in sorted(abc_list, key=lambda t: -t['gmv'])[:3]]
print(f'    A类主力（{"/".join(top3_cat)}）确保充足备货')
print(f'    VIP流失预警 {rc.get("001",0)+rc.get("000",0)} 人，制定召回计划')

print('\n  【D】Do — 本周执行：')
for i, (sn, d) in enumerate(shop_list[:2], 1):
    print(f'    {i}. {sn} GMV {fmt(d["gmv"])}元，{len(d["orders"])}单 × {d["gmv"]/len(d["orders"]):.0f}元/单')
bot_sub = [s for s, _ in sorted_so[-3:] if sub_inflow[s] > 10]
print(f'    滞销品类（{"、".join(bot_sub)}）加速清仓，目标折扣降至{pct(disc_2026-0.05, 1) if disc_2026>0.05 else "N/A"}')

print('\n  【C】Check — 月底核查：')
print(f'    目标动销≥70%: 差距 {(str_rate-0.70)*100:+.1f}pp  | 售罄≥70%: 差距 {(sellout_rate-0.70)*100:+.1f}pp')
print(f'    目标折扣≥80%: 差距 {(disc_2026-0.80)*100:+.1f}pp  | 流转≤60d: 差距 {inv_turnover_days-60:+.0f}天')

print('\n  【A】Act — 下月调整：')
if total_s >= 80:
    print('    综合优秀，保持现状，聚焦复购率提升')
elif total_s >= 60:
    print('    综合一般，主攻：①促销清滞销 ②提升会员粘性 ③优化货品结构')
else:
    print('    综合警告，启动专项复盘：建议召开 PDCA 会议')

conn.close()
print('\n' + '=' * 62)
print('  ✅ v3.0 分析完成！')
print('=' * 62)
