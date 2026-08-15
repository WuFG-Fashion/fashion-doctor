#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建 MODING GROUP 品牌墙实体页，并将卡宾提升为核心品牌。
"""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r"D:\Fashion Doctor\fashion-doctor")
WIKI = ROOT / "knowledge_base" / "wiki"
ENTITIES = WIKI / "entities"
COMPARISONS = WIKI / "comparisons"
KB = ROOT / "knowledge_base" / "kb_benchmarks.json"
INDEX = WIKI / "index.md"
TODAY = "2026-08-14"

# 卡宾：核心品牌， richer stub
CABBEEN = {
    "file": "cabbeen.md",
    "title": "卡宾（Cabbeen）",
    "tags": ["cabbeen", "competitor", "menswear", "streetwear", "china_brand", "moding_group", "core"],
    "summary": "中国设计师男装品牌，Cabbeen 由杨紫明 1997 年创立，定位都市潮流/休闲男装，是 MODING GROUP 品牌矩阵中仅次于太平鸟的核心关注品牌。",
    "extra": """## 核心判断

1. **设计师基因 vs 规模化挑战**：Cabbeen 以设计师品牌起家，差异化在于街头潮流与都市休闲结合，但规模、渠道数字化与供应链效率仍需对标太平鸟补齐。
2. **MODING GROUP 矩阵中的男装支点**：与太平鸟（全品类时尚集团）、GXG（通勤男装）、海澜之家（大众男装）形成差异化男装竞争位，可作为"设计师男装"赛道样本。
3. **数据待补**：当前知识库缺乏 Cabbeen 公开财务与运营数据，需后续 ingest 年报/招股书/行业报告。

