# -*- coding: utf-8 -*-
"""修复 2001数二真题-15（及 core_bank no=587 副本）的 ODE 解与最终答案。

正确解：f''+f=2e^x, f(0)=0, f'(0)=2 → f=sin x+e^x-cos x, g=cos x+sin x+e^x
  f(π)=e^π+1，积分 = (e^π+1)/(1+π) ≈ 5.8288
原库错误：f=sin x+e^x-1（把 -cos x 误写成 -1），答案 (e^π-1)/(1+π) ≈ 5.3459，
  且展开式首行多出 +f'(x)/(1+x) 一项（等式不成立）。
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM = os.path.join(ROOT, 'pwa', 'data', 'exam.json')
CORE = os.path.join(ROOT, 'pwa', 'data', 'core_bank.json')

ANSWER = r'''【解析】由 $f'(x)=g(x)$ 得 $f''(x)=g'(x)=2\mathrm{e}^{x}-f(x)$，即 $f''+f=2\mathrm{e}^{x}$。特征方程 $\lambda^{2}+1=0$，$\lambda=1$ 不是特征根，故取特解 $\mathrm{e}^{x}$，通解为 $f(x)=C_{1}\cos x+C_{2}\sin x+\mathrm{e}^{x}$。
由 $f(0)=C_{1}+1=0$ 得 $C_{1}=-1$；由 $f'(0)=C_{2}+1=g(0)=2$ 得 $C_{2}=1$。故
$$f(x)=\sin x+\mathrm{e}^{x}-\cos x,\qquad g(x)=f'(x)=\cos x+\sin x+\mathrm{e}^{x}.$$
（可验证 $f''+f=2\mathrm{e}^{x}$，$f(0)=0$，$g(0)=2$ 均成立。）
又 $\dfrac{\mathrm{d}}{\mathrm{d}x}\!\left[\dfrac{f(x)}{1+x}\right]=\dfrac{f'(x)(1+x)-f(x)}{(1+x)^{2}}=\dfrac{(1+x)g(x)-f(x)}{(1+x)^{2}}=\dfrac{g(x)}{1+x}-\dfrac{f(x)}{(1+x)^{2}}$，即被积函数恰为 $\left[\dfrac{f(x)}{1+x}\right]'$。
所以
$$\int_{0}^{\pi}\left[\frac{g(x)}{1+x}-\frac{f(x)}{(1+x)^{2}}\right]\mathrm{d}x
=\left[\frac{f(x)}{1+x}\right]_{0}^{\pi}=\frac{f(\pi)}{1+\pi}-f(0)=\frac{\sin\pi+\mathrm{e}^{\pi}-\cos\pi}{1+\pi}+0=\frac{\mathrm{e}^{\pi}+1}{1+\pi}.$$'''

IDEA = r'''**思路**：先由 $f'=g,\ g'=2e^x-f$ 得 $f''+f=2e^x$，解出 $f=\sin x+e^x-\cos x,\ g=\cos x+\sin x+e^x$，再把被积式凑成导数。
① $f''+f=2e^x$，$\lambda=1$ 非特征根 → 特解 $e^x$，通解 $f=C_1\cos x+C_2\sin x+e^x$；代入 $f(0)=0,f'(0)=g(0)=2$ 得 $C_1=-1,C_2=1$，即 $f=\sin x+e^x-\cos x$，$g=\cos x+\sin x+e^x$。
② 被积式 $=\left[\dfrac{f}{1+x}\right]'$（把 $f'=g$ 代入分子后与商导数吻合）。
③ 积分 $=\bigl[\tfrac{f(x)}{1+x}\bigr]_0^\pi=\tfrac{f(\pi)}{1+\pi}=\tfrac{e^\pi+1}{1+\pi}$（其中 $f(\pi)=e^\pi+1$）。'''

TIPS_GS = r'''$f'=g,\ g'=2\mathrm e^{x}-f$ 消元：$f''+f=2\mathrm e^{x}$；$\lambda=1$ 非特征根，特解取 $\mathrm e^{x}$，通解 $f=C_{1}\cos x+C_{2}\sin x+\mathrm e^{x}$。初值 $f(0)=0\Rightarrow C_{1}=-1$，$f'(0)=2\Rightarrow C_{2}=1$，故 $f=\sin x+\mathrm e^{x}-\cos x$。'''
TIPS_JQ = r'''被积式 $\dfrac{g}{1+x}-\dfrac{f}{(1+x)^{2}}$ 凑商导数：分母差一次幂 → $\left[\dfrac{f}{1+x}\right]'$（用 $f'=g$ 替换分子后恰好吻合）。'''
TIPS_YC = r'''两个初值 $f(0)=0$、$f'(0)=g(0)=2$ 缺一不可；$\lambda=1$ 非特征根，特解只能是 $e^x$ 而非 $Ae^x$ 再配常数，别把 $-\cos x$ 误写成常数 $-1$。'''
TIPS_ZY = r'''积分即原函数代端点：$\left[\dfrac{f(x)}{1+x}\right]_0^{\pi}=\dfrac{f(\pi)}{1+\pi}=\dfrac{\mathrm e^{\pi}+1}{1+\pi}$，其中 $f(\pi)=\sin\pi+\mathrm e^{\pi}-\cos\pi=\mathrm e^{\pi}+1$。'''


def patch_obj(q, prefix):
    old_ans = q.get('answer', '')
    q['answer'] = (ANSWER if prefix else ANSWER.replace('【解析】', '', 1))
    q['idea'] = (IDEA if prefix else IDEA.replace('**思路**：', '', 1))
    if prefix and isinstance(q.get('tips'), dict):
        q['tips']['gs'] = TIPS_GS
        q['tips']['jq'] = TIPS_JQ
        q['tips']['yc'] = TIPS_YC
        q['tips']['zy'] = TIPS_ZY
    return old_ans


def main():
    # exam.json —— 紧凑单行，默认分隔符
    with open(EXAM, encoding='utf-8') as f:
        exam = json.load(f)
    n = 0
    for p in exam:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                if p['id'] == '2001数二真题' and q['no'] == 15:
                    patch_obj(q, True); n += 1
    assert n == 1, f'exam 命中 {n} 处（应为 1）'
    with open(EXAM, 'w', encoding='utf-8', newline='') as f:
        json.dump(exam, f, ensure_ascii=False)

    # core_bank.json —— indent=1，无尾换行
    with open(CORE, encoding='utf-8') as f:
        core = json.load(f)
    m = 0
    for p in core:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                if q.get('linkedQid') == '2001数二真题-15':
                    patch_obj(q, False); m += 1
    assert m == 1, f'core 命中 {m} 处（应为 1）'
    with open(CORE, 'w', encoding='utf-8', newline='') as f:
        json.dump(core, f, indent=1, ensure_ascii=False)

    print(f'patched exam={n}, core={m}')


if __name__ == '__main__':
    main()
