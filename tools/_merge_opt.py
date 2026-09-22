# -*- coding: utf-8 -*-
# 合并 6 卷 patch 到 exam.json（只改 tips/idea/answer），QA 后写回
import json, io, os

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
exam_q = {}
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            exam_q[(v['id'], str(q['no']))] = q

patch_files = ['_opt_2021.json', '_opt_2022.json', '_opt_2023.json',
               '_opt_2024.json', '_opt_2025.json', '_opt_2026.json']
applied, missing = 0, []
for f in patch_files:
    d = json.load(io.open(os.path.join('tools', f), encoding='utf-8'))
    for vid, items in d.items():
        for no, fields in items.items():
            q = exam_q.get((vid, no))
            if not q:
                missing.append('%s-%s' % (vid, no))
                continue
            # tips 四键校验
            tips = fields.get('tips') or {}
            for k in ('gs', 'jq', 'yc', 'zy'):
                if k not in tips or not str(tips[k]).strip():
                    missing.append('%s-%s tips.%s 缺失' % (vid, no, k))
                    break
            else:
                q['tips'] = {k: str(tips[k]).strip() for k in ('gs', 'jq', 'yc', 'zy')}
            idea = fields.get('idea')
            ans = fields.get('answer')
            if not idea or not str(idea).strip() or not ans or not str(ans).strip():
                missing.append('%s-%s idea/answer 为空' % (vid, no))
            else:
                q['idea'] = str(idea).strip()
                q['answer'] = str(ans).strip()
            applied += 1

print('应用 %d 题；问题 %d 条:' % (applied, len(missing)))
for m in missing[:10]:
    print('  -', m)

# 校验：卷数、题数、$ 配平
nq = sum(len(s.get('questions', [])) for v in exam for s in v.get('sections', []))
print('卷 %d / 题 %d（应 27/607）' % (len(exam), nq))
bad_dollar = 0
for v in exam:
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            for f in ('stem', 'answer', 'idea'):
                t = q.get(f) or ''
                if t.count('$') % 2:
                    bad_dollar += 1
print('奇数 $ 字段数:', bad_dollar)

if not missing:
    with io.open(P, 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('已写回 exam.json')
