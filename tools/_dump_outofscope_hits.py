# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

targets = [
    ('2025数二真题', '10'), ('2024数二真题', '9'), ('2021数二真题', '9'),
    ('2021数二真题', '21'), ('2014数二真题', '8'), ('2011数二真题', '13'),
    ('2010数二真题', '19'), ('2008数二真题', '6'), ('2007数二真题', '9'),
    ('2007数二真题', '24'),
]

for pid, no in targets:
    p = next(p for p in exam if p['id'] == pid)
    q = next(q for s in p['sections'] for q in s['questions'] if str(q['no']) == no)
    print(f"########## {pid} 题 {no} ##########")
    print("--- 题干 ---")
    print(q.get('stem', '')[:200])
    print("--- idea ---")
    print(q.get('idea', '')[:600])
    print("--- answer 前 400 字 ---")
    print((q.get('answer') or '')[:400])
    print()
