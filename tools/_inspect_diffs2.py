# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

src = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
with io.open(src, 'r', encoding='utf-8') as f:
    dgy = json.load(f)
    items = dgy if isinstance(dgy, list) else dgy.get('items', [])

# 2022-1
q2022_1 = next(q for p in exam_data if p['id'] == '2022数二真题' for s in p['sections'] for q in s['questions'] if str(q['no']) == '1')
d2022_1 = next(x for x in items if x['serial'] == 4992)
print("=== 2022-1 ===")
print("本库 opts:", q2022_1.get('options'))
print("大观 opts:", d2022_1.get('options'))
print("大观 ans:", d2022_1.get('answer'))
print("本库 ans[:100]:", q2022_1.get('answer')[:100])

# 2022-10
q2022_10 = next(q for p in exam_data if p['id'] == '2022数二真题' for s in p['sections'] for q in s['questions'] if str(q['no']) == '10')
d2022_10 = next(x for x in items if x['serial'] == 5001)
print("\n=== 2022-10 ===")
print("本库 stem:", repr(q2022_10.get('stem')))
print("大观 stem:", repr(d2022_10.get('stem')))
print("本库 opts:", q2022_10.get('options'))
print("大观 opts:", d2022_10.get('options'))

# 2022-19
q2022_19 = next(q for p in exam_data if p['id'] == '2022数二真题' for s in p['sections'] for q in s['questions'] if str(q['no']) == '19')
d2022_19 = next(x for x in items if x['serial'] == 5010)
print("\n=== 2022-19 ===")
print("本库 ans[:150]:", repr(q2022_19.get('answer')[:150]))
print("大观 ans[:150]:", repr(d2022_19.get('answer')[:150]))
print("大观 exp[:400]:", repr(d2022_19.get('explanation')[:400]))
