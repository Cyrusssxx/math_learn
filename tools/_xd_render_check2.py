# -*- coding: utf-8 -*-
# 修正版：用 JSON 传段（避免多行 LaTeX 被换行切碎导致误报）
import json, io, re, subprocess, os, tempfile

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]

segs = []
for q in qs:
    for f in ('stem', 'answer', 'idea'):
        t = str(q.get(f) or '')
        for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', t):
            s = (m.group(1) or m.group(2)).strip()
            if s:
                segs.append(s)

jsf = os.path.join(tempfile.gettempdir(), '_k2.js')
inp = os.path.join(tempfile.gettempdir(), '_s2.json')
io.open(jsf, 'w', encoding='utf-8').write(
    'const fs=require("fs");const vm=require("vm");const c={};vm.createContext(c);'
    'vm.runInContext(fs.readFileSync("D:/ai code/math-note/pwa/vendor/katex/katex.min.js","utf8"),c);'
    'const ls=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));'
    'let b=0;const bad=[];'
    'for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++;if(bad.length<8)bad.push({seg:x.slice(0,90),err:e.message.slice(0,60)})}}'
    'console.log("total="+ls.length+" fail="+b);if(bad.length)console.log(JSON.stringify(bad,null,1));')
io.open(inp, 'w', encoding='utf-8').write(json.dumps(segs, ensure_ascii=False))
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp],
                   capture_output=True, text=True)
out = r.stdout
print(out[:1500] if out else r.stderr[:500])
for p in (jsf, inp):
    if os.path.exists(p):
        os.remove(p)