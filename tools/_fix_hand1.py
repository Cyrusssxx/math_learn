# -*- coding: utf-8 -*-
"""手工修复第一批（8 字段，精确字符串替换）：显示块之间缺开块/孤立$$/行内裸公式"""
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'

# (卷id或None, 题号, 字段) -> [(old, new), ...]（old 必须在原文中恰好出现）
FIX = [
    ('2000数二真题', '13', 'answer', [
        ('x^{m}$$', 'x^{m}$$'),
        ('\n.$$\n比较', '\n比较'),
        ('比较 x^{n} 的系数：f^{(n)}(0)/n! = \\dfrac{(-1)^{n-3}}{n-2}=\\dfrac{(-1)^{n-1}}{n-2}。',
         '比较 $x^{n}$ 的系数：$f^{(n)}(0)/n! = \\dfrac{(-1)^{n-3}}{n-2}=\\dfrac{(-1)^{n-1}}{n-2}$。'),
        ('故 $$\n$$f^{(n)}(0)=', '故\n$$f^{(n)}(0)='),
        ('\\geqslant 3$$\n.$$$$', '\\geqslant 3$$\n.'),
    ]),
    ('2000数二真题', '18', 'answer', [
        ('(a+1)^{5/2}}.$$V\'(a)=', '(a+1)^{5/2}}.$$\n$$V\'(a)='),
    ]),
    ('2000数二真题', '20', 'answer', [
        ('=2=B.$$\n.$$', '=2=B.$$'),
        ('\\end{pmatrix}$$\n.$$\n由 A^2=', '\\end{pmatrix}$$\n由 $A^2='),
        ('由 A^2=\\alpha(\\beta^{\\mathrm T}\\alpha)\\beta^{\\mathrm T}=2\\alpha\\beta^{\\mathrm T}=2A，故 A^4=8A；B^2=4,\\ B^4=16。',
         '由 $A^2=\\alpha(\\beta^{\\mathrm T}\\alpha)\\beta^{\\mathrm T}=2\\alpha\\beta^{\\mathrm T}=2A$，故 $A^4=8A$；$B^2=4,\\ B^4=16$。'),
        ('原方程化为 2\\cdot4\\cdot(2A)x=8Ax+16x+\\gamma，即\n$$\n$$16Ax=',
         '原方程化为 $2\\cdot4\\cdot(2A)x=8Ax+16x+\\gamma$，即\n$$16Ax='),
        ('令 x=(x_1,x_2,x_3)^{\\mathrm T}，代入得非齐次线性方程组\n$$\n$$\\begin{cases}',
         '令 $x=(x_1,x_2,x_3)^{\\mathrm T}$，代入得非齐次线性方程组\n$$\\begin{cases}'),
    ]),
    ('2000数二真题', '4', 'answer', [
        ('=2,$$b=\\lim_{x\\to\\infty}[(2x-1)\\mathrm{e}^{1/x}-2x]\n=$\\lim_{x\\to\\infty}[2x(\\mathrm{e}^{1/x}-1)-\\mathrm{e}^{1/x}]$\n=',
         '=2,$$\n$$b=\\lim_{x\\to\\infty}[(2x-1)\\mathrm{e}^{1/x}-2x]\n=\\lim_{x\\to\\infty}[2x(\\mathrm{e}^{1/x}-1)-\\mathrm{e}^{1/x}]\n='),
    ]),
    ('2001数二真题', '16', 'answer', [
        ('\\frac{(4x^2+1)^2}{64x}.$$A\'(x)=', '\\frac{(4x^2+1)^2}{64x}.$$\n$$A\'(x)='),
    ]),
    ('2001数二真题', '19', 'answer', [
        ('BXB=E$$(A-B)X(A-B)=E.$$', 'BXB=E$$\n$$(A-B)X(A-B)=E.$$'),
        ('计算 A-B=\\begin{pmatrix}1&-1&-1\\\\0&1&-1\\\\0&0&1\\end{pmatrix}，这是一个下三角矩阵，对角元全为 1，故可逆。',
         '计算 $$A-B=\\begin{pmatrix}1&-1&-1\\\\0&1&-1\\\\0&0&1\\end{pmatrix}$$，这是一个下三角矩阵，对角元全为 1，故可逆。'),
        ('于是 X=(A-B)^{-1}E(A-B)^{-1}=[(A-B)^{-1}]^{2}。',
         '于是 $X=(A-B)^{-1}E(A-B)^{-1}=[(A-B)^{-1}]^{2}$。'),
        ('求 (A-B)^{-1}：对 A-B 这种单位下三角阵，逆矩阵为\n$$\n$$(A-B)^{-1}=',
         '求 $(A-B)^{-1}$：对 $A-B$ 这种单位下三角阵，逆矩阵为\n$$(A-B)^{-1}='),
        ('\\end{pmatrix}$$\n.$$\n因此\n$$\n$$X=', '\\end{pmatrix}$$\n因此\n$$X='),
        ('\\end{pmatrix}$$\n.$$$$', '\\end{pmatrix}$$'),
    ]),
    ('2002数二真题', '5', 'answer', [
        ('\\bigr]$$=\\lambda(\\lambda^{2}-4\\lambda)-2\\cdot(-2\\lambda)+2\\cdot(-2\\lambda)=\\lambda^{3}-4\\lambda^{2}=\\lambda^{2}(\\lambda-4).$$',
         '\\bigr]$$\n$$=\\lambda(\\lambda^{2}-4\\lambda)-2\\cdot(-2\\lambda)+2\\cdot(-2\\lambda)=\\lambda^{3}-4\\lambda^{2}=\\lambda^{2}(\\lambda-4).$$'),
    ]),
    ('2003数二真题', '13', 'answer', [
        ('x-\\arcsin x$$=\\lim_{x\\to 0^{-}}\\frac{3ax^{2}}{1-\\frac{1}{\\sqrt{1-x^{2}}}}\\quad(\\frac{0}{0}\\text{ 型极限，用洛必达法则})$$',
         'x-\\arcsin x$$\n$$=\\lim_{x\\to 0^{-}}\\frac{3ax^{2}}{1-\\frac{1}{\\sqrt{1-x^{2}}}}\\quad(\\frac{0}{0}\\text{ 型极限，用洛必达法则})$$'),
        ('\\text{极限的四则运算})$$=\\lim_{x\\to 0^{-}}\\frac{3ax^{2}}{-\\frac{1}{2}x^{2}}\\quad((1-x^{2})^{\\frac{1}{2}}-1\\square\\dfrac{1}{2}(-x^{2})=-\\dfrac{1}{2}x^{2}\\;(x\\to 0))$$=-6a$$',
         '\\text{极限的四则运算})$$\n$$=\\lim_{x\\to 0^{-}}\\frac{3ax^{2}}{-\\frac{1}{2}x^{2}}\\quad((1-x^{2})^{\\frac{1}{2}}-1\\square\\dfrac{1}{2}(-x^{2})=-\\dfrac{1}{2}x^{2}\\;(x\\to 0))$$\n$$=-6a$$'),
    ]),
]


