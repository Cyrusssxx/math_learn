# -*- coding: utf-8 -*-
import json, io, os

with io.open('pwa/data/notes.json', 'r', encoding='utf-8') as f:
    notes = json.load(f)

# 1. 替换 Note 2 和 Note 21 中的曲率参数方程符号：
n2 = notes[2]
old_md2 = n2['md']
old_curv_n2 = """- **(ii) 参数方程**：设曲线由参数方程 $\\begin{cases} x=\\varphi(t), \\\\ y=\\psi(t) \\end{cases}$ 给出，且具有二阶导数，则曲线在点 $(\\varphi(t),\\psi(t))$ 处的曲率为
  $$K = \\dfrac{\\left|\\varphi'(t)\\psi''(t) - \\varphi''(t)\\psi'(t)\\right|}{\\left\\{[\\varphi'(t)]^2 + [\\psi'(t)]^2\\right\\}^{\\frac{3}{2}}}.$$
  - 💡 **推导速记**：根据参数方程一阶导 $y'_x=\\frac{\\psi'}{\\varphi'}$，二阶导 $y''_{xx}=\\frac{\\varphi'\\psi''-\\varphi''\\psi'}{(\\varphi')^3}$，代入直角坐标公式整理即得（分母提取后为 $[(\\varphi')^2+(\\psi')^2]^{3/2}$）。"""

new_curv_n2 = """- **(ii) 参数方程**：设曲线由参数方程 $\\begin{cases} x=x(t), \\\\ y=y(t) \\end{cases}$（或记为 $x=f(t), y=g(t)$）给出，且具有二阶导数，则曲线在对应点处的曲率为
  $$K = \\dfrac{\\left|x'(t)y''(t) - x''(t)y'(t)\\right|}{\\left\\{[x'(t)]^2 + [y'(t)]^2\\right\\}^{\\frac{3}{2}}}.$$
  - 💡 **推导速记**：由参数方程一阶导 $y'_x=\\frac{y'(t)}{x'(t)}$，二阶导 $y''_{xx}=\\frac{x'(t)y''(t)-x''(t)y'(t)}{[x'(t)]^3}$，代入直角坐标公式通分整理即得（分子为“$x'y''-x''y'$ 的绝对值”，分母为“平方和的 $\\frac32$ 次方”）。"""

assert old_curv_n2 in old_md2, "old_curv_n2 not found"
n2['md'] = old_md2.replace(old_curv_n2, new_curv_n2)

# Note 21: 考前第5记·导数的几何应用
n21 = notes[21]
old_md21 = n21['md']
old_curv_n21 = """  - **参数方程** $\\begin{cases}x=\\varphi(t)\\\\y=\\psi(t)\\end{cases}$：$$K=\\dfrac{\\left|\\varphi'(t)\\psi''(t)-\\varphi''(t)\\psi'(t)\\right|}{\\left\\{[\\varphi'(t)]^2+[\\psi'(t)]^2\\right\\}^{\\frac32}}$$"""

new_curv_n21 = """  - **参数方程** $\\begin{cases}x=x(t)\\\\y=y(t)\\end{cases}$（或 $x=f(t),y=g(t)$）：$$K=\\dfrac{\\left|x'(t)y''(t)-x''(t)y'(t)\\right|}{\\left\\{[x'(t)]^2+[y'(t)]^2\\right\\}^{\\frac32}}$$"""

assert old_curv_n21 in old_md21, "old_curv_n21 not found"
n21['md'] = old_md21.replace(old_curv_n21, new_curv_n21)


# 2. 补全 Note 6: 微分方程（补充伯努利方程）
n6 = notes[6]
old_md6 = n6['md']
old_ode6 = """- ⑤ 一阶线性：$y'+P(x)y=Q(x)$（线性 = $y,y'$ 均一次；$Q(x)=0$ 则为线性齐次）
  - 解法：两端同乘积分因子 $e^{\\int P(x)dx}$，左边凑成 $\\left[e^{\\int P(x)dx}y\\right]'=e^{\\int P(x)dx}Q(x)$
  - 通解公式：$y=e^{-\\int P(x)dx}\\left[\\int e^{\\int P(x)dx}Q(x)dx+C\\right]$
  - 特别地 $Q(x)=0$：$y=Ce^{-\\int P(x)dx}$
  - 例：$y'+\\dfrac{y}{x}=\\dfrac{\\sin x}{x}$：因子 $e^{\\int dx/x}=x$ ⇒ $(xy)'=\\sin x$ ⇒ $y=\\dfrac{C-\\cos x}{x}$"""

new_ode6 = """- ⑤ 一阶线性：$y'+P(x)y=Q(x)$（线性 = $y,y'$ 均一次；$Q(x)=0$ 则为线性齐次）
  - 解法：两端同乘积分因子 $e^{\\int P(x)dx}$，左边凑成 $\\left[e^{\\int P(x)dx}y\\right]'=e^{\\int P(x)dx}Q(x)$
  - 通解公式：$y=e^{-\\int P(x)dx}\\left[\\int e^{\\int P(x)dx}Q(x)dx+C\\right]$
  - 特别地 $Q(x)=0$：$y=Ce^{-\\int P(x)dx}$
  - 例：$y'+\\dfrac{y}{x}=\\dfrac{\\sin x}{x}$：因子 $e^{\\int dx/x}=x$ ⇒ $(xy)'=\\sin x$ ⇒ $y=\\dfrac{C-\\cos x}{x}$
- ⑥ 伯努利方程（高频非线性一阶方程·数一、数二核心考点）：
  $$y' + P(x)y = Q(x)y^n\\quad(n\\neq0, 1)$$
  - 判定特征：右端多了非线性的 $y^n$ 乘积项。
  - 标准化解法（除以 $y^n$ 线性化）：
    1. 两端同除以 $y^n$：$y^{-n}y' + P(x)y^{1-n} = Q(x)$
    2. 令变量代换 $z = y^{1-n}$，则 $\\frac{dz}{dx} = (1-n)y^{-n}y'$，方程即化为关于 $z$ 的**一阶线性微分方程**：
       $$\\dfrac{dz}{dx} + (1-n)P(x)z = (1-n)Q(x)$$
    3. 用一阶线性通解公式求出 $z(x)$，最后回代 $z=y^{1-n}$ 即得原方程通解。"""

