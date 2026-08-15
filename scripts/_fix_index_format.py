#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 index.md 实体表格式：把 cabbeen/moding 移到表头后，去掉破坏表格的空行。"""
from pathlib import Path

INDEX = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki\index.md")
text = INDEX.read_text(encoding="utf-8")

# Split around entities section
start = "### wiki/entities/ — 实体库\n"
end = "### wiki/concepts/ — 概念库\n"
pre, rest = text.split(start, 1)
entities_block, post = rest.split(end, 1)

lines = entities_block.splitlines()
# Collect core rows that were misplaced at the very top
core_rows = []
header_idx = None
for i, line in enumerate(lines):
    if line.startswith("| [[cabbeen]]") or line.startswith("| [[moding_haute_couture|"):
        core_rows.append(line)
    if line.strip() == "| 页面 | 说明 | 标签 |":
        header_idx = i
        break

# Remove those misplaced core rows from their current location
filtered = [l for l in lines if l not in core_rows]

# Now rebuild: keep header + separator, then core_rows, then rest
# Find header/separator again in filtered
rebuilt = []
for i, line in enumerate(filtered):
    rebuilt.append(line)
    if line.strip() == "|------|------|------|":
        # insert core rows right after separator
        rebuilt.extend(core_rows)
        rebuilt.extend(filtered[i+1:])
        break

# Remove blank lines that would break the markdown table (within entities block)
rebuilt = [l for l in rebuilt if l.strip() != ""]

INDEX.write_text(pre + start + "\n".join(rebuilt) + "\n" + end + post, encoding="utf-8")
print("index.md table format fixed")
