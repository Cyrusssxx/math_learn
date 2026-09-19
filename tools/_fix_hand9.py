# -*- coding: utf-8 -*-
# 补修：2007-23（查实际$$位置后拆）、2009-2（短锚点）
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


def getq(rid, no):
    vol = next(v for v in exam if v['id'] == rid)
    return next(x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no)


# 2009-2：短锚点
q = getq('2009数二真题', '2')
v = q['answer']
old = '{a^{2}\\sin ax}{-6bx}$$=\\lim_{x\\to 0}\\frac{a^{2}\\sin ax}'
if old in v:
    nv = v.replace(old, '{a^{2}\\sin ax}{-6bx}$$\n$$=\\lim_{x\\to 0}\\frac{a^{2}\\sin ax}', 1)
    fail, nseg = rc(nv)
    if fail == 0:
        q['answer'] = nv
        print('OK 2009-2')
    else:
        print('W 2009-2 渲染失败 %d/%d' % (fail, nseg))
else:
    print('W 2009-2 未命中')

# 2007-23：打印所有 $$ 位置上下文，手工补
q = getq('2007数二真题', '23')
v = q['answer']
print('2007-23 的 $$ 上下文（前 6 处）：')
n = 0
for m in re.finditer(r'\$\$', v):
    s = max(0, m.start() - 14)
    print('   ...%r...' % v[s:m.start() + 20])
    n += 1
    if n >= 6:
        break
