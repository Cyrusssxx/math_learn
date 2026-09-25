# -*- coding: utf-8 -*-
import sympy as sp

# 积分区域 D: y - 2 <= x <= sqrt(4 - y^2), 0 <= y <= 2
# 被积函数: (x - y)^2 / (x^2 + y^2) = 1 - 2xy/(x^2 + y^2)
# 分成两部分：
# D 由两部分组成（第一象限四分之一圆盘 D1 + 第二象限三角形 D2）：
# D1: 0 <= x <= sqrt(4 - y^2), 0 <= y <= 2, 即 x^2 + y^2 <= 4, x >= 0, y >= 0
# D2: y - 2 <= x <= 0, 0 <= y <= 2，即三角形，顶点为 (0,0), (-2,0), (0,2)

x, y, r, theta = sp.symbols('x y r theta', real=True)

# 1. 积分 1 在 D 上的积分 = D 的面积
# D1 是半径为 2 的四分之一圆，面积 = pi * 2^2 / 4 = pi
# D2 是底为 2 高为 2 的三角形，面积 = 1/2 * 2 * 2 = 2
area_D = sp.pi + 2
print("Area of D =", area_D)

# 2. 积分 2xy / (x^2 + y^2) 在 D 上的积分
# 在 D1 上，由于对称性，x 和 y 对称，2xy/(x^2+y^2) 在 D1 上的积分：
# 极坐标下：r 从 0 到 2，theta 从 0 到 pi/2
# (2 * r^2 * sin(theta) * cos(theta) / r^2) * r dr dtheta = sin(2*theta) * r dr dtheta
I_D1 = sp.integrate(r, (r, 0, 2)) * sp.integrate(sp.sin(2*theta), (theta, 0, sp.pi/2))
print("Integral on D1 =", I_D1) # 2 * 1 = 2

# 在 D2 上：极坐标下 theta 从 pi/2 到 3*pi/4
# 直线 x = y - 2 => r*cos(theta) = r*sin(theta) - 2 => r*(sin(theta) - cos(theta)) = 2 => r = 2 / (sin(theta) - cos(theta))
# 被积函数: sin(2*theta) * r dr dtheta
r_upper = 2 / (sp.sin(theta) - sp.cos(theta))
I_D2 = sp.integrate(sp.sin(2*theta) * sp.integrate(r, (r, 0, r_upper)), (theta, sp.pi/2, 3*sp.pi/4))
print("Integral on D2 =", sp.simplify(I_D2))

total_I = area_D - (I_D1 + I_D2)
print("Total I = Area - (I_D1 + I_D2) =", sp.simplify(total_I))
