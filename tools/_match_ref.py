# -*- coding: utf-8 -*-
"""核心题库（yancai_bank.json）↔ 本地参考题库 全量交叉核对。

参考库：
  A. 大观园 questions.json  5952 题，覆盖数一/二/三真题 1987-2026（含答案+解析）
  B. exam.json             数二真题 607 题
  C. practice.json         大观园已导入版 1402 题
  D. bank_questions.json   827 题

输出：
  tools/_match_report.json   全量结果
  tools/_match_triage.txt    分级核查清单（HIGH=数字差异 / MED=字母差异 / LOW=纯格式）
"""
import json, io, os, re, sys, difflib
from collections import Counter, defaultdict

ROOT = 'D:/ai code/math-note/tools/'
BASE = 'D:/ai code/math-note/pwa/data/'
DGY = ('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/'
       'daguanyuan-for-windows-main/assets/questions.json')

DECOR = ['displaystyle', 'textstyle', 'limits', 'nolimits',
         'quad', 'qquad', 'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
         'mathstrut', 'strut', 'negthinspace', 'thinspace', 'enspace']


def norm(s):
    """LaTeX 归一化：消除格式差异，保留所有数字/字母/结构符号"""
    if not s:
        return ''
    s = str(s)
    s = re.sub(r'【[^】]*】', '', s)                       # 去掉所有【...】标注
    s = re.sub(r'^\s*\(?[a-z.]{4,}\)?\s*', '', s)          # 开头的内部编号 (a.b.c.d.c.g.a)
    s = re.sub(r'^\s*\(?\d{1,2}\)?\s*[.、]?\s*', '', s)    # 开头题号
    s = re.sub(r'第\s*\d+\s*题', '', s)
    s = re.sub(r'例\s*\d+(?:\.\d+)*', '', s)               # 【例3.34】残留 "例3.34"
    s = re.sub(r'（?\s*(?:19|20)\d\d\s*年?\s*[,，]?\s*数[一二三](?:[,、]?数?[一二三])*\s*）?', '', s)
    s = re.sub(r'原书保留真题编号[^。.；;]*', '', s)
    s = s.replace('$$', '$')
    s = re.sub(r'\\math(?:rm|bf|it|cal|bb|frak|sf|tt)\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\text\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\operatorname\{([^{}]*)\}', r'\1', s)
    for d in DECOR:
        s = re.sub(r'\\' + d + r'\b', '', s)
    s = re.sub(r'\\[,;:!]', '', s)
    s = s.replace('\\ ', '')
    s = re.sub(r'\\[dt]frac', r'\\frac', s)
    s = s.replace('\\leqslant', '\\le').replace('\\geqslant', '\\ge')
    s = s.replace('\\neq', '\\ne').replace('\\not=', '\\ne')
    s = s.replace('\\varnothing', '\\emptyset')
    s = s.replace('\\mathrm{d}', 'd').replace('\\mathrm{e}', 'e')
    s = re.sub(r'\\operatorname\{([^{}]*)\}', r'\1', s)
    for v in 'tdxyuvsr':
        s = s.replace('\\,%s' % v, v)
    s = s.replace('\\\\', '@@')
    s = re.sub(r'\\([a-zA-Z]+)', r'\1', s)
    s = s.replace('@@', '@')
    s = re.sub(r'_{2,}', '#', s)
    s = re.sub(r'[\s$，。、；：（）()\[\]{}<>《》"“”‘’\'`~|]', '', s)
    s = s.replace('．', '.').replace('。', '')
    # 中文数字与阿拉伯数字统一（二↔2 等）
    for cn, ar in (('二', '2'), ('三', '3'), ('四', '4'), ('一', '1'), ('两', '2')):
        if len(cn) == 1 and cn in '二三四一两':
            pass
    return s.strip()


def sig_sets(s):
    """提取「显著性指纹」：数字多重集 / 小写字母多重集 / 结构符多重集"""
    digits = tuple(sorted(re.findall(r'\d+', s)))
    letters = tuple(sorted(re.findall(r'[a-zA-Z]', s.lower())))
    struct = tuple(sorted(re.findall(r'[#@+\-*/=<>!^_.,:;]', s)))
    return digits, letters, struct


def classify(core_norm, ref_norm, diffs):
    """全局多重集比较分级：数字集不同=HIGH；字母集不同=MED；否则=LOW"""
    if not diffs:
        return 'EXACT', ''
    cd, cl, cs = sig_sets(core_norm)
    rd, rl, rs = sig_sets(ref_norm)
    if cd != rd:
        return 'HIGH', '数字多重集不同（最危险）'
    if cl != rl:
        return 'MED', '字母多重集不同（变量/函数名差异）'
    if cs != rs:
        return 'LOW', '仅运算符/标点分布不同'
    return 'LOW', '仅文字表述差异'


