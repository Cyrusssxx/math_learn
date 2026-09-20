# -*- coding: utf-8 -*-
# 修复 core_bank.json 剩余残留字段（批次2 修订版：逐字段内容级规范化）
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

# ---------- core-268: 中文行内裸公式 ----------
def fix_268(s):
    s = s.replace('最后，将 t = \\sqrt{e^x - 1} 以及 \\ln(t^2 + 1) = x 代回上式中：',
                  '最后，将 $t = \\sqrt{e^x - 1}$ 以及 $\\ln(t^2 + 1) = x$ 代回上式中：')
    return s
FIX['core-268.answer'] = fix_268

# ---------- core-274: 引用块裸公式 ----------
def fix_274(s):
    s = s.replace('> 观察到 \\frac{d}{dt} \\left[ \\frac{1}{2}(t^2+1)^2 \\right] = \\frac{1}{2} \\cdot 2(t^2+1) \\cdot 2t = 2t^3 + 2t。',
                  '> 观察到 $\\frac{d}{dt} \\left[ \\frac{1}{2}(t^2+1)^2 \\right] = \\frac{1}{2} \\cdot 2(t^2+1) \\cdot 2t = 2t^3 + 2t$。')
    s = s.replace('> 所以我们取 **v = \\frac{1}{2}(t^2+1)^2**。',
                  '> 所以我们取 **$v = \\frac{1}{2}(t^2+1)^2$**。')
    s = s.replace('根据分部积分公式 \\int u dv = uv - \\int v du：',
                  '根据分部积分公式 $\\int u\\,dv = uv - \\int v\\,du$：')
    return s
FIX['core-274.answer'] = fix_274

# ---------- core-283: 中文行内裸公式（多处） ----------
def fix_283(s):
    s = s.replace('对其中的 \\cos^2 2x 再次使用降幂公式 \\cos^2 2x = \\frac{1 + \\cos 4x}{2}：',
                  '对其中的 $\\cos^2 2x$ 再次使用降幂公式 $\\cos^2 2x = \\frac{1 + \\cos 4x}{2}$：')
    s = s.replace('### (3) \\int \\csc^4 x \\, dx', '### (3) $\\int \\csc^4 x \\, dx$')
    s = s.replace('### (4) \\int \\sec^3 x \\, dx', '### (4) $\\int \\sec^3 x \\, dx$')
    s = s.replace('将 \\csc^4 x 拆分为 \\csc^2 x \\cdot \\csc^2 x，并利用公式 \\csc^2 x = 1 + \\cot^2 x 以及 d(\\cot x) = -\\csc^2 x \\, dx。',
                  '将 $\\csc^4 x$ 拆分为 $\\csc^2 x \\cdot \\csc^2 x$，并利用公式 $\\csc^2 x = 1 + \\cot^2 x$ 以及 $d(\\cot x) = -\\csc^2 x \\, dx$。')
    s = s.replace('直接对 \\cot x 积分：', '直接对 $\\cot x$ 积分：')
    s = s.replace('设 u = \\sec x，dv = \\sec^2 x \\, dx。', '设 $u = \\sec x$，$dv = \\sec^2 x \\, dx$。')
    s = s.replace('则 du = \\sec x \\tan x \\, dx，v = \\tan x。', '则 $du = \\sec x \\tan x \\, dx$，$v = \\tan x$。')
    s = s.replace('应用分部积分公式 \\int u \\, dv = uv - \\int v \\, du：',
                  '应用分部积分公式 $\\int u \\, dv = uv - \\int v \\, du$：')
    s = s.replace('将右侧的 -\\int \\sec^3 x \\, dx 移项到等式左边：',
                  '将右侧的 $-\\int \\sec^3 x \\, dx$ 移项到等式左边：')
    s = s.replace('我们已知 \\int \\sec x \\, dx = \\ln |\\sec x + \\tan x| + C_1，代入上式并除以 2：',
                  '我们已知 $\\int \\sec x \\, dx = \\ln |\\sec x + \\tan x| + C_1$，代入上式并除以 2：')
    return s
FIX['core-283.answer'] = fix_283

# ---------- core-339: 跨行 $u=\ln x,\n dv=... ----------
def fix_339(s):
    old = '分部积分（$u=\\ln x,\n dv=(2-x)dx$）：'
    if old in s:
        s = s.replace(old, '分部积分（$u=\\ln x,\\ dv=(2-x)dx$）：')
    return s
