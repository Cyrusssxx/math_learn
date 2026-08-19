#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「常见函数图形」SVG，供 高数0 中学公式速查 / 初等代数 速查。
仅用标准库，输出矢量图到 ../数学导图/img/（源目录），由 build_notes.py 复制进 pwa/data/img/。

坐标系：x 向右、y 向上； axes 过原点（若 0 不在定义域/值域内则贴边）。
曲线：对每个函数均匀采样，超出视图范围的片段自动断笔（可画渐近线效果）。
"""
import math
import os

W, H = 440, 300
ML, MR, MT, MB = 46, 18, 20, 34
PX0, PX1 = ML, W - MR
PY0, PY1 = MT, H - MB
PW, PH = PX1 - PX0, PY1 - PY0

GRID = "#ececec"
AXIS = "#444"
TEXT = "#333"
FAINT = "#9aa"
FONT = "12px -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"


def sx(x, xmin, xmax):
    return PX0 + (x - xmin) / (xmax - xmin) * PW


def sy(y, ymin, ymax):
    return PY1 - (y - ymin) / (ymax - ymin) * PH


def sample_path(f, xmin, xmax, ymin, ymax, n=800):
    """返回若干段折线（每段是 [(x,y),...]），超出 [ymin,ymax] 或非法点自动断笔。"""
    segs, cur = [], []
    dx = (xmax - xmin) / n
    for k in range(n + 1):
        x = xmin + k * dx
        try:
            y = f(x)
        except Exception:
            y = None
        if y is None or not math.isfinite(y) or y < ymin - 0.5 or y > ymax + 0.5:
            if len(cur) >= 2:
                segs.append(cur)
            cur = []
            continue
        cur.append((x, y))
    if len(cur) >= 2:
        segs.append(cur)
    return segs


def poly(seg, xmin, xmax, ymin, ymax):
    pts = " ".join(f"{sx(x,xmin,xmax):.1f},{sy(y,ymin,ymax):.1f}" for x, y in seg)
    return pts


def arrow(x, y, dx, dy):
    """在 (x,y) 处画一个朝 (dx,dy) 方向的箭头多边形。"""
    import math as m
    ang = m.atan2(dy, dx)
    L = 8
    a1 = (x - L * m.cos(ang - 0.4), y - L * m.sin(ang - 0.4))
    a2 = (x - L * m.cos(ang + 0.4), y - L * m.sin(ang + 0.4))
    return f'<polygon points="{x:.1f},{y:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" fill="{AXIS}"/>'


def make_graph(path, name, curves, xmin, xmax, ymin, ymax):
    # 坐标轴位置
    ax_y = sy(0, ymin, ymax) if ymin <= 0 <= ymax else (PY1 if ymin > 0 else PY0)
    ay_x = sx(0, xmin, xmax) if xmin <= 0 <= xmax else (PX0 if xmin > 0 else PX1)

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" style="max-width:100%;height:auto;background:#fff" '
             f'font-family="{FONT}">')

    # 网格
    for t in range(math.ceil(xmin), math.floor(xmax) + 1):
        if t == 0:
            continue
        xx = sx(t, xmin, xmax)
        s.append(f'<line x1="{xx:.1f}" y1="{PY0}" x2="{xx:.1f}" y2="{PY1}" stroke="{GRID}" stroke-width="1"/>')
    for t in range(math.ceil(ymin), math.floor(ymax) + 1):
        if t == 0:
            continue
        yy = sy(t, ymin, ymax)
        s.append(f'<line x1="{PX0}" y1="{yy:.1f}" x2="{PX1}" y2="{yy:.1f}" stroke="{GRID}" stroke-width="1"/>')

    # 坐标轴
    s.append(f'<line x1="{PX0}" y1="{ax_y:.1f}" x2="{PX1}" y2="{ax_y:.1f}" stroke="{AXIS}" stroke-width="1.5"/>')
    s.append(f'<line x1="{ay_x:.1f}" y1="{PY0}" x2="{ay_x:.1f}" y2="{PY1}" stroke="{AXIS}" stroke-width="1.5"/>')
    s.append(arrow(PX1, ax_y, 1, 0))
    s.append(arrow(ay_x, PY0, 0, -1))

    # 轴名
    s.append(f'<text x="{PX1-4}" y="{ax_y-6:.1f}" fill="{AXIS}" font-size="12" text-anchor="end">x</text>')
    s.append(f'<text x="{ay_x+6:.1f}" y="{PY0+12}" fill="{AXIS}" font-size="12" text-anchor="start">y</text>')
    if xmin <= 0 <= xmax and ymin <= 0 <= ymax:
        s.append(f'<text x="{ay_x+4:.1f}" y="{ax_y+13:.1f}" fill="{FAINT}" font-size="11" text-anchor="start">O</text>')

    # 曲线
    for f, color, label, lx, ly in curves:
        for seg in sample_path(f, xmin, xmax, ymin, ymax):
            s.append(f'<polyline points="{poly(seg, xmin, xmax, ymin, ymax)}" fill="none" '
                     f'stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
        # 标签
        lxp = sx(lx, xmin, xmax)
        lyp = sy(ly, ymin, ymax)
        s.append(f'<text x="{lxp:.1f}" y="{lyp:.1f}" fill="{color}" font-size="13" font-weight="600">{label}</text>')

    # 标题
    s.append(f'<text x="{PX0}" y="14" fill="{TEXT}" font-size="13" font-weight="700">{name}</text>')

    s.append('</svg>')
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(s))
    print("written:", os.path.basename(path))


OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "math", "导图", "img"))
os.makedirs(OUT, exist_ok=True)

C = {"red": "#e53935", "blue": "#1e88e5", "green": "#2e9e4f", "purple": "#8e24aa", "orange": "#ef6c00"}

# 1) 常数函数 & 一次函数
make_graph(os.path.join(OUT, "func_0_const_linear.svg"),
           "常数函数与一次函数",
           [(lambda x: 2, C["red"], "y = 2", 2.4, 2.4),
            (lambda x: x + 1, C["blue"], "y = x + 1", 2.6, 3.6)],
           -5, 5, -5, 5)

# 2) 二次函数（抛物线）
make_graph(os.path.join(OUT, "func_1_quad.svg"),
           "二次函数（抛物线）",
           [(lambda x: 0.5 * x * x - 1, C["red"], "y = ½x² − 1", 1.6, 3.2)],
           -5, 5, -5, 9)

# 3) 绝对值函数
make_graph(os.path.join(OUT, "func_2_abs.svg"),
           "绝对值函数",
           [(lambda x: abs(x), C["red"], "y = |x|", 2.6, 3.0)],
           -5, 5, 0, 5)

# 4) 反比例函数
make_graph(os.path.join(OUT, "func_3_reciprocal.svg"),
           "反比例函数",
           [(lambda x: 2 / x, C["red"], "y = 2/x", 1.4, 2.6)],
           -5, 5, -6, 6)

# 5) 幂函数族
make_graph(os.path.join(OUT, "func_4_power.svg"),
           "幂函数族（x ≥ 0）",
           [(lambda x: x * x, C["red"], "y = x²", 0.9, 1.2),
            (lambda x: x, C["blue"], "y = x", 1.7, 1.9),
            (lambda x: math.sqrt(x), C["green"], "y = √x", 0.4, 2.6)],
           0, 2.8, 0, 8)

# 6) 指数函数
make_graph(os.path.join(OUT, "func_5_exp.svg"),
           "指数函数",
           [(lambda x: 2 ** x, C["red"], "y = 2ˣ", 1.8, 3.6),
            (lambda x: 0.5 ** x, C["blue"], "y = (½)ˣ", -1.6, 3.0)],
           -4, 4, -0.5, 9)

# 7) 对数函数
make_graph(os.path.join(OUT, "func_6_log.svg"),
           "对数函数",
           [(lambda x: math.log2(x), C["red"], "y = log₂x", 2.2, 1.6),
            (lambda x: math.log2(x) / math.log2(0.5), C["blue"], "y = log_{½}x", 2.2, -1.2)],
           0.05, 5, -4, 4)

print("全部生成完成 →", OUT)
