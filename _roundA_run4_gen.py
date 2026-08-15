# -*- coding: utf-8 -*-
"""Round A Run4 — 刷新 pass：11 个"已完整实体"品牌（双核 + 品牌墙 + 女装重点补充）。

背景（用户硬性规则 2026-08-15）：每次 A轮必须覆盖全部 focus_brands（当前 36 个）。
此前 3 遍仅跑"少源"品牌，漏了 11 个已完整实体（知识层面 36/36 但流程未重触）。
本轮动作：为 11 个品牌各创建 1 个新 raw + 1 个新 source（R4 刷新页，文件名含 _R4_ 便于溯源），
并向既有实体页追加"近期动态刷新"小节 + 新结论 + 信息链 + 确保竞争格局回链。

复用 run3 模板的 helper，但实体页采用"追加"而非"覆盖"，避免破坏既有完整页面。
产出 _roundA_run4_paths.txt（git 精确暂存）+ _roundA_run4_index_data.json（供 index 脚本）。
"""
import os, re, json

BASE = "knowledge_base/wiki"
ENT = os.path.join(BASE, "entities")
SRC = os.path.join(BASE, "sources")
RAW = os.path.join(BASE, "raw", "articles")
DATE = "2026-08-15"

def safe(s):
    return re.sub(r'[\/\\:*?"<>|]', "_", s).replace(" ", "_").strip()

