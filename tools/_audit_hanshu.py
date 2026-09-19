# -*- coding: utf-8 -*-
"""核查：①核心题库总量 ②「函数」知识点题数与细分支覆盖 ③细分类计数是否漏算"""
import json, io
from collections import Counter

BASE = 'D:/ai code/math-note/pwa/data/'
DGYDIR = ('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
          'daguanyuan-for-windows-main/assets/')

cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))
core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
bank = json.load(io.open(BASE + 'bank_questions.json', encoding='utf-8'))
deep = json.load(io.open(BASE + 'cat_deep.json', encoding='utf-8'))
nodes = deep['nodes']
kids = {}
for cid, v in nodes.items():
    if v['p']:
        kids.setdefault(v['p'], []).append(cid)

def subtree(root):
    out, stack = [], [str(root)]
    while stack:
        x = stack.pop()
        out.append(x)
        stack += kids.get(x, [])
    return set(out)

print('=== ① 题库总量 ===')
coreqs = [q for s in core[0]['sections'] for q in s['questions']]
print('核心题库 core_bank.json: %d 题' % len(coreqs))
print('真题卷   exam.json:      %d 题' % sum(len(s.get('questions', [])) for v in exam for s in v.get('sections', [])))
print('附加题库 bank_questions: %d 题' % (len(bank) if isinstance(bank, list) else len(bank.get('questions', []))))

print()
print('=== ② 本库 L2「函数」知识点 ===')
fn = [(k, v) for k, v in cats.items() if v.get('level') == 2 and (v.get('display') or v.get('name')) == '函数']
for k, v in fn:
    l1 = cats.get(str(v.get('parentId')), {})
    print('本库节点 id=%s 名=%s 父=%s' % (k, v.get('display'), l1.get('display')))

for k, v in fn:
    mine = [q for q in coreqs if str(q.get('catId')) == str(k)]
    print('core_bank 中 catId=%s 的题: %d 道' % (k, len(mine)))
    for q in mine:
        print('    no=%-4s linked=%-18s deepCats=%s' % (q['no'], q.get('linkedQid'), q.get('deepCats')))
    # 大观园对应节点
    dgid = deep['l2root'].get(str(k))
    print('映射到细分类根:', dgid, nodes.get(dgid))
    if dgid:
        st = subtree(dgid)
        print('  该子树节点数:', len(st))
        allm = [q for q in coreqs if any(str(x) in st for x in (q.get('deepCats') or []))]
        print('  core_bank 中落在该子树的题:', len(allm))

print()
print('=== ③ 大观园「函数」节点题量（对照用户说的 27） ===')
raw = json.load(io.open(DGYDIR + 'categories.json', encoding='utf-8'))
dcats = {str(x['id']): x for x in raw['items']}
for k, v in fn:
    dgid = deep['l2root'].get(str(k))
    if not dgid:
        continue
    node = dcats.get(str(dgid))
    print('大观园节点 %s: name=%s parentId=%s totalCount=%s' % (
        dgid, node.get('name'), node.get('parentId'), node.get('totalCount')))
    # 子树 totalCount 合计
    st = subtree(dgid)
    tot = sum(int(dcats[x].get('totalCount') or 0) for x in st if x in dcats)
    print('  子树节点数 %d，totalCount 合计 %d' % (len(st), tot))
    print('  子节点:', [(c, dcats[c]['name'], dcats[c].get('totalCount')) for c in kids.get(str(dgid), []) if c in dcats][:10])
