# -*- coding: utf-8 -*-
"""为 exam.json（数二真题 607 题）计算 deepCats：在大观园题库中匹配同题取细分类节点 id。
   匹配不到 → 用该题在本库 L2 类目（categoryIds）经 _l2_map.json 兜底。
   输出 tools/_deepcats_exam.json ：{ 'paperId-no': [dgyId, ...] }
"""
import json, io, sys, difflib
from collections import Counter

sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import norm, grams                        # noqa: E402

ROOT = 'D:/ai code/math-note/tools/'
BASE = 'D:/ai code/math-note/pwa/data/'
DGYDIR = ('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
          'daguanyuan-for-windows-main/assets/')

raw = json.load(io.open(DGYDIR + 'questions.json', encoding='utf-8'))
if isinstance(raw, list):
    dgy_items = raw
else:
    dgy_items = raw.get('questions') or raw.get('items') or []
keep = set(json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8')).keys())
print('细分类树节点 %d；大观园题 %d' % (len(keep), len(dgy_items)))

ref = []
for it in dgy_items:
    n = norm(it.get('stem') or '')
    if not n:
        continue
    ref.append({'id': str(it.get('id')), 'n': n,
                'full': norm((it.get('stem') or '') + ' ' + ' '.join(str(x) for x in (it.get('options') or []))),
                'cats': [str(c) for c in (it.get('categoryIds') or []) if str(c) in keep],
                'grams': grams(n)})
inv = {}
for i, r in enumerate(ref):
    for g in r['grams']:
        inv.setdefault(g, []).append(i)

l2map = json.load(io.open(ROOT + '_l2_map.json', encoding='utf-8'))
ex = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
out, hit, fb, none = {}, 0, 0, 0
for vol in ex:
    pid = vol.get('id')
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            nq = norm(q.get('stem'))
            key = '%s-%s' % (pid, q.get('no'))
            if not nq:
                none += 1
                continue
            gq = grams(nq)
            cnt = Counter()
            for g in gq:
                for i in inv.get(g, ()):
                    cnt[i] += 1
            best, bi = 0.0, None
            for i, c in cnt.most_common(60):
                r = ref[i]
                s = max(difflib.SequenceMatcher(None, nq, r['n'], autojunk=False).ratio(),
                        difflib.SequenceMatcher(None, nq, r['full'], autojunk=False).ratio())
                if s > best:
                    best, bi = s, i
            ids = []
            if bi is not None and best >= 0.8:
                ids = ref[bi]['cats']
            if ids:
                hit += 1
            else:
                for cid in (q.get('categoryIds') or []):
                    m = l2map.get(str(cid))
                    if m:
                        ids = [m]
                        break
                if ids:
                    fb += 1
                else:
                    none += 1
            if ids:
                out[key] = ids

print('exam deepCats：匹配命中 %d / 兜底 %d / 无 %d（共 %d 题）' % (hit, fb, none, len(out) + none))
json.dump(out, io.open(ROOT + '_deepcats_exam.json', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'), sort_keys=True)
print('已写 tools/_deepcats_exam.json')
