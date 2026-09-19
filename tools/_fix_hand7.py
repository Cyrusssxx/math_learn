# -*- coding: utf-8 -*-
# 补修：2007-11 尾部三$$、2007-23 两处同行 $$
import json, io, re, subprocess, os, tempfile

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))


def rc(t):
    segs = [m.group(1) or m.group(2) for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$', t)]
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


FIX = [
    ('2007数二真题', '11', 'answer', '= -\\frac{1}{6}$$$', '= -\\frac{1}{6}$$'),
    ('2007数二真题', '23', 'answer', '\\end{pmatrix} $$\\xrightarrow{1行\\times(-1)+4行}',
     '\\end{pmatrix} $$\n$$\\xrightarrow{1行\\times(-1)+4行}'),
    ('2007数二真题', '23', 'answer', '\\end{pmatrix} $$\\xrightarrow{换行}',
     '\\end{pmatrix} $$\n$$\\xrightarrow{换行}'),
]
for rid, no, f, old, new in FIX:
    vol = next(v for v in exam if v['id'] == rid)
    q = next(x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no)
    v = q.get(f) or ''
    if old not in v:
        print('W 未命中:', repr(old[:40]))
        continue
    nv = v.replace(old, new, 1)
    fail, nseg = rc(nv)
    if fail == 0:
        q[f] = nv
        print('OK %s 第%s题.%s' % (rid, no, f))
    else:
        print('W %s 第%s题.%s 渲染失败 %d/%d' % (rid, no, f, fail, nseg))

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
