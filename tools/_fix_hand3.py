# -*- coding: utf-8 -*-
"""手工修复第三批：core-14 方法二残缺块删除、core-106 补开块"""
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = {
    ('14', 'answer'): [
        ('\n$$\n 方法二（洛必达法则）：\n$$\n\\begin{aligned} & \\lim_{x\\to0}\\frac{e^{x^{2}}-e^{2-2\\cos\\end{aligned}\n$$\n',
         '\n（方法二·洛必达法则的演算数据残缺，已省略；方法一已给出完整求解）\n'),
    ],
    ('14', 'idea'): [
        ('\n$$\n 方法二（洛必达法则）：\n$$\n\\begin{aligned} & \\lim_{x\\to0}\\frac{e^{x^{2}}-e^{2-2\\cos\\end{aligned}\n$$\n',
         '\n（方法二·洛必达法则的演算数据残缺，已省略；方法一已给出完整求解）\n'),
    ],
    ('106', 'answer'): [
        (',$$f(x)=x+a\\left(x-\\frac{x^2}{2}+\\frac{x^3}{3}\\right)',
         ',$$\n$$f(x)=x+a\\left(x-\\frac{x^2}{2}+\\frac{x^3}{3}\\right)'),
        ('f(x)\\sim kx^3，故', '$f(x)\\sim kx^3$，故'),
    ],
}


def render_check(text):
    segs = [m.group(1) or m.group(2) for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$', text)]
    if not segs:
        return 0, 0
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


def main():
    core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
    core_q = {str(q['no']): q for s in core[0]['sections'] for q in s['questions']}
    applied, failed = 0, []
    for (no, f), reps in FIX.items():
        q = core_q.get(no)
        if not q:
            continue
        v = q.get(f) or ''
        nv = v
        for old, new in reps:
            if old not in nv:
                failed.append('core-%s.%s 未命中: %r' % (no, f, old[:40]))
            else:
                nv = nv.replace(old, new, 1)
        if nv != v:
            fail, nseg = render_check(nv)
            if fail == 0:
                q[f] = nv
                applied += 1
                print('✅ core-%s.%s' % (no, f))
            else:
                failed.append('core-%s.%s 渲染失败 %d/%d' % (no, f, fail, nseg))
    with io.open(BASE + 'core_bank.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(core, fp, ensure_ascii=False, separators=(',', ':'))
    print('应用 %d；失败 %d：%s' % (applied, len(failed), '；'.join(failed[:6])))


if __name__ == '__main__':
    main()
