#!/usr/bin/env python3
"""Cross-file contradiction scan v2 — accurate attribution.
Rules to suppress false positives:
- A source/comparison number is attributed to brand B only when B appears on the
  SAME LINE as the metric value (line-level), preventing peer-table misattribution.
- A source contributes B's metrics only if the source is ABOUT B
  (filename/title contains B's alias) OR it's a line clearly labeling B.
- Currency guarding: revenue/net_profit compared only when same currency context.
"""
import os
import re, json
from pathlib import Path
from collections import defaultdict

WIKI = Path(os.environ.get("KB_ROOT") or Path(__file__).resolve().parents[1] / "knowledge_base")  # KB 根：KB_ROOT 环境变量优先，默认按脚本位置推导 / "wiki"

BRANDS = {
    'peacebird':   ['太平鸟', 'PEACEBIRD'],
    'muson_gxg':   ['GXG', '慕尚'],
    'fast_retailing': ['迅销', '优衣库', 'UNIQLO'],
    'inditex_zara': ['ZARA', 'zara', 'Inditex'],
    'hla':         ['海澜之家', '海澜'],
    'semir':       ['森马'],
    'lululemon':   ['lululemon', 'Lululemon'],
    'jnby':        ['江南布衣', 'JNBY'],
    'bienlefen':   ['比音勒芬'],
    'bosideng':    ['波司登'],
    'hm':          ['H&M', 'H & M'],
    'anta':        ['安踏'],
    'burberry':    ['博柏利', 'Burberry'],
    'top_sports':  ['滔搏'],
    'septwolves':  ['七匹狼'],
    'lilanz':      ['利郎'],
}

METRICS = {
    'gross_margin': r'(?:毛利率|毛利)[：:\s约]*?([\d.]+)\s*%',
    'net_margin':   r'(?:净利率|净利)[：:\s约]*?([\d.]+)\s*%',
    'revenue':      r'(?:营收|收入|营业总收入)[：:\s约]*?([\d.]+)\s*亿',
    'net_profit':   r'(?:归母净利润|净利润|归母净利)[：:\s约]*?([\d.]+)\s*亿',
    'revenue_growth': r'(?:营收|收入).{0,10}?(?:增长|同比|增速)[：:\s约]*?([\d.+-]+)\s*%',
    'profit_growth':  r'(?:净利|利润).{0,10}?(?:增长|同比|增速)[：:\s约]*?([\d.+-]+)\s*%',
}

FX = re.compile(r'(美元|USD|US\$|欧元|€|EUR|SEK|瑞典克朗|英镑|£|GBP|日元|JPY|亿日元|亿欧元|亿瑞典|亿英镑|亿美)')

def detect_period(text, pos):
    window = text[max(0, pos-70):pos]
    y = '2026' if '2025' not in window else '2025'
    if re.search(r'FY2025|2025FY|2025全年|2025年全|全年', window): return 'FY2025'
    if re.search(r'九个月|前三季度|9M|9个月', window): return f'{y}9M'
    if re.search(r'H1|上半年|中报|半年', window): return f'{y}H1'
    if re.search(r'Q1|一季度|1季度|季报', window): return f'{y}Q1'
    if re.search(r'Q2|二季度|2季度', window): return f'{y}Q2'
    if re.search(r'Q3|三季度|3季度', window): return f'{y}Q3'
    if re.search(r'FY2026|2026财年|2026全年', window): return 'FY2026'
    return 'unspecified'

records = []

def add(brand, metric, period, val, rel, cur=None):
    records.append(dict(brand=brand, metric=metric, period=period, val=val, rel=rel, cur=cur))

# 1) ENTITY pages — whole page belongs to the brand
for f in (WIKI/'entities').glob('*.md'):
    b = f.stem
    if b not in BRANDS:
        continue
    text = f.read_text(encoding='utf-8', errors='ignore')
    for metric, pat in METRICS.items():
        for mm in re.finditer(pat, text, re.IGNORECASE):
            val = float(mm.group(1))
            mpos = mm.end()
            period = detect_period(text, mpos)
            cur = 'fx' if FX.search(text[max(0,mpos-40):mpos+5]) else None
            add(b, metric, period, val, str(f.relative_to(WIKI)), cur)

# 2) COMPARISONS + 3) SOURCES — line-level, brand on same line as metric
def scan_linebased(path, about_brand=None):
    rel = str(path.relative_to(WIKI))
    text = path.read_text(encoding='utf-8', errors='ignore')
    for line in text.splitlines():
        for brand, aliases in BRANDS.items():
            if about_brand and brand != about_brand:
                continue
            if not any(a in line for a in aliases):
                continue
            for metric, pat in METRICS.items():
                for mm in re.finditer(pat, line, re.IGNORECASE):
                    val = float(mm.group(1))
                    mpos = mm.end()
                    period = detect_period(line, mpos)
                    cur = 'fx' if FX.search(line[max(0,mpos-40):mpos+5]) else None
                    add(brand, metric, period, val, rel, cur)

for f in (WIKI/'comparisons').glob('*.md'):
    scan_linebased(f)

for f in (WIKI/'sources').glob('*.md'):
    nm = f.name
    # only sources about a specific brand (filename contains an alias) contribute
    matched = [b for b, aliases in BRANDS.items() if any(a in nm for a in aliases)]
    if not matched:
        continue
    # sources covering multiple brands (rankings/peer tables) — still line-based per brand
    scan_linebased(f)

# Group by (brand, metric, period). Per file value + currency.
groups = defaultdict(lambda: defaultdict(list))
for r in records:
    groups[(r['brand'], r['metric'], r['period'])][r['rel']].append(r)

contradictions = []
for (b, m, p), filemap in groups.items():
    if p == 'unspecified':
        continue
    # group files by currency for revenue/net_profit
    if m in ('revenue', 'net_profit'):
        by_cur = defaultdict(dict)
        for rel, rs in filemap.items():
            cur = rs[0]['cur'] or 'rmb'
            by_cur[cur][rel] = sum(x['val'] for x in rs)/len(rs)
        for cur, fm in by_cur.items():
            if len(fm) < 2:
                continue
            vals = list(fm.values())
            lo, hi = min(vals), max(vals)
            tol = max(1.0, hi*0.03)
            if hi-lo > tol:
                contradictions.append((b, m, p, cur, fm))
    else:
        if len(filemap) < 2:
            continue
        fm = {rel: sum(x['val'] for x in rs)/len(rs) for rel, rs in filemap.items()}
        vals = list(fm.values())
        lo, hi = min(vals), max(vals)
        tol = max(1.5, hi*0.03) if m in ('gross_margin','net_margin') else hi*0.03
        if hi-lo > tol:
            contradictions.append((b, m, p, 'pct', fm))

print("🔍 跨文件矛盾检测 v2 (line-level attribution + 货币守卫)")
print("=" * 70)
if not contradictions:
    print("✅ 无数据矛盾")
else:
    for b, m, p, cur, fm in contradictions:
        parts = "  |  ".join(f"{rel}={v:.2f}" for rel, v in fm.items())
        print(f"⚠️ 矛盾：[{b}] [{m}] [{p}] [{cur}]  {parts}")

with open(Path(__file__).resolve().parents[1] / "_contradiction_scan_result.json", 'w', encoding='utf-8') as f:
    json.dump([{'brand':b,'metric':m,'period':p,'cur':c,'per_file':{k:round(v,4) for k,v in fm.items()}}
               for b,m,p,c,fm in contradictions], f, ensure_ascii=False, indent=2)
print(f"\n共发现 {len(contradictions)} 处跨文件矛盾（已保存）")
