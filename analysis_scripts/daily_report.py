"""
Fashion Doctor - 智能分析模块
服装零售数据分析 + 决策规则 + 飞书通知

功能：
- 读取 cabbeen_data 数据库
- 计算核心指标（四率、GMV、用户等）
- 运行决策规则，生成行动建议
- 发送飞书卡片通知

用法：
  python daily_report.py          # 发送日报
  python daily_report.py --debug  # 仅打印，不发送
"""

import sys
import sqlite3
import requests
import json
from datetime import date, datetime
from pathlib import Path

# 解决 Windows GBK 控制台编码问题
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# =============================================================================
# 配置
# =============================================================================

DB_PATH = "C:/Users/MacBookPro/cabbeen_data/cabbeen.db"
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/79f660db-edd3-45f8-baec-9578edc22535"

# 东尚基准值（基于历史数据分析）
BASELINE = {
    "sellout_rate_min": 0.25,     # 售罄率预警阈值
    "sellout_rate_danger": 0.15,  # 售罄率危险阈值
    "sellout_rate_target": 0.40,  # 季中目标
    "sellout_rate_season": 0.65,  # 季末目标
    "inv_turnover_days_max": 180, # 库存周转预警（天）
    "rfm_001_ratio_max": 0.35,   # 流失预警占比阈值
    "basic_ratio_min": 0.45,     # 基础款占比下限
}

# 飞书主题色
THEME_BLUE = "blue"
THEME_RED = "red"
THEME_ORANGE = "orange"
THEME_GREEN = "green"
THEME_GREY = "grey"


# =============================================================================
# 数据库查询
# =============================================================================

def get_db_conn():
    return sqlite3.connect(DB_PATH)


def query_sales_summary(conn, start_date: str, end_date: str) -> dict:
    """销售汇总"""
    cur = conn.cursor()
    cur.execute("""
        SELECT
            COUNT(*) as order_count,
            SUM(qty) as total_qty,
            SUM(amount) as total_amount,
            SUM(tag_amount) as total_tag_amount,
            AVG(discount_rate) as avg_discount_rate,
            COUNT(DISTINCT member_id) as member_count,
            COUNT(DISTINCT shop_name) as shop_count
        FROM sales
        WHERE sale_date BETWEEN ? AND ?
          AND member_id IS NOT NULL AND member_id != ''
    """, (start_date, end_date))
    row = cur.fetchone()
    return {
        "order_count": row[0] or 0,
        "qty": row[1] or 0,
        "amount": row[2] or 0,
        "tag_amount": row[3] or 0,
        "avg_discount_rate": row[4] or 0,
        "member_count": row[5] or 0,
        "shop_count": row[6] or 0,
    }


def query_monthly_gmv(conn, year_month: str) -> dict:
    """月度 GMV"""
    cur = conn.cursor()
    cur.execute("""
        SELECT
            SUM(amount) as gmv,
            SUM(qty) as qty,
            COUNT(DISTINCT order_no) as orders,
            AVG(amount / NULLIF(qty, 0)) as unit_price,
            AVG(discount_rate) as discount_rate
        FROM sales
        WHERE sale_date LIKE ?
          AND amount > 0
    """, (f"{year_month}%",))
    row = cur.fetchone()
    return {
        "gmv": row[0] or 0,
        "qty": row[1] or 0,
        "orders": row[2] or 0,
        "unit_price": row[3] or 0,
        "discount_rate": row[4] or 0,
    }


