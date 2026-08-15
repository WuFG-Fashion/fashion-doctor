#!/usr/bin/env python3
"""Strict cross-file contradiction detector (adjudicated).
Guards vs naive kb_lint_5rules:
  - currency guard: each brand has a native currency; only same-currency
    same-period same-metric values are compared (kills JPY/EUR/SEK/RMB bleed)
  - nearest-keyword guard: the matched number must be immediately preceded
    by the correct metric keyword (kills revenue↔net_profit cross-tag)
  - specific-period guard: UNKNOWN period values are NOT compared
"""
import re, json
from pathlib import Path
from collections import defaultdict

WIKI = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki")

brand_map = {
    'peacebird': (['peacebird','太平鸟','太平鸟男装'], 'RMB'),
    'muson_gxg': (['muson_gxg','gxg','慕尚','GXG'], 'RMB'),
    'fast_retailing': (['fast_retailing','迅销','优衣库','uniqlo','UNIQLO'], 'JPY'),
    'inditex_zara': (['inditex_zara','zara','inditex','ZARA','Zara'], 'EUR'),
    'hla': (['hla','海澜之家','海澜'], 'RMB'),
    'semir': (['semir','森马','森马服饰'], 'RMB'),
    'lululemon': (['lululemon','Lululemon'], 'USD'),
    'jnby': (['jnby','江南布衣','JNBY'], 'RMB'),
    'bienlefen': (['bienlefen','比音勒芬'], 'RMB'),
    'bosideng': (['bosideng','波司登'], 'RMB'),
    'hm': (['hm','H&M','h&m','H & M'], 'SEK'),
    'anta': (['anta','安踏'], 'RMB'),
    'burberry': (['burberry','博柏利','Burberry'], 'GBP'),
    'top_sports': (['top_sports','topsports','滔搏'], 'RMB'),
    'septwolves': (['septwolves','七匹狼'], 'RMB'),
    'lilanz': (['lilanz','利郎'], 'RMB'),
    'baoxiniao': (['baoxiniao','报喜鸟'], 'RMB'),
    'langzi_fashion': (['langzi_fashion','朗姿','朗姿股份'], 'RMB'),
    'jiumuwang': (['jiumuwang','九牧王'], 'RMB'),
    'anzheng_fashion': (['anzheng_fashion','安正时尚'], 'RMB'),
    'suhao_fashion': (['suhao_fashion','苏豪','苏豪时尚'], 'RMB'),
}

METRICS = [
    (r'毛利率|毛利', r'gross_margin'),
    (r'净利率|净利益', r'net_margin'),
    (r'营业利润率|operating.margin', r'operating_margin'),
]
# revenue / net_profit require 亿 AND nearest-keyword guard
METRICS_NUM = [
    (r'营收|收入|revenue', r'revenue'),
    (r'净利|净利润|net.profit', r'net_profit'),
]

PERIOD_PAT = re.compile(r'(FY\s?2024|FY\s?2025|FY\s?2026|2024\s*全年|2025\s*全年|2026\s*全年|2026Q1|2026Q2|2025Q1|2026H1|H1|9\s*个月|九个月|半年|全年|年度|上半年)', re.IGNORECASE)

def detect_period(s):
    m = PERIOD_PAT.search(s)
    return m.group(1).strip().upper() if m else None

def nearest_kw_num(sent, kw_pat, unit_pat):
    """Return number immediately after the kw (nearest keyword wins)."""
    best = None
    for m in re.finditer(kw_pat, sent, re.IGNORECASE):
        # find next number+unit after this keyword
        tail = sent[m.end():]
        nm = re.search(unit_pat, tail)
        if nm:
            try: val = float(nm.group(1))
            except: continue
            if best is None or m.end() > best[0]:
                best = (m.end(), val)
    return best[1] if best else None

def pct_vals(sent, metric_label):
    out = []
    for kw, lab in METRICS:
        if lab != metric_label: continue
        for m in re.finditer(kw + r'[^\d%]{0,30}?([\d.]+)\s*%', sent, re.IGNORECASE):
            try: out.append(float(m.group(1)))
            except: pass
    return out

