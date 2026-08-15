#!/usr/bin/env python3
"""Fix genuine broken wikilinks found by kb_lint_5rules.py (run 2026-08-14).
Genuine broken set (after excluding playbook-target false positives + valid
vault-relative [[CLAUDE.md]]):
  1) 6 malformed triple-bracket merges  [[A, [[B]]  ->  [[A]], [[B]]
  2) 2 misnamed source targets (extra 半年 / _ vs - in date)
  3) 5 template/meta refs to non-existent pages (Home/human/MOC_L04)
Playbook-target links (导购培训SOP/清仓决策树/季初订货节奏) are VALID -> untouched.
"""
import re
from pathlib import Path

WIKI = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki")
PY = lambda p: WIKI / p

def patch(rel, repls):
    f = PY(rel)
    t = f.read_text(encoding='utf-8')
    orig = t
    for old, new in repls:
        if old not in t:
            print(f"  ⚠️  PATTERN NOT FOUND in {rel}: {old[:40]!r}")
            continue
        t = t.replace(old, new)
    if t != orig:
        f.write_text(t, encoding='utf-8')
        print(f"  ✅ fixed {rel}")
    else:
        print(f"  ·  no change {rel}")

# ── 1) malformed triple-bracket: [[A, [[B]] -> [[A]], [[B]] ──
MALFORMED = [
    "entities/深维智信.md",
    "concepts/AI导购陪练.md",
    "concepts/柔性供应链与商品企划.md",
    "concepts/动态OTB管理.md",
    "concepts/全渠道会员一体化.md",
    "concepts/会员复购率提升策略.md",
]
print("== 1) 修复 6 处 [[]] 三重括号合并 ==")
for rel in MALFORMED:
    f = PY(rel)
    t = f.read_text(encoding='utf-8')
    orig = t
    # [[NAME, [[  ->  [[NAME]], [[
    t2 = re.sub(r'\[\[([^\]]+?),\s*\[\[', r'[[\1]], [[', t)
    if t2 != orig:
        f.write_text(t2, encoding='utf-8')
        print(f"  ✅ fixed {rel}")
    else:
        print(f"  ⚠️  no malformed pattern in {rel}")

# ── 2) misnamed source targets ──
print("== 2) 修复 2 处误名目标 ==")
patch("entities/fast_retailing.md", [
    ("[[2026-08-12_迅销优衣库2026H1半年业绩_中国门店989家]]",
     "[[2026-08-12_迅销优衣库2026H1业绩_中国门店989家]]"),
])
patch("entities/peacebird.md", [
    ("[[2026_06_19_服装供应链SCM白皮书2026]]",
     "[[2026-06-19_服装供应链SCM白皮书2026]]"),
])

# ── 3) template / meta refs to non-existent pages ──
print("== 3) 修复 5 处模板/元引用（指向不存在页面）==")
# 决策日志_模板.md : Home x2, human x2 -> plain text (preserve words, drop broken link)
patch("playbooks/决策日志_模板.md", [
    ("[[Home]]", "Home"),
    ("[[human]]", "human"),
])
# _template.md : Home -> plain text (CLAUDE.md is a valid vault-relative link, keep)
patch("playbooks/_template.md", [
    ("[[Home]]", "Home"),
])
# 导购培训SOP.md : MOC_L04_导购能力评估 has no target page -> plain text
patch("playbooks/导购培训SOP.md", [
    ("[[MOC_L04_导购能力评估]]", "MOC_L04_导购能力评估"),
])

print("\nDONE.")
