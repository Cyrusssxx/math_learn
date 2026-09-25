# -*- coding: utf-8 -*-
import json, io, subprocess, os, tempfile

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

# 抓取 2022 和 2024 的全部文本段落进行 KaTeX 渲染验证
p_list = [p for p in exam_data if p['id'] in ('2022数二真题', '2024数二真题')]

segs = []
import re
for p in p_list:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            for fld in ['stem', 'answer', 'idea']:
                txt = q.get(fld, '')
                for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', txt):
                    formula = m.group(1) or m.group(2)
                    if formula.strip():
                        segs.append(formula.strip())
            for opt in q.get('options', []):
                for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', opt):
                    formula = m.group(1) or m.group(2)
                    if formula.strip():
                        segs.append(formula.strip())

print(f"2022 & 2024 公式总段数: {len(segs)}")

jsf = os.path.join(tempfile.gettempdir(), '_check_22_24_katex.js')
inp = os.path.join(tempfile.gettempdir(), '_check_22_24_segs.json')

with io.open(jsf, 'w', encoding='utf-8') as f:
    f.write('''
const fs = require('fs');
const vm = require('vm');
const c = {};
vm.createContext(c);
vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js', 'utf8'), c);
const ls = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let fail = 0;
const bad = [];
for (const x of ls) {
    try {
        c.katex.renderToString(x, { throwOnError: true });
    } catch (e) {
        fail++;
        if (bad.length < 5) bad.push({ s: x.slice(0, 80), e: e.message });
    }
}
console.log(`total=${ls.length} fail=${fail}`);
if (bad.length) console.log(JSON.stringify(bad, null, 2));
''')

with io.open(inp, 'w', encoding='utf-8') as f:
    json.dump(segs, f, ensure_ascii=False)

res = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("stderr:", res.stderr)

for p in (jsf, inp):
    if os.path.exists(p):
        os.remove(p)
