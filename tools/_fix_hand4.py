# -*- coding: utf-8 -*-
"""删除 core-14 方法二残缺块（answer/idea），渲染验证后写回"""
import json, io, re, subprocess, os, tempfile

P = 'D:/ai code/math-note/pwa/data/core_bank.json'
core = json.load(io.open(P, encoding='utf-8'))
core_q = {str(q['no']): q for s in core[0]['sections'] for q in s['questions']}

OLD = '\n 方法二（洛必达法则）：\n$$\n\\begin{aligned} & \\lim_{x\\to0}\\frac{e^{x^{2}}-e^{2-2\\cos\\end{aligned}'
NEW = '\n（方法二·洛必达法则的演算数据残缺，已省略；方法一已给出完整求解）'


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


for f in ('answer', 'idea'):
    v = core_q['14'].get(f) or ''
    if OLD not in v:
        print('⚠️ core-14.%s 未命中；现 repr 前 60:', repr(v[:60]))
        continue
    nv = v.replace(OLD, NEW, 1)
    fail, nseg = render_check(nv)
    if fail == 0:
        core_q['14'][f] = nv
        print('✅ core-14.%s 已修复' % f)
    else:
        print('⚠️ core-14.%s 渲染失败 %d/%d' % (f, fail, nseg))

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(core, fp, ensure_ascii=False, separators=(',', ':'))