FIX['core-339.answer'] = fix_339

# ---------- core-383: 块粘连缺开块（修正 old） ----------
def fix_383(s):
    old = '\\end{cases}$$\n\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,$$'
    new = '\\end{cases}$$\n$$\n\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,$$'
    if old in s:
        s = s.replace(old, new)
    else:
        old2 = '\\end{cases}$$\n\\lim_{x\\to\\pi^-}F(x)'
        if old2 in s:
            s = s.replace(old2, '\\end{cases}$$\n$$\n\\lim_{x\\to\\pi^-}F(x)')
    return s
FIX['core-383.answer'] = fix_383

# ---------- core-405: \substack 内换行 -> \\ ----------
def fix_405(s):
    s = s.replace('\\substack{x\\to 0\n y\\to 1}', '\\substack{x\\to 0\\\\ y\\to 1}')
    s = s.replace('\\text{则}', '则')
    return s
FIX['core-405.stem'] = fix_405

# ---------- core-412: \substack{u=1\nv=1} 两处 ----------
def fix_412(s):
    s = s.replace('\\right|_{\\substack{u=1\nv=1}}', '\\right|_{\\substack{u=1\\\\v=1}}')
    s = s.replace('\\text{与}', '与')
    return s
FIX['core-412.stem'] = fix_412

# ---------- core-413.stem: 整体重写 ----------
def fix_413stem(s):
    return '设函数 $F(x,y)=\\int_0^{xy}\\frac{\\sin t}{1+t^2}\\,dt$，则 $\\left.\\frac{\\partial^2 F}{\\partial x^2}\\right|_{\\substack{x=0\\\\y=2}}=$ ______.'
FIX['core-413.stem'] = fix_413stem

# ---------- core-413.answer/idea: 第二块缺开块 ----------
def fix_413(s):
    old = '$$\n\\frac{\\partial F}{\\partial x}=y\\cdot\\frac{\\sin(xy)}{1+(xy)^{2}}\n$$\n\\frac{\\partial^{2}F}{\\partial x^{2}}=y\\cdot\\frac{y\\cos(xy)\\cdot(1+(xy)^{2})-\\sin(xy)\\cdot2xy^{2}}{(1+(xy)^{2})^{2}}\n$$'
    new = '$$\n\\frac{\\partial F}{\\partial x}=y\\cdot\\frac{\\sin(xy)}{1+(xy)^{2}}\n$$\n$$\n\\frac{\\partial^{2}F}{\\partial x^{2}}=y\\cdot\\frac{y\\cos(xy)\\cdot(1+(xy)^{2})-\\sin(xy)\\cdot2xy^{2}}{(1+(xy)^{2})^{2}}\n$$'
    if old not in s:
        # 容错：直接找 \frac{\partial^{2}F 前是否紧跟 $$
        idx = s.find('\\frac{\\partial^{2}F}{\\partial x^{2}}')
        if idx > 0:
            prev = s[:idx]
            if not prev.endswith('$$\n'):
                # 找到上一个块结尾 $$\n，在其后补 $$\n
                m = re.search(r'(\$\$)\n', s[:idx])
                if m:
                    cut = m.end()
                    s = s[:cut] + '$$\n' + s[cut:]
        return s
    return s.replace(old, new)
FIX['core-413.answer'] = fix_413
FIX['core-413.idea'] = fix_413

# ---------- core-419: 第二个块缺开块 ----------
def fix_419(s):
    old = '$$\n \\frac{\\mathrm{d}y}{\\mathrm{d}x}=\\frac{\\partial f}{\\partial u}\\cdot(-\\sin x)+\\frac{\\partial f}{\\partial v}\\cdot(2x) \n$$\n \\begin{aligned}\\frac{\\mathrm{d}^{2}y}{\\mathrm{d}x^{2}}=&'
    new = '$$\n \\frac{\\mathrm{d}y}{\\mathrm{d}x}=\\frac{\\partial f}{\\partial u}\\cdot(-\\sin x)+\\frac{\\partial f}{\\partial v}\\cdot(2x) \n$$\n$$\n \\begin{aligned}\\frac{\\mathrm{d}^{2}y}{\\mathrm{d}x^{2}}=&'
    if old in s:
        return s.replace(old, new)
    # 容错：\begin{aligned} 前补 $$
    idx = s.find('\\begin{aligned}')
    if idx > 0:
        prev = s[:idx]
        if not prev.rstrip().endswith('$$'):
            m = re.search(r'(\$\$)\s*$', prev, re.M)
            if m and not prev.endswith('$$\n') and not prev.endswith('$$ '):
                s = s[:m.start()+2] + '\n$$\n' + s[m.end():]
    return s
