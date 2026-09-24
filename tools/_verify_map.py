# -*- coding: utf-8 -*-
# 验证节点同 id 同名 + 检查 serial 冲突 + 打印现有 xd 条目字段结构
import json, io, re

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
dy_cats = json.load(io.open(ROOT + 'categories.json', encoding='utf-8'))['items']
dy_node = {int(n['id']): n for n in dy_cats}
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

our_xl = [nid for nid in our_node if 1 in our_anc(nid)]
print('=== 同 id 同名校验（我们 45 节点）===')
bad = []
for nid in sorted(our_xl):
    a = str(our_node[nid].get('name') or '').strip()
    b = str(dy_node.get(nid, {}).get('name') or '').strip()
    if a != b:
        bad.append((nid, a, b))
print('不一致:', bad if bad else '无（全部同名）✓')

# 现有 xd_bank 的 no 集合与字段
xd = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
xq = [q for s in xd[0]['sections'] for q in s['questions']]
nos = set(str(q['no']) for q in xq)
print()
print('现有 xd 条数:', len(xq), '| no 范围:', min(int(n) for n in nos), '-', max(int(n) for n in nos))
print('现有条目字段:', sorted(xq[0].keys()))
print('样本:', json.dumps({k: (str(v)[:60]) for k, v in xq[0].items()}, ensure_ascii=False))

# 大观园老年份缺失题的 serial
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))['items']
print()
print('大观园 serial 范围:', min(q['serial'] for q in qs), '-', max(q['serial'] for q in qs))
print('总题数:', len(qs), '| serial 唯一性:', len(set(q['serial'] for q in qs)) == len(qs))