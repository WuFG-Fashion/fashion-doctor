# -*- coding: utf-8 -*-
"""Round A Run 3 — 登记 7 个 source 页到 index.md，并向 服装行业竞争格局 追加 7 品牌回链。
读取 _roundA_run3_index_data.json（由 gen 脚本产出，保证文件名一致）。"""
import os, re, json

IDX="knowledge_base/wiki/index.md"
COMP="knowledge_base/wiki/concepts/服装行业竞争格局.md"
DATA="_roundA_run3_index_data.json"

d=json.load(open(DATA,encoding="utf-8"))
SOURCES=d["SOURCES"]
BACKLINKS=d["BACKLINKS"]

# ---- index.md: insert source rows after the NAUTICA Run1 source line ----
idx=open(IDX,encoding="utf-8").read()
anchor="2026-08-15_NAUTICA___ABG_中国运营切换速览_2026"
assert anchor in idx, "Run1 nautica source anchor missing in index.md"
ins_lines=[]
for fn,summ,tags in SOURCES:
    ins_lines.append("| [[%s]] ⭐ NEW | %s | %s |" % (fn[:-3], summ, tags))
insert_block="\n".join(ins_lines)
idx=idx.replace(anchor, anchor+"\n"+insert_block, 1)
open(IDX,"w",encoding="utf-8").write(idx)
print("index.md: inserted", len(SOURCES), "source rows after nautica anchor.")

# ---- 服装行业竞争格局.md: append backlinks at end of 关联页面 section ----
comp=open(COMP,encoding="utf-8").read()
m=re.search(r"(## 关联页面.*?)(\n## |\Z)",comp,re.S)
assert m, "关联页面 section not found"
sec=m.group(1)
added=0
for key,desc in BACKLINKS:
    bullet="- [[%s]] — %s" % (key,desc)
    if bullet not in sec:
        sec=sec.rstrip("\n")+"\n"+bullet+"\n"
        added+=1
comp=comp[:m.start(1)]+sec+comp[m.end(1):]
open(COMP,"w",encoding="utf-8").write(comp)
print("服装行业竞争格局: appended", added, "backlinks.")

print("OK")
