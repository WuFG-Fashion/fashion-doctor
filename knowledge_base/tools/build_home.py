# -*- coding: utf-8 -*-
# Home.md 生成器（T4 视图层）：扫描 v2.1 八分区物理树，产出带实时计数的 Home.md。
# 规则（specs/知识库v2架构方案_讨论稿.md §3 T4）：视图全脚本生成、人只改模板（本脚本），禁止手改 Home.md。
import io, os
from datetime import date

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.join(KB, "Home.md")


def count_md(rel):
    d = os.path.join(KB, rel)
    if not os.path.isdir(d):
        return 0
    n = 0
    for dp, _dns, fs in os.walk(d):
        n += sum(1 for f in fs if f.endswith(".md"))
    return n


def main():
    c = {
        "sources": count_md("30_wiki/sources"),
        "entities": count_md("30_wiki/entities"),
        "concepts": count_md("30_wiki/concepts"),
        "comparisons": count_md("30_wiki/comparisons"),
        "practices": count_md("30_wiki/practices"),
        "playbooks": count_md("30_wiki/playbooks"),
        "raw": count_md("10_web/articles"),
        "inbox": count_md("00_inbox"),
        "courseware": count_md("40_companies/dongshang/06_培训课件"),
        "legacy": count_md("50_legacy"),
    }
    today = date.today().isoformat()
    lines = [
        "---",
        "title: Fashion Doctor 知识库",
        "type: view",
        "layer: T4",
        "scope: public",
        "retrieval: explicit_only",
        "status: active",
        "generated_by: tools/build_home.py",
        "generated_at: %s" % today,
        "---",
        "",
        "# 🏠 Fashion Doctor 知识库",
        "",
        "> 服装连锁门店运营知识库 · v2.1 八分区架构（2026-09-12 物理落地）",
        "> **本页由 `tools/build_home.py` 生成（T4 视图层），禁止手改**——改结构请改脚本。",
        "",
        "## 编译层（30_wiki · 机器写）",
        "",
        "| 库 | 说明 | 页数 |",
        "|---|---|---|",
        "| 来源摘要 sources | 每篇 10_web 原料的结构化摘要 | %d |" % c["sources"],
        "| 品牌实体 entities | 品牌/公司/人物实体页 | %d |" % c["entities"],
        "| 核心概念 concepts | KPI/方法论/术语 | %d |" % c["concepts"],
        "| 对比分析 comparisons | 跨品牌横向对比（S 轮合成） | %d |" % c["comparisons"],
        "| 实践方法 practices | 可落地的技术实践 | %d |" % c["practices"],
        "| 作战手册 playbooks | SOP/决策树/复盘模板 | %d |" % c["playbooks"],
        "",
        "语义导航总图：[[index]] ｜ 全局综述：[[overview]]",
        "",
        "## 分区地图",
        "",
        "| 分区 | 内容 | 页数/说明 |",
        "|---|---|---|",
        "| `00_inbox/` | 临时收集（老板随手丢，周五提炼） | %d 篇 |" % c["inbox"],
        "| `10_web/` | 网络采集原料层 | %d 篇 |" % c["raw"],
        "| `20_personal/` | 个人知识沉淀（retrieval:never，不进 RAG） | 私密 |",
        "| `brand_wall/` | 品牌墙（35 focus_brands 共享参考层） | 见 kb_benchmarks.json |",
        "| `40_companies/dongshang/` | 东尚公司域（制度/课件/语义层） | 课件 %d 篇 |" % c["courseware"],
        "| `50_legacy/` | 历史归档（MOC/L3 死层，只读） | %d 篇 |" % c["legacy"],
        "| `90_meta/` | 索引/健康快照/日志 | log.md + __index__ + _health |",
        "",
        "## 精选入口",
        "",
        "- **行业格局**：[[服装行业竞争格局]]（实体/概念/对比的总枢纽）",
        "- **双核对照**：[[core_brands_peacebird_cabbeen_2026]] ｜ [[peacebird]] ｜ [[cabbeen]]",
        "- **怎么干**：[[清仓决策树]] ｜ [[季初订货节奏]] ｜ [[导购培训SOP]]",
        "- **规则手册**：[[CLAUDE]]（命名/链接/ingest 流程，T0 只能人改）",
        "",
        "## 快速开始",
        "",
        "1. **查某个品牌** → [[index]] 或直接 `Ctrl/Cmd + O` 搜品牌名",
        "2. **查方法论** → 30_wiki/concepts + playbooks",
        "3. **看跨品牌模式** → 30_wiki/comparisons（每周日 S 轮合成）",
        "4. **看知识图谱** → 左上角「图谱」按钮",
        "",
        "---",
        "",
        "*生成时间：%s · by tools/build_home.py（T4 视图，人只改模板）*" % today,
        "",
    ]
    with io.open(HOME, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print("Home.md regenerated:", c)


if __name__ == "__main__":
    main()
