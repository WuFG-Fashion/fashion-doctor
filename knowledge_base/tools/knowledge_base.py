"""
Fashion Doctor 知识库 CLI 入口
用法：
  python knowledge_base.py <查询词> [--选项]
  python knowledge_base.py --suggest        # 建议查询
  python knowledge_base.py --hot            # 热门查询
  python knowledge_base.py --list           # 列出所有条目
  python knowledge_base.py --stat           # 统计摘要
  python knowledge_base.py --interactive    # 交互模式

选项：
  --type md|pdf|excel|image|ppt|link       # 内容类型筛选
  --top-k N                                  # 每文件最多段落数（默认3）
  --json                                    # JSON格式输出
  --compact                                 # 紧凑输出

示例：
  python knowledge_base.py 未动销率
  python knowledge_base.py 太平鸟男装 --type md --json
  python knowledge_base.py VIP分层 --compact
"""
import sys
import os

# 将 knowledge_base 目录加入路径
KB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KB_DIR)

from retrieval_mod import retrieve, load_index, search_index, add_kb_entry, get_suggested_queries, get_hot_queries

def cmd_list(l2_filter=None):
    """列出知识库所有条目"""
    index = load_index()
    cats = index.get("L2_categories", [])
    print(f"\n{'='*60}")
    print(f"Fashion Doctor 知识库  (共 {index.get('total_entries', 0)} 条)")
    print(f"{'─'*60}")
    for cat in cats:
        entries = cat.get("L3", [])
        print(f"\n[L2] {cat['id']}  {cat.get('name', '')}  ({len(entries)} 条)")
        for e in entries:
            print(f"    - {e['id']}  {e['name']}")
    print()


def cmd_stat():
    """统计摘要"""
    index = load_index()
    cats = index.get("L2_categories", [])
    total = index.get("total_entries", 0)
    print(f"\n[知识库统计]")
    print(f"  版本：{index.get('kb_version', '?')}")
    print(f"  总条目：{total}")
    print(f"  L2分类：{len(cats)}")
    print()
    for cat in cats:
        entries = cat.get("L3", [])
        bar = "*" * len(entries)
        print(f"  {cat.get('name','?')} [{bar}] {len(entries)} 条")
    print()


def cmd_search(query, content_type=None, top_k=3, output_format="text"):
    """检索知识库"""
    r = retrieve(query, content_type=content_type, top_k=top_k, output_format=output_format)
    r.print_summary(format=output_format)
    return r


def cmd_suggest():
    """显示建议查询"""
    suggestions = get_suggested_queries()
    print("\n[建议查询词]")
    print(f"{'='*40}")
    for i, s in enumerate(suggestions, 1):
        print(f"  {i:2}. {s}")
    print()


def cmd_hot():
    """显示热门查询"""
    hot = get_hot_queries()
    print("\n[热门查询]")
    print(f"{'='*40}")
    for h in hot:
        bar = "*" * min(h['count'], 5)
        print(f"  {bar} [{h['count']:2}] {h['query']}")
        print(f"       -> {h['desc']}")
    print()


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return

    # 特殊命令
    if "--suggest" in args:
        cmd_suggest()
        return

    if "--hot" in args:
        cmd_hot()
        return

    if "--list" in args:
        cmd_list()
        return

    if "--stat" in args:
        cmd_stat()
        return

    if "--interactive" in args:
        print("[Fashion Doctor 知识库 - 交互模式]")
        print("提示：输入 --suggest 查看建议，输入 --hot 查看热门，或 Ctrl+C 退出\n")
        try:
            while True:
                q = input("查询> ").strip()
                if not q:
                    continue
                if q in ("exit", "quit", "q"):
                    break
                if q.startswith("--"):
                    print(f"[提示] 使用 python knowledge_base.py {q}")
                    continue
                cmd_search(q)
        except (KeyboardInterrupt, EOFError):
            print("\n退出")
        return

    # 按位置取查询词（跳过选项）
    positional = [a for a in args if not a.startswith("--")]
    if not positional:
        print("错误：请提供查询词")
        print("提示：python knowledge_base.py --suggest 查看建议查询")
        return

    query = positional[0]
    content_type = None
    top_k = 3
    output_format = "text"

    for i, a in enumerate(args):
        if a == "--type" and i + 1 < len(args):
            content_type = args[i + 1]
        if a == "--top-k" and i + 1 < len(args):
            top_k = int(args[i + 1])
        if a == "--json":
            output_format = "json"
        if a == "--compact":
            output_format = "compact"

    cmd_search(query, content_type=content_type, top_k=top_k, output_format=output_format)


if __name__ == "__main__":
    main()