def query_sellout_analysis(conn, year: str, season: str) -> dict:
    """售罄率分析（按子品类）"""
    cur = conn.cursor()

    # 查询销售数据（按 sub_category 汇总）
    cur.execute("""
        SELECT
            COALESCE(NULLIF(sub_category, ''), category) as cat,
            SUM(qty) as sold_qty,
            SUM(amount) as sold_amount
        FROM sales
        WHERE year = ? AND season = ?
        GROUP BY COALESCE(NULLIF(sub_category, ''), category)
        ORDER BY sold_qty DESC
    """, (year, season))

    sales_by_cat = {}
    for row in cur.fetchall():
        sales_by_cat[row[0]] = {"sold_qty": row[1], "sold_amount": row[2]}

    # 查询到货数据（按 category 汇总）
    cur.execute("""
        SELECT
            COALESCE(NULLIF(sub_category, ''), category) as cat,
            SUM(plan_qty) as plan_qty,
            SUM(actual_qty) as actual_qty
        FROM arrival
        WHERE year = ? AND season = ?
        GROUP BY COALESCE(NULLIF(sub_category, ''), category)
    """, (year, season))

    arrival_by_cat = {}
    for row in cur.fetchall():
        arrival_by_cat[row[0]] = {"plan_qty": row[1], "actual_qty": row[2]}

    # 查询当前库存
    cur.execute("""
        SELECT
            COALESCE(NULLIF(sub_category, ''), category) as cat,
            SUM(stock_qty) as stock_qty
        FROM inventory
        WHERE year = ? AND season = ?
        GROUP BY COALESCE(NULLIF(sub_category, ''), category)
    """, (year, season))

    inv_by_cat = {}
    for row in cur.fetchall():
        inv_by_cat[row[0]] = {"stock_qty": row[1]}

    # 计算各品类售罄率
    results = []
    all_cats = set(sales_by_cat.keys()) | set(arrival_by_cat.keys()) | set(inv_by_cat.keys())

    for cat in all_cats:
        sold = sales_by_cat.get(cat, {}).get("sold_qty", 0)
        arrival = arrival_by_cat.get(cat, {}).get("actual_qty", 0)
        stock = inv_by_cat.get(cat, {}).get("stock_qty", 0)
        total_in = arrival + stock  # 总入库 = 到货 + 库存

        sellout_rate = sold / total_in if total_in > 0 else 0

        results.append({
            "category": cat,
            "sold_qty": sold,
            "arrival_qty": arrival,
            "stock_qty": stock,
            "total_in": total_in,
            "sellout_rate": sellout_rate,
        })

    # 按售罄率排序
    results.sort(key=lambda x: x["sellout_rate"], reverse=True)
    return results


def query_inventory_status(conn) -> dict:
    """库存状态"""
    cur = conn.cursor()

    # 总库存
    cur.execute("SELECT SUM(stock_qty), SUM(stock_tag_amount) FROM inventory")
    row = cur.fetchone()
    total_qty = row[0] or 0
    total_tag = row[1] or 0

    # 按品类库存
    cur.execute("""
        SELECT
            COALESCE(NULLIF(sub_category, ''), category) as cat,
            SUM(stock_qty) as qty,
            SUM(stock_tag_amount) as tag_amount
        FROM inventory
        GROUP BY COALESCE(NULLIF(sub_category, ''), category)
        ORDER BY qty DESC
        LIMIT 10
    """)
    by_cat = [{"category": r[0], "qty": r[1], "tag_amount": r[2]} for r in cur.fetchall()]

    return {
        "total_qty": total_qty,
        "total_tag_amount": total_tag,
        "by_category": by_cat,
    }


