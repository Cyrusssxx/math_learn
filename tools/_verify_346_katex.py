# -*- coding: utf-8 -*-
import json, io, subprocess, os, tempfile, re

with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)

questions = [q for s in xd[0]['sections'] for q in s['questions']]
print(f"当前题库题目总数: {len(questions)}")

segs = []
for q in questions:
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

print(f"提取出 LaTeX 公式段数: {len(segs)}")

jsf = os.path.join(tempfile.gettempdir(), '_check_346_katex.js')
inp = os.path.join(tempfile.gettempdir(), '_check_346_segs.json')

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
        if (bad.length < 10) bad.push({ s: x.slice(0, 80), e: e.message });
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
