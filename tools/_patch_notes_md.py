# -*- coding: utf-8 -*-
"""多元微分笔记（notes.json[7]）补全「二阶偏导」公式：f''xx/f''xy/f''yy + 复合函数二阶展开 + 隐函数二阶。"""
import json, io

P = 'D:/ai code/math-note/pwa/data/notes.json'
d = json.load(io.open(P, encoding='utf-8'))
md = d[7]['md']

OLD = """- **高阶偏导数**：$\\dfrac{\\partial^2 z}{\\partial x^2}=f''_{xx}$、$\\dfrac{\\partial^2 z}{\\partial x\\partial y}=f''_{xy}$ 等
  - 二阶混合偏导数 $f''_{xy},f''_{yx}$ **连续必相等**"""

NEW = """- **高阶偏导数**（$z=f(x,y)$）
  - $\\dfrac{\\partial^2 z}{\\partial x^2}=f''_{xx}(x,y)$，$\\dfrac{\\partial^2 z}{\\partial x\\partial y}=f''_{xy}(x,y)$，$\\dfrac{\\partial^2 z}{\\partial y^2}=f''_{yy}(x,y)$
  - 记号含义：$f''_{xx}=\\dfrac{\\partial}{\\partial x}\\left(\\dfrac{\\partial z}{\\partial x}\\right)$；$f''_{xy}=\\dfrac{\\partial}{\\partial y}\\left(\\dfrac{\\partial z}{\\partial x}\\right)$（先对 $x$ 后对 $y$）
  - ⚠️ 二阶混合偏导 $f''_{xy}=f''_{yx}$ **连续必相等**（不连续可不等：经典反例 $f_{xy}(0,0)=-1\\neq f_{yx}(0,0)=1$）
- **复合函数二阶偏导**（$z=f(u,v)$，$u=u(x,y),\\ v=v(x,y)$）
  - $\\dfrac{\\partial^2 z}{\\partial x^2}=f''_{uu}(u'_x)^2+2f''_{uv}\\,u'_xv'_x+f''_{vv}(v'_x)^2+f'_u\\,u''_{xx}+f'_v\\,v''_{xx}$（$\\dfrac{\\partial^2 z}{\\partial x\\partial y}$、$\\dfrac{\\partial^2 z}{\\partial y^2}$ 同理，$u'_x$ 换成对应偏导）
  - 记忆：二阶按 $f_{11},f_{12},f_{22}$ 三类归并，$f_{12}=f_{21}$ 对称；一阶项 $f'_u\\,u''_{xx}+f'_v\\,v''_{xx}$ 易漏，勿忘
- **隐函数二阶偏导**：一阶式 $z_x=-\\dfrac{F_x}{F_z}$ 再对 $x$ 求一次导，移项解出 $z_{xx}$，逐层代值（$F_z$ 含 $z$ 时先定 $z_0$）"""

assert OLD in md, '未找到原文，中止（防误改）'
d[7]['md'] = md.replace(OLD, NEW, 1)

with io.open(P, 'w', encoding='utf-8', newline='') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# 校验：写回后可再解析 + 确认新内容
d2 = json.load(io.open(P, encoding='utf-8'))
ok1 = "f''_{xx}(x,y)" in d2[7]['md']
ok2 = '复合函数二阶偏导' in d2[7]['md']
ok3 = '隐函数二阶偏导' in d2[7]['md']
print('写入成功 | 含 fxx(x,y) 记号:', ok1, '| 复合二阶:', ok2, '| 隐函数二阶:', ok3)