FIX['core-419.answer'] = fix_419

# ---------- core-420: \substack{x=1\ny=1} ----------
def fix_420(s):
    s = s.replace('\\right|_{\\substack{x=1\ny=1}}', '\\right|_{\\substack{x=1\\\\y=1}}')
    return s
FIX['core-420.stem'] = fix_420

# ---------- core-424: 整段链式块重排为独立显示块 ----------
def fix_424(s):
    # 把「$$A$$\nB$$\nC$$...」链 拆成「$$\nA\n$$\n\n$$\nB\n$$\n...」。
    # 策略：找到所有以 $$ 开头、到下一个 $$ 为止的子串逐个换成独立块。
    # 424 的链全部是「$$X$$内容$$Y$$...」同行或跨行结构，用正则切分太脆弱，
    # 直接按原文语义重构（分式内容不变，仅重组定界符）。
    head = '【解析】由复合函数链式法则得\n'
    body = s[len(head):]
    # 从 body 中提取每个「$$公式$$」或「公式$$」片段：
    # 输入形如: $$A$$\nB$$\nC$$=D$$\nE$$\n故 ...\n$$=F$$
    # 目标: 每个公式独立成 $$\n...\n$$ 块，中文行保留
    # 用 token 化：$$x$$ 视为完整块（含起始$$），随后紧跟内容（非$$开头）直到下一个$$，
    # 把「内容+$$」补成「$$\n内容\n$$」。
    # 简单可靠法：把 body 中所有连续公式行重组。
    parts = []
    # 先按 $$\n 与 \n$$ 把链切分
    tokens = re.split(r'(\$\$)', body)
    # tokens: [txt, '$$', txt, '$$', ...] —— 重组为成对块
    out_tokens = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == '$$':
            # 向后收集到下一个 $$（数学内容展开可能含换行）
            j = i + 1
            buf = []
            while j < len(tokens):
                if tokens[j] == '$$':
                    break
                buf.append(tokens[j])
                j += 1
            content = ''.join(buf).strip()
            if content:
                out_tokens.append('$$\n' + content + '\n$$')
                # 若内容以 \\ 结尾& 无 env，保持
            else:
                out_tokens.append('$$')
            i = j + 1
        else:
            # 非 $$ 文本：若为「中文行内裸公式」保持原样；若是公式内容（在块外）补块
            if t.strip() and not re.search(r'[\u4e00-\u9fff]', t) and '\\' in t:
                out_tokens.append('$$\n' + t.strip() + '\n$$')
            else:
                out_tokens.append(t)
            i += 1
    return head + ''.join(out_tokens)
FIX['core-424.answer'] = fix_424

# ---------- core-425: 中文裸公式 + 连续空块清理 ----------
def fix_425(s):
    s = s.replace('代入原方程 2u_{xx}-2u_{yy}+3u_x+3u_y=0，各项约去公因子 e^{ax+by}：',
                  '代入原方程 $2u_{xx}-2u_{yy}+3u_x+3u_y=0$，各项约去公因子 $e^{ax+by}$：')
    s = s.replace('令系数为 0：\n$$\n$$\n4a+3=0,\\qquad 3-4b=0', '令系数为 0：\n$$\n4a+3=0,\\qquad 3-4b=0')
    s = s.replace('$$\n$$\n$$\n2\\left(v_{xx}+2av_x+a^2v\\right)', '$$\n2\\left(v_{xx}+2av_x+a^2v\\right)')
    s = s.replace('+3(v_x+av)+3(v_y+bv)=0\n$$\n$$\n按', '+3(v_x+av)+3(v_y+bv)=0\n$$\n按')
    return s
FIX['core-425.answer'] = fix_425

