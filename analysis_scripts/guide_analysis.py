# -*- coding: utf-8 -*-
import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('C:/Users/MacBookPro/cabbeen_data/cabbeen.db')
cur = conn.cursor()

# 更详细的导购分析
sql = '''
SELECT 
    guide_name,
    SUM(qty) as total_qty,
    SUM(amount) as total_gmv,
    COUNT(DISTINCT order_no) as order_count,
    COUNT(DISTINCT member_id) as customer_count,
    COUNT(DISTINCT CASE WHEN is_vip = '1' THEN member_id ELSE NULL END) as vip_customer_count,
    SUM(tag_amount) as total_tag,
    AVG(discount_rate) as avg_discount,
    COUNT(DISTINCT category) as cat_variety,
    COUNT(DISTINCT sub_category) as subcat_variety
FROM sales
WHERE year = 2026
GROUP BY guide_name
ORDER BY total_gmv DESC
LIMIT 15
'''

# VIP订单数（去重订单数，需要单独查询）
vip_order_sql = '''
SELECT 
    guide_name,
    COUNT(DISTINCT order_no) as vip_order_count
FROM sales
WHERE year = 2026 AND is_vip = '1'
GROUP BY guide_name
'''

cur.execute(sql)
rows = cur.fetchall()

# 先查询VIP订单数（去重订单数）
cur.execute(vip_order_sql)
vip_order_rows = {r[0]: r[1] for r in cur.fetchall()}

print('=== 2026年导购能力模型分析 ===')
print()
print('{:<8} {:>6} {:>8} {:>7} {:>7} {:>7} {:>7} {:>8}'.format(
    '姓名', '销量', 'GMV', '连带', '客单价', 'VIP率', '折扣', '品类数'))
print('-' * 75)

all_data = []
for r in rows:
    name, qty, gmv, orders, customers, vip_customers, tag, disc, cat_n, subcat_n = r
    vip_orders = vip_order_rows.get(name, 0)
    # 连带率 = 销量/订单数（件/单，服装行业1.5-2.0正常）
    linkage = qty / orders if orders > 0 else 0
    # 客单价 = GMV/订单数
    avg_price = gmv / orders if orders > 0 else 0
    # VIP率 = VIP订单数/总订单数（会员消费占比，≤100%）
    vip_order_rate = vip_orders / orders * 100 if orders > 0 else 0
    # VIP渗透率 = VIP会员数/总会员数（有会员号的客户中，VIP占比）
    vip_penetration = vip_customers / customers * 100 if customers > 0 else 0
    # 折扣率 = 实收/吊牌
    disc_rate = gmv / tag if tag > 0 else 0
    # 复购率 = 有多次购买的会员/总会员数
    cur.execute('''
        SELECT COUNT(*) FROM (
            SELECT member_id FROM sales 
            WHERE guide_name = ? AND year = 2026 
            GROUP BY member_id HAVING COUNT(*) > 1
        )
    ''', (name,))
    repurchase = cur.fetchone()[0]
    repurchase_rate = repurchase / customers * 100 if customers > 0 else 0
    
    all_data.append({
        'name': name, 'qty': qty, 'gmv': gmv, 'orders': orders,
        'linkage': linkage, 'avg_price': avg_price, 
        'vip_order_rate': vip_order_rate,  # VIP订单占比
        'vip_penetration': vip_penetration,  # VIP渗透率
        'disc_rate': disc_rate, 'cat_n': cat_n, 'subcat_n': subcat_n,
        'repurchase': repurchase, 'repurchase_rate': repurchase_rate,
        'vip_customers': vip_customers, 'vip_orders': vip_orders,
        'customers': customers
    })
    
    print('{:<8} {:>6.0f} {:>8.0f} {:>7.2f} {:>7.0f} {:>7.1f}% {:>6.1f}折 {:>6}'.format(
        name, qty, gmv, linkage, avg_price, vip_order_rate, disc_rate * 10, subcat_n
    ))

