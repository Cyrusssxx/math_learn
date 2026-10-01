# -*- coding: utf-8 -*-
"""分析未匹配的 51 题：打印其与同年数二真题最佳匹配的相似度，判断是否属转写差异"""
import json, io, re, difflib

def norm(s):
    s = re.sub(r'\$[^$]*\$', ' ', str(s or ''))
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[\s\{\}\(\)\[\]\_\^\&\,\.\;\:\'\"\`\|]', '', s)
    return s.lower()

def parse_year(src):
    m = re.search(r'(19|20)\d{2}', str(src or ''))
    return int(m.group(0)) if m else None

def has_shu2(src):
    return bool(re.search(r'数[一二三]{1,3}', str(src or '')) and '二' in str(src or ''))

with io.open('pwa/data/core_bank.json', encoding='utf-8') as f:
    core = json.load(f)
with io.open('pwa/data/exam.json', encoding='utf-8') as f:
    exam = json.load(f)

exam_idx = {}
for p in exam:
    y = parse_year(p['id'])
    if y is None:
        continue
    exam_idx[y] = [(f"{p['id']}-{q['no']}", norm(q.get('stem', '')), str(q.get('stem'))[:60])
                   for s in p.get('sections', []) for q in s.get('questions', [])]

rows = []
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            src = str(q.get('source') or '')
            y = parse_year(src)
            if q.get('linkedQid') or y is None or not has_shu2(src) or y not in exam_idx:
                continue
            a = norm(q.get('stem', ''))
            scored = sorted(((difflib.SequenceMatcher(None, a[:150], b[:150]).ratio(), qid, bs) for qid, b, bs in exam_idx[y]), reverse=True)
            if not scored:
                continue
            best, bestq, bstem = scored[0]
            rows.append((round(best, 3), q.get('no'), src, bestq, str(q.get('stem'))[:50], bstem))

rows.sort(reverse=True)
print(f'未匹配题 {len(rows)} 道，按最佳相似度降序：')
for r, no, src, qid, stem, bstem in rows:
    print(f'\n[{r}] core no={no} ({src})')
    print(f'   core : {stem}')
    print(f'   exam : {qid} | {bstem}')
