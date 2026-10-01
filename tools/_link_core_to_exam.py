# -*- coding: utf-8 -*-
"""把核心题库中「数二真题来源」的题与 exam.json 数二真题按题干匹配，补齐 linkedQid，
使笔记 / 收藏 / 掌握标记在真题页与分类页核心题库之间共享同一 qid。
"""
import json, io, re, difflib, shutil, os

CORE = 'pwa/data/core_bank.json'
EXAM = 'pwa/data/exam.json'

def norm(s):
    s = re.sub(r'\$[^$]*\$', ' ', str(s or ''))
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[\s\{\}\(\)\[\]\_\^\&\,\.\;\:\'\"\`\|]', '', s)
    return s.lower()

def parse_year(src):
    m = re.search(r'(19|20)\d{2}', str(src or ''))
    return int(m.group(0)) if m else None

def has_shu2(src):
    """source 的科目串是否包含数二"""
    return bool(re.search(r'数[一二三]{1,3}', str(src or '')) and '二' in str(src or ''))

with io.open(CORE, encoding='utf-8') as f:
    core = json.load(f)
with io.open(EXAM, encoding='utf-8') as f:
    exam = json.load(f)

# exam 索引：年份 -> [(qid, 题干norm)]
exam_idx = {}
for p in exam:
    y = parse_year(p['id'])
    if y is None:
        continue
    arr = []
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            arr.append((f"{p['id']}-{q['no']}", norm(q.get('stem', ''))))
    exam_idx[y] = arr

core_qs = [q for p in core for s in p.get('sections', []) for q in s.get('questions', [])]

report = {'candidates': 0, 'already': 0, 'matched': 0, 'ambiguous': 0, 'nomatch': 0, 'not_shu2': 0}
new_links = []
pairs_sample = []
for q in core_qs:
    src = str(q.get('source') or '')
    y = parse_year(src)
    if y is None or not has_shu2(src) or y not in exam_idx:
        report['not_shu2'] += 1
        continue
    report['candidates'] += 1
    if q.get('linkedQid'):
        report['already'] += 1
        continue
    a = norm(q.get('stem', ''))
    scored = sorted(((difflib.SequenceMatcher(None, a[:150], b[:150]).ratio(), qid) for qid, b in exam_idx[y]),
                    reverse=True)
    if not scored:
        report['nomatch'] += 1
        continue
    best, bestq = scored[0]
    second = scored[1][0] if len(scored) > 1 else 0
    if best >= 0.85 and (best - second) >= 0.03:
        q['linkedQid'] = bestq
        new_links.append((q.get('no'), bestq, round(best, 3)))
        report['matched'] += 1
        if len(pairs_sample) < 12:
            pairs_sample.append((q.get('no'), src, bestq, round(best, 3), str(q.get('stem'))[:52]))
    elif best >= 0.85:
        report['ambiguous'] += 1
    else:
        report['nomatch'] += 1

print('候选（数二真题来源、年份在 2000-2026）:', report['candidates'])
print('  其中已有 linkedQid:', report['already'])
print('  本次新匹配成功:', report['matched'])
print('  相似但存在并列（跳过）:', report['ambiguous'])
print('  未找到 >=0.85 匹配:', report['nomatch'])
print('非数二来源/年份不在范围（不动）:', report['not_shu2'])
print('\n新匹配示例（core no | source | 真题 qid | 相似度 | 题干）:')
for no, src, qid, r, stem in pairs_sample:
    print(f'  {no} | {src} | {qid} | {r} | {stem}')

# 备份后写回
shutil.copy(CORE, CORE + '.bak')
with io.open(CORE, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

# 验证
with io.open(CORE, encoding='utf-8') as f:
    chk = json.load(f)
linked = sum(1 for p in chk for s in p.get('sections', []) for q in s.get('questions', []) if q.get('linkedQid'))
total = sum(1 for p in chk for s in p.get('sections', []) for q in s.get('questions', []))
print(f'\n写回完成：core 共 {total} 题，带 linkedQid 的 {linked} 题（{linked / total * 100:.1f}%）')
