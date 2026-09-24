# -*- coding: utf-8 -*-
# 修「高数2-一元微分」极值/拐点第三充分条件为 n 阶通用形式 + KaTeX 渲染验证
import json, io, re, subprocess, os, tempfile

P = 'pwa/data/notes.json'
d = json.load(io.open(P, encoding='utf-8'))
n2 = next(n for n in d if n.get('name') == '高数2-一元微分')
md = n2['md']

OLD1 = '''  - 条件三：$f'(x_0)=\\cdots=f^{(2n-1)}(x_0)=0,\\ f^{(2n)}(x_0)\\neq0$——$>0$ 极小，$<0$ 极大（例 $f=x^4$）'''
NEW1 = '''  - 条件三（n 阶判别）：$f'(x_0)=\\cdots=f^{(n-1)}(x_0)=0,\\ f^{(n)}(x_0)\\neq0$（$n\\ge2$）——$n$ 为偶数 ⟹ 极值（$f^{(n)}(x_0)>0$ 极小值，$f^{(n)}(x_0)<0$ 极大值）；$n$ 为奇数 ⟹ **不取得极值**（例 $f=x^4$ 取极小，$f=x^3$ 无极值）'''

OLD2 = '''  - 条件三：$f''(x_0)=\\cdots=f^{(2n)}(x_0)=0,\\ f^{(2n+1)}(x_0)\\neq0$ ⟹ 拐点（例 $f=x^5$）'''
NEW2 = '''  - 条件三（n 阶判别，与极值相反）：$f''(x_0)=\\cdots=f^{(n-1)}(x_0)=0,\\ f^{(n)}(x_0)\\neq0$（$n\\ge3$）——$n$ 为奇数 ⟹ 拐点（例 $f=x^3$，$n=3$）；$n$ 为偶数 ⟹ **不是拐点**（例 $f=x^4$，$n=4$ 时为极值点）'''

c1 = md.count(OLD1)
c2 = md.count(OLD2)
assert c1 == 1 and c2 == 1, '锚点不唯一: 极值=%d 拐点=%d' % (c1, c2)
md = md.replace(OLD1, NEW1).replace(OLD2, NEW2)
n2['md'] = md

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(d, fp, ensure_ascii=False, indent=2)

# KaTeX 渲染验证（新文本中的 $ 段）
segs = [m.group(1) or m.group(2) for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', md)]
jsf = os.path.join(tempfile.gettempdir(), '_kj.js')
inp = os.path.join(tempfile.gettempfile if False else tempfile.gettempdir(), '_sj.json')
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

# 复查替换结果
d3 = json.load(io.open(P, encoding='utf-8'))
md3 = next(n for n in d3 if n.get('name') == '高数2-一元微分')['md']
i = md3.find('极值充分')
print('=== 修改后（极值充分 + 拐点充分）===')
print(md3[i:i + 620])