# -*- coding: utf-8 -*-
"""Round B (L2_03/04/05): corrected frontmatter normalizer.
Restores clean sources/cross_refs arrays with bidirectional links."""
import re, os

WIKI = r"D:\Fashion Doctor\fashion-doctor\knowledge_base\wiki"
TODAY = "2026-08-03"

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

def parse_single_array(line):
    """Parse 'key: [a, b, c]' -> list of item strings. Robust to nested brackets."""
    start = line.index('[')
    end = line.rindex(']')
    body = line[start+1:end]
    return [x.strip().strip('"').strip("'") for x in body.split(',') if x.strip()]

def extract_crossref_tokens(line):
    """Extract [[token]] tokens from a cross_refs line (token may contain |alias)."""
    start = line.index('[')
    end = line.rindex(']')
    body = line[start+1:end]
    toks = re.findall(r'\[\[([^\[\]]+)\]\]', body)
    # fallback: catch malformed single-close [[x]
    toks += re.findall(r'\[\[([^\[\]]+)\]', body)
    # dedupe preserve order
    seen = set(); out = []
    for t in toks:
        if t not in seen:
            seen.add(t); out.append(t)
    return out

def update_file(relpath, new_srcs):
    path = os.path.join(WIKI, relpath)
    with open(path, encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    if not lines or lines[0].strip() != '---':
        print(f"SKIP (no fm): {relpath}"); return
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end = i; break
    if end is None:
        print(f"SKIP (unclosed): {relpath}"); return

    added_src = 0; added_cr = 0
    i = 0
    while i <= end:
        line = lines[i]
        m = re.match(r'^(\s*)sources:\s*\[.*\]\s*$', line)
        if m:
            items = parse_single_array(line)
            for s in new_srcs:
                if s not in items:
                    items.append(s); added_src += 1
            lines[i] = f"sources: [{', '.join(items)}]"
        elif re.match(r'^(\s*)sources:\s*$', line):
            # block list
            j = i + 1
            existing = []
            while j < len(lines) and re.match(r'^\s*-\s+', lines[j]):
                existing.append(lines[j].strip()[2:].strip())
                j += 1
            merged = existing[:]
            for s in new_srcs:
                if s not in merged:
                    merged.append(s); added_src += 1
            lines[i:j] = [line] + [f"  - {s}" for s in merged]
            # recompute end
            for k in range(len(lines)-1, 0, -1):
                if lines[k].strip() == '---':
                    end = k; break
        elif re.match(r'^(\s*)cross_refs:\s*\[.*\]\s*$', line):
            toks = extract_crossref_tokens(line)
            for s in new_srcs:
                t = f"[[{s}]]"
                if t not in toks:
                    toks.append(t); added_cr += 1
            lines[i] = "cross_refs: [" + ", ".join(toks) + "]"
        elif re.match(r'^(\s*)updated:\s*\S+', line):
            lines[i] = re.sub(r'updated:\s*\S+', f'updated: {TODAY}', line)
        i += 1

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"OK {relpath}: +src={added_src} +cr={added_cr}")

for rel, srcs in MAP.items():
    update_file(rel, srcs)
print("DONE")
