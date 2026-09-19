# -*- coding: utf-8 -*-
"""内容级修复（针对残留字段）：中文行内的裸 LaTeX 公式段 → 包 $...$；$$ 配对；渲染验证+回滚。
   规则（保守，避免制造碎片）：
   F1 公式段 = 从 \ 命令开始，到「中文/中文标点」或行尾结束；段内含 2+ LaTeX 命令 或 含 '=' 或
      含 \frac|\lim|\sum|\int 等强特征 → 包 $...$
   F2 $$ 配对：状态机补缺/删多
   每字段修后做 KaTeX 段级渲染验证（throwOnError），失败 → 回滚该字段。
"""
import json, io, re, subprocess, os, tempfile, sys

BASE = 'D:/ai code/math-note/pwa/data/'
HAN = re.compile(r'[\u4e00-\u9fff]')
STRONG = re.compile(r'\\frac|\\dfrac|\\lim|\\sum|\\int|\\iint|\\sqrt|\\begin|\\left|\\right|=')
CMD2 = re.compile(r'\\[a-zA-Z]{2,}')
CN_PUNC = re.compile(r'[\u4e00-\u9fff。；，、：？！（）【】]')


def formula_segments(line):
    """返回该行应包裹的公式段（列表）"""
    segs = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '\\':
            # 命令开始
            m = CMD2.match(line, i)
            if m:
                j = i
                # 向后扩展到中文/中文标点/行尾
                while j < len(line) and not CN_PUNC.match(line[j]):
                    j += 1
                seg = line[i:j]
                # 判定：强特征 或 (2+ 命令 且 有运算符号)
                if (len(seg) > 4 and (STRONG.search(seg) or (len(CMD2.findall(seg)) >= 2 and re.search(r'[=+\-^_{}\\[\\]]', seg)))):
                    segs.append((i, j, seg))
                    i = j
                    continue
        i += 1
    return segs


def fix_field(v):
    orig = v
    # F1：行内裸公式段包裹
    lines = v.split('\n')
    out = []
    for L in lines:
        segs = formula_segments(L)
        if not segs:
            out.append(L)
            continue
        nv = ''
        cur = 0
        for a, b, seg in segs:
            nv += L[cur:a] + '$' + seg + '$'
            cur = b
        nv += L[cur:]
        out.append(nv)
    v = '\n'.join(out)
    # F2：$$ 配对（独立 $$ 行计数为奇数 → 补；连续开块吞正文 → 删）
    lines = v.split('\n')
    dd = [i for i, L in enumerate(lines) if L.strip() == '$$']
    if len(dd) % 2 == 1:
        # 补一个闭合在末尾
        lines.insert(len(lines), '$$')
        v = '\n'.join(lines)
    return v, v != orig


def render_check(text):
    """提取公式段并 KaTeX 渲染；返回 (fail_count, seg_count)"""
    segs = []
    for m in re.finditer(r'\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$', text):
        segs.append(m.group(1) or m.group(2))
    for L in text.split('\n'):
        if '$' in L or HAN.search(L):
            continue
        if re.search(r'\\[a-zA-Z]{2,}', L) and re.search(r'[=+\-^_{}\\]', L):
            t = L.strip()
            disp = bool(re.search(r'\\begin\{', t))
            envs = re.findall(r'\\begin\{([^}]+)\}', t)
            for env in envs:
                nb = len(re.findall(r'\\begin\{%s\}' % re.escape(env), t))
                ne = len(re.findall(r'\\end\{%s\}' % re.escape(env), t))
                if nb > ne:
                    t += '\\end{%s}' % env * (nb - ne)
            segs.append(t)
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
    from collections import defaultdict
    audit = json.load(io.open('D:/ai code/math-note/tools/_full_audit.json', encoding='utf-8'))
    bad_keys = set(audit['bad'].keys())
    fix_map = {}   # 字段key -> (kind, no, field)
    for k in bad_keys:
        if '真题' in k:
            dash = k.index('-')
            rid = k[:dash]
            rest = k[dash + 1:]
            no = rest[:rest.rindex('.')]
            f = rest[rest.rindex('.') + 1:]
            fix_map[k] = ('exam', rid, no, f)
        elif k.startswith('core-'):
            rest = k[len('core-'):]
            no = rest[:rest.rindex('.')]
            f = rest[rest.rindex('.') + 1:]
            fix_map[k] = ('core', None, no, f)

    core = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
    exam = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
    core_q = {str(q['no']): q for s in core[0]['sections'] for q in s['questions']}
    exam_q = {}
    for vol in exam:
        for s in vol.get('sections', []):
            for q in s.get('questions', []):
                exam_q[(vol['id'], str(q['no']))] = q

    ok, rollback, skip = 0, [], 0
    for k, (kind, rid, no, f) in sorted(fix_map.items()):
        q = core_q.get(no) if kind == 'core' else exam_q.get((rid, no))
        if not q:
            skip += 1
            continue
        v = q.get(f) or ''
        nv, ch = fix_field(v)
        if not ch:
            ok += 1          # 无需改（或改完一样）
            continue
        fail, nseg = render_check(nv)
        if fail == 0:
            q[f] = nv
            ok += 1
        else:
            rollback.append((k, fail, nseg))

    with io.open(BASE + 'core_bank.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(core, fp, ensure_ascii=False, separators=(',', ':'))
    with io.open(BASE + 'exam.json', 'w', encoding='utf-8', newline='') as fp:
        json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
    print('处理 %d 字段：修好/无需改 %d，回滚 %d' % (len(fix_map), ok, len(rollback)))
    for k, fail, nseg in rollback[:10]:
        print('  回滚 %s（失败 %d/%d 段）' % (k, fail, nseg))


if __name__ == '__main__':
    main()
