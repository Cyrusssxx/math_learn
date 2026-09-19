# -*- coding: utf-8 -*-
"""手工修复第二批（core 侧）：块间缺开块、中文行内裸公式、空块$$$$、残缺块删除"""
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = {
    # (题号, 字段) -> [(old, new)]
    ('14', 'answer'): [
        # 方法二的 aligned 块残缺（缺 x} 后半），渲染必炸 → 整块删除，保留方法一
        ('\n方法二（洛必达法则）：\n$$\n\\begin{aligned} & \\lim_{x\\to0}\\frac{e^{x^{2}}-e^{2-2\\cos\\end{aligned}\n$$\n',
         '\n（方法二·洛必达法则的演算在此数据中残缺，已省略；方法一已给出完整求解）\n'),
    ],
    ('14', 'idea'): [
        ('\n方法二（洛必达法则）：\n$$\n\\begin{aligned} & \\lim_{x\\to0}\\frac{e^{x^{2}}-e^{2-2\\cos\\end{aligned}\n$$\n',
         '\n（方法二·洛必达法则的演算在此数据中残缺，已省略；方法一已给出完整求解）\n'),
    ],
    ('50', 'answer'): [
        ('A 中令 t=1/x，则 x\\to0^+ 时 t\\to+\\infty，(1+1/x)^x=(1+t)^{1/t}\\to1，故 A 正确。',
         'A 中令 $t=1/x$，则 $x\\to0^+$ 时 $t\\to+\\infty$，$(1+1/x)^x=(1+t)^{1/t}\\to1$，故 A 正确。'),
        ('C 的极限为 e^{-1}，不是 -e。D 的极限为 e^{-1}，不是 e。',
         'C 的极限为 $e^{-1}$，不是 $-e$。D 的极限为 $e^{-1}$，不是 $e$。'),
    ],
    ('50', 'idea'): [
        ('A 中令 t=1/x，则 x\\to0^+ 时 t\\to+\\infty，(1+1/x)^x=(1+t)^{1/t}\\to1，',
         'A 中令 $t=1/x$，则 $x\\to0^+$ 时 $t\\to+\\infty$，$(1+1/x)^x=(1+t)^{1/t}\\to1$，'),
        ('C 的极限为 e^{-1}，不是 -e。D 的极限为 e^{-1}，不是 e。',
         'C 的极限为 $e^{-1}$，不是 $-e$。D 的极限为 $e^{-1}$，不是 $e$。'),
    ],
    ('98', 'answer'): [
        ('\\text{阶为 }2);$$\\ln(1+\\sqrt[3]{x})',
         '\\text{阶为 }2);$$\n$$\\ln(1+\\sqrt[3]{x})'),
        ('\\text{阶为 }5/6);$$\\sqrt[3]{x+1}-1',
         '\\text{阶为 }5/6);$$\n$$\\sqrt[3]{x+1}-1'),
    ],
    ('100', 'answer'): [
        ('}{x^3}=0$$\\Rightarrow \\lim_{x\\to 0}\\frac{\\mathrm{e}^x(1+Bx+Cx^2)+\\mathrm{e}',
         '}{x^3}=0$$\n$$\\Rightarrow \\lim_{x\\to 0}\\frac{\\mathrm{e}^x(1+Bx+Cx^2)+\\mathrm{e}'),
    ],
    ('106', 'answer'): [
        ('o(x^3),$$f(x)=x+a\\left(x-\\frac{x^2}{2}+\\frac{x^3}{3}\\right)+b\\left(x^2-\\frac{x^4}{6}\\right)+o(x^3).$$',
         'o(x^3),$$\n$$f(x)=x+a\\left(x-\\frac{x^2}{2}+\\frac{x^3}{3}\\right)+b\\left(x^2-\\frac{x^4}{6}\\right)+o(x^3).$$'),
        ('f(x)\\sim kx^3，故', '$f(x)\\sim kx^3$，故'),
    ],
    ('146', 'answer'): [
        ('【答案】$$$$ 且', '【答案】且'),
        ('【答案】$$$$ 且', '【答案】且'),
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
            failed.append('core-%s 不存在' % no)
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
    print()
    print('应用 %d；未命中/失败 %d：' % (applied, len(failed)))
    for x in failed[:8]:
        print('  ⚠️ ' + x)


if __name__ == '__main__':
    main()
