# -*- coding: utf-8 -*-
# 补修 2007-23 两处（$$ 同行接 \xrightarrow → 拆新块）
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


vol = next(v for v in exam if v['id'] == '2007数二真题')
q = next(x for s in vol['sections'] for x in s['questions'] if str(x['no']) == '23')
v = q['answer']
reps = [
    ('\\end{pmatrix}$$\nxrightarrow{1行\\times(-1)+4行}',
     '\\end{pmatrix}$$\n$$\nxrightarrow{1行\\times(-1)+4行}'),
    ('\\end{pmatrix}$$\nxrightarrow{换行}',
     '\\end{pmatrix}$$\n$$\nxrightarrow{换行}'),
]
nv = v
hit = []
for old, new in reps:
    if old in nv:
        nv = nv.replace(old, new, 1)
        hit.append(old[:20])
    else:
        print('W 未命中:', repr(old[:30]))
if nv != v:
    fail, nseg = rc(nv)
    if fail == 0:
        q['answer'] = nv
        print('OK 2007-23（命中 %d 处）' % len(hit))
    else:
        print('W 2007-23 渲染失败 %d/%d' % (fail, nseg))

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
