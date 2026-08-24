# -*- coding: utf-8 -*-
"""
服装零售数据分析脚本 v1.0
基于 retail_knowledge_base.md 理论模型
运行真实数据，输出决策建议

使用说明：
    python retail_analysis_v1.py

输出：
    1. GMV 仪表盘
    2. 四率诊断（动销率/售罄率/折扣率/流转率）
    3. ABC 分类
    4. 721 货品结构
    5. RFM 用户分层
    6. 波士顿矩阵
    7. AIPL 链路
    8. 月度运营健康度
    9. 行动指南
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

# ========== 配置 ==========
DB_PATH = 'C:/Users/MacBookPro/cabbeen_data/cabbeen.db'
OUTPUT_PATH = 'C:/Users/MacBookPro/WorkBuddy/20260421102454/retail_analysis_report.md'
TODAY = '2026-04-21'
ANALYSIS_MONTH = '2026-03'  # 分析月份（最近完整月份）

# ========== 数据库连接 ==========
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def q(sql, params=None):
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    return cur.fetchall()


def pct(a, b):
    if b == 0 or b is None:
        return 'N/A'
    return f'{a / b * 100:.1f}%'


# ========== 1. 基础数据准备 ==========
print('📊 正在加载基础数据...')

# 销售数据
all_sales = q("SELECT * FROM sales")
print(f'  总销售记录: {len(all_sales):,} 条')

# 库存数据
all_inv = q("SELECT * FROM inventory")
print(f'  总库存记录: {len(all_inv):,} 条')

# 到货数据
all_arr = q("SELECT * FROM arrival")
print(f'  总到货记录: {len(all_arr):,} 条')

# 订单数据
all_orders = q("SELECT * FROM orders")
print(f'  总订单记录: {len(all_orders):,} 条')

# 店铺数据
shops = q("SELECT * FROM shops")
print(f'  店铺数: {len(shops)} 家')

# 会员销售（有member_id的）
vip_sales = q("SELECT * FROM sales WHERE member_id IS NOT NULL AND member_id != ''")
print(f'  会员销售记录: {len(vip_sales):,} 条 ({len(vip_sales)/len(all_sales)*100:.1f}%)')

# 日期范围
r = q("SELECT MIN(sale_date), MAX(sale_date) FROM sales")[0]
print(f'  销售日期范围: {r[0]} ~ {r[1]}')

print()

# ========== 2. GMV 仪表盘 ==========
print('📊 计算 GMV 仪表盘...')

# 年度 GMV
year_sales = [s for s in all_sales if str(s['sale_date']).startswith('2026')]
gmv_2026 = sum(s['amount'] for s in year_sales)
qty_2026 = sum(s['qty'] for s in year_sales)
orders_2026 = len(set(s['order_no'] for s in year_sales))
avg_unit_price = gmv_2026 / qty_2026 if qty_2026 > 0 else 0
avg_order_value = gmv_2026 / orders_2026 if orders_2026 > 0 else 0
print(f'  2026年 GMV: {gmv_2026:,.0f} 元')
print(f'  2026年 销售件数: {qty_2026:,}')
print(f'  2026年 订单数: {orders_2026:,}')
print(f'  2026年 件单价: {avg_unit_price:.1f} 元')
print(f'  2026年 客单价: {avg_order_value:.1f} 元')

# 月度 GMV
month_sales = [s for s in all_sales if str(s['sale_date']).startswith(ANALYSIS_MONTH)]
gmv_month = sum(s['amount'] for s in month_sales)
qty_month = sum(s['qty'] for s in month_sales)
orders_month = len(set(s['order_no'] for s in month_sales))
# 上年同月
last_year_month = [s for s in all_sales if str(s['sale_date']).startswith('2025-' + ANALYSIS_MONTH[-2:])]
gmv_last_year = sum(s['amount'] for s in last_year_month)
print(f'  {ANALYSIS_MONTH} GMV: {gmv_month:,.0f} 元 (上年同期: {gmv_last_year:,.0f} 元)')
if gmv_last_year > 0:
    yoy = (gmv_month - gmv_last_year) / gmv_last_year * 100
    print(f'  同比: {yoy:+.1f}%')

# 品类 GMV 分解
cat_gmv = defaultdict(float)
for s in year_sales:
    cat_gmv[s['category'] or '未知'] += s['amount']
cat_gmv_sorted = sorted(cat_gmv.items(), key=lambda x: -x[1])

# 门店 GMV 分解
shop_gmv = defaultdict(float)
for s in year_sales:
    shop_gmv[s['shop_name'] or '未知'] += s['amount']
shop_gmv_sorted = sorted(shop_gmv.items(), key=lambda x: -x[1])

# ========== 3. 四率诊断 ==========
print('📊 计算四率诊断...')

# 3.1 动销率（按品类/单品）
# 有销售记录的SKU数 / 总SKU数（库存中的SKU）
inv_skus = set(s['style_color'] or s['barcode'] for s in all_inv if s['style_color'] or s['barcode'])
sold_skus = set(s['style_color'] or s['barcode'] for s in all_sales if s['style_color'] or s['barcode'])
sold_inv_skus = inv_skus & sold_skus  # 库存中有的且有销售的
str_total = len(inv_skus)  # 总SKU
str_sold = len(sold_inv_skus)  # 有销售的SKU
str_rate = str_sold / str_total if str_total > 0 else 0
print(f'  动销率: {str_rate:.1%} ({str_sold}/{str_total} 个SKU)')

# 3.2 售罄率（按品类）
# 销售数量 / (期初库存 + 到货数量)
# 用当前库存快照估算
inv_qty_by_cat = defaultdict(int)
for inv in all_inv:
    inv_qty_by_cat[inv['category'] or '未知'] += inv['stock_qty']

arr_qty_by_cat = defaultdict(int)
for arr in all_arr:
    arr_qty_by_cat[arr['category'] or '未知'] += arr['actual_qty']

sold_qty_by_cat = defaultdict(int)
for s in year_sales:
    sold_qty_by_cat[s['category'] or '未知'] += s['qty']

# 整体售罄率
total_inv = sum(inv['stock_qty'] for inv in all_inv)
total_arr = sum(arr['actual_qty'] for arr in all_arr)
total_sold_year = sum(s['qty'] for s in year_sales)
total_inflow = total_inv + total_arr
sellout_rate = total_sold_year / total_inflow if total_inflow > 0 else 0
print(f'  售罄率: {sellout_rate:.1%} ({total_sold_year:,}件 / {total_inflow:,}件)')

# 按品类计算售罄率
cat_sellout = {}
for cat in set(list(inv_qty_by_cat.keys()) + list(arr_qty_by_cat.keys())):
    inflow = inv_qty_by_cat[cat] + arr_qty_by_cat[cat]
    sold = sold_qty_by_cat[cat]
    cat_sellout[cat] = sold / inflow if inflow > 0 else 0

# 3.3 折扣率
# 实收金额 / 吊牌金额
total_amount = sum(s['amount'] for s in year_sales)
total_tag = sum((s['tag_amount'] or s['tag_price'] * s['qty']) for s in year_sales)
discount_rate = total_amount / total_tag if total_tag > 0 else 0
avg_discount = discount_rate * 10  # 换算成折扣
print(f'  折扣率: {discount_rate:.2%}（约 {avg_discount:.1f} 折）')
print(f'  实收: {total_amount:,.0f} 元 / 吊牌: {total_tag:,.0f} 元')

# 3.4 流转率（库存周转天数）
# 月均库存 / 月均销售 * 30
avg_inv_qty = total_inv  # 当前库存
avg_monthly_sold = total_sold_year / 4  # 假设2026年4个月
inv_turnover_days = (avg_inv_qty / avg_monthly_sold * 30) if avg_monthly_sold > 0 else 0
print(f'  库存周转天数: {inv_turnover_days:.0f} 天')

# ========== 4. ABC 分类（按品类） ==========
print('📊 计算 ABC 分类...')
cat_sales_data = []
for cat, gm in cat_gmv.items():
    sold_qty = sold_qty_by_cat.get(cat, 0)
    sold_amount = cat_gmv.get(cat, 0)
    sellout = cat_sellout.get(cat, 0)
    cat_sales_data.append({
        'category': cat,
        'gmv': gm,
        'qty': sold_qty,
        'sellout': sellout,
        'pct': 0,
        'cum_pct': 0,
        'abc': ''
    })

total_gmv = sum(c['gmv'] for c in cat_sales_data)
for c in cat_sales_data:
    c['pct'] = c['gmv'] / total_gmv if total_gmv > 0 else 0

cat_sales_data.sort(key=lambda x: -x['gmv'])
cum = 0
for c in cat_sales_data:
    cum += c['pct']
    c['cum_pct'] = cum
    if cum <= 0.70:
        c['abc'] = 'A'
    elif cum <= 0.90:
        c['abc'] = 'B'
    else:
        c['abc'] = 'C'

for c in cat_sales_data:
    print(f"  {c['abc']}类 | {c['category']:<10} | GMV:{c['gmv']:>10,.0f} | 占比:{c['pct']:.1%} | 累计:{c['cum_pct']:.1%} | 售罄:{c['sellout']:.1%}")

# ========== 5. 721 货品结构 ==========
print('📊 分析 721 货品结构...')
# 按 sub_category 分类估算（用 fit_name 近似）
basic_cats = ['T恤', '衬衫', '裤', '牛仔', '基础', '休闲裤', '牛仔裤']
fashion_cats = ['连衣裙', '裙', '潮流', '时尚', '卫衣', '外套', '毛衫']
image_cats = ['高定', '限量', '礼服', '西装', '套装']

basic_gmv = sum(v for k, v in cat_gmv.items() if any(b in k for b in basic_cats))
fashion_gmv = sum(v for k, v in cat_gmv.items() if any(f in k for f in fashion_cats))
image_gmv = sum(v for k, v in cat_gmv.items() if any(i in k for i in image_cats))
other_gmv = total_gmv - basic_gmv - fashion_gmv - image_gmv

print(f'  基础款 GMV: {basic_gmv:,.0f} ({basic_gmv/total_gmv:.1%})')
print(f'  时尚款 GMV: {fashion_gmv:,.0f} ({fashion_gmv/total_gmv:.1%})')
print(f'  形象款 GMV: {image_gmv:,.0f} ({image_gmv/total_gmv:.1%})')
print(f'  其他 GMV:   {other_gmv:,.0f} ({other_gmv/total_gmv:.1%})')

# ========== 6. RFM 用户分层 ==========
print('📊 计算 RFM 用户分层...')

# 按 member_id 分组
member_stats = defaultdict(lambda: {'amount': 0, 'qty': 0, 'dates': [], 'orders': set()})
for s in year_sales:
    mid = s['member_id']
    if mid and mid.strip():
        member_stats[mid]['amount'] += s['amount']
        member_stats[mid]['qty'] += s['qty']
        member_stats[mid]['dates'].append(s['sale_date'])
        member_stats[mid]['orders'].add(s['order_no'])

print(f'  会员总数: {len(member_stats):,}')

# 计算 R/F/M
ref_date = datetime.strptime('2026-04-21', '%Y-%m-%d')
R_THRESHOLD = 60  # 60天内有消费
F_THRESHOLD = 2   # 2次以上购买
M_THRESHOLD = 1000  # 累计消费1000元

rfm_counts = {
    '111_顶级价值': 0, '110_潜力': 0, '101_重要': 0, '100_新客': 0,
    '011_维护': 0, '010_一般': 0, '001_流失风险': 0, '000_流失': 0
}

for mid, stats in member_stats.items():
    max_date = max(stats['dates']) if stats['dates'] else None
    days_ago = (ref_date - datetime.strptime(str(max_date), '%Y-%m-%d')).days if max_date else 999
    f = len(stats['orders'])
    m = stats['amount']

    r_score = 1 if days_ago <= R_THRESHOLD else 0
    f_score = 1 if f >= F_THRESHOLD else 0
    m_score = 1 if m >= M_THRESHOLD else 0
    code = f'{r_score}{f_score}{m_score}'

    labels = {
        '111': '111_顶级价值', '110': '110_潜力', '101': '101_重要', '100': '100_新客',
        '011': '011_维护', '010': '010_一般', '001': '001_流失风险', '000': '000_流失'
    }
    rfm_counts[labels[code]] += 1

for label, cnt in rfm_counts.items():
    pct_val = cnt / len(member_stats) * 100 if len(member_stats) > 0 else 0
    print(f'  {label:<12}: {cnt:>5,} 人 ({pct_val:.1f}%)')

# 计算各层 GMV 贡献
rfm_gmv = defaultdict(float)
for s in year_sales:
    mid = s['member_id']
    if mid and mid.strip() and mid in member_stats:
        stats = member_stats[mid]
        max_date = max(stats['dates'])
        days_ago = (ref_date - datetime.strptime(str(max_date), '%Y-%m-%d')).days
        f = len(stats['orders'])
        m = stats['amount']
        r_score = 1 if days_ago <= R_THRESHOLD else 0
        f_score = 1 if f >= F_THRESHOLD else 0
        m_score = 1 if m >= M_THRESHOLD else 0
        code = f'{r_score}{f_score}{m_score}'
        labels = {
            '111': '111_顶级价值', '110': '110_潜力', '101': '101_重要', '100': '100_新客',
            '011': '011_维护', '010': '010_一般', '001': '001_流失风险', '000': '000_流失'
        }
        rfm_gmv[labels[code]] += s['amount']

print('\n  RFM 分层 GMV 贡献:')
for label in rfm_counts:
    gmv_val = rfm_gmv[label]
    cnt_val = rfm_counts[label]
    gmv_pct = gmv_val / total_gmv * 100 if total_gmv > 0 else 0
    print(f'  {label:<12}: GMV {gmv_val:>10,.0f} 元 ({gmv_pct:.1f}%) | {cnt_val:>5} 人')

# ========== 7. AIPL 链路分析 ==========
print('📊 分析 AIPL 链路...')
total_members = len(member_stats)
loyal_members = sum(1 for mid, s in member_stats.items()
                    if len(s['orders']) >= 2)  # 2次以上 = 忠诚
repeat_members = sum(1 for mid, s in member_stats.items()
                     if len(s['orders']) >= 1)  # 有购买 = 兴趣+
# 估算：忠诚 = L，重复购买 = P，1次 = I，只浏览未购 = A（无法估算）

A_count = total_members  # 曝光（估算为总注册会员）
I_count = repeat_members  # 兴趣
P_count = repeat_members  # 购买
L_count = loyal_members   # 忠诚

AI_rate = I_count / A_count if A_count > 0 else 0
IP_rate = P_count / I_count if I_count > 0 else 0
PL_rate = L_count / P_count if P_count > 0 else 0

print(f'  A（认知/曝光）: 约 {A_count:,} 人')
print(f'  I（兴趣/购买意向）: 约 {I_count:,} 人 (A→I 转化: {AI_rate:.1%})')
print(f'  P（购买/首购）: 约 {P_count:,} 人 (I→P 转化: {IP_rate:.1%})')
print(f'  L（忠诚/复购）: 约 {L_count:,} 人 (P→L 复购率: {PL_rate:.1%})')

# ========== 8. 波士顿矩阵（按品类） ==========
print('📊 计算波士顿矩阵...')

# 计算同比增长率（用2025同年数据）
last_year_cat_gmv = defaultdict(float)
for s in [x for x in all_sales if str(x['sale_date']).startswith('2025')]:
    last_year_cat_gmv[s['category'] or '未知'] += s['amount']

bcg_data = []
for cat, gm in cat_gmv.items():
    gm_ly = last_year_cat_gmv.get(cat, 0)
    growth = (gm - gm_ly) / gm_ly if gm_ly > 0 else 0
    # 相对市场份额：用总GMV占比估算
    market_share = gm / total_gmv if total_gmv > 0 else 0
    bcg_data.append({
        'category': cat,
        'gmv': gm,
        'growth': growth,
        'share': market_share,
        'type': ''
    })

# 分类阈值
growth_threshold = 0.10  # 10%增长率
share_threshold = 0.15    # 15%市场份额

for b in bcg_data:
    if b['growth'] >= growth_threshold and b['share'] >= share_threshold:
        b['type'] = '⭐ 明星类'
    elif b['growth'] < growth_threshold and b['share'] >= share_threshold:
        b['type'] = '💰 金牛类'
    elif b['growth'] >= growth_threshold and b['share'] < share_threshold:
        b['type'] = '❓ 问题类'
    else:
        b['type'] = '🐕 瘦狗类'

for b in bcg_data:
    print(f"  {b['type']:<8} | {b['category']:<10} | GMV:{b['gmv']:>10,.0f} | 同比:{b['growth']:+.1%} | 份额:{b['share']:.1%}")

# ========== 9. 月度健康度打分 ==========
print('📊 计算月度健康度...')
scores = {}

# 售罄率评分 (满分25)
str_val = sellout_rate
scores['售罄率'] = min(25, str_val / 0.70 * 25) if str_val > 0 else 0

# 折扣率评分 (满分25) — 目标82折
disc_val = discount_rate
scores['折扣率'] = min(25, disc_val / 0.82 * 25) if disc_val > 0 else 0

# 动销率评分 (满分25)
str_sc = str_rate
scores['动销率'] = min(25, str_sc / 0.70 * 25) if str_sc > 0 else 0

# 流转率评分 (满分25) — 目标60天
days_val = inv_turnover_days
scores['流转率'] = min(25, 60 / days_val * 25) if days_val > 0 else 0

total_score = sum(scores.values())
print(f'  售罄率: {scores["售罄率"]:.0f}/25')
print(f'  折扣率: {scores["折扣率"]:.0f}/25')
print(f'  动销率: {scores["动销率"]:.0f}/25')
print(f'  流转率: {scores["流转率"]:.0f}/25')
print(f'  综合健康度: {total_score:.0f}/100')

# ========== 10. 门店分析 ==========
print('📊 门店 GMV 排名...')
for shop, gm in shop_gmv_sorted[:10]:
    print(f'  {shop:<20}: {gm:>12,.0f} 元 ({gm/total_gmv:.1%})')

conn.close()
print('\n✅ 数据分析完成！')
print(f'📄 报告输出至: {OUTPUT_PATH}')
