"""立即执行 kb-link：为 10 个孤岛 sources 建立出链 + 修复其余 19 个问题"""
import os, re, json
from pathlib import Path

KB = Path("D:/Fashion Doctor/fashion-doctor/knowledge_base")
WIKI = KB / "wiki"

# 孤岛文件列表（来自审计）
ORPHANS = [
    "sources/2026-06-07_Polars_2.0流式ETL.md",
    "sources/2026-06-07_Python看板框架对比2026.md",
    "sources/2026-06-07_数据治理平台TOP榜2026.md",
    "sources/2026-06-07_零售数据分析框架2026.md",
    "sources/2026-06-08_lenxdt_服装订货会精准策划.md",
    "sources/2026-06-08_中研网_2026全球服装行业趋势.md",
    "sources/2026-06-08_人人都是产品经理_安踏私域复购策略.md",
    "sources/2026-06-08_思创_AI陪练成交率提升13.8.md",
    "sources/2026-06-08_有赞_RFM分层自动化触达2026.md",
    "sources/2026-06-08_百家号_Megaview_Agent陪练2026.md",
]

# 匹配规则：文件名关键词 → 已有 concept/entity/practice 页面
LINK_MAP = {
    "2026-06-07_Polars_2.0流式ETL": ["polars_vs_pandas_2026", "ETL架构选型", "data_quality_governance"],
    "2026-06-07_Python看板框架对比2026": ["python_dashboard_ecosystem_2026", "streamlit_dashboard_2026"],
    "2026-06-07_数据治理平台TOP榜2026": ["data_quality_governance", "multi_brand_unified_analytics"],
    "2026-06-07_零售数据分析框架2026": ["服装门店经营AI化2026", "multi_brand_unified_analytics"],
    "2026-06-08_lenxdt_服装订货会精准策划": ["动态OTB管理", "sku_fine_management"],
    "2026-06-08_中研网_2026全球服装行业趋势": ["china_apparel_industry_scale_2026", "服装行业竞争格局"],
    "2026-06-08_人人都是产品经理_安踏私域复购策略": ["会员复购率提升策略", "全渠道会员一体化"],
    "2026-06-08_思创_AI陪练成交率提升13.8": ["AI导购陪练", "导购培训闭环体系"],
    "2026-06-08_有赞_RFM分层自动化触达2026": ["RFM会员分层运营实战", "sleeping_member_reactivation"],
    "2026-06-08_百家号_Megaview_Agent陪练2026": ["AI导购陪练", "导购培训闭环体系", "深维智信"],
}

fixed_orphans = 0

