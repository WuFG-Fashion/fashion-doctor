"""CLAUDE.md 合规性深度审计 —— 逐项对照规范检查所有 wiki 页面"""
import os, re, json
from pathlib import Path
from datetime import date

KB = Path("D:/Fashion Doctor/fashion-doctor/knowledge_base")
WIKI = KB / "wiki"
TODAY = date.today()

# ── 工具函数 ──
def parse_frontmatter(text):
    """解析 YAML frontmatter，返回 dict 和 剩余内容"""
    fm = {}
    remaining = text
    if text.startswith("---"):
        end = text.find("---", 4)
        if end != -1:
            block = text[4:end]
            remaining = text[end+3:].strip()
            for line in block.strip().split("\n"):
                line = line.strip()
                if ":" in line and not line.startswith("#"):
                    key, _, val = line.partition(":")
                    key, val = key.strip(), val.strip()
                    # 解析列表
                    if val.startswith("[") and val.endswith("]"):
                        val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
                    fm[key] = val
    return fm, remaining

def has_frontmatter(text):
    return text.strip().startswith("---")

def has_oneliner(text):
    """检查是否有一句话摘要 (blockquote after title)"""
    lines = [l.strip() for l in text.split("\n")]
    for l in lines:
        if l.startswith("> "):
            return True
    return False

def has_cross_refs(text):
    """是否有 [[双链]]"""
    return bool(re.search(r'\[\[.+?\]\]', text))

def has_tags(text):
    """是否有标签"""
    return bool(re.search(r'tags:\s*\[', text))

def has_sources_ref(text):
    """是否有来源标注"""
    # 检查 frontmatter sources 或文中的 > **来源**：
    return bool(re.search(r'sources:', text)) or bool(re.search(r'\*\*来源\*\*', text))

def count_h1(text):
    return len(re.findall(r'^# [^#]', text, re.MULTILINE))

def count_sections(text):
    return len(re.findall(r'^## ', text, re.MULTILINE))

def estimate_size(text):
    """估算内容量（移除 frontmatter 和空行后）"""
    if text.startswith("---"):
        end = text.find("---", 4)
        if end != -1:
            text = text[end+3:]
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return len(lines)

def check_directory_type(fpath):
    """检查文件所在目录是否与 type 一致"""
    rel = Path(fpath)
    parent = rel.parent.name
    mapping = {
        "entities": "entity", "concepts": "concept",
        "practices": "practice", "comparisons": "comparison",
        "sources": "source"
    }
    return mapping.get(parent, "unknown")

# ── 主审计逻辑 ──
all_pages = []
errors = []

for md_file in sorted(WIKI.rglob("*.md")):
    rel = md_file.relative_to(WIKI)
    parent = md_file.parent.name
    
    # 跳过 index.md 和 log.md（元文件）
    if md_file.name in ("index.md", "log.md", "overview.md"):
        continue
    
    content = md_file.read_text(encoding="utf-8", errors="ignore")
    fm, body = parse_frontmatter(content)
    expected_type = check_directory_type(md_file)
    
    record = {
        "file": str(rel),
        "directory": parent,
        "has_fm": has_frontmatter(content),
        "fm_type": fm.get("type", ""),
        "expected_type": expected_type,
        "fm_title": fm.get("title", ""),
        "fm_tags": isinstance(fm.get("tags"), list),
        "fm_sources": bool(fm.get("sources")),
        "fm_created": fm.get("created", ""),
        "fm_updated": fm.get("updated", ""),
        "fm_cross_refs": bool(fm.get("cross_refs")),
        "body_has_oneliner": has_oneliner(body),
        "body_has_cross_refs": has_cross_refs(body),
        "body_has_sources": has_sources_ref(content),
        "body_h1_count": count_h1(body),
        "body_section_count": count_sections(body),
        "body_size_lines": estimate_size(content),
        "issues": []
    }
    
    # ── 逐项检查 ──
    # 1. Frontmatter 存在
    if not record["has_fm"]:
        record["issues"].append("❌ 缺少 YAML frontmatter（CLAUDE.md 2.1 强制要求）")
    else:
        # 2. type 字段
        if not record["fm_type"]:
            record["issues"].append("⚠️ frontmatter 缺少 type 字段")
        elif record["fm_type"] != record["expected_type"]:
            record["issues"].append(f"⚠️ type={record['fm_type']} 但位于 {parent}/ 目录（应为 {expected_type}）")
        
        # 3. title
        if not record["fm_title"]:
            record["issues"].append("⚠️ frontmatter 缺少 title 字段")
        
        # 4. tags
        if not record["fm_tags"]:
            record["issues"].append("⚠️ frontmatter 缺少 tags 字段（CLAUDE.md 4.3）")
        
        # 5. sources
        if not record["fm_sources"]:
            record["issues"].append("⚠️ frontmatter 缺少 sources 字段（CLAUDE.md 5.1）")
        
        # 6. created/updated
        if not record["fm_created"]:
            record["issues"].append("⚠️ frontmatter 缺少 created 字段")
        if not record["fm_updated"]:
            record["issues"].append("⚠️ frontmatter 缺少 updated 字段")
    
    # 7. 一句话摘要
    if not record["body_has_oneliner"]:
        record["issues"].append("⚠️ 缺少一句话摘要 (blockquote)（CLAUDE.md 5.1）")
    
    # 8. [[双链]]
    if not record["body_has_cross_refs"]:
        record["issues"].append("❌ 没有任何 [[双链]]（CLAUDE.md 5.1 要求至少一条）")
    
    # 9. 来源标注
    if not record["body_has_sources"]:
        record["issues"].append("⚠️ 缺少来源标注（CLAUDE.md 5.1）")
    
    # 10. h1 数量
    if record["body_h1_count"] == 0:
        record["issues"].append("❌ 页面没有 # H1 标题")
    elif record["body_h1_count"] > 1:
        record["issues"].append(f"⚠️ 页面有 {record['body_h1_count']} 个 H1 标题")
    
    # 11. 过期检查（CLAUDE.md 3.4: 90 天）
    if record["fm_updated"]:
        try:
            parts = record["fm_updated"].strip().split("-")
            updated_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
            days_old = (TODAY - updated_date).days
            if days_old > 90:
                record["issues"].append(f"❌ 过期 {days_old} 天（CLAUDE.md 3.4: >90天需刷新）")
            record["days_since_update"] = days_old
        except:
            pass
    
    all_pages.append(record)

