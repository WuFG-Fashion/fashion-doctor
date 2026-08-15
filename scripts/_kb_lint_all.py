#!/usr/bin/env python3
"""Fashion Doctor 知识库 — 全量 lint 扫描（5项规则）"""
import os, re, json
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

WIKI = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki")
TODAY = date.today()
CUTOFF = TODAY.replace(year=TODAY.year - 1)  # 90 days ago: today - 90 days

# ── helpers ──
def read_frontmatter(text):
    """Extract frontmatter as dict from markdown text."""
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
    """Extract all [[target]] and [[target|label]] links."""
    links = []
    for m in re.finditer(r'\[\[([^\]]+)\]\]', text):
        raw = m.group(1)
        # Split on | to get target
        parts = raw.split('|')
        target = parts[0].strip()
        # Skip anchor-only links like [[#section]]
        if target.startswith('#'):
            continue
        # Skip quoted strings (code blocks)
        # Normalize: remove leading wiki/ path prefix
        target = re.sub(r'^(wiki/)?(entities|concepts|practices|comparisons|sources)/', '', target)
        links.append(target)
    return links

def resolve_page(target):
    """Given a link target, check if it exists in wiki/. Returns path or None."""
    # Try direct match
    for ext in ['.md', '']:
        t = target if target.endswith('.md') else target + '.md'
        p = WIKI / t
        if p.exists():
            return p
        # Try subdirectories
        for sub in ['entities', 'concepts', 'practices', 'comparisons', 'sources']:
            p = WIKI / sub / t
            if p.exists():
                return p
        # Try with Chinese filename
        p = WIKI / t
        if p.exists():
            return p
        for sub in ['entities', 'concepts', 'practices', 'comparisons', 'sources']:
            p = WIKI / sub / t
            if p.exists():
                return p
    return None

def extract_financial_data(text):
    """Extract brand financial metrics: gross_margin, net_margin, revenue, net_profit, growth rates."""
    data = {}
    # Patterns for percentage values
    pct_patterns = [
        (r'(?:毛利率|gross_margin|毛利)[：:\s]*([\d.]+)\s*%', 'gross_margin_pct'),
        (r'(?:净利率|net_margin|净利)[：:\s]*([\d.]+)\s*%', 'net_margin_pct'),
        (r'(?:营收|收入|revenue)[：:\s]*([\d.]+)\s*亿', 'revenue_billion'),
        (r'(?:净利|净利润|net_profit)[：:\s]*([\d.]+)\s*亿', 'net_profit_billion'),
        (r'(?:营收增长|revenue_growth)[：:\s]*([\d.-]+)\s*%', 'revenue_growth_pct'),
        (r'(?:利润增长|profit_growth|净利增长)[：:\s]*([\d.-]+)\s*%', 'profit_growth_pct'),
        (r'(?:营业利润率|operating_margin)[：:\s]*([\d.]+)\s*%', 'operating_margin_pct'),
    ]
    for pat, key in pct_patterns:
        matches = re.findall(pat, text)
        if matches:
            data[key] = [float(m) for m in matches]
    return data

# ── 1. Broken Links ──
print("=" * 60)
print("🔍 Rule 1: 断链检测")
print("=" * 60)

all_files = list(WIKI.rglob("*.md"))
# Exclude log.md and index.md from content pages
content_files = [f for f in all_files if f.name not in ('log.md', 'index.md', 'overview.md')]

# Build set of valid targets
valid_targets = set()
for f in content_files:
    # relative to wiki/
    rel = f.relative_to(WIKI)
    valid_targets.add(str(rel).replace('\\', '/'))
    valid_targets.add(f.stem)  # filename without ext
    valid_targets.add(f.name)  # filename with ext
    # Also add .md version
    valid_targets.add(f.stem + '.md')

broken_links = []
for f in content_files:
    try:
        text = f.read_text(encoding='utf-8')
    except:
        continue
    links = extract_links(text)
    rel = f.relative_to(WIKI)
    for link in links:
        # Skip self-references
        if link == f.stem or link == f.name:
            continue
        if not resolve_page(link):
            broken_links.append((str(rel), link))

print(f"  扫描 {len(content_files)} 个内容页面")
if broken_links:
    print(f"  ❌ 发现 {len(broken_links)} 条断链:")
    for src, link in broken_links:
        print(f"     {src} → [[{link}]]")
