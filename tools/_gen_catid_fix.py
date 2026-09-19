# -*- coding: utf-8 -*-
"""生成 catId 修正表：用「大观园细分类标签」反推每题正确的本库知识点。
   输出 tools/_catid_fix.json = { "core": {题号: 新catId}, "exam": {卷id-题号: 新catId} }
   同时打印抽样供人工核对。"""
import json, io
from collections import Counter, defaultdict

BASE = 'D:/ai code/math-note/pwa/data/'
TOOLS = 'D:/ai code/math-note/tools/'
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes, l2root = deep['nodes'], deep['l2root']
cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))

kids = {}
for cid, v in nodes.items():
    if v['p']:
        kids.setdefault(v['p'], []).append(cid)


def subtree(root):
    out, stack, seen = [], [str(root)], set()
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
        stack += kids.get(x, [])
    return out


SUB = {k: set(subtree(v)) for k, v in l2root.items()}
node2l2 = defaultdict(list)
for l2, st in SUB.items():
    for n in st:
        node2l2[n].append(l2)


def l2name(cid):
    v = cats.get(str(cid), {})
    p = cats.get(str(v.get('parentId')), {})
    return '%s / %s' % (p.get('display') or p.get('name') or '?', v.get('display') or v.get('name') or '?')


def best_l2(dc):
    """由大观园标签反推本库 L2（取票数最多；平票取子树更小=更具体的那个）"""
    cand = Counter()
    for x in dc:
        for l2 in node2l2.get(str(x), []):
            cand[l2] += 1
    if not cand:
        return None
    top = max(cand.values())
    tied = [k for k, v in cand.items() if v == top]
    return min(tied, key=lambda k: len(SUB[k]))


# ---------- core ----------
bak = json.load(io.open('D:/ai code/math-note/_bak_core.json', encoding='utf-8'))
qs = [q for s in bak[0]['sections'] for q in s['questions']]
core_fix, core_stat = {}, Counter()
for q in qs:
    cat = str(q.get('catId'))
    dc = [str(x) for x in (q.get('deepCats') or [])]
    b = best_l2(dc)
    if b is None:
        core_stat['无法判定'] += 1
        continue
    if b == cat:
        core_stat['一致'] += 1
    else:
        core_fix[str(q['no'])] = b
        core_stat['修正'] += 1

# ---------- exam ----------
bak2 = json.load(io.open('D:/ai code/math-note/_bak_exam.json', encoding='utf-8'))
exam_fix, exam_stat = {}, Counter()
for vol in bak2:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            cids = [str(x) for x in (q.get('categoryIds') or [])]
            dc = [str(x) for x in (q.get('deepCats') or [])]
            if not cids:
                exam_stat['无原类目'] += 1
                continue
            b = best_l2(dc)
            if b is None:
                exam_stat['无法判定'] += 1
                continue
            if b == cids[0]:
                exam_stat['一致'] += 1
            else:
                exam_fix['%s-%s' % (vol.get('id'), q.get('no'))] = b
                exam_stat['修正'] += 1

out = {'core': core_fix, 'exam': exam_fix}
json.dump(out, io.open(TOOLS + '_catid_fix.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1, sort_keys=True)
print('core:', dict(core_stat))
print('exam:', dict(exam_stat))
print('已写 tools/_catid_fix.json（core %d / exam %d 条修正）' % (len(core_fix), len(exam_fix)))

print()
print('=== 抽样核对（题号 | 现 → 应改 | 大观园标签路径）===')
def dpath(nid):
    out, cur, g = [], str(nid), 0
    while cur in nodes and g < 30:
        out.append(nodes[cur]['n'])
        cur = nodes[cur]['p']
        g += 1
    return ' / '.join(reversed(out))

shown = 0
for q in qs:
    no = str(q['no'])
    if no in core_fix:
        print('  题%-4s 现[%s] → 应[%s]' % (no, l2name(q['catId']), l2name(core_fix[no])))
        print('        标签: %s' % dpath((q.get('deepCats') or ['?'])[0]))
        shown += 1
        if shown >= 10:
            break