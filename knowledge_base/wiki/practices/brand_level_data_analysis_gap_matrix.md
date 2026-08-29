---
type: practice
title: 品牌级数据分析覆盖缺口矩阵（focus_brands 36）
aliases:
  - "brand level data analysis gap matrix"
  - "品牌级数据分析缺口"
  - "focus_brands 数据分析覆盖"
tags: [multi_brand, data_analysis, gap_analysis, focus_brands, cabbeen, peacebird, crocs, audit]
sources: [2026-08-29_DuckLake_1.0_数据湖格式生产就绪, 2026-08-29_零售数据质量可观测性_Great_Expectations_dbt, 2026-08-29_多品牌服装零售数据中台案例_会员OneID跨品牌复购, multi_brand_unified_analytics, 2026-08-26_多品牌零售数据中台与全域用户治理实践2026, 2026-08-26_太平鸟数字化与数据分析体系2026]
created: 2026-08-29
updated: 2026-08-29
cross_refs: [[cabbeen]], [[peacebird]], [[crocs]], [[服装行业竞争格局]], [[multi_brand_unified_analytics]], [[brand_config_driven_system]], [hxg]]
---

# 品牌级数据分析覆盖缺口矩阵（focus_brands 36）

> **一句话摘要**：对 `kb_benchmarks.json` 的 **focus_brands 36 品牌**做"数据分析视角覆盖"审计——区别于 L2 域级缺口，本页专门识别**品牌级**缺口：哪些品牌有 A轮财务/门店数据、却缺 L2_06/07 的数据分析视角（BI 指标、售罄率趋势 SQL、渠道结构分析）。这是 C轮"查漏须覆盖品牌级数据分析缺口"的落地清单。

> **来源**：第零步扫描 36 品牌实体页 + 本轮三篇来源（DuckLake / 数据质量可观测性 / 多品牌服装中台案例）
> **最后更新**：2026-08-29

## 核心要点

1. **品牌级缺口 ≠ 域级缺口**：L2_06/07 域级已较完整（SQL/BI/ETL/湖仓 practice 齐全），真正的缺口在**品牌颗粒度**——36 品牌实体页中仅竞品 `gxg` 含 BI 分析小节，**0/36 含"数据分析/BI 视角"的系统化分析页**。
2. **数据可得性决定优先级**：36 品牌按"财报级数据可得性"分三层（L1 双核 / L2 上市公司 / L3 品牌墙+女装），缺口价值随可得性递减。
3. **双核已部分补**：[[peacebird]] 已有"数字化与数据分析体系"源页；[[cabbeen]] / [[crocs]] 仍缺品牌级分析实践页。
4. **下轮锚点**：先做双核品牌级分析实践（售罄率趋势 SQL / 渠道结构 BI / 门店绩效），再建 L2 上市公司统一指标分析模板。

## 36 品牌注册表·数据分析覆盖缺口矩阵

| 层级 | 品牌 | 财报级数据 | 实体页 | 品牌级分析实践页 | 缺口状态 |
|---|---|:---:|---|---|---|
| **L1 双核** | [[cabbeen]]（HK 02030） | ✅ 2026H1 营收4.53亿/毛利46.3%/门店573/售罄73.8% | ✅ | ❌ | **高优先缺口** |
| **L1 双核** | [[peacebird]] | ✅ 2026H1 营收28.78亿/门店2861/毛利61.2% | ✅ | 🟡 仅"数字化体系"源页 | 部分覆盖 |
| **L1 上市** | [[crocs]]（NASDAQ:CROX） | ✅ Q2'26 营收11.79亿/毛利59.4% | ✅ | ❌ | **高优先缺口** |
| **L2 上市** | dkny / tommy_hilfiger / karl_lagerfeld / salomon / hoka_one_one / levis / diesel | 🟡 母公司财报 | 部分 | ❌ | 中优先 |
| **L2 上市** | gxg / muson（gxg_muson） | ✅ 2025 营收20.56亿 | ✅(含BI小节) | 🟡 | 部分覆盖 |
| **L3 品牌墙** | trussardi / mr_mrs / marcelo_burlon / g_star_raw / lacoste / ellesse / mlb / mlb_kids / nerdy / adlv / chuu / no_one_else / thisisizi8 / awoken_space / awoken_time / the_mr_young / two_am / nautica / etudes / king_baby / humble_humble_r 等 26 品牌 | ❌ 黑箱/媒体估算 | 部分 | ❌ | 探针式补全 |
| **L3 女装** | ariose_years（艾诺丝）/ dekashell（迪卡轩） | ❌ 私企无披露 | 部分 | ❌ | 探针式补全 |

