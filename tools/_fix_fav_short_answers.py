# -*- coding: utf-8 -*-
"""修复「收藏 ∩ 不熟/不会」简短答案审校中发现的 4 处文本错误。

只改 answer/idea/tips 的文本措辞，数学结论本身不动（2019-5 的 tips 是串题的错误内容，
按题干与正确 answer 重写为自洽版本）。

  1. exam.json 2019数二真题-5：tips.jq/yc/zy 串入别的题的 √(6+r²)、且 zy 写反大小关系
  2. core_bank core-2051：tips 串入秩不等式 r(A)+r(B)-n，与实对称矩阵命题无关
  3. core_bank core-1125：idea 首句写 A(1,1,1,1)^T=β，与正确特解 (1,1,2,3)^T 矛盾
  4. core_bank core-2026：tips.zy 自相矛盾（「实对称是充分条件，不是必要条件」却又说「必是实对称」）

写回格式：exam.json 单行紧凑无尾换行；core_bank.json indent=1 无尾换行。
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM = os.path.join(ROOT, 'pwa', 'data', 'exam.json')
CORE = os.path.join(ROOT, 'pwa', 'data', 'core_bank.json')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def save_json(p, obj, indent=None):
    text = json.dumps(obj, ensure_ascii=False, indent=indent)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def find(d, pid, no, linked=None):
    for p in d:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                if linked is not None:
                    if q.get('linkedQid') == linked:
                        return q
                elif p['id'] == pid and q['no'] == no:
                    return q
    raise AssertionError(f'not found: {pid} {no} {linked}')


# ---------- 1. exam.json 2019数二真题-5 ----------
exam = load(EXAM)
q = find(exam, '2019数二真题', 5)
if '6+r^{2}' in q['tips']['jq']:
    q['tips']['jq'] = r'三积分同区域 $D$，只比被积函数：$I_1=\iint r$、$I_2=\iint\sin r$、$I_3=\iint(1-\cos r)$，其中 $r=\sqrt{x^2+y^2}\le\frac\pi2$。'
    q['tips']['yc'] = r'在 $0<r\le\frac\pi2$ 上 $1-\cos r<\sin r<r$（$\sin r<r$；$\sin r-(1-\cos r)=\sin r+\cos r-1>0$，因 $r>0$ 时 $\sin r+\cos r>1$）。'
    q['tips']['zy'] = r'答案 A（逐点 $1-\cos r<\sin r<r$ ⟹ $I_3<I_2<I_1$）。'
    save_json(EXAM, exam, indent=None)
    print('exam 2019-5 tips 已修复')
else:
    print('exam 2019-5 已是修复后版本，跳过')

# ---------- 2-4. core_bank.json ----------
core = load(CORE)

c2051 = find(core, 'core', 2051)
assert 'r(A)+r(B)' in c2051['tips']['gs'], 'core-2051 前提不成立'
c2051['tips'] = {
    'gs': r'实对称矩阵可正交对角化，特征值 $\lambda_i$ 全实：$\operatorname{tr}(A^2)=\sum\lambda_i^2\ge0$；$A^2+E$ 特征值 $\lambda_i^2+1>0$ 故可逆。',
    'zy': r'$A^2=A$（幂等）⟹ 特征值只取 $0$ 或 $1$，$r(A)=1$ 的个数 $=\operatorname{tr}(A)$，故不存在「$A^2=A$ 但 $\operatorname{tr}(A)\ne r(A)$」；选 C。',
}

c1125 = find(core, 'core', 1125)
assert 'A(1,1,1,1)' in c1125['idea'], 'core-1125 前提不成立'
c1125['idea'] = c1125['idea'].replace('A(1,1,1,1)', 'A(1,1,2,3)')

c2026 = find(core, 'core', 2026)
assert '不是必要条件' in c2026['tips']['zy'], 'core-2026 前提不成立'
c2026['tips']['zy'] = r'实对称 ⟺ 可正交对角化（充要）：对称保证可正交对角化；反之若 $A=Q\Lambda Q^{\mathrm T}$（$Q$ 正交）则 $A^{\mathrm T}=A$。别把「实对称」只当充分条件。'

# 5. core-728（linkedQid=DG900JXB-303）：idea 首句误称「左乘或右乘 B 不改解集、ABx=b 与 BAx=b 都与 Ax=b 同解」，
#    但答案自己判定 B 错误正是因 BAx=b ⟺ Ax=B⁻¹b 右端变了 —— 首句与答案自相矛盾。
#    dgy 原卷同题 idea 无此错误首句，按正确逻辑重写首句。
c728 = None
for p in core:
    for s in p['sections']:
        for qq in s['questions']:
            if qq.get('linkedQid') == 'DG900JXB-303':
                c728 = qq
                break
assert c728 is not None and '不改解集' in c728['idea'], 'core-728 前提不成立'
old_head = c728['idea'].split('\n')[0]
c728['idea'] = c728['idea'].replace(
    old_head,
    r'**思想：右乘可逆矩阵 $B$ 只换元 $x\to B^{-1}x$（$ABx=b$ 与 $Ax=b$ 解集一一对应）；左乘 $B$ 把右端改成 $B^{-1}b$（$BAx=b\iff Ax=B^{-1}b$），未必与 $Ax=b$ 同解**。',
    1)

save_json(CORE, core, indent=1)

print('修复完成：exam 2019-5 tips；core 2051 tips / 1125 idea / 2026 tips / 728 idea')
