# -*- coding: utf-8 -*-
# 全库 KaTeX 渲染验证：xd_bank 所有 stem/answer/idea 的 $ 段
import json, io, re, subprocess, os, tempfile

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]
print('总题数:', len(qs))

segs = []
for q in qs:
    for f in ('stem', 'answer', 'idea'):
        t = str(q.get(f) or '')
        for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', t):
            segs.append(m.group(1) or m.group(2))
print('LaTeX 段数:', len(segs))

jsf = os.path.join(tempfile.gettempdir(), '_k.js')
inp = os.path.join(tempfile.gettempdir(), '_s.txt')
io.open(jsf, 'w', encoding='utf-8').write(
    'const fs=require("fs");const vm=require("vm");const c={};vm.createContext(c);'
    'vm.runInContext(fs.readFileSync("D:/ai code/math-note/pwa/vendor/katex/katex.min.js","utf8"),c);'
    'const ls=fs.readFileSync(process.argv[2],"utf8").split(String.fromCharCode(10)).filter(Boolean);'
    'let b=0;const bad=[];'
    'for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++;if(bad.length<6)bad.push(x.slice(0,70))}}'
    'console.log("段数="+ls.length+" 失败="+b);if(bad.length)console.log("失败段: "+bad.join(" || "));')
io.open(inp, 'w', encoding='utf-8').write('\n'.join(segs))
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp],
                   capture_output=True, text=True)
print(r.stdout or r.stderr[:400])
for p in (jsf, inp):
    if os.path.exists(p):
        os.remove(p)