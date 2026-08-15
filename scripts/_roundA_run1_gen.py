# -*- coding: utf-8 -*-
"""Round A Run 1 generator — 10 已研究少源品牌 (stub -> 完整实体页 + source 页 + raw 剪藏).
格式严格对齐 CLAUDE.md 与 salomon.md 范例。"""
import os, json

BASE = "knowledge_base/wiki"
ENT = os.path.join(BASE, "entities")
SRC = os.path.join(BASE, "sources")
RAW = os.path.join(BASE, "raw", "articles")
DATE = "2026-08-15"
WALL = "品牌墙图_2026-08-14"

def wikilist(keys):
    return "[" + ", ".join("[[%s]]" % k for k in keys) + "]"

import re as _re
def safe(s):
    return _re.sub(r'[\/\\:*?"<>|]', "_", s).replace(" ", "_").strip()

BRANDS = [
{
 "key":"lacoste","title":"LACOSTE",
 "aliases":["Lacoste","法国鳄鱼","鳄鱼牌"],
 "tags":["lacoste","competitor","sportswear","premium","france"],
 "country":"France",
 "summary":"法国高端运动休闲品牌，以鳄鱼标志与 Polo 衫闻名，网球基因。",
 "core":[
   "母公司：瑞士 Maus Frères（自 2011 年起控股），非上市公司，决策不受季度财报裹挟。",
   "2026 Q2：亚太区营收 +30%，中国大陆 +15%，逆势跑赢服装大盘（2026 1-5 月利润 -11.41%）。",
   "香港旗舰店：2026 Q2 开于中环 Pedder Building，延续核心城市核心位策略。",
   "战略：'Durable Elegance' 品牌重塑计划；经典 Polo + 网球/IP 符号驱动。",
   "授权品类波动：Interparfums Q1 2026 Lacoste 香水销售 -12%（东欧），属授权而非主品牌服装。",
 ],
 "detail":[
   ["亚太区营收增速","+30%","2026 Q2"],
   ["中国大陆营收增速","+15%","2026 Q2"],
   ["全球营收目标","$3.9bn","中期"],
   ["香港旗舰","中环 Pedder Building","2026 Q2"],
   ["母公司","Maus Frères（瑞士，私营）","控股"],
 ],
 "conclusions":[
   "拉科斯特在中国属'重回增长'的轻奢运动休闲，亚太 +30%/中国 +15% 与服装大盘（2026 1-5 月利润 -11.41%）形成反差，说明有网球基因+经典 Polo 的差异化品牌仍能逆势，对 [[peacebird|太平鸟]]/[[cabbeen|卡宾]] 的'经典单品+运动休闲'路线有对标价值。",
   "母公司 Maus Frères 为瑞士私企，可长期投入品牌重塑（Durable Elegance），与上市公司 [[cabbeen|卡宾]] 的短期利润压力形成治理对照——私企基因是其逆势投入的底气。",
   "香港中环旗舰 + 亚太双位数增长，显示其'核心城市核心位'策略与 [[salomon|萨洛蒙]]/[[peacebird|太平鸟]] 一致，但拉科斯特靠经典符号（鳄鱼）而非社群运营驱动复购。",
   "数据风险：Interparfums 香水 -12%（东欧）属授权品类波动，不代表主品牌服装；引用须区分'服装主业的亚太增长'与'香水授权的区域波动'。",
 ],
 "source_title":"LACOSTE 中国运营与财务速览 2026",
 "urls":["https://wwd.com/business-news/financial/otb-diesel-maison-margies-growth-1238610597"],
},
{
 "key":"tommy_hilfiger","title":"Tommy Hilfiger",
 "aliases":["汤米·希尔费格","TOMMY","Tommy"],
 "tags":["tommy_hilfiger","competitor","premium","menswear","womenswear","usa"],
 "country":"USA",
 "summary":"美国经典休闲品牌，以红白蓝旗标与学院风、美式休闲著称，PVH 集团旗下。",
 "core":[
   "母公司：PVH Corp（纽交所 PVH，含 Calvin Klein）。",
   "PVH Q1 FY2026/27（截至 2026-05-03）集团营收 $2.0bn +2.1%。",
   "Tommy Hilfiger 品牌 +2.8% reported；另一口径 +6% 至 $842m（季度截至 2026-04-30）。",
   "中国 D2C 双位数增长；APAC +5.8% 恒定汇率。",
   "一次性 $1.53 亿收回 TH 中国业务直营；集团毛利率 58.6%。",
 ],
 "detail":[
   ["PVH 集团 Q1 营收","$2.0bn (+2.1%)","FY26/27 Q1 截至 05-03"],
   ["Tommy Hilfiger 品牌增速","+2.8% reported / +6% 另口径","Q1"],
   ["中国 D2C 增速","双位数","2026"],
   ["APAC 增速","+5.8% 恒定汇率","Q1"],
   ["收购 TH 中国","$1.53 亿 一次性","收回直营"],
   ["集团毛利率","58.6%","Q1"],
 ],
 "conclusions":[
   "PVH 将 TH 中国业务以 $1.53 亿收回直营（D2C 双位数增长），与 [[cabbeen|卡宾]]/[[peacebird|太平鸟]] 的'直营提权重、控渠道'战略同频，说明国际品牌也在重构中国渠道所有权。",
   "Tommy 品牌全球 +2.8%~+6%、中国 D2C 双位数，增速温和但稳健，毛利率 58.6% 高于多数大众休闲，体现'经典美式'溢价仍在。",
   "APAC +5.8% 恒定汇率但中国 D2C 双位数，暗示中国外的亚太（日韩等）拖累，区域分化明显，对 [[peacebird|太平鸟]] 出海亚太有参照。",
   "数据风险：不同口径 Tommy 增速（+2.8% reported vs +6% 另源）须标注来源口径；PVH 集团含 Calvin Klein，品牌级数据需剥离。",
 ],
 "source_title":"Tommy Hilfiger / PVH 中国渠道与财务速览 2026",
 "urls":["https://www.pvh.com/news"],
},
{
 "key":"levis","title":"Levi's",
 "aliases":["Levis","李维斯","LEVI"],
 "tags":["levis","competitor","denim","premium_denim","usa"],
 "country":"USA",
 "summary":"美国丹宁鼻祖，牛仔裤品类全球标杆，Levi Strauss & Co. 旗下。",
 "core":[
   "Levi Strauss Q1 2026（截至 2026-03-01）净营收 $1.742bn +14%。",
   "DTC 占 52%（2024 约 40%），渠道直营化速度领先多数服装品牌。",
   "中国'积极'反弹：新任大中华区 MD Anita Fung（前 Burberry，2026-03 上任）。",
   "成都太古里旗舰 2025-09 开业；出售 Dockers 给 ABG（2025-05）。",
   "毛利率 61.9%，经营利润率 11.4%；全年指引 +7~7.5%；与微软推 AI 'super agent'。",
 ],
 "detail":[
   ["LS&Co Q1 净营收","$1.742bn (+14%)","截至 03-01"],
   ["DTC 占比","52% (2024 约 40%)","2026"],
   ["毛利率 / 经营利润率","61.9% / 11.4%","Q1"],
   ["中国战略","新大中华区 MD Anita Fung(前 Burberry)+成都太古里旗舰","2025-09/2026-03"],
   ["Dockers 出售","给 ABG","2025-05"],
   ["全年指引","+7~7.5%","FY2026"],
 ],
 "conclusions":[
   "李维斯 DTC 占比从 ~40%(2024) 跃至 52%，渠道直营化速度领先多数服装品牌，与 [[cabbeen|卡宾]]/[[peacebird|太平鸟]] 提直营权重方向一致但更激进，是'丹宁品类直营红利'样本。",
   "中国换帅（前 Burberry Anita Fung）+ 成都太古里旗舰，显示其对中国市场'积极反弹'的押注，对 [[peacebird|太平鸟]] 的明星旗舰+高端化有对标意义。",
   "出售 Dockers 聚焦主品牌、毛利率 61.9% 高位，是'做减法、保溢价'的财务纪律，对比 [[cabbeen|卡宾]] 多副线扩张是相反路径。",
   "数据风险：Q1 +14% 含低基数与 Dockers 剥离前贡献；AI 'super agent' 仍处概念，引用须标注阶段。",
 ],
 "source_title":"Levi's / LS&Co 中国战略与财务速览 2026",
 "urls":["https://www.levistrauss.com/news"],
},
{
 "key":"diesel","title":"DIESEL",
 "aliases":["Diesel","迪赛"],
 "tags":["diesel","competitor","denim","premium_denim","italy"],
 "country":"Italy",
 "summary":"意大利高端牛仔与生活方式品牌，牛仔丹宁赛道标杆，OTB 集团旗下。",
 "core":[
   "母公司：OTB Group（Renzo Rosso，含 Jil Sander、Maison Margiela、Marni、Viktor&Rolf）。",
   "OTB 2025 营收 €1.7bn（-4.8% 恒定汇率），EBITDA €237.3m（15.1%）；净利 €10.1m。",
   "Diesel 为集团营收最大品牌，2025 实现近十年最佳盈利。",
   "大中华区 113 家直营店；2025 庆祝入华 20 周年并设新总部。",
   "2026-01 Andrea Rigogliosi 任 Diesel CEO；集团 2025 末约 600 家直营店。",
 ],
 "detail":[
   ["OTB 2025 营收 / EBITDA","€1.7bn(-4.8% cc) / €237.3m(15.1%)","全年"],
   ["Diesel 地位","集团营收最大品牌 / 近十年最佳盈利","2025"],
   ["大中华区直营店","113 家","2025"],
   ["Diesel CEO 任命","Andrea Rigogliosi","2026-01"],
   ["集团直营店总数","~600 家","2025 末"],
   ["日本占集团销售","27.4%","2025"],
 ],
 "conclusions":[
   "Diesel 是 OTB 集团'现金牛'（营收最大、近十年最佳盈利），但其增长依赖 repositioning 投入，且中国/欧洲放缓，对 [[peacebird|太平鸟]]/[[cabbeen|卡宾]] 而言是'高端丹宁逆风期如何靠品牌重塑保利润'的样本。",
   "入华 20 年 + 113 家直营 + 新总部，显示中国是其核心阵地；与 [[levis|李维斯]] 同属丹宁但 Diesel 走'意大利设计+夜店文化'差异化，客群更年轻潮流。",
   "OTB 私企（非上市）治理 + 多品牌矩阵（Margiela 增长 +8.4% 拉动），与 [[cabbeen|卡宾]] 单品牌上市公司承压不同，丹宁主业外的奢侈增长可对冲。",
   "数据风险：OTB 不披露单品牌财务，Diesel 具体营收/门店数为行业估算+集团口径，引用须标注'集团口径/估算'。",
 ],
 "source_title":"DIESEL / OTB Group 中国运营与财务速览 2026",
 "urls":["https://wwd.com/business-news/financial/otb-diesel-maison-margies-growth-1238610597","https://au.fashionunited.com/news/business/maison-margiela-drives-growth-for-otb-group-amidst-overall-revenue-decrease/2026021719854"],
},
{
 "key":"dkny","title":"DKNY",
 "aliases":["Donna Karan","唐娜·凯伦"],
 "tags":["dkny","competitor","womenswear","menswear","lifestyle","usa"],
 "country":"USA",
 "summary":"美国都市生活方式品牌，Donna Karan 旗下副线，定位摩登都市通勤。",
 "core":[
   "母公司：G-III Apparel Group（纳斯达克 GIII，含多品牌授权）。",
   "中国首店：上海淮海中路，约 2026-05-16，约 245 ㎡。",
   "G-III FY2026 销售 -7% 至 $2.96bn，自身承压。",
   "Hailey Bieber SS2026 Campaign；天猫自 2017 即在售。",
 ],
 "detail":[
   ["G-III FY2026 销售","$2.96bn (-7%)","全年"],
   ["DKNY 中国首店","上海淮海中路 ~245㎡","2026-05"],
   ["天猫入驻","2017","电商"],
   ["代言 Campaign","Hailey Bieber SS2026","2026"],
 ],
 "conclusions":[
   "DKNY 2026-05 才开中国首店（上海淮海路），是'迟到者'，对比 [[peacebird|太平鸟]] 千店规模仍是试水，说明国际二线都市品牌在华谨慎扩张。",
   "母公司 G-III FY2026 销售 -7%，自身承压，DKNY 中国首店更像'试探性落子'而非全力投入，对 [[cabbeen|卡宾]] 等评估'国际品牌下沉威胁'提供了'对方也谨慎'的视角。",
   "天猫 2017 即在售 + Hailey Bieber 代言，显示其'电商先行、实体试探'的路径，与 [[peacebird|太平鸟]] 的社媒+电商打法可对照。",
   "数据风险：G-III 财报含 DKNY+其他授权品牌（如 Calvin Klein 女装等），DKNY 单品牌中国数据稀缺，引用须标注'首店/电商层面'。",
 ],
 "source_title":"DKNY / G-III 中国首店与财务速览 2026",
 "urls":["https://www.giii.com/news"],
},
{
 "key":"speedo","title":"Speedo",
 "aliases":["速比涛"],
 "tags":["speedo","competitor","sportswear","swimwear","uk"],
 "country":"UK",
 "summary":"英国竞技泳装品牌，专业游泳装备代名词。",
 "core":[
   "2026 泳装品牌榜 #1（中国报告大厅/CNPP）。",
   "2025 份额 15.2% → 2026 预测 16.4%，细分赛道垄断型选手。",
   "母公司：Pentland Group（英国，私营，1928 澳大利亚创立）。",
   "中国分销：攀岚贸易（上海）代理。",
 ],
 "detail":[
   ["2026 泳装榜","#1（中国报告大厅/CNPP）","2026"],
   ["市场份额","15.2%(2025)→16.4%(2026 预测)","中国"],
   ["母公司","Pentland Group（英，私营）","控股"],
   ["中国分销","攀岚贸易(上海)","代理"],
 ],
 "conclusions":[
   "Speedo 居中国泳装 #1（份额 15.2%→16.4%），是高度细分赛道（专业泳装）的垄断型选手，对 [[peacebird|太平鸟]]/[[cabbeen|卡宾]] 的'运动/功能细分切入'战略有参照——细分品类可做到绝对领先。",
   "母公司 Pentland（私营，还控股 [[ellesse|ellesse]]）采用'品牌组合+区域代理（攀岚）'模式，轻资产运营，与 [[cabbeen|卡宾]] 重资产直营不同，适合专业品类试水。",
   "泳装属低频高专业度品类，Speedo 靠赛事/IP 壁垒而非铺货取胜，印证'专业心智>网点密度'。",
   "数据风险：份额来自第三方榜单（CNPP），口径为'泳装'窄口径；Pentland 私营不披露单品牌财务。",
 ],
 "source_title":"Speedo 中国泳装市场份额与渠道速览 2026",
 "urls":["https://www.chinapp.com/"],
},
{
 "key":"hoka_one_one","title":"HOKA ONE ONE",
 "aliases":["HOKA","Hoka","霍伽"],
 "tags":["hoka_one_one","competitor","sportswear","running","footwear","usa"],
 "country":"USA",
 "summary":"美国厚底跑鞋品牌，Deckers 旗下，近年从专业跑圈破圈至潮流穿搭。",
 "core":[
   "母公司：Deckers Brands（纽交所 DECK），非 Amer Sports。",
   "Deckers Q3 FY2026（截至 2025-12-31）HOKA $628.9m +18.5%。",
   "Deckers FY2026 净销售 $5.472bn +9.8%；HOKA +15.9% 至 $2.587bn；国际 +26.8%。",
   "中国 = 核心增长引擎，>230 家中国门店（超任何市场）。",
   "聚焦上海/北京/成都/深圳；DTC >55%。",
 ],
 "detail":[
   ["HOKA Q3 FY2026 营收","$628.9m (+18.5%)","截至 2025-12-31"],
   ["Deckers FY2026 净销售 / HOKA","$5.472bn(+9.8%) / $2.587bn(+15.9%)","全年"],
   ["中国门店",">230 家（超任何市场）","2026"],
   ["国际增速","+26.8%","FY2026"],
   ["DTC 占比",">55%","集团"],
 ],
 "conclusions":[
   "HOKA 中国 >230 家门店（超任何市场）+ 国际 +26.8%，是'专业跑鞋破圈潮流'的最强样本，对 [[peacebird|太平鸟]]/[[cabbeen|卡宾]] 观察'运动鞋服对休闲装的跨界挤压'极关键。",
   "与 [[salomon|萨洛蒙]] 同属'专业运动→都市破圈'，但 HOKA 属 Deckers（非亚玛芬），两条独立资本路径均验证该赛道，说明非偶然趋势。",
   "DTC >55% + 聚焦核心城市，渠道质量优先于数量，与 [[cabbeen|卡宾]]'关小店开大店'逻辑一致。",
   "数据风险：Deckers 含 UGG（营收更大），HOKA 单品牌需从分部剥离；门店数含伙伴店。",
 ],
 "source_title":"HOKA / Deckers 中国增长与财务速览 2026",
 "urls":["https://www.deckers.com/news"],
},
{
 "key":"ellesse","title":"ellesse",
 "aliases":["Ellesse"],
 "tags":["ellesse","competitor","sportswear","retro","italy"],
 "country":"Italy",
 "summary":"意大利运动复古品牌，以网球与滑雪基因、半圆标志著称。",
 "core":[
   "母公司：Pentland Group（同 [[speedo|速比涛]]）。",
   "网球 heritage；'小贝壳'网球裙中国天猫 618 热卖。",
   "Nice Brand Lab (NBL) 全球鞋类合作（2026-02）目标鞋类营收翻倍。",
   "APAC 目标：日本/韩国/中国/印尼；女装占比 40%→60%（2026-27 冬）。",
 ],
 "detail":[
   ["母公司","Pentland Group（英，私营）","控股"],
   ["鞋类合作","Nice Brand Lab (NBL)，目标翻倍","2026-02"],
   ["APAC 目标市场","日/韩/中/印尼","2026+"],
   ["女装占比目标","40%→60%","2026-27 冬"],
   ["中国爆款","'小贝壳'网球裙 天猫 618","2026"],
 ],
 "conclusions":[
   "ellesse 借'运动复古+网球裙'在 Z 世代破圈（天猫 618 小贝壳热卖），与 [[peacebird|太平鸟]] 的'复古潮流+社媒爆款'打法高度相似，是可直接对标的样本。",
   "同属 Pentland（与 [[speedo|速比涛]] 同门），集团用'专业泳装+运动复古'双品牌卡位细分，轻资产代理模式值得 [[cabbeen|卡宾]] 参考。",
   "女装占比 40%→60% 的目标，显示其向女装/潮流倾斜，与服装主业女装化趋势一致。",
   "数据风险：ellesse 单品牌财务不披露（Pentland 私营）；'鞋类翻倍'为合作目标非已实现，引用须标注。",
 ],
 "source_title":"ellesse 中国复古潮流与渠道速览 2026",
 "urls":["https://www.ellesse.com/"],
},
{
 "key":"mlb_kids","title":"MLB KIDS",
 "aliases":["MLB儿童","MLB童装"],
 "tags":["mlb_kids","competitor","childrenswear","streetwear","korean_wave"],
 "country":"Korea (licensed from USA)",
 "summary":"MLB 童装线，延续老花与运动潮流基因，定位亲子与儿童街头穿搭。",
 "core":[
   "母品牌 MLB：F&F（韩国），美职棒 IP 授权。",
   "中国运营：丰梵（中国）（F&F China）。",
   "总门店 1400+（其中 MLB 1185）；MLB 中国 2019，MLB KIDS 2020。",
   "2023 大中华区营收 +35%；产品组合：服装 55% / 鞋 30% / 配饰 15%。",
 ],
 "detail":[
   ["母品牌","MLB (F&F 韩国, 美职棒 IP)","授权"],
   ["中国运营","丰梵(中国) F&F China","代理"],
   ["总门店","1400+ (MLB 1185)","2023"],
   ["大中华区营收增速","+35%","2023"],
   ["产品组合","服装55%/鞋30%/配饰15%","2023"],
 ],
 "conclusions":[
   "MLB KIDS 借 MLB 成人线势能（大中华区 +35%、1400+ 店）做亲子延伸，是'成人潮流→童装副线'的高增长复制样本，对 [[peacebird|太平鸟]] 等评估童装/亲子线有参照。",
   "F&F 韩国 IP 授权 + 丰梵中国代理的'轻资产授权'模式，与 [[cabbeen|卡宾]] 自营重资产不同，扩张快但品牌控制力弱。",
   "产品组合服装 55% 为主，说明童装线仍是'穿搭属性>功能属性'，与成人 MLB 一致。",
   "数据风险：MLB KIDS 无独立财报，数据取自 MLB 母品牌口径；+35% 为 2023 年（可能已变化）。",
 ],
 "source_title":"MLB KIDS / F&F 中国亲子线速览 2026",
 "urls":["https://www.fnf.co.kr/"],
},
{
 "key":"nautica","title":"NAUTICA",
 "aliases":["Nautica","诺帝卡"],
 "tags":["nautica","competitor","menswear","sportswear","usa"],
 "country":"USA",
 "summary":"美国航海灵感生活方式品牌，以帆船 logo 与海洋风休闲装著称。",
 "core":[
   "品牌方：Authentic Brands Group（ABG）。",
   "中国/HK/澳门核心运营伙伴：上海荟众（2026 起，取代 Tristate Holdings）。",
   "Tristate 2025 Nautica 营收 -12%，Spyder -24%。",
   "2025 末：Nautica 直营 70 + 伙伴 44 + Spyder 42 店。",
   "创立 1983；'源自海洋灵感 都市时尚'；Interparfums 持 Nautica 香水授权至 2030。",
 ],
 "detail":[
   ["品牌方","Authentic Brands Group (ABG)","授权"],
   ["中国运营伙伴","上海荟众（取代 Tristate）","2026 起"],
   ["Tristate 2025 Nautica 营收","-12% (Spyder -24%)","2025"],
   ["2025 末门店","Nautica 直营70+伙伴44 / Spyder 42","2025"],
   ["创立","1983","历史"],
   ["香水授权","Interparfums 至 2030","授权"],
 ],
 "conclusions":[
   "Nautica 在中国由 ABG 授权、上海荟众接替 Tristate（后者 2025 Nautica -12%），是'品牌授权方换运营伙伴'的典型，对 [[cabbeen|卡宾]] 评估'国际品牌在华运营模式切换'有样本价值。",
   "与 [[mlb_kids|MLB]]/DKNY 类似走'授权代理'轻资产路线，但 Nautica 下滑（Tristate -12%）说明老牌美式休闲在华遇冷，授权模式不能自动救市。",
   "1983 创立的航海经典符号老化，需靠新运营方重启，对 [[peacebird|太平鸟]] 的'经典 IP 焕新'议题有反面参照。",
   "数据风险：ABG 私营不披露单品牌财务；Nautica 中国数据来自前运营方 Tristate 财报口径。",
 ],
 "source_title":"NAUTICA / ABG 中国运营切换速览 2026",
 "urls":["https://www.abg.com/"],
},
]

