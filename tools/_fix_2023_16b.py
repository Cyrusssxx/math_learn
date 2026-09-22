# -*- coding: utf-8 -*-
# 2023-16：三处「行尾 ：$ + 下行 \begin{...}」跨行 → $$ 独立显示块
import json, io, re, subprocess, os, tempfile

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2023数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '16')
lines = q['answer'].split('\n')

n = 0
for i in range(len(lines) - 1):
    if lines[i].rstrip().endswith('：$'):
        lines[i] = lines[i].rstrip()[:-1]
        nxt = lines[i + 1]
        if '\\begin' in nxt:
            lines[i + 1] = '$$\n' + nxt
            # 找该环境的闭合行，行尾 $ → $$
            j = i + 1
            while j < len(lines) and '\\end' not in lines[j]:
                j += 1
            if j < len(lines):
                r = lines[j].rstrip()
                if r.endswith('$') and not r.endswith('$$'):
                    lines[j] = r + '$'
            n += 1
q['answer'] = '\n'.join(lines)
print('修复处数:', n)

# 渲染验证
segs = [m.group(1) or m.group(2) for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$', q['answer'])]
jsf = os.path.join(tempfile.gettempdir(), '_v.js')
inp = os.path.join(tempfile.gettempdir(), '_v.txt')
io.open(jsf, 'w', encoding='utf-8').write(
    "const fs=require('fs');const vm=require('vm');const c={};vm.createContext(c);"
    "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),c);"
    "const ls=fs.readFileSync(process.argv[2],'utf8').split(String.fromCharCode(10)).filter(Boolean);let b=0;"
    "for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++;console.log('FAIL',x.slice(0,50))}}"
    "console.log('渲染失败',b,'/',ls.length);")
io.open(inp, 'w', encoding='utf-8').write('\n'.join(segs))
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp],
                   capture_output=True, text=True)
print(r.stdout or r.stderr[:200])
for p in (jsf, inp):
    if os.path.exists(p):
        os.remove(p)

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('已写盘')
