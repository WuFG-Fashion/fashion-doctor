#!/usr/bin/env python3
"""Fashion Doctor 知识库 — 每日优化 lint 5项规则完整检测（精确版）。
关键修复：矛盾检测采用「品牌就近窗口归因」，避免整文件关联导致的跨品牌污染。
检测项：1)断链 2)孤岛 3)矛盾(跨 entity/comparison/source 同品牌同指标同周期)
       4)过期 5)分类一致性。结果存 _lint_result.json 并打印报告。
"""
import re, json
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict

WIKI = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki")
TODAY = date.today()
CUTOFF = TODAY - timedelta(days=90)

# ── 基础工具 ──
def strip_code(text):
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]*`', '', text)
    return text

def read_frontmatter(text):
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    return fm

def extract_links(text):
    text = strip_code(text)
    links = []
    for m in re.finditer(r'\[\[([^\]]+)\]\]', text):
        raw = m.group(1)
        target = raw.split('|')[0].strip()
        if not target or target.startswith('#'):
            continue
        target = re.sub(r'^(wiki/)?(entities|concepts|practices|comparisons|sources)/', '', target)
        links.append(target)
    return links

def resolve_page(target):
    # 支持 [[page#anchor]] 形式：锚点链接只要 page 存在即为有效
    base = target.split('#')[0].strip()
    if not base:
        return None
    # 去除可能带的前缀（wiki/ 或 knowledge_base/）
    base = re.sub(r'^(wiki/|knowledge_base/)', '', base)
    t = base if base.endswith('.md') else base + '.md'
    # 1) vault 根（knowledge_base/ 本身，如 CLAUDE.md）
    KB_ROOT = WIKI.parent
    cands = [WIKI / t, WIKI / base, KB_ROOT / t, KB_ROOT / base]
    for sub in ['entities', 'concepts', 'practices', 'comparisons', 'sources', 'playbooks']:
        cands.append(WIKI / sub / t)
        cands.append(WIKI / sub / base)
    for c in cands:
        if c.exists():
            return c
    return None

all_files = list(WIKI.rglob("*.md"))
content_files = [f for f in all_files if f.name not in ('log.md', 'index.md', 'overview.md')]

# ── 1. 断链 ──
print("=" * 64)
print("🔍 规则1：断链检测")
print("=" * 64)
broken = []
for f in content_files:
    text = f.read_text(encoding='utf-8')
    links = extract_links(text)
    rel = str(f.relative_to(WIKI)).replace('\\', '/')
    for link in links:
        if link == f.stem or link == f.name:
            continue
        if not resolve_page(link):
            broken.append((rel, link))
seen = set(); uniq_broken = []
for b in broken:
    if b not in seen:
        seen.add(b); uniq_broken.append(b)
print(f"  扫描 {len(content_files)} 个内容页面，发现 {len(uniq_broken)} 条唯一断链：")
for src, link in uniq_broken:
    print(f"     {src}  →  [[{link}]]")

# ── 2. 孤岛 ──
print("\n" + "=" * 64)
print("🔍 规则2：孤立页面检测（无出链）")
print("=" * 64)
orphans = []
for f in content_files:
    text = f.read_text(encoding='utf-8')
    if not extract_links(text):
        orphans.append(str(f.relative_to(WIKI)).replace('\\', '/'))
print(f"  发现 {len(orphans)} 个孤岛页面：")
for o in orphans:
    print(f"     {o}")

# ── 3. 矛盾检测（品牌就近窗口归因）──
print("\n" + "=" * 64)
print("🔍 规则3：矛盾检测（同品牌·同指标·同周期·跨文件）")
print("=" * 64)

brand_map = {
    'peacebird': ['peacebird', '太平鸟', '太平鸟男装'],
    'muson_gxg': ['muson_gxg', 'gxg', '慕尚', 'GXG'],
    'fast_retailing': ['fast_retailing', '迅销', '优衣库', 'uniqlo', 'UNIQLO'],
    'inditex_zara': ['inditex_zara', 'zara', 'inditex', 'ZARA', 'Zara'],
    'hla': ['hla', '海澜之家', '海澜'],
    'semir': ['semir', '森马', '森马服饰'],
    'lululemon': ['lululemon', 'Lululemon'],
    'jnby': ['jnby', '江南布衣', 'JNBY'],
    'bienlefen': ['bienlefen', '比音勒芬'],
    'bosideng': ['bosideng', '波司登'],
    'hm': ['hm', 'H&M', 'h&m', 'H & M'],
    'anta': ['anta', '安踏'],
    'burberry': ['burberry', '博柏利', 'Burberry'],
    'top_sports': ['top_sports', 'topsports', '滔搏'],
    'septwolves': ['septwolves', '七匹狼'],
    'lilanz': ['lilanz', '利郎'],
    'baoxiniao': ['baoxiniao', '报喜鸟'],
    'langzi_fashion': ['langzi_fashion', '朗姿', '朗姿股份'],
    'jiumuwang': ['jiumuwang', '九牧王'],
    'anzheng_fashion': ['anzheng_fashion', '安正时尚'],
    'suhao_fashion': ['suhao_fashion', '苏豪', '苏豪时尚'],
}

METRICS = [
    (r'(?:毛利率|毛利)[^\d%]{0,30}?([\d.]+)\s*%', 'gross_margin', True),
    (r'(?:净利率|净利益)[^\d%]{0,30}?([\d.]+)\s*%', 'net_margin', True),
    (r'(?:营业利润率|operating.margin)[^\d%]{0,30}?([\d.]+)\s*%', 'operating_margin', True),
    (r'(?:营收|收入|revenue)[^\d%]{0,30}?([\d.]+)\s*亿', 'revenue', False),
    (r'(?:净利|净利润|net.profit)[^\d%]{0,30}?([\d.]+)\s*亿', 'net_profit', False),
    (r'(?:营收[^%\n]{0,40}?增长|revenue.growth)[^\d%]{0,30}?([\d.-]+)\s*%', 'revenue_growth', True),
    (r'(?:净利[^%\n]{0,40}?增长|利润[^%\n]{0,40}?增长|profit.growth)[^\d%]{0,30}?([\d.-]+)\s*%', 'profit_growth', True),
]
PERIOD_PAT = re.compile(r'(FY\s?2024|FY\s?2025|FY\s?2026|2024\s*全年|2025\s*全年|2026\s*全年|2026Q1|2026Q2|2025Q1|Q1|Q2|Q3|H1|9\s*个月|九个月|半年|全年|年度|2026\s*上半年|上半年)', re.IGNORECASE)

def detect_period(snippet):
    m = PERIOD_PAT.search(snippet)
    return m.group(1).strip().upper() if m else 'UNKNOWN'

def sentence_extract(text, brand_aliases):
    """按句子归属：仅当某句同时含品牌别名与指标时，才把该值归属该品牌+该句周期。
    句级归属可消除多品牌汇总表的跨品牌串味，且周期随句内上下文精确判定。"""
    out = defaultdict(list)
    for sent in re.split(r'(?<=[。！？\n])', text):
        low = sent.lower()
        if not any(al.lower() in low for al in brand_aliases):
            continue
        per = detect_period(sent)
        for pat, metric, is_pct in METRICS:
            for m in re.finditer(pat, sent, re.IGNORECASE):
                try:
                    val = float(m.group(1))
                except:
                    continue
                out[metric].append((val, per))
    return out

def period_from_filename(name):
    n = name.lower()
    if '2026q1' in n or '2026_q1' in n: return '2026Q1'
    if '2026q2' in n: return '2026Q2'
    if 'mid2026' in n or 'mid_2026' in n: return 'H1'
    if '2025q1' in n: return '2025Q1'
    if '2025' in n: return 'FY2025'
    if '2026' in n: return 'FY2026'
    return 'UNKNOWN'

# 收集：brand -> metric -> period -> [(value, file)]
data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

# 1) 实体页：按句子归属该单一品牌（句内上下文精确判定周期）
for brand, aliases in brand_map.items():
    epath = WIKI / 'entities' / f'{brand}.md'
    if epath.exists():
        text = epath.read_text(encoding='utf-8')
        res = sentence_extract(text, aliases)
        for metric, vals in res.items():
            for val, per in vals:
                data[brand][metric][per].append((val, 'entities/' + brand + '.md'))

# 2) 对比页：按「品牌名所在行」逐行归属（多品牌汇总表不串味）
for f in (WIKI / 'comparisons').glob('*.md'):
    text = f.read_text(encoding='utf-8')
    rel = str(f.relative_to(WIKI)).replace('\\', '/')
    fper = period_from_filename(f.name)
    for line in text.split('\n'):
        for brand, aliases in brand_map.items():
            if any(al.lower() in line.lower() for al in aliases):
                for pat, metric, is_pct in METRICS:
                    for m in re.finditer(pat, line, re.IGNORECASE):
                        try:
                            val = float(m.group(1))
                        except:
                            continue
                        data[brand][metric][fper].append((val, rel))
                break  # 一行只归属首个匹配品牌

# 3) 来源页：仅取「文件名含该品牌别名」的单品牌专稿，按句归属（排除汇总表串味）
for f in (WIKI / 'sources').glob('*.md'):
    rel = str(f.relative_to(WIKI)).replace('\\', '/')
    text = f.read_text(encoding='utf-8')
    for brand, aliases in brand_map.items():
        if any(al.lower() in f.name.lower() for al in aliases):
            res = sentence_extract(text, aliases)
            for metric, vals in res.items():
                for val, per in vals:
                    data[brand][metric][per].append((val, rel))

contradictions = []
for brand, metric_map in data.items():
    for metric, period_map in metric_map.items():
        for period, vals in period_map.items():
            if len(vals) < 2:
                continue
            files = set(v[1] for v in vals)
            if len(files) < 2:
                continue
            uniq = {}
            for v in vals:
                uniq.setdefault(round(v[0], 4), []).append(v[1])
            if len(uniq) < 2:
                continue
            nums = list(uniq.keys())
            lo, hi = min(nums), max(nums)
            denom = max(abs(hi), 0.01)
            if (hi - lo) / denom > 0.02:
                detail = [(num, sorted(set(fs))) for num, fs in uniq.items()]
                contradictions.append({'brand': brand, 'metric': metric, 'period': period, 'values': detail})

if contradictions:
    print(f"  ⚠️ 发现 {len(contradictions)} 处数据矛盾：")
    for c in contradictions:
        parts = [f"{num}（{', '.join(fs)}）" for num, fs in c['values']]
        print(f"     ⚠️ 矛盾：{c['brand']} {c['metric']} [{c['period']}] -> " + " | ".join(parts))
else:
    print("  ✅ 无数据矛盾")

# ── 4. 过期 ──
print("\n" + "=" * 64)
print(f"🔍 规则4：过期检查（updated > 90天，基准日 {TODAY}）")
print("=" * 64)
expired = []
for f in content_files:
    fm = read_frontmatter(f.read_text(encoding='utf-8'))
    updated = fm.get('updated', '')
    if not updated:
        continue
    try:
        if datetime.strptime(updated, '%Y-%m-%d').date() < CUTOFF:
            expired.append((str(f.relative_to(WIKI)).replace('\\', '/'), updated))
    except:
        pass
if expired:
    print(f"  ❌ 发现 {len(expired)} 个过期页面：")
    for p, d in expired:
        print(f"     {p} (updated: {d})")
else:
    print("  ✅ 0 页过期")

# ── 5. 分类一致性 ──
print("\n" + "=" * 64)
print("🔍 规则5：分类一致性（type vs 目录）")
print("=" * 64)
type_dir_map = {'entity': 'entities', 'concept': 'concepts', 'practice': 'practices',
                'comparison': 'comparisons', 'source': 'sources'}
class_errors = []
for f in content_files:
    fm = read_frontmatter(f.read_text(encoding='utf-8'))
    ftype = fm.get('type', '')
    rel = str(f.relative_to(WIKI)).replace('\\', '/')
    parent_dir = rel.split('/')[0] if '/' in rel else ''
    if ftype and parent_dir and ftype in type_dir_map and parent_dir != type_dir_map[ftype]:
        class_errors.append((rel, ftype, parent_dir, type_dir_map[ftype]))
if class_errors:
    print(f"  ❌ 发现 {len(class_errors)} 处分类错误：")
    for rel, ft, act, exp in class_errors:
        print(f"     {rel}: type={ft}, dir={act}, expected={exp}")
else:
    print("  ✅ 无分类错误")

# ── 汇总 ──
print("\n" + "=" * 64)
print("📊 本轮 lint 统计")
print("=" * 64)
print(f"  断链：{len(uniq_broken)} 条")
print(f"  孤岛：{len(orphans)} 个")
print(f"  矛盾：{len(contradictions)} 处（或 ✅ 无矛盾）" if contradictions else "  矛盾：✅ 无矛盾")
print(f"  过期：{len(expired)} 页（或 ✅ 0 页过期）" if expired else "  过期：✅ 0 页过期")
print(f"  分类错误：{len(class_errors)} 处（或 ✅ 无分类错误）" if class_errors else "  分类错误：✅ 无分类错误")

result = {
    'date': str(TODAY),
    'broken': uniq_broken,
    'orphans': orphans,
    'contradictions': contradictions,
    'expired': expired,
    'class_errors': class_errors,
    'counts': {'broken': len(uniq_broken), 'orphans': len(orphans),
               'contradictions': len(contradictions), 'expired': len(expired),
               'class_errors': len(class_errors)},
}
with open(r"D:\Fashion Doctor\fashion-doctor\_lint_result.json", 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"\n结果已保存到 _lint_result.json")
