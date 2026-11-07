# 一次性修复 core_bank.json no.583（2020 数一）：
# 把 answer 里「完整解析见下方图片」的占位说明，替换为答案册原图的完整文字解析。
# 格式铁律：json.loads -> 改 dict -> json.dumps(indent=1, ensure_ascii=False)，无尾换行。
import json

PATH = 'pwa/data/core_bank.json'

ANSWER = r"""【答案】$am+n$（即 $f'(0)+af(0)=n+am$）

**分析**：不必先解出 $f$。由方程得 $f=-f''-af'$，积分后只剩 $\bigl[-f'-af\bigr]_0^{+\infty}$；需要论证的是上限处 $f(x),f'(x)\to 0$，这由特征方程 $r^2+ar+1=0$ 的根实部恒为负保证，按判别式 $\Delta=a^2-4$ 分三种情况说明。

**第一步：证 $\lim_{x\to+\infty}f(x)=\lim_{x\to+\infty}f'(x)=0$**

特征方程 $r^2+ar+1=0$，$\Delta=a^2-4$。

**① $a\gt2$**：两个不同实根 $r_{1,2}=\dfrac{-a\pm\sqrt{a^2-4}}{2}$，因 $a\gt\sqrt{a^2-4}$，两根均小于 $0$。通解 $f(x)=C_1e^{r_1x}+C_2e^{r_2x}$，$f'(x)=C_1r_1e^{r_1x}+C_2r_2e^{r_2x}$，均趋于 $0$。

**② $a=2$**：二重根 $r=-1$，通解 $f(x)=(C_1+C_2x)e^{-x}$，$f'(x)=(C_2-C_1-C_2x)e^{-x}$，指数衰减压过一次多项式，仍趋于 $0$。

**③ $0\lt a\lt2$**：共轭复根 $r_{1,2}=-\dfrac{a}{2}\pm b i$，$b=\dfrac{\sqrt{4-a^2}}{2}$，通解 $f(x)=e^{-\frac{a}{2}x}\bigl(C_1\cos bx+C_2\sin bx\bigr)$，$f'(x)$ 形式相同。实部 $-\dfrac{a}{2}\lt0$，故 $f,f'\to0$。

三种情况都有 $\lim f=\lim f'=0$，反常积分收敛。

**第二步：把方程改写后积分**

由 $f''(x)+af'(x)+f(x)=0$ 得 $f(x)=-f''(x)-af'(x)$。对任意 $A\gt0$：
$$
\int_0^A f(x)\,\mathrm dx=-\int_0^A f''(x)\,\mathrm dx-a\int_0^A f'(x)\,\mathrm dx=\bigl[-f'(x)-af(x)\bigr]_0^A
$$
$$
=-f'(A)-af(A)+f'(0)+af(0).
$$
令 $A\to+\infty$，由第一步 $-f'(A)-af(A)\to0$，所以
$$
\int_0^{+\infty}f(x)\,\mathrm dx=f'(0)+af(0)=n+am=am+n .
$$

**易错点**：① 不验证 $f,f'\to0$ 就把上限当 $0$ 代入——$a\gt0$ 保证特征根实部为负，这一步才是本题考点；② 下限是减去 $-f'(0)-af(0)$，结果是 $+f'(0)+af(0)$，别写成 $-n-am$；③ $0\lt a\lt2$ 时解衰减振荡、$a=2$ 时重根带 $x$ 因子，两者仍收敛，别误判发散。"""

IDEA = r"""**思路概括：** 不求 $f$ 的具体解，由 $f=-f''-af'$ 直接积分，把反常积分化成边界项 $\bigl[-f'-af\bigr]_0^{+\infty}$；特征方程 $r^2+ar+1=0$ 按 $\Delta=a^2-4$ 分 $a\gt2$、$a=2$、$0\lt a\lt2$ 三种情况，均有特征根实部为负，故 $f,f'\to0$，只剩初值 $f'(0)+af(0)=n+am$。"""

d = json.loads(open(PATH, encoding='utf-8').read())
papers = d['papers'] if isinstance(d, dict) else d
n = 0
for p in papers:
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            if q.get('no') == 583:
                # 幂等：允许对「旧占位版」或「本次已改版」重复执行
                assert ('完整解析见下方图片' in q['answer']) or q['answer'].startswith('【答案】$am+n$'), \
                    '583 的 answer 已变成其它内容，请人工确认'
                assert '$am+n$' in q['answer'], '583 的答案不是 $am+n$，请人工确认'
                q['answer'] = ANSWER
                q['idea'] = IDEA
                n += 1
assert n == 1, '命中题数异常: %d' % n
out = json.dumps(d, indent=1, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(out)
print('no.583 已更新：answer %d 字、idea %d 字' % (len(ANSWER), len(IDEA)))
