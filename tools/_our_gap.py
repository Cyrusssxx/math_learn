# -*- coding: utf-8 -*-
# 计算：大观园真题线代 328 道（数二可用）中，我们库覆盖多少、缺多少
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

RE_TRACE = re.compile(r'[（(]?\s*(19|20)\d\d\s*[）)]?\s*[，,；;]?\s*(数学[一二三]|数[一二三])')
target = [q for q in qs if assign(q) is not None and RE_TRACE.search(str(q.get('source') or '')) and assign(q) != 8]
print('大观园真题线代（数二可用）:', len(target))

def norm(t):
    s = re.sub(r'\s+', '', str(t or '')).replace('$', '')
    s = re.sub(r'\\dfrac|\\tfrac', r'\\frac', s)
    s = re.sub(r'\\left|\\right|\\!|\\,', '', s)
    return s

# 我们库：xd_bank + exam.json + core_bank + bank_questions
our = []
for f, path in (('xd', 'pwa/data/xd_bank.json'), ('exam', 'pwa/data/exam.json'),
                ('core', 'pwa/data/core_bank.json')):
    d = json.load(io.open(path, encoding='utf-8'))
    if f == 'exam':
        for v in d:
            for s in v.get('sections', []):
                for q in s.get('questions', []):
                    our.append((f, q))
    elif isinstance(d, list):
        for v in d:
            for s in v.get('sections', []):
                for q in s.get('questions', []):
                    our.append((f, q))
    else:
        for s in d.get('sections', []):
            for q in s.get('questions', []):
                our.append((f, q))
try:
    bq = json.load(io.open('pwa/data/bank_questions.json', encoding='utf-8'))
    its = bq.get('items') if isinstance(bq, dict) else bq
    for q in its:
        our.append(('bank', q))
except Exception as e:
    print('bank 读取失败', e)

print('我们库题量（xd+exam+core+bank）:', len(our))
our_exact = set()
our_pref = set()
for _, q in our:
    n = norm(q.get('stem'))
    if len(n) >= 12:
        our_exact.add(n)
        our_pref.add(n[:34])

hit, miss = [], []
for q in target:
    n = norm(q.get('stem'))
    if len(n) < 12:
        continue
    if n in our_exact or n[:34] in our_pref:
        hit.append(q)
    else:
        miss.append(q)
print()
print('✅ 我们已有: %d' % len(hit))
print('❌ 我们缺失: %d' % len(miss))
c = Counter(XL2[assign(q)] for q in miss)
print('缺失分布:', dict(c))
c2 = Counter(XL2[assign(q)] for q in hit)
print('已有分布:', dict(c2))
print()
print('缺失样本 12:')
for q in miss[:12]:
    print('  serial=%-6s %-30s %s' % (q.get('serial'), str(q.get('source'))[:30], norm(q.get('stem'))[:56]))