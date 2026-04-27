# -*- coding: utf-8 -*-
"""
近30天导购深度分析（含VIP维度）
时间范围：2026-03-23 ~ 2026-04-22
"""
import sqlite3, sys, io, json

# 强制UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB = r"C:\Users\MacBookPro\cabbeen_data\cabbeen.db"
START_DATE = "2026-03-23"
END_DATE = "2026-04-22"

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def fetchall(sql, params=()):
    cur = get_conn().cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    return [dict(r) for r in rows]  # 转换为dict

def fetchone(sql, params=()):
    cur = get_conn().cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    return dict(row) if row else None

def pct(a, b):
    return round(a / b * 100, 1) if b else 0.0

def avg(a, b):
    return round(a / b, 1) if b else 0.0

# ============================================================
# 1. 基础指标（近30天）
# ============================================================
base_sql = """
SELECT
    guide_name,
    SUM(qty)                              AS total_qty,
    SUM(amount)                            AS total_gmv,
    SUM(tag_amount)                        AS total_tag,
    COUNT(DISTINCT order_no)               AS total_orders,
    COUNT(DISTINCT member_id)               AS total_members,
    COUNT(DISTINCT category)                AS cat_count
FROM sales
WHERE date(sale_date) BETWEEN ? AND ?
GROUP BY guide_name
ORDER BY total_gmv DESC
"""
rows = fetchall(base_sql, (START_DATE, END_DATE))

# ============================================================
# 2. VIP订单（去重order_no）
# ============================================================
vip_order_sql = """
SELECT guide_name, 
       COUNT(DISTINCT order_no) AS vip_orders,
       SUM(qty) AS vip_qty,
       SUM(amount) AS vip_gmv
FROM sales
WHERE date(sale_date) BETWEEN ? AND ? 
  AND member_id IS NOT NULL AND member_id != ''
GROUP BY guide_name
"""
vip_map = {r["guide_name"]: r for r in fetchall(vip_order_sql, (START_DATE, END_DATE))}

# ============================================================
# 3. 复购会员（有多笔订单的VIP）
# ============================================================
repurchase_sql = """
SELECT guide_name, COUNT(*) AS repurchase_members
FROM (
    SELECT guide_name, member_id
    FROM sales
    WHERE date(sale_date) BETWEEN ? AND ? 
      AND member_id IS NOT NULL AND member_id != ''
    GROUP BY guide_name, member_id
    HAVING COUNT(DISTINCT order_no) > 1
)
GROUP BY guide_name
"""
repurchase_map = {r["guide_name"]: r["repurchase_members"] for r in fetchall(repurchase_sql, (START_DATE, END_DATE))}

# ============================================================
# 4. 新VIP会员（首次购买时间在近30天内）
# ============================================================
new_vip_sql = """
SELECT s.guide_name, COUNT(DISTINCT s.member_id) AS new_vip_count
FROM sales s
WHERE date(s.sale_date) BETWEEN ? AND ?
  AND s.member_id IS NOT NULL AND s.member_id != ''
  AND s.member_id NOT IN (
      SELECT member_id FROM sales 
      WHERE date(sale_date) < ?
        AND member_id IS NOT NULL AND member_id != ''
  )
GROUP BY s.guide_name
"""
new_vip_map = {r["guide_name"]: r["new_vip_count"] for r in fetchall(new_vip_sql, (START_DATE, END_DATE, START_DATE))}

# ============================================================
# 5. VIP GMV / 新客GMV
# ============================================================
vip_gmv_sql = """
SELECT guide_name, 
       SUM(CASE WHEN member_id IS NOT NULL AND member_id != '' THEN amount ELSE 0 END) AS vip_gmv,
       SUM(CASE WHEN member_id IS NULL OR member_id = '' THEN amount ELSE 0 END) AS new_gmv
FROM sales
WHERE date(sale_date) BETWEEN ? AND ?
GROUP BY guide_name
"""
gmv_map = {r["guide_name"]: r for r in fetchall(vip_gmv_sql, (START_DATE, END_DATE))}

