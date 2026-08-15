# -*- coding: utf-8 -*-
"""为 wiki/entities 与 wiki/concepts 全量注入 frontmatter aliases（RAG 实体/概念解析）。"""
import re
from pathlib import Path

WIKI = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki")

# ---- 实体精选别名：中/英/股票代码/常见别称 ----
ENTITY_ALIASES = {
    "peacebird": ["太平鸟", "PEACEBIRD", "太平鸟服饰", "603877.SH", "太平鸟男装", "太平鸟女装"],
    "cabbeen": ["卡宾", "Cabbeen", "卡宾服饰", "2030.HK", "HK 02030", "卡宾男装"],
    "muson_gxg": ["慕尚集团", "GXG", "慕尚", "1817.HK", "gxg.jeans"],
    "hla": ["海澜之家", "HLA", "600398.SH", "海澜"],
    "semir": ["森马", "森马服饰", "Semir", "002563.SZ", "巴拉巴拉", "Balabala"],
    "fast_retailing": ["迅销", "迅销集团", "Fast Retailing", "优衣库", "UNIQLO", "9983.HK", "6288.HK"],
    "inditex_zara": ["Inditex", "ZARA", "飒拉", "印地纺", "ITX.MC"],
    "hm": ["H&M", "Hennes & Mauritz", "HM", "HM-B.ST"],
    "lululemon": ["lululemon", "Lululemon", "露露乐蒙", "露露柠檬", "LULU"],
    "anta": ["安踏", "安踏集团", "ANTA", "安踏体育", "2020.HK"],
    "bosideng": ["波司登", "Bosideng", "3998.HK"],
    "lilanz": ["利郎", "LILANZ", "1234.HK", "中国利郎"],
    "septwolves": ["七匹狼", "SEPTWOLVES", "002029.SZ"],
    "baoxiniao": ["报喜鸟", "002154.SZ", "BAOXINIAO", "报喜鸟控股"],
    "bienlefen": ["比音勒芬", "Biem.L.Fdlkk", "002832.SZ"],
    "jnby": ["江南布衣", "JNBY", "3306.HK"],
    "jiumuwang": ["九牧王", "601566.SH", "JOEONE"],
    "langzi_fashion": ["朗姿", "朗姿股份", "002612.SZ", "LANCY"],
    "anzheng_fashion": ["安正时尚", "安正时尚集团", "603839.SH", "玖姿", "JZ"],
    "ariose_years": ["艾诺丝", "艾诺丝·雅诗", "ARIOSE YEARS", "ARIOSE", "雅诗"],
    "dekashell": ["迪卡轩", "DEKASHELL"],
    "moco_epo": ["MO&Co.", "MOCo", "EPO", "EPO集团", "摩安珂", "赢家时尚"],
    "top_sports": ["滔搏", "滔搏国际", "TOP SPORTS", "6110.HK", "滔搏运动"],
    "trussardi": ["Trussardi", "楚萨迪", "托鲁纱缔"],
    "burberry": ["Burberry", "博柏利", "巴宝莉", "BRBY.L"],
    "crocs": ["Crocs", "卡骆驰", "CROX"],
    "levis": ["Levi's", "Levis", "李维斯", "LEVI"],
    "tommy_hilfiger": ["Tommy Hilfiger", "汤米·希尔费格", "TOMMY", "Tommy"],
    "lacoste": ["LACOSTE", "Lacoste", "法国鳄鱼", "鳄鱼牌"],
    "salomon": ["SALOMON", "Salomon", "萨洛蒙"],
    "hoka_one_one": ["HOKA ONE ONE", "HOKA", "Hoka", "霍伽"],
    "diesel": ["DIESEL", "Diesel", "迪赛"],
    "dkny": ["DKNY", "Donna Karan", "唐娜·凯伦"],
    "g_star_raw": ["G-STAR RAW", "G-Star", "GStar"],
    "dickies": ["Dickies", "迪凯斯"],
    "nautica": ["NAUTICA", "Nautica", "诺帝卡"],
    "speedo": ["Speedo", "速比涛"],
    "ellesse": ["ellesse", "Ellesse"],
    "karl_lagerfeld": ["KARL LAGERFELD", "Karl Lagerfeld", "卡尔·拉格斐", "老佛爷"],
    "marcelo_burlon": ["Marcelo Burlon", "Marcelo Burlon County of Milan"],
    "mr_mrs": ["Mr & Mrs Italy", "Mr&Mrs Italy"],
    "mlb": ["MLB", "MLB服饰", "美国职业棒球大联盟"],
    "mlb_kids": ["MLB KIDS", "MLB儿童", "MLB童装"],
    "adlv": ["ADLV", "acmé de la vie", "acme de la vie", "韩国ADLV"],
    "chuu": ["chuu", "CHUU", "韩国chuu"],
    "nerdy": ["NERDY", "Nerdy", "韩国NERDY"],
    "no_one_else": ["NO ONE ELSE", "No One Else"],
    "thisisizi8": ["thisisIZI8", "IZI8"],
    "awoken_space": ["AWOKEN-SPACE", "AWOKEN SPACE"],
    "awoken_time": ["AWOKEN-TIME", "AWOKEN TIME"],
    "koyo": ["KOYO"],
    "the_mr_young": ["THE MR YOUNG", "The Mr Young"],
    "two_am": ["2AM"],
    "king_baby": ["KING BABY", "King Baby"],
    "etudes": ["Études", "Etudes"],
    "suhao_fashion": ["苏豪时尚", "苏豪"],
    "style3d_lingdi": ["凌迪科技", "Style3D", "凌迪", "Lingdi"],
    "丽晶": ["丽晶", "丽晶软件", "Regent"],
    "安奈儿": ["安奈儿", "Annil", "002875.SZ"],
    "探马SCRM": ["探马", "探马SCRM", "Tanma", "探马科技"],
    "深维智信": ["深维智信", "Megaview", "深维"],
}

