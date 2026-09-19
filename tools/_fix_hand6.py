# -*- coding: utf-8 -*-
# 手工修复第六批（6 个字段）：块间补开块、畸形 $$$ 修正、\xrightarrow 去多余花括号
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = {
    ('2006数二真题', '7', 'answer'): [
        ('\\quad (\\text{再用一次拉氏定理})$$=f\'\'(\\eta)(\\xi-x_0)\\square x, \\quad \\text{其中 } x_0 < \\xi < x_0+\\square x, x_0 < \\eta < \\xi$$',
         '\\quad (\\text{再用一次拉氏定理})$$\n$$=f\'\'(\\eta)(\\xi-x_0)\\square x, \\quad \\text{其中 } x_0 < \\xi < x_0+\\square x, x_0 < \\eta < \\xi$$'),
        ('由于 f\'\'(x)>0，从而 \\square y-\\mathrm{d}y>0。又由于 \\mathrm{d}y=f\'(x_0)\\square x>0，故选[A]',
         '由于 $f\'\'(x)>0$，从而 $\\square y-\\mathrm{d}y>0$。又由于 $\\mathrm{d}y=f\'(x_0)\\square x>0$，故选 $[A]$'),
    ],
    ('2006数二真题', '22', 'answer'): [
        ('\\xrightarrow{[3pt]{[2]+[4](-4)}}', '\\xrightarrow[3pt]{[2]+[4](-4)}'),
    ],
    ('2007数二真题', '11', 'answer'): [
        ('**答案：** $-$\\dfrac{1}{6}$$', '**答案：** $-\\dfrac{1}{6}$'),
        ('$$$\\lim_{x \\to 0} \\frac{\\arctan x - \\sin x}{x^3}', '$$\\lim_{x \\to 0} \\frac{\\arctan x - \\sin x}{x^3}'),
        ('- \\frac{1}{6}$$$', '- \\frac{1}{6}$$'),
    ],
    ('2007数二真题', '16', 'answer'): [
        ('\\end{pmatrix}$$A^3=A^2\\cdot A=', '\\end{pmatrix}$$\n$$A^3=A^2\\cdot A='),
    ],
    ('2007数二真题', '23', 'answer'): [
        ('\\end{pmatrix}$$\nxrightarrow{1行\\times(-1)+4行}', '\\end{pmatrix}$$\n$$\nxrightarrow{1行\\times(-1)+4行}'),
        ('\\end{pmatrix}$$\nxrightarrow{换行}', '\\end{pmatrix}$$\n$$\nxrightarrow{换行}'),
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
                print('OK %s 第%s题.%s' % (rid, no, f))
            else:
                failed.append('%s 第%s题.%s 渲染失败 %d/%d' % (rid, no, f, fail, nseg))
    with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('应用 %d；未命中/失败 %d：' % (applied, len(failed)))
    for x in failed[:8]:
        print('  W ' + x)


if __name__ == '__main__':
    main()
