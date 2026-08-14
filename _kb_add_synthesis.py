#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_kb_add_synthesis.py — 知识库「结论+信息链」骨架批量补全

用途：
  为 wiki/concepts/ 与 wiki/entities/ 中缺失 CLAUDE.md 2.3 强制区块
  （## 结论 / ## 信息链）的页面，自动插入骨架。
  - ## 信息链：由页面现有 [[双链]] 图谱机械派生（上游来源 → 本页 → 下游实体/概念/对比/打法），
    并列出指向「尚未建页」目标的断点（顺带发现孤岛/断链）。
  - ## 结论：插入带「摘要原材 + TODO」的骨架。不伪造洞察——真实洞察由 AI（agent）按优先级生成、人工审阅。

用法：
  python _kb_add_synthesis.py --dry-run            # 仅打印将插入的内容，不改文件
  python _kb_add_synthesis.py --limit 5            # 仅处理中心度最高的前 5 页（需先有 _health/_synthesis_backlog.json）
  python _kb_add_synthesis.py                      # 全量执行（幂等：已有区块则跳过）
  python _kb_add_synthesis.py --only peacebird semir   # 仅处理指定页面名

依赖：仅标准库。
"""
import os, re, glob, argparse, json, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.join(ROOT, "knowledge_base", "wiki")
SOURCES = os.path.join(WIKI, "sources")
CONCEPTS = os.path.join(WIKI, "concepts")
ENTITIES = os.path.join(WIKI, "entities")
COMPARISONS = os.path.join(WIKI, "comparisons")
PLAYBOOKS = os.path.join(WIKI, "playbooks")

MAX_LINKS_PER_GROUP = 15  # 信息链每组最多列出条数，超出折叠为「(+N 更多)」


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def parse_links(text):
    """返回所有 [[target|alias]] / [[target]] 中的 target（去空白）。"""
    return [m.strip() for m in re.findall(r"\[\[([^\]\|]+)", text)]


def split_frontmatter(text):
    """返回 (frontmatter_str, body_str)。无 frontmatter 时 frontmatter=''。"""
    if text.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
        if m:
            return m.group(0), text[m.end():]
    return "", text


def get_fm_field(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else ""


def build_index():
    """建立 页面名 -> (文件夹类别) 映射，用于分类与存在性判断。"""
    idx = {}
    for cat, folder in [("source", SOURCES), ("concept", CONCEPTS),
                        ("entity", ENTITIES), ("comparison", COMPARISONS),
                        ("playbook", PLAYBOOKS)]:
        for p in glob.glob(os.path.join(folder, "*.md")):
            idx[os.path.basename(p)[:-3]] = cat
    return idx


def derive_info_chain(body, page_name, idx, title, ptype):
    """由现有 [[双链]] 机械派生信息链文本。"""
    links = parse_links(body)
    # 去重保序
    seen, ordered = set(), []
    for l in links:
        if l and l not in seen:
            seen.add(l); ordered.append(l)

    groups = {"source": [], "entity": [], "concept": [], "comparison": [], "playbook": [], "unknown": [], "missing": []}
    SKIP = {"CLAUDE.md"}  # 文档引用，非 wiki 页，不计入断点
    for l in ordered:
        if l in SKIP:
            continue
        cat = idx.get(l)
        if cat is None:
            groups["missing"].append(l)
        else:
            groups[cat].append(l)

    def fmt(lst, cat_label):
        if not lst:
            return f"- 关联{cat_label}：无"
        shown = lst[:MAX_LINKS_PER_GROUP]
        tail = ""
        if len(lst) > MAX_LINKS_PER_GROUP:
            tail = f" · …(+{len(lst)-MAX_LINKS_PER_GROUP} 更多)"
        return f"- 关联{cat_label}：" + " · ".join(f"[[{x}]]" for x in shown) + tail

    lines = ["## 信息链", ""]
    if groups["source"]:
        src = groups["source"][:MAX_LINKS_PER_GROUP]
        tail = f" · …(+{len(groups['source'])-MAX_LINKS_PER_GROUP} 更多)" if len(groups["source"])>MAX_LINKS_PER_GROUP else ""
        lines.append(f"- **上游 · 来源支撑**：" + " · ".join(f"[[{x}]]" for x in src) + tail + "（本页事实来自这些原始采集）")
    else:
        lines.append("- **上游 · 来源支撑**：无（建议补充源头 source 页）")
    lines.append(f"- **本页定位**：{ptype} —— {title or page_name}")
    lines.append(fmt(groups["entity"], "实体"))
    lines.append(fmt(groups["concept"], "概念"))
    lines.append(fmt(groups["comparison"], "对比"))
    lines.append(fmt(groups["playbook"], "打法"))
    if groups["missing"]:
        m = groups["missing"][:MAX_LINKS_PER_GROUP]
        tail = f" · …(+{len(groups['missing'])-MAX_LINKS_PER_GROUP} 更多)" if len(groups['missing'])>MAX_LINKS_PER_GROUP else ""
        lines.append("- ⚠️ **断点（指向未建页）**：" + " · ".join(f"[[{x}]]" for x in m) + tail + "（待补页或修正双链）")
    else:
        lines.append("- ⚠️ **断点检查**：无（所有出站双链均有目标页）")
    lines.append("")
    return "\n".join(lines)


def derive_conclusion_skeleton(summary_text):
    """结论骨架：放摘要原材 + TODO，不伪造洞察。"""
    raw = summary_text.strip()
    if not raw:
        raw = "（本页暂未提取到顶部摘要，请补充一句话摘要）"
    # 去掉每行前导 '>' 与空格，合并为引用
    quoted = "\n> ".join(line.lstrip("> ").rstrip() for line in raw.split("\n"))
    block = [
        "## 结论",
        "",
        "> ⏳ **待 AI 合成洞察**：本页结论应为「判断 / 推论」（例：行业进入 X 期、Y 是胜负手），"
        "禁止数据复述。以下为本页顶部摘要，作为合成原始素材：",
        ">",
        f"> {quoted}",
        "",
        "_（AI 将基于本页数据提炼 2–4 条结论洞察；规范见 [[CLAUDE.md]] 2.3 区块规范）_",
        "",
    ]
    return "\n".join(block)


def extract_summary(body):
    """提取全文第一个 blockquote 连续块（frontmatter 之后、无论前面是否有 # H1 标题）。"""
    fm, b = split_frontmatter(body)
    lines = b.split("\n")
    # 找到第一个以 '>' 起始的行
    start = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith(">"):
            start = i
            break
    if start is None:
        return ""
    buf = []
    i = start
    while i < len(lines) and lines[i].lstrip().startswith(">"):
        buf.append(lines[i])
        i += 1
    return "\n".join(buf)


