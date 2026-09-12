# 每日健康快照 · 2026-08-27 · A2 轮（固定分组 11 品牌·品牌主体全维度）

> 生成时间：2026-08-27 07:00（A2 自动化 `automation-1787745271156` 触发）
> 范围：A2 分组 = etudes, g_star_raw, hoka_one_one, humble_humble_r, karl_lagerfeld, king_baby, lacoste, levis, marcelo_burlon, mlb, mlb_kids（11 品牌，非 12）

## 一、本轮采集概览

| 指标 | 数值 |
|------|------|
| 新采集 source 页 | 6 篇 |
| 实体页刷新（追加「近期动态刷新」段） | 11 篇（全分组覆盖） |
| 显式核对无新增品牌 | 5 篇（etudes / g_star_raw / hoka_one_one / humble_humble_r / mlb，均 08-26 已入库，本轮复核一致） |
| 织网双链 | 6 源出链 + 11 实体回链 + 概念互链 |
| 矛盾检测 | 硬冲突 0 处；ℹ️ 基准核对 4 处（均一致，无数值冲突） |
| 索引重建 | 1193 L3 条目（目标 1082+ ✅） |
| 孤岛 | 0 |

## 二、6 篇新 source 页清单（全含 结论 + 信息链 + confidence + brand_specific）

| source 页 | 品牌 | confidence | 关键新增 |
|-----------|------|-----------|----------|
| 2026-08-27_A2_king_baby_全维度动态 | king_baby | 媒体估算 | 私有估值 $2–19M 离散、中国专柜（北京西单/三里屯/广州天环）、明星种草矩阵 |
| 2026-08-27_A2_lacoste_全维度动态 | lacoste | 第三方数据 | 2026 品牌焕新、香港 Pedder 历史建筑旗舰、Plaza/Miami/Lafayette 体验营销、~€3B |
| 2026-08-27_A2_levis_全维度动态 | levis | 财报 | Q1 $1.74B(+14.1%)/Q2 $1.56B(+8%)/DTC 51%/中国 Anita Fung(Burberry)+成都太古里 |
| 2026-08-27_A2_marcelo_burlon_全维度动态 | marcelo_burlon | 媒体估算 | 授权 Farfetch→Daddato Next、FILA×Levi's 501 联名、财务缺位 |
| 2026-08-27_A2_mlb_kids_全维度动态 | mlb_kids | 财报 | F&F 中国 9603 亿韩元、门店 1078→1094、618 运动品类 #18 |
| 2026-08-27_A2_karl_lagerfeld_七匹狼中报落地 | karl_lagerfeld | 财报 | 七匹狼 2026H1 实际中报：营收 14.15 亿 / 归母 -2730 万 / 扣非 +392% |

## 三、矛盾 / 基准核对

- ⚠️ **硬冲突 0 处**。
- ℹ️ **基准核对 4 处（一致，非矛盾）**：
  1. karl_lagerfeld：2026H1 实际归母 -2730 万，落 08-26 预告区间（-1950~ -2900 万）上沿，方向一致。
  2. levis：Q2 营收 $1.56B / 有机 +6% 与本轮 source 一致。
  3. mlb：中国 2025 营收 9603 亿韩元 / Q1 3996 亿（实为 3031 亿）与 08-23 源一致（注：3031 亿韩元 Q1 已记录，无冲突）。
  4. lacoste / king_baby / marcelo_burlon / mlb_kids：均为新品牌页，无历史同指标冲突。

## 四、置信度分布（本轮 6 源）

- 财报：2（karl_lagerfeld、levis）
- 第三方数据：1（lacoste）
- 媒体估算：3（king_baby、marcelo_burlon、mlb_kids）
- brand_specific：6/6 = true

## 五、待办 / 待验证

- king_baby / marcelo_burlon 财务为私有估算，建议仅作量级参考，不纳入竞品财务基准。
- mlb_kids 独立营收/同店增长未单列，需 F&F 分部或运营方数据回填。
- karl_lagerfeld 中国分部 2026H1 是否继续减值、有无出售计划待七匹狼后续公告。

## 六、索引与提交

- master_index.json 已重建：1193 L3 条目（2026-08-27 07:08）。
- git：precise-add（6 源 + 11 实体 + master_index.json）→ commit → push main。
