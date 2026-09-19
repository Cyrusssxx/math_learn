# -*- coding: utf-8 -*-
"""渲染体检（输出失败字段清单，供 jsdom 复检）"""
import json, io, re, subprocess, os, tempfile, sys

BASE = 'D:/ai code/math-note/pwa/data/'
TOOLS = 'D:/ai code/math-note/tools/'
sys.path.insert(0, TOOLS)
from _render_audit import extract, CMD, HAN                      # noqa

FILES = {'exam': BASE + 'exam.json', 'core': BASE + 'core_bank.json'}


def main():
    js = (
        "const fs=require('fs');const vm=require('vm');const c={};vm.createContext(c);\n"
        "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),c);\n"
        "const lines=fs.readFileSync(process.argv[2],'utf8').split(String.fromCharCode(10)).filter(Boolean);\n"
        "const bad=[];\n"
        "for(let i=0;i<lines.length;i++){const idx=lines[i].indexOf(String.fromCharCode(9));"
        "const loc=lines[i].slice(0,idx);const seg=lines[i].slice(idx+1);\n"
        "try{c.katex.renderToString(seg,{throwOnError:true});}catch(e){bad.push([loc,seg.slice(0,60),e.message.slice(0,40)]);}}\n"
        "fs.writeFileSync(process.argv[3],JSON.stringify(bad));\n"
    )
    jsf = os.path.join(tempfile.gettempdir(), '_kb2.js')
    io.open(jsf, 'w', encoding='utf-8').write(js)

    for tag, path in FILES.items():
        d = json.load(io.open(path, encoding='utf-8'))
        rows = []
        for vol in (d if isinstance(d, list) else [d[0]]):
            for sec in vol.get('sections', []):
                for q in sec.get('questions', []):
                    for f in ('stem', 'answer', 'idea'):
                        v = q.get(f) or ''
                        if not v:
                            continue
                        segs, bare = extract(v)
                        for k, seg in segs:
                            rows.append('%s\t%s' % ('%s-%s.%s' % (vol.get('id'), q.get('no'), f), seg))
                        for seg, disp in bare:
                            rows.append('%s\t%s' % ('%s-%s.%s' % (vol.get('id'), q.get('no'), f), seg))
        inp = os.path.join(tempfile.gettempdir(), '_s2.txt')
        outp = os.path.join(tempfile.gettempdir(), '_b2.json')
        io.open(inp, 'w', encoding='utf-8').write('\n'.join(rows))
        subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, inp, outp],
                       capture_output=True, text=True)
        bad = json.loads(io.open(outp, encoding='utf-8').read() or '[]') if os.path.exists(outp) else []
        from collections import Counter, defaultdict
        byfield = defaultdict(list)
        for loc, seg, msg in bad:
            byfield[loc].append((seg, msg))
        print('=' * 70)
        print('%s：失败公式 %d 个，涉及字段 %d 个' % (tag, len(bad), len(byfield)))
        for loc, items in sorted(byfield.items(), key=lambda x: -len(x[1]))[:14]:
            print('  %s  %d 处' % (loc, len(items)))
        # 输出清单供 jsdom 复检
        io.open(os.path.join(TOOLS, '_bad_fields_%s.json' % tag), 'w', encoding='utf-8').write(
            json.dumps({k: v for k, v in byfield.items()}, ensure_ascii=False, indent=0))
    os.remove(jsf)


if __name__ == '__main__':
    main()
