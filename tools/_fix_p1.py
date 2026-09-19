# -*- coding: utf-8 -*-
"""P1 修复：把「display 块之间」的裸公式段（无中文、含 LaTeX 命令）包成 $$ 显示块。
   例：`$$A$$X$$B$$` → `$$A$$\n$$X$$\n$$B$$`（X 为裸公式段）
   渲染验证 + 回滚。作用于全部残留字段。"""
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
HAN = re.compile(r'[\u4e00-\u9fff]')
CMD = re.compile(r'\\[a-zA-Z]{2,}')
LEAD_PUNC = re.compile(r'^[。，,；;：:.\s]+')


def fix_p1(v):
    parts = v.split('$$')
    out = []
    changed = False
    for i, p in enumerate(parts):
        if i % 2 == 0:
            # 块间文本
            s = p
            if (not HAN.search(s) and '$' not in s and CMD.search(s)
                    and re.search(r'[=+\-^_{}\\]', s) and len(s.strip()) > 4):
                seg = s.strip()
                lead = LEAD_PUNC.match(seg)
                lead = lead.group(0) if lead else ''
                seg = seg[len(lead):]
                # 尾部标点截掉
                tail = re.search(r'[.,;:。，；]+$', seg)
                tail_txt = tail.group(0) if tail else ''
                if tail:
                    seg = seg[:tail.start()]
                out.append(lead + '\n$$' + seg + '$$\n' + tail_txt)
                changed = True
            else:
                out.append(p)
        else:
            out.append('$$' + p + '$$')
    return ''.join(out), changed


def render_check(text):
    segs = []
    for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$', text):
        segs.append(m.group(1) or m.group(2))
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
    audit = json.load(io.open('D:/ai code/math-note/tools/_full_audit.json', encoding='utf-8'))
    bad_keys = sorted(audit['bad'].keys())
    core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
    exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
    core_q = {str(q['no']): q for s in core[0]['sections'] for q in s['questions']}
    exam_q = {}
    for vol in exam:
        for s in vol.get('sections', []):
            for q in s.get('questions', []):
                exam_q[(vol['id'], str(q['no']))] = q
    ok, rb, skip = 0, [], 0
    for k in bad_keys:
        if '真题' in k:
            dsh = k.index('-'); rid = k[:dsh]; rest = k[dsh+1:]
            no = rest[:rest.rindex('.')]; f = rest[rest.rindex('.')+1:]
            q = exam_q.get((rid, no))
        else:
            rest = k[len('core-'):]
            no = rest[:rest.rindex('.')]; f = rest[rest.rindex('.')+1:]
            q = core_q.get(no)
        if not q:
            continue
        v = q.get(f) or ''
        nv, ch = fix_p1(v)
        if not ch:
            skip += 1
            continue
        fail, nseg = render_check(nv)
        if fail == 0:
            q[f] = nv
            ok += 1
        else:
            rb.append((k, fail, nseg))
    with io.open(BASE + 'core_bank.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(core, fp, ensure_ascii=False, separators=(',', ':'))
    with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('P1：修好 %d，回滚 %d，跳过 %d（共 %d）' % (ok, len(rb), skip, len(bad_keys)))
    for k, fail, nseg in rb[:6]:
        print('  回滚 %s（%d/%d）' % (k, fail, nseg))


if __name__ == '__main__':
    main()
