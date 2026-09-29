# -*- coding: utf-8 -*-
"""修复 qid 冲突导致的「笔记串题」：
用题干相似度（归一化后 SequenceMatcher）判断 linkedQid 是否误匹配；
对明显不同题（ratio < 0.5）清除其 linkedQid，使其回到独立 qid（core-xx / xd-xx）。
"""
import json, io, re, difflib
from collections import defaultdict

def norm(s):
    s = re.sub(r'\$[^$]*\$', ' ', str(s or ''))          # 去行内公式
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)                    # 去 LaTeX 命令
    s = re.sub(r'[\s\{\}\(\)\[\]\_\^\&\%\,\.\;\:\'\"\`]', '', s)
    return s.lower()

def sim(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a[:120], b[:120]).ratio()

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)
with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

exam_stem = {}
for p in exam:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            exam_stem[f"{p['id']}-{q['no']}"] = q.get('stem', '')

by_qid = defaultdict(list)
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            qid = q.get('linkedQid')
            if qid:
                by_qid[qid].append(('core', q, p, s))
for p in xd:
    for s in p['sections']:
        for q in s['questions']:
            qid = q.get('linkedQid')
            if qid:
                by_qid[qid].append(('xd', q, p, s))

fixed, kept = [], []
for qid, items in sorted(by_qid.items()):
    if len(items) < 2:
        continue
    es = norm(exam_stem.get(qid, ''))
    # 每条与真题题干的相似度
    scored = []
    for src, q, p, s in items:
        scored.append((sim(norm(q.get('stem', '')), es), src, q))
    best = max(scored, key=lambda x: x[0])
    for ratio, src, q in scored:
        no = q.get('no')
        if ratio < 0.5:
            # 明确不是同一道题 → 解除误绑定
            q.pop('linkedQid', None)
            fixed.append((src, no, qid, round(ratio, 2)))
        else:
            kept.append((src, no, qid, round(ratio, 2)))

# 写回（紧凑单行）
with io.open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))
with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(xd, f, ensure_ascii=False, separators=(',', ':'))

print(f'已解除误绑定（不同题）{len(fixed)} 处：')
for src, no, qid, r in fixed:
    print(f'  [{src}] no={no} 原绑定 {qid}（相似度 {r}）→ 改为独立 qid')
print(f'\n保留绑定（确为同题）{len(kept)} 处（示例）：')
for src, no, qid, r in kept[:8]:
    print(f'  [{src}] no={no} → {qid}（相似度 {r}）')
