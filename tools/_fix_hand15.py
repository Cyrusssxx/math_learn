# -*- coding: utf-8 -*-
# 手工修复第十二批：行内裸公式包 $、孤立 .$$ 删除、空块对清理
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
FIX = {
    ('2012数二真题', '23', 'answer'): [
        ('故 B 的特征值为 \\lambda_1=0,\\lambda_2=2,\\lambda_3=6。',
         '故 $B$ 的特征值为 $\\lambda_1=0,\\lambda_2=2,\\lambda_3=6$。'),
    ],
    ('2013数二真题', '17', 'answer'): [
        ('\\frac{32}{3}$$\n,$$\\int_2^6', '\\frac{32}{3}$$\n$$\n,\n$$\\int_2^6'),
    ],
    ('2013数二真题', '21', 'answer'): [
        ('=\\frac{e^2+1}{4}$$\n.$$', '=\\frac{e^2+1}{4}$$'),
        ('（Ⅱ）面积 S=\\displaystyle\\int_1^e\\left(\\frac14x^2-\\frac12\\ln x\\right)dx=\\left[\\frac{x^3}{12}-\\frac12(x\\ln x-x)\\right]_1^e=\\frac{e^3}{12}-\\frac{1}{12}-\\frac12=\\frac{e^3-7}{12}.\n$$',
         '（Ⅱ）面积\n$$S=\\displaystyle\\int_1^e\\left(\\frac14x^2-\\frac12\\ln x\\right)dx=\\left[\\frac{x^3}{12}-\\frac12(x\\ln x-x)\\right]_1^e=\\frac{e^3}{12}-\\frac{1}{12}-\\frac12=\\frac{e^3-7}{12}.$$'),
        ('=\\frac{e^4-1}{16}-\\frac12\\left(\\frac{e^2}{2}-\\frac{e^2}{4}+\\frac14', '=\\frac{e^4-1}{16}-\\frac12\\left(\\frac{e^2}{2}-\\frac{e^2}{4}+\\frac14'),
    ],
    ('2013数二真题', '22', 'answer'): [
        ('=\\begin{pmatrix}0&1\\\\1&b\\end{pmatrix}$$\n.$$', '=\\begin{pmatrix}0&1\\\\1&b\\end{pmatrix}$$'),
        ('（也可先取迹：\\operatorname{tr}(AC-CA)=0，故必有 \\operatorname{tr}(B)=b=0。）',
         '（也可先取迹：$\\operatorname{tr}(AC-CA)=0$，故必有 $\\operatorname{tr}(B)=b=0$。）'),
        ('由第 1 式 x_2=a x_3，代入第 4 式得 b=x_2-a x_3=0；由第 3 式 x_1=x_3+x_4+1，代入第 2 式：',
         '由第 1 式 $x_2=a x_3$，代入第 4 式得 $b=x_2-a x_3=0$；由第 3 式 $x_1=x_3+x_4+1$，代入第 2 式：'),
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
    exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
    applied, failed = 0, []
    for (rid, no, f), reps in FIX.items():
        vol = next((v for v in exam if v['id'] == rid), None)
        if not vol:
            continue
        q = next((x for s in vol['sections'] for x in s['questions'] if str(x['no']) == no), None)
        if not q:
            continue
        v = q.get(f) or ''
        nv = v
        for old, new in reps:
            if old not in nv:
                failed.append('%s 第%s题.%s 未命中: %r' % (rid, no, f, old[:30]))
            else:
                nv = nv.replace(old, new, 1)
        if nv != v:
            fail, nseg = render_check(nv)
            if fail == 0:
                q[f] = nv
                applied += 1
                print('OK %s 第%s题.%s' % (rid, no, f))
            else:
                failed.append('%s 第%s题.%s 渲染失败 %d/%d' % (rid, no, f, fail, nseg))
    with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('应用 %d；未命中/失败 %d' % (applied, len(failed)))
    for x in failed[:8]:
        print('  W ' + x)


if __name__ == '__main__':
    main()
