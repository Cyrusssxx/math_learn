# -*- coding: utf-8 -*-
# 修复 core_bank.json 56 个残留字段（批次1：结构性定界符与空环境对）
# 原则：只改格式，数学内容与答案数值不变；\square 保留
import json, re, io, sys
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

# ============ 每字段修复函数：输入原值 -> 输出新值 ============
FIX = {}

# ---- core-100: 两处中文行内裸公式 1+B-A=0 / J=\infty 包 $ ----
def fix_100(s):
    s = s.replace('要求分子极限为 0，即 1+B-A=0，否则 J=\\infty', '要求分子极限为 $0$，即 $1+B-A=0$，否则 $J=\\infty$')
    s = s.replace('要求分子极限为 0，即 1+2B+2C=0，否则 J=\\infty', '要求分子极限为 $0$，即 $1+2B+2C=0$，否则 $J=\\infty$')
    return s
FIX['core-100.answer'] = fix_100

# ---- core-146: 【答案】$$ 行内开块 -> 换行独立；结尾残缺公式段删除留注记 ----
def fix_146(s):
    # 开头：`【答案】$$` 同行，mdBlock 不识别为开块 → 拆成独立行
    s = s.replace('【答案】$$\nf', '【答案】\n$$\nf', 1)
    # 残缺尾部：(2) 的洛必达分子被截断在 g'(x) 后，无法补全且无法渲染 → 整段替换注记
    tail = '$ \\lim_{x\\to0}f\'(x)=\\lim_{x\\to0}\\frac{x g\'(x)-g(x)+x e^{-x}+e^{-x}}{x^{2}}\\stackrel{L}{=}\\lim_{x\\to0}\\frac{g\'(x)+x g\'\'(x)-g\'(x'
    if tail in s:
        s = s.replace(tail, '(2) $ \\lim_{x\\to0}f\'(x)=\\lim_{x\\to0}\\frac{x g\'(x)-g(x)+x e^{-x}+e^{-x}}{x^{2}}\\stackrel{L}{=}\\cdots$（原解答此处数据残缺，已省略）')
    else:
        # 兜底：以 -g'(x 为界截断
        idx = s.find("-g'(x")
        if idx > 0:
            s = s[:idx].rstrip() + '（原解答此处数据残缺，已省略）'
    return s
FIX['core-146.answer'] = fix_146
FIX['core-146.idea'] = fix_146

# ---- core-184: 畸形定界符 $y=x+$\sin\dfrac1x$$ 与 $$k=$..$$..$$$ ----
def fix_184(s):
    s = s.replace('对 $y=x+$\\sin\\dfrac1x$$：', '对 $y=x+\\sin\\dfrac1x$：')
    old = '$$k=$\\lim_{x\\to\\infty}\\frac{y}{x}=\\lim_{x\\to\\infty}\\frac{x+\\sin\\frac1x}{x}=1,$$b=\\lim_{x\\to\\infty}(y-kx)=\\lim_{x\\to\\infty}\\sin\\frac1x=0,$$$'
    new = '$$k=\\lim_{x\\to\\infty}\\frac{y}{x}=\\lim_{x\\to\\infty}\\frac{x+\\sin\\frac1x}{x}=1,\\qquad b=\\lim_{x\\to\\infty}(y-kx)=\\lim_{x\\to\\infty}\\sin\\frac1x=0.$$'
    s = s.replace(old, new)
    return s
FIX['core-184.answer'] = fix_184

# ---- core-188: 块粘连 a=...$$b=...$$ 缺开块 ----
def fix_188(s):
    old = '=1$$b = \\lim_{x \\to +\\infty} (y-a\\cdot x)'
    new = '=1$$\n$$\nb = \\lim_{x \\to +\\infty} (y-a\\cdot x)'
    s = s.replace(old, new)
    return s
FIX['core-188.answer'] = fix_188

# ---- core-5: $$..\begin{aligned}\end{aligned} 空对 -> begin 让内容进环境 ----
def fix_5(s):
    old = '$$\n\\begin{aligned}\\end{aligned}\nG(x+2)'
    new = '$$\n\\begin{aligned}\nG(x+2)'
    s = s.replace(old, new)
    return s
