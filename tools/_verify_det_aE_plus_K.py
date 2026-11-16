# -*- coding: utf-8 -*-
"""字段级 diff + 公式片段比对：验证只改了 core-1180 / dgy-9 的 idea。"""
import json
import re
import subprocess
from collections import Counter

ROOT = '.'


def head(p):
    return json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', 'HEAD:' + p]).decode('utf-8'))


def loc(p):
    return json.load(open(p, encoding='utf-8'))


def find(d, pid, no):
    for p in d:
        for sec in p['sections']:
            for q in sec.get('questions', []):
                if p['id'] == pid and q['no'] == no:
                    return q
    raise AssertionError('not found %s %s' % (pid, no))


def questions(d):
    for p in d:
        for sec in p['sections']:
            for q in sec.get('questions', []):
                yield q


RF = re.compile(r'\$\$([\s\S]*?)\$\$|\$([^\$\n]+)\$')


def frags(t):
    return [(m.group(1) if m.group(1) is not None else m.group(2)).strip()
            for m in RF.finditer(t or '')]


# --- core-1180 ---
co, cn = head('pwa/data/core_bank.json'), loc('pwa/data/core_bank.json')
oq, nq = find(co, 'core', 1180), find(cn, 'core', 1180)
ch = [k for k in set(oq) | set(nq) if oq.get(k) != nq.get(k)]
print('core-1180 changed:', ch)
assert ch == ['idea']
assert '观察每列和' not in nq['idea']
assert '每列元素和均为 $0$' in nq['idea']
assert 'bmtr' not in nq['idea']
# answer / idea 其他字段数学公式：answer 零改动；idea 是重写，核对关键公式存在
assert frags(oq['answer']) == frags(nq['answer']), 'core answer 公式被改'
assert 'a^2(a^2-4)' in nq['idea']
assert '0,0,2,-2' in nq['idea']

# --- dgy-9 ---
do, dn = head('pwa/data/dgy_items.json'), loc('pwa/data/dgy_items.json')
oq, nq = find(do, 'DG900JXB', 9), find(dn, 'DG900JXB', 9)
ch = [k for k in set(oq) | set(nq) if oq.get(k) != nq.get(k)]
print('dgy-9 changed:', ch)
assert ch == ['idea']
assert '特征值易求' not in nq['idea']
assert frags(oq['answer']) == frags(nq['answer']), 'dgy answer 公式被改'
assert '0,0,2,-2' in nq['idea']

# --- 全库其他题零改动 ---
for a, b in zip(questions(co), questions(cn)):
    if a.get('no') == 1180 and a.get('linkedQid') == '2020数二真题-14':
        continue  # 唯一目标题（core-1180 / linked 真题-14）
    assert a == b, 'core 有非目标题变化'
for a, b in zip(questions(do), questions(dn)):
    if a.get('no') == 9:
        continue
    assert a == b, 'dgy 有非目标题变化'

# --- 新 idea 的 LaTeX 结构自检（括号/环境配对）---
for t in (find(cn, 'core', 1180)['idea'], find(dn, 'DG900JXB', 9)['idea']):
    assert t.count('\\begin{pmatrix}') == t.count('\\end{pmatrix}'), 'pmatrix 不配对'
    assert t.count('$') % 2 == 0, '$ 不配对'
    assert '\\\\' in t, '矩阵换行符缺失'

print('OK：全库仅 2 处 idea 变化，数值答案零改动，LaTeX 结构配对正常')
