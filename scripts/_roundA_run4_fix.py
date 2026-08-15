# -*- coding: utf-8 -*-
"""Run4 收尾修正：
1) 实体页 frontmatter sources 中 R4 条目误带 .md 后缀，统一去掉以匹配既有裸文件名约定。
2) 校验：每个实体页 cross_refs 含 [[服装行业竞争格局]]、且含"近期动态刷新"小节。
"""
import os, re

ENT="knowledge_base/wiki/entities"
KEYS=["cabbeen","peacebird","trussardi","karl_lagerfeld","salomon","crocs","mlb","two_am","chuu","ariose_years","dekashell"]

for k in KEYS:
    p=os.path.join(ENT,k+".md")
    s=open(p,encoding="utf-8").read()
    # fix .md in R4 source entries (only frontmatter sources line)
    s2=re.sub(r"(2026-08-15_R4_[^\]]*?)\.md(\s*\])", r"\1\2", s)
    # verify
    has_xr="[[服装行业竞争格局]]" in s2
    has_sec="近期动态刷新（2026-08-15 · A轮第4轮全量覆盖）" in s2
    changed = (s2!=s)
    if changed:
        open(p,"w",encoding="utf-8").write(s2)
    print("%-14s | .md fixed=%s | 竞争格局回链=%s | 刷新小节=%s" % (k, changed, has_xr, has_sec))
print("FIX DONE")
