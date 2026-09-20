# -*- coding: utf-8 -*-
# 校验：bak(原始) vs 当前，56 个目标字段中「数学数值内容」是否保持
# 策略：把字段中的 LaTeX 命令与数字 token 提取出来比对（忽略定界符/空白/行结构差异）
import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

B1 = 'pwa/data/core_bank.json.bak'
B2 = 'pwa/data/core_bank.json'
d1 = json.load(open(B1, encoding='utf-8'))
d2 = json.load(open(B2, encoding='utf-8'))

def build_index(data):
    idx = {}
    for s in data[0]['sections']:
        for q in s['questions']:
            for f in ('stem', 'answer', 'idea'):
                if f in q and q[f]:
                    idx[f'core-{q["no"]}.{f}'] = q[f]
    return idx

i1 = build_index(d1)
i2 = build_index(d2)
todo = json.load(open('tools/_todo_core.json', encoding='utf-8'))

def math_tokens(s):
    """提取数学语义 token：所有 LaTeX 命令名、数字、关键符号，忽略 $ 定界与空白"""
    toks = []
    for m in re.finditer(r'\\([a-zA-Z]+)', s):
        toks.append('C:' + m.group(1))
    for m in re.finditer(r'(?<![a-zA-Z\\])(\d+(?:\.\d+)?)', s):
        toks.append('N:' + m.group(1))
    # 关键独立符号（非命令数字内）
    for m in re.finditer(r'(?<![a-zA-Z\\])([+\\-×÷=<>≤≥≠≈±−])', s):
        toks.append('S:' + m.group(1))
    return toks

report = []
for k in todo:
    old = i1.get(k, '')
    new = i2.get(k, '')
    if old == new:
        report.append((k, 'unchanged'))
        continue
    t1, t2 = math_tokens(old), math_tokens(new)
    # multiset 比较
    from collections import Counter
    c1, c2 = Counter(t1), Counter(t2)
    added = c2 - c1
    removed = c1 - c2
    if not added and not removed:
        report.append((k, 'tokens-equal'))
    else:
        report.append((k, f'DIFF removed={dict(removed)} added={dict(added)}'))

n_diff = 0
for k, st in report:
    if st != 'tokens-equal' and st != 'unchanged':
        n_diff += 1
        print('!!!', k, '->', st[:200])
print('共处理字段:', len(report))
print('token 级内容一致:', sum(1 for _, s in report if s in ('tokens-equal', 'unchanged')))
print('疑似数学内容变化:', n_diff)