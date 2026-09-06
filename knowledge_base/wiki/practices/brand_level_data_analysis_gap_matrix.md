---
type: practice
title: 品牌级数据分析覆盖缺口矩阵（focus_brands 35）
aliases:
  - "brand level data analysis gap matrix"
  - "品牌级数据分析缺口"
  - "focus_brands 数据分析覆盖"
tags: [multi_brand, data_analysis, gap_analysis, focus_brands, cabbeen, peacebird, crocs, audit]
sources: [2026-08-29_DuckLake_1.0_数据湖格式生产就绪, 2026-08-29_零售数据质量可观测性_Great_Expectations_dbt, 2026-08-29_多品牌服装零售数据中台案例_会员OneID跨品牌复购, multi_brand_unified_analytics, 2026-08-26_多品牌零售数据中台与全域用户治理实践2026, 2026-08-26_太平鸟数字化与数据分析体系2026, peacebird_brand_analytics_2026, cabbeen_brand_analytics_2026, crocs_financial_benchmark_template_2026]
created: 2026-08-29
updated: 2026-09-06
cross_refs: [[cabbeen]], [[peacebird]], [[crocs]], [[muson_gxg]], [[服装行业竞争格局]], [[multi_brand_unified_analytics]], [[brand_config_driven_system]], [[peacebird_brand_analytics_2026]], [[cabbeen_brand_analytics_2026]], [[crocs_financial_benchmark_template_2026]]
---

# 品牌级数据分析覆盖缺口矩阵（focus_brands 35）

> **一句话摘要**：对 `kb_benchmarks.json` 的 **focus_brands 35 品牌**做"数据分析视角覆盖"审计——区别于 L2 域级缺口，本页专门识别**品牌级**缺口：哪些品牌有 A轮财务/门店数据、却缺 L2_06/07 的数据分析视角（BI 指标、售罄率趋势 SQL、渠道结构分析）。这是 C轮"查漏须覆盖品牌级数据分析缺口"的落地清单。

> **来源**：第零步扫描 35 品牌实体页 + 多轮 C 轮来源（DuckLake / 数据质量可观测性 / 多品牌服装中台案例 / 太平鸟数字化体系 / 品牌级分析实践页）
> **最后更新**：2026-09-06

## 核心要点

1. **品牌级缺口 ≠ 域级缺口**：L2_06/07 域级已较完整（SQL/BI/ETL/湖仓 practice 齐全），真正的缺口在**品牌颗粒度**——35 品牌实体页中仅竞品 `gxg` 含 BI 分析小节；2026-08-29 首建本矩阵时 **0/35 含"数据分析/BI 视角"的系统化分析页**。
2. **数据可得性决定优先级**：35 品牌按"财报级数据可得性"分三层（L1 双核 / L2 上市公司 / L3 品牌墙+女装），缺口价值随可得性递减。
3. **P0 全部闭环（3/35）**：2026-09-03 补 [[cabbeen_brand_analytics_2026|卡宾]]（售罄率直算型）+ [[crocs_financial_benchmark_template_2026|Crocs]]（财报对标模板型）；2026-09-06 补 [[peacebird_brand_analytics_2026|太平鸟]]（代理链型）——双核 + 第三财报品牌三种披露形态全覆盖。
4. **下轮锚点（P1）**：L2 上市公司统一指标分析模板（dkny/tommy/karl/salomon/hoka/levis/diesel），复用三种既有模板骨架，不必从零设计。

## 35 品牌注册表·数据分析覆盖缺口矩阵

| 层级 | 品牌 | 财报级数据 | 实体页 | 品牌级分析实践页 | 缺口状态 |
|---|---|:---:|---|---|---|
| **L1 双核** | [[cabbeen]]（HK 02030） | ✅ 2026H1 营收4.53亿/毛利46.3%/门店573/售罄73.8% | ✅ | ✅ [[cabbeen_brand_analytics_2026]] | **已闭环**（09-03） |
| **L1 双核** | [[peacebird]] | ✅ 2026H1 营收28.78亿/门店2861/毛利61.2% | ✅ | ✅ [[peacebird_brand_analytics_2026]] | **已闭环**（09-06） |
| **L1 上市** | [[crocs]]（NASDAQ:CROX） | ✅ Q2'26 营收11.79亿/毛利59.4% | ✅ | ✅ [[crocs_financial_benchmark_template_2026]] | **已闭环**（09-03） |
| **L2 上市** | dkny / tommy_hilfiger / karl_lagerfeld / salomon / hoka_one_one / levis / diesel | 🟡 母公司财报 | 部分 | ❌ | **中优先（P1 下轮）** |
| **L2 上市** | gxg / muson（[[muson_gxg]]） | ✅ 2025 营收20.56亿 | ✅(含BI小节) | 🟡 | 部分覆盖 |
| **L3 品牌墙** | trussardi / mr_mrs / marcelo_burlon / g_star_raw / lacoste / ellesse / mlb / mlb_kids / nerdy / adlv / chuu / no_one_else / thisisizi8 / awoken_space / awoken_time / the_mr_young / two_am / nautica / etudes / king_baby / humble_humble_r 等 21 品牌 | ❌ 黑箱/媒体估算 | 部分 | ❌ | 探针式补全 |
| **L3 女装** | ariose_years（艾诺丝）/ dekashell（迪卡轩） | ❌ 私企无披露 | 部分 | ❌ | 探针式补全 |