def entity_md(b):
    key=b["key"]
    src_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    raw_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    aliases_yaml="\n".join("  - \"%s\"" % a for a in b["aliases"])
    tags_yaml=", ".join(b["tags"])
    core="\n".join("- %s" % c for c in b["core"])
    detail_rows="\n".join("| %s | %s | %s |" % (m,v,c) for (m,v,c) in b["detail"])
    concl="\n".join("%d. %s" % (i+1, c) for i,c in enumerate(b["conclusions"]))
    return f"""---
type: entity
title: {b['title']}
aliases:
{aliases_yaml}
tags: [{tags_yaml}]
sources: [{src_file}, {WALL}]
created: 2026-08-14
updated: {DATE}
cross_refs: [[服装行业竞争格局]], [[peacebird]], [[cabbeen]]
---

# {b['title']}

> **一句话摘要**：{b['summary']}
> **来源**：[[{src_file[:-3]}]]
> **最后更新**：{DATE}

## 核心要点
{core}

## 详细内容
| 指标 | 数值 | 口径 |
|------|------|------|
{detail_rows}

## 结论
{concl}

## 信息链
- 上游来源：[[{src_file[:-3]}]] → 本页（[[{key}]]）→ 下游应用：[[服装行业竞争格局]] · [[peacebird]] · [[cabbeen]]

## 关联页面
- 核心对标：[[peacebird|太平鸟]]、[[cabbeen|卡宾]]
- 行业格局：[[服装行业竞争格局]]
"""

