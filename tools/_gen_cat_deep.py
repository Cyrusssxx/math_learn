# -*- coding: utf-8 -*-
"""生成细分类树 pwa/data/cat_deep.json（大观园数二相关 826 节点），
   并为核心题库 606 题计算 deepCats（大观园细分类节点 id，含子树查询用）。
   匹配策略：在大观园题库里按题干匹配（gram 预筛 + 0.8 阈值）取 categoryIds；
             匹配不到 → 用该题 catId 在本库 L2→大观园 映射（_l2_map.json）兜底。
"""
import json, io, re, sys, difflib
from collections import Counter

sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import load_refs, norm, grams            # noqa: E402

ROOT = 'D:/ai code/math-note/tools/'
BASE = 'D:/ai code/math-note/pwa/data/'
DGYDIR = ('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
          'daguanyuan-for-windows-main/assets/')

# ---------- 1) 细分类树 ----------
cats = {str(x['id']): x for x in json.load(io.open(DGYDIR + 'categories.json', encoding='utf-8'))['items']}
kids = {}
for k, v in cats.items():
    kids.setdefault(str(v.get('parentId')), []).append(k)


def subtree(root):
    out, stack = [], [str(root)]
    while stack:
        x = stack.pop()
        out.append(x)
        stack += kids.get(x, [])
    return out


keep = set(subtree(223)) | set(subtree(1))          # 高等数学 + 线性代数
tree = {}
for cid in keep:
    v = cats[cid]
    p = v.get('parentId')
    tree[cid] = {'n': v['name'], 'p': (str(p) if p not in (None, 0, '0') else '')}
print('细分类树节点: %d（高数+线代）' % len(tree))
json.dump(tree, io.open(BASE + 'cat_deep.json', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'), sort_keys=True)
print('已写 pwa/data/cat_deep.json')

# ---------- 2) 大观园题库索引（id → categoryIds） ----------
dgy_raw = json.load(io.open(DGYDIR + 'questions.json', encoding='utf-8'))
if isinstance(dgy_raw, dict):
    dgy_items = dgy_raw.get('questions') or dgy_raw.get('items') or []
else:
    dgy_items = dgy_raw
dgy_cats = {str(it.get('id')): [str(c) for c in (it.get('categoryIds') or [])] for it in dgy_items}
print('大观园题库 %d 条（含 categoryIds）' % len(dgy_cats))

# ---------- 3) 核心题 → deepCats ----------
bank = json.load(io.open(ROOT + 'yancai_bank.json', encoding='utf-8'))
qs = bank['questions']
l2map = json.load(io.open(ROOT + '_l2_map.json', encoding='utf-8'))

refs = load_refs()
refs = [r for r in refs if str(r.get('ref')) == 'dgy']
for r in refs:
    r['n'] = norm(r['stem'] or '')
    r['full'] = norm((r['stem'] or '') + ' ' + ' '.join(str(x) for x in (r.get('options') or [])))
inv = {}
for i, r in enumerate(refs):
    for g in r['grams']:
        inv.setdefault(g, []).append(i)
print('dgy 参考库索引 %d 条' % len(refs))

hit, fallback, none = 0, 0, 0
deep = {}
for q in qs:
    nq = norm(q.get('stem'))
    gq = grams(nq)
    cnt = Counter()
    for g in gq:
        for i in inv.get(g, ()):
            cnt[i] += 1
    best, bi = 0.0, None
    for i, c in cnt.most_common(60):
        r = refs[i]
        a = difflib.SequenceMatcher(None, nq, r['n'], autojunk=False).ratio()
        b = difflib.SequenceMatcher(None, nq, r['full'], autojunk=False).ratio()
        s = max(a, b)
        if s > best:
            best, bi = s, i
    ids = []
    if bi is not None and best >= 0.8:
        ids = [c for c in dgy_cats.get(str(refs[bi]['rid']), []) if c in keep]
    if ids:
        hit += 1
    else:
        m = l2map.get(str(q.get('catId')))
        if m:
            ids = [m]
            fallback += 1
        else:
            none += 1
    if ids:
        deep[q['id']] = ids

print('deepCats：匹配命中 %d / 兜底(L2映射) %d / 无 %d' % (hit, fallback, none))
n_multi = sum(1 for v in deep.values() if len(v) > 1)
avg = sum(len(v) for v in deep.values()) / max(1, len(deep))
print('平均每题 %.1f 个细分类节点，多标签题 %d 道' % (avg, n_multi))
json.dump(deep, io.open(ROOT + '_deepcats_core.json', 'w', encoding='utf-8'),
          ensure_ascii=False, separators=(',', ':'), sort_keys=True)
print('已写 tools/_deepcats_core.json')