## 关联对标
- 同集团/同矩阵：[[moding_haute_couture|MODING GROUP]]
- 直接竞品：[[peacebird|太平鸟]]、[[muson_gxg|GXG/慕尚]]、[[lilanz|利郎]]、[[hla|海澜之家]]
- 概念：[[男装品牌竞争格局2026Q1]]、[[服装行业竞争格局]]
""",
}

# MODING GROUP 品牌墙其余品牌（按图中从左到右、从上到下）
BRANDS = [
    {"file": "trussardi.md", "title": "Trussardi", "tags": ["trussardi", "competitor", "luxury", "italy", "leather", "moding_group"], "summary": "意大利百年奢侈品牌，以皮具与高级成衣闻名，现属 MODING GROUP 矩阵中的顶奢线代表。", "country": "Italy"},
    {"file": "awoken_space.md", "title": "AWOKEN-SPACE", "tags": ["awoken_space", "competitor", "streetwear", "moding_group"], "summary": "MODING GROUP 旗下潮流品牌，定位年轻街头与空间美学。", "country": "China"},
    {"file": "mr_mrs.md", "title": "Mr & Mrs Italy", "tags": ["mr_mrs", "competitor", "luxury", "outerwear", "italy", "moding_group"], "summary": "意大利高端皮草派克外套品牌，以军绿色皮草内胆派克大衣出圈。", "country": "Italy"},
    {"file": "king_baby.md", "title": "KING BABY", "tags": ["king_baby", "competitor", "accessories", "jewelry", "streetwear", "moding_group"], "summary": "美国摇滚风格银饰与配饰品牌，定位潮流文化周边。", "country": "USA"},
    {"file": "marcelo_burlon.md", "title": "Marcelo Burlon", "tags": ["marcelo_burlon", "competitor", "streetwear", "luxury_streetwear", "italy", "moding_group"], "summary": "意大利高端街头品牌，以翅膀图腾与俱乐部文化著称。", "country": "Italy"},
    {"file": "etudes.md", "title": "Études", "tags": ["etudes", "competitor", "menswear", "contemporary", "france", "moding_group"], "summary": "法国当代男装/无性别品牌，以艺术联名与蓝色调视觉识别著称。", "country": "France"},
    {"file": "diesel.md", "title": "DIESEL", "tags": ["diesel", "competitor", "denim", "premium_denim", "italy", "moding_group"], "summary": "意大利高端牛仔与生活方式品牌，牛仔丹宁赛道标杆。", "country": "Italy"},
    {"file": "g_star_raw.md", "title": "G-STAR RAW", "tags": ["g_star_raw", "competitor", "denim", "premium_denim", "netherlands", "moding_group"], "summary": "荷兰高端牛仔品牌，以 raw denim 与 3D 剪裁闻名。", "country": "Netherlands"},
    {"file": "dkny.md", "title": "DKNY", "tags": ["dkny", "competitor", "womenswear", "menswear", "lifestyle", "usa", "moding_group"], "summary": "美国都市生活方式品牌，Donna Karan 旗下副线，定位摩登都市通勤。", "country": "USA"},
    {"file": "karl_lagerfeld.md", "title": "KARL LAGERFELD", "tags": ["karl_lagerfeld", "competitor", "luxury", "womenswear", "menswear", "germany", "moding_group"], "summary": "以老佛爷命名的轻奢品牌，由 KARL LAGERFELD 授权运营，覆盖成衣、配饰与香水。", "country": "Germany/France"},
    {"file": "koyo.md", "title": "KOYO", "tags": ["koyo", "competitor", "streetwear", "contemporary", "moding_group"], "summary": "MODING GROUP 旗下当代潮流品牌，具体定位待补充。", "country": "China"},
    {"file": "tommy_hilfiger.md", "title": "Tommy Hilfiger", "tags": ["tommy_hilfiger", "competitor", "premium", "menswear", "womenswear", "usa", "moding_group"], "summary": "美国经典休闲品牌，以红白蓝旗标与学院风、美式休闲著称，PVH 集团旗下。", "country": "USA"},
    {"file": "lacoste.md", "title": "LACOSTE", "tags": ["lacoste", "competitor", "sportswear", "premium", "france", "moding_group"], "summary": "法国高端运动休闲品牌，以鳄鱼标志与 Polo 衫闻名，网球基因。", "country": "France"},
    {"file": "nautica.md", "title": "NAUTICA", "tags": ["nautica", "competitor", "menswear", "sportswear", "usa", "moding_group"], "summary": "美国航海灵感生活方式品牌，以帆船 logo 与海洋风休闲装著称。", "country": "USA"},
    {"file": "salomon.md", "title": "SALOMON", "tags": ["salomon", "competitor", "sportswear", "outdoor", "trail_running", "france", "moding_group"], "summary": "法国户外与越野跑装备品牌，亚玛芬体育旗下，山系/机能风潮代表。", "country": "France"},
    {"file": "speedo.md", "title": "Speedo", "tags": ["speedo", "competitor", "sportswear", "swimwear", "uk", "moding_group"], "summary": "英国竞技泳装品牌，专业游泳装备代名词。", "country": "UK"},
    {"file": "hoka_one_one.md", "title": "HOKA ONE ONE", "tags": ["hoka_one_one", "competitor", "sportswear", "running", "footwear", "usa", "moding_group"], "summary": "美国厚底跑鞋品牌，Deckers 旗下，近年从专业跑圈破圈至潮流穿搭。", "country": "USA"},
    {"file": "adlv.md", "title": "ADLV（acmé de la vie）", "tags": ["adlv", "competitor", "streetwear", "korean_wave", "moding_group"], "summary": "韩国街头潮牌，以婴儿脸印花与 oversize 版型在东亚市场走红。", "country": "Korea"},
    {"file": "awoken_time.md", "title": "AWOKEN-TIME", "tags": ["awoken_time", "competitor", "streetwear", "moding_group"], "summary": "MODING GROUP 旗下潮流品牌，与 AWOKEN-SPACE 同属集团潮流线。", "country": "China"},
    {"file": "ellesse.md", "title": "ellesse", "tags": ["ellesse", "competitor", "sportswear", "retro", "italy", "moding_group"], "summary": "意大利运动复古品牌，以网球与滑雪基因、半圆标志著称。", "country": "Italy"},
    {"file": "mlb.md", "title": "MLB", "tags": ["mlb", "competitor", "streetwear", "sportswear", "korean_wave", "moding_group"], "summary": "韩国 F&F 公司运营的潮流品牌，以美国职业棒球大联盟授权 logo 与帽饰、老花包出圈。", "country": "Korea (licensed from USA)"},
    {"file": "nerdy.md", "title": "NERDY", "tags": ["nerdy", "competitor", "streetwear", "korean_wave", "moding_group"], "summary": "韩国潮流品牌，以彩色运动套装与 K-pop 明星同款走红。", "country": "Korea"},
    {"file": "no_one_else.md", "title": "NO ONE ELSE", "tags": ["no_one_else", "competitor", "streetwear", "womenswear", "korean_wave", "moding_group"], "summary": "韩国/东亚潮流女装品牌，强调个性与无性别穿搭。", "country": "Korea"},
    {"file": "chuu.md", "title": "chuu", "tags": ["chuu", "competitor", "womenswear", "korean_wave", "fast_fashion", "moding_group"], "summary": "韩国快时尚女装品牌，以甜美辣妹风、-5kg 牛仔裤营销著称。", "country": "Korea"},
    {"file": "thisisizi8.md", "title": "thisisIZI8", "tags": ["thisisizi8", "competitor", "streetwear", "korean_wave", "moding_group"], "summary": "韩国/东亚潮流品牌，定位 Z 世代街头与社交货币穿搭。", "country": "Korea"},
    {"file": "levis.md", "title": "Levi's", "tags": ["levis", "competitor", "denim", "premium_denim", "usa", "moding_group"], "summary": "美国丹宁鼻祖，牛仔裤品类全球标杆，Levi Strauss & Co. 旗下。", "country": "USA"},
    {"file": "the_mr_young.md", "title": "THE MR YOUNG", "tags": ["the_mr_young", "competitor", "menswear", "contemporary", "moding_group"], "summary": "MODING GROUP 旗下 contemporary 男装品牌，具体定位待补充。", "country": "China"},
    {"file": "dickies.md", "title": "Dickies", "tags": ["dickies", "competitor", "workwear", "streetwear", "usa", "moding_group"], "summary": "美国工装品牌，以 874 工装裤与工装夹克闻名，VF 集团旗下。", "country": "USA"},
    {"file": "mlb_kids.md", "title": "MLB KIDS", "tags": ["mlb_kids", "competitor", "childrenswear", "streetwear", "korean_wave", "moding_group"], "summary": "MLB 童装线，延续老花与运动潮流基因，定位亲子与儿童街头穿搭。", "country": "Korea (licensed from USA)"},
    {"file": "two_am.md", "title": "2AM", "tags": ["two_am", "competitor", "menswear", "streetwear", "moding_group"], "summary": "MODING GROUP 旗下男装/潮流品牌，具体定位待补充。", "country": "China"},
    {"file": "crocs.md", "title": "Crocs", "tags": ["crocs", "competitor", "footwear", "casual", "usa", "moding_group"], "summary": "美国休闲洞洞鞋品牌，以舒适、IP 联名与个性化鞋花（Jibbitz）破圈。", "country": "USA"},
    {"file": "moding_haute_couture.md", "title": "MODING 高定（摩登高定）", "tags": ["moding_group", "haute_couture", "luxury", "private_service", "moding_group"], "summary": "MODING GROUP 旗下高端定制/顶奢服务线，承接高净值客户私人订制需求。", "country": "China"},
]


def make_entity(b, core=False):
    tags = ", ".join(b["tags"])
    sources = "[MODING_GROUP_brand_wall_2026]" if not core else "[MODING_GROUP_brand_wall_2026, 待补充公开财报/招股书]"
    cross = "[[peacebird]], [[cabbeen]], [[moding_haute_couture|MODING GROUP]], [[服装行业竞争格局]]" if not core else \
        "[[peacebird]], [[muson_gxg]], [[hla]], [[lilanz]], [[menswear_brands_2026q1]], [[男装品牌竞争格局2026Q1]], [[服装行业竞争格局]], [[core_brands_peacebird_cabbeen_2026]]"
    extra = b.get("extra", "")
    country_line = f"- 国家/地区：{b.get('country', '待补充')}\n" if "country" in b else ""
    return f"""---
