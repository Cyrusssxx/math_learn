# -*- coding: utf-8 -*-
"""批量修复器 v3（融合手工经验）：
   A 块间裸公式段（剥离 \\text{...} 后无中文）→ 整段包 $$ 显示块
   B 含中文的行 → 只包其中的公式子串（\\ 开头到中文标点/行尾，含 =|\\frac|\\lim 等强特征）→ $...$
   C 孤立 `.$$` 行（仅标点+$$）→ 删除
   D 空块 `$$$$` → 删除
   E 三 `$$$` → `$$`
   对 tools/_full_audit.json 里的残留字段批量应用；每字段渲染验证，失败回滚。
"""
import json, io, re, subprocess, os, tempfile

BASE = 'D:/ai code/math-note/pwa/data/'
HAN = re.compile(r'[\u4e00-\u9fff]')
CMD = re.compile(r'\\[a-zA-Z]{2,}')
CN_PUNC = re.compile(r'[\u4e00-\u9fff。；，、：？！（）【】“”‘’]')
STRONG = re.compile(r'\\frac|\\dfrac|\\lim|\\sum|\\int|\\sqrt|\\begin|[=<>]|\\partial|\\mathrm|\\sin|\\cos|\\ln|\\displaystyle')
LEAD = re.compile(r'^[。，,；;：:.\s]+')
TAIL = re.compile(r'[.,;:。，；]+$')


def strip_text(s):
    s = re.sub(r'\\text\{[^}]*\}', '', s)
    s = re.sub(r'\\operatorname\{[^}]*\}', '', s)
    return s


def wrap_sub_in_line(L):
    """含中文的行：把其中的公式子串包 $...$"""
    out = L
    i = 0
    res = ''
    while i < len(L):
        if L[i] == '\\' and CMD.match(L, i):
            j = i
            # 扩展到中文标点或行尾（花括号平衡）
            depth = 0
            while j < len(L):
                ch = L[j]
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth < 0:
                        break
                elif depth == 0 and CN_PUNC.match(ch):
                    break
                j += 1
            seg = L[i:j].rstrip()
            if len(seg) > 3 and STRONG.search(seg):
                m = TAIL.search(seg)
                tt = m.group(0) if m else ''
                if m:
                    seg = seg[:m.start()]
                res += '$' + seg + '$' + tt
            else:
                res += L[i:j]
            i = j
        else:
            res += L[i]
            i += 1
    return res


def fix_field(v):
    orig = v
    # A + B：基于 $$ 分隔符流
    parts = v.split('$$')
    out = []
    for i, p in enumerate(parts):
        if i % 2 == 0:
            s = p
            s_clean = strip_text(s)
            if (not HAN.search(s_clean) and '$' not in s and CMD.search(s)
                    and re.search(r'[=+\-^_{}\\]', s) and len(s.strip()) > 4):
                seg = s.strip()
                lead = LEAD.match(seg)
                lead = lead.group(0) if lead else ''
                seg = seg[len(lead):]
                tail = TAIL.search(seg)
                tt = tail.group(0) if tail else ''
                if tail:
                    seg = seg[:tail.start()]
                if len(seg.strip()) > 4:
                    out.append(lead + '\n$$\n' + seg.strip() + '\n$$\n' + tt)
                    continue
            # 含中文：尝试包公式子串（若该段不是纯中文说明文字）
            if HAN.search(s) and '$' not in s and CMD.search(s) and STRONG.search(s):
                out.append(wrap_sub_in_line(s))
                continue
            out.append(p)
        else:
            out.append('$$' + p + '$$')
    v = ''.join(out)
    # C/D/E：行级清理
    lines = v.split('\n')
    res = []
    for L in lines:
        st = L.strip()
        if st == '$$$$':
            continue
        if re.match(r'^[.。，,]\s*\$\$$', st):
            continue
        if st == '$$$':
            res.append('$$')
            continue
        res.append(L)
    v = '\n'.join(res)
    return v, v != orig


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
            dsh = k.index('-'); rid = k[:dsh]; rest = k[dsh + 1:]
            no = rest[:rest.rindex('.')]; f = rest[rest.rindex('.') + 1:]
            q = exam_q.get((rid, no))
        else:
            rest = k[len('core-'):]
            no = rest[:rest.rindex('.')]; f = rest[rest.rindex('.') + 1:]
            q = core_q.get(no)
        if not q:
            continue
        v = q.get(f) or ''
        nv, ch = fix_field(v)
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
    print('批量 v3：修好 %d，回滚 %d，跳过 %d（共 %d）' % (ok, len(rb), skip, len(bad_keys)))
    for k, fail, nseg in rb[:6]:
        print('  回滚 %s（%d/%d）' % (k, fail, nseg))


if __name__ == '__main__':
    main()