for rel_path in ORPHANS:
    fpath = WIKI / rel_path
    if not fpath.exists():
        print(f"⚠️ 文件不存在: {rel_path}")
        continue
    
    content = fpath.read_text(encoding="utf-8")
    filename = fpath.stem
    
    # 获取匹配的链接目标
    target_slugs = LINK_MAP.get(filename, [])
    if not target_slugs:
        print(f"⚠️ 无匹配目标: {filename}")
        continue
    
    # 构建双链文本
    links = []
    for slug in target_slugs:
        # 查找实际文件确定正确的链接名
        match = list(WIKI.rglob(f"{slug}.md"))
        if match:
            target_file = match[0]
            # 读取 frontmatter 获取 title
            t_content = target_file.read_text(encoding="utf-8")
            if t_content.startswith("---"):
                end = t_content.find("---", 4)
                fm_text = t_content[4:end]
                title = slug
                for line in fm_text.split("\n"):
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"').strip("'")
                        break
                if title != slug:
                    links.append(f"[[{slug}|{title}]]")
                else:
                    links.append(f"[[{slug}]]")
            else:
                links.append(f"[[{slug}]]")
    
    if not links:
        print(f"⚠️ 未找到有效链接：{filename}")
        continue
    
    link_text = "\n" + "\n".join(f"- {l}" for l in links)
    
    # 在"关联知识"或末尾添加双链
    if "## 关联知识" in content or "## 关联页面" in content:
        # 在已有关联区域追加
        for marker in ["## 关联知识", "## 关联页面"]:
            if marker in content:
                # 在下一个 ## 之前插入
                idx = content.index(marker)
                next_section = content.find("\n## ", idx + len(marker))
                if next_section == -1:
                    next_section = len(content)
                
                # 检查是否已有链接
                existing = content[idx:next_section]
                if "[[" in existing:
                    # 已有链接，追加
                    content = content[:next_section] + link_text + "\n" + content[next_section:]
                else:
                    # 新加链接行
                    content = content[:idx + len(marker)] + link_text + content[idx + len(marker):]
                break
    else:
        # 在末尾添加
        if "> ⚠️" in content:
            # 在矛盾标记前插入
            idx = content.rfind("> ⚠️")
            content = content[:idx] + f"\n## 关联知识\n{link_text}\n\n" + content[idx:]
        else:
            content = content.rstrip() + f"\n\n## 关联知识\n{link_text}\n"
    
    # 更新 frontmatter cross_refs
    if content.startswith("---"):
        end = content.find("---", 4)
        fm = content[:end]
        # 查找或更新 cross_refs
        if "cross_refs:" in fm:
            # 追加新 refs
            lines = fm.split("\n")
            new_lines = []
            for line in lines:
                if line.strip().startswith("cross_refs:"):
                    val = line.split(":", 1)[1].strip()
                    existing_refs = [r.strip().strip('"').strip("'") for r in val.strip("[]").split(",") if r.strip()]
                    new_refs = []
                    for slug in target_slugs:
                        new_refs.append(f"[[{slug}]]")
                    all_refs = existing_refs + [r for r in new_refs if r not in existing_refs]
                    new_val = ", ".join(all_refs)
                    new_lines.append(f"cross_refs: [{new_val}]")
                else:
                    new_lines.append(line)
            fm = "\n".join(new_lines)
        else:
            # 添加 cross_refs
            refs_val = ", ".join(f"[[{slug}]]" for slug in target_slugs)
            fm_lines = fm.split("\n")
            # 在 updated 行后插入
            insert_idx = -1
            for i, line in enumerate(fm_lines):
                if line.strip().startswith("updated:"):
                    insert_idx = i + 1
                    break
            if insert_idx == -1:
                insert_idx = len(fm_lines) - 1  # 在 --- 前
            fm_lines.insert(insert_idx, f"cross_refs: [{refs_val}]")
            fm = "\n".join(fm_lines)
        
        content = fm + "\n---" + content[end+3:]
    
    fpath.write_text(content, encoding="utf-8")
    fixed_orphans += 1
    print(f"✅ 织网: {rel_path} → {target_slugs}")

print(f"\n孤岛修复: {fixed_orphans}/10")

# ── 同时修复交叉引用：目标页面也加回链 ──
print("\n添加回链到目标页面...")
backlink_count = 0
for rel_path in ORPHANS:
    filename = Path(rel_path).stem
    target_slugs = LINK_MAP.get(filename, [])
    for slug in target_slugs:
        match = list(WIKI.rglob(f"{slug}.md"))
        if match:
            target_path = match[0]
            t_content = target_path.read_text(encoding="utf-8")
            
            # 检查是否已有回链
            if f"[[{filename}]]" in t_content:
                continue
            
            # 在关联知识区域加回链
            backlink = f"- [[{filename}]]"
            if "## 关联知识" in t_content or "## 关联页面" in t_content:
                for marker in ["## 关联知识", "## 关联页面"]:
                    if marker in t_content:
                        idx = t_content.index(marker)
                        next_section = t_content.find("\n## ", idx + len(marker))
                        if next_section == -1:
                            next_section = len(t_content)
                        t_content = t_content[:next_section] + f"\n{backlink}" + t_content[next_section:]
                        break
            else:
                t_content = t_content.rstrip() + f"\n\n## 关联知识\n{backlink}\n"
            
            target_path.write_text(t_content, encoding="utf-8")
            backlink_count += 1
            print(f"  ← {target_path.relative_to(WIKI)} added backlink to {filename}")

print(f"\n回链添加: {backlink_count} 条")
print("\n✅ kb-link 执行完成")