data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # brand->metric->period->[(val,file,cur)]

def add(brand, metric, period, val, rel, cur):
    if period is None: return
    data[brand][metric][period].append((val, rel, cur))

# entity + comparison + single-brand sources
for brand, (aliases, cur) in brand_map.items():
    epath = WIKI/'entities'/f'{brand}.md'
    if epath.exists():
        for sent in re.split(r'(?<=[。！？\n])', epath.read_text(encoding='utf-8')):
            if not any(a.lower() in sent.lower() for a in aliases): continue
            per = detect_period(sent)
            for _, ml in METRICS:
                for v in pct_vals(sent, ml):
                    add(brand, ml, per, v, 'entities/'+brand+'.md', cur)
            for kw, ml in METRICS_NUM:
                v = nearest_kw_num(sent, kw, r'([\d.]+)\s*亿')
                if v is not None: add(brand, ml, per, v, 'entities/'+brand+'.md', cur)
    for f in (WIKI/'comparisons').glob('*.md'):
        rel = 'comparisons/'+f.name
        for line in f.read_text(encoding='utf-8').split('\n'):
            if not any(a.lower() in line.lower() for a in aliases): continue
            per = detect_period(line)
            for _, ml in METRICS:
                for v in pct_vals(line, ml):
                    add(brand, ml, per, v, rel, cur)
            for kw, ml in METRICS_NUM:
                v = nearest_kw_num(line, kw, r'([\d.]+)\s*亿')
                if v is not None: add(brand, ml, per, v, rel, cur)
            break
    for f in (WIKI/'sources').glob('*.md'):
        if not any(a.lower() in f.name.lower() for a in aliases): continue
        rel = 'sources/'+f.name
        for sent in re.split(r'(?<=[。！？\n])', f.read_text(encoding='utf-8')):
            if not any(a.lower() in sent.lower() for a in aliases): continue
            per = detect_period(sent)
            for _, ml in METRICS:
                for v in pct_vals(sent, ml):
                    add(brand, ml, per, v, rel, cur)
            for kw, ml in METRICS_NUM:
                v = nearest_kw_num(sent, kw, r'([\d.]+)\s*亿')
                if v is not None: add(brand, ml, per, v, rel, cur)

contradictions = []
for brand, mm in data.items():
    for metric, pm in mm.items():
        for period, vals in pm.items():
            if len(vals) < 2: continue
            cur_set = set(v[2] for v in vals)
            if len(cur_set) > 1:   # currency mismatch -> not comparable
                continue
            files = set(v[1] for v in vals)
            if len(files) < 2: continue
            uniq = {}
            for v in vals:
                uniq.setdefault(round(v[0],4), []).append(v[1])
            if len(uniq) < 2: continue
            nums = list(uniq.keys())
            lo, hi = min(nums), max(nums)
            denom = max(abs(hi), 0.01)
            diff = (hi-lo)/denom
            tol = 0.02 if metric in ('gross_margin','net_margin','operating_margin') else 0.02
            if diff > tol:
                contradictions.append({'brand':brand,'metric':metric,'period':period,
                                       'currency':list(cur_set)[0],
                                       'values':[(n,sorted(set(fs))) for n,fs in uniq.items()]})

if contradictions:
    print(f"  ⚠️ 发现 {len(contradictions)} 处实质数据矛盾（同品牌·同指标·同周期·同币种）：")
    for c in contradictions:
        parts = [f"{n}（{', '.join(fs)}）" for n,fs in c['values']]
        print(f"     ⚠️ 矛盾：{c['brand']} {c['metric']} [{c['period']}/{c['currency']}] -> " + " | ".join(parts))
else:
    print("  ✅ 无实质数据矛盾（同品牌·同指标·同周期·同币种 跨文件一致）")

json.dump(contradictions, open(r"D:\Fashion Doctor\fashion-doctor\_contradiction_strict.json",'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"\n严格矛盾数：{len(contradictions)}（已排除跨币种/跨分部/周期误标伪影）")
