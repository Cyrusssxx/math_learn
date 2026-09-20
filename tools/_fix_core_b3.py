# -*- coding: utf-8 -*-
# 修复 core_bank.json 剩余 6 个字段（批次3：整段规范化重写，保留数学内容）
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = 'pwa/data/core_bank.json'

def load():
    with open(SRC, encoding='utf-8') as f:
        return json.load(f)

def find_q(data, no):
    for s in data[0]['sections']:
        for q in s['questions']:
            if str(q['no']) == str(no):
                return q
    return None

FIX = {}

# ---------------- core-383: 拆同行块 ----------------
def fix_383(s):
    old = '$$F(x)=\\begin{cases}\\displaystyle\\int_0^x\\sin t\\,dt=1-\\cos x,&0\\le x<\\pi,\\\\[6pt]\\displaystyle\\int_0^\\pi\\sin t\\,dt+\\int_\\pi^x2\\,dt=2(x-\\pi+1),&\\pi\\le x\\le2\\pi.\\end{cases}$$\n\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,$$'
    new = '$$\nF(x)=\\begin{cases}\\displaystyle\\int_0^x\\sin t\\,dt=1-\\cos x,&0\\le x<\\pi,\\\\[6pt]\\displaystyle\\int_0^\\pi\\sin t\\,dt+\\int_\\pi^x2\\,dt=2(x-\\pi+1),&\\pi\\le x\\le2\\pi.\\end{cases}\n$$\n$$\n\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,\n$$'
    if old in s:
        return s.replace(old, new)
    return s
FIX['core-383.answer'] = fix_383

# ---------------- core-578: 第二处 cases 空对 ----------------
def fix_578(s):
    old = '$$\n\\begin{cases}\\end{cases}\n\\dfrac{dx}{dt}-2te^{-x}=0,\\\\\nx(0)=0\n\\end{cases}\n$$'
    new = '$$\n\\begin{cases}\n\\dfrac{dx}{dt}-2te^{-x}=0,\\\\\nx(0)=0\n\\end{cases}\n$$'
    if old in s:
        return s.replace(old, new)
    # 兜底：去掉 \begin{cases}\end{cases} 空对（宽容匹配）
    import re
    s2 = re.sub(r'\\begin\{cases\}\\end\{cases\}\n', '', s)
    return s2
FIX['core-578.stem'] = fix_578

# ---------------- core-274: 引用块裸公式已修，剩 v=... 区域 ；整段重排 ----------------
def fix_274(s):
    # 段1：则： 后的 v=.. 与 > 引用
    old = '设 $u = \\arctan t$，$dv = (2t^3 + 2t) dt$。\n则：\n$$\n$$v = \\int (2t^3 + 2t) dt = \\frac{1}{2}t^4 + t^2 = \\frac{1}{2}(t^4 + 2t^2)$$\n$$\n\n> **技巧提示：**'
    new = '设 $u = \\arctan t$，$dv = (2t^3 + 2t) dt$。\n则：\n$$\nv = \\int (2t^3 + 2t) dt = \\frac{1}{2}t^4 + t^2 = \\frac{1}{2}(t^4 + 2t^2)\n$$\n\n> **技巧提示：**'
    if old in s:
        s = s.replace(old, new)
    # I = ... 两块（46-50 行）
    old2 = '$$\n$$I = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\int \\frac{1}{2}(t^2+1)^2 \\cdot \\frac{1}{1+t^2} dt$$\n$$\nI = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\frac{1}{2} \\int (t^2+1) dt\n$$'
    new2 = '$$\nI = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\int \\frac{1}{2}(t^2+1)^2 \\cdot \\frac{1}{1+t^2} dt\n$$\n$$\nI = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\frac{1}{2} \\int (t^2+1) dt\n$$'
    if old2 in s:
        s = s.replace(old2, new2)
    return s
FIX['core-274.answer'] = fix_274