> 注：focus_brands 当前 **35** 个（`kb_benchmarks.json` 权威计数，含 `humble_humble_r`；2026-08-29 本页曾误记为 36"新增 humble"——经核对 JSON 35 已含 humble，2026-09-06 统一为 35，见 [[multi_brand_unified_analytics|多品牌统一分析架构]] 同步修正）。

## 品牌级缺口的下轮优先方向

| 优先级 | 动作 | 交付物 | 对应品牌 |
|---|---|---|---|
| ✅ P0 完成 | 补双核品牌级分析实践 | [[cabbeen_brand_analytics_2026]]（售罄率趋势 SQL + 渠道口径表 + 门店绩效） | [[cabbeen]] |
| ✅ P0 完成 | 建第三家财报品牌对标页 | [[crocs_financial_benchmark_template_2026]]（GMROI/售罄/周转对标模板） | [[crocs]] |
| ✅ P0 完成 | 补双核第二家品牌级分析 | [[peacebird_brand_analytics_2026]]（渠道三拆/门店绩效/存货代理链/盈利质量穿透） | [[peacebird]] |
| P1 | L2 上市公司统一指标分析模板 | 财报品牌通用指标分析 practice | dkny/tommy/karl/salomon/hoka/levis/diesel |
| P2 | 品牌墙探针式补全 | 媒体估算口径的品牌快照源页 | 品牌墙 21 + 女装 2 |

## 结论

1. **C轮的"品牌感知"不是技术搜索绑品牌名，而是查漏必须落到品牌颗粒度**——2026-08-29 首建时 35 品牌实体页 0 个含系统化数据分析视角，这是比 L2 域级缺口更隐蔽、更该补的真缺口；历经两轮 C 轮（09-03/09-06）已闭环 P0 三行。
2. **双核（cabbeen/peacebird）与 crocs 是最高杠杆的突破口**：三者已有财报级数据，补品牌级分析实践的边际成本最低、对 [[multi_brand_unified_analytics|多品牌统一分析架构]] 的"被分析对象"填充最直接——现已产出三种披露形态的模板（卡宾直算售罄率 / 太平鸟存货代理链 / Crocs 财报对标），P1 上市公司组可直接复用。
3. **品牌墙 21 品牌与女装 2 品牌应探针式补全**，不做深度分析页——其数据黑箱/媒体估算属性决定深度分析 ROI 低，强行造页只会产生低置信度孤岛。
4. 本矩阵须**每轮回溯**：随 A轮实体页与 C轮实践页增长，品牌级覆盖率（当前 3/35）应作为 C轮健康快照的固定指标。

## 信息链

上游来源 [[brand_level_data_analysis_gap_matrix|本页]] ← 第零步扫描（35 品牌实体页）+ [[2026-08-29_多品牌服装零售数据中台案例_会员OneID跨品牌复购|多品牌中台案例]] / [[2026-08-29_DuckLake_1.0_数据湖格式生产就绪|DuckLake]] / [[2026-08-29_零售数据质量可观测性_Great_Expectations_dbt|数据质量可观测性]] / [[2026-08-26_太平鸟数字化与数据分析体系2026]]
→ 本页（品牌级数据分析覆盖审计）
→ 下游应用：[[multi_brand_unified_analytics|多品牌统一分析架构]]（被分析对象 = focus_brands 35）、[[服装行业竞争格局]]（35 品牌集团化运营）、[[cabbeen_brand_analytics_2026]] / [[peacebird_brand_analytics_2026]] / [[crocs_financial_benchmark_template_2026]]（三种模板闭环 3/35）、[[brand_config_driven_system|品牌配置驱动系统]]（品牌注册表数据可得性分层）

## 关联页面

- [[cabbeen]]
- [[peacebird]]
- [[crocs]]
- [[muson_gxg]]
- [[服装行业竞争格局]]
- [[multi_brand_unified_analytics]]
- [[brand_config_driven_system]]
- [[cabbeen_brand_analytics_2026]]
- [[peacebird_brand_analytics_2026]]
- [[crocs_financial_benchmark_template_2026]]
- [[2026-08-29_DuckLake_1.0_数据湖格式生产就绪]]
- [[2026-08-29_零售数据质量可观测性_Great_Expectations_dbt]]
- [[2026-08-29_多品牌服装零售数据中台案例_会员OneID跨品牌复购]]
- [[2026-08-26_太平鸟数字化与数据分析体系2026]]

## 待办 / 待验证

- ✅ **计数统一**：focus_brands 计数曾在本页与 [[multi_brand_unified_analytics|多品牌统一分析架构]] 间出现 35 vs 36 分歧（2026-08-29 曾误记 36"新增 humble"）——2026-09-06 核对 `kb_benchmarks.json` 权威为 **35 个（已含 humble_humble_r）**，两页已同步修正为 35，口径分歧关闭。
- 品牌级覆盖率（3/35）为截至 2026-09-06 快照，随 A/C 轮增长须动态更新，避免与本页快照失同步。
