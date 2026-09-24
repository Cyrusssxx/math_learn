# -*- coding: utf-8 -*-
# 建树映射 + 多种子集统计，反查截图的 30/78/45/75/59/40（总 327）对应哪个筛选口径
import json, io, re
from collections import Counter

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))['items']
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))['items']

node = {}
for n in cats:
    node[int(n['id'])] = n

def ancestors(nid):
    out, cur, guard = [], nid, 0
    while cur is not None and guard < 20:
        out.append(cur)
        p = node.get(cur, {}).get('parentId')
        cur = int(p) if p is not None else None
        guard += 1
    return out

# 线代 L2（parent=1）
XL1 = 1
XL2 = {int(n['id']): n['name'] for n in cats if int(n.get('parentId') or 0) == XL1}
print('线代 L2 节点:', XL2)

# 每个 L2 的后代集合
desc = {}
for cid in XL2:
    s = set()
    for nid in node:
        if cid in ancestors(nid):
            s.add(nid)
    desc[cid] = s
print('各 L2 后代节点数:', {XL2[k]: len(v) for k, v in desc.items()})

def l2_of(q):
    out = set()
    for c in (q.get('categoryIds') or []):
        try:
            c = int(c)
        except Exception:
            continue
        for cid, s in desc.items():
            if c in s:
                out.add(cid)
    return out

xl_qs = [q for q in qs if l2_of(q)]
print()
print('挂线代（含深层子节点）的题:', len(xl_qs))

def breakdown(subset, label):
    c = Counter()
    for q in subset:
        for cid in l2_of(q):
            c[cid] += 1
    row = [c.get(cid, 0) for cid in sorted(XL2)]
    print('%-22s 总=%4d | ' % (label, len(subset)) + ' '.join('%s=%d' % (XL2[cid], c.get(cid, 0)) for cid in sorted(XL2)))
    return row

TARGET = [30, 78, 45, 75, 59, 40]
print()
print('截图目标:            总= 327 | ' + ' '.join('%s=%d' % (XL2[cid], t) for cid, t in zip(sorted(XL2), TARGET)))
print()

breakdown(xl_qs, 'A_全部线代(全科目)')

def src_kind(s):
    s = str(s or '')
    if '数学一二三' in s: return 'B_共用'
    if re.search(r'数一|数三', s): return 'C_数一数三'
    if re.search(r'数二', s): return 'A_数二'
    if re.search(r'19\d\d|20\d\d', s): return 'D_年份'
    return 'E_无标注'

# 子集
subB = [q for q in xl_qs if src_kind(q.get('source')) != 'C_数一数三']
breakdown(subB, 'B_去数一数三')
subA = [q for q in xl_qs if src_kind(q.get('source')) == 'A_数二']
breakdown(subA, 'C_仅source含数二')
subD = [q for q in xl_qs if src_kind(q.get('source')) in ('A_数二', 'D_年份')]
breakdown(subD, 'D_数二+年份')
subE = [q for q in xl_qs if src_kind(q.get('source')) == 'E_无标注']
breakdown(subE, 'E_无标注(大观园自编)')
subC = [q for q in xl_qs if src_kind(q.get('source')) == 'C_数一数三']
breakdown(subC, 'F_仅数一数三')
# 真题严格：source 形如 "(YYYY 数X)" / "YYYY 数X" / 含"真题"
def is_zhenti(s):
    s = str(s or '')
    return bool(re.search(r'真题', s)) or bool(re.fullmatch(r'[（(]?\s*(19|20)\d\d\s*[）)]?\s*(数[一二三](、[二三])?)?\s*', s.strip()))
subZ = [q for q in xl_qs if is_zhenti(q.get('source'))]
breakdown(subZ, 'G_严格真题source')
print()
print('source 类型分布(线代全量):', dict(Counter(src_kind(q.get('source')) for q in xl_qs)))