# ---------------- core-283: KL 模式：`$$\n=X\n$$` 裸公式行补开块 + 其余裸行 ----
def fix_283(s):
    import re
    # 模式A: "$$\n" 开头行后紧跟 "= ..." 裸行（无 $ 无中文）→ 在裸行前补 "$$\n"
    # 即 "\n$$\n= " -> "\n$$\n$$\n= "? 不对——目标是每个公式独立成块：
    # 原: ...dx\n$$\n= \frac{1}{4}...dx\n$$\n  期望: ...dx\n$$\n$$\n= ...dx\n$$\n ？不行，会产生空块。
    # 正确目标: 闭块 $$ 换行后 新块: $$\n= X\n$$
    # 找 "\n$$\n= (\\)" 且该 $$ 前面一行不是 "$$"（即 $$ 是上一公式块的闭）
    # 直接用手工序列替换（每处格式："...X\n$$\n= Y\n$$\n"）
    pairs = [
        ('\\right)^2 dx\n$$\n= \\frac{1}{4} \\int (1 + 2\\cos 2x + \\cos^2 2x) \\, dx\n$$',
         '\\right)^2 dx\n$$\n$$\n= \\frac{1}{4} \\int (1 + 2\\cos 2x + \\cos^2 2x) \\, dx\n$$'),
        ('\\left( \\frac{3}{2} + 2\\cos 2x + \\frac{1}{2}\\cos 4x \\right) dx\n$$\n= \\frac{1}{4} \\left( \\frac{3}{2}x + \\sin 2x + \\frac{1}{8}\\sin 4x \\right) + C\n$$',
         '\\left( \\frac{3}{2} + 2\\cos 2x + \\frac{1}{2}\\cos 4x \\right) dx\n$$\n$$\n= \\frac{1}{4} \\left( \\frac{3}{2}x + \\sin 2x + \\frac{1}{8}\\sin 4x \\right) + C\n$$'),
        ('\\frac{1}{8}\\sin 4x \\right) + C\n$$\n= \\frac{3}{8}x + \\frac{1}{4}\\sin 2x + \\frac{1}{32}\\sin 4x + C\n$$',
         '\\frac{1}{8}\\sin 4x \\right) + C\n$$\n$$\n= \\frac{3}{8}x + \\frac{1}{4}\\sin 2x + \\frac{1}{32}\\sin 4x + C\n$$'),
        ('\\csc^2 x \\cdot \\csc^2 x \\, dx\n$$\n= \\int (1 + \\cot^2 x) (-d(\\cot x))\n$$\n= -\\int (1 + \\cot^2 x) \\, d(\\cot x)\n$$',
         '\\csc^2 x \\cdot \\csc^2 x \\, dx\n$$\n$$\n= \\int (1 + \\cot^2 x) (-d(\\cot x))\n$$\n$$\n= -\\int (1 + \\cot^2 x) \\, d(\\cot x)\n$$'),
        ('\\sec x \\tan x - \\int \\tan x \\cdot (\\sec x \\tan x) \\, dx\n$$\n= \\sec x \\tan x - \\int \\sec x \\tan^2 x \\, dx\n$$',
         '\\sec x \\tan x - \\int \\tan x \\cdot (\\sec x \\tan x) \\, dx\n$$\n$$\n= \\sec x \\tan x - \\int \\sec x \\tan^2 x \\, dx\n$$'),
        ('\\int \\sec^3 x \\, dx = \\sec x \\tan x - \\int \\sec x (\\sec^2 x - 1) \\, dx\n$$\n\\int \\sec^3 x \\, dx = \\sec x \\tan x - \\int \\sec^3 x \\, dx + \\int \\sec x \\, dx\n$$',
         '\\int \\sec^3 x \\, dx = \\sec x \\tan x - \\int \\sec x (\\sec^2 x - 1) \\, dx\n$$\n$$\n\\int \\sec^3 x \\, dx = \\sec x \\tan x - \\int \\sec^3 x \\, dx + \\int \\sec x \\, dx\n$$'),
        ('\\cos^2 x \\cdot \\sin x \\, dx\n$$\n= \\int (1 - \\cos^2 x) (-d(\\cos x))\n$$\n= \\int (\\cos^2 x - 1) \\, d(\\cos x)\n$$',
         '\\cos^2 x \\cdot \\sin x \\, dx\n$$\n$$\n= \\int (1 - \\cos^2 x) (-d(\\cos x))\n$$\n$$\n= \\int (\\cos^2 x - 1) \\, d(\\cos x)\n$$'),
    ]
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
    return s