# ============================================================
# 6. VIP多件订单
# ============================================================
vip_multi_sql = """
SELECT guide_name, 
       COUNT(DISTINCT CASE WHEN vip_order=1 THEN order_no END) AS total_vip_orders,
       COUNT(DISTINCT CASE WHEN vip_order=1 AND multi_item=1 THEN order_no END) AS vip_multi_orders
FROM (
    SELECT guide_name, order_no,
           CASE WHEN member_id IS NOT NULL AND member_id != '' THEN 1 ELSE 0 END AS vip_order,
           CASE WHEN qty > 1 THEN 1 ELSE 0 END AS multi_item
    FROM sales
    WHERE date(sale_date) BETWEEN ? AND ?
)
GROUP BY guide_name
"""
vip_multi_map = {r["guide_name"]: r for r in fetchall(vip_multi_sql, (START_DATE, END_DATE))}

# ============================================================
# 7. SKU分散度（使用style_code）
# ============================================================
sku_disp_sql = """
SELECT guide_name, style_code, SUM(qty) AS sku_qty
FROM sales
WHERE date(sale_date) BETWEEN ? AND ?
  AND style_code IS NOT NULL AND style_code != ''
GROUP BY guide_name, style_code
"""
sku_raw = fetchall(sku_disp_sql, (START_DATE, END_DATE))

# 手动计算
sku_data = {}
for r in sku_raw:
    gn = r["guide_name"]
    if gn not in sku_data:
        sku_data[gn] = {"sku_count": 0, "total_qty": 0, "top1_qty": 0}
    sku_data[gn]["sku_count"] += 1
    sku_data[gn]["total_qty"] += r["sku_qty"]
    if r["sku_qty"] > sku_data[gn]["top1_qty"]:
        sku_data[gn]["top1_qty"] = r["sku_qty"]
sku_map = sku_data

# ============================================================
# 8. 高价商品占比（吊牌价>800）
# ============================================================
high_price_sql = """
SELECT guide_name,
       SUM(amount) AS total_gmv,
       SUM(CASE WHEN tag_price > 800 THEN amount ELSE 0 END) AS high_price_gmv
FROM sales
WHERE date(sale_date) BETWEEN ? AND ?
GROUP BY guide_name
"""
price_map = {r["guide_name"]: r for r in fetchall(high_price_sql, (START_DATE, END_DATE))}

# ============================================================
# 9. 非VIP分析
# ============================================================
non_vip_sql = """
SELECT guide_name, 
       COUNT(DISTINCT order_no) AS non_vip_orders,
       SUM(qty) AS non_vip_qty,
       SUM(amount) AS non_vip_gmv
FROM sales
WHERE date(sale_date) BETWEEN ? AND ?
  AND (member_id IS NULL OR member_id = '')
GROUP BY guide_name
"""
non_vip_map = {r["guide_name"]: r for r in fetchall(non_vip_sql, (START_DATE, END_DATE))}