BRANDS = [
{
 "key":"cabbeen","title":"卡宾（Cabbeen）","slug":"卡宾2026最新动态",
 "tags":["cabbeen","competitor","menswear","streetwear","core","hk_listed"],
 "summary":"卡宾 2026H1 毛利率 46.3% 为亮点但经营溢利 -24.7%，8 月马来 Sunway 新店、推进 AI 虚拟试穿与海外试水。",
 "urls":["https://www.toutiao.com/article/7673368771800662564/",
         "https://finance.sina.com.cn/stock/hkstock/ggscyd/2026-08-07/doc-inimnkum3234356.shtml",
         "https://cj.sina.com.cn/articles/view/3914987272/e959f70802702yu6c"],
 "refresh_core":[
   "2026-08 吉隆坡 The Starhill 快闪（携 2AM 联名 3D 打印鞋）后，8 月于马来 Sunway Velocity 新开门店，海外（马来）门店累计 2 家，标志全球扩张试水。",
   "2026H1 财报解读（环球网 8-13）：毛利率 46.3%（+2.5pp）为最大亮点，但经营溢利 -24.7%（利润率 8.5% vs 12.1%），揭示'增收增利、效率承压'，行业进入'产品力+经营效率'竞争阶段。",
   "公司推进 AI 虚拟试穿、智能穿搭等数字化工具；线下门店形象升级、强化到店试穿体验与互动转化。",
   "品牌矩阵：主品牌 Cabbeen 约 60% / Cabbeen Urban（卡宾都市）28.6% / 2AM 4.1%；线上 +12.3% > 线下 +4.7%。",
 ],
 "refresh_conclusion":"卡宾 2026H1 以'毛利率改善 + 数字化升级 + 海外试水（马来）'为主线，但存货周转 246 天（+38 天）与经营溢利下滑暴露效率短板；双核中定位'设计师差异化 + 科技面料'样本，与太平鸟规模龙头形成对照，A轮本轮已重触。",
},
{
 "key":"peacebird","title":"太平鸟（PEACEBIRD）","slug":"太平鸟2026H1动态",
 "tags":["peacebird","competitor","womenswear","menswear","a_share","core"],
 "summary":"太平鸟 2026H1 营收 28.78 亿(-0.72%)/归母 1.02 亿(+30.89%)/扣非 5071 万(+269.91%)，净关店 137 家至 2861，增长>50%靠非经常性损益。",
 "urls":["https://ima.qq.com/wiki/?shareId=6cb013606cc304bc65259ce96ec552d42a8da28ef80172d2947d5cc16cefae16",
         "https://newzzbcx.cs.com.cn/cxnews.html?name=new20260730190521gwayfjij",
         "https://egs.stcn.com/news/detail/2321504.html"],
 "refresh_core":[
   "2026H1 营收 28.78 亿(-0.72%)、归母 1.02 亿(+30.89%)、扣非 5071 万(+269.91%)；净关店 137 家至 2861；加盟 -10.32% / 线上 7.71 亿(+3.06%)。",
   "分品牌：女 10.84 亿(+2.26%)/男 11.96 亿(+1.38%)/乐町 1.81 亿(-22.02%)/童 3.90 亿(+3.62%)；毛利率 61.21%(+1.4pct)。",
   "非经常性损益 5100.91 万（政府补助 3597.82 万 + 金融资产 2677.81 万），归母增长>50%靠非经常性，主业质量待验证。",
   "三十周年：宁波奥体盛典、2-5-10 战略、POWER ON 大秀；治疗小狗 eteecy 男装联名；张江平'弱化大众化路线'；股东陈红朝减持 942 万股(2.00%/1.08 亿)。",
 ],
 "refresh_conclusion":"太平鸟 2026H1'收入微降、利润高增'主要靠非经常性损益与费用管控，主业经营质量仍承压、净关店延续；双核中以规模与女装基本盘见长，与卡宾差异化并存，A轮本轮已重触。",
},
{
 "key":"trussardi","title":"Trussardi (楚萨迪)","slug":"楚萨迪2025业绩重启",
 "tags":["trussardi","competitor","luxury","italy","leather","focus_brand"],
 "summary":"Trussardi 2025 营收 €29M(+70%)但 EBITDA 亏 €1M（重建期投入），Miroglio 2024 收购后定位生活方式，11 家独立店、中东/游艇延伸。",
 "urls":["https://in.fashionnetwork.com/news/-we-want-to-return-trussardi-to-centre-stage-says-miroglio-group-s-alberto-racca,1851747.html",
         "https://www.sina.cn/news/detail/5321101610584733.html",
         "https://www.laconceria.it/en/luxury/ceo-alberto-racca-on-the-rebuilding-of-trussardi"],
 "refresh_core":[
   "2025 营收近 €29M(+70%)，EBITDA 由 2024 盈利 €1.2M 转为亏损 €1M（重建期营销/传播投入），净亏由 €2.7M 扩大至 €5.1M。",
   "Miroglio 集团 2024 收购；当前 11 家独立店（科莫/维罗纳新开），2026 计划意/海外（土耳其/乌兹别克/亚美尼亚/黑山/俄罗斯）新开。",
   "生活方式延伸：迪拜 Trussardi Residences（与 Luxury Living）、热那亚国际游艇展生活方式伙伴；时装>90%，家居/美妆/珠宝/眼镜/香氛/童装授权经营。",
   "中国：特福隆(上海)商业运营管理有限公司代理运营；2026-04 退出俄罗斯市场。",
 ],
 "refresh_conclusion":"Trussardi 在 Miroglio 主导下处于'商业重建期'——营收高增但盈利承压，靠生活方式+中东/游艇延伸重建高端站位；对双核高端化是'小众奢侈重建'对照样本，A轮本轮已重触。",
},
{
 "key":"karl_lagerfeld","title":"Karl Lagerfeld (卡尔拉格斐)","slug":"卡尔拉格斐2026中国",
 "tags":["karl_lagerfeld","competitor","luxury","womenswear","menswear","germany","focus_brand"],
 "summary":"七匹狼 2017 以 3.2 亿收购大中华区；2025 营收 3.77 亿、净亏 6649 万、减值 8279 万；2026H1 营收 1.88 亿、净利 277 万(+147.3%)，中国 54 店。",
 "urls":["https://wap.eastmoney.com/a/202604273720679476.html",
         "https://www.sohu.com/a/1014120556_114984",
         "https://finance.biggo.com/news/6t7U1p0B6tLPsnrZjZcx",
         "https://so.html5.qq.com/page/real/search_news?docid=70000021_5046a56190658852"],
 "refresh_core":[
   "七匹狼 2017 以 3.2 亿收购大中华区；2025 Karl Lagerfeld 营收 3.77 亿、净亏 6649 万、减值 8279 万、净资产 -1.6 亿；2026H1 营收 1.88 亿、净利 277.42 万(+147.3%) 扭亏。",
   "中国 54 家店（约 70% 三四线）；运营商加拉格(上海)商贸有限公司；定位轻奢成衣/配饰/香水。",
   "2026 营销快闪：上海愚园路 pop-up（5 月）、深圳万象天地'KARL 巴黎俱乐部'(7.17-7.30) 强化年轻化。",
   "母公司七匹狼 2026H1 营收 8.85 亿(+4.9%)/归母 4982 万(-66.67%，炒股收益减少)/扣非 1.56 亿(+302.63%)；预计 2026 上半年由盈转亏(1950-2900 万)。",
 ],
 "refresh_conclusion":"Karl Lagerfeld 中国 2026H1 扭亏靠费用管控与快闪营销，但母企七匹狼主业承压、投资端波动；是'代理轻奢品牌在中国扭亏'的样本，对双核高端线有渠道/营销参照，A轮本轮已重触。",
},
{
 "key":"salomon","title":"Salomon (萨洛蒙)","slug":"萨洛蒙2026Q1中国",
 "tags":["salomon","competitor","sportswear","outdoor","trail_running","france","focus_brand"],
 "summary":"亚玛芬 2026Q1 营收 $19.46B(+32.1%)，大中华 +44.5% 至 $6.45B；Salomon 户外 +42% 至 $7.14B 超始祖鸟成集团增长火车头，中国门店 Q1 净 +9→302。",
 "urls":["https://www.news.cn/fashion/20260522/3004f47ee1ab4305a50d54fb086a3d87/c.html",
         "https://www.fxbaogao.com/detail/5433353",
         "https://finance.biggo.com.tw/news/Ume-RJ4BNl__-4_GJVKD",
         "https://longbridge.com/en/quote/AS.US/news/292582541"],
 "refresh_core":[
   "亚玛芬(AS) 2026Q1 营收 $19.46B(+32.1%)，大中华 +44.5% 至 $6.45B；户外性能（Salomon）+$42% 至 $7.14B，占比 36.7% 超始祖鸟成集团增长火车头。",
   "中国门店 Q1 净 +9→302，全年计划净 +45（原 +35）；聚焦高流量商场大店模型；'运奢'定位拓展泛运动人群。",
   "大中华区新任负责人杜文君（上海交大/Nike 20 年）推动 Salomon 向全品类户外转型（鞋→服延伸）。",
   "2025 Salomon >$2B(+35%)，大中华 $18.62B(+43.4%)；鞋服双线全球走红，成亚玛芬'第二增长曲线'。",
 ],
 "refresh_conclusion":"Salomon 借亚玛芬运营成中国运动户外'第二始祖鸟'，大店+运奢打法高速扩张；对双核是'专业品牌时尚化+渠道效率'的强对标，A轮本轮已重触。",
},
{
 "key":"crocs","title":"Crocs (卡骆驰)","slug":"卡骆驰2026Q2中国",
 "tags":["crocs","competitor","footwear","casual","usa","focus_brand"],
 "summary":"Crocs 2026Q2 营收 $1.2B(+2%)，核心品牌首破单季 $1B(+4%)；中国双位数增长，芭蕾风洞洞鞋破圈，樊振东全球代言，但白牌平替冲击高价联名。",
 "urls":["https://finance.yahoo.com/markets/stocks/articles/crocs-q2-earnings-call-highlights-160421616.html",
         "https://www.nasdaq.com/articles/crocs-q2-earnings-call-highlights",
         "https://k.sina.com.cn/article_7879849969_1d5acf7f106801hfv8.html",
         "https://new.qq.com/rain/a/20260811A0CFFH00"],
 "refresh_core":[
   "2026Q2 营收 $1.2B(+2%)，Crocs 品牌首破单季 $1B(+4%)；HEYDUDE -6%；国际 +7%（中国/印度/日本双位数）；DTC +12%。",
   "毛利率 60%(-170bps，关税冲击)；全年指引上调（营收 +1~2% / Crocs +2~3%）；授权 $1.5B 回购。",
   "中国双位数增长；芭蕾风洞洞鞋(399 元)天猫单链售 4 万、抖音话题 1.2 亿；樊振东 2025-07 全球代言。",
   "平替冲击：白牌 29.9/39.9 元月销数十万双，高价联名(瑞幸 569 元)遇冷；基础款(200-500 元)撑基本盘，高端时尚形象与性价比矛盾。",
 ],
 "refresh_conclusion":"Crocs 中国靠品类创新(芭蕾风)+代言实现双位数增长，但高价联名遇冷、白牌平替分流，'时尚溢价 vs 性价比'矛盾凸显；对双核是休闲品类'爆款迭代+平替防御'样本，A轮本轮已重触。",
},
{
 "key":"mlb","title":"MLB (F&F)","slug":"MLB_FF_2026中国万亿",
 "tags":["mlb","competitor","streetwear","sportswear","korean_wave","focus_brand"],
 "summary":"F&F 2026Q1 合并营收 5609 亿韩元(+10.9%)，中国法人 3031 亿(+17.2%)；2025 中国 9603 亿韩元、2026 预计破 1 万亿，MLB 中国门店 1078→1094。",
 "urls":["https://biz.chosun.com/en/en-retail/2026/05/07/2UTWQI2QHJDYTEDVPOA5RPNJG4/",
         "https://www.chosun.com/english/industry-en/2026/05/07/4YCHY56A3RBT5EKOZIGW3ZNZXE/",
         "https://www.theguru.co.kr/news/article.html?no=102362",
         "http://beautynext.cn/deepselection.html?newsid=4128105"],
 "refresh_core":[
   "F&F 2026Q1 合并营收 5609 亿韩元(+10.9%)/营业 1535 亿(+24.2%)；中国法人 3031 亿(+17.2%) 领跑。",
   "中国法人 2025 达 9603 亿韩元，2026 预计破 1 万亿；MLB 中国门店 1078→1094(2026)；同店销售 +15%。",
   "Discovery Expedition 中国 5→23→40 店(2026)；F&F 收购香氛 Hetras 70% 股权，拓展生活方式。",
   "中国依赖度 51.1%，MLB 占 F&F 约 65%；第二引擎 Discovery 培育中，缓解单品牌风险。",
 ],
 "refresh_conclusion":"MLB(F&F) 凭'MLB 授权 IP + 帽饰/老花'在中国高速增至万亿韩元规模，但中国依赖度过高、需 Discovery 第二曲线；是'韩潮 IP 授权爆发'标杆，对双核年轻线有直接竞争，A轮本轮已重触。",
},
{
 "key":"two_am","title":"2AM (凌晨两点)","slug":"2AM卡宾3D打印鞋",
 "tags":["two_am","competitor","streetwear","footwear","cabbeen_sub","focus_brand"],
 "summary":"卡宾旗下年轻潮牌/鞋履线；2026-03 吉隆坡 The Starhill 快闪（3D 打印鞋）标志全球扩张，占卡宾营收约 4.1%。",
 "urls":["https://mytruthmedia.com?p=100693/",
         "https://www.malaymail.com/news/showbiz/2026/03/07/final-hours-to-catch-cabbeen-and-2am-pop-up-as-futuristic-fashion-takeover-at-starhill-draws-kl-crowds/211736",
         "https://www.daily8.com/en/article/a90f7361bfe0ba94b05b7a84dd5d239d",
         "https://cpv3dev3.appasia.net/?p=4834474"],
 "refresh_core":[
   "卡宾旗下年轻潮牌/鞋履线；2026-03-04 至 03-08 吉隆坡 The Starhill 快闪（与 CABBEEN 联名），标志全球扩张（马来深耕）。",
   "3D 打印运动鞋系列（360° 透气格栅结构，轻量+环保）：AWAKE / ROCKER / EVOLVE / HYBRID，售价 RM389-RM1189。",
   "占卡宾营收约 4.1%；马来 Sunway Velocity、Pavilion Bukit Jalil 已有门店，与 CABBEEN 主牌协同出海。",
 ],
 "refresh_conclusion":"2AM 以'3D 打印鞋履 + 科技街头'作为卡宾年轻化与出海试验田，体量小(占 4.1%)但代表'制造+设计'差异化路径；对双核是子品牌孵化样本，A轮本轮已重触。",
},
{
 "key":"chuu","title":"CHUU","slug":"CHUU_2026退潮样本",
 "tags":["chuu","competitor","womenswear","korean_wave","fast_fashion","focus_brand"],
 "summary":"韩国 PPB STUDIO 快时尚女装；2026 初中国 300+ 店，赵露思首位全球代言人，但韩潮退潮、声量≠转化、白牌平替分流。",
 "urls":["https://baike.baidu.com/item/Chuu",
         "https://yun-f.cfw.cn/view/n381513.html",
         "https://new.qq.com/rain/a/20250806A0576H00",
         "https://k.sina.com.cn/article_6724296968_190cca10801901ab1m.html"],
 "refresh_core":[
   "韩国 PPB STUDIO 快时尚女装；2026 初中国 300+ 店（与 NO ONE ELSE 合计 231 家 2021-2025），主要中高端商场。",
   "2026-03 赵露思成首位全球代言人，'甜酷混搭'定位；核心客群 15-28 岁。",
   "杭州黯涉品牌管理集团运营；定价 99-899 元；线上天猫/京东/抖音/小红书/得物。",
   "韩潮退潮风险：声量≠转化，白牌平替冲击；高端女装'艾诺丝/迪卡轩'分流年轻客群。",
 ],
 "refresh_conclusion":"CHUU 是中国'韩潮快时尚'代表但已现退潮——门店规模仍在但声量转化走弱、平替分流；对双核女装线是'韩流红利消退'的预警样本，A轮本轮已重触。",
},
{
 "key":"ariose_years","title":"艾诺丝雅诗 (ARIOSE YEARS)","slug":"艾诺丝雅诗2026动态",
 "tags":["ariose_years","competitor","womenswear","premium","focus_brand"],
 "summary":"杭州爱唯（2025-12 更名爱唯时尚集团）；ARIOSE YEARS 中高端女装 1800+ 店/年销约 50 亿/百万会员，子品牌 AW PROJECT 重奢拓店。",
 "urls":["https://aiqicha.baidu.com/details/rankList?query=a597151601884fd426024ff821ed621c&type=20",
         "https://aiqicha.baidu.com/details/ugknowledge?id=e7b078e8eb75790b95b00ff249602f46",
         "https://baike.baidu.com/item/%E6%9D%AD%E5%B7%9E%E7%88%B1%E5%94%AF%E6%9C%8D%E9%A5%B0%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/8297998",
         "https://m.maigoo.com/brand/112533.html"],
 "refresh_core":[
   "杭州爱唯服饰 2025-12-17 更名'杭州爱唯时尚集团有限公司'；ARIOSE YEARS 艾诺丝雅诗 2005 创立，中高端都市简约女装。",
   "全国 1800+ 店(2026-03)，年销约 50 亿，百万会员，杭州女装 TOP3，号称'EP 雅莹平替'。",
   "子品牌 AW PROJECT（2024-09 轻奢设计师，上海首店港汇恒隆首日 60 万）；2026-03 注册'ARIOSE YEARS/ARIOSE'。",
   "价格带：衬衫 789-1380/裙约 1280/外套 980（奥莱 455-703/768/566）；一二线 A/B+ 商圈直营+奥莱专柜。",
 ],
 "refresh_conclusion":"艾诺丝雅诗以'高性价比中高端女装 + 规模门店(1800+)+ 子品牌 AW PROJECT 轻奢上探'稳居杭州女装头部；是双核女装'区域龙头规模化'对标，A轮本轮已重触。",
},
{
 "key":"dekashell","title":"迪卡轩 (DEKASHELL)","slug":"迪卡轩2026春季",
 "tags":["dekashell","competitor","womenswear","light_elegant","focus_brand"],
 "summary":"杭州旭弘实业（原佰加服饰）轻淑女装；2007 创立，30 省 600+ 店，战略冲杭州女装头部；2026 春季'无界映像'联名艺术家。",
 "urls":["http://dekashell.ef43.com.cn",
         "https://www.quanzhi.com/company/145578395",
         "https://www.zhipin.com/job_detail/04f8446a3eff38bc03J83tq5FldS.html",
         "https://ima.qq.com/wiki/?shareId=2dab671ee2cf3fb4a2bbf567a5b98a48d4efb3947b83a6f9c503a78046f05072"],
 "refresh_core":[
   "杭州旭弘实业（原佰加服饰）轻淑女装；2007 创立，30 省 600+ 店（另一口径 300+），战略冲杭州女装头部阵营。",
   "2026 春季系列'无界映像 BOUNDLESS REFLECTIONS'，联手阿姆斯特丹艺术家 Imke Ligthart；'Style by Me'理念。",
   "定位都市优雅/简约/轻松；非上市无财报；加盟模式（需加盟费+保证金），中高档价格。",
   "客群：都市新女性；与艾诺丝雅诗同属杭州女装重点补充品牌，区域集群效应明显。",
 ],
 "refresh_conclusion":"迪卡轩以'轻淑女装 + 艺术联名(2026 春季无界映像) + 加盟规模(600+店)'稳居杭州女装新锐；与艾诺丝同属用户指定重点女装补充，A轮本轮已重触。",
},
]

