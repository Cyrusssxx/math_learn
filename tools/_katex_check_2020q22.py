# -*- coding: utf-8 -*-
"""KaTeX 渲染校验：exam.json 2020数二22题 answer 修复后 + 全库含 $$ 的 answer 抽样"""
import json, io, re, subprocess, os

EXAM = 'D:/ai code/math-note/pwa/data/exam.json'
ex = json.load(io.open(EXAM, encoding='utf-8'))

# 取 2020数二22 answer 的全部 $..$ 与 $$..$$ 段
target = None
for vol in ex:
    if str(vol.get('year')) == '2020':
        for sec in vol.get('sections', []):
            for q in sec.get('questions', []):
                if q.get('no') == 22:
                    target = q.get('answer') or ''
print('2020数二22 answer len:', len(target))

segments = []
# 显示块 $$..$$
for m in re.finditer(r'\$\$(.+?)\$\$', target, re.S):
    segments.append(('display', m.group(1)))
# 行内 $..$
for m in re.finditer(r'(?<!\$)\$([^$\n]+)\$(?!\$)', target):
    segments.append(('inline', m.group(1)))
print('公式段数: %d（display %d / inline %d）' % (
    len(segments), sum(1 for k, _ in segments if k == 'display'),
    sum(1 for k, _ in segments if k == 'inline')))

tmp = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_katex_seg.txt'
io.open(tmp, 'w', encoding='utf-8').write('\n'.join(t for _, t in segments))

NODE = 'C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
js = (
    "const fs=require('fs');\n"
    "const tests=fs.readFileSync(process.argv[2],'utf8').split('\\n').filter(Boolean);\n"
    "const vm=require('vm');\n"
    "const ctx={}; vm.createContext(ctx);\n"
    "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),ctx);\n"
    "const katex=ctx.katex;\n"
    "let bad=0;\n"
    "for(const t of tests){ try{ katex.renderToString(t,{throwOnError:true}); }catch(e){ bad++; "
    "console.log('  BAD:',t.slice(0,70).replace(/\\n/g,' '),'->',e.message.slice(0,50)); } }\n"
    "console.log('KaTeX 渲染失败:',bad,'/',tests.length);\n"
)
jsf = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_katex_check.js'
io.open(jsf, 'w', encoding='utf-8').write(js)
r = subprocess.run([NODE, jsf, tmp], capture_output=True, text=True)
print(r.stdout)
if r.stderr:
    print('stderr:', r.stderr[:300])
os.remove(tmp)
os.remove(jsf)
