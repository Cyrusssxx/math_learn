# -*- coding: utf-8 -*-
# 生成大观园线代补充题库 xd_bank.json（挂 exam_categories 线代知识点）
# 数二范围：线代全节点（大观园无独立"向量空间"节点 → 全部保留；id 与 exam_categories 一致直接复用）
import json, io

DGY = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
cats = json.load(io.open(DGY + 'categories.json', encoding='utf-8'))['items']
q = json.load(io.open(DGY + 'questions.json', encoding='utf-8'))['items']
ecats = json.load(io.open('pwa/data/exam_categories.json', encoding='utf-8'))

# 线代子树节点（大观园 id）
xd_nodes = set()
def collect(nid):
    xd_nodes.add(nid)
    for it in cats:
        if str(it.get('parentId')) == str(nid):
            collect(str(it['id']))
collect('1')

# exam_categories 已有节点 id（int）
ecids = set()
for nid, n in ecats.items():
    try:
        ecids.add(int(nid))
    except Exception:
        pass

# 线代节点 ∩ exam_categories（可挂载的）
usable = sorted(int(x) for x in xd_nodes if int(x) in ecids)
print('线代节点 %d 个，可挂载到 exam_categories 的 %d 个' % (len(xd_nodes), len(usable)))
# 不能挂的（大观园有但 exam_categories 无）
missing = sorted(int(x) for x in xd_nodes if int(x) not in ecids)
print('大观园有但 exam 分类无（无法挂载）:', missing)

# 提取线代题（categoryIds 含线代节点）
xd_items = []
no_cat = 0
for it in q:
    cids = [str(c) for c in (it.get('categoryIds') or [])]
    xc = [int(c) for c in cids if c in xd_nodes and int(c) in ecids]
    if xc:
        xd_items.append((it, xc))
    elif any(c in xd_nodes for c in cids):
        no_cat += 1
print('线代题 %d 道（其中 %d 道 categoryIds 不可挂载到 exam 分类，跳过）' % (len(xd_items), no_cat))

# 组装 xd_bank.json（同 exam.json/core_bank.json 结构）
sections = {}
for it, xc in xd_items:
    # 按第一个可挂载知识点分组（保持顺序）
    c0 = str(xc[0])
    sections.setdefault(c0, []).append({
        'no': it.get('serial') or it.get('id'),
        'stem': it.get('stem') or '',
        'options': it.get('options') or [],
        'answer': it.get('answer') or '',
        'idea': it.get('explanation') or '',
        'source': it.get('source') or '',
        'categoryIds': xc,
    })

bank = [{'id': 'xd', 'title': '线性代数补充题库（大观园）', 'sections': [
    {'title': str(c0), 'questions': qs} for c0, qs in sections.items()
]}]
with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as fp:
    json.dump(bank, fp, ensure_ascii=False, separators=(',', ':'))

total = sum(len(qs) for s in bank[0]['sections'] for qs in [s['questions']])
print('已生成 xd_bank.json：%d 道（分 %d 个知识点分组）' % (total, len(bank[0]['sections'])))
