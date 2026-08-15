# -*- coding: utf-8 -*-
"""Round A Run 3 generator — 7 少源品牌 (stub -> 完整实体页 + source 页 + raw 剪藏).
格式严格对齐 CLAUDE.md 与 Run 1/2 模板。复用 entity_md/source_md/raw_md。
同时产出 _roundA_run3_paths.txt（git 精确暂存）与 _roundA_run3_index_data.json（供 index 脚本）。
"""
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
 "key":"mr_mrs","title":"MR&MRS ITALY (皮草夫妇)",
 "aliases":["MR&MRS ITALY","Mr & Mrs Italy","皮草夫妇","MR and MRS ITALY","MR&MRS"],
 "tags":["mr_mrs","competitor","luxury","fur","outerwear","italy"],
 "country":"Italy",
 "summary":"意大利奢侈皮草派克大衣品牌，2007 年创立，以手工皮草派克大衣闻名，因韩剧《来自星星的你》全智贤同款爆红。",
 "core":[
   "创立：2007 年意大利，设计师 Alessia Giacobino；以复古美军工装为灵感，注入摩登元素。",
   "标志单品：手工皮草内衬派克大衣（parka），100% 意大利制造，纯手工染色与修整。",
   "因韩剧《来自星星的你》全智贤同款军绿派克大衣爆红，成为明星冬日'奢华替代羽绒服'选择（蕾哈娜/Cara Delevingne 等亦为粉丝）。",
   "中国：获弘毅资本（Hony Capital）投资；门店覆盖北京/上海/青岛/重庆/大连/成都/香港，首店大连时代广场（2014-06-26）。",
   "其他精品店：IGER 北京东方新天地、南京德基广场、长沙友谊商店、太原天美新天地；曾与 LETASCA、THE CAPECODE 联名。",
 ],
 "detail":[
   ["创立","2007，意大利，Alessia Giacobino","历史"],
   ["标志单品","手工皮草派克大衣（100% 意大利制造）","符号"],
   ["爆红","韩剧《来自星星的你》全智贤同款","营销"],
   ["中国资本","获弘毅资本（Hony）投资","治理"],
   ["中国门店","北京/上海/青岛/重庆/大连/成都/香港","2026"],
   ["中国首店","大连时代广场（2014-06-26）","时点"],
 ],
 "conclusions":[
   "MR&MRS ITALY 以'派克大衣+奢华皮草'切入高端御寒外套，与 [[peacebird|太平鸟]] 的'联名IP+社媒爆款'打法不同，属'影视同款驱动的小众奢侈'样本，对双核高端化有对照价值。",
   "其中国获弘毅资本加持、多城开店，显示国际小众奢侈仍加注中国市场，与 [[cabbeen|卡宾]]/[[peacebird|太平鸟]] 的本土高端线形成'外牌 vs 国牌'高端竞争面。",
   "必须区分：本页指意大利 MR&MRS ITALY（皮草夫妇），非广州甲东乙南'MR'女装（mrealm.com.cn，2011 中国女装）、亦非 MR&MS 银饰或 MR 汉堡先生——同名不同业，RAG 检索须靠 aliases 消歧。",
   "数据风险：MR&MRS ITALY 私营不披露中国单店财务；门店清单来自品牌稿与媒体盘点（2014-2019 口径），近年拓店节奏放缓，引用须标注时点。",
 ],
 "source_title":"MR&MRS ITALY 皮草夫妇 中国奢侈派克大衣速览 2026",
 "urls":["http://m.mxgxt.com/news/view/314508","https://www.huizhouyuxin.com/article/27fa7326572d3907f9271f2e.html"],
},
{
 "key":"nerdy","title":"NERDY (널디)",
 "aliases":["NERDY","널디","纳迪","NERDY 紫色运动服"],
 "tags":["nerdy","competitor","streetwear","korean_wave","sportswear","china"],
 "country":"Korea",
 "summary":"韩国首尔街头潮流品牌，MODEUS（莫媞美思）运营，以纽约街头风格+签名紫色 Track Suit 走红，中国由杭州弗娜瑞品牌管理运营。",
 "core":[
   "诞生于韩国首尔，由 MODEUS（莫媞美思）株式会社运营；标语'为平凡中不平凡的人打造的街头品牌'，倡导'自由·自我·本性'。",
   "纽约街头风格（NY series），签名单品 TRACK SET 运动服（紫色 Track Suit 风靡韩娱圈），共 9 大系列十余配色。",
   "中国：杭州下沙天街店、银泰百货武林店C馆（杭州）等；电商天猫/京东；中国运营商 杭州弗娜瑞品牌管理有限公司。",
   "传播：连续 2 年赞助韩国偶像运动会，国内赞助《快乐大本营》；早期借韩流偶像机场穿搭破圈。",
   "客群：18-25 岁学生与都市青年，主打高性价比潮流运动休闲。",
 ],
 "detail":[
   ["诞生","韩国首尔，MODEUS（莫媞美思）运营","治理"],
   ["风格","纽约街头 + 签名紫色 Track Suit","定位"],
   ["爆款","TRACK SET 运动服（9 系列）","符号"],
   ["中国门店","杭州下沙天街/银泰武林C馆等","2026"],
   ["中国运营","杭州弗娜瑞品牌管理有限公司","渠道"],
   ["电商","天猫/京东官方旗舰","渠道"],
 ],
 "conclusions":[
   "NERDY 以'韩流偶像+紫色 Track Suit+高性价比'在 Z 世代破圈，与 [[peacebird|太平鸟]] 的'联名IP+社媒爆款'打法高度同源，是韩潮快时尚在中国的直接竞品样本。",
   "其中国由杭州弗娜瑞运营、多城落地，与 [[chuu|chuu]]/[[no_one_else|NO ONE ELSE]] 等同属'韩潮扎堆入华'浪潮，对双核抢夺年轻客群构成压力面。",
   "须区分：本页指韩国 NERDY（널디）潮流品牌；美股 NRDY（Nerdy Inc.）是美国教育科技公司，ticker 同名不同业，RAG 检索须靠 aliases 消歧。",
   "数据风险：NERDY 中国门店数/运营方来自媒体盘点（非财报），且韩潮近年在中国有退潮风险，引用须标注'媒体口径'。",
 ],
 "source_title":"NERDY 韩国潮流品牌 中国门店与运营商速览 2026",
 "urls":["https://baike.sogou.com/v184138330.htm","https://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_4662857737126327938"],
},
{
 "key":"no_one_else","title":"NO ONE ELSE",
 "aliases":["NO ONE ELSE","NOE","无名之辈","无性别潮牌"],
 "tags":["no_one_else","competitor","streetwear","korean","unisex","womenswear"],
 "country":"Korea",
 "summary":"韩国 PPB STUDIO 旗下无性别设计师潮牌（chuu 姐妹品牌），2012 年创立，千禧混搭风，2021 随 chuu 入华由杭州黯涉运营。",
 "core":[
   "创立：2012 年韩国，隶属 PPB STUDIO；与少女潮牌 chuu 为同公司'姐妹品牌'。",
   "定位无性别（unisex）男女通款，主打'千禧混搭风'（millennial mix-match），融合户外工装/复古/美式/撞色拼色。",
   "中国：2021 年与 chuu 以直营+代理形式入华，由杭州黯涉品牌管理集团有限公司运营；首店 2021-10 长沙国金街。",
   "门店：北京（朝阳大悦城）/上海（五角场万达）/深圳（万象天地）/杭州/重庆/南京（德基）/武汉等多城；口径从 2022 约 10+ 家增至 2024 约 40-50 元（chuu+NOE 合计 231 家/2021-2025）。",
   "客单价约 400-600 元；价格带 99-899 元（与 chuu 同区间），高互动性+绿色门店设计吸客。",
 ],
 "detail":[
   ["创立","2012 韩国，PPB STUDIO","历史"],
   ["关系","chuu 姐妹品牌（同公司）","集团"],
   ["风格","无性别 + 千禧混搭风","定位"],
   ["入华","2021 直营+代理，杭州黯涉运营","渠道"],
   ["中国首店","2021-10 长沙国金街","时点"],
   ["门店(估)","约 40-50 家（2024；chuu+NOE 合计231/2021-25）","2024"],
 ],
 "conclusions":[
   "NO ONE ELSE 以'无性别+千禧混搭'与 [[chuu|chuu]] 同门出击，是韩潮快时尚在中国'多品牌矩阵'打法的样本，对 [[peacebird|太平鸟]] 的少女/年轻线构成直接竞争。",
   "其与 chuu 合计 231 家店（2021-2025）、吃下 Zara/H&M 让出的份额，印证'韩潮扎堆+高性价比+风格店'在中国年轻市场的有效性，值得双核借鉴门店体验设计。",
   "数据风险：NOE 单品牌门店数无独立披露，各家口径差异大（2022 约10+ vs 2024 约40-50 vs 合计231含chuu），引用须标注'含chuu/估算'。",
 ],
 "source_title":"NO ONE ELSE PPB STUDIO 无性别潮牌 中国门店速览 2026",
 "urls":["https://www.brandstar.com.cn/in-depth/7661","https://c.m.163.com/news/a/HG21BVPL05158BF0.html"],
},
{
 "key":"the_mr_young","title":"THE MR YOUNG (密特·扬)",
 "aliases":["THE MR YOUNG","THEMRYOUNG","密特·扬","密特扬"],
 "tags":["the_mr_young","competitor","guochao","streetwear","china","menswear"],
 "country":"China",
 "summary":"中国本土'轻奢国潮'原创品牌，根植上海，由曾代理 MLB 的上海艾动实业运营，主打高审美潮流生活方式。",
 "core":[
   "根植中国文化、出生于上海的原创潮流品牌，定位'轻奢国潮'，注重设计/材质/版型/工艺与穿着舒适度。",
   "运营方：上海艾动实业有限公司（2007 成立，曾为 MLB 中华区总代理至 2021-06），现以经营 THE MR YOUNG 等原创潮流品牌为主。",
   "品牌 IP'扬仔'——极地漫游者形象；与艺术家单飞、涂鸦艺术家毛裤老师、鲸鱼赛车俱乐部（GT）等联名，打造艺术空间。",
   "门店：银泰杭州武林总店A馆7楼、城西银泰城店、绍兴大通、义乌银泰等；覆盖一二线商圈。",
   "注：艾动官网称'代理潮流品牌自 2007 登陆大陆开设专卖店 500+ 家/150+ 城市'——此为运营方累计代理品牌口径，非 THE MR YOUNG 单品牌门店数，单品牌规模未独立披露。",
 ],
 "detail":[
   ["定位","中国本土'轻奢国潮'原创","定位"],
   ["运营方","上海艾动实业（曾代理MLB至2021-06）","治理"],
   ["IP/联名","扬仔 + 单飞/毛裤老师/鲸鱼赛车","营销"],
   ["门店(确认)","银泰杭州武林/城西/绍兴大通/义乌银泰","2026"],
   ["规模口径","艾动累计500+店/150+城=代理品牌合计","辨析"],
   ["数据完整度","THE MR YOUNG 单品牌门店数未披露","备注"],
 ],
 "conclusions":[
   "THE MR YOUNG 以'轻奢国潮+艺术联名+高审美'切入，是本土国潮对标 [[peacebird|太平鸟]] 中高端线的样本，其'IP+艺术家联名'打法值得双核参考。",
   "运营方上海艾动曾为 MLB 中华区总代理，具备国际潮牌运营经验后转向原创，是'代理商→自创品牌'的转型路径，与 [[cabbeen|卡宾]] 的原创男装路线有交集。",
   "关键辨析：'500+ 店/150+ 城市'是艾动公司累计代理品牌的口径，不可直接等同 THE MR YOUNG 单品牌规模；本页仅能确认杭州/绍兴/义乌等少数门店，引用须严格区分。",
   "数据风险：THE MR YOUNG 单品牌财务与门店数未公开，公开信息多为品牌稿，引用须标注'品牌整体/代理合计口径'。",
 ],
 "source_title":"THE MR YOUNG 密特扬 中国轻奢国潮品牌速览 2026",
 "urls":["https://www.fengxian.gov.cn/xdjd/tzxd/tzzn/jjyq/20210311/3412-9d5dbf09-03f3-490a-ad76-f4b8d370583f.html","https://www.qixin.com/company/b62d0464-e7ed-4bb7-8198-5897a16b926e"],
},
{
 "key":"thisisizi8","title":"thisisIZI8",
 "aliases":["thisisIZI8","IZI8","THISISIZI8","克莱因蓝买手店"],
 "tags":["thisisizi8","competitor","concept_store","buyer_store","korean","china"],
 "country":"Korea",
 "summary":"韩国血统综合型概念买手品牌店，2013 年由 Koyo William 创立，集 80+ 潮流品牌，中国首店 2024-01-15 深圳万象天地。",
 "core":[
   "创立：2013 年，源于对韩国时装的热情；创始人 Koyo William（亦为 KOYO JEANS 创办人）。",
   "定位：集服装/艺术/文化/生活为一体的综合型概念买手品牌店，DNA'Every day is new'——每日上新不同品牌货品。",
   "引入 80+ 潮流 DNA 品牌：HUMAN MADE、NERDY、AMBLER、RSC、Bearbrick、Soap Studio、ESSENTIALS、Rosa.K、OGR 等。",
   "中国：首店 2024-01-15 深圳万象天地 SL367（克莱因蓝集装箱/便利店冰柜/地铁车厢/潮玩墙装置）；华中首店武汉万象城；武汉武商MALL国广。",
   "运营方：国威（东莞）贸易有限公司；以高性价比集合+场景化社交空间吸引 Z 世代。",
 ],
 "detail":[
   ["创立","2013，创始人 Koyo William","历史"],
   ["性质","综合型概念买手品牌店（80+ 品牌）","定位"],
   ["中国首店","2024-01-15 深圳万象天地","时点"],
   ["华中首店","武汉万象城 / 武商MALL国广","2024+"],
   ["运营方","国威(东莞)贸易有限公司","治理"],
   ["标志","克莱因蓝 + 集装箱/地铁车厢装置","视觉"],
 ],
 "conclusions":[
   "thisisIZI8 以'韩国血统买手店+80+ 品牌集合+克莱因蓝场景'在中国落地，是'买手集合店'新势力样本，对 [[peacebird|太平鸟]] 的'多品牌/场景化'探索有近距离参照。",
   "其与 [[koyo|KOYO JEANS]] 同出 Koyo William 之手，构成'设计师个人 IP→多业态（自营牛仔+买手集合）'的矩阵，是观察设计师创业路径的稀缺样本。",
   "与 [[nerdy|NERDY]] 形成'集合店 vs 单品牌'对照：thisisIZI8 把 NERDY 等收入店中，二者是'渠道—品牌'共生关系，对双核理解'买手店 vs 直营'有启发。",
   "数据风险：thisisIZI8 私营不披露财务；门店数以'首店+华中首店'为主，全国铺开节奏待观察，引用须标注时点。",
 ],
 "source_title":"thisisIZI8 韩国概念买手店 中国首店与品牌矩阵速览 2026",
 "urls":["https://www.ellechina.com/fashion/news/1642424662","https://fashion.huanqiu.com/article/46Rt4F8TjeA?re=nextnews"],
 "extra_refs":["koyo","nerdy"],
},
{
 "key":"koyo","title":"KOYO JEANS",
 "aliases":["KOYO JEANS","KOYO","koyo jeans","高龙"],
 "tags":["koyo","competitor","denim","streetwear","menswear","hongkong","designer"],
 "country":"HongKong",
 "summary":"香港设计师 Koyo William 2002 年创立的欧式街头牛仔品牌，哥特摇滚+施华洛世奇钉珠，'Destroy & Reborn' 风格，广州高龙贸易运营。",
 "core":[
   "创立：2002 年，创办人 Koyo William（香港）；定位国际舞台，骨干为法式浪漫+哥特式华丽摇滚。",
   "风格：'Destroy & Reborn' 颠覆性哲学；少有华人设计师以 fashion denim 在欧洲打响；标志性华丽哥德摇滚+金属钉珠（施华洛世奇）点缀。",
   "架构：法国设计中心 + 香港行政中心 + 中国大陆生产物流中心'三位一体'；骷髅头'K' logo 象征人人平等。",
   "运营：广州高龙贸易有限公司（2008 成立，2024 重新注册）；入驻国内一线商场 50+ 家。",
   "明星背书：G-Dragon、2NE1、CL、黄晓明、谢霆锋、张晋、蔡少芬、吴卓羲、Beyond 黄贯中、林峰等；门店含香港海港城、广州太古汇、成都IFS、长沙IFS 等。",
 ],
 "detail":[
   ["创立","2002，创始人 Koyo William（香港）","历史"],
   ["风格","哥特摇滚 + 施华洛世奇钉珠 / Destroy&Reborn","设计"],
   ["架构","法国设计/香港行政/大陆生产物流 三位一体","供应链"],
   ["运营方","广州高龙贸易有限公司（2024重注）","治理"],
   ["中国网点","入驻一线商场 50+ 家","2026"],
   ["明星","G-Dragon/黄晓明/谢霆锋/林峰等","营销"],
 ],
 "conclusions":[
   "KOYO JEANS 以'哥特摇滚+钉珠工艺+华人设计师欧洲突围'形成差异化，对 [[cabbeen|卡宾]] 的实穿男装路线是'重工艺设计师牌'对照样本。",
   "其与 [[thisisizi8|thisisIZI8]] 同出 Koyo William，构成设计师多业态矩阵——这一'个人 IP 跨业态'路径，对双核评估'设计师驱动 vs 公司化运营'有启发。",
   "广州高龙贸易曾注销后于 2024 重新注册，运营主体稳定性待观察；'入驻 50+ 一线商场'为招聘口径，单品牌直营/加盟占比未披露。",
   "数据风险：KOYO JEANS 私营不披露财务；门店清单来自品牌稿与招聘页（含香港/大陆），引用须标注口径与时点。",
 ],
 "source_title":"KOYO JEANS Koyo William 中国欧式街头牛仔速览 2026",
 "urls":["http://www.huobaoweishang.com/pinpai/99729.html","https://m.liepin.com/company/8686632"],
 "extra_refs":["thisisizi8"],
},
{
 "key":"marcelo_burlon","title":"Marcelo Burlon County of Milan",
 "aliases":["Marcelo Burlon","County of Milan","MB","马尔塞罗·布尔隆"],
 "tags":["marcelo_burlon","competitor","designer","luxury","italy","argentina"],
 "country":"Italy",
 "summary":"意大利（阿根廷裔主理人）潮流时装屋，2012 年前后创立，Mapuche 十字/巴塔哥尼亚元素，全球首店 2017 香港（已关），中国借 D-mop 多品牌店铺货。",
 "core":[
   "主理人 Marcelo Burlon（阿根廷裔），身兼 DJ/造型师/艺术总监；曾任意 Givenchy by Riccardo Tisci 公关顾问。",
   "设计语言：Mapuche 十字（巴塔哥尼亚）、阿根廷鸟羽、神秘符号、rave/club 文化；涵盖男/女/童装，都市周末休闲。",
   "全球首家专门店：2017-09-15 香港海港城海运大厦 OT310C（火山石装潢），已於 2022 关闭；澳门银河时尚汇亦有店。",
   "中国大陆：主要通过多品牌买手店 D-mop（太古汇等）在广州/东莞等地铺货；曾与 Kappa（2017 联名）、G-SHOCK 联名。",
   "属'fashion 2.0'跨文化混搭品牌，强调多样性与都市感。",
 ],
 "detail":[
   ["主理人","Marcelo Burlon（阿根廷裔），前 Givenchy 公关顾问","人物"],
   ["设计","Mapuche十字/巴塔哥尼亚/rave文化","风格"],
   ["全球首店","2017-09-15 香港海港城（2022 关闭）","时点"],
   ["中国路径","D-mop 多品牌店（广州/东莞太古汇等）","渠道"],
   ["联名","Kappa(2017) / G-SHOCK","合作"],
   ["品类","男/女/童装 都市休闲","产品"],
 ],
 "conclusions":[
   "Marcelo Burlon 以'DJ/夜店文化+Mapuche 符号'的潮流时装屋定位，与 [[peacebird|太平鸟]] 的'潮流联名'方向有风格参照，但量级与渠道（依赖买手店）差异大。",
   "其香港首店 2017 开业、2022 关闭，印证'国际小众潮牌直营店在中国存活难'，对 [[cabbeen|卡宾]]/[[peacebird|太平鸟]] 评估'直营 vs 买手/代理'有反面教材价值。",
   "中国大陆主要靠 D-mop 等买手店铺货而非直营，说明其在中国仍处'符号曝光'阶段，尚未真正落地规模化零售。",
   "数据风险：Marcelo Burlon 私营不披露中国销售；香港店已关闭，大陆门店数为买手店代销口径，引用须标注'买手店/已关店'。",
 ],
 "source_title":"Marcelo Burlon County of Milan 中国渠道与香港首店速览 2026",
 "urls":["https://hypebeast.com/tw/2017/9/marcelo-burlon-county-of-milan-open-in-hong-kong","https://shopsinhk.com/marcelo-burlon-clothing-store-in-hong-kong.html"],
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
    extra=b.get("extra_refs",[])
    cross="[[服装行业竞争格局]], [[peacebird]], [[cabbeen]]"
    if extra:
        cross += ", " + ", ".join("[[%s]]" % e for e in extra)
    return f"""---
type: entity
title: {b['title']}
aliases:
{aliases_yaml}
tags: [{tags_yaml}]
sources: [{src_file}, {WALL}]
created: {DATE}
updated: {DATE}
cross_refs: {cross}
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
- 上游来源：[[{src_file[:-3]}]] → 本页（[[{key}]]）→ 下游应用：{cross}

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

written=[]
index_sources=[]
index_backlinks=[]

for b in BRANDS:
    src_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    raw_file="%s_%s.md" % (DATE, safe(b["source_title"]))
    ep=os.path.join(ENT, b["key"]+".md"); sp=os.path.join(SRC, src_file); rp=os.path.join(RAW, raw_file)
    with open(ep, "w", encoding="utf-8") as f: f.write(entity_md(b))
    with open(sp, "w", encoding="utf-8") as f: f.write(source_md(b))
    with open(rp, "w", encoding="utf-8") as f: f.write(raw_md(b))
    written.append(ep); written.append(sp); written.append(rp)
    # index source row summary (concise)
    summ=b["summary"]
    if len(summ)>60: summ=summ[:58]+"…"
    index_sources.append((src_file, b["summary"], ", ".join(b["tags"]+["source"])))
    bl_desc=b["summary"]
    if len(bl_desc)>46: bl_desc=bl_desc[:44]+"…"
    index_backlinks.append((b["key"], bl_desc+" (2026)"))
    print("written:", b["key"], "|", src_file)

# pathspec for git (exact, from this script's writes)
with open("_roundA_run3_paths.txt","w",encoding="utf-8") as f:
    f.write("\n".join(written)+"\n")

# index data for the index-update script
json.dump({"SOURCES":index_sources,"BACKLINKS":index_backlinks},
          open("_roundA_run3_index_data.json","w",encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\nDONE. %d brands, %d files. pathspec + index_data written." % (len(BRANDS), len(written)))
