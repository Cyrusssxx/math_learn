# -*- coding: utf-8 -*-
"""生成 pwa/data/core_bank.json —— 与 exam.json 同结构，供 category.js 零改动挂载到同一棵分类树。

每个 question:
  no, kind, type, stem, options[], answer, categoryIds[catId], source(题源), srcPage, srcOrder
"""
import json, io, re
from collections import defaultdict

ROOT = 'D:/ai code/math-note/tools/'
BASE = 'D:/ai code/math-note/pwa/data/'
BANK = ROOT + 'yancai_bank.json'
OUT = BASE + 'core_bank.json'

cats = json.load(io.open(BASE + 'exam_categories.json', encoding='utf-8'))
bank = json.load(io.open(BANK, encoding='utf-8'))

# 用高置信交叉核对结果回填「视觉转写题」的参考答案（score >= 0.92 才回填，宁缺勿错）
rep_ans = {}
rep_idea = {}
try:
    rep = json.load(io.open(ROOT + '_match_report.json', encoding='utf-8'))
    for r in rep:
        b = r.get('best')
        if b and b.get('score', 0) >= 0.92:
            if (b.get('answer') or '').strip():
                rep_ans[r['id']] = b['answer'].strip()
            if (b.get('explanation') or '').strip():
                rep_idea[r['id']] = b['explanation'].strip()
    print('高置信回填候选：答案 %d 题 / 解析 %d 题' % (len(rep_ans), len(rep_idea)))
except Exception as e:
    print('!! 读取匹配报告失败:', e)

qs = [q for q in bank['questions'] if q.get('catId')]
print('待导出 %d 题（题库 %d）' % (len(qs), len(bank['questions'])))

KIND = {'choice': 'choice', 'fill': 'blank', 'calc': 'calc', 'proof': 'proof'}


def clean_stem(q, stem):
    s = stem or ''
    # 参考库里的题图引用（asset://sha256/...）在 PWA 里不可用 → 换成提示
    if re.search(r'!\[[^\]]*\]\(asset://', s):
        s = re.sub(r'!\[[^\]]*\]\(asset://[^)]*\)', '', s).strip()
        s += '（本题含原题图形，见原书 P%d）' % max(1, q['page'] - 10)
    elif re.search(r'如图|图形所示|图像所示|图形如', s) and '见原书' not in s:
        s += '（图形见原书 P%d）' % max(1, q['page'] - 10)
    return s


# 先按 (page, order) 排出全局顺序
qs.sort(key=lambda q: (q['page'], q['order']))
seq = 0
by_chapter = defaultdict(list)
for q in qs:
    seq += 1
    cid = str(q['catId'])
    ch = cats[str(cats[cid]['parentId'])]
    options = []
    if isinstance(q.get('options'), dict):
        options = [q['options'][k] for k in 'ABCD' if q['options'].get(k)]
    out = {
        'no': seq,
        'kind': KIND.get(q.get('type') or 'fill', 'blank'),
        'type': KIND.get(q.get('type') or 'fill', 'blank'),
        'stem': clean_stem(q, q.get('stem')),
        'options': options,
        'answer': ((q.get('ref_answer') or '').strip() or rep_ans.get(q['id'], '')),
        'idea': (q.get('ref_idea') or '').strip() or rep_idea.get(q['id'], ''),
        'categoryIds': [int(cid)],
        'catId': int(cid),
        'source': q.get('source') or '',
        'srcPage': q['page'],
        'srcOrder': q['order'],
        'status': q.get('status'),
    }
    by_chapter[ch['name']].append(out)

# 章节顺序：按分类树里的章节 id 排（极限→一元微分→一元积分→多元微分→二重积分→微分方程→线代）
CH_ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程',
            '行列式', '矩阵', '向量', '线性方程组', '特征值与特征向量', '二次型']
sections = []
for name in CH_ORDER:
    if name in by_chapter and by_chapter[name]:
        sections.append({'title': name, 'questions': by_chapter[name]})
for name, arr in by_chapter.items():
    if name not in CH_ORDER and arr:
        sections.append({'title': name, 'questions': arr})

paper = [{
    'id': 'core',
    'year': '',
    'title': '数二核心题库（大观严选题）',
    'file': '',
    'sections': sections,
}]

with io.open(OUT, 'w', encoding='utf-8', newline='') as f:
    # 与 exam.json / practice.json 保持一致的紧凑单行格式（PWA 预缓存，体积优先）
    json.dump(paper, f, ensure_ascii=False, separators=(',', ':'))

print('已写 %s（%.0f KB）' % (OUT, len(json.dumps(paper, ensure_ascii=False)) / 1024))
print()
print('=== 章节分布 ===')
for s in sections:
    choice = sum(1 for q in s['questions'] if q['kind'] == 'choice')
    print('  %-10s %3d 题（选择 %d）' % (s['title'], len(s['questions']), choice))
print()
print('选项缺失的选择题:', sum(1 for q in qs if q.get('type') == 'choice'
                              and not (q.get('options') or {})))
allq = [q for s in sections for q in s['questions']]
print('带答案的题:', sum(1 for q in allq if q['answer'].strip()))
print('带解析的题:', sum(1 for q in allq if q['idea'].strip()))
print('含“见原书”图形提示的题:', sum(1 for q in allq if '见原书' in q['stem']))