# ---------- core-431: 尾部 **答案：** 空块 ----------
def fix_431(s):
    s = s.replace('**答案：**\n$$\n$$\\frac{1}{8e^2}$$', '**答案：**\n$$\n\\frac{1}{8e^2}\n$$')
    return s
FIX['core-431.answer'] = fix_431

# ---------- core-442: 中文行内 \begin{cases} 裸公式 + f_y' 块前缺开 ----------
def fix_442(s):
    s = s.replace('令 \\begin{cases}\\dfrac{2x^{2}+x-1-y^{2}}{x^{3}}=0,\\\\\\dfrac{y}{x^{2}}=0,\\end{cases} 解得 y=0,x=\\dfrac{1}{2} 或 x=-1。于是，f(x,y) 有两个驻点 (-1,0),\\left(\\dfrac{1}{2},0\\right)。',
                  '令 $\\begin{cases}\\dfrac{2x^{2}+x-1-y^{2}}{x^{3}}=0,\\\\\\dfrac{y}{x^{2}}=0,\\end{cases}$ 解得 $y=0,\\ x=\\dfrac{1}{2}$ 或 $x=-1$。于是，$f(x,y)$ 有两个驻点 $(-1,0),\\left(\\dfrac{1}{2},0\\right)$。')
    # f_y'(x,y)=...$$ 缺开块：前面是 \end{aligned}\n$$\n
    old = '\\end{aligned}\n$$\nf_{y}^{\\prime}(x,y)=\\frac{2y}{2x^{2}}=\\frac{y}{x^{2}}.\n$$'
    new = '\\end{aligned}\n$$\n$$\nf_{y}^{\\prime}(x,y)=\\frac{2y}{2x^{2}}=\\frac{y}{x^{2}}.\n$$'
    if old in s:
        s = s.replace(old, new)
    # f_xy'' 与 f_yy'' 同理
    old2 = '\\end{aligned}\n$$\nf_{xy}^{\\prime\\prime}(x,y)=-\\frac{2y}{x^{3}}.\n$$\nf_{yy}^{\\prime\\prime}(x,y)=\\frac{1}{x^{2}}.\n$$'
    new2 = '\\end{aligned}\n$$\n$$\nf_{xy}^{\\prime\\prime}(x,y)=-\\frac{2y}{x^{3}}.\n$$\n$$\nf_{yy}^{\\prime\\prime}(x,y)=\\frac{1}{x^{2}}.\n$$'
    if old2 in s:
        s = s.replace(old2, new2)
    return s
FIX['core-442.answer'] = fix_442

# ---------- core-535: 开头【答案】$$ 持块 + 等式链缺开块 ----------
def fix_535(s):
    # 开头:【答案】$$2ex - x e^x$$ —— 单行块 OK；但 mdBlock 行首 【 不触发，改为独立行
    old = '【答案】$$\n2ex - x e^x\n$$'
    new = '【答案】\n$$\n2ex - x e^x\n$$'
    s = s.replace(old, new)
    # e = -e + C / C = 2e 缺开块
    old2 = '$$\ne = -1 \\cdot e^1 + C \\cdot 1\n$$\ne = -e + C\n$$\nC = 2e\n$$'
    new2 = '$$\ne = -1 \\cdot e^1 + C \\cdot 1\n$$\n$$\ne = -e + C\n$$\n$$\nC = 2e\n$$'
    s = s.replace(old2, new2)
    return s
FIX['core-535.answer'] = fix_535

# ---------- core-578: \begin{cases}\end{cases} 空对 ----------
def fix_578(s):
    s = s.replace('$$\n\\begin{cases}\\end{cases}\nx=x(t),\\\\\ny=\\displaystyle\\int_0^{t^2}\\ln(1+u)\\,du\n\\end{cases}\n$$',
                  '$$\n\\begin{cases}\nx=x(t),\\\\\ny=\\displaystyle\\int_0^{t^2}\\ln(1+u)\\,du\n\\end{cases}\n$$')
    s = s.replace('$$\n\\begin{cases}\\end{cases}\n\\dfrac{dx}{dt}-2te^{-x}=0,\\\\x(0)=0\n\\end{cases}\n$$',
                  '$$\n\\begin{cases}\n\\dfrac{dx}{dt}-2te^{-x}=0,\\\\x(0)=0\n\\end{cases}\n$$')
    return s
FIX['core-578.stem'] = fix_578

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