# ============================================================
# 计算指标
# ============================================================
all_data = []
for r in rows:
    name     = r["guide_name"]
    qty      = r["total_qty"] or 0
    gmv      = r["total_gmv"] or 0
    tag      = r["total_tag"] or 0
    orders   = r["total_orders"] or 0
    members  = r["total_members"] or 0
    cats     = r["cat_count"] or 0

    vm       = vip_map.get(name, {})
    vip_orders = vm.get("vip_orders", 0) or 0
    vip_qty    = vm.get("vip_qty", 0) or 0
    vip_gmv_v  = vm.get("vip_gmv", 0) or 0
    rep_mem    = repurchase_map.get(name, 0) or 0
    new_vip    = new_vip_map.get(name, 0) or 0
    gm         = gmv_map.get(name, {})
    new_cust_gmv = gm.get("new_gmv", 0) or 0
    vmm        = vip_multi_map.get(name, {})
    vip_multi  = vmm.get("vip_multi_orders", 0) or 0
    sm         = sku_map.get(name, {})
    sku_count  = sm.get("sku_count", 0) or 0
    top1_qty   = sm.get("top1_qty", 0) or 0
    ppm        = price_map.get(name, {})
    high_gmv   = ppm.get("high_price_gmv", 0) or 0
    nvm        = non_vip_map.get(name, {})
    non_vip_orders = nvm.get("non_vip_orders", 0) or 0
    non_vip_qty = nvm.get("non_vip_qty", 0) or 0
    non_vip_gmv = nvm.get("non_vip_gmv", 0) or 0

    # 基础指标
    linkage      = round(qty / orders, 2) if orders > 0 else 0
    avg_price    = round(gmv / orders, 0) if orders > 0 else 0
    overall_disc = round(gmv / tag * 10, 1) if tag > 0 else 0

    # VIP指标
    vip_rate      = pct(vip_orders, orders)                    
    vip_gmv_rate  = pct(vip_gmv_v, gmv)                        
    vip_linkage   = round(vip_qty / vip_orders, 2) if vip_orders > 0 else 0
    vip_avg_price = round(vip_gmv_v / vip_orders, 0) if vip_orders > 0 else 0
    repurchase_rate = pct(rep_mem, members)                    
    new_vip_rate  = pct(new_vip, members)                      
    new_cust_rate = pct(new_cust_gmv, gmv)                     
    vip_multi_rate = pct(vip_multi, vip_orders)                

    # 非VIP指标
    non_vip_linkage = round(non_vip_qty / non_vip_orders, 2) if non_vip_orders > 0 else 0
    non_vip_avg_price = round(non_vip_gmv / non_vip_orders, 0) if non_vip_orders > 0 else 0
    vip_vs_nonvip_diff = vip_avg_price - non_vip_avg_price

    # SKU分散度
    sku_disp = round(top1_qty / qty * 100, 1) if qty > 0 else 0

    # 高价商品
    high_price_rate = pct(high_gmv, gmv)

    all_data.append({
        "name": name,
        "gmv": gmv, "qty": qty, "orders": orders, "members": members, "cats": cats,
        "linkage": linkage, "avg_price": avg_price, "overall_disc": overall_disc,
        "vip_orders": vip_orders, "vip_rate": vip_rate,
        "vip_gmv": vip_gmv_v, "vip_gmv_rate": vip_gmv_rate,
        "vip_linkage": vip_linkage, "vip_avg_price": vip_avg_price,
        "rep_mem": rep_mem, "repurchase_rate": repurchase_rate,
        "new_vip": new_vip, "new_vip_rate": new_vip_rate,
        "new_cust_gmv": new_cust_gmv, "new_cust_rate": new_cust_rate,
        "vip_multi": vip_multi, "vip_multi_rate": vip_multi_rate,
        "sku_count": sku_count, "sku_disp": sku_disp,
        "high_gmv": high_gmv, "high_price_rate": high_price_rate,
        "non_vip_orders": non_vip_orders, "non_vip_rate": pct(non_vip_orders, orders),
        "non_vip_linkage": non_vip_linkage, "non_vip_avg_price": non_vip_avg_price,
        "vip_vs_nonvip_diff": vip_vs_nonvip_diff,
    })

# 按GMV排序
all_data.sort(key=lambda x: x["gmv"], reverse=True)

# ============================================================
# 计算全员和TOP3均值
# ============================================================
def calc_avg(data_list, keys):
    return {k: sum(d[k] for d in data_list) / len(data_list) for k in keys}

all_keys = ["vip_rate", "vip_gmv_rate", "vip_avg_price", "vip_linkage", 
            "repurchase_rate", "new_vip_rate", "vip_multi_rate",
            "sku_disp", "high_price_rate", "non_vip_rate",
            "vip_vs_nonvip_diff"]

avg_all = calc_avg(all_data, all_keys)
top3 = all_data[:3] if len(all_data) >= 3 else all_data
avg_top3 = calc_avg(top3, all_keys)

# ============================================================
# 导出结果
# ============================================================
result = {
    "period": f"{START_DATE} ~ {END_DATE}",
    "all_data": all_data,
    "top3": top3,
    "avg_all": avg_all,
    "avg_top3": avg_top3,
}

output_path = r"c:\Users\MacBookPro\Fashion Doctor\guide_30day_result.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"OK: {output_path}")
print(f"共 {len(all_data)} 名导购，近30天 {sum(d['orders'] for d in all_data)} 笔订单，GMV {sum(d['gmv'] for d in all_data):,.0f} 元")
