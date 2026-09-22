# -*- coding: utf-8 -*-
# 2023-16：所有 =8$。 → =8$$（两处）
import json, io

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2023数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '16')
a = q['answer']
n = a.count('=8$。')
q['answer'] = a.replace('=8$。', '=8$$')
with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('替换处数:', n)