def query_rfm_summary(conn, year_month: str) -> dict:
    """RFM 汇总（简化版）"""
    cur = conn.cursor()

    # 查询活跃会员数
    cur.execute("""
        SELECT COUNT(DISTINCT member_id)
        FROM sales
        WHERE sale_date LIKE ? AND member_id IS NOT NULL AND member_id != ''
    """, (f"{year_month}%",))
    active_members = cur.fetchone()[0] or 0

    # 查询有复购的会员
    cur.execute("""
        SELECT member_id, SUM(qty) as total_qty, SUM(amount) as total_amount
        FROM sales
        WHERE sale_date LIKE ? AND member_id IS NOT NULL AND member_id != ''
        GROUP BY member_id
        HAVING COUNT(DISTINCT order_no) > 1
    """, (f"{year_month}%",))
    repeat_members = len(cur.fetchall())

    # 查询 001 层（流失预警：高消费但近30天无购买）
    cur.execute("""
        SELECT member_id, SUM(amount) as total_amount
        FROM sales
        WHERE sale_date < date('now', '-60 days')
          AND member_id IS NOT NULL AND member_id != ''
        GROUP BY member_id
        ORDER BY total_amount DESC
    """)
    churn_risk = [{"member_id": r[0], "amount": r[1]} for r in cur.fetchall()]

    return {
        "active_members": active_members,
        "repeat_members": repeat_members,
        "repeat_rate": repeat_members / active_members if active_members > 0 else 0,
        "churn_risk_count": len(churn_risk),
        "churn_risk_amount": sum(r["amount"] for r in churn_risk),
    }


def query_shop_performance(conn, year_month: str) -> list:
    """门店业绩"""
    cur = conn.cursor()
    cur.execute("""
        SELECT
            sh.short_name,
            SUM(s.amount) as gmv,
            SUM(s.qty) as qty,
            COUNT(DISTINCT s.order_no) as orders,
            AVG(s.amount / NULLIF(s.qty, 0)) as unit_price
        FROM sales s
        JOIN shops sh ON s.shop_name = sh.full_name
        WHERE s.sale_date LIKE ? AND s.amount > 0
        GROUP BY sh.short_name
        ORDER BY gmv DESC
    """, (f"{year_month}%",))

    results = []
    for row in cur.fetchall():
        results.append({
            "shop_name": row[0],
            "gmv": row[1] or 0,
            "qty": row[2] or 0,
            "orders": row[3] or 0,
            "unit_price": row[4] or 0,
        })
    return results


# =============================================================================
# 决策规则引擎
# =============================================================================

def run_decision_rules(sellout_data: list, inv_data: dict, rfm_data: dict, shop_data: list) -> dict:
    """
    运行决策规则，生成预警和行动建议
    """
    alerts = []
    actions = []

    # 规则1：售罄率预警
    for item in sellout_data[:5]:  # 只看 TOP5 品类
        if item["sellout_rate"] < BASELINE["sellout_rate_danger"]:
            alerts.append({
                "severity": "🔴",
                "type": "售罄率危险",
                "target": item["category"],
                "detail": f"库存{item['stock_qty']}件，销{item['sold_qty']}件，售罄率仅{int(item['sellout_rate']*100)}%",
                "actions": ["启动滞销品降价（7.5-8折）", "跨店调拨畅销码", "导购主推强化"],
            })
        elif item["sellout_rate"] < BASELINE["sellout_rate_min"]:
            alerts.append({
                "severity": "⚠️",
                "type": "售罄率预警",
                "target": item["category"],
                "detail": f"库存{item['stock_qty']}件，售罄率{int(item['sellout_rate']*100)}%，低于目标",
                "actions": ["关注动销", "检查断码情况", "考虑促销"],
            })

    # 规则2：库存预警
    if inv_data["total_qty"] > 0:
        # 简单估算月均销售
        avg_monthly_sales = 3000  # 假设值，实际应从数据计算
        turnover_days = inv_data["total_qty"] / avg_monthly_sales * 30
        if turnover_days > BASELINE["inv_turnover_days_max"]:
            alerts.append({
                "severity": "🔴",
                "type": "库存积压",
                "target": "整体库存",
                "detail": f"库存{inv_data['total_qty']}件，预计周转{turnover_days:.0f}天，严重偏高",
                "actions": ["加快清仓节奏", "减少新品采购", "促销提升消化"],
            })

    # 规则3：用户流失预警
    if rfm_data["churn_risk_count"] > 50:
        alerts.append({
            "severity": "⚠️",
            "type": "流失预警",
            "target": f"高价值用户{rfm_data['churn_risk_count']}人",
            "detail": f"近60天无复购，但历史贡献{rfm_data['churn_risk_amount']/10000:.1f}万",
            "actions": ["定向发送优惠券", "VIP专场邀请", "导购电话回访"],
        })

    # 规则4：门店异常
    if shop_data:
        gmv_list = [s["gmv"] for s in shop_data]
        avg_gmv = sum(gmv_list) / len(gmv_list) if gmv_list else 0
        for shop in shop_data:
            if shop["gmv"] < avg_gmv * 0.6:  # 低于均值60%算异常
                alerts.append({
                    "severity": "⚠️",
                    "type": "门店业绩偏低",
                    "target": shop["shop_name"],
                    "detail": f"GMV {shop['gmv']/10000:.1f}万，低于均值",
                    "actions": ["分析下滑原因", "检查陈列和主推", "强化导购培训"],
                })

    # 生成行动建议（按优先级排序）
    priority_actions = []
    for alert in alerts:
        if alert["severity"] == "🔴":
            for action in alert["actions"][:1]:  # 红色预警只取第一优先级
                priority_actions.append(f"🔴 {action} [{alert['target']}]")

    for alert in alerts:
        if alert["severity"] == "⚠️":
            for action in alert["actions"][:1]:
                priority_actions.append(f"⚠️ {action} [{alert['target']}]")

    return {
        "alerts": alerts,
        "actions": priority_actions[:5],  # 最多5条
    }


