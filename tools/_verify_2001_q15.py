# -*- coding: utf-8 -*-
"""字段级 diff 验证：对照 git HEAD 的原始 exam/core，只允许 answer/idea/tips 变化。"""
import json, subprocess, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def head_json(path):
    out = subprocess.check_output(['git', '-C', ROOT, 'show', 'HEAD:' + path])
    return json.loads(out.decode('utf-8'))


def local_json(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return json.load(f)


def find_q(d, pid, no):
    for p in d:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                if p['id'] == pid and q['no'] == no:
                    return q
    return None


def find_linked(d, lq):
    for p in d:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                if q.get('linkedQid') == lq:
                    return q
    return None


def diff_keys(o, n):
    return sorted(k for k in (set(o) | set(n)) if o.get(k) != n.get(k))


eo, en = head_json('pwa/data/exam.json'), local_json('pwa/data/exam.json')
co, cn = head_json('pwa/data/core_bank.json'), local_json('pwa/data/core_bank.json')

oq, nq = find_q(eo, '2001数二真题', 15), find_q(en, '2001数二真题', 15)
oc, nc = find_linked(co, '2001数二真题-15'), find_linked(cn, '2001数二真题-15')
assert oq and nq and oc and nc

c1, c2 = diff_keys(oq, nq), diff_keys(oc, nc)
print('exam changed:', c1)
print('core changed:', c2)
assert set(c1) <= {'answer', 'idea', 'tips'}, c1
assert set(c2) <= {'answer', 'idea', 'tips'}, c2

# 除目标题外，所有卷/题对象必须完全一致
for i, (a, b) in enumerate(zip(eo, en)):
    assert a.get('id') == b.get('id'), ('exam paper id', i)
    if a['id'] == '2001数二真题':
        for j, (sa, sb) in enumerate(zip(a['sections'], b['sections'])):
            for k, (qa, qb) in enumerate(zip(sa['questions'], sb['questions'])):
                if qa['no'] != 15:
                    assert qa == qb, ('exam other q', i, j, k)
    else:
        assert a == b, ('exam other paper', i)
for i, (a, b) in enumerate(zip(co, cn)):
    for j, (sa, sb) in enumerate(zip(a['sections'], b['sections'])):
        for k, (qa, qb) in enumerate(zip(sa['questions'], sb['questions'])):
            if qa.get('linkedQid') != '2001数二真题-15':
                assert qa == qb, ('core other q', i, j, k)
print('所有其他题目逐字段一致 OK')

# 内容断言
a = nq['answer']
assert '\\mathrm{e}^{\\pi}+1' in a or 'e^{\\pi}+1' in a, '缺正确答案 +1'
assert '\\mathrm{e}^{\\pi}-1' not in a and 'e^{\\pi}-1' not in a, '残留错误答案 -1'
assert '\\sin x+\\mathrm{e}^{x}-\\cos x' in a, '缺正确 f'
assert '\\cos x+\\sin x+\\mathrm{e}^{x}' in a, '缺正确 g'
assert '数值' not in a
print('内容断言 OK: f=sin x+e^x-cos x, 答案=(e^π+1)/(1+π)')
