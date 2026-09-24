# -*- coding: utf-8 -*-
# 精确计算各子集的 L2 分布，定位截图的 30/78/45/75/59/40（总327）
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

xl = {nid for nid in node if 1 in anc(nid)}
XL2 = {int(n['id']): n['name'] for n in cats if int(n.get('parentId') or 0) == 1}
desc = {cid: {nid for nid in node if cid in anc(nid)} for cid in XL2}

xq = [q for q in qs if any(int(c) in xl for c in (q.get('categoryIds') or []) if str(c).isdigit())]
print('大观园线代总数:', len(xq))

def is_zhenti(q):
    s = str(q.get('source') or '').strip()
    if re.search(r'880|900|姜晓千|李永乐|张宇|李艳芳|强化|基础|题源|模拟|冲刺|套', s):
        return False
    return bool(re.match(r'^[（(]?\s*(19|20)\d\d', s))

def math_two(q):
    s = str(q.get('source') or '')
    if '数二' in s:
        return True
    return ('数一' not in s) and ('数三' not in s)

def bd(subset, label):
    c = Counter()
    for q in subset:
        for cid in XL2:
            if any(int(x) in desc[cid] for x in (q.get('categoryIds') or []) if str(x).isdigit()):
                c[cid] += 1
    print('%-26s 总=%4d | ' % (label, len(subset)) + ' '.join('%s=%d' % (XL2[cid], c.get(cid, 0)) for cid in sorted(XL2)))
    return [c.get(cid, 0) for cid in sorted(XL2)]

TARGET = [30, 78, 45, 75, 59, 40]
print('%-26s 总= 327 | ' % '★截图目标' + ' '.join('%s=%d' % (XL2[cid], t) for cid, t in zip(sorted(XL2), TARGET)))
print()

zt = [q for q in xq if is_zhenti(q)]
bd(zt, '真题(全科目)')
bd([q for q in zt if math_two(q)], '真题∩数二口径')
bd([q for q in zt if '数二' in str(q.get('source') or '')], '真题∩source含数二')
bd([q for q in zt if re.search(r'数一|数三', str(q.get('source') or ''))], '真题∩数一数三')
bd([q for q in xq if not is_zhenti(q)], '非真题(练习册/自编)')
bd([q for q in xq if math_two(q)], '数二口径(全部source)')
bd([q for q in xq if str(q.get('source') or '').strip() == ''], 'source为空')
bd([q for q in xq if q.get('core')], 'core=True')
bd([q for q in xq if not q.get('core')], 'core=False')