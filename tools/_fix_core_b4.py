# -*- coding: utf-8 -*-
# 修复 core_bank.json 剩余 4 字段（批次4：精确修正）
import json, io, sys, re
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

# ---------------- core-383: 同行块拆分 ----------------
def fix_383(s):
    old = '$$F(x)=\\begin{cases}\\displaystyle\\int_0^x\\sin t\\,dt=1-\\cos x,&0\\le x<\\pi,\\\\[6pt]\\displaystyle\\int_0^\\pi\\sin t\\,dt+\\int_\\pi^x2\\,dt=2(x-\\pi+1),&\\pi\\le x\\le2\\pi.\\end{cases}$$\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,$$'
    new = '$$F(x)=\\begin{cases}\\displaystyle\\int_0^x\\sin t\\,dt=1-\\cos x,&0\\le x<\\pi,\\\\[6pt]\\displaystyle\\int_0^\\pi\\sin t\\,dt+\\int_\\pi^x2\\,dt=2(x-\\pi+1),&\\pi\\le x\\le2\\pi.\\end{cases}$$\n$$\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,$$'
    if old in s:
        return s.replace(old, new)
    # 兜底：在 \end{cases}$$ 后补换行与开块
    s = re.sub(r'(\\end\{cases\})\$\$(\\lim)', r'\1$$\n$$\2', s)
    return s
FIX['core-383.answer'] = fix_383

# ---------------- core-424: 把裸公式行（无中文、含\ 命令、无 $）自动包块；处理 $$$$ 粘连 ----------------
def fix_424(s):
    # 1) 清 $$$$ 粘连（连续4美元字符 = 闭+开）
    s = s.replace('$$$$', '$$\n$$')
    # 2) 通用兜底：独立「裸公式行」自动包 $$..$$（与 mdBlock 兜底一致，但更彻底，
    #    因为 mdBlock 的兜底仅对整行且含 [=+\-^_{}] 生效；这里针对所有行构造良好结构）
    out = []
    for line in s.split('\n'):
        l = line.strip()
        # 跳过块标记/中文行/空行/已有$的行
        if l == '' or l.startswith('$$') or l.endswith('$$') or '$' in l:
            out.append(line)
            continue
        if not re.search(r'[\u4e00-\u9fff]', l) and '\\' in l and l != '$$':
            # 裸公式行 → 包成独立显示块
            out.append('$$\n' + l + '\n$$')
        else:
            out.append(line)
    return '\n'.join(out)
FIX['core-424.answer'] = fix_424

# ---------------- core-274: 剩余坏点 ----------------
def fix_274(s):
    # 坏点1: "则：\n$$\n$$v = ...$$\n$$\n" —— 双 $$ 行 + 同行块
    old = '则：\n$$\n$$v = \\int (2t^3 + 2t) dt = \\frac{1}{2}t^4 + t^2 = \\frac{1}{2}(t^4 + 2t^2)$$\n$$'
    new = '则：\n$$\nv = \\int (2t^3 + 2t) dt = \\frac{1}{2}t^4 + t^2 = \\frac{1}{2}(t^4 + 2t^2)\n$$'
    if old in s:
        s = s.replace(old, new)
    # 坏点2: $$\n$$I = ...$$\n$$\nI = ...\n$$\n
    old2 = '$$\n$$I = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\int \\frac{1}{2}(t^2+1)^2 \\cdot \\frac{1}{1+t^2} dt$$\n$$\nI = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\frac{1}{2} \\int (t^2+1) dt\n$$'
    new2 = '$$\nI = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\int \\frac{1}{2}(t^2+1)^2 \\cdot \\frac{1}{1+t^2} dt\n$$\n$$\nI = \\frac{1}{2}(t^2+1)^2 \\arctan t - \\frac{1}{2} \\int (t^2+1) dt\n$$'
    if old2 in s:
        s = s.replace(old2, new2)
    # 坏点3: I2 与 I3 同行块（行55/57?）看 probe：55 '$$' 57 '$$'——先跑再定
    return s
FIX['core-274.answer'] = fix_274

# ---------------- core-283: 兜底裸公式行 + 同行块修正 ----------------
def fix_283(s):
    # 同行 $$..$$（含中文夹行的）拆开
    s = s.replace('\\cos^2 2x = \\frac{1 + \\cos 4x}{2}$：', '\\cos^2 2x = \\frac{1 + \\cos 4x}{2}$：')
    # 逐行处理：裸公式行包块
    out = []
    for line in s.split('\n'):
        l = line.strip()
        if l == '' or l.startswith('$$') or l.endswith('$$') or '$' in l:
            out.append(line)
            continue
        if not re.search(r'[\u4e00-\u9fff]', l) and '\\' in l:
            # 若整行既有公式又含配角（如 "= X + Y" 无中文）→ 包块；含中文则跳过（中文行内再单独包）
            out.append('$$\n' + l + '\n$$')
        else:
            out.append(line)
    return '\n'.join(out)
FIX['core-283.answer'] = fix_283

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