def grams(s, n=3):
    if len(s) <= n:
        return {s} if s else set()
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def years_of(src):
    return re.findall(r'(?:19|20)\d\d', str(src or ''))


def subj_of(src):
    m = re.search(r'数([一二三123])', str(src or ''))
    if not m:
        return ''
    return {'一': '一', '1': '一', '二': '二', '2': '二', '三': '三', '3': '三'}[m.group(1)]


def load_refs():
    refs = []

    def add(r):
        r['norm'] = norm(r['stem'])
        r['grams'] = grams(r['norm'])
        if r['norm']:
            refs.append(r)

    if os.path.exists(DGY):
        d = json.load(io.open(DGY, encoding='utf-8'))
        items = d if isinstance(d, list) else (d.get('questions') or d.get('items') or d)
        if isinstance(items, dict):
            items = list(items.values())
        for q in items:
            add({'ref': 'dgy', 'rid': str(q.get('id')), 'src': str(q.get('source') or ''),
                 'stem': q.get('stem') or '', 'options': q.get('options') or [],
                 'answer': q.get('answer') or '', 'explanation': q.get('explanation') or '',
                 'categoryIds': q.get('categoryIds') or []})
    ex = json.load(io.open(BASE + 'exam.json', encoding='utf-8'))
    for vol in ex:
        y = str(vol.get('year'))
        for sec in vol.get('sections', []):
            for q in sec.get('questions', []):
                add({'ref': 'exam', 'rid': '%s-%s' % (y, q.get('no')), 'src': '%s数二' % y,
                     'stem': q.get('stem') or '', 'options': list(q.get('options') or []),
                     'answer': q.get('answer') or '', 'explanation': q.get('idea') or '',
                     'categoryIds': q.get('categoryIds') or []})
    pr = json.load(io.open(BASE + 'practice.json', encoding='utf-8'))
    for vol in pr:
        for sec in vol.get('sections', []):
            for q in sec.get('questions', []):
                add({'ref': 'practice', 'rid': str(q.get('dg_id') or q.get('no')),
                     'src': str(q.get('source') or ''), 'stem': q.get('stem') or '',
                     'options': q.get('options') or [], 'answer': q.get('answer') or '',
                     'explanation': q.get('idea') or '',
                     'categoryIds': q.get('categoryIds') or []})
    bq = json.load(io.open(BASE + 'bank_questions.json', encoding='utf-8'))
    for q in bq.get('items', []):
        add({'ref': 'bankq', 'rid': str(q.get('id')), 'src': str(q.get('source') or ''),
             'stem': q.get('stem') or '', 'options': q.get('options') or [],
             'answer': q.get('answer') or '', 'explanation': q.get('explanation') or '',
             'categoryIds': q.get('categoryIds') or []})
    return refs


def build_index(refs):
    inv = defaultdict(list)
    for i, r in enumerate(refs):
        for g in r['grams']:
            inv[g].append(i)
    return inv


def diff_ops(a, b, ctx=8):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        out.append({'tag': tag,
                    'core': a[max(0, i1 - ctx):i2 + ctx],
                    'ref': b[max(0, j1 - ctx):j2 + ctx],
                    'ecore': a[i1:i2], 'eref': b[j1:j2]})   # 精确差异段（用于分级）
    return out


SIG_DIGIT = re.compile(r'\d')
SIG_ALPHA = re.compile(r'[a-zA-Z]')


