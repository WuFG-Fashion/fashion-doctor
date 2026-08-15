#!/usr/bin/env python3
"""受控更新 kb_benchmarks.json —— 仅新增、绝不覆盖既有键。
1) 刷新 updated / meta.last_scan / meta.files_scanned / meta.data_points
2) 仅向 competitors 追加「知识库中已存在、但 benchmarks 缺失」的真实竞品品牌实体
   工具/厂商类实体（style3d_lingdi/丽晶/探马SCRM/深维智信）排除
3) 新品牌指标用谨慎正则从实体页提取，dry-run 先打印待写入值供核验
"""
import json, re, sys
from pathlib import Path
from datetime import date

KB = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base")
WIKI = KB / "wiki"
BENCH = KB / "kb_benchmarks.json"

EXISTING = set(json.load(open(BENCH, encoding='utf-8'))['competitors'].keys())
# 实体目录中真实竞品品牌（排除工具/厂商）
NEW_BRANDS = ['anta', 'anzheng_fashion', 'jiumuwang', 'suhao_fashion', '安奈儿']
VENDOR_SKIP = {'style3d_lingdi', '丽晶', '探马SCRM', '深维智信'}

def extract(text):
    d = {}
    m = re.search(r'(?:毛利率|毛利)[^\d%]{0,20}?([\d.]+)\s*%', text)
    if m: d['gross_margin'] = round(float(m.group(1)) / 100, 4)
    m = re.search(r'(?:净利率|净利益)[^\d%]{0,20}?([\d.]+)\s*%', text)
    if m: d['net_margin'] = round(float(m.group(1)) / 100, 4)
    m = re.search(r'(?:营收|收入|revenue)[^\d%]{0,20}?([\d.]+)\s*亿', text)
    if m: d['revenue_billion'] = float(m.group(1))
    m = re.search(r'(?:净利|净利润|net.profit)[^\d%]{0,20}?([\d.]+)\s*亿', text)
    if m: d['net_profit_billion'] = float(m.group(1))
    m = re.search(r'(?:营收[^%\n]{0,30}?增长|revenue.growth)[^\d%]{0,20}?([\d.-]+)\s*%', text)
    if m: d['revenue_growth'] = float(m.group(1))
    m = re.search(r'(?:净利[^%\n]{0,30}?增长|利润[^%\n]{0,30}?增长|profit.growth)[^\d%]{0,20}?([\d.-]+)\s*%', text)
    if m: d['profit_growth'] = float(m.group(1))
    return d

b = json.load(open(BENCH, encoding='utf-8'))
today = str(date.today())

proposed = {}
for brand in NEW_BRANDS:
    if brand in EXISTING or brand in VENDOR_SKIP:
        continue
    ep = WIKI / 'entities' / f'{brand}.md'
    if not ep.exists():
        continue
    data = extract(ep.read_text(encoding='utf-8'))
    # 受控门槛：仅当实体页含「稳定毛利率 + 营收」时才纳入基准，
    # 排除仅含 H1 预告区间/亏损/无财务字段的早初期实体，避免污染基准
    if data and 'gross_margin' in data and 'revenue_billion' in data:
        proposed[brand] = data

print(f"📅 今日：{today}")
print(f"📂 既有竞品键：{len(EXISTING)} 个")
print(f"➕ 拟新增竞品（受控、不覆盖既有）：")
for k, v in proposed.items():
    print(f"   {k}: {v}")

if '--apply' not in sys.argv:
    print("\n[DRY-RUN] 未写入。加 --apply 真正写入。")
    raise SystemExit

# 写入
b['updated'] = today
b['meta']['last_scan'] = today
ents = list((WIKI / 'entities').glob('*.md'))
concs = list((WIKI / 'concepts').glob('*.md'))
b['meta']['files_scanned'] = f"{len(ents)} 个 wiki/entities 文件 + {len(concs)} 个 wiki/concepts 文件"
for k, v in proposed.items():
    b['competitors'][k] = v
# 重新统计数据点
total = sum(len(v) if isinstance(v, dict) else 1 for k, v in b.items() if k not in ('updated', 'meta'))
b['meta']['data_points'] = f"{total}+条数值"

json.dump(b, open(BENCH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"\n✅ kb_benchmarks.json 已更新（受控）→ {today}")
print(f"   竞品数：{len(b['competitors'])}，扫描：{b['meta']['files_scanned']}")
