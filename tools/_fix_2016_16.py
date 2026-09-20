# -*- coding: utf-8 -*-
# 精修 2016数二16.answer（内容完整，只修格式）：空块对清理 + 中文行内裸公式包 $
import json, io, re, subprocess, os, tempfile

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
q = next(x for v in exam if v['id'] == '2016数二真题' for s in v['sections'] for x in s['questions'] if str(x['no']) == '16')

lines = q['answer'].split('\n')
# 1) 删除孤立/空块对：L10、L11（f(x) 块前两个空 $$）、L15（L14 闭后孤立）、L18
def is_dd(L):
    return L.strip() == '$$'
remove = {10, 11, 15, 18}
lines = [L for i, L in enumerate(lines) if i not in remove]
out = []
for L in lines:
    s = L
    # 2) 中文行内裸公式包 $
    s = s.replace('故 f(x)=$\\dfrac43x^3-x^2+\\dfrac13$。当 x\\ge1 时，',
                  '故 $f(x)=\\dfrac43x^3-x^2+\\dfrac13$。当 $x\\ge1$ 时，')
    s = s.replace('分段求导：f\'(x)=\\begin{cases}4x^2-2x,&0<x<1\\\\2x,&x\\ge1\\end{cases}，且 f\'_-(1)=2=f\'_+(1)，f\'(x) 在 x=1 连续。',
                  '分段求导：$f\'(x)=\\begin{cases}4x^2-2x,&0<x<1\\\\2x,&x\\ge1\\end{cases}$，且 $f\'_-(1)=2=f\'_+(1)$，$f\'(x)$ 在 $x=1$ 连续。')
    s = s.replace('令 f\'(x)=0 得 x=\\dfrac12。当 0<x<\\dfrac12 时 2x(2x-1)<0，当 x>\\dfrac12 时 f\'(x)>0，故最小值在 x=\\dfrac12 处取得：',
                  '令 $f\'(x)=0$ 得 $x=\\dfrac12$。当 $0<x<\\dfrac12$ 时 $2x(2x-1)<0$，当 $x>\\dfrac12$ 时 $f\'(x)>0$，故最小值在 $x=\\dfrac12$ 处取得：')
    out.append(s)
nv = '\n'.join(out)


def rc(t):
    segs = [m.group(1) or m.group(2) for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$', t)]
    jsf = os.path.join(tempfile.gettempdir(), '_v.js')
    inp = os.path.join(tempfile.gettempdir(), '_v.txt')
    io.open(jsf, 'w', encoding='utf-8').write(
        "const fs=require('fs');const vm=require('vm');const c={};vm.createContext(c);"
        "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),c);"
        "const ls=fs.readFileSync(process.argv[2],'utf8').split(String.fromCharCode(10)).filter(Boolean);let b=0;"
        "for(const x of ls){try{c.katex.renderToString(x,{throwOnError:true})}catch(e){b++}}"
        "fs.writeFileSync(process.argv[3],JSON.stringify(b));")
    io.open(inp, 'w', encoding='utf-8').write('\n'.join(segs))
    oup = os.path.join(tempfile.gettempdir(), '_v.json')
    subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp, oup],
                   capture_output=True, text=True)
    b = int(json.loads(io.open(oup, encoding='utf-8').read()))
    for p in (jsf, inp, oup):
        if os.path.exists(p):
            os.remove(p)
    return b, len(segs)


fail, nseg = rc(nv)
print('渲染自检: 失败 %d/%d' % (fail, nseg))
if fail == 0:
    q['answer'] = nv
    with io.open(P, 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('OK 2016-16 已修复')
else:
    print('渲染失败，未写盘')