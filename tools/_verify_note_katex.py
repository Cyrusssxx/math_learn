# -*- coding: utf-8 -*-
# 单独验证「高数2-一元微分」修改后 md 的 KaTeX 渲染
import json, io, re, subprocess, os, tempfile

d = json.load(io.open('pwa/data/notes.json', encoding='utf-8'))
md = next(n for n in d if n.get('name') == '高数2-一元微分')['md']
segs = [m.group(1) or m.group(2) for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', md)]
jsf = os.path.join(tempfile.gettempdir(), '_kj.js')
inp = os.path.join(tempfile.gettempdir(), '_sj.json')
io.open(jsf, 'w', encoding='utf-8').write(
    'const fs=require("fs");const vm=require("vm");const c={};vm.createContext(c);'
    'vm.runInContext(fs.readFileSync("D:/ai code/math-note/pwa/vendor/katex/katex.min.js","utf8"),c);'
    'const ls=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));'
    'let b=0;const bad=[];'
    'for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++;if(bad.length<6)bad.push({s:x.slice(0,60),e:e.message.slice(0,40)})}}'
    'console.log("total="+ls.length+" fail="+b);if(bad.length)console.log(JSON.stringify(bad));')
io.open(inp, 'w', encoding='utf-8').write(json.dumps(segs, ensure_ascii=False))
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp],
                   capture_output=True, text=True)
print(r.stdout or r.stderr[:400])
for p in (jsf, inp):
    if os.path.exists(p):
        os.remove(p)