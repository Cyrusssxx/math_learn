# -*- coding: utf-8 -*-
# 手工修复第十一批：块间缺开块（2009-8、2012-23、2013-16/17）
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = {
    ('2009数二真题', '8', 'answer'): [
        ("APE_{12}(1)]$$=E_{12}^{T}(1)\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}E_{12}(1)$$",
         "APE_{12}(1)]$$\n$$=E_{12}^{T}(1)\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}E_{12}(1)$$"),
        ("E_{12}(1)$$=\\begin{pmatrix}1&1&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}",
         "E_{12}(1)$$\n$$=\\begin{pmatrix}1&1&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&2\\end{pmatrix}"),
    ],
    ('2012数二真题', '23', 'answer'): [
        ('=\\begin{pmatrix}2&0&2\\\\0&2&2\\\\2&2&4\\end{pmatrix}.$$|\\lambda I-B|=',
         '=\\begin{pmatrix}2&0&2\\\\0&2&2\\\\2&2&4\\end{pmatrix}.$$\n$$|\\lambda I-B|='),
        ('= (\\lambda-2)\\big[(\\lambda-2)(\\lambda-4)-4\\big]-2\\cdot2(\\lambda-2)=\\lambda(\\lambda-2)(\\lambda-6),$$',
         '= (\\lambda-2)\\big[(\\lambda-2)(\\lambda-4)-4\\big]-2\\cdot2(\\lambda-2)=\\lambda(\\lambda-2)(\\lambda-6),$$'),
    ],
    ('2013数二真题', '16', 'answer'): [
        ('\\frac{3\\pi}{5}a^{\\frac53},$$V_y=2\\pi\\int_0^a',
         '\\frac{3\\pi}{5}a^{\\frac53},$$\n$$V_y=2\\pi\\int_0^a'),
    ],
    ('2013数二真题', '17', 'answer'): [
        ('\\frac{8}{3}\\cdot\\frac{2^4}{4}=\\frac{32}{3}$$\n,$$\\int_2^6',
         '\\frac{8}{3}\\cdot\\frac{2^4}{4}=\\frac{32}{3}$$\n,$$\n$$\\int_2^6'),
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
