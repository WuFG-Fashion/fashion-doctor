"""
知识库索引自动更新脚本
=============================
功能：扫描 knowledge_base/ 下所有文件，自动更新 master_index.json
用途：每次新增知识库内容后运行，保持索引同步

用法：
    python kb_updater.py          # 扫描并更新
    python kb_updater.py --dry   # 仅显示差异，不写入
    python kb_updater.py --show  # 显示当前索引内容
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

KB_ROOT = Path(os.environ.get("KB_ROOT") or Path(__file__).resolve().parents[1])  # knowledge_base/ 根：KB_ROOT 环境变量优先，默认按脚本位置推导（修复：此前误用 parent 指向 tools/）
INDEX_FILE = KB_ROOT / "90_meta" / "__index__" / "master_index.json"

# ── L2 品类映射（目录名 → 品类信息）─────────────────
L2_MAP = {
    "L2_00_AI前沿信息":                  {"id": "L2_00", "name": "AI前沿信息",             "desc": "AI前沿、行业大模型、零售AI工具"},
    "L2_01_零售基础理论":                {"id": "L2_01", "name": "零售基础理论",           "desc": "KPI体系、数据模型、零售术语、行业基准"},
    "L2_02_竞品分析":                    {"id": "L2_02", "name": "竞品分析",               "desc": "太平鸟/GXG/MLB/速写数据对比"},
    "L2_03_会员与VIP运营":               {"id": "L2_03", "name": "会员与VIP运营",          "desc": "会员体系设计、RFM分层、VIP运营"},
    "L2_04_导购能力评估":                {"id": "L2_04", "name": "导购能力评估",           "desc": "导购能力模型、销售话术、人效评估"},
    "L2_05_商品企划":                    {"id": "L2_05", "name": "商品企划",               "desc": "OTB管理、波段上货、商品生命周期"},
    "L2_06_数据分析实务":                {"id": "L2_06", "name": "数据分析实务",           "desc": "数据分析方法、指标口径、看板实务"},
    "L2_07_服装多品牌数据分析系统构建":   {"id": "L2_07", "name": "多品牌数据分析系统构建", "desc": "多品牌系统架构、ETL、RAG基建"},
}

# ── 支持的文件类型 ───────────────────────────────────
SUPPORTED_EXTS = {".md", ".xlsx", ".xls", ".csv", ".pdf", ".png", ".jpg", ".jpeg", ".pptx", ".txt"}

# ── wiki/ 新架构映射（子目录 → 目录信息）──────────────
WIKI_MAP = {
    "sources":     {"id": "WIKI_S", "name": "来源库",         "desc": "采集来源摘要页（每篇一个 source）", "type": "source"},
    "entities":    {"id": "WIKI_E", "name": "实体库",         "desc": "品牌/公司/人物/产品实体页", "type": "entity"},
    "concepts":    {"id": "WIKI_C", "name": "概念库",         "desc": "方法论/术语/指标体系概念页", "type": "concept"},
    "comparisons": {"id": "WIKI_P", "name": "对比库",         "desc": "跨实体/跨品牌对比分析页", "type": "comparison"},
    "playbooks":   {"id": "WIKI_B", "name": "作战手册",       "desc": "可操作的打法/SOP/决策树", "type": "playbook"},
    "practices":   {"id": "WIKI_R", "name": "实践库",         "desc": "技术实践/落地案例页", "type": "practice"},
}

# ── v2.1 frontmatter 数据契约（specs/知识库v2架构方案_讨论稿.md §13.2）──
# layer 缺省值（仅当页面 frontmatter 未写 layer 时使用，属提示值非权威值）
LAYER_DEFAULTS = {
    "source": "T2", "entity": "T2",
    "concept": "T1", "comparison": "T1", "practice": "T1", "playbook": "T1",
}
# frontmatter 中按「key: value」单行提取的字段
CONTRACT_FIELDS = ("layer", "scope", "company", "volatility", "as_of",
                   "review_due_at", "expires_at", "status", "superseded_by", "retrieval")


def scan_kb():
    """扫描知识库目录，返回按L2/L3组织的文件清单（兼容历史 L2 架构）"""
    kb = {}
    for L2_dir in KB_ROOT.iterdir():
        if not L2_dir.is_dir() or L2_dir.name.startswith("__"):
            continue
        L2_key = L2_dir.name
        if L2_key not in L2_MAP:
            continue  # 未知目录（如 wiki/raw、_health）静默跳过，避免噪音

        L2_info = L2_MAP[L2_key]
        L3_list = []
        for L3_dir in L2_dir.iterdir():
            if not L3_dir.is_dir():
                continue
            # 找L3目录下的第一个支持的文件
            files = [f for f in L3_dir.iterdir() if f.suffix in SUPPORTED_EXTS]
            if files:
                # 取第一个文件作为代表
                main_file = sorted(files, key=lambda x: (x.suffix != ".md", x.name))[0]
                parts = L3_dir.name.split("_")
                L3_id = parts[0] + "_" + parts[1] + "_" + parts[2]  # L3_XX_NN
                L3_name = "_".join(parts[3:]) if len(parts) > 3 else parts[-1]
                L3_list.append({
                    "id": L3_id,
                    "name": L3_name,
                    "path": str(main_file.relative_to(KB_ROOT)).replace("\\", "/"),
                    "file_count": len(files),
                    "status": "ok"
                })
        if L3_list:
            kb[L2_key] = {"info": L2_info, "L3": L3_list}
    return kb


def scan_wiki():
    """扫描 wiki/ 新架构，每页一个条目（含 frontmatter 元数据）"""
    wiki_root = KB_ROOT / "30_wiki"
    if not wiki_root.is_dir():
        return {}
    wiki = {}
    total_excluded = {"retired": 0, "never": 0, "explicit_only": 0}
    for sub_name, info in WIKI_MAP.items():
        sub_dir = wiki_root / sub_name
        if not sub_dir.is_dir():
            continue
        entries = []
        for f in sorted(sub_dir.glob("*.md")):
            title = f.stem
            meta = {
                "aliases": [], "confidence": None, "brand_specific": None,
                "type": info.get("type"),
                "layer": LAYER_DEFAULTS.get(info.get("type")),  # 提示值，frontmatter 可覆写
                "scope": "public", "company": None, "volatility": None,
                "as_of": None, "review_due_at": None, "expires_at": None,
                "status": "active", "superseded_by": None, "retrieval": "eligible",
            }
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                fm = re.search(r"^---\n(.*?)\n---", text, re.S)
                if fm:
                    body = fm.group(1)
                    am = re.search(r"^aliases:\s*(\[.*?\]|.+)$", body, re.M)
                    if am:
                        raw = am.group(1).strip()
                        aliases = re.findall(r'"([^"]+)"|\'([^\']+)\'', raw)
                        meta["aliases"] = [a or b for a, b in aliases] or [raw.strip("[]").strip()]
                    for key in CONTRACT_FIELDS:
                        m = re.search(rf"^{key}:\s*(.+)$", body, re.M)
                        if m:
                            val = m.group(1).strip().strip('"\'')
                            if val and val.lower() not in ("null", "none", "~", ""):
                                meta[key] = val
                    cm = re.search(r"^confidence:\s*(\S+)", body, re.M)
                    if cm:
                        meta["confidence"] = cm.group(1).strip()
                    bm = re.search(r"^brand_specific:\s*(true|false)", body, re.M)
                    if bm:
                        meta["brand_specific"] = bm.group(1) == "true"
            except Exception:
                pass
            # 个人域双保险：scope=personal 或物理路径在个人域 → 强制不可检索
            rel_posix = str(f.relative_to(KB_ROOT)).replace("\\", "/")
            if meta.get("scope") == "personal" or rel_posix.startswith("20_personal/") or "/00_inbox/" in rel_posix:
                meta["retrieval"] = "never"
            # 状态门禁：retired 不入索引（物理删除永远只由人批，这里只是不再索引）
            if meta.get("status") == "retired":
                total_excluded["retired"] += 1
                continue
            if meta.get("retrieval") == "never":
                total_excluded["never"] += 1
            elif meta.get("retrieval") == "explicit_only":
                total_excluded["explicit_only"] += 1
            entries.append({
                "id": f"{info['id']}_{sub_name}_{len(entries)}",
                "name": title,
                "path": rel_posix,
                "file_count": 1,
                "status": "ok",              # 扫描状态（沿用旧语义，勿与生命周期混淆）
                "lifecycle": meta.pop("status"),  # v2.1 生命周期状态（active/stale/expired/retired）
                **meta,
            })
        if entries:
            wiki[sub_name] = {"info": info, "L3": entries}
    wiki["__excluded__"] = total_excluded  # 供 main() 打印；build_index 会跳过
    return wiki


def build_index(kb: dict, wiki: dict = None) -> dict:
    """根据扫描结果构建新索引（含 wiki 新架构）"""
    categories = []
    total = 0
    for L2_key, data in sorted(kb.items()):
        cat = {
            "id": data["info"]["id"],
            "name": data["info"]["name"],
            "desc": data["info"]["desc"],
            "L3": data["L3"],
            "arch": "legacy"
        }
        categories.append(cat)
        total += len(data["L3"])

    wiki = wiki or {}
    for wk, data in sorted(wiki.items()):
        if wk.startswith("__"):  # __excluded__ 等统计键不入索引
            continue
        cat = {
            "id": data["info"]["id"],
            "name": data["info"]["name"],
            "desc": data["info"]["desc"],
            "L3": data["L3"],
            "arch": "wiki"
        }
        categories.append(cat)
        total += len(data["L3"])

    return {
        "kb_version": "3.1",   # v2.1 契约：条目含 lifecycle/type/layer/scope/retrieval 等字段
        "kb_root": str(KB_ROOT),
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_entries": total,
        "levels": {
            "L1": {"name": "知识库总库", "desc": "Fashion Doctor 服装零售知识库根目录"},
            "L2": {"name": "品类库", "desc": "按业务域分类（wiki 新架构；旧 L2 目录已于 2026-08-24 退役，磁盘无 L2 目录，不再索引）"},
            "L3": {"name": "专题库", "desc": "L2下的细分专题，每条内容存为一个文件"}
        },
        "field_contract": {
            "version": "v2.1",
            "source": "specs/知识库v2架构方案_讨论稿.md §13.2",
            "fields": ["type", "layer", "scope", "company", "volatility", "as_of",
                       "review_due_at", "expires_at", "lifecycle", "superseded_by", "retrieval"],
            "gating": "lifecycle in (expired,retired) 或 retrieval in (never,explicit_only) 的条目，检索默认不召回"
        },
        "L2_categories": categories,
        "retrieval_module": {
            "path": "knowledge_base/retrieval_mod.py",
            "desc": "检索主模块，含5种内容类型提取器"
        }
    }


def main():
    dry = "--dry" in sys.argv
    show = "--show" in sys.argv

    if show:
        if INDEX_FILE.exists():
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                idx = json.load(f)
            print(json.dumps(idx, ensure_ascii=False, indent=2))
        else:
            print("❌ 索引文件不存在")
        return

    print("🔍 扫描知识库目录...")
    kb = scan_kb()
    wiki = scan_wiki()

    print(f"\n📊 扫描结果（legacy L2 {sum(len(v['L3']) for v in kb.values())} 条 + wiki {sum(len(v['L3']) for k, v in wiki.items() if not k.startswith('__'))} 条）：")
    for L2_key, data in sorted(kb.items()):
        print(f"  {data['info']['name']} ({len(data['L3'])}个L3)")
        for L3 in data["L3"]:
            print(f"    └─ {L3['name']} ({L3['file_count']}文件)")
    for wk, data in sorted(wiki.items()):
        if wk.startswith("__"):
            continue
        print(f"  [wiki] {data['info']['name']} ({len(data['L3'])}个条目)")
        for L3 in data["L3"][:5]:
            print(f"    └─ {L3['name']} ({L3['file_count']}文件)")
        if len(data["L3"]) > 5:
            print(f"    … 等 {len(data['L3'])} 个")
    excl = wiki.get("__excluded__", {})
    if any(excl.values()):
        print(f"\n🚫 门禁排除：retired 不入索引 {excl['retired']} 条 | retrieval=never {excl['never']} 条 | explicit_only {excl['explicit_only']} 条")

    new_index = build_index(kb, wiki)

    if dry:
        print("\n🔍 [DRY模式] 不写入，仅显示差异：")
        print(json.dumps(new_index, ensure_ascii=False, indent=2))
        return

    # 写入
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(new_index, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 索引已更新：{new_index['total_entries']} 个L3条目，{datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
