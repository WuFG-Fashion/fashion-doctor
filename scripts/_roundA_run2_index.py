# -*- coding: utf-8 -*-
"""Round A Run 2 — 登记 8 个 source 页到 index.md，并向 服装行业竞争格局 追加 8 品牌回链。"""
import os, re

IDX="knowledge_base/wiki/index.md"
COMP="knowledge_base/wiki/concepts/服装行业竞争格局.md"

# (source_md_filename, 摘要, tags)
SOURCES=[
 ("2026-08-15_ADLV_acme_de_la_vie_中国门店与品牌速览_2026.md",
  "ADLV/acme de la vie 2026：韩国双胞胎2017/大脸宝宝/中国约14店(上海MOHO天津长春大连沈阳)/深圳大悦城待开",
  "adlv, competitor, streetwear, korean, source"),
 ("2026-08-15_AWOKEN_TIME_中国潮流集合店门店与运营速览_2026.md",
  "AWOKEN TIME 2026：武汉800㎡旗舰(武商MALL)/多店集群/襄阳宜昌南昌外拓/上海泗泾签约/咖啡+潮玩场景店",
  "awoken_time, competitor, streetwear, china, source"),
 ("2026-08-15_AWOKEN_SPACE_中国潮流副线速览_2026.md",
  "AWOKEN SPACE 2026：AWOKEN体系'空间/场景'副线，与AWOKEN TIME同源/武汉集群/离散数据有限",
  "awoken_space, competitor, streetwear, china, source"),
 ("2026-08-15_Dickies___VF_中国工装市场与出售速览_2026.md",
  "Dickies/VF 2026：1922美式工装/874经典/VF 2017收购并于2026Q3出售/中国2007子公司/199-599中端",
  "dickies, competitor, workwear, usa, source"),
 ("2026-08-15_Études_Studio_法国艺术时装屋与2030蓝图_2026.md",
  "Études Studio 2026：法国艺术时装屋(非韩妆)/2012巴黎/80伙伴30市场/2030五倍+DTC20→45%/皮具扩展",
  "etudes, competitor, designer, french, source"),
 ("2026-08-15_G-Star_RAW_中国丹宁运营与渠道速览_2026.md",
  "G-Star RAW 2026：荷兰丹宁1989/极星服饰上海运营/近150网点60+城市/Raw Denim先驱/京东旗舰",
  "g_star_raw, competitor, denim, netherlands, source"),
 ("2026-08-15_HumbleHumbleR_谦而不卑_中国新锐男装速览_2026.md",
  "HumbleHumbleR 2026：2025本土新锐男装/谦而不卑/首店宁波3天46万/宁波阪急臻选店/武汉长沙杭州拓",
  "humble_humble_r, competitor, streetwear, china, source"),
 ("2026-08-15_KING_BABY_中国摇滚银饰与渠道速览_2026.md",
  "KING BABY 2026：2000洛杉矶摇滚银饰/金北陛上海运营/中国超10旗舰(北京西单大悦城)/厦门K11",
  "king_baby, competitor, jewelry, usa, source"),
]

BACKLINKS=[
 ("adlv","韩国无性别潮牌，中国约14店(上海MOHO/天津/长春等)，大脸宝宝破圈(2026)"),
 ("awoken_time","中国本土潮流集合店，武汉800㎡旗舰+多店集群，咖啡潮玩场景店(2026)"),
 ("awoken_space","中国AWOKEN体系'空间/场景'副线，与AWOKEN TIME同源(2026)"),
 ("dickies","美国百年工装(874)，VF 2017收购并于2026Q3出售，中国中端(2026)"),
 ("etudes","法国艺术时装屋(非韩妆)，2012巴黎/2030五倍+DTC45%(2026)"),
 ("g_star_raw","荷兰丹宁Raw Denim先驱，极星服饰上海运营，中国近150网点(2026)"),
 ("humble_humble_r","2025本土新锐男装'谦而不卑'，首店宁波3天46万，高潜待验证(2026)"),
 ("king_baby","美国摇滚银饰，金北陛上海运营，中国超10旗舰(2026)"),
]

# ---- index.md: insert source rows after the NAUTICA Run1 source line ----
idx=open(IDX,encoding="utf-8").read()
anchor="2026-08-15_NAUTICA___ABG_中国运营切换速览_2026"
assert anchor in idx, "Run1 nautica source anchor missing in index.md"
ins_lines=[]
for fn,summ,tags in SOURCES:
    ins_lines.append("| [[%s]] ⭐ NEW | %s | %s |" % (fn[:-3], summ, tags))
insert_block="\n".join(ins_lines)
idx=idx.replace(anchor, anchor+"\n"+insert_block, 1)
open(IDX,"w",encoding="utf-8").write(idx)
print("index.md: inserted", len(SOURCES), "source rows after nautica anchor.")

# ---- 服装行业竞争格局.md: append backlinks at end of 关联页面 section ----
comp=open(COMP,encoding="utf-8").read()
m=re.search(r"(## 关联页面.*?)(\n## |\Z)",comp,re.S)
assert m, "关联页面 section not found"
sec=m.group(1)
added=0
for key,desc in BACKLINKS:
    bullet="- [[%s]] — %s" % (key,desc)
    if bullet not in sec:
        sec=sec.rstrip("\n")+"\n"+bullet+"\n"
        added+=1
comp=comp[:m.start(1)]+sec+comp[m.end(1):]
open(COMP,"w",encoding="utf-8").write(comp)
print("服装行业竞争格局: appended", added, "backlinks.")
PY_DONE=1
print("OK")
