#!/usr/bin/env python3
"""Update kb_benchmarks.json — scan wiki/concepts/ and wiki/entities/ for new threshold/benchmark data"""
import os
import json, re
from pathlib import Path
from datetime import date

_KB = Path(os.environ.get("KB_ROOT") or Path(__file__).resolve().parents[1] / "knowledge_base")  # KB 根：KB_ROOT 环境变量优先，默认按脚本位置推导
WIKI = _KB / "wiki"
BENCH_PATH = _KB / "kb_benchmarks.json"

with open(BENCH_PATH, 'r', encoding='utf-8') as f:
    b = json.load(f)

# Update timestamp
b['updated'] = str(date.today())
b['meta']['last_scan'] = str(date.today())

# Count files scanned
entities = list((WIKI / 'entities').glob('*.md'))
concepts = list((WIKI / 'concepts').glob('*.md'))
b['meta']['files_scanned'] = f"{len(entities)} 个 wiki/entities 文件 + {len(concepts)} 个 wiki/concepts 文件"

# Check for new brands not in benchmarks
existing_brands = set(b['competitors'].keys())
for ef in entities:
    brand_key = ef.stem
    if brand_key not in existing_brands and brand_key not in ('丽晶', '探马SCRM', '深维智信'):
        # Extract key metrics
        text = ef.read_text(encoding='utf-8')
        data = {}
        gm = re.search(r'(?:毛利率|毛利|gross.margin)[^\d]*?([\d.]+)\s*%', text)
        nm = re.search(r'(?:净利率|net.margin)[^\d]*?([\d.]+)\s*%', text)
        rev = re.search(r'(?:营收|收入|revenue)[^\d]*?([\d.]+)\s*亿', text)
        np = re.search(r'(?:净利|净利润|net.profit)[^\d]*?([\d.]+)\s*亿', text)
        rg = re.search(r'(?:营收.*?(?:增长|增速|growth)[^\d]*?)([\d.-]+)\s*%', text)
        pg = re.search(r'(?:净利|利润).*?(?:增长|增速|growth)[^\d]*?([\d.-]+)\s*%', text)
        
        if gm: data['gross_margin'] = float(gm.group(1))
        if nm: data['net_margin'] = float(nm.group(1))
        if rev: data['revenue_billion'] = float(rev.group(1))
        if np: data['net_profit_billion'] = float(np.group(1))
        if rg: data['revenue_growth'] = float(rg.group(1))
        if pg: data['profit_growth'] = float(pg.group(1))
        
        if data:
            b['competitors'][brand_key] = data
            print(f"  新增品牌: {brand_key} → {data}")

# Check for new concepts with thresholds
concept_thresholds = {
    'ai_fashion_consumer_2026': 'ai_fashion_consumer_2026',
    'guide_training_camp': 'guide_training_camp',
}

# Update data_points count
total = sum(len(v) if isinstance(v, dict) else 1 for v in b.values() if v != b['meta'] and v != b['updated'])
b['meta']['data_points'] = f"{total}+条数值"

with open(BENCH_PATH, 'w', encoding='utf-8') as f:
    json.dump(b, f, ensure_ascii=False, indent=2)

print(f"✅ kb_benchmarks.json 已更新 → {date.today()}")
print(f"   扫描: {b['meta']['files_scanned']}")
print(f"   数据点: {b['meta']['data_points']}")