# 计算TOP3平均值
top3 = all_data[:3]
avg_top3 = {
    'gmv': sum(d['gmv'] for d in top3) / 3,
    'linkage': sum(d['linkage'] for d in top3) / 3,
    'avg_price': sum(d['avg_price'] for d in top3) / 3,
    'vip_order_rate': sum(d['vip_order_rate'] for d in top3) / 3,
    'vip_penetration': sum(d['vip_penetration'] for d in top3) / 3,
    'disc_rate': sum(d['disc_rate'] for d in top3) / 3,
    'repurchase_rate': sum(d['repurchase_rate'] for d in top3) / 3,
}

# 计算全员平均值
all_avg = {
    'gmv': sum(d['gmv'] for d in all_data) / len(all_data),
    'linkage': sum(d['linkage'] for d in all_data) / len(all_data),
    'avg_price': sum(d['avg_price'] for d in all_data) / len(all_data),
    'vip_order_rate': sum(d['vip_order_rate'] for d in all_data) / len(all_data),
    'vip_penetration': sum(d['vip_penetration'] for d in all_data) / len(all_data),
    'disc_rate': sum(d['disc_rate'] for d in all_data) / len(all_data),
    'repurchase_rate': sum(d['repurchase_rate'] for d in all_data) / len(all_data),
}

print()
print('=== 能力对比 ===')
print('{:<14} {:>10} {:>10} {:>10}'.format('指标', 'TOP3均值', '全员均值', '差距'))
print('-' * 50)
print('{:<14} {:>10.0f} {:>10.0f} {:>+10.0f}'.format('GMV(元)', avg_top3['gmv'], all_avg['gmv'], avg_top3['gmv'] - all_avg['gmv']))
print('{:<14} {:>10.2f} {:>10.2f} {:>+10.2f}'.format('连带率(件/单)', avg_top3['linkage'], all_avg['linkage'], avg_top3['linkage'] - all_avg['linkage']))
print('{:<14} {:>10.0f} {:>10.0f} {:>+10.0f}'.format('客单价(元)', avg_top3['avg_price'], all_avg['avg_price'], avg_top3['avg_price'] - all_avg['avg_price']))
print('{:<14} {:>10.1f}% {:>10.1f}% {:>+10.1f}%'.format('VIP订单率', avg_top3['vip_order_rate'], all_avg['vip_order_rate'], avg_top3['vip_order_rate'] - all_avg['vip_order_rate']))
print('{:<14} {:>10.1f}% {:>10.1f}% {:>+10.1f}%'.format('VIP渗透率', avg_top3['vip_penetration'], all_avg['vip_penetration'], avg_top3['vip_penetration'] - all_avg['vip_penetration']))
print('{:<14} {:>10.1f}折 {:>10.1f}折 {:>+10.1f}折'.format('折扣率', avg_top3['disc_rate']*10, all_avg['disc_rate']*10, (avg_top3['disc_rate'] - all_avg['disc_rate'])*10))
print('{:<14} {:>10.1f}% {:>10.1f}% {:>+10.1f}%'.format('复购率', avg_top3['repurchase_rate'], all_avg['repurchase_rate'], avg_top3['repurchase_rate'] - all_avg['repurchase_rate']))

# 保存数据供后续分析
print()
print('=== TOP3详细分析 ===')
for i, d in enumerate(top3, 1):
    print(f'\n第{i}名: {d["name"]}')
    print(f'  GMV: {d["gmv"]:.0f}元')
    print(f'  连带率: {d["linkage"]:.2f}件/单')
    print(f'  客单价: {d["avg_price"]:.0f}元')
    print(f'  VIP订单率: {d["vip_order_rate"]:.1f}%（VIP订单{d["vip_orders"]:.0f}笔/总订单{d["orders"]:.0f}笔）')
    print(f'  VIP渗透率: {d["vip_penetration"]:.1f}%（VIP会员{d["vip_customers"]:.0f}人/会员总数{d["customers"]:.0f}人）')
    print(f'  折扣率: {d["disc_rate"]*10:.1f}折')
    print(f'  复购率: {d["repurchase_rate"]:.1f}%')
    print(f'  品类宽度: {d["subcat_n"]}个品类')
