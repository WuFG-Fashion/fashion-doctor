#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A1 轮(2026-08-29)实体页织入：将 12 个新 source 双链+结论+信息链织入对应实体页。
幂等：若实体页已含该 source 双链则跳过。仅改 updated 日期 + 追加织入段，不动其它结构。
"""
import re, io
from pathlib import Path

WIKI = Path("D:/Fashion Doctor/fashion-doctor/knowledge_base/wiki")
ENT = WIKI / "entities"
SRC = WIKI / "sources"

# brand_slug -> (source_slug, 结论织入, 下游应用双链)
WEAVE = {
    "cabbeen": ("2026-08-29_cabbeen_2026H1_中报与海外扩张",
        "卡宾 2026H1 营收/毛利双增(4.53亿/+7.4%、毛利46.3%)但经营利润率下滑、库存246天承压；'国潮硬科技联名(航母/火箭)+明星代言(李汶翰)+东南亚出海(马来双店)'三轴并行，是设计师品牌溢价转规模的关键路径，双核差异化定位进一步确立。",
        "[[服装行业竞争格局]] / [[core_brands_peacebird_cabbeen_2026]]"),
    "adlv": ("2026-08-29_adlv_国际市场扩张与联名",
        "ADLV 以'双胞胎创始人+婴儿脸系列'网红基因起家(2017首尔)，2024销售约450亿韩元、中国50+店，借 Disney/PinkFong 亲子联名破圈；私企无审计披露，规模估算为主，是韩国潮流小众品牌中国落地的典型样本。",
        "[[服装行业竞争格局]] / [[chuu]]"),
    "ariose_years": ("2026-08-29_ariose_years_2025业绩与AWPROJECT高端线",
        "艾诺丝(ARIOSE YEARS)2025营收约50亿、1800+店，2026推重奢线 AW PROJECT(上海港汇恒隆首日60万)上探价格带；杭州爱唯时尚集团操盘，是重点补充女装中'轻淑→重奢'升级路径的代表。",
        "[[服装行业竞争格局]] / [[dekashell]]"),
    "awoken_space": ("2026-08-29_awoken_space_资料稀缺标注",
        "AWOKEN SPACE 本轮未检索到独立服装品牌实体(仅 Malibu 疗愈工作室及与 AWOKEN TIME 混淆)，按护栏'不强行编造'标待核验；知识库暂不新增伪数据，留待后续定向核查。",
        "[[awoken_time]] / [[服装行业竞争格局]]"),
    "awoken_time": ("2026-08-29_awoken_time_武汉潮流集合店扩张",
        "AWOKEN TIME 为武汉本土潮流集合店(800+㎡、白猿宇宙 IP)，4家武汉店+外拓，是区域潮流集合店'在地文化+大店体验'模型的样本；与 AWOKEN SPACE 命名易混，已作区分标注。",
        "[[awoken_space]] / [[服装行业竞争格局]]"),
    "chuu": ("2026-08-29_chuu_赵露思代言与300店",
        "CHUU 中国超300店(2025-10)、赵露思首位全球代言(2026-03)拉动声量，但版型/质量争议持续；是韩系快时尚女装'明星带货+争议并存'的典型，需跟踪复购与口碑修复。",
        "[[服装行业竞争格局]] / [[ariose_years]]"),
    "crocs": ("2026-08-29_crocs_Q2营销与樊振东代言",
        "Crocs 2026 Q2 营收$1.179B、Crocs 品牌首破$1B、中国双位数增长，樊振东代言+BAPE联名售罄+芭蕾风洞洞鞋延续潮流势能；洞洞鞋品类中国增长引擎明确。",
        "[[服装行业竞争格局]] / [[dickies]]"),
    "dekashell": ("2026-08-29_dekashell_运营主体注销风险",
        "迪卡轩(DEKASHELL)运营主体'杭州佰加服饰有限公司'已于2023-05-08注销，构成品牌运营主体注销风险信号；历史页记'杭州旭弘实业'口径待核验，本轮作为新增风险信号收录、不强行修正历史。",
        "[[服装行业竞争格局]] / [[ariose_years]]"),
    "dickies": ("2026-08-29_dickies_易主Bluestar与密集联名",
        "Dickies 被 VF 以6亿美元售予 Bluestar Alliance(2025-09)，2026密集联名(UNION/White Mountaineering/哈雷)重启潮流叙事；所有权更迭后品牌运营策略转向'联名驱动'需持续跟踪。",
        "[[服装行业竞争格局]] / [[crocs]]"),
    "diesel": ("2026-08-29_diesel_OTB业绩与新CEO",
        "Diesel 母公司 OTB 2025营收€1.6bn(-5%)但 Diesel 实现十年最佳盈利，Andrea Rigogliosi 任新 CEO(2026-01)；品牌进入'盈利修复+新领导层'周期，是品牌墙中修复向好的样本。",
        "[[服装行业竞争格局]]"),
    "dkny": ("2026-08-29_dkny_上海首店与HaileyBieber",
        "DKNY 上海淮海中路首店(2026-05-16,245㎡)+ Hailey Bieber campaign，借 G-III 授权重启中国直营声量；是品牌墙'授权重启+明星 campaign'重入中国市场的样本。",
        "[[服装行业竞争格局]]"),
    "ellesse": ("2026-08-29_ellesse_鞋履全球授权与Smiley联名",
        "Ellesse 隶属 Pentland，NBL 获鞋履全球授权(2026-02翻倍目标)，Smiley/Michael Kors 联名延续运动时尚复古势能；是品牌墙中'授权扩张+联名'双轮驱动样本。",
        "[[服装行业竞争格局]] / [[crocs]]"),
}

def get_summary(src_slug):
    p = SRC / f"{src_slug}.md"
    if not p.exists():
        return "(摘要未取)"
    s = p.read_text(encoding="utf-8")
    for line in s.splitlines():
        if "一句话摘要" in line:
            return line.lstrip("> ").strip()
    return "(摘要未取)"

ok, skip = 0, 0
for brand, (src, concl, down) in WEAVE.items():
    ep = ENT / f"{brand}.md"
    if not ep.exists():
        print(f"⚠️ 实体页不存在: {brand}"); continue
    s = ep.read_text(encoding="utf-8")
    if f"[[{src}]]" in s:
        print(f"↩️ 已含 {src}，跳过 {brand}"); skip += 1; continue
    summ = get_summary(src)
    # 更新 updated 日期
    s = re.sub(r'(?m)^updated:.*$', 'updated: 2026-08-29', s, count=1)
    # 追加 sources 列表(单行 [..])中的 slug（防御：仅当为单行列表且不含该 slug）
    s = re.sub(r'(?m)^sources:\s*\[([^\]]*)\]\s*$',
               lambda m: f"sources: [{m.group(1).rstrip()}, {src}]" if src not in m.group(1) else m.group(0),
               s, count=1)
    section = (
        f"\n\n## A1轮全维度采集织入（2026-08-29）\n\n"
        f"> 本轮 A1 对本品做 2026 全维度核验，新增信号见 [[{src}]]。\n"
        f"- {summ}\n\n"
        f"**结论（织入）**：{concl}\n"
        f"**信息链（织入）**：[[{src}]] → 本页（[[{brand}]]） → 下游 {down}\n"
    )
    s = s.rstrip() + section
    ep.write_text(s, encoding="utf-8", newline="\n")
    ok += 1
    print(f"✅ 织入 {brand} ← {src}")

print(f"\n织入完成：新增 {ok} / 跳过 {skip}")
