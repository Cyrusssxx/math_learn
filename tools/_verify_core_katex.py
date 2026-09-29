# -*- coding: utf-8 -*-
"""校验 core_bank 指定题号（默认 25、29）答案/解析中的 LaTeX 公式可编译"""
import json, io, re, subprocess, os, tempfile, sys

NOS = [int(x) for x in (sys.argv[1:] or ['25', '29'])]

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

segs = []
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            if q.get('no') not in NOS:
                continue
            blob = ' '.join(str(q.get(k) or '') for k in ('stem', 'answer', 'idea'))
            for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', blob):
                t = (m.group(1) or m.group(2) or '').strip()
                if t:
                    segs.append(t)

print(f'待校验公式段数（题号 {NOS}）: {len(segs)}')

js = os.path.join(tempfile.gettempdir(), '_chk_core_katex.js')
inp = os.path.join(tempfile.gettempdir(), '_chk_core_segs.json')
with io.open(js, 'w', encoding='utf-8') as f:
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
  try { c.katex.renderToString(x, { throwOnError: true }); }
  catch (e) { fail++; if (bad.length < 8) bad.push({ s: x.slice(0, 70), e: e.message }); }
}
console.log('total=' + ls.length + ' fail=' + fail);
if (bad.length) console.log(JSON.stringify(bad, null, 1));
''')
with io.open(inp, 'w', encoding='utf-8') as f:
    json.dump(segs, f, ensure_ascii=False)

r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', js, inp],
                   capture_output=True, text=True)
print(r.stdout)
if r.stderr:
    print('stderr:', r.stderr)
for p in (js, inp):
    if os.path.exists(p):
        os.remove(p)
