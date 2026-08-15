#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlled update of kb_benchmarks.json — Step 5 of daily optimization.
Adds 6 concept-level threshold keys + guide_kpi.attach_rate_boost.
Preserves existing schema; only adds/updates, never overwrites unrelated keys.
"""
import json
from pathlib import Path

PATH = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\kb_benchmarks.json")

d = json.load(open(PATH, encoding="utf-8"))

# ---- New concept-level threshold sets (from 2026-08-07 wiki/sources) ----
new_sets = {
    "sku_rationalization": {
        "source": "wiki/sources/2026-08-07_retailnorthstar_SKU合理化五步减法与复杂度五区间.md",
        "annual_sku_creep": [0.12, 0.18],          # SKU 年均自然增长 12%–18%
        "transfer_rate_with_substitute": [0.6, 0.8], # 有替代款销售转移率 60%–80%
        "transfer_rate_without_substitute": [0.2, 0.4], # 无替代款 20%–40%
        "reduction_target": [0.15, 0.25],           # SKU 降幅 15%–25%
        "sell_through_lift_pct": [0.03, 0.08],      # 季末售罄率提升 3–8pct
        "dead_stock_reduction_pct": [0.2, 0.3],      # 断码率降 20%–30%
        "inventory_turnover_lift_per_year": [0.5, 1.0], # 库存周转提升 +0.5–1.0 次/年
        "sales_change_range": [0.0, 0.05],          # 销售额变化 持平~+5%
        "guide_memorizable_styles": [40, 60],        # 导购可熟练讲解款式数上限 40–60 款
    },
    "sps_model": {
        "source": "wiki/sources/2026-08-07_单款店均效率SPS与款式宽度反推模型.md",
        "sps_healthy": 8,                            # 单款店均销量健康值 ≥8 件
        "sps_warn": 5,                              # 预警线 <5 件
        "sps_too_narrow": 20,                       # 偏窄信号 >20 件
        "store_styles_100sqm": [120, 180],          # 100㎡ 店均上柜 120–180 款
        "store_styles_200sqm": [200, 280],          # 200㎡ 店均上柜 200–280 款
        "perf_inflection_over_limit_pct": 0.2,       # 超上限 +20% 后坪效下降
        "category_sps": {                           # 分品类 SPS 参考
            "basic": [15, 30],                       # 基础款（T恤/衬衫）
            "core": [8, 15],                         # 核心款（外套/连衣裙）
            "image": [2, 5],                         # 形象款
            "accessory": [20, 40],                   # 配饰
        },
    },
    "labor_efficiency": {
        "source": "wiki/sources/2026-08-07_零售人效三层指标与弹性排班四杠杆.md",
        "sales_per_head_month_median": [80000, 120000], # 人均销售额月 8–12 万
        "sales_per_head_month_excellent": 150000,       # ≥15 万
        "sph_median": [400, 600],                       # 人时销售额 SPH 400–600 元
        "sph_excellent": 800,                           # ≥800 元
        "labor_cost_ratio_healthy": [0.08, 0.12],       # 人力成本率 8%–12%
        "labor_cost_ratio_warning": 0.15,               # >15% 预警
        "scheduling_fit_range": [0.9, 1.1],             # 排班吻合度 90%–110%
        "peak_coverage_min": 0.85,                      # 高峰覆盖率 ≥85%
        "monthly_turnover_median": [0.04, 0.06],         # 月度离职率 4%–6%
        "monthly_turnover_warning": 0.08,               # >8% 预警
        "new_hire_90d_retention_median": [0.55, 0.65],   # 新人 90 天留存 55%–65%
        "new_hire_90d_retention_excellent": 0.75,        # ≥75%
        "flex_levers_cost_reduction_pct": [0.015, 0.03], # 人力成本率降 1.5–3pct
        "flex_levers_sph_boost_pct": [0.12, 0.18],       # SPH 提升 12%–18%
        "flex_levers_peak_loss_reduction_pct": [0.2, 0.3], # 高峰流失客减 20%–30%
    },
    "guide_four_quadrant": {
        "source": "wiki/sources/2026-08-07_帷幄_鞋服导购四象限评估与五项行为指标.md",
        "potential_type_share_of_underperformers": [0.2, 0.3], # 潜力型占不达标 20%–30%
        "demand_questions_median": [2, 3],                     # 需求提问数 2–3 个
        "demand_questions_excellent": 5,                        # 优秀者 5 个以上
        "attach_rate_boost_pct": [0.08, 0.15],                 # 连带率提升 8%–15%
        "reception_conversion_boost_pct": [0.1, 0.2],           # 接待转化率提升 10%–20%
        "low_performer_improvement_days": [30, 60],             # 低效人员改善期 30–60 天
    },
    "digital_twin_store_manager": {
        "source": "wiki/sources/2026-08-07_数字孪生店长_排班自动化与店长工时再分配.md",
        "automatable_hours_share": 0.4,                  # 店长可自动化工时 ~40%
        "scheduling_time_reduction_pct": 0.89,           # 排班耗时 -89%
        "coaching_time_share_before": 0.25,              # 带教 25%
        "coaching_time_share_after": [0.35, 0.4],        # →35%–40%
        "labor_efficiency_boost_pct": [0.08, 0.12],      # 人效提升 8%–12%
        "peak_coverage_before": [0.65, 0.7],             # 高峰覆盖率 65%–70%
        "peak_coverage_after": 0.85,                     # →85%+
        "traffic_history_weeks": [8, 12],                # 客流曲线训练历史 8–12 周
    },
    "merchandise_calendar": {
        "source": "wiki/sources/2026-08-07_商品企划日历倒排周期与波段配比.md",
        "futures_lead_time_months": 9,                   # 期货 T-9 定调→上市 9 个月
        "sample_review_elimination_rate": [0.3, 0.4],    # 样衣评审淘汰 30%–40%
        "futures_share": [0.6, 0.8],                     # 期货 60%–80%
        "quick_response_share": [0.2, 0.4],              # 快反 20%–40%
        "quick_response_lead_days": [30, 45],            # 快反 30–45 天
        "waves_per_season": [3, 5],                      # 一季 3–5 波
        "first_wave_share": [0.3, 0.35],                 # 首波 30%–35%
        "second_wave_share": [0.25, 0.3],                # 第二波 25%–30%
        "third_wave_share": [0.2, 0.25],                 # 第三波 20%–25%
        "fourth_fifth_wave_share": [0.15, 0.2],          # 第四/五波 15%–20%
    },
}

added = []
for key, val in new_sets.items():
    if key not in d:
        d[key] = val
        added.append(key)
    else:
        print(f"  SKIP (already present): {key}")

# ---- guide_kpi.attach_rate_boost (NEW per 帷幄 suggestion) ----
if "guide_kpi" in d:
    if "attach_rate_boost" not in d["guide_kpi"]:
        d["guide_kpi"]["attach_rate_boost"] = [0.08, 0.15]
        added.append("guide_kpi.attach_rate_boost")
    else:
        print("  SKIP (already present): guide_kpi.attach_rate_boost")

# ---- Metadata update ----
d["updated"] = "2026-08-08"
d["meta"]["last_scan"] = "2026-08-08"
d["meta"]["files_scanned"] = "27 个 wiki/entities 文件 + 52 个 wiki/concepts 文件"

json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("\n=== Step 5 benchmark update complete ===")
print("Added keys:", added)
print("Total top-level keys now:", len(d))
print("updated:", d["updated"])
print("files_scanned:", d["meta"]["files_scanned"])