FIX['core-5.answer'] = fix_5
FIX['core-5.idea'] = fix_5

# ---- core-73: a_{n+1}.. 缺开块 + 中文行 `所以{a_n}` 包 ----
def fix_73(s):
    old = '=f(k),\n$$\na_{n+1}-a_{n}=\\sum_{k=1}^{n+1}f(k)-\\sum_{k=1}^{n}f(k)-\\int_{1}^{n+1}f(x)\\mathrm{d}x+\\int_{1}^{n}f(x)\\mathrm{d}x=f(n+1)-\\int_{n}^{n+1}f(x)\\mathrm{d}x\\leqslant0,\n$$\n所以\\{a_{n}\\}单调减少。又由上式，知\n$$\nf(k)-\\int_{k}^{k+1}f(x)\\mathrm{d}x\\geqslant0,\\int_{n}^{n+1}f(x)\\mathrm{d}x\\geqslant0,\n$$\n故'
    new = '=f(k),\n$$\n$$\na_{n+1}-a_{n}=\\sum_{k=1}^{n+1}f(k)-\\sum_{k=1}^{n}f(k)-\\int_{1}^{n+1}f(x)\\mathrm{d}x+\\int_{1}^{n}f(x)\\mathrm{d}x=f(n+1)-\\int_{n}^{n+1}f(x)\\mathrm{d}x\\leqslant0,\n$$\n所以$\\{a_{n}\\}$单调减少。又由上式，知\n$$\nf(k)-\\int_{k}^{k+1}f(x)\\mathrm{d}x\\geqslant0,\\int_{n}^{n+1}f(x)\\mathrm{d}x\\geqslant0,\n$$\n故'
    s = s.replace(old, new)
    return s
FIX['core-73.answer'] = fix_73
FIX['core-73.idea'] = fix_73

# ---- core-133: 字面 \n 两字符 -> 真实换行 ----
def fix_133(s):
    s = s.replace('\\n', '\n')
    return s
FIX['core-133.answer'] = fix_133
FIX['core-133.idea'] = fix_133

# ---- core-194: 【答案】$$ 行内开块 -> 独立行 ----
def fix_194(s):
    s = s.replace('【答案】$$\ny=', '【答案】\n$$\ny=', 1)
    return s
FIX['core-194.answer'] = fix_194

# ---- core-217: 多处问题 ----
def fix_217(s):
    s = s.replace('【答案】【答案】', '【答案】')
    # 故 f(x)=$..$。当 x\ge1 时  -> 行内裸公式归位
    s = s.replace('故 f(x)=$\\dfrac43x^3-x^2+\\dfrac13$。当 x\\ge1 时，', '故 $f(x)=\\dfrac43x^3-x^2+\\dfrac13$。当 $x\\ge1$ 时，')
    # 连续三个 $$ 空块 -> 单个显示块
    s = s.replace('当 $x\\ge1$ 时，\n$$\n$$\n$$\nf(x)=', '当 $x\\ge1$ 时，\n$$\nf(x)=')
    s = s.replace('=x^2-\\frac13\n$$\n$$\n分段求导', '=x^2-\\frac13\n$$\n分段求导')
    s = s.replace('分段求导：f\'(x)=\\begin{cases}4x^2-2x,&0<x<1\\\\2x,&x\\ge1\\end{cases}，且 f\'_-(1)=2=f\'_+(1)，f\'(x) 在 x=1 连续。',
                  '分段求导：$f\'(x)=\\begin{cases}4x^2-2x,&0<x<1\\\\2x,&x\\ge1\\end{cases}$，且 $f\'_-(1)=2=f\'_+(1)$，$f\'(x)$ 在 $x=1$ 连续。')
    s = s.replace('令 f\'(x)=0 得 x=\\dfrac12。当 0<x<\\dfrac12 时 2x(2x-1)<0，当 x>\\dfrac12 时 f\'(x)>0，故最小值在 x=\\dfrac12 处取得：\n$$\n$$\nf\\left(\\frac12\\right)',
                  '令 $f\'(x)=0$ 得 $x=\\dfrac12$。当 $0<x<\\dfrac12$ 时 $2x(2x-1)<0$，当 $x>\\dfrac12$ 时 $f\'(x)>0$，故最小值在 $x=\\dfrac12$ 处取得：\n$$\nf\\left(\\frac12\\right)')
    # 尾部 .$$$$ 空块删
    s = s.replace('。$$$$', '。')
    return s