type: entity
title: {b['title']}
tags: [{tags}]
sources: {sources}
created: {TODAY}
updated: {TODAY}
cross_refs: {cross}
---

# {b['title']}

> **一句话摘要**：{b['summary']}

{country_line}
## 结论

> ⏳ **待补充**：本页为 MODING GROUP 品牌墙录入 stub，需后续补充公开财务、渠道、产品与战略数据，再生成合成洞察。

_（规范见 [[CLAUDE.md]] 2.3）_

## 关联页面
- 同集团矩阵：[[moding_haute_couture|MODING GROUP]]
- 核心对标：[[peacebird|太平鸟]]{'' if core else '、[[cabbeen|卡宾]]'}
- 行业格局：[[服装行业竞争格局]]

{extra}
"""


def write_entities():
    created = []
    # cabbeen first
    cab_path = ENTITIES / CABBEEN["file"]
    if not cab_path.exists():
        cab_path.write_text(make_entity(CABBEEN, core=True), encoding="utf-8")
        created.append(CABBEEN["file"])
    # others
    for b in BRANDS:
        p = ENTITIES / b["file"]
        if p.exists():
            continue
        p.write_text(make_entity(b), encoding="utf-8")
        created.append(b["file"])
    return created


def create_core_comparison():
    comp = COMPARISONS / "core_brands_peacebird_cabbeen_2026.md"
    if comp.exists():
        return comp.name
    content = f"""---
