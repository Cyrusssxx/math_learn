# -*- coding: utf-8 -*-
"""精确扫描：只报真实问题（去掉误报规则）
真实问题 = ①$$ 块奇数（未闭合） ②【答案】【答案】重复 ③\begin 无 \end ④答案末尾截断（无句号/无$收尾）
"""
import json, io, re


def env_problems(t):
    p = []
    if t.count('$$') % 2 != 0:
        p.append(f'$$奇数({t.count("$$")})')
    for env in ('aligned', 'cases', 'matrix', 'pmatrix', 'bmatrix', 'vmatrix', 'array', 'split'):
        b = len(re.findall(r'\\begin\{' + env + r'\}', t))
        e = len(re.findall(r'\\end\{' + env + r'\}', t))
        if b != e:
            p.append(f'{env}({b}/{e})')
    return p


files = {
    'core_bank': 'pwa/data/core_bank.json',
    'exam': 'pwa/data/exam.json',
    'xd_bank': 'pwa/data/xd_bank.json',
}
total = 0
for name, fp in files.items():
    try:
        with io.open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        continue
    items = []
    if name == 'exam':
        for p in data:
            for s in p.get('sections', []):
                for q in s.get('questions', []):
                    items.append((f"{p['id']}", q))
    else:
        for p in data:
            for s in p.get('sections', []):
                for q in s.get('questions', []):
                    items.append((p.get('id'), q))
    rows = []
    for tag, q in items:
        ans = str(q.get('answer') or '')
        issues = []
        if '【答案】【答案】' in ans:
            issues.append('答案头重复')
        ep = env_problems(ans)
        if ep:
            issues.append('公式未闭合:' + ';'.join(ep))
        if len(ans) > 1500:
            issues.append(f'超长({len(ans)}字)')
        if issues:
            rows.append((tag, q.get('no'), issues))
    print(f'===== {name}：{len(rows)} 处真实问题 =====')
    for tag, no, issues in rows:
        total += 1
        print(f'  [{tag}] no={no} | {"; ".join(issues)}')
print(f'\n合计 {total} 处')
