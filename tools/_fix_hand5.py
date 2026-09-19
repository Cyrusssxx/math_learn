# -*- coding: utf-8 -*-
# 手工修复第五批（8 个 exam 字段）：块间补开块 + 自定义命令替换 + 行内裸公式包 $
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = {
    ('2003数二真题', '8', 'answer'): [
        ('\\text{（凑重要极限形式）}$$=(1+e^{-1})^{\\frac{3}{2}}-1\\quad\\text{（重要极限）}$$',
         '\\text{（凑重要极限形式）}$$\n$$=(1+e^{-1})^{\\frac{3}{2}}-1\\quad\\text{（重要极限）}$$'),
        ('所以选项(B)正确。$$', '所以选项(B)正确。'),
    ],
    ('2004数二真题', '15', 'answer'): [
        # \xlongequal KaTeX 不支持 → \overset
        ('\\xlongequal{e^{\\Box}-1\\sim\\Box}', '\\overset{e^{\\Box}-1\\sim\\Box}{=}'),
        ('\\xlongequal{\\text{洛}}', '\\overset{\\text{洛}}{=}'),
        (',(x^{2})\'$$=\\lim_{x\\to 0}\\frac{1}{2+\\cos x}\\cdot(-\\sin x)=-\\frac{1}{2}\\lim_{x\\to 0}\\frac{1}{2+\\cos x}\\cdot\\frac{\\sin x}{x}=-\\frac{1}{2}\\cdot\\frac{1}{3}\\cdot 1=-\\frac{1}{6}$$',
         ',(x^{2})\'$$\n$$=\\lim_{x\\to 0}\\frac{1}{2+\\cos x}\\cdot(-\\sin x)=-\\frac{1}{2}\\lim_{x\\to 0}\\frac{1}{2+\\cos x}\\cdot\\frac{\\sin x}{x}=-\\frac{1}{2}\\cdot\\frac{1}{3}\\cdot 1=-\\frac{1}{6}$$'),
    ],
    ('2004数二真题', '16', 'answer'): [
        ('=-4$$f\'_{+}(0)=\\lim_{x\\to 0^{+}}\\frac{f(x)-f(0)}{x-0}=\\lim_{x\\to 0^{+}}\\frac{kx(x+2)(x+4)-0}{x}=8k.$$',
         '=-4$$\n$$f\'_{+}(0)=\\lim_{x\\to 0^{+}}\\frac{f(x)-f(0)}{x-0}=\\lim_{x\\to 0^{+}}\\frac{kx(x+2)(x+4)-0}{x}=8k.$$'),
    ],
    ('2004数二真题', '22', 'answer'): [
        ('$\\eta_{1}=(-1,1,0,\\cdots,0)^{T},\\;\\eta_{', '$\\eta_{1}=(-1,1,0,\\cdots,0)^{T}$，$\\eta_{'),
    ],
    ('2004数二真题', '23', 'answer'): [
        ('\\end{vmatrix}$$\nxrightarrow', '\\end{vmatrix}$$\n$$\nxrightarrow'),
    ],
    ('2005数二真题', '15', 'answer'): [
        ('}\\stackrel{\\text{整理}}{=}', '\\overset{\\text{整理}}{=}'),
        ('}\\stackrel{\\text{上下同除 }x}{=}', '\\overset{\\text{上下同除 }x}{=}'),
    ],
    ('2005数二真题', '16', 'answer'): [
        ('\\frac{1}{2}(e^{x}-x-1),$$S_{2}(y)=\\int_{1}^{y}(\\ln t-\\varphi(t))dt,$$',
         '\\frac{1}{2}(e^{x}-x-1),$$\n$$S_{2}(y)=\\int_{1}^{y}(\\ln t-\\varphi(t))dt,$$'),
        ('由 S_{1}(x)=S_{2}(y)，得', '由 $S_{1}(x)=S_{2}(y)$，得'),
    ],
    ('2005数二真题', '2', 'answer'): [
        ('=1,$$b=\\lim_{x\\to+\\infty}[f(x)-ax]=\\lim_{x\\to+\\infty}\\left[\\frac{(1+x)^{\\frac{3}{2}}-x^{\\frac{3}{2}}}{\\sqrt{x}}\\right]=\\frac{3}{2},$$',
         '=1,$$\n$$b=\\lim_{x\\to+\\infty}[f(x)-ax]=\\lim_{x\\to+\\infty}\\left[\\frac{(1+x)^{\\frac{3}{2}}-x^{\\frac{3}{2}}}{\\sqrt{x}}\\right]=\\frac{3}{2},$$'),
    ],
}


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
    exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
    applied, failed = 0, []
    for (rid, no, f), reps in FIX.items():
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
                failed.append('%s 第%s题.%s 未命中: %r' % (rid, no, f, old[:36]))
            else:
                nv = nv.replace(old, new, 1)
        if nv != v:
            fail, nseg = render_check(nv)
            if fail == 0:
                q[f] = nv
                applied += 1
                print('✅ %s 第%s题.%s' % (rid, no, f))
            else:
                failed.append('%s 第%s题.%s 渲染失败 %d/%d' % (rid, no, f, fail, nseg))
    with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print()
    print('应用 %d；未命中/失败 %d：' % (applied, len(failed)))
    for x in failed[:8]:
        print('  ⚠️ ' + x)


if __name__ == '__main__':
    main()
