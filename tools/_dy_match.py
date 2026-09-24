# -*- coding: utf-8 -*-
# 单归属计数 + 多子集搜索，精确命中截图 30/78/45/75/59/40（总327）
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
    """每题只归一个 L2：取最深的线代祖先（并列取 id 最小），无线代则 None"""
    best = None
    for c in (q.get('categoryIds') or []):
        if not str(c).isdigit():
            continue
        ch = anc(int(c))
        if 1 not in ch:
            continue
        for cid in ORDER:
            if cid in ch:
                depth = ch.index(cid)
                if best is None or depth > best[0] or (depth == best[0] and cid < best[1]):
                    best = (depth, cid)
    return best[1] if best else None

def bd(subset, label, show=True):
    c = Counter()
    n = 0
    for q in subset:
        a = assign(q)
        if a is None:
            continue
        c[a] += 1
        n += 1
    row = [c.get(cid, 0) for cid in ORDER]
    if show:
        print('%-28s 总=%4d | ' % (label, n) + ' '.join('%s=%d' % (XL2[oid], c.get(oid, 0)) for oid in ORDER))
    return n, row

TARGET = [30, 78, 45, 75, 59, 40]
print('%-28s 总= 327 | ' % '★截图目标' + ' '.join('%s=%d' % (XL2[oid], t) for oid, t in zip(ORDER, TARGET)))
print()

def is_zhenti(s):
    s = str(s or '')
    if re.search(r'880|900|姜晓千|李永乐|张宇|李艳芳|强化|基础|题源|模拟|冲刺|套|习题', s):
        return False
    return bool(re.search(r'(19|20)\d\d', s))

allx = [q for q in qs if assign(q) is not None]
bd(allx, 'A 全部线代')
MATH1_ONLY = XL2.get(8)  # 数学一专项
zt = [q for q in allx if is_zhenti(q.get('source'))]
bd(zt, 'B 真题(年份source,全科目)')
bd([q for q in zt if assign(q) != 8], 'B2 真题(排数学一专项)')

# 真题：source 形如 (YYYY 数X) / YYYY 数X（严格）
def zt_strict(s):
    s = str(s or '').strip()
    return bool(re.match(r'^[（(]?\s*(19|20)\d\d\s*[）)]?\s*[，,]?\s*(数[一二三]|数学[一二三]|数[一二三、，,]+)*\s*[）)]?\s*$', s))
bd([q for q in allx if zt_strict(q.get('source'))], 'C 真题(严格正则)')

print()
print('--- 与目标逐项差（B 真题全科目）---')
n, row = bd(zt, 'B 真题(年份source,全科目)', show=False)
print('B:', n, row)
print('目标:', sum(TARGET), TARGET)
print('差:', [t - r for t, r in zip(TARGET, row)])