FIX['core-283.answer'] = fix_283

# ---------------- core-424: 上一轮产生「$$$$」粘连：闭块与开块合并为「$$\n$$\n」----
def fix_424(s):
    # 上轮 token 化把块写成 '$$\nX\n$$' 紧挨 '$$\nY\n$$' → 出现 '$$\n$$' 或 'X\n$$\n$$\nY'，
    # mdBlock 视 '$$' 行为开块、'$$' 行闭块 —— '$$\n$$\n' 是空块，无害；但 'X\n$$\n$$\n' 后面接 'Y'
    # 正确结构应每块独立：$$\nX\n$$\n\n$$\nY\n$$ …这里已经是。坏点实质：中文行「故 4\dfrac…」夹到了块内。
    # 检查并对「故」行处理：如果 "故 4\dfrac" 前面是 "$$\n" 孤行，说明中文被吞进块。
    # 直接修正：确保「故 4\dfrac{...}」行不在 $$...$$ 块内。定位该行上下文。
    idx = s.find('故 4\\dfrac')
    if idx > 0:
        # 前一个 $$ 与后一个 $$ 的配对
        before = s[:idx]
        # 若 before 以 '\n$$\n' 结尾（开块孤行）→ 说明故 进块；改为 '\n$$\n故 $...$'
        if before.endswith('\n$$\n'):
            # 找到故行结束（下一个 \n 或 $$）
            s = s[:idx] + '故 $4\\dfrac{\\partial^{2}u}{\\partial x^{2}}+12\\dfrac{\\partial^{2}u}{\\partial x\\partial y}+5\\dfrac{\\partial^{2}u}{\\partial y^{2}}$\n'
            s = s.replace('\\partial y^{2}}$\n$$\n', '\\partial y^{2}}$\n$$\n')
            s = s.replace('\\partial y^{2}}$\n\n$$', '\\partial y^{2}}$\n\n$$')
    # 通用清理：\n$$\n$$\n -> \n$$\n（空块一次）避免连续空块干扰
    s = s.replace('\n$$\n$$\n', '\n$$\n')
    # 保证每个公式行后的 $$ 与下一块隔一行？不需要。
    return s
FIX['core-424.answer'] = fix_424

# ---------------- core-431: 【答案】$$ 行内开块；若干同行 $$X$$ 保持 -----
def fix_431(s):
    # 开头【答案】$$..$$ 拆独立行
    old = '【答案】$$\n\\frac{1}{8e^2}\n$$'
    new = '【答案】\n$$\n\\frac{1}{8e^2}\n$$'
    if old in s:
        s = s.replace(old, new)
    # 尾部 **答案：** 前的空块
    s = s.replace('**答案：**\n$$\n$$\\frac{1}{8e^2}$$', '**答案：**\n$$\n\\frac{1}{8e^2}\n$$')
    return s
FIX['core-431.answer'] = fix_431

if __name__ == '__main__':
    data = load()
    n_ok = n_noop = 0
    for k, fn in FIX.items():
        no = k.split('-')[1].split('.')[0]
        field = k.split('.')[1]
        q = find_q(data, no)
        if q is None or field not in q:
            print('MISS Q:', k)
            continue
        old = q[field]
        new = fn(old)
        if new == old:
            print('NOOP :', k)
            n_noop += 1
        q[field] = new
        n_ok += 1
    print('applied:', n_ok, 'noop:', n_noop)
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('written.')