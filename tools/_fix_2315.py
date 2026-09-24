# -*- coding: utf-8 -*-
# 修正 2023数二真题-15：所求积分区间 0~3 → 1~3（参考库 serial=4891 原题为 [1,3]，答案 1/2）
import json, io, re, subprocess, os, tempfile

P = 'pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
v = next(v for v in exam if v['id'] == '2023数二真题')
q = next(q for s in v['sections'] for q in s['questions'] if str(q['no']) == '15')

old_stem = q['stem']
new_stem = old_stem.replace('$\\int_0^3 f(x)\\,dx=$', '$\\int_1^3 f(x)\\,dx=$')
assert new_stem != old_stem, '题干锚点未命中'
q['stem'] = new_stem

q['answer'] = (
    '【答案】$\\dfrac12$\n'
    '$$\\int_1^3f(x)\\,dx=\\int_1^2f(x)\\,dx+\\int_2^3f(x)\\,dx.$$\n'
    '第二项令 $u=x-2$，由 $f(u+2)=f(u)+u$ 得\n'
    '$$\\int_2^3f(x)\\,dx=\\int_0^1\\bigl[f(u)+u\\bigr]\\,du=\\int_0^1f(u)\\,du+\\frac12.$$\n'
    '因此\n'
    '$$\\int_1^3f(x)\\,dx=\\left(\\int_1^2f(x)\\,dx+\\int_0^1f(x)\\,dx\\right)+\\frac12=\\int_0^2f(x)\\,dx+\\frac12=0+\\frac12=\\frac12.$$'
)

q['idea'] = (
    '**思路**：\n'
    '① 拆区间：$\\int_1^3f=\\int_1^2f+\\int_2^3f$。\n'
    '② 对 $\\int_2^3f$ 换元 $u=x-2$，由 $f(u+2)=f(u)+u$ 得 $\\int_0^1f(u)\\,du+\\tfrac12$。\n'
    '③ 与 $\\int_1^2f$ 合并正是题给的 $\\int_0^2f=0$，故结果为 $\\tfrac12$。\n'
    '⚠️ 若问 $\\int_0^3f$，条件不足（$\\int_0^3f=\\tfrac12+\\int_0^1f$，随 $\\int_0^1f$ 变化）；'
    '原题所求区间为 $[1,3]$（2023 真题）。'
)

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))

# KaTeX 验证（本题三字段）
segs = []
for f in ('stem', 'answer', 'idea'):
    for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', str(q.get(f) or '')):
        segs.append((m.group(1) or m.group(2)).strip())
jsf = os.path.join(tempfile.gettempdir(), '_kq.js')
inp = os.path.join(tempfile.gettempdir(), '_sq.json')
io.open(jsf, 'w', encoding='utf-8').write(
    'const fs=require("fs");const vm=require("vm");const c={};vm.createContext(c);'
    'vm.runInContext(fs.readFileSync("D:/ai code/math-note/pwa/vendor/katex/katex.min.js","utf8"),c);'
    'const ls=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));'
    'let b=0;const bad=[];'
    'for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++;if(bad.length<5)bad.push({s:x.slice(0,60),e:e.message.slice(0,40)})}}'
    'console.log("total="+ls.length+" fail="+b);if(bad.length)console.log(JSON.stringify(bad));')
io.open(inp, 'w', encoding='utf-8').write(json.dumps(segs, ensure_ascii=False))
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp],
                   capture_output=True, text=True)
print(r.stdout or r.stderr[:300])
for p in (jsf, inp):
    if os.path.exists(p):
        os.remove(p)

print('新题干:', q['stem'])