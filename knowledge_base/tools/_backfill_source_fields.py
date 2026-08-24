"""
批量回填老 source 页 RAG 字段（aliases / confidence / brand_specific）
=============================================================
背景：2026-08 之前的 774 篇老 source 页缺少 RAG 必填字段（aliases 28% / confidence 27% / brand_specific 24%），
本地 LLM 检索时"半盲"。本脚本按文件名来源段 + 正文特征自动推导并回填。

用法：
    python tools/_backfill_source_fields.py --dry   # 仅统计，不写入
    python tools/_backfill_source_fields.py          # 写入

推导规则：
1. confidence：
   - 文件名含 财报/年报/中报/季报/业绩 → 财报
   - 来源段为知名机构（商务部/服装协会/券商/咨询）→ 第三方数据
   - 来源段为品牌名（focus_brands）→ 品牌自宣
   - 文件名含 轮次标记（A1/A2/A3/R4/B/C/S）→ 按正文特征判断（财报数字→财报；含"预计/约/估"→媒体估算；否则第三方数据）
   - 其余 → 媒体估算
2. brand_specific：
   - 文件名或正文含 focus_brands 品牌名（中/英）→ true，否则 false
3. aliases：
   - 从 title 拆分：去除日期/来源前缀后取主题核心词 + 品牌别名
"""

import glob
import json
import os
import re
import sys
from collections import Counter

KB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(KB_ROOT, "wiki", "sources")
BENCH = os.path.join(KB_ROOT, "kb_benchmarks.json")

# ── 品牌名清单（focus_brands + 中文名 + 别名）────────────────
BRAND_ALIASES = {
    "peacebird": ["太平鸟", "PEACEBIRD"],
    "cabbeen": ["卡宾", "Cabbeen"],
    "adlv": ["ADLV", "爱德蒙"],
    "ariose_years": ["艾诺丝雅诗", "ARIOSE YEARS", "艾诺丝"],
    "awoken_space": ["AWOKEN SPACE"],
    "awoken_time": ["AWOKEN TIME"],
    "chuu": ["CHUU", "秋"],
    "crocs": ["卡骆驰", "Crocs"],
    "dekashell": ["迪卡轩", "DEKASHELL"],
    "dickies": ["Dickies", "迪凯斯"],
    "diesel": ["Diesel", "迪赛"],
    "dkny": ["DKNY"],
    "ellesse": ["Ellesse"],
    "etudes": ["Etudes", "Etds"],
    "g_star_raw": ["G-Star RAW"],
    "hoka_one_one": ["HOKA", "霍咖"],
    "humble_humble_r": ["HUMBLE HUMBLE R"],
    "karl_lagerfeld": ["Karl Lagerfeld", "老佛爷"],
    "king_baby": ["KING BABY"],
    "lacoste": ["Lacoste", "鳄鱼恤"],
    "levis": ["Levi's", "李维斯"],
    "marcelo_burlon": ["Marcelo Burlon"],
    "mlb": ["MLB", "美国职棒大联盟"],
    "mlb_kids": ["MLB KIDS"],
    "mr_mrs": ["MR & MRS", "MR&MRS"],
    "nautica": ["Nautica", "诺帝卡"],
    "nerdy": ["NERDY", "NDY"],
    "no_one_else": ["NO ONE ELSE"],
    "salomon": ["Salomon", "萨洛蒙"],
    "speedo": ["Speedo", "速比涛"],
    "the_mr_young": ["The Mr. Young"],
    "thisisizi8": ["thisisIZI8"],
    "tommy_hilfiger": ["Tommy Hilfiger", "汤米希尔费格"],
    "trussardi": ["Trussardi", "楚萨迪"],
    "two_am": ["2AM", "2AM CHINA"],
}
FOCUS_KEYS = set(BRAND_ALIASES.keys())
FOCUS_NAMES = set()
for v in BRAND_ALIASES.values():
    FOCUS_NAMES.update(v)
FOCUS_NAMES.update(FOCUS_KEYS)

# ── confidence 规则 ────────────────────────────────────
CONF_FINANCIAL = re.compile(r"财报|年报|中报|半年报|季报|业绩|盈喜|盈警|FY20|Q[1-4]")
CONF_INSTITUTION = re.compile(
    r"商务部|中国服装协会|广发证券|招商证券|中信证券|申万|欧睿|艾媒|魔镜|久谦|中研|联商|亿邦|咨询|券商"
    r"|羊毛市场|中华全国商业信息|国家统计局|中国商业联合会|retailnorthstar|InsiderMonkey"
)
CONF_BRAND_SELF = re.compile(
    r"品牌自宣|官方微博|官微|品牌方|官网|新闻稿|发布会|CFW|NamuWiki|luxeco|maideyi|fancyhints"
)
CONF_THIRD_PARTY = re.compile(
    r"知乎|搜狐|百家号|公众号|新浪|网易|腾讯|界面|36氪|IT之家|CSDN|有赞|第七在线|迪尚集团|新华网|中财网"
    r"|Megaview|megaview|Streamlit|Polars|DuckDB|FineDataLink|Kanaries|PANTEL|chenxutan"
)
ROUND_MARKS = re.compile(r"^(A[123]|R[0-9]|B|C|S)[_.]|_[A-Za-z0-9]+$")

