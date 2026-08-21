# 每日健康快照 — 2026-08-21（A2 轮）

> 生成：2026-08-21 08:15 · 触发：ingestA2（A2 固定分组 12 品牌·品牌主体全维度）
> 对照基准：log.md 最近一次 optimize（2026-08-14 04:05）lint 结论 = 断链14/孤岛0/矛盾0/过期0/分类0

## 本轮概况

| 指标 | 数值 |
|------|------|
| 采集 source 页 | 10 篇（g_star_raw / hoka_one_one / humble_humble_r / karl_lagerfeld / king_baby / lacoste / levis / marcelo_burlon / mlb / mlb_kids） |
| 显式无新增品牌 | 2 个（etudes / koyo — 探针无有效新信号，不重复造页） |
| 织网双链 | 10 实体回链 + 10 source→concept/entity 出链 + 实体页内概念互链（≈30 条） |
| 矛盾 | 1 处 ⚠️（mlb Q2 预估 vs 实际，时序差异） |
| 基准核对 | 3 处 ℹ️（levis Q2 一致 / karl KL 净亏一致 / hoka 财期差异） |
| 新增「结论+信息链」页 | 10 source 页全含 + 10 entity 刷新小节全含 |
| 孤岛数 | 0 |
| 断链（本轮新增双链） | 0 |
| superseded_by 回填 | 0（本轮为增量补充，无同指标数值替代） |

## 本轮缺口清单与覆盖

预检（第零步）：12 品牌全部「OK」（实体页齐 + source≥3），无缺实体/少源品牌 → 按规则仍全维度检索核验。

| 品牌 | 预检 | 本轮检索结果 | 处置 |
|------|------|--------------|------|
| etudes | OK(4源) | AW26 Résonances 系已有收录，无新信号 | 无新增 |
| g_star_raw | OK(4源) | SoHo 新店+Agbobly 联名、印度授权、裁员75人、ClassiQ | 新 source + 实体刷新 |
| hoka_one_one | OK(4源) | Deckers FY2026 创纪录、中国 230 店成最大市场 | 新 source + 实体刷新 |
| humble_humble_r | OK(4源) | 明星矩阵营销、Softcore 系列、奥莱下沉 | 新 source + 实体刷新 |
| karl_lagerfeld | OK(5源) | 七匹狼年报细化、KL 净资产-1.6亿、门店净减98 | 新 source + 实体刷新 |
| king_baby | OK(5源) | 新奥尔良首店、厦门 K11/西单大悦城布点 | 新 source + 实体刷新 |
| koyo | OK(4源) | 探针命中干扰项（咖啡/球鞋），无有效信号 | 无新增 |
| lacoste | OK(4源) | 香港毕打行旗舰、视觉焕新、法网联名 | 新 source + 实体刷新 |
| levis | OK(3源) | Q2 DTC 51%、换帅 Anita Fung、全年指引上调 | 新 source + 实体刷新 |
| marcelo_burlon | OK(4源) | County of Milan 主体、Driade 联名、童装代理 | 新 source + 实体刷新 |
| mlb | OK(9源) | 入境游红利、香港+20%、Q2 预估 4026-4150 亿 | 新 source + 实体刷新 |
| mlb_kids | OK(4源) | 依附成人线店中店模式、全家桶消费 | 新 source + 实体刷新 |

## 矛盾清单（第六步输出）

1. ⚠️ **mlb 2026Q2 营收口径**：本轮券商预估 4,026-4,150 亿韩元（韩华 7-21 / NH 6-25）vs 08-18 已收录实际值 3,996 亿 +5.5% → 判为「预估 vs 实际」时序差异，非同一时点矛盾；已在 source 页标注，RAG 引用以实际值（3,996 亿）为准。

## 健康基线（lint 对照）

- 断链：14（08-14 optimize）→ 本轮新增双链 0 断链 ✅
- 孤岛：0（本轮 10 新 source 全有出链）✅
- 矛盾：全库 `⚠️ 数据矛盾` 标记页 58（含本轮 1 处；log 记录为 1 处新增，与 grep 计数口径一致——grep 计数含历史累计，log 仅记本轮增量）✅
- 结论+信息链：10/10 source 页 + 10/10 entity 刷新小节 ✅

## 下轮优先方向（仅限 A2 组 12 品牌）

- **etudes / koyo**：连续两轮无新增，下轮可降为探针级核验（1 次检索），若仍无新信号保持「无新增」记录。
- **mlb**：跟踪 TaylorMade 收购进展与 Q2 实际值确认（券商预估 vs 实际的收敛方向）；中国库存调整期何时结束是核心变量。
- **levis**：跟踪大中华区换帅（Anita Fung）后 Q3 中国表现与 Blue Tab 高端线在华落地。
- **karl_lagerfeld**：跟踪七匹狼 2026 中报 KL 分部亏损是否收窄、无形资产是否继续减值。
- **g_star_raw**：跟踪 WHP 重组后门店效率、印度授权 6 个月后的规模数据。
- **hoka_one_one**：跟踪中国 230 店后的开店节奏（每年 20-25 家）与 FY27Q2 增速是否回升。
