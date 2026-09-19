# -*- coding: utf-8 -*-
"""KaTeX 抽检 2020 数二第15题（answer+idea）全部公式段"""
import json, io, re, subprocess, os

ex = json.load(io.open('D:/ai code/math-note/pwa/data/exam.json', encoding='utf-8'))
q15 = None
for vol in ex:
    if str(vol.get('year')) == '2020':
        for sec in vol.get('sections', []):
            for q in sec.get('questions', []):
                if q.get('no') == 15:
                    q15 = q

segs = []
for f in ('answer', 'idea'):
    v = q15.get(f) or ''
    for m in re.finditer(r'\$\$(.+?)\$\$', v, re.S):
        segs.append(m.group(1).replace('\n', ' '))
    for m in re.finditer(r'(?<!\$)\$([^$\n]+)\$(?!\$)', v):
        segs.append(m.group(1))
print('公式段数:', len(segs))

tmp = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_s.txt'
jsf = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_c.js'
io.open(tmp, 'w', encoding='utf-8').write('\n'.join(segs))
js = (
    "const fs=require('fs');\n"
    "const t=fs.readFileSync(process.argv[2],'utf8').split(String.fromCharCode(10)).filter(Boolean);\n"
    "const vm=require('vm');\n"
    "const c={};vm.createContext(c);\n"
    "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),c);\n"
    "let bad=0;\n"
    "for(const x of t){ try{ c.katex.renderToString(x,{throwOnError:true}); }catch(e){ bad++; console.log('  BAD:',x.slice(0,60),'->',e.message.slice(0,50)); } }\n"
    "console.log('KaTeX 渲染失败:',bad,'/',t.length);\n"
)
io.open(jsf, 'w', encoding='utf-8').write(js)
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, tmp],
                   capture_output=True, text=True)
print(r.stdout or r.stderr[:300])
os.remove(tmp)
os.remove(jsf)
