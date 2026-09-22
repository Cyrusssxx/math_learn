# -*- coding: utf-8 -*-
# 修复 6 卷中「\neq 丢反斜杠 → eq」的错误（排除 \geq 等合法命令）
import json, io, re

P = 'D:/ai code/math-note/pwa/data/exam.json'
VOLS = {'2021数二真题', '2022数二真题', '2023数二真题', '2024数二真题', '2025数二真题', '2026数二真题'}


def fix_eq(s):
    """把裸 eq（非命令内）替换为 \\neq"""
    out = []
    i = 0
    while True:
        m = re.search(r'(?<![\\])eq(?![a-zA-Z])', s[i:])
        if not m:
            out.append(s[i:])
            break
        pos = i + m.start()
        out.append(s[i:pos])
        pre = s[:pos]
        # eq 前若是 \命令的字母尾部（如 \geq 的 g）→ 不替换
        if re.search(r'\\[a-zA-Z]+$', pre):
            out.append('eq')
        else:
            out.append('\\neq')
        i = pos + 2
    return ''.join(out)


exam = json.load(io.open(P, encoding='utf-8'))
fixed = 0
for v in exam:
    if v['id'] not in VOLS:
        continue
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            for f in ('stem', 'answer', 'idea', 'tips'):
                t = q.get(f) or ''
                if isinstance(t, dict):
                    nv = {}
                    for k, val in t.items():
                        ns = fix_eq(str(val))
                        nv[k] = ns if ns != val else val
                        if ns != val:
                            fixed += 1
                    q[f] = nv
                else:
                    ns = fix_eq(t)
                    if ns != t:
                        q[f] = ns
                        fixed += 1

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('替换处数:', fixed)

# 复查
exam2 = json.load(io.open(P, encoding='utf-8'))
left = 0
for v in exam2:
    if v['id'] not in VOLS:
        continue
    for s in v.get('sections', []):
        for q in s.get('questions', []):
            for f in ('stem', 'answer', 'idea', 'tips'):
                t = q.get(f) or ''
                if isinstance(t, dict):
                    t = json.dumps(t, ensure_ascii=False)
                for m in re.finditer(r'(?<![\\])eq(?![a-zA-Z])', t):
                    pre = t[:m.start()]
                    if not re.search(r'\\[a-zA-Z]+$', pre):
                        left += 1
print('残留裸 eq:', left)
