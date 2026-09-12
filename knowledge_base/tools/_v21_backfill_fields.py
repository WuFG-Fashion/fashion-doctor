# -*- coding: utf-8 -*-
# v2.1 logical-layering backfill: add layer/scope/volatility/as_of/expires_at|review_due_at/status
# to existing pages. Additive only - never overwrites existing keys. Idempotent.
# Rules (specs/知识库v2架构方案_讨论稿.md section 13.2/13.3):
#   entities    T2 brand slow(expires+180d)
#   concepts    T1 public evergreen(review+180d)
#   sources     T2 scope=brand_specific?brand:public  confidence==财报?slow(+180):fast(+90)
#   comparisons T1 public slow(review+180d)   (per S-round convention)
#   practices   T1 public evergreen(review+180d)
#   playbooks   T1 public evergreen(review+180d)
#   raw/articles T3 scope=brand?(focus_brands filename match):public fast(expires+90d)
import io, json, os, re, sys
from datetime import date, timedelta

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(KB, "wiki")
REPORT = os.path.join(KB, "_health", "2026-09-12_v21_backfill_report.md")

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
KEY_RE = re.compile(r"^([A-Za-z_]+):")


def load_focus_brands():
    p = os.path.join(KB, "kb_benchmarks.json")
    try:
        with io.open(p, encoding="utf-8") as f:
            data = json.load(f)
        fb = data.get("focus_brands", [])
        return set(x.lower() for x in fb)
    except Exception:
        return set()


FOCUS = load_focus_brands()


def parse_date(s):
    if not s:
        return None
    m = DATE_RE.search(str(s))
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def split_frontmatter(text):
    """Return (fm_lines, body, had_fm). fm excludes the --- fences."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text, False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:]), True
    return None, text, False


def fm_get(fm_lines, key):
    for ln in fm_lines:
        if ln.startswith(key + ":"):
            return ln.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def fm_has(fm_lines, key):
    for ln in fm_lines:
        if KEY_RE.match(ln) and ln.split(":", 1)[0] == key:
            return True
    return False


def brand_in_name(name):
    n = name.lower()
    for b in FOCUS:
        if b and b in n:
            return b
    return None


def plan_for(relpath, fname, fm_lines, fullpath=None):
    """Return dict of fields to add (already resolved values)."""
    as_of = parse_date(fname)  # sources 文件名日期 = 采集日 ≈ 信息观察时点，优先
    if as_of is None and fm_lines is not None:
        as_of = parse_date(fm_get(fm_lines, "updated")) or parse_date(fm_get(fm_lines, "created"))
    if as_of is None:
        as_of = date.fromtimestamp(os.path.getmtime(fullpath or os.path.join(WIKI, relpath)))
    d = as_of

    if relpath.startswith("entities/"):
        return {"layer": "T2", "scope": "brand", "volatility": "slow",
                "as_of": str(d), "expires_at": str(d + timedelta(days=180)), "status": "active"}
    if relpath.startswith("concepts/"):
        return {"layer": "T1", "scope": "public", "volatility": "evergreen",
                "as_of": str(d), "review_due_at": str(d + timedelta(days=180)), "status": "active"}
    if relpath.startswith("sources/"):
        bs = (fm_get(fm_lines, "brand_specific") or "").lower() == "true"
        conf = fm_get(fm_lines, "confidence") or ""
        slow = "财报" in conf  # 含混合口径如 "财报（安踏数据）| 品牌自宣"
        if slow:
            return {"layer": "T2", "scope": "brand" if bs else "public", "volatility": "slow",
                    "as_of": str(d), "expires_at": str(d + timedelta(days=180)), "status": "active"}
        return {"layer": "T2", "scope": "brand" if bs else "public", "volatility": "fast",
                "as_of": str(d), "expires_at": str(d + timedelta(days=90)), "status": "active"}
    if relpath.startswith("comparisons/"):
        return {"layer": "T1", "scope": "public", "volatility": "slow",
                "as_of": str(d), "review_due_at": str(d + timedelta(days=180)), "status": "active"}
    if relpath.startswith("practices/") or relpath.startswith("playbooks/"):
        return {"layer": "T1", "scope": "public", "volatility": "evergreen",
                "as_of": str(d), "review_due_at": str(d + timedelta(days=180)), "status": "active"}
    if relpath.startswith("10_web/articles/"):
        b = brand_in_name(fname)
        return {"type": "raw", "layer": "T3", "scope": "brand" if b else "public",
                "volatility": "fast", "as_of": str(d),
                "expires_at": str(d + timedelta(days=90)), "status": "active"}
    return None


def main():
    targets = ["entities", "concepts", "sources", "comparisons", "practices", "playbooks"]
    extra_kb_dirs = ["10_web/articles"]  # KB-rooted (not under wiki/)
    stats = {}
    changed_files = 0
    skipped = 0
    walk_units = [(os.path.join(WIKI, t), WIKI, t) for t in targets]
    walk_units += [(os.path.join(KB, t), KB, t) for t in extra_kb_dirs]
    for root, rel_base, t in walk_units:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for fn in sorted(files):
                if not fn.endswith(".md"):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, rel_base).replace("\\", "/")
                with io.open(full, encoding="utf-8") as f:
                    text = f.read()
                fm_lines, body, had_fm = split_frontmatter(text)
                plan = plan_for(rel, fn, fm_lines, full) if had_fm else plan_for(rel, fn, None, full)
                if plan is None:
                    continue
                if had_fm:
                    adds = [(k, v) for k, v in plan.items() if not fm_has(fm_lines, k)]
                    if not adds:
                        skipped += 1
                        continue
                    new_fm = list(fm_lines) + ["%s: %s" % (k, v) for k, v in adds]
                    new_text = "---\n" + "\n".join(new_fm) + "\n---\n" + body
                else:
                    adds = list(plan.items())
                    new_text = "---\n" + "\n".join("%s: %s" % kv for kv in adds) + "\n---\n\n" + text
                with io.open(full, "w", encoding="utf-8", newline="\n") as f:
                    f.write(new_text)
                changed_files += 1
                top = t.split("/")[0]
                st = stats.setdefault(t, {"files": 0, "fields": 0})
                st["files"] += 1
                st["fields"] += len(adds)
    lines = ["# v2.1 逻辑分层字段回填报告", "",
             "- 日期：2026-09-12", "- 模式：批量回填（只增不改，幂等）",
             "- 改动文件数：%d；已合规跳过：%d" % (changed_files, skipped), "",
             "| 目录 | 文件数 | 补字段数 |", "|---|---|---|"]
    for t in list(targets) + extra_kb_dirs:
        if t in stats:
            lines.append("| %s | %d | %d |" % (t, stats[t]["files"], stats[t]["fields"]))
    lines += ["", "## 口径", "",
              "- entities T2/brand/slow+180d; concepts T1/public/evergreen+180d 复核",
              "- sources T2，scope 取 brand_specific；confidence=财报 → slow+180d，其余 fast+90d",
              "- comparisons T1/public/slow+180d 复核（沿 S 轮约定）; practices/playbooks T1/public/evergreen+180d 复核",
              "- 10_web/articles T3，文件名命中 focus_brands → brand 否则 public，fast+90d",
              "- as_of 取 文件名日期→updated→created→mtime；全部 status: active（不判过期，由 TTL 引擎后续校准）"]
    with io.open(REPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(json.dumps({"changed": changed_files, "skipped": skipped, "stats": stats}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
