# -*- coding: utf-8 -*-
# 手工修复第十批：块间缺开块补 \n$$（2009-2/8/9、2010-19、2011-16）
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = {
    ('2009数二真题', '2', 'answer'): [
        ('\\frac{a^{2}\\sin ax}{-6bx}$$=\\lim_{x\\to 0}\\frac{a^{2}\\sin ax}{-6b\\cdot ax}',
         '\\frac{a^{2}\\sin ax}{-6bx}$$\n$$=\\lim_{x\\to 0}\\frac{a^{2}\\sin ax}{-6b\\cdot ax}'),
    ],
    ('2009数二真题', '8', 'answer'): [
        ('$$Q=PE_{12}(1)$$Q^{T}AQ=',
         '$$Q=PE_{12}(1)$$\n$$Q^{T}AQ='),
        ('$$=E_{12}^{T}(1)$\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}E_{12}(1)$$',
         '$$=E_{12}^{T}(1)\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}E_{12}(1)$$'),
        ('\\end{pmatrix}$$$', '\\end{pmatrix}$$'),
    ],
    ('2009数二真题', '9', 'answer'): [
        ('\\left.\\frac{dx}{dt}\\right|_{t=1}=-1,$$\\frac{dy}{dt}=3t^{2}',
         '\\left.\\frac{dx}{dt}\\right|_{t=1}=-1,$$\n$$\\frac{dy}{dt}=3t^{2}'),
    ],
    ('2010数二真题', '19', 'answer'): [
        ('=\\frac{\\partial u}{\\partial\\xi}+\\frac{\\partial u}{\\partial\\eta},$$\\frac{\\partial u}{\\partial y}',
         '=\\frac{\\partial u}{\\partial\\xi}+\\frac{\\partial u}{\\partial\\eta},$$\n$$\\frac{\\partial u}{\\partial y}'),
        ('=a\\cdot\\frac{\\partial u}{\\partial\\xi}+b\\cdot\\frac{\\partial u}{\\partial\\eta},$$\\frac{\\partial^{2}u}{\\partial x^{2}}',
         '=a\\cdot\\frac{\\partial u}{\\partial\\xi}+b\\cdot\\frac{\\partial u}{\\partial\\eta},$$\n$$\\frac{\\partial^{2}u}{\\partial x^{2}}'),
    ],
    ('2011数二真题', '16', 'answer'): [
        ('\\frac{\\mathrm{d}y}{\\mathrm{d}t}=t^2-1,$$\\frac{\\mathrm{d}y}{\\mathrm{d}x}',
         '\\frac{\\mathrm{d}y}{\\mathrm{d}t}=t^2-1,$$\n$$\\frac{\\mathrm{d}y}{\\mathrm{d}x}'),
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
            continue
        q = next((x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no), None)
        if not q:
            continue
        v = q.get(f) or ''
        nv = v
        for old, new in reps:
            if old not in nv:
                failed.append('%s 第%s题.%s 未命中: %r' % (rid, no, f, old[:32]))
            else:
                nv = nv.replace(old, new, 1)
        if nv != v:
            fail, nseg = render_check(nv)
            if fail == 0:
                q[f] = nv
                applied += 1
                print('OK %s 第%s题.%s' % (rid, no, f))
            else:
                failed.append('%s 第%s题.%s 渲染失败 %d/%d' % (rid, no, f, fail, nseg))
    with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('应用 %d；未命中/失败 %d' % (applied, len(failed)))
    for x in failed[:6]:
        print('  W ' + x)


if __name__ == '__main__':
    main()
