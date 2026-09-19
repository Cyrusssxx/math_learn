# -*- coding: utf-8 -*-
"""列出仍然「回落」的题（core 5 / exam 5）：显示原始标签、修正后归属、题干，查明原因"""
import json, io, subprocess, sys
from collections import defaultdict

BASE = 'D:/ai code/math-note/pwa/data/'
TOOLS = 'D:/ai code/math-note/tools/'
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes, l2root = deep['nodes'], deep['l2root']
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))
FIX = json.load(io.open(TOOLS + '_catid_fix.json', encoding='utf-8'))

kids = {}
for cid, v in nodes.items():
    if v['p']:
        kids.setdefault(v['p'], []).append(cid)


def subtree(root):
    out, st, seen = [], [str(root)], set()
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
        st += kids.get(x, [])
    return set(out)


SUB = {k: subtree(v) for k, v in l2root.items()}
node2l2 = defaultdict(list)
for l2, s in SUB.items():
    for n in s:
        node2l2[n].append(l2)

raw = json.load(io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
                        'daguanyuan-for-windows-main/assets/categories.json', encoding='utf-8'))
dcats = {str(x['id']): x for x in raw['items']}


def dpath(nid):
    out, cur, g = [], str(nid), 0
    while cur in dcats and g < 30:
        out.append(dcats[cur]['name'])
        p = dcats[cur].get('parentId')
        if p in (None, 0, '0'):
            break
        cur = str(p)
        g += 1
    return ' / '.join(reversed(out)) if out else '（大观园中不存在）'


def l2name(cid):
    v = cats.get(str(cid), {})
    p = cats.get(str(v.get('parentId')), {})
    return '%s / %s' % (p.get('display') or p.get('name') or '?', v.get('display') or v.get('name') or '?')


def orig(path):
    return json.loads(subprocess.run(['git', 'show', '226245b:' + path],
                                     cwd='D:/ai code/math-note', capture_output=True, text=True,
                                     encoding='utf-8').stdout)


print('=== core_bank 回落题 ===')
d = orig('pwa/data/core_bank.json')
for s in d[0]['sections']:
    for q in s['questions']:
        cat = str(FIX['core'].get(str(q['no']), q.get('catId')))
        dc = [str(x) for x in (q.get('deepCats') or [])]
        st = SUB.get(cat)
        kept = [x for x in dc if st and x in st]
        if kept:
            continue
        print('题%-4s [%s] 修正后归属: %s' % (q['no'], q.get('source'), l2name(cat)))
        print('   原始标签: %s' % ([dpath(x) for x in dc] if dc else '（无 deepCats）'))
        print('   题干: %s' % (q.get('stem') or '')[:130].replace('\n', ' '))
        print()

print('=== exam 回落题 ===')
d2 = orig('pwa/data/exam.json')
for vol in d2:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            key = '%s-%s' % (vol.get('id'), q.get('no'))
            cids = q.get('categoryIds') or []
            cat = str(FIX['exam'].get(key) or (cids[0] if cids else ''))
            dc = [str(x) for x in (q.get('deepCats') or [])]
            st = SUB.get(cat)
            kept = [x for x in dc if st and x in st]
            if kept:
                continue
            print('%s 修正后归属: %s' % (key, l2name(cat) if cat else '（无）'))
            print('   原始标签: %s' % ([dpath(x) for x in dc] if dc else '（无 deepCats）'))
            print('   题干: %s' % (q.get('stem') or '')[:130].replace('\n', ' '))
            print()