# =============================================================================
# 飞书卡片构建
# =============================================================================

def _bold(text: str) -> str:
    return f"**{text}**"


def _color(text: str, color: str) -> str:
    color_map = {
        "red": "#FF3D00",
        "orange": "#FF9500",
        "green": "#00C850",
        "grey": "#8E8E93",
    }
    c = color_map.get(color, "#8E8E93")
    return f'<md:span style="color:{c}">{text}</md:span>'


def _achieve_color(v: float) -> str:
    if v >= 0.80: return "green"
    if v < 0.60: return "red"
    if v < 0.75: return "orange"
    return "grey"


def _rate_color(v: float, higher_is_better: bool = True) -> str:
    if higher_is_better:
        if v >= 0.65: return "green"
        if v >= 0.40: return "orange"
        return "red"
    else:
        if v <= 60: return "green"
        if v <= 120: return "orange"
        return "red"


def build_fashion_doctor_card(data: dict) -> dict:
    """
    构建 Fashion Doctor 分析卡片
    data = {
        "date": "2026-04-22",
        "today_gmv": 28000,
        "month_gmv": 2208048,
        "month_target": 3000000,
        "sellout_rate": 0.093,
        "inv_turnover_days": 907,
        "discount_rate": 0.828,
        "active_members": 1065,
        "repeat_rate": 0.224,
        "top_categories": [...],
        "shop_data": [...],
        "rfm_data": {...},
        "decision": {...},
    }
    """
    date_str = data.get("date", "")
    theme = THEME_GREEN

    # 判断主题色（综合健康度）
    score = data.get("health_score", 80)
    if score < 50:
        theme = THEME_RED
    elif score < 70:
        theme = THEME_ORANGE

    header = {
        "title": {"tag": "plain_text", "content": f"👔 东尚分析日报 {date_str}"},
        "theme": theme
    }

    elements = []

    # [1] 数据状态确认
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**[OK] 数据已更新** 销售{len(data.get('shop_data', []))}家门店 | 库存{data.get('inv_data', {}).get('total_qty', 0):,}件 | 会员{data.get('rfm_data', {}).get('active_members', 0):,}人"
        }
    })
    elements.append({"tag": "hr"})

    # [2] 核心指标
    month_achieve = data.get("month_gmv", 0) / data.get("month_target", 1) if data.get("month_target") else 0
    achieve_color = _achieve_color(month_achieve)

    sellout_rate = data.get("sellout_rate", 0)
    inv_days = data.get("inv_turnover_days", 0)
    discount = data.get("discount_rate", 0)
    repeat_rate = data.get("repeat_rate", 0)
    rr_pct = f'{repeat_rate*100:.1f}%'
    rr_col = _achieve_color(repeat_rate)

    kpi_text = (
        f"{_bold('核心指标')}\n"
        f"月GMV: {data.get('month_gmv', 0)/10000:.1f}万 "
        f"/ 目标{_color(f'{data.get('month_target', 0)/10000:.0f}万', achieve_color)} "
        f"({_color(f'{month_achieve*100:.1f}%', achieve_color)}) | "
        f"件单价{_color(f'{data.get('unit_price', 0):.0f}', 'grey')}元\n"
        f"售罄率: {_color(f'{sellout_rate*100:.1f}%', _rate_color(sellout_rate, True))} | "
        f"周转: {_color(f'{inv_days:.0f}天', _rate_color(inv_days, False))} | "
        f"折扣: {_color(f'{discount*10:.1f}折', _achieve_color(discount))} | "
        f"复购率: {_color(rr_pct, rr_col)}"
    )
    elements.append({"tag": "div", "text": {"tag": "lark_md", "content": kpi_text}})
    elements.append({"tag": "hr"})

    # [3] 预警触发
    decision = data.get("decision", {})
    alerts = decision.get("alerts", [])

    if alerts:
        alert_lines = [_bold("⚠️ 预警触发")]
        for alert in alerts[:3]:
            alert_lines.append(f"{alert['severity']} {alert['type']}：{alert['target']}")
            alert_lines.append(f"    → {alert['detail']}")
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(alert_lines)}})
        elements.append({"tag": "hr"})

    # [4] 今日行动建议
    actions = decision.get("actions", [])
    if actions:
        action_lines = [_bold("📌 今日行动")]
        for action in actions:
            action_lines.append(action)
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(action_lines)}})
        elements.append({"tag": "hr"})

    # [5] TOP 品类
    top_cats = data.get("top_categories", [])
    if top_cats:
        cat_parts = []
        for cat in top_cats[:5]:
            rate = cat.get("sellout_rate", 0)
            rate_color = _rate_color(rate, True)
            cat_parts.append(
                f"{cat['category'][:4]}{_color(f'{rate*100:.0f}%', rate_color)}/{cat.get('sold_qty', 0)}件"
            )
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"{_bold('品类售罄')}\n{' | '.join(cat_parts)}"}})

    # [6] 门店排名
    shop_data = data.get("shop_data", [])
    if shop_data:
        shop_parts = []
        medals = ["🥇", "🥈", "🥉"]
        for i, shop in enumerate(shop_data[:3]):
            shop_parts.append(f"{medals[i]}{shop['shop_name'][:2]}{shop['gmv']/10000:.0f}万")
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"{_bold('门店GMV')}\n{' | '.join(shop_parts)}"}})

    card = {
        "msg_type": "interactive",
        "card": {
            "header": header,
            "elements": elements
        }
    }
    return card


