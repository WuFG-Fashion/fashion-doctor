# -*- coding: utf-8 -*-
"""
明星导购能力分析 - 决策建议+行动指南版
=====================================

核心功能：
1. 双模式输出（brief/full）
2. 决策建议 - 针对不同时间维度
3. 行动指南 - 针对店铺/导购的个性化建议

使用方式：
    from 明星导购分析 import StarGuideAnalyzer, print_decision_guide
    
    # 完整报告+决策建议
    analyzer = StarGuideAnalyzer(mode='full')
    analyzer.run(days=30)
    analyzer.print_full_report()
    analyzer.print_decision_guide()
    analyzer.print_action_guide()
"""
import os
from pathlib import Path

import sqlite3
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum

# 数据库路径
DB_PATH = os.environ.get("CABBEEN_DB") or str(Path(__file__).resolve().parents[1] / "cabbeen.db")

# 预定义时间段
PERIODS = {
    '2024春': ('2024-03-01', '2024-05-31'),
    '2024夏': ('2024-06-01', '2024-08-31'),
    '2024秋': ('2024-09-01', '2024-11-30'),
    '2024冬': ('2024-12-01', '2024-12-31'),
    '2025-01~02': ('2025-01-01', '2025-02-28'),
    '2025春': ('2025-03-01', '2025-05-31'),
    '2025夏': ('2025-06-01', '2025-08-31'),
    '2025秋': ('2025-09-01', '2025-11-30'),
    '2025冬': ('2025-12-01', '2026-02-28'),
    '2026春': ('2026-03-01', '2026-04-22'),
    '2024下': ('2024-07-01', '2024-12-31'),
    '2025上': ('2025-01-01', '2025-06-30'),
    '2025下': ('2025-07-01', '2025-12-31'),
    '2024全': ('2024-03-01', '2024-12-31'),
    '2025全': ('2025-01-01', '2025-12-31'),
}

# 时间维度配置
TIME_DIMENSIONS = {
    7: {'name': '近7天', 'threshold': 15, 'scene': '即时激励', 'weight': 1},
    15: {'name': '近15天', 'threshold': 10, 'scene': '日常参考', 'weight': 1},
    30: {'name': '近30天', 'threshold': 5, 'scene': '常规考核', 'weight': 2},
    45: {'name': '近45天', 'threshold': 5, 'scene': '深度分析', 'weight': 2},
    365: {'name': '全年', 'threshold': 5, 'scene': '年度评优', 'weight': 3},
}

# 指标阈值（pp）
THRESHOLDS = {
    'top10_rate': 3,      # 含TOP10订单GMV占比
    'hv_rate': 3,         # 高价值占比
    'ld_count': 0.5,      # 连带件数
    'gmv_rank': 3,        # GMV排名
}

# 指标重要性权重
INDICATOR_WEIGHTS = {
    'top10_rate': 0.3,    # TOP10推销
    'hv_rate': 0.4,       # 高价值推销（更重要）
    'ld_count': 0.3,      # 连带能力
}


class OutputMode(Enum):
    BRIEF = 'brief'
    FULL = 'full'


