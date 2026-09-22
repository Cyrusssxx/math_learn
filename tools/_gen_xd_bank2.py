# -*- coding: utf-8 -*-
# 生成大观园线代补充题库 v2：全量 959 题，细节点沿父链映射到 exam_categories 最近可挂载节点
import json, io

DGY = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
cats = json.load(io.open(DGY + 'categories.json', encoding='utf-8'))['items']
q = json.load(io.open(DGY + 'questions.json', encoding='utf-8'))['items']
ecats = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))
ecids = set()
for nid, n in ecats.items():
    try:
        ecids.add(int(nid))
    except Exception:
        pass

byid = {}
for it in cats:
    byid[str(it['id'])] = it

# 线代子树节点
xd_nodes = set()
def collect(nid):
    xd_nodes.add(nid)
    for it in cats:
        if str(it.get('parentId')) == str(nid):
            collect(str(it['id']))
collect('1')

# 细节点 → 最近可挂祖先（含自身）；返回列表（可能有多个？取第一个可挂的）
def nearest(nid):
    seen = set()
    cur = str(nid)
    while cur and cur not in seen:
        seen.add(cur)
        if int(cur) in ecids:
            return int(cur)
        cur = str(byid.get(cur, {}).get('parentId') or '')
    return None

# 统计映射分布
map_cnt = {}
for nid in sorted(xd_nodes, key=int):
    t = nearest(nid)
    if t is None:
        map_cnt[nid] = '×'
    else:
        map_cnt[nid] = str(t)

# 提取全量线代题并映射
items_out = []
skip_no = 0
for it in q:
    cids = [str(c) for c in (it.get('categoryIds') or [])]
    xcids = [c for c in cids if c in xd_nodes]
    if not xcids:
        continue
    mapped = []
    for c in xcids:
        t = nearest(c)
        if t is not None and t not in mapped:
            mapped.append(t)
    if not mapped:
        skip_no += 1
        continue
    items_out.append((it, mapped))

print('可挂载线代题:', len(items_out), '| 无法挂载:', skip_no)

# 组装题库（按知识点分组）
sections = {}
for it, mapped in items_out:
    c0 = str(mapped[0])
    sections.setdefault(c0, []).append({
        'no': it.get('serial') or it.get('id'),
        'stem': it.get('stem') or '',
        'options': it.get('options') or [],
        'answer': it.get('answer') or '',
        'idea': it.get('explanation') or '',
        'source': it.get('source') or '',
        'categoryIds': mapped,
    })

bank = [{'id': 'xd', 'title': '线性代数补充题库（大观园）', 'sections': [
    {'title': c0, 'questions': sections[c0]} for c0 in sorted(sections, key=int)
]}]
with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as fp:
    json.dump(bank, fp, ensure_ascii=False, separators=(',', ':'))

total = sum(len(s['questions']) for s in bank[0]['sections'])
print('已生成 xd_bank.json：%d 道（分 %d 个知识点）' % (total, len(bank[0]['sections'])))
print('知识点分布:')
for s in sorted(bank[0]['sections'], key=lambda x: -len(x['questions'])):
    print('  %s: %d' % (s['title'], len(s['questions'])))
