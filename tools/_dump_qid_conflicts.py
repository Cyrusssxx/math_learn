# -*- coding: utf-8 -*-
"""列出 core 与 xd 之间 qid 冲突的完整清单，并对比题干判断是「同题重复收录」还是「不同题误匹配」"""
import json, io, re
from collections import defaultdict

def norm(s):
    return re.sub(r'[\s\$\\\{\}\(\)\_\^\+\-\=\,\.\;\:\'\"\`\[\]【】]', '', str(s or '')).lower()

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)
with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

# 真题题干索引
exam_stem = {}
for p in exam:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            exam_stem[f"{p['id']}-{q['no']}"] = q.get('stem', '')

by_qid = defaultdict(list)
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            qid = q.get('linkedQid') or f"core-{q.get('no')}"
            by_qid[qid].append(('core', q.get('no'), q.get('stem', ''), q.get('source', '')))
for p in xd:
    for s in p['sections']:
        for q in s['questions']:
            qid = q.get('linkedQid') or f"xd-{q.get('no')}"
            by_qid[qid].append(('xd', q.get('no'), q.get('stem', ''), q.get('source', '')))

conf = {k: v for k, v in by_qid.items() if len(v) > 1}
print(f'qid 冲突组数: {len(conf)}')
for qid, items in sorted(conf.items()):
    exam_s = exam_stem.get(qid, '')
    print('=' * 70)
    print(f'qid={qid}')
    if exam_s:
        print(f'  真题题干: {exam_s[:70]}')
    for src, no, stem, tagsrc in items:
        a = norm(stem)[:34]
        b = norm(exam_s)[:34]
        same = (a and b and (a in b or b in a))
        print(f'  [{src}] no={no} ({tagsrc}) 同题={same}')
        print(f'      {stem[:70]}')