> 注：focus_brands 当前 **36** 个（较 2026-08-26 C轮 practice 所记 35 新增 `humble_humble_r`），已在 [[multi_brand_unified_analytics|多品牌统一分析架构]] 同步修正。

## 品牌级缺口的下轮优先方向

| 优先级 | 动作 | 交付物 | 对应品牌 |
|---|---|---|---|
| P0 | 补双核品牌级分析实践 | cabbeen 售罄率趋势 SQL + 渠道结构 BI + 门店绩效页 | [[cabbeen]] |
| P0 | 建第三家财报品牌对标页 | crocs GMROI/售罄/周转对标模板 | [[crocs]] |
| P1 | L2 上市公司统一指标分析模板 | 财报品牌通用指标分析 practice | dkny/tommy/karl/salomon/hoka/levis/diesel |
| P2 | 品牌墙探针式补全 | 媒体估算口径的品牌快照源页 | 品牌墙 26 + 女装 2 |

## 结论

1. **C轮的"品牌感知"不是技术搜索绑品牌名，而是查漏必须落到品牌颗粒度**——36 品牌实体页 0 个含系统化数据分析视角，这是比 L2 域级缺口更隐蔽、更该补的真缺口。
2. **双核（cabbeen/peacebird）与 crocs 是最高杠杆的突破口**：三者已有财报级数据，补品牌级分析实践的边际成本最低、对 [[multi_brand_unified_analytics|多品牌统一分析架构]] 的"被分析对象"填充最直接。
3. **品牌墙 26 品牌与女装 2 品牌应探针式补全**，不做深度分析页——其数据黑箱/媒体估算属性决定深度分析 ROI 低，强行造页只会产生低置信度孤岛。
4. 本矩阵须**每轮回溯**：随 A轮实体页与 C轮实践页增长，品牌级覆盖率应作为 C轮健康快照的固定指标。

## 信息链

上游来源 [[brand_level_data_analysis_gap_matrix|本页]] ← 第零步扫描（36 品牌实体页）+ [[2026-08-29_多品牌服装零售数据中台案例_会员OneID跨品牌复购|多品牌中台案例]] / [[2026-08-29_DuckLake_1.0_数据湖格式生产就绪|DuckLake]] / [[2026-08-29_零售数据质量可观测性_Great_Expectations_dbt|数据质量可观测性]]
→ 本页（品牌级数据分析覆盖审计）
→ 下游应用：[[multi_brand_unified_analytics|多品牌统一分析架构]]（被分析对象 = focus_brands 36）、[[服装行业竞争格局]]（36 品牌集团化运营）、[[cabbeen]] / [[peacebird]] / [[crocs]]（双核+第三家财报品牌级分析页）、[[brand_config_driven_system|品牌配置驱动系统]]（品牌注册表数据可得性分层）

## 关联页面

- [[cabbeen]]
- [[peacebird]]
- [[crocs]]
- [[服装行业竞争格局]]
- [[multi_brand_unified_analytics]]
- [[brand_config_driven_system]]
- [[2026-08-29_DuckLake_1.0_数据湖格式生产就绪]]
- [[2026-08-29_零售数据质量可观测性_Great_Expectations_dbt]]
- [[2026-08-29_多品牌服装零售数据中台案例_会员OneID跨品牌复购]]

## 待办 / 待验证

- ⚠️ **数据矛盾 / 待验证**：focus_brands 计数 35（见 [[multi_brand_unified_analytics|多品牌统一分析架构]] 2026-08-26 C轮更新）vs 36（当前 `kb_benchmarks.json`，新增 `humble_humble_r`）——已在本页与多品牌 practice 同步修正为 36，待下轮 S轮合成时统一口径。
- 品牌级覆盖率（0/36）为第零步静态扫描结果，随 A/C 轮增长须动态更新，避免与本页快照失同步。