assert old_ode6 in old_md6, "old_ode6 not found"
n6['md'] = old_md6.replace(old_ode6, new_ode6)


# 3. 补全 Note 7: 多元微分（无条件极值充分条件与鞍点概念）
n7 = notes[7]
old_md7 = n7['md']
old_ext7 = """## 无条件极值 <!-- 源:p1 -->

- **定义**：某邻域内 $f(x,y)<f(x_0,y_0)$（或 $>$）⟹ $(x_0,y_0)$ 为极大（小）值点
- **必要条件**：偏导数存在的极值点必有 $f'_x(x_0,y_0)=0,\\ f'_y(x_0,y_0)=0$
- **充分条件（$AC-B^2$ 判别法）**：驻点处记 $A=f''_{xx},\\ B=f''_{xy},\\ C=f''_{yy}$
  - $AC-B^2>0$：是极值；$A>0$ 极小值，$A<0$ 极大值
  - $AC-B^2<0$：不是极值
  - $AC-B^2=0$：可能是极值
    - 若是 → 用保号性证明
    - 若不是 → 取不同路径否定"""

new_ext7 = """## 无条件极值（二元函数极值必要条件与充分判别法） <!-- 源:p1 -->

- **定义**：设函数 $z=f(x,y)$ 在点 $(x_0,y_0)$ 的某邻域内有定义，若对该去心邻域内任意 $(x,y)$ 均有 $f(x,y)<f(x_0,y_0)$（或 $>$），则称 $(x_0,y_0)$ 为极大（小）值点。
- **必要条件**：若偏导数存在的极值点 $(x_0,y_0)$，则必为驻点：
  $$f'_x(x_0,y_0)=0,\\qquad f'_y(x_0,y_0)=0.$$
- ⭐ **充分条件（$AC-B^2$ 判别法·二元极值核心判定定理）**：
  设 $f(x,y)$ 在驻点 $(x_0,y_0)$ 的某邻域内具有二阶连续偏导数，在驻点处记：
  $$A = f''_{xx}(x_0,y_0),\\qquad B = f''_{xy}(x_0,y_0),\\qquad C = f''_{yy}(x_0,y_0),\\qquad \\Delta = AC - B^2.$$
  - 1. 若 **$AC - B^2 > 0$**：**必取得极值**！
    - 当 $A > 0$（由 $AC>B^2\\ge0$ 必有 $C>0$）时，为**极小值**；
    - 当 $A < 0$（必有 $C<0$）时，为**极大值**。
  - 2. 若 **$AC - B^2 < 0$**：**必不取得极值**（该驻点为**鞍点**）。
  - 3. 若 **$AC - B^2 = 0$**：判定定理**失效**（可能取极大、极小或无极值）：
    - 若要证明是极值 → 利用局部因式分解或正定性证明 $\\Delta f$ 恒正或恒负；
    - 若要否定极值 → 寻找两条不同趋近路径（如沿 $y=x$ 与沿 $y=0$）使增量符号相反。"""

assert old_ext7 in old_md7, "old_ext7 not found"
n7['md'] = old_md7.replace(old_ext7, new_ext7)


# 4. 修复 Note 10: 范德蒙行列式排版缺失反斜杠问题
n10 = notes[10]
old_md10 = n10['md']
old_vand_bad = "- 范德蒙：$D_n=\\begin{vmatrix}1&1&\\cdots&1\\\\x_1&x_2&\\cdots&x_n\\\\x_1^2&x_2^2&\\cdots&x_n^2\\vdots&\\vdots&&\\vdots\\\\x_1^{n-1}&x_2^{n-1}&\\cdots&x_n^{n-1}\\end{vmatrix}=\\prod\\limits_{1\\le i<j\\le n}(x_j-x_i)$"

new_vand_good = """- **范德蒙德行列式（标准型与转置型）**：
  $$D_n=\\begin{vmatrix}1&1&\\cdots&1\\\\x_1&x_2&\\cdots&x_n\\\\x_1^2&x_2^2&\\cdots&x_n^2\\\\\\vdots&\\vdots&&\\vdots\\\\x_1^{n-1}&x_2^{n-1}&\\cdots&x_n^{n-1}\\end{vmatrix}=\\prod_{1\\le j < i \\le n}(x_i-x_j)$$
  转置型同样成立：
  $$\\begin{vmatrix}1&x_1&x_1^2&\\cdots&x_1^{n-1}\\\\1&x_2&x_2^2&\\cdots&x_2^{n-1}\\\\\\vdots&\\vdots&\\vdots&&\\vdots\\\\1&x_n&x_n^2&\\cdots&x_n^{n-1}\\end{vmatrix}=\\prod_{1\\le j < i \\le n}(x_i-x_j)$$
  非零充要条件：$x_1,x_2,\\dots,x_n$ 两两互不相等。"""

assert old_vand_bad in old_md10, "old_vand_bad not found"
n10['md'] = old_md10.replace(old_vand_bad, new_vand_good)


# 写回 notes.json
with io.open('pwa/data/notes.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(notes, f, ensure_ascii=False, indent=2)

print("全部四处核心定义与公式修改修缮成功！")
