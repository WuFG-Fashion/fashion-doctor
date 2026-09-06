"""Round B 2026-09-06 织网：为本轮 6 篇新增 source 的目标页补回链 + 更新 index.md 登记"""
import re
from pathlib import Path

KB = Path("D:/Fashion Doctor/fashion-doctor/knowledge_base")
WIKI = KB / "wiki"

NEW_SOURCES = [
    "sources/2026-09-06_B_会员日活动营销日历与ROI测算.md",
    "sources/2026-09-06_B_会员积分权益体系与忠诚度设计2026.md",
    "sources/2026-09-06_B_星级导购认证与职级晋升体系.md",
    "sources/2026-09-06_B_门店服务质量神秘顾客暗访评估.md",
    "sources/2026-09-06_B_补单追单与快反决策量化模型.md",
    "sources/2026-09-06_B_门店分级店群与分货策略.md",
]

def extract_links(content: str):
    """提取 [[目标]] 或 [[目标|文本]]，返回目标名列表（去重，跳过 raw 引用）"""
    links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)
    out = []
    for l in links:
        l = l.strip()
        if "/" in l:
            continue
        if l not in out:
            out.append(l)
    return out

def add_backlink(target_path: Path, source_stem: str) -> bool:
    t = target_path.read_text(encoding="utf-8")
    if f"[[{source_stem}]]" in t:
        return False
    backlink = f"- [[{source_stem}]]"
    if "## 关联页面" in t or "## 关联知识" in t:
        for marker in ["## 关联页面", "## 关联知识"]:
            if marker in t:
                idx = t.index(marker)
                next_section = t.find("\n## ", idx + len(marker))
                if next_section == -1:
                    next_section = len(t)
                seg = t[idx:next_section]
                if "[[" in seg:
                    t = t[:next_section] + f"\n{backlink}" + t[next_section:]
                else:
                    t = t[:idx + len(marker)] + f"\n{backlink}" + t[idx + len(marker):]
                target_path.write_text(t, encoding="utf-8")
                return True
    t = t.rstrip() + f"\n\n## 关联知识\n{backlink}\n"
    target_path.write_text(t, encoding="utf-8")
    return True

total_backlinks = 0
for rel in NEW_SOURCES:
    fpath = WIKI / rel
    if not fpath.exists():
        print(f"⚠️ 不存在: {rel}")
        continue
    stem = fpath.stem
    content = fpath.read_text(encoding="utf-8")
    targets = extract_links(content)
    added = 0
    for target in targets:
        matches = list(WIKI.rglob(f"{target}.md"))
        if not matches:
            print(f"  ? 目标缺失: {target} (from {stem})")
            continue
        for m in matches:
            if m.stem == stem:
                continue
            if add_backlink(m, stem):
                added += 1
    total_backlinks += added
    print(f"✅ {stem}: 出链 {len(targets)} 条 / 新增回链 {added} 条")

print(f"\n织网完成，新增回链 {total_backlinks} 条")

# ── 更新 index.md 登记本轮 source ──
index_path = WIKI / "index.md"
if index_path.exists():
    idx = index_path.read_text(encoding="utf-8")
    marker = "## sources"
    added_lines = []
    for rel in NEW_SOURCES:
        fname = Path(rel).name
        if fname in idx:
            continue
        added_lines.append(f"- [[{fname}]]")
    if added_lines and marker in idx:
        pos = idx.index(marker)
        next_h2 = idx.find("\n## ", pos + len(marker))
        seg_end = next_h2 if next_h2 != -1 else len(idx)
        seg = idx[pos:seg_end]
        first_item = seg.find("\n- ")
        if first_item == -1:
            idx = idx[:pos + len(marker)] + "\n" + "\n".join(added_lines) + "\n" + idx[pos + len(marker):]
        else:
            insert_at = pos + first_item + 1
            idx = idx[:insert_at] + "\n".join(added_lines) + "\n" + idx[insert_at:]
        index_path.write_text(idx, encoding="utf-8")
        print(f"✅ index.md 已登记 {len(added_lines)} 条新 source")
    else:
        print("ℹ️ index.md 无需登记或缺少 sources 区")
else:
    print("⚠️ index.md 不存在，跳过登记")

print("\n✅ 本轮织网全部完成")
