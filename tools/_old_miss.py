# -*- coding: utf-8 -*-
# Step1-2：统计老年份缺失题数量 + 看结构（大观园题 vs 我们 xd_bank 格式、线代节点映射基础）
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

def norm(t):
    s = re.sub(r'\s+', '', str(t or '')).replace('$', '')
    s = re.sub(r'\\dfrac|\\tfrac', r'\\frac', s)
    s = re.sub(r'\\left|\\right|\\!|\\,', '', s)
    return s

# 我们库
our = []
for path in ('pwa/data/xd_bank.json', 'pwa/data/exam.json', 'pwa/data/core_bank.json'):
    d = json.load(io.open(path, encoding='utf-8'))
    if isinstance(d, list):
        for v in d:
            for s in v.get('sections', []):
                for q in s.get('questions', []):
                    our.append(q)
bq = json.load(io.open('pwa/data/bank_questions.json', encoding='utf-8'))
for q in (bq.get('items') if isinstance(bq, dict) else bq):
    our.append(q)
our_set = set()
for q in our:
    n = norm(q.get('stem'))
    if len(n) >= 12:
        our_set.add(n[:34])

miss = [q for q in target if len(norm(q.get('stem'))) >= 12 and norm(q.get('stem'))[:34] not in our_set]
print('缺失总数:', len(miss))

# 老年份（1987-1999）
def year_of(src):
    m = re.search(r'[（(]?\s*((?:19|20)\d\d)', str(src or ''))
    return int(m.group(1)) if m else None

old = [q for q in miss if (year_of(q.get('source')) or 9999) <= 1999]
print('其中老年份(<=1999):', len(old))
c = Counter(XL2[assign(q)] for q in old)
print('老年份缺失分布:', dict(c))
c2 = Counter(str(q.get('source'))[:16] for q in old)
print()
print('source 分布 top15:')
for s, n in c2.most_common(15):
    print('  %-18s %d' % (s, n))
print()
print('=== 样本 3 条（大观园原始字段）===')
for q in old[:3]:
    print('serial=%s | source=%s | type=%s' % (q.get('serial'), q.get('source'), q.get('type')))
    print('  stem:', (q.get('stem') or '')[:120].replace('\n', ' '))
    print('  options:', (q.get('options') or [])[:4])
    print('  answer:', (q.get('answer') or '')[:120])
    print('  explanation:', (q.get('explanation') or '')[:150].replace('\n', ' '))
    print('  categoryIds:', q.get('categoryIds'))
    print()
print('=== 我们 exam_categories.json 线代节点 ===')
ec = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))
for nid, n in sorted(ec.items(), key=lambda kv: int(kv[0])):
    try:
        pid = int(n.get('parentId') or 0)
    except Exception:
        continue
    if int(nid) == 1 or pid in (1, 2, 3, 4, 5, 6, 7):
        print('  id=%s parent=%s name=%s' % (nid, n.get('parentId'), n.get('name')))