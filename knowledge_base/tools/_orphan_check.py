import os, re, sys
from collections import Counter
from pathlib import Path
# 解析为 knowledge_base/wiki 的绝对路径，避免依赖调用方 cwd（仓库根 vs knowledge_base 目录）
WIKI = str(Path(__file__).resolve().parents[1] / 'wiki')
SKIP={'.obsidian','__pycache__','tools'}
if not os.path.isdir(WIKI):
    sys.exit(f"[orphan_check] wiki 目录不存在: {WIKI}")
lp=re.compile(r'\[\[([^\]|#\n]+?)(?:\||#|\]\])')
def norm(t):
    t=t.strip()
    return t[:-3] if t.endswith('.md') else t
allf=set(); targets=set()
for dp,dns,fns in os.walk(WIKI):
    dns[:]=[d for d in dns if d not in SKIP]
    for fn in fns:
        if not fn.endswith('.md'): continue
        p=os.path.join(dp,fn).replace(os.sep,'/'); allf.add(p)
        try: s=open(p,encoding='utf-8').read()
        except: continue
        targets.update(norm(t) for t in lp.findall(s))
resolved={norm(t) for t in targets}
orphans=[]
for f in allf:
    b=norm(os.path.basename(f)[:-3])
    if b not in resolved and b[2:] not in resolved:
        orphans.append(f)
print(f"wiki/ 总文件: {len(allf)}")
print(f"wiki/ 无入链(孤岛): {len(orphans)}  ({len(orphans)/len(allf)*100:.1f}%)")
print(f"wiki/ 入链覆盖率: {(len(allf)-len(orphans))/len(allf)*100:.1f}%")
print("\n孤岛按目录:")
base = WIKI.replace(os.sep, '/')
for k,v in Counter(f.replace(base+'/','').split('/')[0] for f in orphans).most_common():
    print(f"  {v:>4}  wiki/{k}")
if orphans:
    print("\n孤岛清单(最多20条):")
    for f in sorted(orphans)[:20]:
        print("  -", f.replace(base+'/',''))
