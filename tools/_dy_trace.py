# -*- coding: utf-8 -*-
# 按「source 含 (YYYY 数X) 溯源」重算真题子集，精确对齐截图 30/78/45/75/59/40
import json, io, re
from collections import Counter

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))['items']
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))['items']
node = {int(n['id']): n for n in cats}

def anc(nid):
    out, cur, g = [], nid, 0
    while cur is not None and g < 20:
        out.append(cur)
        p = node.get(cur, {}).get('parentId')
        cur = int(p) if p is not None else None
        g += 1
    return out

XL2 = {int(n['id']): n['name'] for n in cats if int(n.get('parentId') or 0) == 1}
ORDER = sorted(XL2)

def assign(q):
    best = None
    for c in (q.get('categoryIds') or []):
        if not str(c).isdigit():
            continue
        ch = anc(int(c))
        if 1 not in ch:
            continue
        for cid in ORDER:
            if cid in ch:
                d = ch.index(cid)
                if best is None or d > best[0] or (d == best[0] and cid < best[1]):
                    best = (d, cid)
    return best[1] if best else None

def bd(subset, label):
    c = Counter()
    n = 0
    for q in subset:
        a = assign(q)
        if a is None:
            continue
        c[a] += 1
        n += 1
    print('%-30s 总=%4d | ' % (label, n) + ' '.join('%s=%d' % (XL2[o], c.get(o, 0)) for o in ORDER))
    return n, [c.get(o, 0) for o in ORDER]

TARGET = [30, 78, 45, 75, 59, 40]
print('%-30s 总= 327 | ' % '★截图目标' + ' '.join('%s=%d' % (XL2[o], t) for o, t in zip(ORDER, TARGET)))
print()

allx = [q for q in qs if assign(q) is not None]
# 溯源真题：source 中含 "(YYYY 数X)" 或 "YYYY 数X"（年份后紧跟科目标记）
RE_TRACE = re.compile(r'[（(]?\s*(19|20)\d\d\s*[）)]?\s*[，,；;]?\s*(数学[一二三]|数[一二三])')

bd(allx, 'A 全部线代')
tr = [q for q in allx if RE_TRACE.search(str(q.get('source') or ''))]
bd(tr, 'B 溯源真题(含880溯源)')
bd([q for q in tr if assign(q) != 8], 'B2 溯源真题(排数学一专项)')
# 只看 学一专项 之外的
bd([q for q in allx if RE_TRACE.search(str(q.get('source') or '')) and '880' not in str(q.get('source') or '') and '900' not in str(q.get('source') or '')],
   'C 溯源真题(排880/900)')
# 数二口径
def m2(s):
    s = str(s or '')
    return ('数二' in s) or (('数一' not in s) and ('数三' not in s))
bd([q for q in tr if m2(q.get('source'))], 'D 溯源真题∩数二口径')