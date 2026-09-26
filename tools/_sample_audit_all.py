# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    questions = [q for s in json.load(f)[0]['sections'] for q in s['questions']]

print(f"总题数: {len(questions)}")
print("=== 抽查 10 道不同题目的答案与解析质量 ===")
sample_indices = [0, 15, 30, 60, 100, 150, 200, 250, 300, 345]

for idx in sample_indices:
    q = questions[idx]
    print(f"\n[#{q.get('pdfNo'):03d}] no: {q.get('no')} | 来源: {q.get('source')}")
    print(f"  题干: {q.get('stem')[:60].replace(chr(10), ' ')}")
    if q.get('options'):
        print(f"  选项: {q.get('options')}")
    print(f"  答案: {repr(q.get('answer'))[:80]}")
    print(f"  解析长度: {len(str(q.get('idea')))} 字")
    print(f"  解析内容: {repr(q.get('idea'))[:120]}...")
