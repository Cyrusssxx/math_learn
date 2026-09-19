# -*- coding: utf-8 -*-
"""应用 catId 修正表：把题库中错配的知识点改为「由大观园细分类标签反推」的正确知识点。"""
import json, io
from collections import Counter

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = json.load(io.open('D:/ai code/math-note/tools/_catid_fix.json', encoding='utf-8'))
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))


def l2name(cid):
    v = cats.get(str(cid), {})
    p = cats.get(str(v.get('parentId')), {})
    return '%s / %s' % (p.get('display') or p.get('name') or '?', v.get('display') or v.get('name') or '?')


# ---------- core_bank ----------
P = BASE + 'core_bank.json'
d = json.load(io.open(P, encoding='utf-8'))
before = Counter()
after = Counter()
hit = 0
for s in d[0]['sections']:
    for q in s['questions']:
        cat = str(q.get('catId'))
        before[cat] += 1
        new = FIX['core'].get(str(q.get('no')))
        if new:
            q['catId'] = int(new) if str(new).isdigit() else new
            if isinstance(q.get('categoryIds'), list):
                q['categoryIds'] = [q['catId']]
            hit += 1
        after[str(q['catId'])] += 1
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
print('core_bank 应用修正: %d 条' % hit)

# ---------- exam ----------
P2 = BASE + 'exam.json'
e = json.load(io.open(P2, encoding='utf-8'))
hit2 = 0
for vol in e:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            new = FIX['exam'].get('%s-%s' % (vol.get('id'), q.get('no')))
            if new:
                q['categoryIds'] = [int(new) if str(new).isdigit() else new]
                hit2 += 1
with io.open(P2, 'w', encoding='utf-8', newline='') as f:
    json.dump(e, f, ensure_ascii=False, separators=(',', ':'))
print('exam.json 应用修正: %d 条' % hit2)

# ---------- 题数变化（Top 变化项） ----------
print()
print('=== 知识点题数变化（前后差 ≥ 2）===')
keys = set(before) | set(after)
rows = sorted(((abs(after[k] - before[k]), k, before[k], after[k]) for k in keys), reverse=True)
n = 0
for diff, k, b, a in rows:
    if diff >= 2:
        print('  %-24s %3d → %3d (%+d)' % (l2name(k), b, a, a - b))
        n += 1
    if n >= 14:
        break

# 函数知识点专项
fn = next(k for k, v in cats.items() if v.get('level') == 2 and (v.get('display') or v.get('name')) == '函数'
          and cats[str(v.get('parentId'))].get('display') == '极限')
print()
print('「函数」知识点: %d → %d 题' % (before[str(fn)], after[str(fn)]))