def source_md(b):
    src_file="2026-08-15_R4_%s.md" % safe(b["slug"])
    raw_file="2026-08-15_R4_%s.md" % safe(b["slug"])
    tags=", ".join(b["tags"]+["2026","competitor_update","R4_refresh"])
    core="\n".join("- %s" % c for c in b["refresh_core"])
    urls="\n".join("- %s" % u for u in b["urls"])
    return f"""---
type: source
title: {b['source_title'] if 'source_title' in b else b['slug']}
tags: [{tags}]
sources: [raw/articles/{raw_file}]
created: {DATE}
updated: {DATE}
cross_refs: [[{b['key']}]], [[服装行业竞争格局]]
---

# {DATE} {b['source_title'] if 'source_title' in b else b['slug']}

> **一句话摘要**：{b['summary']} 本页为 Round A 第 4 轮（全量覆盖焦点品牌）2025-2026 最新动态刷新，落位实体 [[{b['key']}]]。

## 核心要点
{core}

## 来源链接
{urls}

## 关联页面
- [[{b['key']}]] — 实体页
- [[服装行业竞争格局]] — 行业格局
"""

def raw_md(b):
    raw_file="2026-08-15_R4_%s.md" % safe(b["slug"])
    urls="\n".join("- %s" % u for u in b["urls"])
    core="\n".join("- %s" % c for c in b["refresh_core"])
    return f"""# {DATE} {b['slug']}（raw 剪藏）

> 采集方式：WebSearch 提炼，Round A 第 4 轮 全量覆盖刷新。
> 关联实体：{b['title']}（{b['key']}）

## 原文/来源链接
{urls}

## 关键事实（提炼）
{core}

## 备注
- 本文件为原始资料层（raw），仅供 [[../wiki/sources/{raw_file[:-3]}]] 引用。
"""