type: comparison
title: 太平鸟 vs 卡宾 — 2026 核心品牌对标
compared_entities: [peacebird, cabbeen]
tags: [peacebird, cabbeen, competitor, menswear, core_brand, comparison, 2026]
sources: [MODING_GROUP_brand_wall_2026, 太平鸟公开财报]
created: {TODAY}
updated: {TODAY}
cross_refs: [[peacebird]], [[cabbeen]], [[muson_gxg]], [[hla]], [[lilanz]], [[semir]], [[menswear_brands_2026q1]], [[four_brands_2025]], [[three_brands_mid2026]]
---

# 太平鸟 vs 卡宾 — 核心品牌对标

> **一句话摘要**：太平鸟是国内全品类时尚集团龙头（A股 603877），卡宾是设计师男装起源的潮流品牌；二者在 MODING GROUP/男装赛道中形成"规模龙头 + 设计师差异化"的核心对标组合。

## 核心差异

| 维度 | 太平鸟 | 卡宾 Cabbeen |
|------|--------|-------------|
| 起源 | 1996 年宁波，大众时尚集团 | 1997 年，设计师杨紫明创立 |
| 定位 | 全品类中高端时尚（男/女/童/乐町） | 都市潮流/设计师男装 |
| 资本化 | A 股上市，公开财报完整 | 未上市/数据待补充 |
| 规模 | 2025 营收 63.34 亿，门店 2861 家 | 待补充 |
| 核心能力 | 品牌矩阵 + 渠道数字化 + 供应链 | 设计师 IP + 潮流文化 |
| 关键课题 | 关店提质、加盟下滑、盈利质量 | 规模化、渠道效率、数据透明 |

## 结论

1. **卡宾应作为"设计师男装"赛道的核心观察样本**：与太平鸟的"大众时尚集团"路径不同，卡宾代表设计师品牌商业化路线，可补全知识库对男装多元竞争形态的理解。
2. **数据补齐是首要任务**：卡宾缺乏公开财务，后续需 ingest 招股书、行业报告或集团内部数据，否则难以做量化对标。
3. **竞争关系并非零和**：太平鸟与卡宾分别覆盖"大众时尚"与"潮流设计"两个价格带，真正的直接交锋在商场渠道与年轻男性客群。