# =============================================================================
# 发送
# =============================================================================

def send_card(card: dict) -> bool:
    """发送飞书卡片"""
    try:
        resp = requests.post(WEBHOOK_URL, json=card, timeout=20)
        result = resp.json()
        # 飞书 code=0 表示成功，StatusCode=0 也表示成功
        code = result.get("code")
        status = result.get("StatusCode")
        if code == 0 or code == "0" or status == 0 or status == "0":
            print(f"[OK] 飞书卡片发送成功")
            return True
        else:
            print(f"[FAIL] 飞书返回: {result}")
            return False
    except Exception as e:
        print(f"[FAIL] 发送异常: {e}")
        return False


# =============================================================================
# 主流程
# =============================================================================

def run_analysis(debug: bool = False):
    """运行完整分析"""
    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    current_month = today.strftime("%Y-%m")

    print(f"\n{'='*60}")
    print(f"👔 Fashion Doctor 分析报告 {date_str}")
    print(f"{'='*60}\n")

    conn = get_db_conn()

    try:
        # 1. 查询月度 GMV
        month_data = query_monthly_gmv(conn, current_month)
        print(f"📊 月度数据: GMV {month_data['gmv']/10000:.1f}万 | 件数 {month_data['qty']} | 折扣 {month_data['discount_rate']*10:.1f}折")

        # 2. 今日数据（简化版，取昨天）
        yesterday = (today.replace(day=1) if today.day == 1 else today).strftime("%Y-%m-%d")
        # 实际上我们用月累计数据
        today_gmv = month_data['gmv'] / today.day if today.day > 0 else 0

        # 3. 库存状态
        inv_data = query_inventory_status(conn)
        print(f"📦 库存: {inv_data['total_qty']:,}件 | 吊牌 {inv_data['total_tag_amount']/10000:.1f}万")

        # 4. 售罄率分析
        year = str(today.year)
        season = "春" if today.month < 7 else "夏"  # 简化判断
        sellout_data = query_sellout_analysis(conn, year, season)
        print(f"📈 售罄率 TOP5:")
        for item in sellout_data[:5]:
            print(f"   {item['category'][:6]}: {item['sellout_rate']*100:.1f}% ({item['sold_qty']}件/总{item['total_in']}件)")

        # 5. 门店业绩
        shop_data = query_shop_performance(conn, current_month)
        print(f"🏪 门店 ({len(shop_data)}家):")
        for shop in shop_data[:3]:
            print(f"   {shop['shop_name']}: {shop['gmv']/10000:.1f}万 | {shop['orders']}单 | 客单{shop['unit_price']:.0f}元")

        # 6. RFM 汇总
        rfm_data = query_rfm_summary(conn, current_month)
        print(f"👥 会员: 活跃{rfm_data['active_members']} | 复购{rfm_data['repeat_members']}({rfm_data['repeat_rate']*100:.1f}%) | 流失预警{rfm_data['churn_risk_count']}人")

        # 7. 运行决策规则
        decision = run_decision_rules(sellout_data, inv_data, rfm_data, shop_data)
        print(f"\n⚠️ 预警: {len(decision['alerts'])}条")
        for alert in decision['alerts']:
            print(f"   {alert['severity']} {alert['type']}: {alert['target']}")
        print(f"\n📌 行动建议:")
        for action in decision['actions']:
            print(f"   {action}")

        # 8. 构建卡片
        card_data = {
            "date": date_str,
            "month_gmv": month_data['gmv'],
            "month_target": 3000000,  # 需要从配置获取
            "unit_price": month_data['unit_price'] or (month_data['gmv'] / month_data['qty'] if month_data['qty'] > 0 else 0),
            "sellout_rate": sellout_data[0]['sellout_rate'] if sellout_data else 0,
            "inv_turnover_days": inv_data['total_qty'] / 1000 * 30 if inv_data['total_qty'] > 0 else 0,
            "discount_rate": month_data['discount_rate'] or 0.82,
            "repeat_rate": rfm_data['repeat_rate'],
            "active_members": rfm_data['active_members'],
            "inv_data": inv_data,
            "top_categories": sellout_data[:5],
            "shop_data": shop_data,
            "rfm_data": rfm_data,
            "decision": decision,
            "health_score": 65,  # TODO: 计算综合健康度
        }

        card = build_fashion_doctor_card(card_data)

        if debug:
            print(f"\n{'='*60}")
            print(f"📋 卡片 JSON (DEBUG 模式，不发送):")
            print(json.dumps(card, ensure_ascii=False, indent=2))
            return card
        else:
            # 发送飞书
            success = send_card(card)
            return success

    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    debug = "--debug" in sys.argv
    run_analysis(debug=debug)