class StarGuideAnalyzer:
    """明星导购能力分析器"""
    
    def __init__(self, db_path: str = DB_PATH, mode: str = 'full'):
        self.db_path = db_path
        self.mode = OutputMode(mode)
        self.conn = None
        self.result = None
        self.guide_details = []  # 导购详细数据
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.text_factory = str
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
    
    # ========== 数据获取方法 ==========
    
    def get_top3(self, start_date: str, end_date: str) -> List[str]:
        """获取时间段内的TOP3导购"""
        cur = self.conn.cursor()
        cur.execute('''
            SELECT guide_name, SUM(amount) as gmv
            FROM sales WHERE sale_date >= ? AND sale_date <= ?
            GROUP BY guide_name ORDER BY gmv DESC LIMIT 3
        ''', (start_date, end_date))
        return [r[0] for r in cur.fetchall()]
    
    def get_top10_styles(self, start_date: str, end_date: str) -> List[str]:
        """获取时间段内的TOP10款式"""
        cur = self.conn.cursor()
        cur.execute('''
            SELECT style_color FROM (
                SELECT style_color, SUM(qty) as q FROM sales
                WHERE sale_date >= ? AND sale_date <= ?
                GROUP BY style_color ORDER BY q DESC LIMIT 10
            )
        ''', (start_date, end_date))
        return [r[0] for r in cur.fetchall()]
    
    def get_all_guides(self, start_date: str, end_date: str) -> List[str]:
        """获取时间段内的所有导购"""
        cur = self.conn.cursor()
        cur.execute('''
            SELECT DISTINCT guide_name FROM sales 
            WHERE sale_date >= ? AND sale_date <= ?
        ''', (start_date, end_date))
        return [r[0] for r in cur.fetchall()]
    
    def get_shop_for_guide(self, guide: str, start_date: str, end_date: str) -> str:
        """获取导购所在店铺"""
        cur = self.conn.cursor()
        cur.execute('''
            SELECT shop_name FROM sales 
            WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ?
            LIMIT 1
        ''', (guide, start_date, end_date))
        r = cur.fetchone()
        return r[0] if r else ''
    
    def analyze_guide(self, guide: str, start_date: str, end_date: str, 
                      top10: List[str], top3: List[str]) -> Optional[Dict]:
        """分析单个导购"""
        cur = self.conn.cursor()
        
        # 基础数据
        cur.execute('''
            SELECT SUM(amount), COUNT(DISTINCT order_no), SUM(qty)
            FROM sales WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ?
        ''', (guide, start_date, end_date))
        gmv, orders, qty = cur.fetchone()
        
        if not gmv or gmv < 5000:
            return None
        
        placeholders = ','.join('?' * len(top10)) if top10 else ''
        
        # 含TOP10订单GMV
        top10_order_amt = 0
        if top10:
            cur.execute(f'''
                SELECT SUM(s.amount) FROM sales s
                WHERE s.guide_name = ? AND s.sale_date >= ? AND s.sale_date <= ?
                AND s.order_no IN (
                    SELECT DISTINCT order_no FROM sales 
                    WHERE sale_date >= ? AND sale_date <= ? AND style_color IN ({placeholders})
                )
            ''', [guide, start_date, end_date, start_date, end_date] + top10)
            top10_order_amt = cur.fetchone()[0] or 0
        
        # 连带件数
        cur.execute('''
            SELECT AVG(sub.qty) FROM (
                SELECT order_no, SUM(qty) as qty FROM sales
                WHERE guide_name = ? AND sale_date >= ? AND sale_date <= ?
                GROUP BY order_no
            ) sub
        ''', (guide, start_date, end_date))
        ld_count = cur.fetchone()[0] or 0
        
        # 高价值占比
        hv_rate = 0
        cur.execute('''
            SELECT tag_price FROM sales 
            WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ? AND tag_price IS NOT NULL
        ''', (start_date, end_date, guide))
        prices = [r[0] for r in cur.fetchall() if r[0]]
        if prices:
            threshold = sorted(prices)[int(len(prices) * 0.75)]
            cur.execute('''
                SELECT SUM(amount) FROM sales 
                WHERE sale_date >= ? AND sale_date <= ? AND guide_name = ? AND tag_price >= ?
            ''', (start_date, end_date, guide, threshold))
            hv_amt = cur.fetchone()[0] or 0
            hv_rate = hv_amt / gmv * 100 if gmv > 0 else 0
        
        return {
            'guide': guide,
            'gmv': gmv,
            'orders': orders,
            'avg_per_order': gmv / orders if orders > 0 else 0,
            'ld_count': ld_count,
            'top10_rate': top10_order_amt / gmv * 100 if gmv > 0 else 0,
            'hv_rate': hv_rate,
            'is_top3': guide in top3,
            'rank': 0,
        }
    
    def analyze_period(self, start_date: str, end_date: str, period_name: str = '') -> Optional[Dict]:
        """分析单个时间段"""
        top3 = self.get_top3(start_date, end_date)
        if len(top3) < 3:
            return None
        
        top10 = self.get_top10_styles(start_date, end_date)
        if not top10:
            return None
        
        all_guides = self.get_all_guides(start_date, end_date)
        
        results = []
        for guide in all_guides:
            guide_data = self.analyze_guide(guide, start_date, end_date, top10, top3)
            if guide_data:
                results.append(guide_data)
        
        if not results:
            return None
        
        # 按GMV排序
        results.sort(key=lambda x: x['gmv'], reverse=True)
        for i, r in enumerate(results):
            r['rank'] = i + 1
        
        top3_list = [r for r in results if r['is_top3']]
        non_list = [r for r in results if not r['is_top3']]
        
        def avg(lst, key):
            vals = [r[key] for r in lst if r[key] is not None]
            return sum(vals) / len(vals) if vals else 0
        
        return {
            'period': period_name,
            'start_date': start_date,
            'end_date': end_date,
            'top3': top3,
            'top3_top10_rate': avg(top3_list, 'top10_rate'),
            'non_top10_rate': avg(non_list, 'top10_rate'),
            'top3_hv_rate': avg(top3_list, 'hv_rate'),
            'non_hv_rate': avg(non_list, 'hv_rate'),
            'top3_ld': avg(top3_list, 'ld_count'),
            'non_ld': avg(non_list, 'ld_count'),
            'top3_gmv': sum(r['gmv'] for r in top3_list),
            'non_gmv': sum(r['gmv'] for r in non_list),
            'top3_count': len(top3_list),
            'non_count': len(non_list),
            'guide_details': results,  # 保存详细数据
        }
    
    def run(self, days: int = 30, periods: List[str] = None) -> Dict:
        """运行分析"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # 获取正确的时间维度配置
        dim = TIME_DIMENSIONS.get(days, TIME_DIMENSIONS[30])
        dim['name'] = f'近{days}天'  # 修正标题
        
        recent_result = self.analyze_period(start_date, end_date, f'近{days}天')
        self.guide_details = recent_result['guide_details'] if recent_result else []
        
        period_results = []
        if periods:
            for p in periods:
                if p in PERIODS:
                    result = self.analyze_period(PERIODS[p][0], PERIODS[p][1], p)
                    if result:
                        period_results.append(result)
        
        self.result = {
            'recent': recent_result,
            'periods': period_results,
            'dimension': dim,
        }
        return self.result
    
    # ========== 决策建议生成 ==========
    
    def generate_decision_guide(self) -> Dict:
        """生成决策建议"""
        if not self.result or not self.result['recent']:
            return {}
        
        r = self.result['recent']
        dim = self.result['dimension']
        threshold = dim['threshold']
        
        diff_top10 = r['top3_top10_rate'] - r['non_top10_rate']
        diff_hv = r['top3_hv_rate'] - r['non_hv_rate']
        diff_ld = r['top3_ld'] - r['non_ld']
        
        # 综合评分
        score_top3 = (
            (1 if diff_top10 > 0 else 0) * INDICATOR_WEIGHTS['top10_rate'] +
            (1 if diff_hv > 0 else 0) * INDICATOR_WEIGHTS['hv_rate'] +
            (1 if diff_ld > 0 else 0) * INDICATOR_WEIGHTS['ld_count']
        )
        
        # 决策判断
        if diff_top10 > threshold and diff_hv > threshold and diff_ld > threshold:
            decision = 'TOP3全面领先'
            level = 'green'
        elif diff_top10 > threshold or diff_hv > threshold:
            decision = 'TOP3部分领先'
            level = 'yellow'
        elif abs(diff_top10) < threshold and abs(diff_hv) < threshold:
            decision = '双方持平'
            level = 'gray'
        else:
            decision = '非TOP3领先'
            level = 'red'
        
        return {
            'dimension': dim['name'],
            'scene': dim['scene'],
            'threshold': threshold,
            'decision': decision,
            'level': level,
            'diff_top10': diff_top10,
            'diff_hv': diff_hv,
            'diff_ld': diff_ld,
            'summary': f"含TOP10订单{diff_top10:+.1f}pp，高价值{diff_hv:+.1f}pp，连带{diff_ld:+.1f}件",
        }
    
    def generate_action_guide(self) -> Dict:
        """生成行动指南"""
        if not self.result or not self.result['recent']:
            return {}
        
        r = self.result['recent']
        dim = self.result['dimension']
        threshold = dim['threshold']
        
        diff_top10 = r['top3_top10_rate'] - r['non_top10_rate']
        diff_hv = r['top3_hv_rate'] - r['non_hv_rate']
        
        actions = {
            'top3': [],
            'non_top3': [],
            'shop': [],
            'priority_guide': [],
        }
        
        # TOP3行动建议
        if diff_top10 > threshold:
            actions['top3'].append({
                'indicator': 'TOP10推销',
                'status': 'ahead',
                'action': '保持优势，扩大领先',
                'detail': f'含TOP10订单GMV占比领先{diff_top10:.1f}pp，继续保持'
            })
        elif diff_top10 < -threshold:
            actions['top3'].append({
                'indicator': 'TOP10推销',
                'status': 'behind',
                'action': '加强TOP10推销',
                'detail': f'含TOP10订单GMV占比落后{abs(diff_top10):.1f}pp，需提升'
            })
        
        if diff_hv > threshold:
            actions['top3'].append({
                'indicator': '高价值推销',
                'status': 'ahead',
                'action': '保持高价值推销优势',
                'detail': f'高价值占比领先{diff_hv:.1f}pp，继续推广高价商品'
            })
        elif diff_hv < -threshold:
            actions['top3'].append({
                'indicator': '高价值推销',
                'status': 'behind',
                'action': '提升高价值商品推销',
                'detail': f'高价值占比落后{abs(diff_hv):.1f}pp，加强高价商品推荐'
            })
        
        # 非TOP3行动建议
        if diff_top10 < -threshold:
            actions['non_top3'].append({
                'indicator': 'TOP10推销',
                'priority': 'high',
                'action': '主动推销TOP10款',
                'detail': f'向TOP3学习推销技巧，主动推荐TOP10款'
            })
        
        if diff_hv < -threshold:
            actions['non_top3'].append({
                'indicator': '高价值推销',
                'priority': 'high',
                'action': '提升高价值商品占比',
                'detail': f'学习TOP3的高价值推销方法，提升客单价'
            })
        
        # 找出需重点提升的导购
        non_top3_guides = [g for g in self.guide_details if not g['is_top3']]
        priority_guides = []
        
        for g in non_top3_guides:
            gaps = []
            if g['top10_rate'] < r['non_top10_rate'] - threshold:
                gaps.append('TOP10')
            if g['hv_rate'] < r['non_hv_rate'] - threshold:
                gaps.append('高价值')
            if gaps:
                priority_guides.append({
                    'guide': g['guide'],
                    'gmv': g['gmv'],
                    'gaps': gaps,
                    'suggestion': f"重点提升：{'/'.join(gaps)}推销能力"
                })
        
        priority_guides.sort(key=lambda x: len(x['gaps']), reverse=True)
        actions['priority_guide'] = priority_guides[:5]  # 最多5人
        
        # 店铺行动建议
        if diff_top10 < -threshold or diff_hv < -threshold:
            actions['shop'] = [
                '组织TOP3经验分享会',
                '安排TOP3与非TOP3结对帮扶',
                '制定非TOP3提升计划并跟踪'
            ]
        else:
            actions['shop'] = [
                '继续保持当前状态',
                '定期复盘分析'
            ]
        
        return actions
    
    # ========== 输出方法 ==========
    
    def _brief_summary(self) -> str:
        """一行核心结论"""
        if not self.result or not self.result['recent']:
            return "⚠️ 数据不足"
        
        r = self.result['recent']
        dim = self.result['dimension']
        diff_top10 = r['top3_top10_rate'] - r['non_top10_rate']
        diff_hv = r['top3_hv_rate'] - r['non_hv_rate']
        
        if diff_top10 > THRESHOLDS['top10_rate'] and diff_hv > THRESHOLDS['hv_rate']:
            status = "✅ 双领先"
        elif diff_top10 > THRESHOLDS['top10_rate']:
            status = f"✅ TOP10+{diff_top10:.0f}pp"
        elif diff_hv > THRESHOLDS['hv_rate']:
            status = f"✅ 高价值+{diff_hv:.0f}pp"
        elif abs(diff_top10) < THRESHOLDS['top10_rate'] and abs(diff_hv) < THRESHOLDS['hv_rate']:
            status = "⚪ 基本持平"
        else:
            status = "❌ 非TOP3领先"
        
        return f"{dim['name']} | TOP3:{r['top3_top10_rate']:.0f}% vs 非TOP3:{r['non_top10_rate']:.0f}% | {status}"
    
    def _full_summary(self) -> str:
        """完整报告头部"""
        if not self.result or not self.result['recent']:
            return "⚠️ 数据不足"
        
        r = self.result['recent']
        dim = self.result['dimension']
        
        diff_top10 = r['top3_top10_rate'] - r['non_top10_rate']
        diff_hv = r['top3_hv_rate'] - r['non_hv_rate']
        diff_ld = r['top3_ld'] - r['non_ld']
        
        return f"""
{'═'*80}
📊 明星导购能力分析报告 · {dim['name']}
{'═'*80}

