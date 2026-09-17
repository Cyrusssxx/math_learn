# -*- coding: utf-8 -*-
"""答案覆盖度体检：现有 core_bank.json 里答案的覆盖率与质量（短答案 vs 完整解析）。"""
import json, io, re, sys, difflib
from collections import Counter

sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import load_refs, norm, grams            # noqa: E402

BASE = 'D:/ai code/math-note/pwa/data/'
ROOT = 'D:/ai code/math-note/tools/'
bank = json.load(io.open(ROOT + 'yancai_bank.json', encoding='utf-8'))
qs = bank['questions']
print('题库 %d 题' % len(qs))

# ---- 现状：bank 里的 ref_answer ----
have_ref = [q for q in qs if (q.get('ref_answer') or '').strip()]
print('带 ref_answer 的：%d' % len(have_ref))

# ---- exam.json 可用性：数二 2000-2026 带完整答案+解析 ----
exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
exam_items = []
for vol in exam:
    y = str(vol.get('year'))
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            stem = q.get('stem') or ''
            exam_items.append({
                'year': y, 'no': q.get('no'), 'kind': q.get('kind'),
                'stem': stem, 'norm': norm(stem), 'grams': grams(norm(stem)),
                'answer': q.get('answer') or '', 'idea': q.get('idea') or '',
            })
print('exam.json 可用条目 %d（数二 2000-2026，带【答案】+【解析】）' % len(exam_items))

inv = {}
for i, e in enumerate(exam_items):
    for g in e['grams']:
        inv.setdefault(g, []).append(i)

# ---- 逐题判定：能否用 exam.json 升级/补全答案 ----
plan_exam, plan_ref, none_yet = [], [], []
for q in qs:
    yr = re.findall(r'(20\d\d|19\d\d)', q.get('source') or '')
    if not any(2000 <= int(y) <= 2026 for y in yr) or '数二' not in (q.get('source') or ''):
        if (q.get('ref_answer') or '').strip():
            plan_ref.append(q)
        else:
            none_yet.append(q)
        continue
    nq = norm(q.get('stem'))
    gq = grams(nq)
    cnt = Counter()
    for g in gq:
        for i in inv.get(g, ()):
            cnt[i] += 1
    best, bi = 0.0, None
    for i, c in cnt.most_common(60):
        s = difflib.SequenceMatcher(None, nq, exam_items[i]['norm'], autojunk=False).ratio()
        if s > best:
            best, bi = s, i
    if bi is not None and best >= 0.9 and (exam_items[bi]['answer'] or '').strip():
        plan_exam.append((q, exam_items[bi], round(best, 3)))
    elif (q.get('ref_answer') or '').strip():
        plan_ref.append(q)
    else:
        none_yet.append(q)

print()
print('可用 exam.json 完整答案升级 : %d 题' % len(plan_exam))
print('用参考库答案（大观园等）    : %d 题' % len(plan_ref))
print('两种都没有（仍缺答案）      : %d 题' % len(none_yet))

# ---- 现有答案的质量分布 ----
short = sum(1 for q in qs if 0 < len((q.get('ref_answer') or '').strip()) <= 3)
mid = sum(1 for q in qs if 3 < len((q.get('ref_answer') or '').strip()) <= 60)
long_ = sum(1 for q in qs if len((q.get('ref_answer') or '').strip()) > 60)
print()
print('现有 ref_answer 长度分布：<=3 字符 %d | 4-60 %d | >60 %d' % (short, mid, long_))

print()
print('=== exam.json 升级样本（前 8） ===')
for q, e, s in plan_exam[:8]:
    print('  [%s] src=%s <- exam %s 第%s题 (%.2f)' % (q['id'], q.get('source'), e['year'], e['no'], s))
    print('      新答案: %s' % (e['answer'] or '')[:100].replace('\n', ' '))

print()
print('=== 仍缺答案的 %d 题 ===' % len(none_yet))
for q in none_yet[:40]:
    print('  [%s] src=%s | %s' % (q['id'], q.get('source'), (q.get('stem') or '')[:90].replace('\n', ' ')))
