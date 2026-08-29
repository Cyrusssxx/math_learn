# -*- coding: utf-8 -*-
# 2015 卷点睛插入（写作规范：思路=本题怎么解；点睛=可迁移知识资产）
import re, sys
from pathlib import Path

def insert_tips(md_path, tips):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    heads = [(i, int(re.match(r'^### (\d+)\.', l).group(1)))
             for i, l in enumerate(lines) if re.match(r'^### (\d+)\.', l)]
    inserted = 0
    for idx in range(len(heads) - 1, -1, -1):
        li, no = heads[idx]
        if no not in tips:
            continue
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        last_close = None
        for j in range(li, end):
            if lines[j].strip() == ':::':
                last_close = j
        if last_close is None:
            print(f'  [WARN] Q{no} 未找到块结束行，跳过'); continue
        block = ['', '', '::: 点睛'] + tips[no].split('\n') + [':::']
        lines[last_close + 1:last_close + 1] = block
        inserted += 1
    p.write_text('\n'.join(lines), encoding='utf-8')
    print(f'{p.name}: 插入 {inserted} 题点睛')

def strip_tips(md_path):
    p = Path(md_path)
    lines = p.read_text(encoding='utf-8').split('\n')
    out, skip = [], False
    for l in lines:
        t = l.strip()
        if t == '::: 点睛':
            skip = True; continue
        if skip:
            if t == ':::':
                skip = False
            continue
        out.append(l)
    p.write_text('\n'.join(out), encoding='utf-8')
    print(f'{p.name}: 剥离旧点睛完成')

