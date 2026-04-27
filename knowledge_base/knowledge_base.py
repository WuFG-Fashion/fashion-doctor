"""
Fashion Doctor 知识库 CLI 入口
用法：
  python knowledge_base.py <查询词> [--type md|pdf|excel|image|ppt|link] [--top-k N]
  python knowledge_base.py --list [L2_id]
  python knowledge_base.py --stat
  python knowledge_base.py --interactive
  python knowledge_base.py --add <L2_id> <L3_name> <content_file>
"""
import sys
import os

# 将 knowledge_base 目录加入路径
KB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KB_DIR)

from retrieval_mod import retrieve, load_index, search_index, add_kb_entry

def cmd_list(l2_filter=None):
    """列出知识库所有条目"""
    index = load_index()
    cats = index.get("L2_categories", [])
    print(f"\n{'='*50}")
    print(f"Fashion Doctor 知识库  (共 {index.get('total_entries', 0)} 条)")
    print(f"{'='*50}")
    for cat in cats:
        entries = cat.get("L3", [])
        print(f"\n[L2] {cat['id']}  {cat.get('name', '')}  ({len(entries)} 条)")
        for e in entries:
            print(f"    {e['id']}  {e['name']}  ({e.get('status','md')})")
    print()


def cmd_stat():
    """统计摘要"""
    index = load_index()
    cats = index.get("L2_categories", [])
    total = index.get("total_entries", 0)
    print(f"\n知识库统计")
    print(f"  总条目: {total}")
    print(f"  L2分类: {len(cats)}")
    for cat in cats:
        entries = cat.get("L3", [])
        print(f"    {cat.get('name','?')} ({len(entries)} 条)")
    print()


def cmd_search(query, content_type=None, top_k=3):
    """检索知识库"""
    r = retrieve(query, content_type=content_type, top_k=top_k)
    r.print_summary()
    return r


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--list" in args:
        cmd_list()
        return

    if "--stat" in args:
        cmd_stat()
        return

    if "--interactive" in args:
        print("🔍 Fashion Doctor 知识库（交互模式）")
        print("输入查询内容，或按 Ctrl+C 退出\n")
        try:
            while True:
                q = input("查询> ").strip()
                if not q:
                    continue
                if q in ("exit", "quit", "q"):
                    break
                cmd_search(q)
        except (KeyboardInterrupt, EOFError):
            print("\n退出")
        return

    # 按位置取查询词（跳过选项）
    positional = [a for a in args if not a.startswith("--")]
    if not positional:
        print("错误：请提供查询词")
        print(__doc__)
        return

    query = positional[0]
    content_type = None
    top_k = 3

    for i, a in enumerate(args):
        if a == "--type" and i + 1 < len(args):
            content_type = args[i + 1]
        if a == "--top-k" and i + 1 < len(args):
            top_k = int(args[i + 1])

    cmd_search(query, content_type=content_type, top_k=top_k)


if __name__ == "__main__":
    main()
