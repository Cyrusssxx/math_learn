# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

p24 = next(p for p in exam if p['id'] == '2024数二真题')

# 打印题 17 与 题 22 的完整 idea/answer
for no in ['17', '22']:
    q = next(q for s in p24['sections'] for q in s['questions'] if str(q['no']) == no)
    print(f"===== 2024 题 {no} =====")
    print("--- idea ---")
    print(q.get('idea', ''))
    print("--- answer 前 500 字 ---")
    print(q.get('answer', '')[:500])
    print()

# 全卷扫描"考纲外"关键词
print("===== 全卷考纲外关键词扫描 =====")
kw = ['雅可比', '向量空间', '过渡矩阵', '基变换', '正交补', '不变子空间', 'Jacobian']
for s in p24['sections']:
    for q in s['questions']:
        text = (q.get('idea', '') or '') + (q.get('answer', '') or '') + (q.get('tips', {}) and json.dumps(q.get('tips', {}), ensure_ascii=False) or '')
        hits = [k for k in kw if k in text]
        if hits:
            print(f"题 {q['no']}: 命中 {hits}")