## 信息链
- 上游来源：MODING GROUP 品牌墙 + 太平鸟财报 → 本页
- 下游应用：[[menswear_brands_2026q1]] / [[男装品牌竞争格局2026Q1]] / [[服装行业竞争格局]]
"""
    comp.write_text(content, encoding="utf-8")
    return comp.name


def update_index():
    text = INDEX.read_text(encoding="utf-8")
    # 1) 在实体表顶部插入卡宾（核心）与 MODING 集团高定
    marker = "### wiki/entities/ — 实体库\n"
    insert = """| [[cabbeen]] ⭐ NEW | 卡宾（Cabbeen），设计师男装/潮流品牌；本项目仅次于太平鸟的核心关注品牌 | brand, competitor, menswear, streetwear, core |
| [[moding_haute_couture|MODING 高定]] ⭐ NEW | MODING GROUP 旗下高定/顶奢服务线 | haute_couture, luxury, moding_group |
"""
    if "[[cabbeen]]" not in text:
        text = text.replace(marker, marker + insert, 1)

    # 2) 在实体表末尾（MO&Co 之后或表格末尾）追加其余 MODING 品牌
    # 找到 entities 表格结束后的下一个 ### 标题
    end_marker = "### wiki/concepts/ — 概念库\n"
    brands_rows = ""
    for b in BRANDS:
        if b["file"] == "moding_haute_couture.md":
            continue  # 已在顶部插入
        tag_str = ", ".join(b["tags"][:5])
        brands_rows += f"| [[{b['file'].replace('.md', '')}]] ⭐ NEW | {b['title']}，{b['summary']} | {tag_str} |\n"
    if brands_rows and "[[trussardi]]" not in text:
        text = text.replace(end_marker, brands_rows + end_marker, 1)

    # 3) 更新 updated
    text = re.sub(r"updated: \d{4}-\d{2}-\d{2}", f"updated: {TODAY}", text, count=1)
    INDEX.write_text(text, encoding="utf-8")
    return "index.md updated"


def update_peacebird_crossrefs():
    p = ENTITIES / "peacebird.md"
    text = p.read_text(encoding="utf-8")
    # cross_refs 是 frontmatter 单行，追加 cabbeen 和 core comparison
    additions = []
    if "[[cabbeen]]" not in text:
        additions.append("[[cabbeen]]")
    if "[[core_brands_peacebird_cabbeen_2026]]" not in text:
        additions.append("[[core_brands_peacebird_cabbeen_2026]]")
    if additions:
        # 在 cross_refs 行末尾 ] 之前插入
        pattern = r"(cross_refs: \[.*)(\])"
        repl = r"\1, " + ", ".join(additions) + r"\2"
        text = re.sub(pattern, repl, text, count=1, flags=re.DOTALL)
        p.write_text(text, encoding="utf-8")
    return additions


def update_benchmarks():
    data = json.loads(KB.read_text(encoding="utf-8"))
    new_competitors = ["cabbeen", "trussardi", "awoken_space", "mr_mrs", "king_baby", "marcelo_burlon",
                       "etudes", "diesel", "g_star_raw", "dkny", "karl_lagerfeld", "koyo",
                       "tommy_hilfiger", "lacoste", "nautica", "salomon", "speedo", "hoka_one_one",
                       "adlv", "awoken_time", "ellesse", "mlb", "nerdy", "no_one_else", "chuu",
                       "thisisizi8", "levis", "the_mr_young", "dickies", "mlb_kids", "two_am",
                       "crocs", "moding_haute_couture"]
    added = []
    for key in new_competitors:
        if key not in data["competitors"]:
            data["competitors"][key] = {}
            added.append(key)
    data["updated"] = TODAY
    data["meta"]["updated"] = TODAY
    data["meta"]["last_scan"] = TODAY
    data["meta"]["files_scanned"] = f"{len(list(ENTITIES.glob('*.md')))} 个 wiki/entities 文件 + 56 个 wiki/concepts 文件"
    KB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return added


if __name__ == "__main__":
    created = write_entities()
    comp_name = create_core_comparison()
    idx_msg = update_index()
    additions = update_peacebird_crossrefs()
    added_bench = update_benchmarks()
    print(f"创建实体: {len(created)} 个")
    print(f"核心对比页: {comp_name}")
    print(f"索引: {idx_msg}")
    print(f"peacebird cross_refs 追加: {additions}")
    print(f"benchmarks 新增竞品: {len(added_bench)} 个")