def entity_append(b, existing):
    src_file="2026-08-15_R4_%s.md" % safe(b["slug"])
    # 1) add source to frontmatter sources (if not present)
    m=re.search(r"^sources:\s*\[(.*?)\]\s*$", existing, re.M)
    if m:
        cur=m.group(1).strip()
        if src_file not in cur:
            new=(cur+", "+src_file) if cur else src_file
            existing=existing[:m.start()]+"sources: [%s]"%new+existing[m.end():]
    # 2) ensure cross_refs has 服装行业竞争格局
    m2=re.search(r"^cross_refs:\s*(.*?)\s*$", existing, re.M)
    if m2:
        cr=m2.group(1)
        if "[[服装行业竞争格局]]" not in cr:
            existing=existing[:m2.start()]+"cross_refs: "+cr.rstrip()+", [[服装行业竞争格局]]"+existing[m2.end():]
    # 3) append refresh section before 关联页面 or at end
    sec=f"""
## 近期动态刷新（{DATE} · A轮第4轮全量覆盖）

> 本轮按用户硬性规则"每次 A轮必须覆盖全部 focus_brands"对既有实体页做 2025-2026 最新动态刷新。

### 本轮核心动态
{chr(10).join('- '+c for c in b['refresh_core'])}

### 本轮新增结论
- {b['refresh_conclusion']}

### 信息链（本轮）
- 上游来源：[[{src_file[:-3]}]] → 本页（[[{b['key']}]]）→ 下游应用：[[服装行业竞争格局]]、[[peacebird]]、[[cabbeen]]
"""
    if "## 关联页面" in existing:
        existing=existing.replace("## 关联页面", sec.strip()+"\n\n## 关联页面", 1)
    else:
        existing=existing.rstrip("\n")+"\n"+sec
    return existing

