# -*- coding: utf-8 -*-
import sympy as sp

# 验证直角坐标下对 (x - y)^2 / (x^2 + y^2) 在 D 上的积分
x, y = sp.symbols('x y', real=True)
integrand = (x - y)**2 / (x**2 + y**2)

# D: y 从 0 到 2, x 从 y - 2 到 sqrt(4 - y^2)
# 分成 D2 (三角形) 和 D1 (四分之一圆)
# D2: y 从 0 到 2, x 从 y - 2 到 0
I2 = sp.integrate(sp.integrate(integrand, (x, y - 2, 0)), (y, 0, 2))
print("I2 (D2 三角形) =", sp.simplify(I2))

# D1: y 从 0 到 2, x 从 0 到 sqrt(4 - y^2)
# 极坐标下 D1: theta 0 to pi/2, r 0 to 2
# (cos - sin)^2 * r dr dtheta = (1 - sin(2theta)) * 2 = 2 * (pi/2 - 1) = pi - 2
I1 = sp.pi - 2
print("I1 (D1 四分之一圆) =", I1)
print("Total I = I1 + I2 =", sp.simplify(I1 + I2))