【核心指标对比】
  指标              TOP3         非TOP3        差距
  ─────────────────────────────────────────────────────
  含TOP10订单GMV    {r['top3_top10_rate']:>6.1f}%      {r['non_top10_rate']:>6.1f}%      {diff_top10:>+5.1f}pp
  高价值占比        {r['top3_hv_rate']:>6.1f}%      {r['non_hv_rate']:>6.1f}%      {diff_hv:>+5.1f}pp
  连带件数          {r['top3_ld']:>6.1f}件      {r['non_ld']:>6.1f}件      {diff_ld:>+5.1f}件

【人员构成】
  TOP3：{', '.join(r['top3'])}（{r['top3_count']}人）
  非TOP3：{r['non_count']}人

【GMV占比】
  TOP3：{r['top3_gmv']:,.0f}元（{r['top3_gmv']/(r['top3_gmv']+r['non_gmv'])*100:.1f}%）
  非TOP3：{r['non_gmv']:,.0f}元（{r['non_gmv']/(r['top3_gmv']+r['non_gmv'])*100:.1f}%）"""

    def _full_period_table(self) -> str:
        """历史时间段表格"""
        if not self.result or not self.result['periods']:
            return ""
        
        header = """
【历史对比】
  时间段          含TOP10占比          高价值占比          结论
  ──────────────────────────────────────────────────────────────────────"""
        rows = []
        for p in self.result['periods']:
            diff_t = p['top3_top10_rate'] - p['non_top10_rate']
            diff_h = p['top3_hv_rate'] - p['non_hv_rate']
            
            if diff_t > THRESHOLDS['top10_rate'] and diff_h > THRESHOLDS['hv_rate']:
                mark = "✅ 双领先"
            elif diff_t > THRESHOLDS['top10_rate']:
                mark = f"✅ TOP10+{diff_t:.0f}pp"
            elif diff_h > THRESHOLDS['hv_rate']:
                mark = f"✅ 高价值+{diff_h:.0f}pp"
            elif diff_t < -THRESHOLDS['top10_rate'] and diff_h < -THRESHOLDS['hv_rate']:
                mark = "❌ 双落后"
            elif abs(diff_t) < THRESHOLDS['top10_rate'] and abs(diff_h) < THRESHOLDS['hv_rate']:
                mark = "⚪ 持平"
            else:
                mark = "⚠️ 互有胜负"
            
            rows.append(f"  {p['period']:<12} {p['top3_top10_rate']:>5.1f}%/{p['non_top10_rate']:>5.1f}%      "
                       f"{p['top3_hv_rate']:>5.1f}%/{p['non_hv_rate']:>5.1f}%      {mark}")
        
        return header + '\n'.join(rows)
    
    def print_report(self):
        """打印报告"""
        if self.mode == OutputMode.BRIEF:
            print(self._brief_summary())
        else:
            print(self._full_summary())
            print(self._full_period_table())
            print("═"*80)
    
    def print_decision_guide(self):
        """打印决策建议"""
        guide = self.generate_decision_guide()
        if not guide:
            return
        
        level_emoji = {'green': '🟢', 'yellow': '🟡', 'gray': '⚪', 'red': '🔴'}
        
        print(f"""
{'─'*80}
🎯 决策建议 · {guide['dimension']}
{'─'*80}

  场景：{guide['scene']}（阈值±{guide['threshold']}pp）
  
  【综合判断】{level_emoji.get(guide['level'], '⚪')} {guide['decision']}
  
  【指标差距】
    • 含TOP10订单GMV占比：{guide['diff_top10']:+.1f}pp
    • 高价值占比：{guide['diff_hv']:+.1f}pp
    • 连带件数：{guide['diff_ld']:+.1f}件
