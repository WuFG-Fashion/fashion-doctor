# -*- coding: utf-8 -*-
"""
v2.1 isolation & retrieval-access verification (specs §13.5 / §13.9②③④; boss-approved 2026-09-13)
Idempotent read-only check. Exit 0 = PASS, 1 = FAIL.
Checks:
  1. master_index.json contains ZERO entries from 20_personal/ or 40_companies/
     (个人域完全独立索引 + 公司域永不进共享索引)
  2. search_index() never returns retrieval=never / explicit_only / lifecycle expired|retired entries
  3. load_explicit(): T4 view (explicit_only) allowed; 20_personal refused; path traversal refused
  4. company-domain metadata coverage: all 40_companies/dongshang/*.md have scope:company + company:dongshang
"""
import os, sys, io, json, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
KB = r"D:\Fashion Doctor\fashion-doctor\knowledge_base"
sys.path.insert(0, os.path.join(KB, "tools"))

import retrieval_mod as R  # noqa: E402

fails = []

# ── 1. index isolation ─────────────────────────────────────────
idx = R.load_index()
if not idx:
    print("FAIL: master_index.json missing/unreadable")
    sys.exit(1)
n_pers = n_co = n_total = 0
never_cnt = explicit_cnt = expired_life = 0
for cat in idx.get("L2_categories", []):
    for e in cat.get("L3", []):
        n_total += 1
        p = str(e.get("path", ""))
        if p.startswith("20_personal/"):
            n_pers += 1
        if p.startswith("40_companies/"):
            n_co += 1
        r = e.get("retrieval", "eligible")
        if r == "never":
            never_cnt += 1
        elif r == "explicit_only":
            explicit_cnt += 1
        if (e.get("lifecycle") or "active") in ("expired", "retired"):
            expired_life += 1
print(f"[1] index entries={n_total} | 20_personal={n_pers} | 40_companies={n_co} | "
      f"retrieval never={never_cnt} explicit_only={explicit_cnt} expired/retired={expired_life}")
if n_pers or n_co:
    fails.append(f"index contains personal({n_pers})/company({n_co}) entries")
if never_cnt or explicit_cnt or expired_life:
    print("    (note: gated entries present in index but must be skipped at query time — check [2])")

# ── 2. search-time gating ──────────────────────────────────────
queries = ["个人", "太平鸟", "会员", "售罄率", "清仓", "培训"]
leak_never = leak_explicit = leak_life = 0
for q in queries:
    for m in R.search_index(q, idx):
        pass  # search_index already skips; count via raw scan below
# raw scan: verify skip logic directly
def raw_hits(q):
    return R.search_index(q, idx)
for q in queries:
    for m in raw_hits(q):
        # re-derive gating from index entry to double-check
        pass
# stronger: simulate by scanning all entries for any that WOULD match but are gated
leak = 0
for cat in idx.get("L2_categories", []):
    for e in cat.get("L3", []):
        life = e.get("lifecycle") or "active"
        r = e.get("retrieval", "eligible")
        if life in ("expired", "retired") or r in ("never", "explicit_only"):
            # try to match it against queries; if it would match, it must not leak
            for q in queries:
                res = R.search_index(q, idx)
                if any(x["id"] == e["id"] for x in res):
                    leak += 1
                    fails.append(f"gated entry leaked into results: {e['id']} ({q})")
print(f"[2] search-time gating: gated-entry leaks={leak}")

# ── 3. explicit injection channel ──────────────────────────────
t1 = R.load_explicit("Home.md")
ok1 = t1.get("allowed") and t1.get("retrieval") == "explicit_only"
print(f"[3a] --inject Home.md (T4 explicit_only): allowed={t1.get('allowed')} -> {'PASS' if ok1 else 'FAIL'}")
if not ok1:
    fails.append("T4 explicit injection refused unexpectedly")

t2 = R.load_explicit("20_personal/README.md")
ok2 = (not t2.get("allowed")) and ("个人域" in t2.get("reason", "") or "拒绝" in t2.get("reason", ""))
print(f"[3b] --inject 20_personal/README.md (never): allowed={t2.get('allowed')} reason={t2.get('reason','')[:40]} -> {'PASS' if ok2 else 'FAIL'}")
if not ok2:
    fails.append("personal-domain injection NOT refused")

t3 = R.load_explicit("../outside_secret.txt")
ok3 = not t3.get("allowed")
print(f"[3c] --inject path traversal: allowed={t3.get('allowed')} -> {'PASS' if ok3 else 'FAIL'}")
if not ok3:
    fails.append("path traversal not blocked")

t4 = R.load_explicit("40_companies/dongshang/01_制度/前台销售输机管理.md")
ok4 = t4.get("allowed")
print(f"[3d] --inject company page (eligible): allowed={t4.get('allowed')} -> {'PASS' if ok4 else 'FAIL'}")
if not ok4:
    fails.append("company eligible page injection refused unexpectedly")

# ── 4. company metadata coverage ───────────────────────────────
co_root = os.path.join(KB, "40_companies", "dongshang")
tot = ok = 0
for dirpath, dirnames, filenames in os.walk(co_root):
    for fn in filenames:
        if not fn.endswith(".md"):
            continue
        tot += 1
        with open(os.path.join(dirpath, fn), "rb") as f:
            head = f.read()  # full read: truncated multi-byte utf-8 chars would break strict decode and misroute to gbk
        txt = None
        for enc in ("utf-8", "gbk"):
            try:
                txt = head.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if txt and txt.startswith("---") and re.search(r"^scope:\s*company", txt, re.M) \
           and re.search(r"^company:\s*dongshang", txt, re.M):
            ok += 1
        else:
            fails.append(f"company file missing/incorrect fm: {fn}")
print(f"[4] company fm coverage: {ok}/{tot}")

print("\n==== RESULT:", "PASS ✅" if not fails else f"FAIL ❌ ({len(fails)}) ====")
for f_ in fails:
    print("  -", f_)
sys.exit(0 if not fails else 1)
