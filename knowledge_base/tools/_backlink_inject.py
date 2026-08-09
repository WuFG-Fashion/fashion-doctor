#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量回链注入器 (kb-link 引擎)
扫描 wiki/ 下所有页面的 frontmatter cross_refs 出链，
在「被引用页」的「关联页面」区块追加回链，实现双向织网 (CLAUDE.md §3.5)。
- 幂等：已存在的回链不重复追加
- 仅作用于 wiki/ 下页面（不碰 raw/ L2_*/ Home / MOC / human）
- 解析目标页时匹配 basename（忽略 .md / |alias / #anchor）
"""
import os, re, io

WIKI = 'wiki'
SKIP = {'.obsidian', '__pycache__', 'tools'}
link_pat = re.compile(r'\[\[([^\]#|]+?)(?:\|[^]]*)?\]\]')

def build_index():
    idx = {}
    for dp, dns, fns in os.walk(WIKI):
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            if not fn.endswith('.md'):
                continue
            base = fn[:-3]
            idx[base] = os.path.join(dp, fn).replace('\\', '/')
    return idx

def frontmatter_links(path):
    s = io.open(path, encoding='utf-8').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', s, re.S)
    if not m:
        return [], s
    return link_pat.findall(m.group(1)), s

def norm(l):
    l = l.strip()
    if l.endswith('.md'):
        l = l[:-3]
    return l

def main():
    idx = build_index()
    # 1) 收集每页出链（目标必须是 wiki 内已存在的页，且不是自己）
    outgoing = {}
    for base, path in idx.items():
        links, _ = frontmatter_links(path)
        targets = set()
        for l in links:
            t = norm(l)
            if t in idx and idx[t] != path:
                targets.add(t)
        if targets:
            outgoing[path] = targets

    # 2) 反向聚合：目标页 -> 引用它的源页集合
    backlinks = {}
    for path, targets in outgoing.items():
        src = os.path.basename(path)[:-3]
        for t in targets:
            backlinks.setdefault(idx[t], set()).add(src)

    # 3) 注入回链（幂等）
    def inject(path, new_bases):
        s = io.open(path, encoding='utf-8').read()
        existing = {norm(e) for e in link_pat.findall(s)}
        to_add = [b for b in new_bases if b not in existing]
        if not to_add:
            return 0
        m = re.search(r'(?m)^#{2,3} 关联页面\s*$', s)
        bullets = '\n' + '\n'.join(f'- [[{b}]]' for b in to_add)
        if m:
            rest = s[m.end():]
            nm = re.search(r'(?m)^#{1,3} ', rest)
            pos = m.end() + (nm.start() if nm else len(rest))
            head, tail = s[:pos], s[pos:]
            if not head.endswith('\n'):
                head += '\n'
            s = head + bullets + '\n' + tail
        else:
            if not s.endswith('\n'):
                s += '\n'
            s += '\n## 关联页面\n' + bullets + '\n'
        io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
        return len(to_add)

    total_pages = 0
    total_links = 0
    for tp, srcs in backlinks.items():
        n = inject(tp, sorted(srcs))
        if n:
            total_pages += 1
            total_links += n
    print(f"回链注入完成：更新 {total_pages} 个目标页，新增 {total_links} 条回链")
    print(f"（涉及源页 {sum(len(v) for v in backlinks.values())} 个引用关系）")

if __name__ == '__main__':
    main()