""")
    
    def print_action_guide(self):
        """打印行动指南"""
        actions = self.generate_action_guide()
        if not actions:
            return
        
        print(f"""
{'─'*80}
📋 行动指南
{'─'*80}""")
        
        # TOP3行动
        if actions['top3']:
            print("\n【TOP3保持项】")
            for a in actions['top3']:
                emoji = '✅' if a['status'] == 'ahead' else '⚠️'
                print(f"  {emoji} {a['indicator']}：{a['detail']}")
        
        # 非TOP3行动
        if actions['non_top3']:
            print("\n【非TOP3改进项】")
            for a in actions['non_top3']:
                priority_mark = '🔴' if a['priority'] == 'high' else '🟡'
                print(f"  {priority_mark} {a['indicator']}：{a['detail']}")
        
        # 重点导购
        if actions['priority_guide']:
            print("\n【重点提升导购】")
            for g in actions['priority_guide']:
                print(f"  🔸 {g['guide']}（GMV {g['gmv']:,.0f}元）：{g['suggestion']}")
        
        # 店铺行动
        if actions['shop']:
            print("\n【店铺行动】")
            for i, s in enumerate(actions['shop'], 1):
                print(f"  {i}. {s}")
        
        print()
    
    def get_brief(self) -> str:
        """获取一行结论"""
        return self._brief_summary()
    
    def get_decision_guide(self) -> Dict:
        """获取决策建议"""
        return self.generate_decision_guide()
    
    def get_action_guide(self) -> Dict:
        """获取行动指南"""
        return self.generate_action_guide()


# ========== 快捷函数 ==========

def quick_analyze(days: int = 30) -> str:
    """快速分析 - 返回一行结论"""
    with StarGuideAnalyzer(mode='brief') as analyzer:
        analyzer.run(days=days)
        return analyzer.get_brief()


def full_analyze(days: int = 30, periods: List[str] = None) -> Dict:
    """完整分析"""
    with StarGuideAnalyzer(mode='full') as analyzer:
        analyzer.run(days=days, periods=periods)
        return analyzer.result


def print_decision_guide(days: int = 30):
    """打印完整报告+决策建议+行动指南"""
    with StarGuideAnalyzer(mode='full') as analyzer:
        analyzer.run(days=days, periods=['2025全', '2024全'])
        analyzer.print_report()
        analyzer.print_decision_guide()
        analyzer.print_action_guide()


# ========== 命令行入口 ==========
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='明星导购能力分析')
    parser.add_argument('--mode', '-m', choices=['brief', 'full'], default='full')
    parser.add_argument('--days', '-d', type=int, default=30)
    parser.add_argument('--periods', '-p', nargs='+', choices=list(PERIODS.keys()))
    parser.add_argument('--guide', '-g', action='store_true', help='包含行动指南')
    args = parser.parse_args()
    
    sys.stdout.reconfigure(encoding='utf-8')
    
    with StarGuideAnalyzer(mode=args.mode) as analyzer:
        analyzer.run(days=args.days, periods=args.periods)
        analyzer.print_report()
        if args.guide or args.mode == 'full':
            analyzer.print_decision_guide()
            analyzer.print_action_guide()