# ---- 概念精选别名（高价值 KPI/方法论）----
CONCEPT_ALIASES = {
    "sell_through_examination_standard_2026": ["售罄率考核基准", "售罄率", "售罄", "Sell-Through Rate", "STR"],
    "动态OTB管理": ["动态OTB管理", "OTB", "Open-to-Buy", "采购预算", "开放采购"],
    "会员复购率提升策略": ["会员复购率提升策略", "复购率", "会员复购", "Repurchase Rate"],
    "sku_fine_management": ["服装SKU精细化管理", "SKU管理", "SKU精细化", "SKU"],
    "sleeping_member_reactivation": ["沉睡会员唤醒策略", "沉睡会员", "会员唤醒", "休眠会员"],
    "semantic_layer_metrics_2026": ["语义层", "指标层", "Semantic Layer", "Metrics Layer"],
    "data_lakehouse_2026": ["湖仓一体", "Lakehouse", "数据湖仓"],
    "duckdb_olap_engine_2026": ["DuckDB", "嵌入式OLAP", "OLAP引擎"],
    "polars_vs_pandas_2026": ["Polars", "Pandas", "DuckDB", "数据框选型"],
    "streamlit_dashboard_2026": ["Streamlit", "Streamlit看板", "Streamlit仪表盘"],
    "retail_data_workflow_2026": ["零售数据分析工作流", "CRISP-DM", "数据分析流程"],
    "data_quality_governance": ["数据质量治理", "数据质量", "Data Quality"],
    "库存清仓策略": ["库存清仓策略", "清仓", "库存清仓", "清仓策略"],
    "柔性供应链与商品企划": ["柔性供应链", "商品企划", "快反供应链"],
    "服装行业竞争格局": ["服装行业竞争格局", "竞争格局", "行业格局"],
    "男装品牌竞争格局2026Q1": ["男装品牌竞争格局", "男装竞争格局", "男装格局"],
    "etl_governance_convergence_2026": ["ETL治理一体化", "ETL", "数据管道"],
    "ETL架构选型": ["ETL架构选型", "ETL", "ETL架构", "数据管道选型"],
    "AI导购陪练": ["AI导购陪练", "导购陪练", "AI陪练", "虚拟客户陪练"],
    "ai_virtual_tryon_2026": ["AI虚拟试衣", "虚拟试衣", "Virtual Try-On", "VTO"],
    "全渠道会员一体化": ["全渠道会员一体化", "全渠道会员", "会员一体化", "Omnichannel会员"],
    "会员与VIP运营体系2026": ["会员与VIP运营体系", "VIP运营", "会员运营", "VIP分层"],
}


def humanize_slug(slug):
    return slug.replace("_", " ")


def auto_aliases(stem, title):
    """无精选时自动派生：中文标题 + 英文(括号/slug) + slug 人性化。"""
    out = []
    # 中文主名（去括号英文/年份）
    zh = re.sub(r"[（(].*?[)）]", "", title).strip()
    zh = re.sub(r"\s*20\d{2}.*$", "", zh).strip(" —-")
    if zh:
        out.append(zh)
    # 括号内英文
    for m in re.findall(r"[（(]([^)）]+)[)）]", title):
        m = m.strip()
        if re.search(r"[A-Za-z]", m):
            out.append(m)
    # slug 人性化（含字母时）
    hs = humanize_slug(stem)
    if re.search(r"[A-Za-z]", stem):
        out.append(hs)
    return out


def get_title(fm):
    m = re.search(r"^title:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else ""


def inject(path, aliases):
    txt = path.read_text(encoding="utf-8")
    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", txt, re.S)
    if not m:
        return False, "no frontmatter"
    head, fm, tail = m.group(1), m.group(2), m.group(3)
    if re.search(r"^aliases:", fm, re.M):
        return False, "already has aliases"
    # 去重 & 去 title 完全相同项 & 去空
    title = get_title(fm)
    seen, clean = set(), []
    for a in aliases:
        a = (a or "").strip()
        if not a or a == title or a in seen:
            continue
        seen.add(a)
        clean.append(a)
    if not clean:
        return False, "no aliases derived"
    block = "aliases:\n" + "".join(f'  - "{a}"\n' for a in clean)
    # 插到 title 行之后；若无 title 行则插到 frontmatter 顶部
    if re.search(r"^title:.*$", fm, re.M):
        fm_new = re.sub(r"(^title:.*$)", r"\1\n" + block.rstrip("\n"), fm, count=1, flags=re.M)
    else:
        fm_new = block + fm
    path.write_text(head + fm_new + tail + txt[m.end():], encoding="utf-8")
    return True, f"+{len(clean)}"


def run(dir_name, curated):
    dd = WIKI / dir_name
    ok = skip = 0
    for p in sorted(dd.glob("*.md")):
        txt = p.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
        fm = m.group(1) if m else ""
        title = get_title(fm)
        aliases = curated.get(p.stem) or auto_aliases(p.stem, title)
        done, msg = inject(p, aliases)
        if done:
            ok += 1
        else:
            skip += 1
            print(f"  [skip] {dir_name}/{p.stem}: {msg}")
    print(f"{dir_name}: 注入 {ok}，跳过 {skip}")


run("entities", ENTITY_ALIASES)
run("concepts", CONCEPT_ALIASES)
print("done")