os.makedirs(ENT, exist_ok=True)
os.makedirs(SRC, exist_ok=True)
os.makedirs(RAW, exist_ok=True)

written=[]
index_sources=[]
index_backlinks=[]

for b in BRANDS:
    src_file="2026-08-15_R4_%s.md" % safe(b["slug"])
    raw_file="2026-08-15_R4_%s.md" % safe(b["slug"])
    ep=os.path.join(ENT, b["key"]+".md"); sp=os.path.join(SRC, src_file); rp=os.path.join(RAW, raw_file)
    # entity (append)
    with open(ep, encoding="utf-8") as f:
        old=f.read()
    new_ent=entity_append(b, old)
    with open(ep, "w", encoding="utf-8") as f:
        f.write(new_ent)
    # source + raw
    with open(sp, "w", encoding="utf-8") as f:
        f.write(source_md(b))
    with open(rp, "w", encoding="utf-8") as f:
        f.write(raw_md(b))
    written.append(ep); written.append(sp); written.append(rp)
    summ=b["summary"]
    if len(summ)>60: summ=summ[:58]+"…"
    index_sources.append((src_file, summ, ", ".join(b["tags"]+["source","R4"])))
    bl_desc=b["summary"]
    if len(bl_desc)>46: bl_desc=bl_desc[:44]+"…"
    index_backlinks.append((b["key"], bl_desc+" (2026 R4刷新)"))
    print("written:", b["key"], "|", src_file)

with open("_roundA_run4_paths.txt","w",encoding="utf-8") as f:
    f.write("\n".join(written)+"\n")

json.dump({"SOURCES":index_sources,"BACKLINKS":index_backlinks},
          open("_roundA_run4_index_data.json","w",encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\nDONE. %d brands, %d files. pathspec + index_data written." % (len(BRANDS), len(written)))
