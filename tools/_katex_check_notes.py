# -*- coding: utf-8 -*-
"""提取多元微分笔记新公式段 → KaTeX 渲染校验"""
import json, io, re, subprocess, os

md = json.load(io.open('D:/ai code/math-note/pwa/data/notes.json', encoding='utf-8'))[7]['md']
s = md.find('高阶偏导数')
e = md.find('## 多元复合函数求偏导')
seg = md[s:e]
tests = [m.group(1) for m in re.finditer(r'\$([^$]+)\$', seg)]
tmp = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_katex_seg.txt'
io.open(tmp, 'w', encoding='utf-8').write('\n'.join(tests))
print('公式数:', len(tests))

NODE = 'C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
js = r"""
const fs=require('fs');
const tests=fs.readFileSync(process.argv[2],'utf8').split('\n').filter(Boolean);
const vm=require('vm');
const ctx={}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),ctx);
const katex=ctx.katex;
let bad=0;
for(const t of tests){ try{ katex.renderToString(t,{throwOnError:true}); }catch(e){ bad++; console.log('  BAD:',t.slice(0,80),'->',e.message.slice(0,60)); } }
console.log('KaTeX 渲染失败:',bad,'/',tests.length);
"""
jsf = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_katex_check.js'
io.open(jsf, 'w', encoding='utf-8').write(js)
r = subprocess.run([NODE, jsf, tmp], capture_output=True, text=True)
print(r.stdout)
if r.stderr:
    print('stderr:', r.stderr[:300])
os.remove(tmp)
os.remove(jsf)
