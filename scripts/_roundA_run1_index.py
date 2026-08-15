# -*- coding: utf-8 -*-
import os
BASE="knowledge_base/wiki"
IDX=os.path.join(BASE,"index.md")
GEP=os.path.join(BASE,"concepts","服装行业竞争格局.md")

# 10 source rows (filename | oneline | tags)
SRC=[
("2026-08-15_LACOSTE_中国运营与财务速览_2026.md","LACOSTE 2026：Maus Frères瑞士私企/亚太+30%中国+15%/香港中环旗舰/Durable Elegance重塑","lacoste, competitor, sportswear, premium, france, source"),
("2026-08-15_Tommy_Hilfiger___PVH_中国渠道与财务速览_2026.md","Tommy Hilfiger/PVH 2026：Q1集团$2.0bn+2.1%/TH+2.8~6%/中国D2C双位数/$1.53亿收回中国直营","tommy_hilfiger, competitor, premium, usa, pvh, source"),
("2026-08-15_Levi's___LS&Co_中国战略与财务速览_2026.md","Levi's/LS&Co 2026：Q1 $1.742bn+14%/DTC 52%/中国换帅Anita Fung+成都太古里旗舰/售Dockers","levis, competitor, denim, usa, source"),
("2026-08-15_DIESEL___OTB_Group_中国运营与财务速览_2026.md","DIESEL/OTB 2026：集团€1.7bn/-4.8%/Diesel近十年最佳盈利/大中华113店/入华20年","diesel, competitor, denim, italy, otb, source"),
("2026-08-15_DKNY___G-III_中国首店与财务速览_2026.md","DKNY/G-III 2026：中国首店上海淮海路245㎡/G-III销售-7%/天猫2017+Hailey Bieber","dkny, competitor, womenswear, usa, source"),
("2026-08-15_Speedo_中国泳装市场份额与渠道速览_2026.md","Speedo 2026：中国泳装榜#1/份额15.2%→16.4%/Pentland私营/攀岚贸易代理","speedo, competitor, swimwear, uk, source"),
("2026-08-15_HOKA___Deckers_中国增长与财务速览_2026.md","HOKA/Deckers 2026：Q3 $628.9m+18.5%/中国>230店超任何市场/国际+26.8%/DTC>55%","hoka_one_one, competitor, running, usa, deckers, source"),
("2026-08-15_ellesse_中国复古潮流与渠道速览_2026.md","ellesse 2026：Pentland/网球裙天猫618爆款/NBL鞋类翻倍/女装40→60%/APAC日韩中印尼","ellesse, competitor, retro, italy, source"),
("2026-08-15_MLB_KIDS___F&F_中国亲子线速览_2026.md","MLB KIDS/F&F 2026：丰梵中国代理/大中华+35%/1400+店/服装55%鞋30%配饰15%","mlb_kids, competitor, childrenswear, korean, source"),
("2026-08-15_NAUTICA___ABG_中国运营切换速览_2026.md","NAUTICA/ABG 2026：上海荟众接替Tristate(2025 Nautica-12%)/1983航海经典/Interparfums香水至2030","nautica, competitor, menswear, usa, source"),
]

# index.md: insert before "### L2/L3 历史分类"
t=open(IDX,encoding="utf-8").read()
rows="\n".join("| [[%s]] ⭐ NEW | %s | %s |" % (fn[:-3], desc, tags) for (fn,desc,tags) in SRC)
anchor="\n### L2/L3 历史分类（只读保留）"
assert anchor in t, "anchor not found in index.md"
t=t.replace(anchor, "\n"+rows+"\n"+anchor,1)
open(IDX,"w",encoding="utf-8").write(t)
print("index.md: inserted %d source rows" % len(SRC))

# 服装行业竞争格局: append brand backlinks at end of 关联页面
g=open(GEP,encoding="utf-8").read()
brands=[
("lacoste","瑞士私企高端运动休闲，亚太+30%逆势（2026）"),
("tommy_hilfiger","PVH美式经典，中国D2C双位数+$1.53亿收回直营（2026）"),
("levis","丹宁鼻祖，DTC 52%+中国换帅反弹（2026）"),
("diesel","OTB意大利高端丹宁，大中华113店入华20年（2026）"),
("dkny","G-III都市生活方式，中国首店上海淮海路（2026）"),
("speedo","Pentland专业泳装中国#1，份额15.2%→16.4%（2026）"),
("hoka_one_one","Deckers厚底跑鞋，中国>230店破圈潮流（2026）"),
("ellesse","Pentland运动复古，网球裙天猫618爆款（2026）"),
("mlb_kids","F&F亲子线，借MLB势能大中华+35%（2026）"),
("nautica","ABG航海经典，上海荟众接替Tristate（2026）"),
]
links="\n".join("- [[%s]] — %s" % (k,d) for (k,d) in brands)
if g.endswith("\n"):
    g=g+links+"\n"
else:
    g=g+"\n"+links+"\n"
open(GEP,"w",encoding="utf-8").write(g)
print("服装行业竞争格局: appended %d brand backlinks" % len(brands))
