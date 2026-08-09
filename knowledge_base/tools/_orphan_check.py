import os, re
from collections import Counter
WIKI='wiki'; SKIP={'.obsidian','__pycache__','tools'}
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
for k,v in Counter('/'.join(f.split('/')[:2]) for f in orphans).most_common():
    print(f"  {v:>4}  {k}")
