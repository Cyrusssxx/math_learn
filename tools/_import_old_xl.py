# -*- coding: utf-8 -*-
# 导入：大观园老年份(<=1999)数一/数三线代真题 109 道 → xd_bank.json
import json, io, re, shutil

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
dy_cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))['items']
dy_node = {int(n['id']): n for n in dy_cats}
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))['items']

our = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))
our_node = {int(k): v for k, v in our.items()}

def our_anc(nid):
    out, cur, g = [], nid, 0
    while cur is not None and g < 10:
        out.append(cur)
        p = our_node.get(cur, {}).get('parentId')
        cur = int(p) if p is not None and str(p).isdigit() else None
        g += 1
    return out

our_xl = {nid for nid in our_node if 1 in our_anc(nid)}

def dy_anc(nid):
    out, cur, g = [], nid, 0
    while cur is not None and g < 12:
        out.append(cur)
        p = dy_node.get(cur, {}).get('parentId')
        cur = int(p) if p is not None else None
        g += 1
    return out

XL2 = {int(n['id']): n['name'] for n in dy_cats if int(n.get('parentId') or 0) == 1}
ORDER = sorted(XL2)

def assign_l2(q):
    best = None
    for c in (q.get('categoryIds') or []):
        if not str(c).isdigit():
            continue
        ch = dy_anc(int(c))
        if 1 not in ch:
            continue
        for cid in ORDER:
            if cid in ch:
                d = ch.index(cid)
                if best is None or d > best[0] or (d == best[0] and cid < best[1]):
                    best = (d, cid)
    return best[1] if best else None

def map_cids(q):
    """大观园 categoryIds → 我们节点（同 id 存在则用；否则沿父链上溯到我们最近的节点）"""
    out = []
    for c in (q.get('categoryIds') or []):
        if not str(c).isdigit():
            continue
        c = int(c)
        for cand in dy_anc(c):
            if cand in our_xl:
                if cand not in out:
                    out.append(cand)
                break
    if not out:
        l2 = assign_l2(q)
        if l2:
            out = [l2]
    return out

RE_TRACE = re.compile(r'[（(]?\s*(19|20)\d\d\s*[）)]?\s*[，,；;]?\s*(数学[一二三]|数[一二三])')
target = [q for q in qs if assign_l2(q) is not None and RE_TRACE.search(str(q.get('source') or '')) and assign_l2(q) != 8]

def norm(t):
    s = re.sub(r'\s+', '', str(t or '')).replace('$', '')
    s = re.sub(r'\\dfrac|\\tfrac', r'\\frac', s)
    s = re.sub(r'\\left|\\right|\\!|\\,', '', s)
    return s

our_all = []
for path in ('pwa/data/xd_bank.json', 'pwa/data/exam.json', 'pwa/data/core_bank.json'):
    d = json.load(io.open(path, encoding='utf-8'))
    if isinstance(d, list):
        for v in d:
            for s in v.get('sections', []):
                for q in s.get('questions', []):
                    our_all.append(q)
bq = json.load(io.open('pwa/data/bank_questions.json', encoding='utf-8'))
for q in (bq.get('items') if isinstance(bq, dict) else bq):
    our_all.append(q)
our_pref = set()
for q in our_all:
    n = norm(q.get('stem'))
    if len(n) >= 12:
        our_pref.add(n[:34])

def year_of(src):
    m = re.search(r'[（(]?\s*((?:19|20)\d\d)', str(src or ''))
    return int(m.group(1)) if m else None

old = [q for q in target
       if len(norm(q.get('stem'))) >= 12 and norm(q.get('stem'))[:34] not in our_pref
       and (year_of(q.get('source')) or 9999) <= 1999]
print('待导入老年份题:', len(old))

# serial 冲突检查
xd = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
xq = [q for s in xd[0]['sections'] for q in s['questions']]
exist_no = set(str(q['no']) for q in xq)
conflict = [q for q in old if str(q['serial']) in exist_no]
print('serial 冲突:', len(conflict), [q['serial'] for q in conflict][:10])

new_qs = []
for q in old:
    if str(q['serial']) in exist_no:
        continue
    new_qs.append({
        'no': str(q['serial']),
        'stem': q.get('stem') or '',
        'options': q.get('options') or [],
        'answer': q.get('answer') or '',
        'idea': q.get('explanation') or '',
        'source': q.get('source') or '',
        'categoryIds': map_cids(q),
    })
print('生成新条目:', len(new_qs))
nocid = [q['no'] for q in new_qs if not q['categoryIds']]
print('无 catId 的:', len(nocid), nocid[:10])
# catId 分布
from collections import Counter
c = Counter(cid for q in new_qs for cid in q['categoryIds'])
print('catId 分布:', dict(c))

# 追加为新 section
shutil.copy('pwa/data/xd_bank.json', 'pwa/data/xd_bank.json.bak')
xd[0]['sections'].append({
    'title': '数一/数三线代真题（1987-1999·数二考纲通用）',
    'questions': new_qs,
})
with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as fp:
    json.dump(xd, fp, ensure_ascii=False, separators=(',', ':'))
print('已写入 xd_bank.json')
d2 = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
print('写入后总题数:', sum(len(s['questions']) for s in d2[0]['sections']))