# -*- coding: utf-8 -*-
"""Round A Run 2 generator — 8 少源品牌 (stub -> 完整实体页 + source 页 + raw 剪藏).
格式严格对齐 CLAUDE.md 与 salomon.md 范例（复用 Run 1 模板）。"""
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
 "key":"adlv","title":"ADLV (acme de la vie)",
 "aliases":["ADLV","acme de la vie","大脸宝宝","아크메드라비"],
 "tags":["adlv","competitor","streetwear","korean_wave","womenswear"],
 "country":"Korea",
 "summary":"韩国潮流品牌，由双胞胎兄弟 2017 年创立，以'大脸宝宝'系列 T 恤蹿红，主打无性别可爱街头。",
 "core":[
   "创立：2017 年，韩国首尔，一对热爱潮流的双胞胎兄弟创办，从买手店起家。",
   "品牌名法语意为'人生的巅峰时刻'，主张'不分性别、不分年纪'的自由潮流精神。",
   "靠'大脸宝宝'卡通 T 恤迅速蹿红，借 EXO、BTS 成员及 KOL 传播打开亚洲市场。",
   "中国内地约 14 家店：上海 MOHO、天津南开大悦城、长春红旗街万达、大连恒隆/柏威年、沈阳皇城恒隆等；深圳大悦城店即将开业。",
   "产品线扩展至服装、帽饰、鞋履；全球已开店，持续扩张亚洲。",
 ],
 "detail":[
   ["创立","2017，韩国首尔，双胞胎兄弟","历史"],
   ["品牌名含义","法语'人生巅峰时刻'，无性别主张","定位"],
   ["爆款","'大脸宝宝'卡通 T 恤","符号"],
   ["中国内地门店","约 14 家（上海/天津/长春/大连/沈阳等）","2026"],
   ["待开门店","深圳大悦城店","近期"],
   ["传播","EXO/BTS 成员 + KOL 机场穿搭","营销"],
 ],
 "conclusions":[
   "ADLV 走'可爱卡通+无性别+韩流偶像'的轻量破圈路径，与中国 [[peacebird|太平鸟]] 的'联名IP+社媒爆款'打法高度同源，是可对标的中端潮牌样本。",
   "中国约 14 店、集中一二线标杆 mall，扩张克制，与 [[awoken_time|AWOKEN TIME]] 等本土潮牌同期抢占 Z 世代，构成'韩潮 vs 国潮'的直接竞争面。",
   "产品线延展帽饰/鞋履，从 T 恤单品向全品类过渡，是'一个爆款符号撑起品牌'的典型生命周期。",
   "数据风险：ADLV 中国门店数/运营方来自媒体盘点（非财报），且韩妆/韩潮近年在中国有退潮风险，引用须标注'媒体口径'。",
 ],
 "source_title":"ADLV acme de la vie 中国门店与品牌速览 2026",
 "urls":["http://live.xqnmlyi.cn/news/50c599427.html"],
},
{
 "key":"awoken_time","title":"AWOKEN TIME",
 "aliases":["AWOKEN TIME","唤醒时刻","AWOKEN"],
 "tags":["awoken_time","competitor","streetwear","concept_store","china","wuhan"],
 "country":"China",
 "summary":"中国本土潮流集合店品牌 AWOKEN 的'时间/生活馆'线，以潮玩+咖啡+服饰的场景化门店出圈。",
 "core":[
   "品牌主张'个性、时尚、活力，唤醒生活每一时刻'；设微光/昼夜/传橙三大服装系列。",
   "武汉为总部与核心市场：武商 MALL 超 800㎡ 旗舰（国广店）、梦时代、江宸天街、经开永旺、江夏永旺等多店。",
   "外拓：襄阳武商、宜昌国贸、南昌武商 MALL 均已落店；上海泗泾招商花园城（2026 四季度开业）已签约。",
   "门店融入时尚咖啡区 + 潮玩/生活用品，超越传统服饰集合店，靠场景打卡吸引年轻人。",
   "注重与明星/KOL 合作打造热点营销，对标新一代国潮集合店。",
 ],
 "detail":[
   ["品牌主张","个性/时尚/活力，唤醒生活每一时刻","定位"],
   ["服装系列","微光 / 昼夜 / 传橙 三大系列","产品"],
   ["武汉旗舰","武商MALL 国广店 超800㎡","2026"],
   ["武汉门店","梦时代/江宸天街/经开永旺/江夏永旺 等","集群"],
   ["外拓城市","襄阳/宜昌/南昌/上海(泗泾签约)","2026+"],
   ["门店特色","咖啡区 + 潮玩/生活用品 + 场景打卡","差异化"],
 ],
 "conclusions":[
   "AWOKEN TIME 以'服装+咖啡+潮玩'的场景化集合店模式在武汉密集开店，是本土 [[humble_humble_r|HumbleHumbleR]] 之外另一类'新国潮集合店'样本，对 [[peacebird|太平鸟]] 的'门店体验化'方向有近距离参照。",
   "武汉单城多店（4+）+ 外拓襄阳/宜昌/南昌，显示其'区域深耕再复制'的扩张节奏，与全国撒网的国际品牌相反。",
   "'场景打卡+KOL'驱动到店，本质是用空间叙事替代单纯卖货，印证线下门店正向'内容场'转型。",
   "数据风险：门店数与开业时间多来自赢商网等商业地产媒体，且品牌仍处快速扩张期，数据变动快，引用须标注时点。",
 ],
 "source_title":"AWOKEN TIME 中国潮流集合店门店与运营速览 2026",
 "urls":["https://m.winshang.com/news717273.html","https://www.toutiao.com/article/7314928749164675647/"],
},
{
 "key":"awoken_space","title":"AWOKEN SPACE",
 "aliases":["AWOKEN SPACE","AWOKEN 空间线"],
 "tags":["awoken_space","competitor","streetwear","concept_store","china","wuhan"],
 "country":"China",
 "summary":"中国本土潮流品牌 AWOKEN 的'空间/场景'概念副线，与 AWOKEN TIME 共享品牌哲学与武汉集群。",
 "core":[
   "与 [[awoken_time|AWOKEN TIME]] 同属中国本土潮流品牌 AWOKEN 体系，共享'唤醒生活每一时刻'的品牌哲学。",
   "定位'空间/场景'概念线，强调场景化零售体验，是 AWOKEN 多线矩阵中的一支。",
   "依托武汉总部集群与供应链，与 AWOKEN TIME 共用设计/营销资源，协同扩张。",
   "公开独立数据较少，多以 AWOKEN 品牌整体对外发声，离散信息有限。",
 ],
 "detail":[
   ["所属体系","AWOKEN（中国本土潮流品牌）","集团"],
   ["定位","'空间/场景'概念副线","产品线"],
   ["品牌哲学","与 AWOKEN TIME 共享'唤醒每一时刻'","同源"],
   ["市场","武汉集群 + 协同外拓","区域"],
   ["数据完整度","离散信息有限（多为品牌整体口径）","备注"],
 ],
 "conclusions":[
   "AWOKEN SPACE 作为 AWOKEN 体系的'空间/场景'副线，与 [[awoken_time|AWOKEN TIME]] 构成同一本土潮牌的多线矩阵，对 [[peacebird|太平鸟]] 的'副线/系列化'打法有近距离样本价值。",
   "其独立数据稀缺，说明品牌仍以母品牌 AWOKEN 整体对外，副线尚未独立披露——这是本土新潮牌'先母品牌后副线'的常见路径。",
   "与 [[humble_humble_r|HumbleHumbleR]] 同属 2025 前后崛起的本土新潮牌，共同构成'国潮集合/场景店'新势力，值得持续追踪。",
   "数据风险：AWOKEN SPACE 公开资料极少，本页以品牌整体口径+合理推断撰写，待后续采集补充离散事实；引用须标注'品牌整体口径'。",
 ],
 "source_title":"AWOKEN SPACE 中国潮流副线速览 2026",
 "urls":["https://m.winshang.com/news717273.html"],
},
{
 "key":"dickies","title":"Dickies",
 "aliases":["Dickies","迪克尔斯","874工装裤"],
 "tags":["dickies","competitor","workwear","american","casual"],
 "country":"USA",
 "summary":"美国百年工装品牌，以 874 经典工装裤与卡其工装著称，VF 集团旗下（2026 年已出售）。",
 "core":[
   "创立：1922 年美国；经典 874 工装裤（1967 推出），'Durable Elegance'式硬核工装基因。",
   "母公司：VF Corporation（威富集团，纽交所 VFC），2017 年收购 Dickies。",
   "VF 已于 2026 财年第三季度（截至 2026-03-28 当年）完成 Dickies 出售。",
   "中国：2007 年设全资子公司；线下覆盖多数一二线核心商圈，价格 199-599 元中端。",
   "产品以棉混纺耐磨工装为主，新品节奏偏慢（约每季 1-2 波），认知度高但创新缓。",
 ],
 "detail":[
   ["创立","1922 美国","历史"],
   ["经典单品","874 工装裤（1967）","符号"],
   ["母公司","VF Corp（VFC），2017 收购","治理"],
   ["重大变动","VF 2026 财年 Q3 完成出售 Dickies","2026"],
   ["中国布局","2007 设全资子公司，一二线核心商圈","渠道"],
   ["价格带","199-599 元（中端）","定位"],
 ],
 "conclusions":[
   "Dickies 在 VF 2026 财年 Q3 被出售，是'国际集团剥离非核心工装资产'的信号，对 [[cabbeen|卡宾]]/[[peacebird|太平鸟]] 评估'工装赛道是否被国际资本看淡'有参照。",
   "其'经典 874 + 中端定价 + 慢上新'模式认知度高但增长钝化，与 [[levis|李维斯]] 的激进直营化形成对照——同为美式丹宁/工装，路径分化。",
   "中国 2007 即设子公司、深耕一二线，证明其基础盘稳固，但被剥离开意味 VF 认为增长空间有限。",
   "数据风险：VF 财报中 Dickies 已作为'已终止/出售'项处理，历史季度数据需区分'持有期'与'剥离后'口径。",
 ],
 "source_title":"Dickies / VF 中国工装市场与出售速览 2026",
 "urls":["https://dickies.com.cn/?p=11","https://www.hangyeob.com/archives/408290.html"],
},
{
 "key":"etudes","title":"Études Studio",
 "aliases":["Etudes","Études","Études Studio","艾蒂德斯"],
 "tags":["etudes","competitor","designer","french","art_led"],
 "country":"France",
 "summary":"法国艺术导向时装屋（注意与韩妆 ETUDE HOUSE 伊蒂之屋区分），2012 年巴黎创立，男装+出版+艺术策展。",
 "core":[
   "注意区分：本页指法国时装屋 Études Studio，非韩国彩妆 ETUDE HOUSE（伊蒂之屋）。",
   "创立：2012 年巴黎，联合创始人 Aurélien Arbet 与 Jérémie Egry（2024 年 Jose Lamali 离任）。",
   "全球约 30 个市场、80 家零售合作伙伴；2024 年 6 月重返巴黎男装周（东京宫发布 'Surroundings'）。",
   "2030 蓝图：5 倍增速；DTC（电商+零售）占比 5 年内 20%→45%；扩展配饰/鞋履/眼镜/皮具（2026 秋冬）。",
   "巴黎玛黑区 hybrid 旗舰（含艺术书店）拟于男装周开业；创意工作室约占业务 10%。",
 ],
 "detail":[
   ["性质","法国艺术导向时装屋（非韩妆）","辨析"],
   ["创立","2012 巴黎，Arbet & Egry","历史"],
   ["零售网络","~30 市场 / 80 零售伙伴","2024"],
   ["2030 目标","5 倍增速；DTC 20%→45%","战略"],
   ["品类扩展","配饰/鞋履/眼镜/皮具（2026 秋冬）","产品"],
   ["巴黎旗舰","玛黑区 hybrid 旗舰（含书店）","零售"],
 ],
 "conclusions":[
   "Études 以'艺术策展+出版+时装'的策展型品牌模式区别于传统时装屋，对 [[peacebird|太平鸟]] 探索'品牌文化属性'有非主流参照。",
   "其 2030 蓝图把 DTC 占比拉到 45%、扩展皮具配饰，是'小众艺术牌如何商业化'的样本，与 [[cabbeen|卡宾]] 的规模化路径相反但互补观察。",
   "必须区分 French Études Studio 与 Korean ETUDE HOUSE（伊蒂之屋，彩妆，2026 闭店整顿）——同名不同业，RAG 检索须靠 aliases 消歧。",
   "数据风险：Études 私营不披露财务；5 倍增速/45% DTC 为规划目标非已实现，引用须标注'2030 规划'。",
 ],
 "source_title":"Études Studio 法国艺术时装屋与2030蓝图 2026",
 "urls":["https://www.fashionnetwork.cn/share/3754.html","https://poshe.shop/blogs/news/etudes-studio-s-next-chapter-brice-groulier-s-plan-to-turn-art-led-label-into-an-accessories-powerhouse"],
},
{
 "key":"g_star_raw","title":"G-Star RAW",
 "aliases":["G-Star","GSTAR RAW","极星","G-STAR"],
 "tags":["g_star_raw","competitor","denim","premium_denim","netherlands"],
 "country":"Netherlands",
 "summary":"荷兰丹宁品牌，1989 年阿姆斯特丹创立，'原始牛仔 Raw Denim'先驱，中国由极星服饰商贸（上海）运营。",
 "core":[
   "创立：1989 年荷兰阿姆斯特丹，哲学'Just the Product / 产品至上'。",
   "1996 年推出原始牛仔（Raw Denim）系列，是未经处理牛仔布时装化的先驱。",
   "中国运营：极星服饰商贸（上海）有限公司（2013-10-10 成立，外国法人独资，Robert Jaap Schilder）。",
   "中国大陆近 150 个专门店及专柜，覆盖 60+ 城市（上海/北京/广州/杭州/成都等）；北京/上海/广州/深圳/天津/港澳有直营。",
   "特许经营生产商广州番禺翡翠制衣；京东官方旗舰店在售。",
 ],
 "detail":[
   ["创立","1989 阿姆斯特丹，'产品至上'","历史"],
   ["标志创新","1996 Raw Denim 原始牛仔先驱","技术"],
   ["中国运营方","极星服饰商贸(上海)（外独，2013 成立）","治理"],
   ["中国门店","近 150 专门店/专柜，60+ 城市","2026"],
   ["生产","广州番禺翡翠制衣（特许）","供应链"],
   ["电商","京东官方旗舰店","渠道"],
 ],
 "conclusions":[
   "G-Star RAW 在中国由极星服饰（独立外企）运营、近 150 网点，是'丹宁专业牌规模化'样本，与 [[levis|李维斯]]/[[diesel|Diesel]] 同台竞争高端丹宁。",
   "其'产品至上+原始牛仔'的工艺叙事，区别于 Diesel 的夜店文化、Levi's 的美式经典，三者在丹宁赛道形成不同心智卡位。",
   "注意：部分商业设计稿将 G-Star RAW 与'卡宾旗下'并列列出，疑为设计公司客户清单的松散表述；G-Star RAW 中国实为极星服饰独立运营，与 [[cabbeen|卡宾]] 无股权关系，引用须澄清。",
   "数据风险：近 150 网点来自 2026 牛仔裤排行榜媒体口径，含专柜非全直营；极星私营不披露单品牌财务。",
 ],
 "source_title":"G-Star RAW 中国丹宁运营与渠道速览 2026",
 "urls":["http://m.51ef.com.cn/corp/corpabout-214952.html","https://www.fadabao.net/news-37226.html"],
},
{
 "key":"humble_humble_r","title":"HumbleHumbleR (谦而不卑)",
 "aliases":["HumbleHumbleR","谦而不卑","HUMBLEWEAR"],
 "tags":["humble_humble_r","competitor","streetwear","china","menswear","new_brand"],
 "country":"China",
 "summary":"中国本土设计师潮流男装，2025 年创立，以'BE HUMBLE/谦而不卑'中性情绪与高质价比切入 Z 世代。",
 "core":[
   "创立：2025 年，中国本土设计师潮流品牌，哲学'BE HUMBLE 保持谦逊'，主张'谦而不卑'中性情绪。",
   "定位中高端潮流男装，价格亲民；覆盖工装夹克、oversize 卫衣、简约针织、利落衬衫，含牛仔/HUMBLEWEAR 系列。",
   "首店 2025-09-05 宁波鄞州万达，开业三天创 46 万元销售；2026-01-24 宁波阪急开出全国首家臻选店。",
   "外拓：武汉杉杉奥莱（华中首店）、杭州湖滨银泰（首店）相继开业；未来布局杭州/上海/武汉/长沙/太原。",
   "由行业顶尖团队打造，强调极简剪裁与功能性平衡、供应链价格优势。",
 ],
 "detail":[
   ["创立","2025，中国本土设计师潮牌","历史"],
   ["哲学","BE HUMBLE / 谦而不卑 中性情绪","定位"],
   ["首店","2025-09-05 宁波鄞州万达（3天46万）","起点"],
   ["臻选店","2026-01-24 宁波阪急 全国首家臻选店","升级"],
   ["外拓","武汉杉杉奥莱(华中首店)/杭州湖滨银泰首店","2026"],
   ["未来城市","杭州/上海/武汉/长沙/太原","规划"],
 ],
 "conclusions":[
   "HumbleHumbleR 是 2025 新锐本土男装，靠'谦而不卑'情绪+高质价比+首店经济快速铺开，与 [[awoken_time|AWOKEN TIME]] 同属'新国潮'势力，对 [[peacebird|太平鸟]] 构成年轻客群争夺。",
   "其'首店三天 46 万 + 高端商场臻选店'的打法，是用'克制叙事+空间体验'替代 loud logo，与 [[cabbeen|卡宾]] 的实穿男装路线有交集。",
   "2025 创立即多城首店，节奏快于多数新牌，但规模仍小，属'高潜待验证'样本，需持续追踪复购与扩店质量。",
   "数据风险：品牌极新（2025），公开数据来自首店报道与奥莱招商稿，财务/同店数据缺失，引用须标注'早期/媒体报道'。",
 ],
 "source_title":"HumbleHumbleR 谦而不卑 中国新锐男装速览 2026",
 "urls":["https://m.winshang.com/news737874.html","https://www.sina.cn/news/detail/5209339623377954.html","https://m.winshang.com/news739806.html"],
},
{
 "key":"king_baby","title":"KING BABY",
 "aliases":["King Baby","KINGBABY","金北陛"],
 "tags":["king_baby","competitor","jewelry","accessories","rock","usa"],
 "country":"USA",
 "summary":"美国摇滚风银饰与皮具品牌，2000 年洛杉矶创立，以哥特摇滚+手工银饰著称，中国由金北陛（上海）贸易运营。",
 "core":[
   "创立：2000 年，创始人兼设计师 Mitchell Binder，洛杉矶；植根摇滚不灭灵魂与骑手精神。",
   "产品：手工银饰、皮革、宝石，银的硬朗与皮革柔软冲突，塑造桀骜不驯的金属摇滚形象。",
   "中国运营：金北陛（上海）贸易有限公司；中国大陆超 10 家旗舰店（北京西单大悦城等）。",
   "渠道：亦进入厦门 K11 Select 等高端商场；代理方含重庆贻和商贸（同时代理 NBA、PINKO 等）。",
   "全球：Santa Monica / Nashville / Las Vegas Caesars Palace 等多地旗舰，中国为其重要海外市场。",
 ],
 "detail":[
   ["创立","2000 洛杉矶，Mitchell Binder","历史"],
   ["设计","哥特摇滚 + 手工银饰/皮革/宝石","风格"],
   ["中国运营","金北陛(上海)贸易有限公司","治理"],
   ["中国门店","超 10 家旗舰（北京西单大悦城等）","2026"],
   ["渠道拓展","厦门 K11 Select 等高端 mall","2026"],
   ["代理","重庆贻和商贸（同代理 NBA/PINKO）","中国"],
 ],
 "conclusions":[
   "KING BABY 以'摇滚银饰+皮具'的配饰型品牌在中国开超 10 店，是'小众风格配饰也能规模化'的样本，对 [[peacebird|太平鸟]] 的配饰线扩张有参照。",
   "其'美国设计师品牌+中国贸易公司运营+高端 mall'的轻资产路径，与 [[nautica|Nautica]]/[[mlb_kids|MLB]] 的授权代理模式同源，适合风格型小众牌。",
   "银饰/皮革属高毛利配饰，与 [[cabbeen|卡宾]] 以服装为主的毛利结构不同，是'配饰拉动利润'的可观察案例。",
   "数据风险：KING BABY 私营不披露中国单店财务；门店数来自品牌官网与拓展平台，含伙伴店，引用须标注口径。",
 ],
 "source_title":"KING BABY 中国摇滚银饰与渠道速览 2026",
 "urls":["https://kingbabystudio.com/pages/king-baby-stores","https://www.shangchan.cn/brands/show-5739.html","https://www.sina.cn/news/detail/5324922403428290.html"],
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
