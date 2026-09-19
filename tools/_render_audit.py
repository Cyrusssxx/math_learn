# -*- coding: utf-8 -*-
"""渲染级全库体检：对每题字段提取公式段（$...$ / $$...$$ / 裸公式行），逐个交给 KaTeX 渲染，
   统计渲染失败（KaTeX throwOnError）与「裸公式行未被 mdBlock 兜底」等情况。"""
import json, io, re, subprocess, os, sys, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
TOOLS = 'D:/ai code/math-note/tools/'
sys.path.insert(0, TOOLS)

FILES = {'exam': BASE + 'exam.json', 'core': BASE + 'core_bank.json'}

# 公式段提取：$$...$$（跨行）/ $...$（行内）/ 裸公式行（无 $ 但含 LaTeX，模拟 mdBlock 兜底）
DD = re.compile(r'\$\$(.+?)\$\$', re.S)
IN = re.compile(r'(?<!\$)\$([^$\n]+)\$(?!\$)')
CMD = re.compile(r'\\(?:frac|dfrac|tfrac|lim|left|right|begin|end|sum|int|iint|sqrt|ln|cdot|to|infty|partial|alpha|beta|gamma|theta|lambda|Delta|sigma|sin|cos|tan|cot|sec|csc|arctan|mathrm|text|quad|qquad|displaystyle|overline|vec|boldsymbol|matrix|pmatrix|cases|Bigl|Bigr|Big|big|log|max|min|exp|qquad|pm|mp|neq|leq|geq|sim|approx|cdot|circ|ast|prime)')
HAN = re.compile(r'[\u4e00-\u9fff]')


def extract(v):
    segs, bare = [], []
    used = set()
    for m in DD.finditer(v):
        segs.append(('D', m.group(1).replace('\n', ' ')))
        used.add(m.span())
    for m in IN.finditer(v):
        if any(a <= m.start() < b for a, b in used):
            continue
        segs.append(('I', m.group(1)))
        used.add(m.span())
    for i, L in enumerate(v.split('\n')):
        if '$' in L or HAN.search(L):
            continue
        if CMD.search(L) and L.strip() and len(L.strip()) > 3 and re.search(r'[=+\-^_{}\\]', L):
            # 模拟 mdBlock 裸公式行兜底：\begin 环境 → $$（display）+ 自动补缺失的 \end{X}；否则包 $（inline）
            t = L.strip()
            disp = bool(re.search(r'\\begin\{', t)) or bool(re.search(r'\\end\{', t))
            if disp:
                for env in re.findall(r'\\begin\{([^}]+)\}', t):
                    nb = len(re.findall(r'\\begin\{%s\}' % re.escape(env), t))
                    ne = len(re.findall(r'\\end\{%s\}' % re.escape(env), t))
                    t += '\\end{%s}' % env * max(0, nb - ne)
            bare.append((t, disp))
    return segs, bare


def main():
    js = (
        "const fs=require('fs');const vm=require('vm');const c={};vm.createContext(c);\n"
        "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),c);\n"
        "const lines=fs.readFileSync(process.argv[2],'utf8').split(String.fromCharCode(10)).filter(Boolean);\n"
        "let bad=[];\n"
        "for(let i=0;i<lines.length;i++){const [tag,loc,seg]=lines[i].split(String.fromCharCode(9));\n"
        "try{c.katex.renderToString(seg,{throwOnError:true});}catch(e){bad.push([tag,loc,seg.slice(0,60),e.message.slice(0,40)]);}}\n"
        "fs.writeFileSync(process.argv[3],JSON.stringify(bad));\n"
    )
    jsf = os.path.join(tempfile.gettempdir(), '_katex_batch.js')
    io.open(jsf, 'w', encoding='utf-8').write(js)

    for tag, path in FILES.items():
        d = json.load(io.open(path, encoding='utf-8'))
        rows = []          # tag, loc, seg
        fields_stat = {}
        for vol in (d if isinstance(d, list) else [d[0]]):
            for sec in vol.get('sections', []):
                for q in sec.get('questions', []):
                    for f in ('stem', 'answer', 'idea'):
                        v = q.get(f) or ''
                        if not v:
                            continue
                        segs, bare = extract(v)
                        for k, seg in segs:
                            rows.append('%s\t%s-%s.%s\t%s' % (k, vol.get('id'), q.get('no'), f, seg))
                        for seg, disp in bare:
                            # katex.renderToString 期望裸 LaTeX（不带 $ 分隔符）；页面里 renderMathInElement 剥掉 $ 再渲染
                            rows.append('%s\t%s-%s.%s\t%s' % ('B', vol.get('id'), q.get('no'), f, seg))
                        if bare:
                            fields_stat.setdefault('%s 第%s题.%s' % (vol.get('id'), q.get('no'), f), len(bare))
        inp = os.path.join(tempfile.gettempdir(), '_seg.txt')
        outp = os.path.join(tempfile.gettempdir(), '_bad.json')
        io.open(inp, 'w', encoding='utf-8').write('\n'.join(rows))
        r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp, outp],
                           capture_output=True, text=True)
        bad = json.loads(io.open(outp, encoding='utf-8').read() or '[]') if os.path.exists(outp) else []
        print('=' * 70)
        print('%s：公式段 %d 个，KaTeX 渲染失败 %d 个' % (tag, len(rows), len(bad)))
        from collections import Counter
        print('  失败类型分布:', dict(Counter(b[0] for b in bad)))
        for b in bad[:8]:
            print('    [%s] %s | %s → %s' % (b[0], b[1], b[2][:50], b[3]))
        bare_fields = sorted(fields_stat.items(), key=lambda x: -x[1])
        print('  含裸公式行的字段 %d 个（Top5）:' % len(bare_fields))
        for k, v in bare_fields[:5]:
            print('    %s  %d 行' % (k, v))
    os.remove(jsf)


if __name__ == '__main__':
    main()