def first_content_header_pos(text):
    """返回全文（含 frontmatter）中第一个内容 '## ' 标题的行号；结论将插在其前。
    注意：返回的是全文绝对行号（已计入 frontmatter 偏移），调用方直接对全文 lines 使用。"""
    fm, b = split_frontmatter(text)
    offset = 0
    if fm:
        idx = text.find(b)
        if idx >= 0:
            offset = text[:idx].count("\n")
    lines = b.split("\n")
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+\S", ln):
            return offset + i
    return -1


def insert_conclusion(body, skeleton):
    pos = first_content_header_pos(body)
    lines = body.split("\n")
    if pos == -1:
        # 无内容标题：追加到末尾
        return body.rstrip() + "\n\n" + skeleton.rstrip() + "\n"
    # 在第一个内容 ## 之前插入（空行分隔）
    out = lines[:pos] + ["", skeleton.rstrip(), ""] + lines[pos:]
    return "\n".join(out)


def insert_info_chain(body, chain):
    """在 '## 关联页面'（最后一个）之前插入；缺则插到末尾或最后一个 '## ' 前。"""
    lines = body.split("\n")
    # 找最后一个 ## 关联页面
    target = -1
    for i, ln in enumerate(lines):
        if re.match(r"^##\s*关联页面", ln):
            target = i
    if target != -1:
        out = lines[:target] + [chain.rstrip(), ""] + lines[target:]
        return "\n".join(out)
    # 回退：最后一个 ## 前
    last = -1
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+\S", ln):
            last = i
    if last != -1:
        out = lines[:last] + [chain.rstrip(), ""] + lines[last:]
        return "\n".join(out)
    return body.rstrip() + "\n\n" + chain.rstrip() + "\n"


def process_file(path, page_name, idx, dry_run, only_set=None):
    text = read(path)
    has_concl = bool(re.search(r"^##\s*结论", text, re.M))
    has_chain = bool(re.search(r"^##\s*信息链", text, re.M))
    fm, _ = split_frontmatter(text)
    title = get_fm_field(fm, "title")
    ptype = get_fm_field(fm, "type") or "page"

    actions = []
    new_text = text
    if not has_concl:
        summary = extract_summary(text)
        skeleton = derive_conclusion_skeleton(summary)
        new_text = insert_conclusion(new_text, skeleton)
        actions.append("结论")
    if not has_chain:
        chain = derive_info_chain(new_text, page_name, idx, title, ptype)
        new_text = insert_info_chain(new_text, chain)
        actions.append("信息链")

    if not actions:
        return None  # 已完整，跳过

    if dry_run:
        print(f"\n===== DRY-RUN {page_name} → 将插入: {', '.join(actions)} =====")
        if "结论" in actions:
            print(derive_conclusion_skeleton(extract_summary(text)))
        if "信息链" in actions:
            print(derive_info_chain(text, page_name, idx, title, ptype))
        return "dry"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return actions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()

    idx = build_index()
    # 收集候选页（concepts + entities）
    cand = []
    for folder in (CONCEPTS, ENTITIES):
        for p in glob.glob(os.path.join(folder, "*.md")):
            cand.append((p, os.path.basename(p)[:-3]))

    # 过滤：仅缺区块者
    todo = []
    for p, name in cand:
        t = read(p)
        if not re.search(r"^##\s*结论", t, re.M) or not re.search(r"^##\s*信息链", t, re.M):
            todo.append((p, name))

    if args.only:
        todo = [(p, n) for p, n in todo if n in set(args.only)]

    # 按中心度排序（读 backlog）
    order = {}
    bp = os.path.join(ROOT, "knowledge_base", "_health", "_synthesis_backlog.json")
    if os.path.exists(bp):
        try:
            bl = json.load(open(bp, encoding="utf-8"))
            order = {x["name"]: i for i, x in enumerate(bl)}
        except Exception:
            pass
    todo.sort(key=lambda x: order.get(x[1], 9999))

    if args.limit:
        todo = todo[:args.limit]

    print(f"[KB合成] 待处理页: {len(todo)}" + (" (DRY-RUN)" if args.dry_run else ""))
    done = 0
    for p, name in todo:
        r = process_file(p, name, idx, args.dry_run)
        if r and r != "dry":
            done += 1
            print(f"  ✓ {name}: +{','.join(r)}")
        elif r == "dry":
            done += 1
    print(f"[KB合成] 完成 {done} 页" + ("（dry-run，未写盘）" if args.dry_run else ""))


if __name__ == "__main__":
    main()