def opt_compare(core_opts, ref_opts):
    """选择题选项比对，返回 (状态, 明细)。core_opts 可能是 dict{'A':..} 或 list。"""
    if isinstance(core_opts, dict):
        core_opts = ['%s %s' % (k, v) for k, v in core_opts.items()]
    if not core_opts or not ref_opts:
        return 'N/A', []
    def keyof(o):
        m = re.match(r'\s*[（(]?([A-D])[）)]?\s*', str(o))
        if m:
            return m.group(1), norm(str(o)[m.end():])
        return None, norm(str(o))
    core_map = {}
    for o in core_opts:
        k, v = keyof(o)
        if k:
            core_map[k] = v
    ref_map = {}
    for o in ref_opts:
        k, v = keyof(o)
        if k:
            ref_map[k] = v
    if not core_map or not ref_map:
        # 参考库选项无字母前缀，退化为按序比对
        co = [norm(str(o)) for o in core_opts]
        ro = [norm(str(o)) for o in ref_opts]
        if len(co) != len(ro):
            return 'DIFF', [{'tag': 'count', 'core': '%d项' % len(co), 'ref': '%d项' % len(ro)}]
        bad = [{'tag': 'opt%s' % chr(65 + i), 'core': co[i], 'ref': ro[i]}
               for i in range(len(co)) if co[i] != ro[i]]
        return ('SAME' if not bad else 'DIFF'), bad[:6]
    bad = []
    for k in sorted(set(core_map) | set(ref_map)):
        a = core_map.get(k, '【缺】')
        b = ref_map.get(k, '【缺】')
        if a != b:
            bad.append({'tag': 'opt' + k, 'core': a, 'ref': b})
    return ('SAME' if not bad else 'DIFF'), bad[:6]


def show_one(qid, refs=None, topn=8):
    """指定题：列出同年同科参考候选中相似度最高的若干条，供人工定稿"""
    bank = json.load(io.open(ROOT + 'yancai_bank.json', encoding='utf-8'))
    q = next((x for x in bank['questions'] if x['id'] == qid), None)
    if not q:
        print('没有这道题:', qid)
        return
    nq = norm(q['stem'])
    subj = subj_of(q.get('source'))
    yr = years_of(q.get('source'))
    print('=' * 76)
    print('核心题 [%s] page=%s src=%s' % (qid, q['page'], q.get('source')))
    print('STEM:', (q.get('stem') or '')[:400])
    if isinstance(q.get('options'), dict):
        for k in 'ABCD':
            if q['options'].get(k):
                print('   (%s) %s' % (k, q['options'][k][:180]))
    keep = [i for i, r in enumerate(refs)
            if (not yr or any(y in r['src'] for y in yr))]
    if not keep:
        keep = range(len(refs))
    scored = []
    for i in keep:
        s = difflib.SequenceMatcher(None, nq, refs[i]['norm'], autojunk=False).ratio()
        scored.append((s, i))
    scored.sort(key=lambda x: -x[0])
    print('--- 同源候选 Top%d（年份 %s）---' % (topn, yr))
    for s, i in scored[:topn]:
        r = refs[i]
        print('  %.3f [%s %s] %s' % (s, r['ref'], r['src'], r['rid']))
        print('       %s' % (r['stem'] or '').replace('\n', ' ')[:230])
        if r['options']:
            print('       选项:', str(r['options'])[:160])
        print('       答案:', (r['answer'] or '')[:120].replace('\n', ' '))


