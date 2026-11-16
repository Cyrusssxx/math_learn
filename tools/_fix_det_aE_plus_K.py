# -*- coding: utf-8 -*-
"""修正「aE+K 四阶行列式」题的思路说明。

数值答案 a^2(a^2-4) 正确，不动。
错误点：core-1180 的 idea 写「观察每列和得特征值 2」，
但 K 的每行每列元素和全是 0（K(1,1,1,1)^T=0），列和只能看出特征值 0；
特征值 ±2 来自分块 K=[[0,B],[B,0]]（B 的特征值 0,-2）。
dgy-9 的 idea 只笼统说「特征值易求」，补上严谨求法。

写回格式：
  core_bank.json = indent=1，无尾换行
  dgy_items.json = 紧凑单行（json.dumps 默认 separators），无尾换行
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa', 'data', 'core_bank.json')
DGY = os.path.join(ROOT, 'pwa', 'data', 'dgy_items.json')

NEW_IDEA_CORE = (
    '**思路：拆成 $aE+K$（$K$ 与 $a$ 无关的常数阵），用 $K$ 的特征值算 $|aE+K|$**。\n'
    '① 原矩阵 $=aE+K$（$K$ 为与 $a$ 无关的常数矩阵）；\n'
    '② 求 $K$ 的特征值：$K$ 每行每列元素和均为 $0$（$K(1,1,1,1)^{\\mathrm T}=0$），故 $0$ 是特征值；'
    '又 $K$ 可分块为 $\\begin{pmatrix}0&B\\\\B&0\\end{pmatrix}$，其中 $B=\\begin{pmatrix}-1&1\\\\1&-1\\end{pmatrix}$ '
    '的特征值为 $0,-2$，故 $K$ 的特征值为 $\\pm 0,\\ \\pm(-2)$，即 $0,0,2,-2$'
    '（**列和为 $0$ 只说明有特征值 $0$，特征值 $\\pm2$ 来自分块，如 $K(1,-1,-1,1)^{\\mathrm T}=2(1,-1,-1,1)^{\\mathrm T}$**）；\n'
    '③ $|aE+K|=\\prod_i(a+\\lambda_i)=a\\cdot a\\cdot(a+2)(a-2)=a^2(a^2-4)$。'
)

NEW_IDEA_DGY = (
    '把矩阵拆成 $aE+K$（$K$ 为与 $a$ 无关的 $\\pm1$ 常数阵），则 $|aE+K|=\\prod(a+\\lambda_i)$。'
    '$K$ 的特征值这样求：每行每列元素和为 $0$（$K(1,1,1,1)^{\\mathrm T}=0$），'
    '且分块 $K=\\begin{pmatrix}0&B\\\\B&0\\end{pmatrix}$（$B=\\begin{pmatrix}-1&1\\\\1&-1\\end{pmatrix}$ '
    '的特征值为 $0,-2$），故 $K$ 有特征值 $0,0,2,-2$；于是 $aE+K$ 的特征值为 $a,\\ a,\\ a+2,\\ a-2$，'
    '相乘得 $a^2(a^2-4)$。比直接展开 $4$ 阶行列式快得多。'
)


def load(path):
    with open(path, encoding='utf-8', newline='') as f:
        return json.load(f)


def save(path, data, indent):
    text = json.dumps(data, ensure_ascii=False, indent=indent)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def find(data, paper_id, no):
    for p in data:
        if p.get('id') != paper_id:
            continue
        for sec in p.get('sections', []):
            for q in sec.get('questions', []):
                if q.get('no') == no:
                    return q
    raise SystemExit('not found: %s - %s' % (paper_id, no))


# --- core-1180 ---
core = load(CORE)
q = find(core, 'core', 1180)
assert '观察每列和得特征值 $2$' in q['idea'], 'core-1180 前提不成立'
assert q['answer'].strip().startswith('$$'), 'core-1180 answer 结构异常'
q['idea'] = NEW_IDEA_CORE
save(CORE, core, 1)

# --- dgy-9 ---
dgy = load(DGY)
q = find(dgy, 'DG900JXB', 9)
assert '特征值易求' in q['idea'], 'dgy-9 前提不成立'
assert '【答案】' in q['answer'], 'dgy-9 answer 结构异常'
q['idea'] = NEW_IDEA_DGY
save(DGY, dgy, None)

print('修复完成：core-1180 idea、dgy-9 idea（数值答案未动）')