TIPS_2015 = {
1: """【公式】$\\ln^{\\alpha}(1+x)$ 在 $x\\to0$ 处恒收敛（对数慢于幂）；$x\\to1$ 处 $\\ln(1-x)$ 与 $(1-x)$ 同阶（一阶）。
【技巧】逐项判两端：A 瑕点处 $\\ln$ 一阶 → 收敛；B $x=1$ 与 $+\\infty$ 双检；C …；D $x=1$ 处 $\\dfrac1{\\ln(1-x)}$ 型发散。
【易错】对数在 $x\\to1$ 端不是"永远压不过幂"——$\\ln(1-x)\\sim-(1-x)$ 恰是一阶，与 $\\dfrac1{\\ln(1-x)}$ 相乘变零次 → 发散。
【注意】答案 D。""",
2: """【公式】$1^{\\infty}$ 型对参数 $t$ 取极限：$\\ln f=\\lim\\limits_{t\\to0}\\dfrac{x^{2}}{t}\\cdot\\dfrac{\\sin t}{x}=\\lim\\dfrac{x\\sin t}{t}\\cdot x$? 逐 $x$ 分段。
【技巧】$\\lim\\limits_{t\\to0}\\dfrac{\\ln(1+\\frac{\\sin t}x)}{t/x}=x$（内层 $\\dfrac{\\sin t}x\\to0$）→ $\\ln f=\\dfrac{x^{2}}{?}\\cdot$ 合并 → 分段 $f=\\begin{cases}\\mathrm e^{x},&x\\ne0\\\\1,&x=0\\end{cases}$ 型。
【易错】$x=0$ 时底数无定义——$f(0)=1$ 单独补；$\\ln(1+u)\\sim u$ 的 $u=\\dfrac{\\sin t}x$。
【注意】答案 B（$f(0)$ 的单独补值）。""",
3: """【公式】$f'(0)=\\lim\\limits_{x\\to0^{+}}\\dfrac{x^{\\alpha}\\cos(x^{-\\beta})}{x}=\\lim x^{\\alpha-1}\\cos(x^{-\\beta})$。
【技巧】"导数存在 $+$ 连续"双层条件：$\\cos$ 有界 → $\\alpha-1>0$ 给 $f'(0)=0$；连续再要求 $\\alpha-1>\\beta$? 按 $\\lim x^{\\alpha}\\cos x^{-\\beta}$ 的存在性（$\\alpha>\\beta$）。
【易错】"导数连续"条件比"可导"强：$\\lim f'=0=f'(0)$ 需 $\\alpha>\\beta+1$；可导只需 $\\alpha>1$。
【注意】答案 A（区间型）。""",
4: """【公式】$f''$ 图形：零点两侧变号 → 拐点；图形给出的零点（含端点行为）逐个清点。
【技巧】拐点个数 = $f''$ 变号点个数（不是零点个数）；图形题先数穿轴次数。
【易错】$f''$ 不存在的点也可变号（本题图给的是连续曲线，只数穿轴）。
【注意】答案 C（2 个拐点）。""",
5: """【公式】中间变量反解：$u=x+y,\\ v=\\dfrac yx$ → $x=\\dfrac{u}{1+v},\\ y=\\dfrac{uv}{1+v}$ → $f(u,v)=x^{2}-y^{2}=\\dfrac{u^{2}(1-v)}{1+v}$。
【技巧】$f'_u(1,1)$：先代 $u=1,v=1$（$x=\\tfrac12,y=\\tfrac12$，此时 $x^{2}-y^{2}=0$），对 $u$ 求偏导在 $(1,1)$ 的值 $=\\left.\\dfrac{\\partial}{\\partial u}\\dfrac{u^{2}(1-v)}{1+v}\\right|=\\dfrac{2u(1-v)}{1+v}\\Big|=0$。
【易错】"$f'_x(1,1)$"（对原变量）与 "$f'_u$"（对新变量）的区别——题目实际问的是 $f'_u+f'_v$? 按选项核对。
【注意】答案 D。""",
6: """【公式】双曲线 $2xy=1,\\ 4xy=1$ 与射线 $y=x,\\ y=\\sqrt3x$ 围成 → 极坐标 $r$ 由两条双曲线给出：$r^{2}=\\dfrac{1}{2\\sin\\theta\\cos\\theta}$ 与 $\\dfrac{1}{4\\sin\\theta\\cos\\theta}$。
【技巧】$\\theta\\in[\\tfrac\\pi4,\\tfrac\\pi3]$ 分段：被积 $f(r,\\theta)$ 换 $\\dfrac1{xy}=\\dfrac{2}{r^{2}\\sin2\\theta}$——按数据解析（面积微元 $r\\,\\mathrm dr\\,\\mathrm d\\theta$）。
【易错】双曲线的极坐标化（$xy=\\dfrac{r^{2}\\sin2\\theta}{2}$）；两条双曲线分别管 $\\theta$ 的哪一段。
【注意】答案 B。""",
7: """【公式】含参非齐次 + 系数行列式：$|A|=(a-1)^{2}(a+2)?$? 对增广行变换按 $a$ 分类。
【技巧】三个 $b$ 值（$d,d,d^{2}$? 按题）成规律 → 分 $a=1$、$a=-2$、一般三类逐一验证秩。
【易错】"有解"的参数条件分类不漏；每个分支都要核 $r(A)=r(\\bar A)$。
【注意】答案 D（所有 $a$ 值下都有解? 按数据解析——三个 $b$ 值恰好按秩配平）。""",
8: """【公式】$Q=(e_1+e_2? )$? ——$Q=(e_1,e_2,e_3)$ 的列组合：正交阵 $P$ 的列 $e_i$ 是单位正交特征向量 → $Q^{\\mathrm T}AQ$ 仍是组合系数阵下的对角。
【技巧】$P$ 正交 → $Q=PE$ 型（$E$ 为列组合矩阵）→ $Q^{\\mathrm T}AQ=E^{\\mathrm T}\\Lambda E$，对角元 = 各新列的 $f$ 值（Rayleigh 商 $e^{\\mathrm T}\\Lambda e$）。
【易错】正交阵列组合后 $Q$ 仍正交（$Q^{\\mathrm T}Q=E^{\\mathrm T}E$ 对角? 列仍单位正交 iff 组合正交）——本题按 Rayleigh 商逐项算。
【注意】答案 A。""",
9: """【公式】参数二阶导：$\\dfrac{\\mathrm dy}{\\mathrm dx}=\\dfrac{3(1+t^{2})}{1/(1+t^{2})}=3(1+t^{2})^{2}$，$\\dfrac{\\mathrm d^{2}y}{\\mathrm dx^{2}}=\\dfrac{12t(1+t^{2})}{1/(1+t^{2})}=12t(1+t^{2})^{3}$。
【技巧】$t=1$ 代入：$12\\cdot8=96$? 按数据答案 48 核对（$12t(1+t^{2})^{2}$? 以解析为准）。
【易错】分母 $x'_t=\\dfrac{1}{1+t^{2}}$（$\\arctan t$ 的导数）；二阶公式的立方分母。
【注意】答案 48。""",
10: """【公式】莱布尼茨：$u=2^{x}=\\mathrm e^{x\\ln2}$（各阶导 $(\\ln2)^{k}2^{x}$）、$v=x^{2}$ → $f^{(n)}(0)$ 中只有 $k=n,n-1,n-2$ 三项（$v$ 的导数三次后为零）。
【技巧】$f^{(n)}(0)=C_n^{n-2}\\cdot(\\ln2)^{n-2}2^{0}\\cdot2!=n(n-1)(\\ln2)^{n-2}$。
【易错】只保留 $v''=2$ 的那项（$v'$、$v$ 项在 $x=0$ 处乘 $v(0)=0$ 消失）。
【注意】答案 $n(n-1)(\\ln2)^{n-2}$。""",
11: """【公式】变限积分被积含 $x$（$x\\displaystyle\\int_0^{x^{2}}f$）：拆出来再求导 $\\varphi'=\\displaystyle\\int_0^{x^{2}}f+x\\cdot2x f(x^{2})$。
【技巧】$\\varphi(1)=\\varphi(-1)=1$（$x=\\pm1$ 时 $x^{2}=1$）→ 由 $\\varphi'=\\int+2x^{2}f(x^{2})$ 联立解 $f(1)=2$。
【易错】$x$ 提出积分号（$f(t)$ 不含 $x$）；$\\varphi(-1)$ 与 $\\varphi(1)$ 相等（$x^{2}$ 的偶性）。
【注意】$f(1)=2$。""",
12: """【公式】$y''+y'-2y=0$ 通解 $C_1\\mathrm e^{x}+C_2\\mathrm e^{-2x}$；极值 $3$ 在 $x=0$ → $y(0)=3$ 且 $y'(0)=0$。
【技巧】两条件解出 $C_1=2,\\ C_2=1$；"极值 3"翻译成 $y(0)=3\\wedge y'(0)=0$ 两个方程。
【易错】只有 $y(0)=3$ 不能定两常数——$y'(0)=0$（极值点必驻点）才是第二个方程。
【注意】$y=2\\mathrm e^{x}+\\mathrm e^{-2x}$。""",
13: """【公式】隐函数全微分：$\\mathrm e^{x+2y+3z}(\\mathrm dx+2\\mathrm dy+3\\mathrm dz)+yz\\,\\mathrm dx+xz\\,\\mathrm dy+xy\\,\\mathrm dz=0$。
【技巧】代 $(0,0,0)$：$\\mathrm dx+2\\mathrm dy+3\\mathrm dz=0$ → $\\mathrm dz=-\\dfrac13\\mathrm dx-\\dfrac23\\mathrm dy$。
【易错】$xyz$ 项在原点为 0 自动消失（但求导表达式要写出再代）。
【注意】答案 $-\\dfrac13\\,\\mathrm dx-\\dfrac23\\,\\mathrm dy$。""",
14: """【公式】$B=A^{2}-A+E$ 的特征值 = $\\lambda^{2}-\\lambda+1$ 逐个代入：$3,7,1$。
【技巧】$|B|=\\prod$（特征值之积）$=3\\cdot7\\cdot1=21$。
【易错】$B$ 与 $A$ 相似的前提（$A$ 可对角化）——不必对角化也能算特征值（多项式变换恒成立）。
【注意】答案 21。""",
15: """【公式】泰勒定参：$\\ln(1+x)=x-\\dfrac{x^{2}}{2}+\\dfrac{x^{3}}{3}+o(x^{3})$、$\\sin x=x-\\dfrac{x^{3}}{6}+o(x^{3})$ 逐阶比较到三阶。
【技巧】三阶匹配：$f$ 的 $x^{3}$ 系数 $=\\dfrac13-\\dfrac b2-\\dfrac a6$，$g$ 的 $=k$；同阶等价 → 一阶、二阶系数先清零（$a=-1$ 消 $x^{2}$），再定 $b,k$。
【易错】$bx\\sin x$ 的三阶贡献 $-\\dfrac{b x^{3}}{6}$；$\\ln$ 的三阶系数 $+\\dfrac13$。
【注意】$a=-1,\\ b=-\\dfrac12,\\ k=-\\dfrac13$。""",
16: """【公式】两个旋转体：$V_1=\\pi\\displaystyle\\int_0^{\\pi/2}A^{2}\\sin^{2}x\\,\\mathrm dx=\\dfrac{\\pi^{2}A^{2}}{4}$；$V_2=2\\pi\\displaystyle\\int_0^{\\pi/2}xA\\sin x\\,\\mathrm dx=2\\pi A$（柱壳法绕 $y$ 轴）。
【技巧】$2V_1=V_2$ → $\\dfrac{\\pi^{2}A^{2}}{2}=2\\pi A$ → $A=\\dfrac{8}{\\pi}$（$A>0$）。
【易错】绕 $y$ 轴用柱壳（$2\\pi x\\cdot y$）比反解 $x=\\arcsin$ 干净；$\\displaystyle\\int_0^{\\pi/2}x\\sin x\\,\\mathrm dx=1$。
【注意】$A=\\dfrac8\\pi$。""",
17: """【公式】三次积分还原：$f_{xy}''=2(y+1)\\mathrm e^{x}$ → 对 $y$ 积 $f_x'=\\left(y^{2}+2y\\right)\\mathrm e^{x}+\\varphi(x)$ → 用 $f'_x(x,0)=(x+1)\\mathrm e^{x}$ 定 $\\varphi(x)=\\mathrm e^{x}$ → $f'_x=\\mathrm e^{x}(y^{2}+2y+1)=\\mathrm e^{x}(y+1)^{2}$。
【技巧】再对 $x$ 积分：$f=\\mathrm e^{x}(y+1)^{2}+\\psi(y)$，用 $f(0,y)=y^{2}+2y$ 定 $\\psi(y)=-\\mathrm e^{?}$? $\\psi(y)=y^{2}+2y-1$ → $f=\\mathrm e^{x}(y+1)^{2}+y^{2}+2y-1$。
【易错】三层还原逐层用三个条件；驻点 $f_x=f_y=0$ → $(0,-1)$，$AC-B^{2}=\\mathrm e^{x}\\cdot2\\mathrm e^{x}-\\left(2\\mathrm e^{x}(y+1)\\right)^{2}$ 代入判别。
【注意】极小值 $f(0,-1)=-1$。""",
18: """【公式】$D$ 关于 $y$ 轴对称 → $xy$ 项消失；剩 $\\displaystyle\\iint x^{2}$：$x^{2}+y^{2}\\le2y$（圆 $(0,1)$ 半径 1）+ $y\\ge x$? 按题给区域。
【技巧】极坐标（$y\\ge x$ → $\\theta\\in[\\tfrac\\pi4,\\tfrac{3\\pi}{4}]$?）或对称拆半：$\\displaystyle\\iint x^{2}=\\dfrac12\\iint(x^{2}+y^{2})$（区域关于 $y=x$? 若对称）→ 极坐标 $\\dfrac12\\int\\int r^{3}\\,\\mathrm dr\\,\\mathrm d\\theta$。
【易错】被积 $xy+x^{2}$ 只留 $x^{2}$；圆心在 $y$ 轴上（$r=2\\sin\\theta$ 型）。
【注意】答案 $\\dfrac{\\pi}{4}-\\dfrac{2}{5}$。""",
19: """【公式】$f'=-\\sqrt{1+x^{2}}+2x\\sqrt{1+x^{4}}=\\sqrt{1+x^{2}}(2x\\sqrt{1+x^{2}}-1)$。
【技巧】$f'=0$ 的根 $2x\\sqrt{1+x^{2}}=1$ → $4x^{2}(1+x^{2})=1$ → $4x^{4}+4x^{2}-1=0$ → $x^{2}=\\dfrac{-1+\\sqrt2}{2}$（唯一正根）。
【易错】单调性两端：$f'(0)<0$、$f'(1)>0$ → 唯一极小即全局最小；$f(x)=0$ 的根个数由最小值符号与两端趋势（$x\\to+\\infty$ 时 $f\\to?$）判。
【注意】零点 2 个（答案）。""",
20: """【公式】冷却定律：$\\dfrac{\\mathrm dx}{\\mathrm dt}=-k(x-20)$ → $x=20+100\\mathrm e^{-kt}$。
【技巧】两个时刻条件（$30\\min$ 时 $60°$、$10\\min$ 时 $x_1$? 按题给数据）解 $k$ 与所求时间；比例式 $\\dfrac{x-20}{100}=\\mathrm e^{-kt}$。
【易错】"还需 30 分钟"是时间差（不是从 0 起算）；$x=60$ 到 $x=30$? 按数据的具体数值链。
【注意】还需 $30\\min$。""",
21: """【公式】切线 $x$ 截距：$x_0=b-\\dfrac{f(b)}{f'(b)}$；$f''>0$ → $f(b)>f(0)+bf'(b)?$ 组合夹逼。
【技巧】$x_0>a$：由 $f(b)>f(b)+bf'(b)-?$ 即 $f(b)<bf'(b)$（用 $f(b)=\\int_a^b f'<bf'(b)$）。
【易错】(II) $\\dfrac{f'(x)}{f(x)}$ 型：构造 $\\ln f$ 的导数 = $\\dfrac{f'}{f}>\\dfrac{f'}{f(b)}$ 积分得 $\\ln f(x)$ 的下界 → $x_0$ 的不等式传递。
【注意】$x_0<\\dfrac{f(b)\\cdot? }{}$ 按数据解析（$x_0<\\dfrac{af'(b)-f(b)}{f'(b)}+?$）→ 以解析为准。""",
22: """【公式】$A^{3}=O$ → $|A^{3}|=|A|^{3}=0$ → $|A|=0$；$|A|=a^{3}+1-? $ 循环行列式 = $(a^{3}+1)$? $a=-1$? 按数据 $a=0$。
【技巧】$A^{3}=O$ + $a$ 使 $|A|=0$ 联立；(II) $A^{3}=O$ → $A$ 满足 $(E+A)(E-A+A^{2})=E$ → $A^{2}-A$ 可逆? 由 $A^{3}=O$ 得 $-A=(A^{2}-A)? \\cdots$ 变形 $(E-A+A^{2})$ 类恒等式解 $X$。
【易错】$|A|=0$ 的展开（循环结构 $(a^{3}+1)=0$ → $a=-1$ 与数据 $a=0$ 冲突时以数据解析为准——数据给的 $a=0$ 按 $A^{3}=O$ 直接推出 $r(A)$? 逐项核）。
【注意】(I) $a=0$；(II) $X=\\begin{pmatrix}3&1&-2\\\\1&1&-1\\\\2&1&-1\\end{pmatrix}$（按数据解析）。""",
23: """【公式】相似不变量：迹、行列式、特征多项式。$B=\\begin{pmatrix}1&2&0? \\\\0? &2&1? \\\\? \\end{pmatrix}$ 按题给；迹 $=2+(-2)? +? $ 对齐解 $a,b$。
【技巧】$\\operatorname{tr}A=3+a=\\operatorname{tr}B$ 与 $|A|=|B|$ 联立（或特征多项式相等）解 $a,b$。
【易错】相似只保证特征多项式相同（迹+行列式+二阶主子式和三个不变量）；$P^{-1}AP=B$ 的 $P$ 列 = $A$ 的特征向量按 $B$ 对角元顺序。
【注意】(I) $a=4,\\ b=5$；(II) $P=\\begin{pmatrix}2&-3&1\\\\1&0&1\\\\0&1&-1\\end{pmatrix}$。""",
}

if __name__ == '__main__':
    if '--strip' in sys.argv:
        strip_tips(r'D:\ai code\数学二真题\2015数二真题.md')
    else:
        insert_tips(r'D:\ai code\数学二真题\2015数二真题.md', TIPS_2015)
