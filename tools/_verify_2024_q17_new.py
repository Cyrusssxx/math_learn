# -*- coding: utf-8 -*-
"""验证 2024 题17 新解法的数学正确性（SymPy 数值/符号双重验证）"""
import sympy as sp

x, y = sp.symbols('x y', positive=True)

# 区域 D：第一象限, 1/3 <= xy <= 3, x/3 <= y <= 3x
integrand = 1 + x - y

# 直接直角坐标分块积分（与新解析完全一致）
I1 = sp.integrate(sp.integrate(integrand, (y, 1/(3*x), 3*x)), (x, sp.Rational(1, 3), 1))
I2 = sp.integrate(sp.integrate(integrand, (y, x/3, 3/x)), (x, 1, 3))
I = sp.simplify(I1 + I2)
print("I =", I, "（期望 8ln3/3）")
assert sp.simplify(I - sp.Rational(8, 3)*sp.log(3)) == 0, "I 不等于 8ln3/3！"
print("✅ I = 8ln3/3 验证通过")

# 验证对称性论断：x-y 在 D 上积分为 0
J1 = sp.integrate(sp.integrate(x - y, (y, 1/(3*x), 3*x)), (x, sp.Rational(1, 3), 1))
J2 = sp.integrate(sp.integrate(x - y, (y, x/3, 3/x)), (x, 1, 3))
J = sp.simplify(J1 + J2)
print("∫∫(x-y)dσ =", J)
assert J == 0, "x-y 积分不为 0！"
print("✅ 对称性消项 ∫∫(x-y)dσ = 0 验证通过")

# 验证面积
S1 = sp.integrate(sp.integrate(1, (y, 1/(3*x), 3*x)), (x, sp.Rational(1, 3), 1))
S2 = sp.integrate(sp.integrate(1, (y, x/3, 3/x)), (x, 1, 3))
S = sp.simplify(S1 + S2)
print("S_D =", S, "（期望 8ln3/3）")
assert sp.simplify(S - sp.Rational(8, 3)*sp.log(3)) == 0
print("✅ S_D = 8ln3/3 验证通过")
