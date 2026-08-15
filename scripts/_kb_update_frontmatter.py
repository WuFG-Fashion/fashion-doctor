# -*- coding: utf-8 -*-
"""Round B (L2_03/04/05): register new sources + add bidirectional cross_refs to target pages."""
import re, os

WIKI = r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki"
TODAY = "2026-08-03"

# target file (relative to WIKI) -> list of new source basenames (no .md)
MAP = {
    "concepts/会员复购率提升策略.md": [
        "2026-08-03_数字化转型网_服装私域会员运营四大场景",
        "2026-08-03_微盟见实_七匹狼会员深度运营五年最高增长",
    ],
    "concepts/全渠道会员一体化.md": [
        "2026-08-03_数字化转型网_服装私域会员运营四大场景",
        "2026-08-03_微盟见实_七匹狼会员深度运营五年最高增长",
        "2026-08-03_丽晶_服装门店12核心指标与日周月三层经营节奏",
    ],
    "practices/私域运营方法论.md": [
        "2026-08-03_数字化转型网_服装私域会员运营四大场景",
        "2026-08-03_微盟见实_七匹狼会员深度运营五年最高增长",
    ],
    "concepts/sleeping_member_reactivation.md": [
        "2026-08-03_数字化转型网_服装私域会员运营四大场景",
    ],
    "entities/septwolves.md": [
        "2026-08-03_微盟见实_七匹狼会员深度运营五年最高增长",
    ],
    "entities/深维智信.md": [
        "2026-08-03_Megaview_新人上岗考核可量化导购能力模型",
    ],
    "concepts/AI导购陪练.md": [
        "2026-08-03_Megaview_新人上岗考核可量化导购能力模型",
    ],
    "concepts/导购培训闭环体系.md": [
        "2026-08-03_Megaview_新人上岗考核可量化导购能力模型",
        "2026-08-03_丽晶_服装门店12核心指标与日周月三层经营节奏",
    ],
    "entities/丽晶.md": [
        "2026-08-03_丽晶_服装门店12核心指标与日周月三层经营节奏",
    ],
    "concepts/服装门店经营AI化2026.md": [
        "2026-08-03_丽晶_服装门店12核心指标与日周月三层经营节奏",
    ],
    "concepts/动态OTB管理.md": [
        "2026-08-03_第七在线_商品计划终极指南中国鞋服零售",
        "2026-08-03_第七在线_InfoQ_AI_Agent改变商品计划",
    ],
    "concepts/柔性供应链与商品企划.md": [
        "2026-08-03_第七在线_商品计划终极指南中国鞋服零售",
        "2026-08-03_第七在线_InfoQ_AI_Agent改变商品计划",
    ],
    "concepts/服装企划趋势渠道.md": [
        "2026-08-03_第七在线_商品计划终极指南中国鞋服零售",
        "2026-08-03_第七在线_InfoQ_AI_Agent改变商品计划",
    ],
    "concepts/sku_fine_management.md": [
        "2026-08-03_第七在线_商品计划终极指南中国鞋服零售",
    ],
}

def parse_inline_array(line):
    m = re.match(r'^\s*\S+:\s*\[(.*)\]\s*$', line)
    if not m:
        return None
    body = m.group(1).strip()
    if not body:
        return []
    items = [x.strip().strip('"').strip("'") for x in body.split(',')]
    return [x for x in items if x]

def rebuild_inline_array(items):
    return "[" + ", ".join(items) + "]"

def update_block_list(lines, idx, new_items):
    """Append '- item' lines after a block-list key at lines[idx], until next non-list line."""
    # collect existing block items
    j = idx + 1
    existing = []
    while j < len(lines) and re.match(r'^\s*-\s+', lines[j]):
        existing.append(lines[j].strip()[2:].strip().strip('"').strip("'"))
        j += 1
    merged = existing[:]
    added = []
    for it in new_items:
        if it not in merged:
            merged.append(it)
            added.append(it)
    # rebuild block
    block = [lines[idx]] + [f"  - {it}" for it in merged]
    # replace lines[idx:j] with block
    lines[idx:j] = block
    return added

def update_file(relpath, new_srcs):
    path = os.path.join(WIKI, relpath)
    with open(path, encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    # locate frontmatter
    if not lines or lines[0].strip() != '---':
        print(f"SKIP (no frontmatter): {relpath}")
        return
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end = i
            break
    if end is None:
        print(f"SKIP (unclosed fm): {relpath}")
        return

    added_src = []
    added_cr = []
    # process frontmatter lines
    i = 0
    while i <= end:
        line = lines[i]
        if re.match(r'^\s*sources:\s*\[.*\]\s*$', line):
            items = parse_inline_array(line)
            for s in new_srcs:
                if s not in items:
                    items.append(s); added_src.append(s)
            lines[i] = re.sub(r'\[.*\]', rebuild_inline_array(items), line, count=1)
        elif re.match(r'^\s*sources:\s*$', line):
            added_src = update_block_list(lines, i, new_srcs)
            # updating block changed line indices; recompute end
            # find new end
            for k in range(len(lines)-1, 0, -1):
                if lines[k].strip() == '---':
                    end = k; break
        elif re.match(r'^\s*cross_refs:\s*\[.*\]\s*$', line):
            items = parse_inline_array(line)
            new_cr = [f"[[{s}]]" for s in new_srcs]
            for c in new_cr:
                if c not in items:
                    items.append(c); added_cr.append(c)
            lines[i] = re.sub(r'\[.*\]', rebuild_inline_array(items), line, count=1)
        elif re.match(r'^\s*updated:\s*\S+', line):
            lines[i] = re.sub(r'updated:\s*\S+', f'updated: {TODAY}', line)
        i += 1

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"OK {relpath}: +src={len(added_src)} +cr={len(added_cr)}")

for rel, srcs in MAP.items():
    update_file(rel, srcs)
print("DONE")