def show_many(ids):
    refs = load_refs()
    for qid in ids:
        show_one(qid, refs)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == 'show':
        show_many(sys.argv[2:])
        return
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    bank = json.load(io.open(ROOT + 'yancai_bank.json', encoding='utf-8'))
    qs = bank['questions']
    if limit:
        qs = qs[:limit]

    refs = load_refs()
    inv = build_index(refs)
    print('参考库载入 %d 题' % len(refs))
    print('待核对核心题库 %d 题' % len(qs))
    print()

    report = []
    buckets = {'HIGH': [], 'MED': [], 'LOW': [], 'NONE': []}

    for q in qs:
        nq = norm(q.get('stem'))
        gq = grams(nq)
        yr = years_of(q.get('source'))
        subj = subj_of(q.get('source'))

        cnt = Counter()
        for g in gq:
            for i in inv.get(g, ()):
                cnt[i] += 1
        cands = [i for i, c in cnt.most_common(400) if c >= max(3, len(gq) * 0.15)]

        scored = []
        for i in cands:
            r = refs[i]
            sim = difflib.SequenceMatcher(None, nq, r['norm'], autojunk=False).ratio()
            if yr and any(y in r['src'] for y in yr):
                sim += 0.06
            if subj and subj in r['src'][:8]:
                sim += 0.03
            scored.append((min(1.0, sim), i))
        scored.sort(key=lambda x: -x[0])
        top = scored[:3]

        best = None
        if top:
            s0, i0 = top[0]
            r0 = refs[i0]
            diffs = diff_ops(nq, r0['norm'])
            ost, odet = opt_compare(q.get('options'), r0['options'])
            best = {'score': round(s0, 4), 'ref': r0['ref'], 'rid': r0['rid'], 'src': r0['src'],
                    'stem': r0['stem'], 'answer': r0['answer'][:400],
                    'explanation': r0['explanation'][:400],
                    'diffs': diffs[:14], 'opt_status': ost, 'opt_diffs': odet,
                    'other': [{'score': round(s, 4), 'src': refs[i]['src'], 'rid': refs[i]['rid'],
                               'stem': refs[i]['stem'][:100]} for s, i in top[1:]]}
        rec = {'id': q['id'], 'page': q['page'], 'order': q['order'], 'source': q.get('source'),
               'type': q.get('type'), 'stem': q.get('stem'),
               'options': q.get('options'), 'best': best}
        report.append(rec)

        if best is None or best['score'] < 0.6:
            buckets['NONE'].append(rec)
            continue
        grade, why = classify(nq, refs[top[0][1]]['norm'] if top else '', best['diffs'] if best else [])
        optbad = best['opt_status'] == 'DIFF'
        if grade == 'EXACT' and not optbad:
            continue
        if optbad and grade == 'LOW':
            grade = 'MED'
        buckets[grade if grade != 'EXACT' else 'LOW'].append(rec)

    with io.open(ROOT + '_match_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    # ---- 可读清单 ----
    lines = []
    stat = Counter()
    for rec in report:
        b = rec['best']
        if b is None or b['score'] < 0.6:
            stat['❌ 未匹配'] += 1
        elif b['score'] >= 0.99 and not b['diffs'] and b['opt_status'] != 'DIFF':
            stat['✅ 完全一致(含选项)'] += 1
        elif b['score'] >= 0.97:
            stat['✅ 题干一致'] += 1
        else:
            stat['🟡 有差异'] += 1

    lines.append('===== 匹配统计 =====')
    for k, v in stat.most_common():
        lines.append('  %-20s %d' % (k, v))
    lines.append('')
    lines.append('===== 按题源 × 等级 =====')
    grid = Counter()
    for rec in report:
        s = str(rec['source'] or '')
        cat = '数一' if '数一' in s else ('数三' if '数三' in s else ('数二' if '数二' in s else '其他'))
        b = rec['best']
        if b is None or b['score'] < 0.6:
            g = '❌'
        elif b['score'] >= 0.97:
            g = '✅'
        elif b['score'] >= 0.85:
            g = '🟡'
        else:
            g = '🟠'
        grid[(cat, g)] += 1
    for cat in ('数一', '数二', '数三', '其他'):
        r = {g: grid.get((cat, g), 0) for g in ('✅', '🟡', '🟠', '❌')}
        lines.append('  %-6s 共%-4d ✅%-4d 🟡%-4d 🟠%-4d ❌%-4d' %
                     (cat, sum(r.values()), r['✅'], r['🟡'], r['🟠'], r['❌']))
    lines.append('')

    for bucket, title in (('HIGH', '🔴 HIGH — 数字差异（必须逐条核对）'),
                          ('MED', '🟠 MED — 字母/选项差异'),
                          ('LOW', '🟢 LOW — 仅标点格式差异'),
                          ('NONE', '❌ 未匹配')):
        rows = buckets[bucket]
        lines.append('')
        lines.append('=' * 78)
        lines.append('%s   共 %d 条' % (title, len(rows)))
        lines.append('=' * 78)
        for rec in rows:
            b = rec['best']
            lines.append('')
            lines.append('[%s] page=%s order=%s src=%s score=%s' %
                         (rec['id'], rec['page'], rec['order'], rec['source'],
                          b['score'] if b else 'NA'))
            lines.append('  核心: %s' % (rec['stem'] or '')[:300])
            if rec.get('options'):
                for k in 'ABCD':
                    if rec['options'].get(k):
                        lines.append('    (%s) %s' % (k, rec['options'][k][:200]))
            if b:
                lines.append('  参考[%s %s]: %s' % (b['ref'], b['rid'], (b['stem'] or '')[:300]))
                if b['opt_diffs']:
                    for d in b['opt_diffs']:
                        lines.append('    选项%s 核心=%s | 参考=%s' % (d['tag'], d['core'][:90], d['ref'][:90]))
                for d in b['diffs'][:8]:
                    lines.append('    差异[%s] 核心=%s | 参考=%s' % (d['tag'], d['core'][:90], d['ref'][:90]))
                lines.append('  参考答案: %s' % (b['answer'] or '')[:200].replace('\n', ' '))
    with io.open(ROOT + '_match_triage.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print('\n'.join(lines[:20]))
    print()
    print('已写 tools/_match_triage.txt（%d 行）与 tools/_match_report.json' % len(lines))


if __name__ == '__main__':
    main()
