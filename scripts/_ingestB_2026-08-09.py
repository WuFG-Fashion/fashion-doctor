# -*- coding: utf-8 -*-
"""
Round B ingest (2026-08-09) — L2_03/04/05
Writes raw articles, source pages, updates concept/entity/L3/index.
Follows existing wiki conventions observed in repo.
"""
import os, re

BASE = r"D:\Fashion Doctor\fashion-doctor\knowledge_base"
RAW = os.path.join(BASE, "raw", "articles")
SRC = os.path.join(BASE, "wiki", "sources")
CON = os.path.join(BASE, "wiki", "concepts")
ENT = os.path.join(BASE, "wiki", "entities")
IDX = os.path.join(BASE, "wiki", "index.md")

def w(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def r(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def links_in(s):
    return re.findall(r'\[\[([^\]]+)\]\]', s)

def base(x):
    return x.split('|')[0].split('#')[0].strip()

# ---------------------------------------------------------------------------
# Article definitions
# ---------------------------------------------------------------------------
ART = []

ART.append(dict(
    name="2026-08-09_桔尚女装_微盟AI会员复购运营",
    topic="L2_03",
    url="https://www.weimob.com / 桔尚女装公开运营报道（WebSearch 2026-08-09）",
    tags=["vip", "membership", "repurchase", "private_domain", "ai", "source"],
    links=["会员复购率提升策略", "全渠道会员一体化"],
    concepts=["会员复购率提升策略", "全渠道会员一体化"],
    l3=["L2_03_会员与VIP运营/L3_03_01_VIP分层模型/vip_tier.md",
        "L2_03_会员与VIP运营/L3_03_02_会员复购分析/2026-06-08_会员复购策略更新.md"],
    raw_body="""# 桔尚女装 微盟AI会员复购运营（原始采集 2026-08-09）

来源：微盟 / 桔尚女装公开运营报道（WebSearch 2026-08-09，Round B / L2_03）

## 关键数据
- 门店规模：约 300 家
- 会员消费金额占比（4月）：56%
- 会员整体复购率：35%
- 复购 GMV 同比增长：+40%
- 技术底座：微盟 AI 会员运营体系（统一 ID / 积分 / 权益 + 标签分层 + 自动化场景触达）

## 要点
桔尚女装以 300+ 门店借助微盟 AI 会员运营，实现会员消费占比 56%、整体复购率 35%、复购 GMV 同比 +40%。
AI 驱动精准分层与场景化复购触达，使复购显著提升。
""",
    src_body="""# 桔尚女装微盟AI会员复购运营

> **一句话摘要**：300家门店女装品牌借微盟AI会员运营，实现会员消费占比56%、复购率35%、复购GMV同比+40%。
> **来源**：微盟/桔尚女装公开运营报道（WebSearch 2026-08-09，Round B / L2_03）
> **最后更新**：2026-08-09

## 核心要点

1. 桔尚女装约 300 家门店，4月会员消费金额占比达 **56%**。
2. 整体会员**复购率 35%**，复购 GMV 同比 **+40%**。
3. 采用微盟 AI 会员运营体系（统一 ID / 积分 / 权益 + 标签分层 + 自动化触达）。
4. AI 驱动精准分层与场景化复购触达，是复购提升的核心杠杆。

## 关键数据

| 指标 | 数值 |
|------|------|
| 门店规模 | ~300 家 |
| 会员消费金额占比（4月） | **56%** |
| 会员整体复购率 | **35%** |
| 复购 GMV 同比 | **+40%** |
| 技术底座 | 微盟 AI 会员运营（标签 / 分层 / 自动化） |

## 关联页面

- [[会员复购率提升策略]]
- [[全渠道会员一体化]]

## 待办 / 待验证

> ⚠️ **数据矛盾**：本源会员**整体复购率 35%**，高于既有基准 `kb_benchmarks.json / membership.apparel_repurchase_excellent = 0.28（28%，服装复购优秀值）`。与 2026-08-07 MO&Co. 源（VIP 复购 35–45% vs 0.28）口径一致，进一步指向需上调复购优秀基准或区分 VIP 分层口径（建议在基准中新增 `vip_tier_repurchase_excellent = 0.35~0.45` 分段口径，而非直接覆盖）。
""",
    contradiction=True,
))

ART.append(dict(
    name="2026-08-09_唯品会_SVIP分层贡献与复购",
    topic="L2_03",
    url="唯品会公开财报 / 会员运营报道（WebSearch 2026-08-09）",
    tags=["vip", "membership", "svip", "repurchase", "source"],
    links=["会员复购率提升策略", "全渠道会员一体化"],
    concepts=["会员复购率提升策略", "全渠道会员一体化"],
    l3=["L2_03_会员与VIP运营/L3_03_01_VIP分层模型/vip_tier.md"],
    raw_body="""# 唯品会 SVIP分层贡献与复购（原始采集 2026-08-09）

来源：唯品会会员运营公开报道（WebSearch 2026-08-09，Round B / L2_03）

## 关键数据
- SVIP（超级会员）贡献 55% 的线上销售额
- SVIP 复购率 86%
- 付费 SVIP 会员数同比 +9%
- 高价值分层对整体 GMV 杠杆显著
""",
    src_body="""# 唯品会SVIP分层贡献与复购

> **一句话摘要**：唯品会 SVIP（超级会员）贡献 55% 线上销售额、复购率 86%，付费 SVIP 同比 +9%。
> **来源**：唯品会会员运营公开报道（WebSearch 2026-08-09，Round B / L2_03）
> **最后更新**：2026-08-09

## 核心要点

1. SVIP 贡献 **55%** 的线上销售额。
2. SVIP **复购率 86%**。
3. 付费 SVIP 会员数同比 **+9%**。
4. 高价值分层对整体 GMV 具有显著杠杆效应。

## 关键数据

| 指标 | 数值 |
|------|------|
| SVIP 贡献线上销售额 | **55%** |
| SVIP 复购率 | **86%** |
| 付费 SVIP 同比 | **+9%** |

## 关联页面

- [[会员复购率提升策略]]
- [[全渠道会员一体化]]

## 待办 / 待验证

（无矛盾：SVIP 为高端子集，kb 无对应 SVIP 基准；86% 复购属超高端会员段，与整体优秀值 28% 口径不同，不冲突。）
""",
    contradiction=False,
))

ART.append(dict(
    name="2026-08-09_中国连锁经营协会_2026会员管理报告",
    topic="L2_03",
    url="中国连锁经营协会《2026中国零售业会员管理报告》（WebSearch 2026-08-09）",
    tags=["vip", "membership", "repurchase", "report", "source"],
    links=["会员复购率提升策略", "全渠道会员一体化"],
    concepts=["会员复购率提升策略", "全渠道会员一体化"],
    l3=["L2_03_会员与VIP运营/L3_03_02_会员复购分析/2026-06-08_会员复购策略更新.md"],
    raw_body="""# 中国连锁经营协会《2026中国零售业会员管理报告》（原始采集 2026-08-09）

来源：中国连锁经营协会《2026中国零售业会员管理报告》（WebSearch 2026-08-09，Round B / L2_03）

## 关键数据
- 实施分层会员管理的企业，会员复购率平均 +42%
- 获客成本平均 -31%
- 报告明确"分层运营"为 2026 零售会员主线
""",
    src_body="""# 中国连锁经营协会《2026中国零售业会员管理报告》

> **一句话摘要**：分层会员运营使复购率 +42%、获客成本 -31%，会员分层成为零售增长核心杠杆。
> **来源**：中国连锁经营协会《2026中国零售业会员管理报告》（WebSearch 2026-08-09，Round B / L2_03）
> **最后更新**：2026-08-09

## 核心要点

1. 实施**分层会员管理**的企业，会员复购率平均 **+42%**。
2. 获客成本平均 **-31%**。
3. 报告明确"分层运营"为 2026 零售会员主线。

## 关键数据

| 指标 | 变化 |
|------|------|
| 分层会员复购率 | **+42%** |
| 获客成本 | **-31%** |

## 关联页面

- [[会员复购率提升策略]]
- [[全渠道会员一体化]]

## 待办 / 待验证

（无矛盾：为相对提升值，非绝对基准冲突；印证分层运营对复购的杠杆效应。）
""",
    contradiction=False,
))

ART.append(dict(
    name="2026-08-09_Rivo_VIP分层忠诚度ROI",
    topic="L2_03",
    url="Rivo loyalty report / 忠诚度市场研究（WebSearch 2026-08-09）",
    tags=["vip", "membership", "loyalty", "repurchase", "source"],
    links=["会员复购率提升策略", "全渠道会员一体化"],
    concepts=["会员复购率提升策略", "全渠道会员一体化"],
    l3=["L2_03_会员与VIP运营/L3_03_01_VIP分层模型/vip_tier.md"],
    raw_body="""# Rivo VIP分层忠诚度ROI（原始采集 2026-08-09）

来源：Rivo loyalty report / 忠诚度市场研究（WebSearch 2026-08-09，Round B / L2_03）

## 关键数据
- VIP 分层 ROI：1.8X
- VIP AOV：$435 vs 普通 $291（+73%）
- VIP 购买频次：3.6X
- Top5% 会员贡献 35% 收入
- 服装复购率：25–26%（美国市场均值）
- 积分兑换者复购 50% vs 非兑换者 10.7%
- 忠诚度市场 2026 达 240 亿美元
""",
    src_body="""# Rivo VIP分层忠诚度ROI

> **一句话摘要**：VIP分层带来 1.8X ROI、AOV 高 73%（$435 vs $291）、Top5% 贡献 35% 收入；服装复购率 25–26%。
> **来源**：Rivo loyalty report / 忠诚度市场研究（WebSearch 2026-08-09，Round B / L2_03）
> **最后更新**：2026-08-09

## 核心要点

1. VIP 分层 **ROI 1.8X**。
2. VIP **AOV $435 vs 普通 $291（+73%）**。
3. VIP 购买频次 **3.6X**。
4. **Top5% 会员贡献 35% 收入**。
5. 服装复购率 **25–26%**（美国市场均值）。
6. 积分兑换者复购 **50%** vs 非兑换者 **10.7%**。
7. 忠诚度市场 2026 达 **240 亿美元**。

## 关键数据

| 指标 | 数值 |
|------|------|
| VIP 分层 ROI | 1.8X |
| VIP AOV | $435（普通 $291，+73%） |
| VIP 购买频次 | 3.6X |
| Top5% 会员收入贡献 | 35% |
| 服装复购率（美国均值） | 25–26% |
| 积分兑换者复购 vs 非兑换 | 50% vs 10.7% |
| 忠诚度市场规模（2026） | 240 亿美元 |

## 关联页面

- [[会员复购率提升策略]]
- [[全渠道会员一体化]]

## 待办 / 待验证

> ⚠️ **数据矛盾**：本源服装复购率 **25–26%**，略低于既有基准 `kb_benchmarks.json / membership.apparel_repurchase_excellent = 0.28（28%，优秀线）`。口径为**美国服装市场均值**（非中国 / 非 VIP 分层），接近优秀线，待验证是否适用中国服装零售基准。
""",
    contradiction=True,
))

ART.append(dict(
    name="2026-08-09_Megaview_导购AI对练改写经验复制",
    topic="L2_04",
    url="https://blog.megaview.com/archives/32387（WebSearch 2026-08-09）",
    tags=["guide", "training", "ai", "megaview", "source"],
    links=["AI导购陪练", "导购培训闭环体系", "深维智信"],
    concepts=["AI导购陪练", "导购培训闭环体系", "深维智信"],
    l3=["L2_04_导购能力评估/L3_04_03_导购培训体系/2026-06-19_三类排名与北森全场景更新.md"],
    raw_body="""# Megaview 导购AI对练改写经验复制（原始采集 2026-08-09）

来源：blog.megaview.com/archives/32387（WebSearch 2026-08-09，Round B / L2_04）

## 关键数据
- 美妆连锁：新导购入职 3 月转化率 12% vs 老导购 28%
- 华东区 30 家门店 63 名新人对照实验
- AI 对练组日均 12.7 轮完整对话 vs 传统组 4.2 次主动开口
- "成交推进"维度首周 31 分 → 3 周 67 分
- 70% 断点发生在顾客表达犹豫后 3 秒内
- 深维智信 Megaview Agent Team（AI 顾客 / 教练 / 评估员）
""",
    src_body="""# Megaview 导购AI对练改写经验复制

> **一句话摘要**：美妆连锁用 Megaview AI 对练，新人日均 12.7 轮对话、成交推进 31→67 分，70% 断点在犹豫后 3 秒内。
> **来源**：blog.megaview.com/archives/32387（WebSearch 2026-08-09，Round B / L2_04）
> **最后更新**：2026-08-09

## 核心要点

1. 美妆连锁：新导购入职 3 月转化率 **12%** vs 老导购 **28%**。
2. 华东区 30 家门店 63 名新人对照实验。
3. AI 对练组日均 **12.7 轮**完整对话 vs 传统组 **4.2 次**主动开口。
4. "成交推进"维度首周 **31 分 → 3 周 67 分**。
5. **70% 断点**发生在顾客表达犹豫后 **3 秒内**。
6. 深维智信 Megaview **Agent Team**（AI 顾客 / 教练 / 评估员）支撑。

## 关键数据

| 指标 | 数值 |
|------|------|
| 新导购 3 月转化率 vs 老导购 | 12% vs 28% |
| AI 对练组日均对话 | 12.7 轮 |
| 传统组日均主动开口 | 4.2 次 |
| 成交推进首周→3周 | 31 → 67 分 |
| 犹豫后 3 秒内断点占比 | 70% |

## 关联页面

- [[AI导购陪练]]
- [[导购培训闭环体系]]
- [[深维智信]]

## 待办 / 待验证

（无矛盾：为场景化技能分维度评分，非 kb `megaview_conversion_boost_pct=0.18` 通用提升口径；"成交推进 31→67 分"属能力雷达子维度，不冲突。）
""",
    contradiction=False,
))

ART.append(dict(
    name="2026-08-09_Megaview_导购启动AI培训实验转化跃升",
    topic="L2_04",
    url="https://www.megaview.com/resource/archives/24420（WebSearch 2026-08-09）",
    tags=["guide", "training", "ai", "megaview", "source"],
    links=["AI导购陪练", "导购培训闭环体系", "深维智信"],
    concepts=["AI导购陪练", "导购培训闭环体系", "深维智信"],
    l3=["L2_04_导购能力评估/L3_04_03_导购培训体系/2026-06-19_三类排名与北森全场景更新.md"],
    raw_body="""# Megaview 导购启动AI培训实验转化跃升（原始采集 2026-08-09）

来源：megaview.com/resource/archives/24420（WebSearch 2026-08-09，Round B / L2_04）

## 关键数据
- 面对价格质疑，参训导购响应时间 -40%，更少直接降价
- 异议处理 >75 分导购，首月成交转化率比未参训新人近一倍
- 线下培训及陪练成本 -50%（7×24 在线陪练）
- MegaRAG 领域知识库，优秀话术 24h 同步全区域
- 区域经理看板识别需复训导购
""",
    src_body="""# Megaview 导购启动AI培训实验转化跃升

> **一句话摘要**：Megaview AI 陪练使价格质疑响应 -40%、异议 >75 分者首月转化近一倍、培训成本 -50%、经验 MegaRAG 24h 同步。
> **来源**：megaview.com/resource/archives/24420（WebSearch 2026-08-09，Round B / L2_04）
> **最后更新**：2026-08-09

## 核心要点

1. 面对价格质疑，参训导购响应时间 **-40%**，更少直接降价。
2. 异议处理 **>75 分**导购，首月成交转化率比未参训新人**近一倍**。
3. 线下培训及陪练成本 **-50%**（7×24 在线陪练）。
4. **MegaRAG** 领域知识库，优秀话术 **24h** 同步全区域。
5. 区域经理看板识别需复训导购，资源精准投放。

## 关键数据

| 指标 | 数值 |
|------|------|
| 价格质疑响应时间 | -40% |
| 异议 >75 分者首月转化 | 近未参训一倍 |
| 培训及陪练成本 | -50% |
| 优秀话术同步时效 | 24h |

## 关联页面

- [[AI导购陪练]]
- [[导购培训闭环体系]]
- [[深维智信]]

## 待办 / 待验证

（无矛盾：kb 无 megaview 成本降低基准；上岗周期 2 月 vs kb `megaview_ramp_months=1.5` 为"综合压缩值"与"达标中位"口径差，非数值冲突。）
""",
    contradiction=False,
))

ART.append(dict(
    name="2026-08-09_服装品牌商品企划五步跃迁",
    topic="L2_05",
    url="https://www.toutiao.com/article/7659258016688062986（WebSearch 2026-08-09）",
    tags=["merchandise", "planning", "otb", "assortment", "source"],
    links=["动态OTB管理", "柔性供应链与商品企划", "服装企划趋势渠道"],
    concepts=["动态OTB管理", "柔性供应链与商品企划", "服装企划趋势渠道"],
    l3=["L2_05_商品企划/L3_05_01_波段上货节奏/wave_timing.md",
        "L2_05_商品企划/L3_05_02_品类结构规划/2026-06-07_企划趋势渠道更新.md"],
    raw_body="""# 服装品牌商品企划五步跃迁（原始采集 2026-08-09）

来源：toutiao.com/article/7659258016688062986（WebSearch 2026-08-09，Round B / L2_05）

## 关键数据
- 第一步 品类角色评价（心智/规模/利润/形象/搭配）
- 第二步 价格带规划（2–3 个核心锚点，避免中段过宽）
- 第三步 3+3+3+3 滚动波段：首单 70%→40%、整体售罄 +8–12pp、折扣深度 -5–10pp、净利 +3–5pp
- 第四步 OTB 滚动决策日历：每周追/缩单 ±20%、每月品类纠偏 ±10%、每季结构复盘
- 第五步 分货与店群管理
""",
    src_body="""# 服装品牌商品企划五步跃迁

> **一句话摘要**：从经验到战略的五步跃迁，3+3+3+3 滚动波段使首单 70%→40%、售罄 +8–12pp、净利 +3–5pp。
> **来源**：toutiao.com/article/7659258016688062986（WebSearch 2026-08-09，Round B / L2_05）
> **最后更新**：2026-08-09

## 核心要点

1. **品类角色评价**：心智 / 规模 / 利润 / 形象 / 搭配，分类管理资源优先级。
2. **价格带规划**：2–3 个核心锚点，避免"中段价格带过宽"两头不讨好。
3. **3+3+3+3 滚动波段**：首单占比 **70%→40%**、整体售罄 **+8–12pp**、折扣深度 **-5–10pp**、净利 **+3–5pp**。
4. **OTB 滚动决策日历**：每周追/缩单 **±20%**、每月品类纠偏 **±10%**、每季结构复盘。
5. **分货与店群管理**：货品到对的地方，最后一公里精细化。

## 关键数据

| 指标 | 变化 |
|------|------|
| 首单占比 | 70% → 40% |
| 整体售罄率 | +8–12pp |
| 折扣深度 | -5–10pp |
| 净利率 | +3–5pp |
| OTB 周调整幅度 | 单款 ±20% |
| OTB 月纠偏 | 品类 ±10% |

## 关联页面

- [[动态OTB管理]]
- [[柔性供应链与商品企划]]
- [[服装企划趋势渠道]]

## 待办 / 待验证

（无矛盾：为相对提升值；OTB 滚动 ±20%/±10% 与 kb `otb.seasonal_deviation=0.15` 口径不同，不冲突。）
""",
    contradiction=False,
))

ART.append(dict(
    name="2026-08-09_第七在线_OTB终极指南公式与最佳实践",
    topic="L2_05",
    url="https://www.7thonline.com.cn/hangyeganhuo-2524.html（WebSearch 2026-08-09）",
    tags=["merchandise", "otb", "planning", "formula", "source"],
    links=["动态OTB管理", "柔性供应链与商品企划", "sku_fine_management|服装SKU精细化管理"],
    concepts=["动态OTB管理", "柔性供应链与商品企划", "sku_fine_management|服装SKU精细化管理"],
    l3=["L2_05_商品企划/L3_05_03_SKU生命周期管理/2026-06-06_动态OTB管理更新.md"],
    raw_body="""# 第七在线 OTB终极指南公式与最佳实践（原始采集 2026-08-09）

来源：7thonline.com.cn/hangyeganhuo-2524.html（WebSearch 2026-08-09，Round B / L2_05）

## 关键数据
- 基础公式：OTB = 计划销售额 + 计划期末库存 − 期初库存 − 已下采购订单
- 进阶：按品类（上装/下装/鞋/配件）和渠道（直营/加盟/电商）分别计算后汇总
- 动态 OTB vs 静态 OTB：本质差异是市场响应速度
- 三大功能：防过度采购 / 保障补货资金 / 联动现金流
- 案例：Aldo Group、Forever 21
""",
    src_body="""# 第七在线 OTB终极指南公式与最佳实践

> **一句话摘要**：OTB = 计划销售 + 期末库存 − 期初 − 已下订单；按品类/渠道分拆，动态 vs 静态决定响应速度。
> **来源**：7thonline.com.cn/hangyeganhuo-2524.html（WebSearch 2026-08-09，Round B / L2_05）
> **最后更新**：2026-08-09

## 核心要点

1. **基础公式**：`OTB = 计划销售额 + 计划期末库存 − 期初库存 − 已下采购订单`。
2. **进阶**：按品类（上装/下装/鞋/配件）和渠道（直营/加盟/电商）分别计算后汇总。
3. **动态 OTB vs 静态 OTB**：本质差异是市场响应速度。
4. **三大功能**：防过度采购 / 保障补货资金 / 联动现金流。
5. **案例**：Aldo Group、Forever 21 高管实践。

## 关键数据

| 维度 | 说明 |
|------|------|
| 基础 OTB 公式 | 计划销售 + 期末库存 − 期初 − 已下订单 |
| 分拆维度 | 品类 × 渠道 |
| 动态 vs 静态 | 响应速度差异 |
| 核心功能 | 防超买 / 保补货 / 联现金流 |

## 关联页面

- [[动态OTB管理]]
- [[柔性供应链与商品企划]]
- [[sku_fine_management|服装SKU精细化管理]]

## 待办 / 待验证

（无矛盾：公式与 kb `otb` 定义一致；无数值冲突。）
""",
    contradiction=False,
))

# ---------------------------------------------------------------------------
# Page update helpers
# ---------------------------------------------------------------------------
def insert_body_links(text, new_links):
    headers = ['## 关联页面', '## 关联知识']
    idx = -1
    for h in headers:
        p = text.find(h)
        if p != -1:
            idx = p
            break
    if idx == -1:
        section = '\n## 关联页面\n\n' + ''.join('- [[' + x + ']]\n' for x in new_links)
        return text.rstrip() + section + '\n'
    before = text[:idx]
    rest = text[idx:]
    nl = rest.index('\n')
    after_header = rest[nl + 1:]
    ns = after_header.find('\n## ')
    if ns == -1:
        body = after_header
        tail = ''
    else:
        body = after_header[:ns]
        tail = after_header[ns:]
    existing = [base(e) for e in links_in(body)]
    to_add = [x for x in new_links if base(x) not in existing]
    if not to_add:
        return text
    added = ''.join('- [[' + x + ']]\n' for x in to_add)
    new_rest = rest[:nl + 1] + body.rstrip('\n') + '\n' + added + '\n' + tail
    return before + new_rest

def add_fm_links(path, new_links):
    text = r(path)
    lines = text.split('\n')
    changed = False
    for i, l in enumerate(lines):
        if l.startswith('cross_refs:'):
            existing = [base(e) for e in links_in(l)]
            to_add = [x for x in new_links if base(x) not in existing]
            if to_add:
                lines[i] = l.rstrip() + ''.join(', [[' + x + ']]' for x in to_add)
                changed = True
            break
    text2 = '\n'.join(lines)
    text3 = insert_body_links(text2, new_links)
    if changed or text3 != text:
        w(path, text3)
        return True
    return False

# ---------------------------------------------------------------------------
# 1. Write raw articles + source pages
# ---------------------------------------------------------------------------
src_rows = []
for a in ART:
    # raw
    w(os.path.join(RAW, a["name"] + ".md"), a["raw_body"])
    # source frontmatter
    fm_links = ", ".join("[[" + x + "]]" for x in a["links"])
    fm = "---\n"
    fm += "type: source\n"
    fm += "title: " + a["name"].split("_", 3)[-1] + "\n"
    fm += "tags: [" + ", ".join(a["tags"]) + "]\n"
    fm += "sources: [raw/articles/" + a["name"] + ".md]\n"
    fm += "created: 2026-08-09\n"
    fm += "updated: 2026-08-09\n"
    fm += "cross_refs: [" + fm_links + "]\n"
    fm += "---\n\n"
    w(os.path.join(SRC, a["name"] + ".md"), fm + a["src_body"])
    # index row
    desc = a["name"].split("_", 3)[-1]
    suffix = a["name"].split("2026-08-09_", 1)[-1]
    summary = {
        "桔尚女装_微盟AI会员复购运营": "桔尚女装微盟AI会员复购运营：300店/会员消费占比56%/复购率35%/复购GMV+40%",
        "唯品会_SVIP分层贡献与复购": "唯品会SVIP分层：SVIP贡献55%线上销售额/复购率86%/付费SVIP+9%",
        "中国连锁经营协会_2026会员管理报告": "中国连锁经营协会2026会员管理报告：分层会员复购+42%/获客成本-31%",
        "Rivo_VIP分层忠诚度ROI": "Rivo VIP分层忠诚度：ROI 1.8X/AOV $435 vs $291(+73%)/Top5%贡献35%收入/服装复购25-26%",
        "Megaview_导购AI对练改写经验复制": "Megaview导购AI对练改写经验复制：美妆连锁/12.7轮vs4.2次/成交推进31→67/70%断点3秒内",
        "Megaview_导购启动AI培训实验转化跃升": "Megaview导购启动AI培训实验：价格质疑响应-40%/异议>75转化近一倍/成本-50%/MegaRAG 24h",
        "服装品牌商品企划五步跃迁": "服装品牌商品企划五步跃迁：3+3+3+3波段/首单70→40%/售罄+8-12pp/净利+3-5pp/OTB±20%±10%",
        "第七在线_OTB终极指南公式与最佳实践": "第七在线OTB终极指南：公式(计划销售+期末−期初−已下)/按品类渠道分拆/动态vs静态",
    }[suffix]
    tags = ", ".join(a["tags"])
    src_rows.append("| [[" + a["name"] + "]] ⭐ NEW | " + summary + " | " + tags + " |")

# ---------------------------------------------------------------------------
# 2. Update concept / entity pages (backlinks)
# ---------------------------------------------------------------------------
concept_file = {
    "会员复购率提升策略": os.path.join(CON, "会员复购率提升策略.md"),
    "全渠道会员一体化": os.path.join(CON, "全渠道会员一体化.md"),
    "AI导购陪练": os.path.join(CON, "AI导购陪练.md"),
    "导购培训闭环体系": os.path.join(CON, "导购培训闭环体系.md"),
    "深维智信": os.path.join(ENT, "深维智信.md"),
    "动态OTB管理": os.path.join(CON, "动态OTB管理.md"),
    "柔性供应链与商品企划": os.path.join(CON, "柔性供应链与商品企划.md"),
    "服装企划趋势渠道": os.path.join(CON, "服装企划趋势渠道.md"),
    "sku_fine_management|服装SKU精细化管理": os.path.join(CON, "sku_fine_management.md"),
}

# build per-concept link lists (dedup) -> backlinks point to SOURCE pages
concept_links = {}
for a in ART:
    for c in a["concepts"]:
        key = c.split("|")[0]
        concept_links.setdefault(key, [])
        if a["name"] not in concept_links[key]:
            concept_links[key].append(a["name"])

for key, links in concept_links.items():
    # map key to file: need alias-aware filename
    fname = None
    for ck, fp in concept_file.items():
        if ck.split("|")[0] == key:
            fname = fp
            break
    if fname is None:
        continue
    add_fm_links(fname, links)

# ---------------------------------------------------------------------------
# 3. L3 sync
# ---------------------------------------------------------------------------
for a in ART:
    for rel in a["l3"]:
        fp = os.path.join(BASE, rel)
        if os.path.exists(fp):
            add_fm_links(fp, [a["name"]])

# ---------------------------------------------------------------------------
# 4. Update index.md
# ---------------------------------------------------------------------------
text = r(IDX)
anchor = "### L2/L3 历史分类（只读保留）"
ai = text.index(anchor)
# idempotent: skip rows whose page already registered
new_rows = []
for row in src_rows:
    m = re.search(r'\[\[([^\]]+)\]\]', row)
    if m and ('[[' + m.group(1) + ']]') in text:
        continue
    new_rows.append(row)
if new_rows:
    block = "\n".join(new_rows) + "\n"
    new_text = text[:ai] + block + text[ai:]
else:
    new_text = text

# concept row notes (idempotent)
notes = {
    "会员复购率提升策略": " + 08-09新增:唯品会SVIP(55%&86%)/中国连锁分层复购+42%/Rivo VIP 1.8X·AOV+73%·Top5% 35%收入(桔尚复购35%见07-11)",
    "全渠道会员一体化": " + 08-09新增:桔尚会员消费占比56%/中国连锁分层复购+42%/唯品会SVIP 55%",
    "AI导购陪练": " + 08-09新增:Megaview对练改写(12.7轮/成交推进31→67)+启动实验(响应-40%/异议>75转化近一倍/成本-50%)",
    "导购培训闭环体系": " + 08-09新增:Megaview对练改写+启动实验(成本-50%/MegaRAG 24h同步)",
    "深维智信": "",  # entity not in concept index table
    "动态OTB管理": " + 08-09新增:滚动OTB日历(±20%/±10%)+第七在线OTB公式(计划销售+期末−期初−已下)",
    "柔性供应链与商品企划": " + 08-09新增:五步跃迁(首单70→40%/售罄+8-12pp)+第七在线OTB公式",
    "服装企划趋势渠道": " + 08-09新增:五步跃迁价格带2-3锚点+3+3+3+3波段",
    "sku_fine_management|服装SKU精细化管理": " + 08-09新增:第七在线OTB公式按品类/渠道分拆",
}
lines = new_text.split('\n')
for key, note in notes.items():
    if not note:
        continue
    kname = key.split("|")[0]
    for i, l in enumerate(lines):
        if l.strip().startswith('| [[' + kname + ']]') or l.strip().startswith('|[[[' + kname + ']]'):
            if note in l:
                break
            parts = l.split('|')
            if len(parts) >= 4:
                parts[2] = parts[2].rstrip() + note
                lines[i] = '|'.join(parts)
                break
new_text = '\n'.join(lines)
w(IDX, new_text)

print("DONE. sources=%d  concepts_updated=%d  l3_targets=%d" % (
    len(ART), len(concept_links), sum(len(a['l3']) for a in ART)))
print("contradictions flagged:", sum(1 for a in ART if a['contradiction']))
