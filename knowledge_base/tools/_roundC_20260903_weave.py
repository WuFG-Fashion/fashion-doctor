# -*- coding: utf-8 -*-
"""Round C (2026-09-03) weave: backlink injection for the 6 new pages.

Reads each new page's frontmatter cross_refs, then injects a reciprocal
"关联页面" bullet into every referenced target page (idempotent).
Only touches wiki/ pages; creates the 关联页面 section if missing.
"""
import os, re, io
from pathlib import Path

WIKI = Path(__file__).resolve().parent.parent / "wiki"
SKIP_DIRS = {".obsidian", "__pycache__"}
link_pat = re.compile(r"\[\[([^\]#|]+?)(?:\|[^]]*)?\]\]")

NEW_PAGES = [
    "sources/2026-09-03_零售BI分角色看板与KPI基准2026.md",
    "sources/2026-09-03_服装库存分析四层拆解与售罄率库龄交叉法.md",
    "sources/2026-09-03_零售经营语义层建设指南_指标统一四层法.md",
    "sources/2026-09-03_全球零售数据平台_中央管控与本地使用.md",
    "practices/cabbeen_brand_analytics_2026.md",
    "practices/crocs_financial_benchmark_template_2026.md",
]


def build_index():
    idx = {}
    for dp, dns, fns in os.walk(WIKI):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith(".md"):
                base = fn[:-3]
                idx.setdefault(base, os.path.join(dp, fn).replace("\\", "/"))
    return idx


def read_frontmatter(path):
    s = io.open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", s, re.S)
    if not m:
        return [], s
    return link_pat.findall(m.group(1)), s


def norm(l):
    l = l.strip()
    return l[:-3] if l.endswith(".md") else l


def inject_backlink(path, new_base):
    s = io.open(path, encoding="utf-8").read()
    if re.search(r"\[\[" + re.escape(new_base) + r"(?:\||\]\])", s):
        return False
    bullet = f"- [[{new_base}]]"
    m = re.search(r"(?m)^## 关联页面\s*$", s)
    if m:
        rest = s[m.end():]
        nm = re.search(r"(?m)^#{1,3} ", rest)
        pos = m.end() + (nm.start() if nm else len(rest))
        s = s[:pos].rstrip() + "\n" + bullet + "\n\n" + s[pos:].lstrip("\n")
    else:
        s = s.rstrip() + f"\n\n## 关联页面\n{bullet}\n"
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    return True


def main():
    idx = build_index()
    ok_pages, ok_links = set(), 0
    for rel in NEW_PAGES:
        path = WIKI / rel
        if not path.exists():
            print(f"!! new page missing: {rel}")
            continue
        base = Path(rel).stem
        links, _ = read_frontmatter(path)
        for raw in links:
            t = norm(raw)
            if t not in idx or idx[t] == str(path).replace("\\", "/"):
                print(f"  - target not in wiki index, skip: {t}")
                continue
            if inject_backlink(idx[t], base):
                ok_pages.add(idx[t])
                ok_links += 1
                print(f"  + backlink -> {t}")
    print(f"weave done: {ok_links} backlinks into {len(ok_pages)} pages")


if __name__ == "__main__":
    main()