FIX['core-217.answer'] = fix_217

# ---- core-231: 块粘连 ;$$\lim_{x\to+\infty} 缺开块 ----
def fix_231(s):
    old = '+\\infty;$$\n\\lim_{x\\to +\\infty}\\varphi(x)'
    if old in s:
        return s
    old2 = '+\\infty;$$\\lim_{x\\to +\\infty}\\varphi(x)'
    new2 = '+\\infty;$$\n$$\\lim_{x\\to +\\infty}\\varphi(x)'
    s = s.replace(old2, new2)
    return s
FIX['core-231.answer'] = fix_231

# ---- core-249 / 265 / 278 / 299 / 503: \begin{aligned}\end{aligned} 空对 ----
def fix_aligned_env(s):
    old = '\n$$\n\\begin{aligned}\\end{aligned}\nI&='
    new = '\n$$\n\\begin{aligned}\nI&='
    s = s.replace(old, new)
    return s
FIX['core-249.answer'] = fix_aligned_env
FIX['core-249.idea'] = fix_aligned_env
def fix_265(s):
    s = s.replace('\\begin{aligned}\\end{aligned}\nI&=', '\\begin{aligned}\nI&=')
    return s
FIX['core-265.answer'] = fix_265
FIX['core-265.idea'] = fix_265
def fix_278(s):
    s = s.replace('\\begin{aligned}\\end{aligned}\n\\int_1^{e^2}', '\\begin{aligned}\n\\int_1^{e^2}')
    return s
FIX['core-278.answer'] = fix_278
FIX['core-278.idea'] = fix_278
def fix_299(s):
    s = s.replace('\\begin{aligned}\\end{aligned}\nI&=', '\\begin{aligned}\nI&=')
    return s
FIX['core-299.answer'] = fix_299
FIX['core-299.idea'] = fix_299
def fix_503(s):
    s = s.replace('\\begin{aligned}\\end{aligned}\nI&=', '\\begin{aligned}\nI&=')
    return s
FIX['core-503.answer'] = fix_503
FIX['core-503.idea'] = fix_503

# ---- core-256: 【答案】$$ / 空块 ----
def fix_256(s):
    s = s.replace('【答案】$$\n\\int', '【答案】\n$$\n\\int', 1)
    return s
FIX['core-256.answer'] = fix_256

# ---- core-267: \begin{align*}\end{align*} 空对 -> \begin{aligned} ----
def fix_267(s):
    s = s.replace('\\begin{align*}\\end{align*}\n\\int_0^1', '\\begin{aligned}\n\\int_0^1')
    s = s.replace('\\end{align*}\n$$', '\\end{aligned}\n$$')
    return s
FIX['core-267.answer'] = fix_267
FIX['core-267.idea'] = fix_267

# ---- core-273: 两处空对（方法一 align*，方法二 aligned）----
def fix_273(s):
    s = s.replace('\\begin{align*}\\end{align*}\n\\int_0^1', '\\begin{aligned}\n\\int_0^1')
    s = s.replace('\\end{align*}\n$$', '\\end{aligned}\n$$')
    s = s.replace('\\begin{aligned}\\end{aligned}\n\\int_0^1', '\\begin{aligned}\n\\int_0^1')
    return s
FIX['core-273.answer'] = fix_273

# ---- core-295: \text{______} 下划线需转义 ----
def fix_295(s):
    s = s.replace('\\text{______}', '\\text{\\_\\_\\_\\_\\_\\_}')
    return s
FIX['core-295.stem'] = fix_295

