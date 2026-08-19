#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「常见函数图形」SVG，供 高数0 中学公式速查 / 函数图形速查 速查。
仅用标准库，输出矢量图到 ../math/导图/img/（源目录），由 build_notes.py 复制进 pwa/data/img/。

坐标系：x 向右、y 向上； axes 过原点（若 0 不在定义域/值域内则贴边）。
特性：
- curve()：均匀采样，超界/非法点自动断笔（可画渐近线、间断点）。
- steps()：阶梯函数（符号/取整）。
- fill_under()：定积分面积填充。
- 支持 discont=[] 强制在某 x 处断笔（跳跃间断点）。
"""
import math
import os

W, H = 440, 300
ML, MR, MT, MB = 46, 18, 22, 34
PX0, PX1 = ML, W - MR
PY0, PY1 = MT, H - MB
PW, PH = PX1 - PX0, PY1 - PY0

GRID = "#ececec"
AXIS = "#444"
TEXT = "#333"
FAINT = "#9aa"
FONT = "12px -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
COL = {"red": "#e53935", "blue": "#1e88e5", "green": "#2e9e4f",
       "purple": "#8e24aa", "orange": "#ef6c00", "gray": "#90a4ae"}


def arrow(x, y, dx, dy):
    ang = math.atan2(dy, dx)
    L = 8
    a1 = (x - L * math.cos(ang - 0.4), y - L * math.sin(ang - 0.4))
    a2 = (x - L * math.cos(ang + 0.4), y - L * math.sin(ang + 0.4))
    return f'<polygon points="{x:.1f},{y:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" fill="{AXIS}"/>'


class G:
    def __init__(self, name, xmin, xmax, ymin, ymax):
        self.name = name
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.ux = PW / (xmax - xmin)
        self.uy = PH / (ymax - ymin)
        self.parts = []

    def sx(self, x): return PX0 + (x - self.xmin) / (self.xmax - self.xmin) * PW

    def _sy(self, y):
        return PY1 - (y - self.ymin) / (self.ymax - self.ymin) * PH

    def grid(self):
        for t in range(math.ceil(self.xmin), math.floor(self.xmax) + 1):
            if t == 0:
                continue
            x = self.sx(t)
            self.parts.append(f'<line x1="{x:.1f}" y1="{PY0}" x2="{x:.1f}" y2="{PY1}" stroke="{GRID}" stroke-width="1"/>')
        for t in range(math.ceil(self.ymin), math.floor(self.ymax) + 1):
            if t == 0:
                continue
            y = self._sy(t)
            self.parts.append(f'<line x1="{PX0}" y1="{y:.1f}" x2="{PX1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')

    def axes(self):
        ay = self._sy(0) if self.ymin <= 0 <= self.ymax else (PY1 if self.ymin > 0 else PY0)
        ax = self.sx(0) if self.xmin <= 0 <= self.xmax else (PX0 if self.xmin > 0 else PX1)
        self.parts.append(f'<line x1="{PX0}" y1="{ay:.1f}" x2="{PX1}" y2="{ay:.1f}" stroke="{AXIS}" stroke-width="1.5"/>')
        self.parts.append(f'<line x1="{ax:.1f}" y1="{PY0}" x2="{ax:.1f}" y2="{PY1}" stroke="{AXIS}" stroke-width="1.5"/>')
        self.parts.append(arrow(PX1, ay, 1, 0))
        self.parts.append(arrow(ax, PY0, 0, -1))
        self.parts.append(f'<text x="{PX1 - 4}" y="{ay - 6:.1f}" fill="{AXIS}" font-size="12" text-anchor="end">x</text>')
        self.parts.append(f'<text x="{ax + 6:.1f}" y="{PY0 + 12}" fill="{AXIS}" font-size="12" text-anchor="start">y</text>')
        if self.xmin <= 0 <= self.xmax and self.ymin <= 0 <= self.ymax:
            self.parts.append(f'<text x="{ax + 4:.1f}" y="{ay + 13:.1f}" fill="{FAINT}" font-size="11" text-anchor="start">O</text>')

    def curve(self, f, color, label=None, lpos=None, discont=None, n=800):
        discont = discont or []
        segs, cur = [], []
        dx = (self.xmax - self.xmin) / n
        for k in range(n + 1):
            x = self.xmin + k * dx
            if any(abs(x - d) < dx * 0.5 for d in discont):
                if len(cur) >= 2:
                    segs.append(cur)
                cur = []
                continue
            try:
                y = f(x)
            except Exception:
                y = None
            if y is None or not math.isfinite(y) or y < self.ymin - 0.5 or y > self.ymax + 0.5:
                if len(cur) >= 2:
                    segs.append(cur)
                cur = []
                continue
            cur.append((x, y))
        if len(cur) >= 2:
            segs.append(cur)
        for seg in segs:
            pts = " ".join(f"{self.sx(x):.1f},{self._sy(y):.1f}" for x, y in seg)
            self.parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
        if label:
            lx, ly = lpos if lpos else (self.xmin + 0.55 * (self.xmax - self.xmin), self.ymax - 0.6)
            self.parts.append(f'<text x="{self.sx(lx):.1f}" y="{self._sy(ly):.1f}" fill="{color}" font-size="13" font-weight="600">{label}</text>')
        return self

    def steps(self, segs, color, label=None, lpos=None):
        for (x1, y1), (x2, y2) in segs:
            self.parts.append(f'<polyline points="{self.sx(x1):.1f},{self._sy(y1):.1f} {self.sx(x2):.1f},{self._sy(y2):.1f}" '
                              f'fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>')
        if label:
            lx, ly = lpos
            self.parts.append(f'<text x="{self.sx(lx):.1f}" y="{self._sy(ly):.1f}" fill="{color}" font-size="13" font-weight="600">{label}</text>')
        return self

    def dot(self, x, y, color, open_=False, r=3.4):
        if open_:
            self.parts.append(f'<circle cx="{self.sx(x):.1f}" cy="{self._sy(y):.1f}" r="{r}" fill="#fff" stroke="{color}" stroke-width="2"/>')
        else:
            self.parts.append(f'<circle cx="{self.sx(x):.1f}" cy="{self._sy(y):.1f}" r="{r}" fill="{color}"/>')
        return self

    def line(self, x1, y1, x2, y2, color, dash=False):
        st = f' stroke-dasharray="6 4"' if dash else ''
        self.parts.append(f'<line x1="{self.sx(x1):.1f}" y1="{self._sy(y1):.1f}" x2="{self.sx(x2):.1f}" y2="{self._sy(y2):.1f}" '
                          f'stroke="{color}" stroke-width="2"{st}/>')
        return self

    def text(self, x, y, s, color=TEXT, size=12, anchor="start", weight="400"):
        self.parts.append(f'<text x="{self.sx(x):.1f}" y="{self._sy(y):.1f}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>')
        return self

    def fill_under(self, f, a, b, color):
        pts = [(a, self.ymin)]
        n = 140
        dx = (b - a) / n
        for k in range(n + 1):
            x = a + k * dx
            pts.append((x, f(x)))
        pts.append((b, self.ymin))
        poly = " ".join(f"{self.sx(x):.1f},{self._sy(y):.1f}" for x, y in pts)
        self.parts.append(f'<polygon points="{poly}" fill="{color}" opacity="0.25"/>')
        return self

    def circle(self, cx, cy, r, fill="none", stroke=AXIS, sw=1.5, opacity=1):
        self.parts.append(f'<circle cx="{self.sx(cx):.1f}" cy="{self._sy(cy):.1f}" r="{r * self.ux:.1f}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>')
        return self

    def poly(self, coords, fill="none", stroke=AXIS, sw=2, opacity=1):
        pts = " ".join(f"{self.sx(x):.1f},{self._sy(y):.1f}" for x, y in coords)
        self.parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}" stroke-linejoin="round"/>')
        return self

    def wedge(self, cx, cy, r, a1, a2, fill, opacity=0.3, stroke=AXIS):
        p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        p2 = (cx + r * math.cos(a2), cy + r * math.sin(a2))
        large = 1 if (a2 - a1) % (2 * math.pi) > math.pi else 0
        self.parts.append(
            f'<path d="M {self.sx(cx):.1f} {self._sy(cy):.1f} L {self.sx(p1[0]):.1f} {self._sy(p1[1]):.1f} '
            f'A {r * self.ux:.1f} {r * self.ux:.1f} 0 {large} 1 {self.sx(p2[0]):.1f} {self._sy(p2[1]):.1f} Z" '
            f'fill="{fill}" opacity="{opacity}" stroke="{stroke}" stroke-width="1"/>')
        return self

    def save(self, path):
        self.grid()
        self.axes()
        s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'style="max-width:100%;height:auto;background:#fff" font-family="{FONT}">']
        s += self.parts
        s.append(f'<text x="{PX0}" y="14" fill="{TEXT}" font-size="13" font-weight="700">{self.name}</text>')
        s.append('</svg>')
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(s))
        print("written:", os.path.basename(path))


OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "math", "导图", "img"))

# ============ A. 基本初等函数（最重要，必背）============
G("常数函数与一次函数", -5, 5, -5, 5).curve(lambda x: 2, COL["red"], "y = 2", (2.4, 2.4)) \
    .curve(lambda x: x + 1, COL["blue"], "y = x + 1", (2.6, 3.6)).save(f"{OUT}/func_01_const_linear.svg")

G("二次函数（抛物线）", -5, 5, -5, 9).curve(lambda x: 0.5 * x * x - 1, COL["red"], "y = ½x² − 1", (1.6, 3.2)) \
    .save(f"{OUT}/func_02_quad.svg")

G("绝对值函数", -5, 5, 0, 5).curve(lambda x: abs(x), COL["red"], "y = |x|", (2.6, 3.0)).save(f"{OUT}/func_03_abs.svg")

G("反比例函数", -5, 5, -6, 6).curve(lambda x: 2 / x, COL["red"], "y = 2/x", (1.4, 2.6)).save(f"{OUT}/func_04_reciprocal.svg")

G("幂函数族（x ≥ 0）", 0, 2.8, 0, 8).curve(lambda x: x * x, COL["red"], "y = x²", (0.9, 1.2)) \
    .curve(lambda x: x, COL["blue"], "y = x", (1.7, 1.9)) \
    .curve(lambda x: math.sqrt(x), COL["green"], "y = √x", (0.4, 2.6)).save(f"{OUT}/func_05_power.svg")

G("指数函数", -4, 4, -0.5, 9).curve(lambda x: 2 ** x, COL["red"], "y = 2ˣ", (1.8, 3.6)) \
    .curve(lambda x: 0.5 ** x, COL["blue"], "y = (½)ˣ", (-1.6, 3.0)).save(f"{OUT}/func_06_exp.svg")

G("对数函数", 0.05, 5, -4, 4).curve(lambda x: math.log2(x), COL["red"], "y = log₂x", (2.2, 1.6)) \
    .curve(lambda x: math.log2(x) / math.log2(0.5), COL["blue"], "y = log_{½}x", (2.2, -1.2)).save(f"{OUT}/func_07_log.svg")

G("正弦函数 y = sin x", -2 * math.pi, 2 * math.pi, -1.6, 1.6).curve(lambda x: math.sin(x), COL["red"], "y = sin x", (1.0, 1.2)) \
    .save(f"{OUT}/func_08_sin.svg")

G("余弦函数 y = cos x", -2 * math.pi, 2 * math.pi, -1.6, 1.6).curve(lambda x: math.cos(x), COL["red"], "y = cos x", (-1.2, 1.2)) \
    .save(f"{OUT}/func_09_cos.svg")

G("正切函数 y = tan x", -5.4, 5.4, -4, 4).curve(lambda x: math.tan(x), COL["red"], "y = tan x", (0.6, 1.8)) \
    .save(f"{OUT}/func_10_tan.svg")

G("反正弦函数 y = arcsin x", -1, 1, -1.8, 1.8).curve(lambda x: math.asin(x), COL["red"], "y = arcsin x", (-0.7, -1.2)) \
    .save(f"{OUT}/func_11_arcsin.svg")

G("反余弦函数 y = arccos x", -1, 1, -0.3, 3.4).curve(lambda x: math.acos(x), COL["red"], "y = arccos x", (0.1, 2.4)) \
    .save(f"{OUT}/func_12_arccos.svg")

G("反正切函数 y = arctan x", -6, 6, -2, 2).curve(lambda x: math.atan(x), COL["red"], "y = arctan x", (2.4, 1.1)) \
    .save(f"{OUT}/func_13_arctan.svg")

# ============ B. 特殊与分段函数 ============
g = G("符号函数 y = sgn x", -5, 5, -2, 2)
g.steps([((-5, -1), (0, -1)), ((0, 1), (5, 1))], COL["red"], "y = sgn x", (-4, 1.5))
g.dot(0, 0, COL["red"])
g.save(f"{OUT}/func_14_sgn.svg")

g = G("取整函数 y = [x]（向下取整）", -5, 5, -5, 5)
segs = [((n, n), (n + 1, n)) for n in range(-5, 5)]
g.steps(segs, COL["red"])
for n in range(-5, 5):
    g.dot(n, n, COL["red"])
g.save(f"{OUT}/func_15_floor.svg")

G("对勾函数 y = x + a/x", -5, 5, -5, 5).curve(lambda x: x + 1 / x, COL["red"], "y = x + 1/x", (1.6, 2.6)) \
    .save(f"{OUT}/func_16_duigou.svg")

g = G("双曲函数 sinh x / cosh x", -3, 3, -4, 4)
g.curve(lambda x: (math.e ** x - math.e ** (-x)) / 2, COL["red"], "y = sinh x", (1.4, 2.4))
g.curve(lambda x: (math.e ** x + math.e ** (-x)) / 2, COL["blue"], "y = cosh x", (1.4, 3.4))
g.save(f"{OUT}/func_17_hyperbolic.svg")

G("分段函数（带折角）", -3, 3, -3, 4).curve(lambda x: -x if x < 0 else x * x, COL["red"], "y = −x (x<0), x² (x≥0)", (0.4, 2.4)) \
    .save(f"{OUT}/func_18_piecewise.svg")

# ============ C. 极限与连续 ============
G("重要极限 (sin x)/x → 1", -6, 6, -0.4, 1.3).curve(lambda x: math.sin(x) / x if x != 0 else 1, COL["red"], "y = (sin x)/x", (2.2, 0.7)) \
    .line(-6, 1, 6, 1, COL["gray"], dash=True).save(f"{OUT}/func_19_lim_sinx_x.svg")

G("重要极限 (1 + 1/x)^x → e", 0.4, 12, 1, 3.2).curve(lambda x: (1 + 1 / x) ** x, COL["red"], "y = (1+1/x)ˣ", (5.5, 2.5)) \
    .line(0.4, math.e, 12, math.e, COL["gray"], dash=True).save(f"{OUT}/func_20_lim_exp_e.svg")

g = G("可去间断点", -3, 4, -1, 4)
g.curve(lambda x: (x * x - 1) / (x - 1) if x != 1 else None, COL["red"], "y = (x²−1)/(x−1)", (2.2, 3.0))
g.dot(1, 2, COL["red"], open_=True)
g.save(f"{OUT}/func_21_disc_removable.svg")

g = G("跳跃间断点", -3, 3, -3, 3)
g.curve(lambda x: 0.5 * x + 1 if x < 0 else 0.5 * x - 1, COL["red"], "y = {0.5x+1, x<0; 0.5x−1, x≥0}", (0.4, 2.2), discont=[0])
g.dot(0, 1, COL["red"], open_=True)
g.dot(0, -1, COL["red"])
g.save(f"{OUT}/func_22_disc_jump.svg")

# ============ D. 导数与微分 ============
g = G("导数几何意义（切线）", -4, 4, -3, 4)
g.curve(lambda x: 0.3 * x * x - 1, COL["red"], "y = f(x)", (1.8, 2.6))
x0 = 1
y0 = 0.3 * x0 * x0 - 1
slope = 0.6 * x0
g.line(x0 - 2.2, y0 + slope * (-2.2), x0 + 2.2, y0 + slope * 2.2, COL["blue"], dash=True)
g.dot(x0, y0, COL["red"])
g.text(x0 + 0.15, y0 - 0.3, "切点", COL["red"], 11)
g.save(f"{OUT}/func_23_deriv_tangent.svg")

g = G("单调性与极值", -3, 3, -3, 3)
g.curve(lambda x: x ** 3 - 3 * x, COL["red"], "y = x³ − 3x", (1.7, 1.8))
g.dot(-1, 2, COL["red"])
g.dot(1, -2, COL["red"])
g.text(-1.5, 2.3, "极大值", COL["red"], 11)
g.text(1.1, -2.4, "极小值", COL["red"], 11)
g.text(-2.6, -1.6, "↑增", COL["green"], 12)
g.text(-0.3, -1.0, "↓减", COL["blue"], 12)
g.text(1.8, 1.4, "↑增", COL["green"], 12)
g.save(f"{OUT}/func_24_monotonic_extremum.svg")

g = G("凹凸性与拐点", -2, 2, -5, 5)
g.curve(lambda x: x ** 3, COL["red"], "y = x³", (1.2, 2.4))
g.dot(0, 0, COL["red"])
g.text(0.15, 0.4, "拐点", COL["red"], 11)
g.text(-1.7, -1.2, "凸（f″<0）", COL["blue"], 11)
g.text(0.5, 1.6, "凹（f″>0）", COL["green"], 11)
g.save(f"{OUT}/func_25_concavity_inflection.svg")

# ============ E. 中值定理几何意义 ============
g = G("罗尔定理（Rolle）", -3, 3, -1, 4)
g.curve(lambda x: 2 - 0.5 * x * x, COL["red"], "y = f(x)", (1.4, 2.4))
g.dot(-2, 0, COL["red"]); g.dot(2, 0, COL["red"]); g.dot(0, 2, COL["red"])
g.line(-2.4, 2, 2.4, 2, COL["blue"], dash=True)
g.text(-2.4, -0.5, "a", COL["red"], 11); g.text(2.0, -0.5, "b", COL["red"], 11)
g.text(0.15, 2.3, "ξ", COL["blue"], 11)
g.save(f"{OUT}/func_26_rolle.svg")

g = G("拉格朗日中值定理", -3, 3, -1, 4)
g.curve(lambda x: 0.5 * x * x, COL["red"], "y = f(x)", (1.6, 2.4))
g.line(-2, 2, 2, 2, COL["gray"], dash=True)          # 弦（水平）
g.line(-0.9, -0.4, 0.9, 0.4, COL["blue"], dash=True)  # 切线（水平，∥弦）
g.dot(-2, 2, COL["red"]); g.dot(2, 2, COL["red"])
g.text(-2.35, 1.6, "a", COL["red"], 11); g.text(2.05, 1.6, "b", COL["red"], 11)
g.save(f"{OUT}/func_27_lagrange.svg")

# ============ F. 积分 ============
g = G("定积分几何意义（面积）", 0, 2, 0, 1.7)
g.fill_under(lambda x: 1.2 * math.sin(math.pi * x / 2), 0, 2, COL["red"])
g.curve(lambda x: 1.2 * math.sin(math.pi * x / 2), COL["red"], "y = f(x)", (0.7, 1.3))
g.save(f"{OUT}/func_28_integral_area.svg")

g = G("变上限积分 Φ(x) = ∫₀ˣ f(t)dt", 0, 2 * math.pi, -1.5, 2.6)
g.curve(lambda x: math.sin(x), COL["red"], "y = f(x)", (4.4, 1.3))
g.curve(lambda x: 1 - math.cos(x), COL["blue"], "y = Φ(x)", (4.4, -0.6))
g.save(f"{OUT}/func_29_variable_integral.svg")

# ============ G. 微分方程 ============
g = G("微分方程 y' = ky 的解", -2, 2, 0, 5)
g.curve(lambda x: math.e ** x, COL["red"], "k>0 增长", (0.5, 3.6))
g.curve(lambda x: math.e ** (-x), COL["blue"], "k<0 衰减", (1.0, 2.0))
g.save(f"{OUT}/func_30_ode_decay.svg")

# ============ H. 多元积分与线代（拓展）============
g = G("极坐标常见区域（拓展）", -1.3, 1.3, -1.3, 1.3)
g.circle(0, 0, 1, fill="#e3f2fd", stroke=COL["blue"], sw=2)        # 圆盘
g.wedge(0, 0, 1, 0, math.pi / 2, "#fff3e0", stroke=COL["orange"])  # 扇形
g.circle(0, 0, 0.5, stroke=COL["gray"], sw=1.5)                   # 圆环内圈
g.text(0.55, 0.55, "扇形", COL["orange"], 11)
g.text(-1.05, -0.15, "圆环", COL["gray"], 11)
g.save(f"{OUT}/func_31_polar.svg")

g = G("线性变换几何意义（拓展）", -1.6, 1.6, -1.6, 1.6)
# 原单位正方形（灰）
g.poly([(0, 0), (1, 0), (1, 1), (0, 1)], fill="#eceff1", stroke=COL["gray"], sw=2)
# A = [[1.2, 0.3], [-0.2, 1.1]] 的像
A = [[1.2, 0.3], [-0.2, 1.1]]
img = lambda v: (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])
g.poly([img((0, 0)), img((1, 0)), img((1, 1)), img((0, 1))], fill="#e8f5e9", stroke=COL["green"], sw=2)
g.text(0.15, 1.25, "原单位正方形", COL["gray"], 11)
g.text(0.5, 0.7, "变换后", COL["green"], 11)
g.save(f"{OUT}/func_32_linalg_transform.svg")

print("全部生成完成 →", OUT)
