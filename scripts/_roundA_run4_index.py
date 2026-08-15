# -*- coding: utf-8 -*-
"""Round A Run4 索引登记：
1) index.md：在 cabbeen 来源行之后插入 11 个 R4 刷新 source 行。
2) 服装行业竞争格局.md：向 关联页面 追加缺失的 8 个品牌回链
   （cabbeen/peacebird/karl_lagerfeld/salomon/crocs/two_am/ariose_years/dekashell），
   用 "- [[key]]" 子串守卫，避免与既有的 chuu/mlb/trussardi 回链重复。
"""
import os, re

IDX="knowledge_base/wiki/index.md"
COMP="knowledge_base/wiki/concepts/服装行业竞争格局.md"

# 11 R4 source rows (filename, 说明, tags) — 插入 index.md 来源库
SRC_ROWS=[
 ("2026-08-15_R4_卡宾2026最新动态.md",
  "卡宾 2026H1 毛利率 46.3% 亮点但经营溢利 -24.7%；8 月马来 Sunway 新店、AI 虚拟试穿、海外试水（R4 全量覆盖刷新）",
  "cabbeen, competitor, menswear, core, hk_listed, R4_refresh, source"),
 ("2026-08-15_R4_太平鸟2026H1动态.md",
  "太平鸟 2026H1 营收 28.78 亿(-0.72%)/归母 1.02 亿(+30.89%)/扣非 5071 万(+269.91%)；净关店 137 家、增长靠非经常性（R4 全量覆盖刷新）",
  "peacebird, competitor, womenswear, a_share, core, R4_refresh, source"),
 ("2026-08-15_R4_楚萨迪2025业绩重启.md",
  "Trussardi 2025 营收 €29M(+70%) 但 EBITDA 亏 €1M（重建期）；Miroglio 收购、11 店、中东/游艇延伸（R4 全量覆盖刷新）",
  "trussardi, competitor, luxury, italy, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_卡尔拉格斐2026中国.md",
  "Karl Lagerfeld 2026H1 营收 1.88 亿/净利 277 万(+147.3%) 扭亏；七匹狼代理、中国 54 店、快闪营销（R4 全量覆盖刷新）",
  "karl_lagerfeld, competitor, luxury, germany, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_萨洛蒙2026Q1中国.md",
  "Salomon 亚玛芬 2026Q1 户外 +42% 超始祖鸟成增长火车头；中国门店 302 净 +45、大店模型（R4 全量覆盖刷新）",
  "salomon, competitor, sportswear, outdoor, france, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_卡骆驰2026Q2中国.md",
  "Crocs 2026Q2 核心品牌首破 $1B/中国双位数增长；芭蕾风破圈但白牌平替冲击高价联名（R4 全量覆盖刷新）",
  "crocs, competitor, footwear, usa, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_MLB_FF_2026中国万亿.md",
  "MLB(F&F) 2026 中国法人预计破 1 万亿韩元、门店 1078→1094；Discovery 第二曲线（R4 全量覆盖刷新）",
  "mlb, competitor, streetwear, korean_wave, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_2AM卡宾3D打印鞋.md",
  "2AM 卡宾旗下 3D 打印鞋履年轻线，占营收 4.1%；2026-03 吉隆坡 The Starhill 快闪出海（R4 全量覆盖刷新）",
  "two_am, competitor, streetwear, footwear, cabbeen_sub, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_CHUU_2026退潮样本.md",
  "CHUU 韩潮快时尚 2026 初 300+ 店、赵露思代言未破圈；声量≠转化、平替分流（R4 全量覆盖刷新）",
  "chuu, competitor, womenswear, korean_wave, fast_fashion, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_艾诺丝雅诗2026动态.md",
  "艾诺丝雅诗 杭州爱唯(2025-12 更名)中高端女装 1800+ 店/年销约 50 亿；AW PROJECT 轻奢上探（R4 全量覆盖刷新）",
  "ariose_years, competitor, womenswear, premium, focus_brand, R4_refresh, source"),
 ("2026-08-15_R4_迪卡轩2026春季.md",
  "迪卡轩 杭州旭弘轻淑女装 600+ 店；2026 春季'无界映像'联名艺术家 Imke Ligthart（R4 全量覆盖刷新）",
  "dekashell, competitor, womenswear, light_elegant, focus_brand, R4_refresh, source"),
]

# 8 条缺失回链（desc 不含"R4"前缀以避免与既有 chuu/mlb/trussardi 重复）
BACKLINKS=[
 ("cabbeen", "双核之一，2026H1 营收 4.53 亿(+7.24%)/毛利率 46.3%/经营溢利 -24.7%/存货周转 246 天；设计师差异化样本（R4 刷新）"),
 ("peacebird", "双核之一，2026H1 营收 28.78 亿(-0.72%)/归母 1.02 亿(+30.89%)/净关店 137 家；规模龙头（R4 刷新）"),
 ("karl_lagerfeld", "七匹狼代理轻奢，2026H1 营收 1.88 亿/净利 277 万(+147.3%) 扭亏，中国 54 店（R4 刷新）"),
 ("salomon", "亚玛芬旗下，2026Q1 户外 +42% 超始祖鸟成增长火车头，中国门店 302 净 +45（R4 刷新）"),
 ("crocs", "洞洞鞋，2026Q2 核心品牌首破 $1B/中国双位数增长，芭蕾风破圈但平替冲击（R4 刷新）"),
 ("two_am", "卡宾旗下 3D 打印鞋履年轻线，占营收 4.1%，马来快闪出海（R4 刷新）"),
 ("ariose_years", "杭州爱唯中高端女装，1800+ 店/年销约 50 亿，AW PROJECT 轻奢上探（R4 刷新）"),
 ("dekashell", "杭州旭弘轻淑女装，600+ 店/2026 春季'无界映像'艺术联名（R4 刷新）"),
]

# ---- index.md 插入 source 行 ----
idx=open(IDX,encoding="utf-8").read()
anchor="2026-08-15_卡宾2026中期业绩与2025年报"
assert anchor in idx, "cabbeen source anchor missing in index.md"
ins="\n".join("| [[%s]] ⭐ NEW | %s | %s |" % (fn[:-3], desc, tags) for fn,desc,tags in SRC_ROWS)
idx=idx.replace(anchor, anchor+"\n"+ins, 1)
open(IDX,"w",encoding="utf-8").write(idx)
print("index.md: inserted %d R4 source rows after cabbeen anchor." % len(SRC_ROWS))

# ---- 服装行业竞争格局.md 追加缺失回链 ----
comp=open(COMP,encoding="utf-8").read()
m=re.search(r"(## 关联页面.*?)(\n## |\Z)",comp,re.S)
assert m, "关联页面 section not found"
sec=m.group(1)
added=0
for key,desc in BACKLINKS:
    guard="- [[%s]]"%key
    if guard not in sec:
        bullet="- [[%s]] — %s" % (key,desc)
        sec=sec.rstrip("\n")+"\n"+bullet+"\n"
        added+=1
comp=comp[:m.start(1)]+sec+comp[m.end(1):]
open(COMP,"w",encoding="utf-8").write(comp)
print("服装行业竞争格局: appended %d backlinks (guarded by - [[key]])." % added)

print("OK")