# ---- core-319: $ 嵌套畸形 ----
def fix_319(s):
    s = s.replace('由归纳法 $f_n(x)=$\\dfrac{x}{1+nx}$$：', '由归纳法 $f_n(x)=\\dfrac{x}{1+nx}$：')
    s = s.replace('$$f_{n+1}(x)=$\\frac{f_n(x)}{1+f_n(x)}', '$$f_{n+1}(x)=\\frac{f_n(x)}{1+f_n(x)}')
    s = s.replace('=\\frac{x}{1+(n+1)x}.$$S_n=', '=\\frac{x}{1+(n+1)x}.$$\n$$\nS_n=')
    s = s.replace('\\frac1n\\left[1-\\frac1n\\ln(1+n)\\right].$$nS_n=', '\\frac1n\\left[1-\\frac1n\\ln(1+n)\\right].$$\n$$\nnS_n=')
    s = s.replace('nS_n=1-\\frac{\\ln(1+n)}{n}\\ \\Rightarrow\\ \\lim_{n\\to\\infty}nS_n=1.$$$', 'nS_n=1-\\frac{\\ln(1+n)}{n}\\ \\Rightarrow\\ \\lim_{n\\to\\infty}nS_n=1.$$')
    return s
FIX['core-319.answer'] = fix_319

# ---- core-339: 跨行 $x=1,\n 2$ 与 \text{绕} ----
def fix_339(s):
    s = s.replace('对应 $x=1,\n 2$。\\text{绕} $y=-1$ 旋转', '对应 $x=1,2$。绕 $y=-1$ 旋转')
    s = s.replace('对应 $x=1, 2$。\\text{绕} $y=-1$ 旋转', '对应 $x=1,2$。绕 $y=-1$ 旋转')
    return s
FIX['core-339.answer'] = fix_339

# ---- core-346: 块粘连 \,dt$$\stackrel 缺开块 ----
def fix_346(s):
    old = '\\sqrt{1+\\sin^{2}t}\\,dt$$\\stackrel{t=\\frac{\\pi}{2}-u}{=}'
    new = '\\sqrt{1+\\sin^{2}t}\\,dt$$\n$$\\stackrel{t=\\frac{\\pi}{2}-u}{=}'
    s = s.replace(old, new)
    return s
FIX['core-346.answer'] = fix_346

# ---- core-347: 中文行内裸公式 ----
def fix_347(s):
    s = s.replace('这里 r=a(1+\\cos\\theta)，r^{\\prime}=-a\\sin\\theta，', '这里 $r=a(1+\\cos\\theta)$，$r^{\\prime}=-a\\sin\\theta$，')
    s = s.replace('故根号内为 a^2[(1+\\cos\\theta)^2+\\sin^2\\theta]=4a^2\\cos^2(\\theta/2)。', '故根号内为 $a^2[(1+\\cos\\theta)^2+\\sin^2\\theta]=4a^2\\cos^2(\\theta/2)$。')
    s = s.replace('因此 L=\\int_0^{2\\pi}2a|\\cos(\\theta/2)|d\\theta=8a。', '因此 $L=\\int_0^{2\\pi}2a|\\cos(\\theta/2)|d\\theta=8a$。')
    return s
FIX['core-347.answer'] = fix_347
def fix_347idea(s):
    s = s.replace('这里 r=a(1+\\cos\\theta)，r^{\\prime}=-a\\sin\\theta，\n', '这里 $r=a(1+\\cos\\theta)$，$r^{\\prime}=-a\\sin\\theta$，')
    # idea 的畸形: a^2[(1+$\cos\theta)^2+\sin^2\theta]=4a^2\cos^2(\theta/2)$
    s = s.replace('故根号内为 a^2[(1+$\\cos\\theta)^2+\\sin^2\\theta]=4a^2\\cos^2(\\theta/2)$ 。', '故根号内为 $a^2[(1+\\cos\\theta)^2+\\sin^2\\theta]=4a^2\\cos^2(\\theta/2)$。')
    s = s.replace('因此 L=\\int_0^{2\\pi}2a|\\cos(\\theta/2)|d\\theta=8a。', '因此 $L=\\int_0^{2\\pi}2a|\\cos(\\theta/2)|d\\theta=8a$。')
    return s
FIX['core-347.idea'] = fix_347idea