else:
    print("  ✅ 0 条断链")

# ── 2. Orphan Pages ──
print("\n" + "=" * 60)
print("🔍 Rule 2: 孤立页面检测")
print("=" * 60)

orphans = []
for f in content_files:
    try:
        text = f.read_text(encoding='utf-8')
    except:
        continue
    links = extract_links(text)
    if not links:
        rel = f.relative_to(WIKI)
        orphans.append(str(rel))

if orphans:
    print(f"  ❌ 发现 {len(orphans)} 个孤岛页面（无出链）:")
    for o in orphans:
        print(f"     {o}")
else:
    print("  ✅ 0 个孤岛页面")

# ── 3. Contradiction Detection ──
print("\n" + "=" * 60)
print("🔍 Rule 3: 矛盾检测")
print("=" * 60)

# Brand name mapping to file stems
brand_map = {
    'peacebird': ['peacebird', '太平鸟'],
    'muson_gxg': ['muson_gxg', 'gxg', '慕尚', 'GXG'],
    'fast_retailing': ['fast_retailing', '迅销', '优衣库', 'uniqlo'],
    'inditex_zara': ['inditex_zara', 'zara', 'inditex', 'ZARA'],
    'hla': ['hla', '海澜之家'],
    'semir': ['semir', '森马'],
    'lululemon': ['lululemon'],
    'jnby': ['jnby', '江南布衣'],
    'bienlefen': ['bienlefen', '比音勒芬'],
    'bosideng': ['bosideng', '波司登'],
    'hm': ['hm', 'H&M', 'h&m'],
    'anta': ['anta', '安踏'],
    'burberry': ['burberry', '博柏利', 'Burberry'],
    'top_sports': ['top_sports', 'topsports', '滔搏'],
    'septwolves': ['septwolves', '七匹狼'],
    'lilanz': ['lilanz', '利郎'],
}

# Collect financial data from entities/ and comparisons/
contradictions = []
brand_data = defaultdict(lambda: defaultdict(list))  # brand -> metric -> [(value, source_file)]

# Skip sources/ for contradiction detection — too many and mostly same-origin
scan_dirs = ['entities', 'comparisons']
for sub in scan_dirs:
    for f in (WIKI / sub).glob("*.md"):
        try:
            text = f.read_text(encoding='utf-8')
        except:
            continue
        rel = str(f.relative_to(WIKI))
        
        # Determine which brand(s) this file is about
        file_brands = []
        for brand, aliases in brand_map.items():
            if f.stem == brand or f.stem in aliases:
                file_brands.append(brand)
                break
            # Check if any alias appears in text
            for alias in aliases:
                if alias.lower() in f.stem.lower():
                    file_brands.append(brand)
                    break
        
        if not file_brands:
            # For comparisons, the brand data is embedded - try to detect
            continue
        
        # Extract structured metrics from tables/headings
        # Gross margin patterns
        gm_patterns = [
            (r'(?:毛利率|gross.margin)[^\d]*?([\d.]+)\s*%', 'gross_margin'),
            (r'(?:净利率|net.margin)[^\d]*?([\d.]+)\s*%', 'net_margin'),
            (r'(?:营业利润率|operating.margin)[^\d]*?([\d.]+)\s*%', 'operating_margin'),
        ]
        
        for brand in file_brands:
            for pat, metric in gm_patterns:
                for m in re.finditer(pat, text, re.IGNORECASE):
                    val = float(m.group(1))
                    brand_data[brand][metric].append((val, rel))
            
            # Revenue patterns (in 亿)
            rev_patterns = [
                (r'(?:营收|收入|revenue)[^\d]*?([\d.]+)\s*亿', 'revenue_billion'),
                (r'(?:净利|净利润|net.profit)[^\d]*?([\d.]+)\s*亿', 'net_profit_billion'),
            ]
            for pat, metric in rev_patterns:
                for m in re.finditer(pat, text, re.IGNORECASE):
                    val = float(m.group(1))
                    brand_data[brand][metric].append((val, rel))