# ── 汇总统计 ──
total = len(all_pages)
no_fm = [p for p in all_pages if not p["has_fm"]]
no_type = [p for p in all_pages if p["has_fm"] and not p["fm_type"]]
type_mismatch = [p for p in all_pages if p["has_fm"] and p["fm_type"] and p["fm_type"] != p["expected_type"]]
no_tags = [p for p in all_pages if not p["fm_tags"]]
no_sources = [p for p in all_pages if not p["fm_sources"] and not p["body_has_sources"]]
no_links = [p for p in all_pages if not p["body_has_cross_refs"]]
no_oneliner = [p for p in all_pages if not p["body_has_oneliner"]]
expired = [p for p in all_pages if any("过期" in i for i in p["issues"])]
issues_pages = [(p["file"], p["issues"]) for p in all_pages if p["issues"]]
perfect_pages = [p for p in all_pages if not p["issues"]]

# 按目录统计
dir_stats = {}
for p in all_pages:
    d = p["directory"]
    if d not in dir_stats:
        dir_stats[d] = {"total": 0, "no_fm": 0, "no_links": 0, "issues": 0}
    dir_stats[d]["total"] += 1
    if not p["has_fm"]: dir_stats[d]["no_fm"] += 1
    if not p["body_has_cross_refs"]: dir_stats[d]["no_links"] += 1
    if p["issues"]: dir_stats[d]["issues"] += 1

# ── 输出 ──
print("=" * 70)
print("📊 CLAUDE.md 合规性深度审计")
print("=" * 70)
print()
print(f"审计时间: {TODAY}")
print(f"页面总数: {total}")
print(f"完全合规: {perfect_pages} 页 ({len(perfect_pages)/total*100:.1f}%){' 🎉' if perfect_pages else ''}")
print(f"有问题: {len(issues_pages)} 页 ({len(issues_pages)/total*100:.1f}%)")
print()

print("=" * 70)
print("📁 按目录统计")
print("=" * 70)
print(f"{'目录':<15} {'总数':>5} {'缺frontmatter':>12} {'缺双链':>8} {'有问题':>8}")
print("-" * 50)
for d in ["sources", "concepts", "entities", "practices", "comparisons"]:
    s = dir_stats.get(d, {})
    print(f"{d:<15} {s.get('total',0):>5} {s.get('no_fm',0):>12} {s.get('no_links',0):>8} {s.get('issues',0):>8}")

print()
print("=" * 70)
print("🔴 关键问题汇总")
print("=" * 70)
print(f"缺少 frontmatter:              {len(no_fm)} 页")
print(f"缺少 type 字段:                {len(no_type)} 页")
print(f"type 与目录不匹配:             {len(type_mismatch)} 页")
print(f"缺少 tags:                     {len(no_tags)} 页")
print(f"缺少来源引用:                  {len(no_sources)} 页")
print(f"没有 [[双链]]（孤岛）:         {len(no_links)} 页")
print(f"缺少一句话摘要:                {len(no_oneliner)} 页")
print(f"过期(>90天):                   {len(expired)} 页")

if type_mismatch:
    print()
    print("type 不匹配详情:")
    for p in type_mismatch:
        print(f"  {p['file']}: fm_type={p['fm_type']}, expected={p['expected_type']}")

if no_links:
    print()
    print("孤岛页面（无 [[双链]]）:")
    for p in no_links:
        print(f"  {p['file']}")

# ── 导出详细报告 ──
report = {
    "audit_date": TODAY.isoformat(),
    "total_pages": total,
    "perfect_pages": len(perfect_pages),
    "issues_pages": len(issues_pages),
    "summary": {
        "no_frontmatter": len(no_fm),
        "no_type": len(no_type),
        "type_mismatch": len(type_mismatch),
        "no_tags": len(no_tags),
        "no_sources": len(no_sources),
        "no_links": len(no_links),
        "no_oneliner": len(no_oneliner),
        "expired_90d": len(expired),
    },
    "directory_stats": {k: v for k, v in dir_stats.items()},
    "issues": [{"file": f, "issues": i} for f, i in issues_pages],
    "orphan_pages": [p["file"] for p in no_links],
}

report_path = KB / "audit_report.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n✅ 详细审计报告: {report_path}")

# 严重程度评分
score = 100
score -= len(no_fm) * 3        # frontmatter 缺失 = 严重
score -= len(no_links) * 5     # 孤岛 = 非常严重
score -= len(no_type) * 1
score -= len(no_sources) * 2
score -= len(no_oneliner) * 1
score -= len(expired) * 2
score = max(0, score)

print(f"\n📈 健康评分: {score}/100")
print(f"  等级: {'🟢 优秀' if score >= 90 else '🟡 良好' if score >= 70 else '🟠 需改进' if score >= 50 else '🔴 严重'}")
