# -*- coding: utf-8 -*-
# 验证：新导入 109 道的 KaTeX 渲染
import json, io, re, subprocess, os, tempfile

xd = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
secs = xd[0]['sections']
newsec = next(s for s in secs if '1987-1999' in s['title'])
print('新 section 题数:', len(newsec['questions']))

segs = []
for q in newsec['questions']:
    for f in ('stem', 'answer', 'idea'):
        for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$', str(q.get(f) or '')):
            s = (m.group(1) or m.group(2)).strip()
            if s:
                segs.append(s)
print('LaTeX 段数:', len(segs))

jsf = os.path.join(tempfile.gettempdir(), '_k3.js')
inp = os.path.join(tempfile.gettempdir(), '_s3.json')
io.open(jsf, 'w', encoding='utf-8').write(
    'const fs=require("fs");const vm=require("vm");const c={};vm.createContext(c);'
    'vm.runInContext(fs.readFileSync("D:/ai code/math-note/pwa/vendor/katex/katex.min.js","utf8"),c);'
    'const ls=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));'
    'let b=0;const bad=[];'
    'for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++;if(bad.length<6)bad.push({s:x.slice(0,70),e:e.message.slice(0,50)})}}'
    'console.log("total="+ls.length+" fail="+b);if(bad.length)console.log(JSON.stringify(bad,null,1));')
io.open(inp, 'w', encoding='utf-8').write(json.dumps(segs, ensure_ascii=False))
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp],
                   capture_output=True, text=True)
print(r.stdout[:800] if r.stdout else r.stderr[:400])
for p in (jsf, inp):
    if os.path.exists(p):
        os.remove(p)

# answer 质量抽查（是否有纯字母答案）
only = [q['no'] for q in newsec['questions']
        if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', str(q.get('answer') or '').strip())
        and re.search(r'[A-Da-d]', str(q.get('answer') or ''))]
print('答案为纯字母的:', len(only), only[:8])
print()
print('样本 3 道:')
for q in newsec['questions'][:3]:
    print('  no=%s src=%s cat=%s' % (q['no'], q['source'], q['categoryIds']))
    print('    stem:', q['stem'][:80].replace('\n', ' '))
    print('    answer:', str(q['answer'])[:70].replace('\n', ' '))
    print('    idea:', str(q['idea'])[:90].replace('\n', ' '))