# ---- core-352: 【答案】【答案】重复；,$$ 逗号粘连；尾部空块 ----
def fix_352(s):
    s = s.replace('【答案】【答案】', '【答案】')
    s = s.replace('\n$$\n,$$s=\\int_4^9', '\n$$\n$$s=\\int_4^9')
    s = s.replace('$$$$', '')
    return s
FIX['core-352.answer'] = fix_352

# ---- core-353: 尾部截断残缺（表面积 S 公式被截断）----
def fix_353(s):
    tail = '$S = 2\\pi + 2\\pi\\int_{0}^{\\frac{\\pi}{2}} y(t) \\sqrt{[x\'(t)]^{2} + [y\'(t)]^{2}} dt = 2\\pi + 2\\pi\\int_{0}^{\\frac{\\pi}{2}} \\sin^{3} t \\sqrt{(3\\cos^{2} t (-\\sin t))^'
    new = '$S = 2\\pi + 2\\pi\\int_{0}^{\\frac{\\pi}{2}} y(t) \\sqrt{[x\'(t)]^{2} + [y\'(t)]^{2}} dt$（原解答此处数据残缺，已省略）'
    if tail in s:
        s = s.replace(tail, new)
    else:
        idx = s.find('\\sqrt{(3\\cos^{2}')
        if idx > 0:
            idx2 = s.find('$$', idx)
            s = s[:idx] + '$' + '（原解答此处数据残缺，已省略）'
    return s
FIX['core-353.answer'] = fix_353
FIX['core-353.idea'] = fix_353

# ---- core-364: 面积 S=$...$.$$ 尾 $ 畸形 + $$..$$ 空块 + 结尾 .$$$$ ----
def fix_364(s):
    s = s.replace('=\\frac{e^3-7}{12}$.$$\n$$\n$$\n\\int_1^e', '=\\frac{e^3-7}{12}$。\n$$\n\\int_1^e')
    s = s.replace('=\\frac{e^4-2e^2-3}{16}\n$$\n$$\n故形心横坐标\n$$\n$$\n\\bar x', '=\\frac{e^4-2e^2-3}{16}\n$$\n故形心横坐标\n$$\n\\bar x')
    s = s.replace('\\frac{3(e^4-2e^2-3)}{4(e^3-7)}$$\n.$$$$', '\\frac{3(e^4-2e^2-3)}{4(e^3-7)}$$\n。')
    return s
FIX['core-364.answer'] = fix_364

# ---- core-383: $$..\end{cases}$$\lim.. 缺开块；中文裸 F(x)、x=\pi ----
def fix_383(s):
    s = s.replace('\\end{cases}$$\n\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,$$', '\\end{cases}$$\n$$\n\\lim_{x\\to\\pi^-}F(x)=\\lim_{x\\to\\pi^+}F(x)=2,$$')
    s = s.replace('故 F(x) 在 x=\\pi 处连续。', '故 $F(x)$ 在 $x=\\pi$ 处连续。')
    return s
FIX['core-383.answer'] = fix_383

# ---- core-489: $$..\Bigr).$$=-2\cos 缺开块 ----
def fix_489(s):
    old = '\\Bigr).$$=-2\\cos\\sqrt2+2\\sqrt2\\sin\\sqrt2+\\Bigl[2\\cos r\\Bigr]_0^{\\sqrt2}'
    new = '\\Bigr).$$\n$$\n=-2\\cos\\sqrt2+2\\sqrt2\\sin\\sqrt2+\\Bigl[2\\cos r\\Bigr]_0^{\\sqrt2}'
    s = s.replace(old, new)
    return s
FIX['core-489.answer'] = fix_489

# ============ 应用 & 写回 ============
if __name__ == '__main__':
    data = load()
    n_ok = 0
    n_miss = 0
    for k, fn in FIX.items():
        no, field = k.split('.')[0].split('-')[1], k.split('.')[1]
        q = find_q(data, no)
        if q is None or field not in q:
            print('MISS Q:', k)
            n_miss += 1
            continue
        old = q[field]
        new = fn(old)
        if new == old:
            print('NOOP :', k)
        q[field] = new
        n_ok += 1
    print('applied:', n_ok, 'miss:', n_miss)
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('written.')