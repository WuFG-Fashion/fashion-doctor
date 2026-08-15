#!/usr/bin/env python3
"""修复 [[target\|alias]] 反斜杠转义导致的断链（全库统一为 [[target|alias]] 惯例）。"""
import re
from pathlib import Path

WIKI = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki")
PAT = re.compile(r'\[\[([^\]\n]*?)\\\|([^\]\n]*?)\]\]')

total = 0
for f in sorted(WIKI.rglob("*.md")):
    t = f.read_text(encoding='utf-8')
    hits = PAT.findall(t)
    if not hits:
        continue
    new = PAT.sub(r'[[\1|\2]]', t)
    f.write_text(new, encoding='utf-8')
    rel = str(f.relative_to(WIKI)).replace('\\', '/')
    for a, b in hits:
        print(f"  FIX {rel}: [[{a}\\|{b}]] -> [[{a}|{b}]]")
    total += len(hits)

print(f"\n共修复 {total} 处反斜杠转义断链")