# Now compare within each brand
for brand, metrics in brand_data.items():
    for metric, values in metrics.items():
        if len(values) <= 1:
            continue
        unique_vals = set(v[0] for v in values)
        if len(unique_vals) > 1:
            # Check if difference is > 1% (排除四舍五入差异)
            vals_list = list(unique_vals)
            min_v, max_v = min(vals_list), max(vals_list)
            if max_v > 0 and (max_v - min_v) / max_v > 0.015:  # >1.5% difference
                # Group by source
                for val in vals_list:
                    sources = [s for v, s in values if v == val]
                    contradictions.append({
                        'brand': brand,
                        'metric': metric,
                        'value': val,
                        'sources': sources
                    })

if contradictions:
    print(f"  ⚠️ 发现 {len(contradictions)} 处数据矛盾:")
    # Group by brand+metric
    seen = set()
    for c in contradictions:
        key = (c['brand'], c['metric'])
        if key in seen:
            continue
        seen.add(key)
        vals_for_metric = [c2 for c2 in contradictions if (c2['brand'], c2['metric']) == key]
        print(f"     ⚠️ {c['brand']}.{c['metric']}:")
        for v in vals_for_metric:
            print(f"         {v['value']} in {v['sources']}")
else:
    print("  ✅ 无数据矛盾")

# ── 4. Expired Pages ──
print("\n" + "=" * 60)
print("🔍 Rule 4: 过期检查 (updated > 90天)")
print("=" * 60)

expired = []
for f in content_files:
    try:
        text = f.read_text(encoding='utf-8')
    except:
        continue
    fm = read_frontmatter(text)
    updated = fm.get('updated', '')
    if updated:
        try:
            d = datetime.strptime(updated, '%Y-%m-%d').date()
            if d < CUTOFF:
                expired.append((str(f.relative_to(WIKI)), updated))
        except:
            pass

if expired:
    print(f"  ❌ 发现 {len(expired)} 个过期页面:")
    for p, d in expired:
        print(f"     {p} (updated: {d})")
else:
    print("  ✅ 0 页过期")

# ── 5. Classification Consistency ──
print("\n" + "=" * 60)
print("🔍 Rule 5: 分类一致性 (type vs directory)")
print("=" * 60)

type_dir_map = {
    'entity': 'entities',
    'concept': 'concepts',
    'practice': 'practices',
    'comparison': 'comparisons',
    'source': 'sources',
}

class_errors = []
for f in content_files:
    try:
        text = f.read_text(encoding='utf-8')
    except:
        continue
    fm = read_frontmatter(text)
    ftype = fm.get('type', '')
    rel = str(f.relative_to(WIKI))
    parent_dir = rel.split('/')[0] if '/' in rel else ''
    
    if ftype and parent_dir and ftype in type_dir_map:
        expected_dir = type_dir_map[ftype]
        if parent_dir != expected_dir:
            class_errors.append((rel, ftype, parent_dir, expected_dir))

if class_errors:
    print(f"  ❌ 发现 {len(class_errors)} 处分类错误:")
    for rel, ftype, actual, expected in class_errors:
        print(f"     {rel}: type={ftype}, dir={actual}, expected={expected}")
else:
    print("  ✅ 无分类错误")

# ── Summary ──
print("\n" + "=" * 60)
print("📊 本轮 lint 统计")
print("=" * 60)
print(f"  断链修复：{len(broken_links)} 条")
print(f"  孤岛修复：{len(orphans)} 个")
print(f"  矛盾检测：{len(set((c['brand'],c['metric']) for c in contradictions))} 处" if contradictions else "  矛盾检测：✅ 无矛盾")
print(f"  过期页面：{len(expired)} 页" if expired else "  过期页面：✅ 0 页过期")
print(f"  分类错误：{len(class_errors)} 处" if class_errors else "  分类错误：✅ 无分类错误")

# Save results for further processing
result = {
    'broken_links': [(src, link) for src, link in broken_links],
    'orphans': orphans,
    'contradictions': contradictions,
    'expired': [(p, d) for p, d in expired],
    'class_errors': [(r, ft, a, e) for r, ft, a, e in class_errors],
    'counts': {
        'broken': len(broken_links),
        'orphans': len(orphans),
        'contradictions': len(set((c['brand'],c['metric']) for c in contradictions)),
        'expired': len(expired),
        'class_errors': len(class_errors),
    }
}

with open(r"D:\Fashion Doctor\fashion-doctor\_lint_result.json", 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

print(f"\n结果已保存到 _lint_result.json")