def infer_confidence(fname, text):
    """根据文件名 + 正文推导 confidence"""
    lower = fname.lower()
    # 1. 财报类关键词优先
    if CONF_FINANCIAL.search(fname):
        return "财报"
    # 2. 品牌名 → 品牌自宣（仅当文件名主体是品牌）
    for key in FOCUS_KEYS:
        if re.search(r"(^|_)" + re.escape(key) + r"(_|$)", lower):
            return "品牌自宣"
    # 3. 轮次标记（A1/A2/A3/R4/B/C/S 采集）→ 按正文判断
    if re.match(r"^\d{4}-\d{2}-\d{2}_(A[123]|R\d|B|C|S)_", fname):
        if CONF_FINANCIAL.search(text):
            return "财报"
        if re.search(r"约|预计|估计|估约|\d+\.?\d*亿(?!\d)", text) and re.search(r"媒体|估算|报道|传", text):
            return "媒体估算"
        return "第三方数据"
    # 4. 机构来源
    if CONF_INSTITUTION.search(fname):
        return "第三方数据"
    # 5. 品牌自宣来源
    if CONF_BRAND_SELF.search(fname):
        return "品牌自宣"
    # 6. 第三方媒体来源
    if CONF_THIRD_PARTY.search(fname):
        return "第三方数据"
    # 7. 兜底
    return "媒体估算"

def infer_brand_specific(fname, text):
    """文件名或正文含焦点品牌名 → true"""
    lower_fname = fname.lower()
    for name in FOCUS_NAMES:
        if isinstance(name, str) and name.lower() in lower_fname:
            return True
    # 正文含品牌名（限制在标题附近，避免正文泛化误判）
    title_m = re.search(r"^#\s*(.+)$", text, re.M)
    if title_m:
        title = title_m.group(1)
        for name in FOCUS_NAMES:
            if isinstance(name, str) and name.lower() in title.lower():
                return True
    return False

def build_aliases(fname, title):
    """生成 aliases：品牌别名 + 主题核心词"""
    aliases = []
    lower_fname = fname.lower()
    lower_title = title.lower()
    # 品牌别名（文件名或标题含品牌 key/中文名）
    for key, names in BRAND_ALIASES.items():
        if key in lower_fname or any(n.lower() in lower_title for n in names):
            aliases.extend(names)
            break
    # 主题核心词：从 title 拆分（分隔符不含 -，避免截断括号内日期）
    title_clean = re.sub(r"^\d{4}-\d{2}-\d{2}[_ ]?", "", title)
    title_clean = re.sub(r"^(A[123]|R\d|B|C|S)[_ ]", "", title_clean)
    # 取前两个 meaningful segment
    segs = re.split(r"[\s_·—]+", title_clean)
    for s in segs:
        s = s.strip()
        if s and len(s) >= 2 and s not in aliases:
            aliases.append(s)
        if len(aliases) >= 4:
            break
    # 兜底：整个 title 作为主别名（保证 RAG 至少一层命中）
    if title_clean and title_clean not in aliases:
        aliases.append(title_clean)
    return aliases[:5]

def main():
    dry = "--dry" in sys.argv
    srcs = sorted(glob.glob(os.path.join(SOURCES, "*.md")))
    stats = Counter()
    changed = 0
    for f in srcs:
        with open(f, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        fm = re.search(r"^---\n(.*?)\n---", text, re.S)
        if not fm:
            continue
        body = fm.group(1)
        fname = os.path.basename(f)
        conf = infer_confidence(fname, text)
        bs = infer_brand_specific(fname, text)
        title_m = re.search(r"^title:\s*(.+)$", body, re.M)
        title = title_m.group(1).strip().strip('"') if title_m else os.path.splitext(fname)[0]
        aliases = build_aliases(fname, title)

        new_lines = []
        need_update = False
        # aliases 始终重算覆盖（修正截断问题）；confidence/brand_specific 仅缺失时补
        for line in body.split("\n"):
            if line.startswith("aliases:"):
                continue  # 删除旧 aliases，统一重写
            if line.startswith("confidence:") and conf:
                continue  # 已有则保留
            if line.startswith("brand_specific:") and bs is not None:
                continue
            new_lines.append(line)
        # 在 tags 行后插入缺失字段
        insert_idx = len(new_lines)
        for i, line in enumerate(new_lines):
            if line.startswith("tags:") or line.startswith("sources:"):
                insert_idx = i + 1
        missing = []
        if "aliases:" in body or True:
            alias_str = json.dumps(aliases[:5], ensure_ascii=False)
            missing.append(f"aliases: {alias_str}")
        if "confidence:" not in body:
            missing.append(f"confidence: {conf}")
        if "brand_specific:" not in body:
            missing.append(f"brand_specific: {'true' if bs else 'false'}")
        if missing:
            need_update = True
            new_lines[insert_idx:insert_idx] = missing
            stats[conf] += 1
            stats[f"brand_specific:{'true' if bs else 'false'}"] += 1
            stats["aliases"] += 1
        if not need_update:
            continue
        new_body = "\n".join(new_lines)
        new_text = text.replace(body, new_body, 1)
        if dry:
            changed += 1
            if changed <= 3:
                print(f"  [dry] {fname} → conf={conf}, bs={bs}, aliases={aliases[:4]}")
        else:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(new_text)
            changed += 1

    print(f"\n{'DRY-RUN' if dry else '已写入'} 修改文件数: {changed}/{len(srcs)}")
    if dry:
        print("字段分布预览:")
        for k, v in stats.most_common():
            print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
