#!/usr/bin/env python3
"""Fix detected broken [[wikilinks]] in the wiki.
Real fixes only; code-block / anchor false positives are preserved."""
from pathlib import Path

WIKI = Path(r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki")

# (file_path_relative_to_wiki, old_string, new_string)
FIXES = [
    # 1. apparel_ai_agents_2026.md: source slug -> real source filename (cross_refs + sources line)
    (r"concepts\apparel_ai_agents_2026.md",
     "2026-07-26_style3d_blog_agentic_ai_fashion_standard.md",
     "2026-07-26_Style3D_Blog_AgenticAI时尚科技行业标准.md"),
    (r"concepts\apparel_ai_agents_2026.md",
     "2026-07-26_vistoya_fashion_ai_agents_cases.md",
     "2026-07-26_Vistoya_2026时尚品牌AI_Agent实战.md"),
    (r"concepts\apparel_ai_agents_2026.md",
     "[[2026-07-26_style3d_blog_agentic_ai_fashion_standard]]",
     "[[2026-07-26_Style3D_Blog_AgenticAI时尚科技行业标准]]"),
    (r"concepts\apparel_ai_agents_2026.md",
     "[[2026-07-26_vistoya_fashion_ai_agents_cases]]",
     "[[2026-07-26_Vistoya_2026时尚品牌AI_Agent实战]]"),
    # 2. source files: 服装SKU精细化管理 -> sku_fine_management (alias preserved)
    (r"sources\2026-07-24_户外品牌_商品组合计划挑战.md",
     "[[服装SKU精细化管理]]", "[[sku_fine_management|服装SKU精细化管理]]"),
    (r"sources\2026-07-24_第七在线_商品计划终极指南.md",
     "[[服装SKU精细化管理]]", "[[sku_fine_management|服装SKU精细化管理]]"),
]

done = 0
for rel, old, new in FIXES:
    p = WIKI / rel
    if not p.exists():
        print(f"SKIP (missing file): {rel}")
        continue
    text = p.read_text(encoding="utf-8")
    if old not in text:
        print(f"SKIP (not found): {rel}  <<{old}>>")
        continue
    cnt = text.count(old)
    text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")
    done += cnt
    print(f"FIX ({cnt}x): {rel}  {old} -> {new}")

print(f"\nTotal replacements applied: {done}")
