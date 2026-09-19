# -*- coding: utf-8 -*-
"""把 deepCats 写入 exam.json（每题一个 deepCats 数组）。exam.json 是紧凑单行 JSON，用 json 读写保持格式。"""
import json, io

BASE = 'D:/ai code/math-note/pwa/data/'
ROOT = 'D:/ai code/math-note/tools/'
DEEP = json.load(io.open(ROOT + '_deepcats_exam.json', encoding='utf-8'))
ex = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))

n = 0
for vol in ex:
    pid = vol.get('id')
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            key = '%s-%s' % (pid, q.get('no'))
            dc = DEEP.get(key)
            if dc:
                q['deepCats'] = dc
                n += 1
            else:
                q['deepCats'] = []

with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(ex, f, ensure_ascii=False, separators=(',', ':'))

# 复查
ex2 = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
tot = sum(len(s.get('questions', [])) for v in ex2 for s in v.get('sections', []))
ok = sum(1 for v in ex2 for s in v.get('sections', []) for q in s.get('questions', []) if q.get('deepCats'))
print('exam.json 写入 deepCats: %d 题（共 %d 题）' % (ok, tot))
assert ok == tot, '有题缺 deepCats'
print('格式检查：单行 =', io.open(BASE + 'exam.json', encoding='utf-8').read().count('\n') == 0)