def render_check(text):
    segs = [m.group(1) or m.group(2) for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$', text)]
    if not segs:
        return 0, 0
    jsf = os.path.join(tempfile.gettempdir(), '_v.js')
    inp = os.path.join(tempfile.gettempdir(), '_v.txt')
    io.open(jsf, 'w', encoding='utf-8').write(
        "const fs=require('fs');const vm=require('vm');const c={};vm.createContext(c);"
        "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),c);"
        "const ls=fs.readFileSync(process.argv[2],'utf8').split(String.fromCharCode(10)).filter(Boolean);let b=0;"
        "for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++}}"
        "fs.writeFileSync(process.argv[3],JSON.stringify(b));")
    io.open(inp, 'w', encoding='utf-8').write('\n'.join(segs))
    oup = os.path.join(tempfile.gettempdir(), '_v.json')
    subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp, oup],
                   capture_output=True, text=True)
    b = int(json.loads(io.open(oup, encoding='utf-8').read()))
    for p in (jsf, inp, oup):
        if os.path.exists(p):
            os.remove(p)
    return b, len(segs)


def main():
    core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
    exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
    applied, failed = 0, []
    for rid, no, f, reps in FIX:
        vol = next((v for v in exam if v['id'] == rid), None)
        if not vol:
            failed.append('%s 卷不存在' % rid)
            continue
        q = next((x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no), None)
        if not q:
            failed.append('%s 第%s题不存在' % (rid, no))
            continue
        v = q.get(f) or ''
        nv = v
        for old, new in reps:
            if old not in nv:
                failed.append('%s 第%s题.%s 未命中: %r' % (rid, no, f, old[:40]))
            else:
                nv = nv.replace(old, new, 1)
        if nv != v:
            fail, nseg = render_check(nv)
            if fail == 0:
                q[f] = nv
                applied += 1
                print('✅ %s 第%s题.%s 修复（%d 处替换）' % (rid, no, f, len(reps)))
            else:
                failed.append('%s 第%s题.%s 渲染失败 %d/%d，未应用' % (rid, no, f, fail, nseg))
    with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print()
    print('应用 %d 个字段；失败/未命中 %d 条：' % (applied, len(failed)))
    for x in failed[:10]:
        print('  ⚠️ ' + x)


if __name__ == '__main__':
    main()
