# -*- coding: utf-8 -*-
"""KaTeX 渲染校验 core_bank no=146/353 的 answer+idea 全部公式段"""
import json, io, re, subprocess, os

cb = json.load(io.open('D:/ai code/math-note/pwa/data/core_bank.json', encoding='utf-8'))
qs = [q for s in cb[0]['sections'] for q in s['questions']]
segments = []
for no in (146, 353):
    q = next(x for x in qs if x['no'] == no)
    for f in ('answer', 'idea'):
        v = q.get(f) or ''
        for m in re.finditer(r'\$\$(.+?)\$\$', v, re.S):
            segments.append((no, f, 'display', m.group(1)))
        for m in re.finditer(r'(?<!\$)\$([^$\n]+)\$(?!\$)', v):
            segments.append((no, f, 'inline', m.group(1)))
print('公式段数:', len(segments))

tmp = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_katex_seg.txt'
io.open(tmp, 'w', encoding='utf-8').write('\n'.join(t[3] for t in segments))
jsf = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_katex_check.js'
js = (
    "const fs=require('fs');\n"
    "const tests=fs.readFileSync(process.argv[2],'utf8').split('\\n').filter(Boolean);\n"
    "const vm=require('vm');\n"
    "const ctx={}; vm.createContext(ctx);\n"
    "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),ctx);\n"
    "const katex=ctx.katex;\n"
    "let bad=0;\n"
    "for(const t of tests){ try{ katex.renderToString(t,{throwOnError:true}); }catch(e){ bad++; "
    "console.log('  BAD:',t.slice(0,60).replace(/\\n/g,' '),'->',e.message.slice(0,50)); } }\n"
    "console.log('KaTeX 渲染失败:',bad,'/',tests.length);\n"
)
io.open(jsf, 'w', encoding='utf-8').write(js)
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, tmp],
                   capture_output=True, text=True)
print(r.stdout)
os.remove(tmp)
os.remove(jsf)