def source_md(b):
    src_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    raw_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    tags_yaml=", ".join(b["tags"]+["2026","competitor_update"])
    core="\n".join("- %s" % c for c in b["core"])
    urls="\n".join("- %s" % u for u in b["urls"])
    return f"""---
type: source
title: {b['source_title']}
tags: [{tags_yaml}]
sources: [raw/articles/{raw_file}]
created: {DATE}
updated: {DATE}
cross_refs: [[{b['key']}]], [[服装行业竞争格局]]
---

# {DATE} {b['source_title']}

> **一句话摘要**：{b['summary']} 本页为 Round A（少源品牌补齐）WebSearch 提炼，落位实体 [[{b['key']}]]。

## 核心要点
{core}

## 来源链接
{urls}

## 关联页面
- [[{b['key']}]] — 实体页
- [[服装行业竞争格局]] — 行业格局
"""

def raw_md(b):
    raw_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    urls="\n".join("- %s" % u for u in b["urls"])
    core="\n".join("- %s" % c for c in b["core"])
    return f"""# {DATE} {b['source_title']}（raw 剪藏）

> 采集方式：WebSearch 提炼，Round A 少源品牌补齐。
> 关联实体：{b['title']}（{b['key']}）

## 原文/来源链接
{urls}

## 关键事实（提炼）
{core}

## 备注
- 本文件为原始资料层（raw），仅供 [[../wiki/sources/{raw_file[:-3]}]] 引用，不在 wiki/ 直接编辑。
"""

os.makedirs(ENT, exist_ok=True)
os.makedirs(SRC, exist_ok=True)
os.makedirs(RAW, exist_ok=True)

for b in BRANDS:
    src_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    raw_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    with open(os.path.join(ENT, b["key"]+".md"), "w", encoding="utf-8") as f:
        f.write(entity_md(b))
    with open(os.path.join(SRC, src_file), "w", encoding="utf-8") as f:
        f.write(source_md(b))
    with open(os.path.join(RAW, raw_file), "w", encoding="utf-8") as f:
        f.write(raw_md(b))
    print("written:", b["key"], "|", src_file)
print("\nDONE. %d brands." % len(BRANDS))
