# -*- coding: utf-8 -*-
"""p91-119 自动重建：文字层切块 → 参考库取 LaTeX → 字符多重集互校。

PDF 有文字层（重排版），因此：
  1) 按标签（如 `i.iv.iv.ii.ii.v)2026 数一二三`）把每页切成题目块；
  2) 从块的标签里取「年份 + 科目」作为题源；
  3) 在本地参考库（大观园 5952 / exam.json / practice / bankq）中按年份+科目筛候选，
     用字符多重集 + 序列相似度找最佳匹配，取其 LaTeX 作为候选题干；
  4) 用文字层字符多重集反查候选题干：一致 → 高置信；不一致 → 标记需人工/视觉复核。

输出：tools/_rest_draft.json（含置信度与差异） + 屏幕摘要
"""
import json, io, re, sys, difflib
from collections import Counter

sys.path.insert(0, 'D:/ai code/math-note/tools')
from _match_ref import load_refs, norm, grams, subj_of, years_of   # noqa: E402

ROOT = 'D:/ai code/math-note/tools/'

TAG = re.compile(r'\(?(?:[a-z0-9]{1,4}\.){2,}[a-z0-9]{0,4}\)?')
# 次级标签：罗马小写点分且以右括号结尾，如 `i.v.i.ii.i.iv)`（原 TAG 会漏）
TAG2 = re.compile(r'(?m)^\s*(?:[a-z]{1,4}\.\s*){1,}[a-z0-9]{0,4}\)')
SRC = re.compile(r'((?:19|20)\d{2})\s*数([一二三123]+)')


FUNCS = (r'(cos|sin|tan|cot|sec|csc|ln|log|arctan|arccos|arcsin|sinh|cosh|tanh|'
         r'exp|max|min|lim|det|gcd|sup|inf|deg|arg|Pr|Re|Im)')


def norm_char(s):
    """只留中文字/字母/数字。函数名保留（PDF 写作 cos、LaTeX 写作 \\cos，须口径一致）"""
    s = re.sub(r'【[^】]*】', '', str(s or ''))
    s = re.sub(r'\\(?:begin|end)\{[^{}]*\}', '', s)
    s = re.sub(r'\\' + FUNCS, lambda m: m.group(1), s)   # 函数名去掉反斜杠保留名字
    s = re.sub(r'\\[a-zA-Z]+', '', s)                     # 其余命令整段删除
    s = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]', '', s)
    return s


def ms(s):
    s = norm_char(s)
    return Counter(re.findall(r'\d', s)), Counter(re.findall(r'[a-zA-Z]', s.lower()))


def split_blocks(text):
    """按标签切块（主标签 + 罗马次级标签），返回 [(tag, body)]"""
    spans = []
    for rx in (TAG, TAG2):
        for m in rx.finditer(text):
            spans.append((m.start(), m.end(), m.group(0)))
    spans.sort()
    # 去重叠
    clean = []
    last_end = -1
    for s, e, t in spans:
        if s < last_end:
            continue
        clean.append((s, e, t))
        last_end = e
    blocks = []
    for i, (s, e, tag) in enumerate(clean):
        end = clean[i + 1][0] if i + 1 < len(clean) else len(text)
        blocks.append((tag, text[e:end]))
    return blocks


def call_type(body):
    b = body
    if re.search(r'(?m)^\s*A[\.、]', b) and re.search(r'(?m)^\s*D[\.、]', b):
        return 'choice'
    if '证明' in b and len(b) < 400:
        return 'proof'
    if re.search(r'= *_{3,}|=\s*___', b) or '____' in b:
        return 'fill'
    if re.search(r'求|计算|确定|讨论', b):
        return 'calc'
    return 'fill'


def clean_body(body, tag=''):
    """剥离页脚/题源标签/内部编号/题号/选项字母，得到纯净题面"""
    b = str(body or '')
    b = b.replace(tag, ' ')
    b = re.sub(r'【例[^】]*】', ' ', b)
    b = re.sub(r'（?\s*(?:19|20)\d{2}\s*年?\s*[,，]?\s*数[一二三](?:[、,，]?\s*数?[一二三])*\s*）?', ' ', b)
    b = re.sub(r'(?:880|660|1000|26\s*版|25\s*版|30\s*例|武\S{0,6}|姜\S{0,6})[^\n]{0,40}', ' ', b)
    b = re.sub(r'大观严选题[^\n]*', ' ', b)
    b = b.replace('澄潇宇', ' ')
    b = re.sub(r'第\s*\d+\s*页[，,]?\s*共\s*\d+\s*页', ' ', b)
    b = re.sub(r'^\s*\(?\d{1,2}\)?\s*[.、]?\s*', ' ', b)               # 仅块首题号
    b = re.sub(r'(?m)^\s*[A-D]\s*[.、．]\s*', ' ', b)                  # 选项字母标记
    b = re.sub(r'(?<=[\s)])[A-D]\s*[.、．]\s*', ' ', b)
    b = re.sub(r'\s+', ' ', b)
    return b.strip()


def ref_full(r):
    """参考题的「题干 + 选项」合并文本"""
    parts = [r['stem'] or '']
    opts = r['options'] or []
    if isinstance(opts, dict):
        opts = list(opts.values())
    for i, o in enumerate(opts):
        parts.append(str(o))
    return ' '.join(parts)


def main():
    tl = json.load(io.open(ROOT + '_yancai_textlayer.json', encoding='utf-8'))
    refs = load_refs()
    by_year = {}
    for i, r in enumerate(refs):
        for y in years_of(r['src']):
            by_year.setdefault(y, []).append(i)
    for r in refs:
        r['full_norm'] = norm_char(ref_full(r))

    out = []
    stat = Counter()
    for p in range(91, 120):
        text = tl.get(str(p), '')
        blocks = split_blocks(text)
        order = 0
        for tag, body in blocks:
            raw = body
            m = SRC.search(tag) or SRC.search(raw[:120])
            if not m:
                continue
            year, subs = m.group(1), m.group(2)
            src_tag = '%s数%s' % (year, subs)
            body_clean = clean_body(raw, tag)
            core = norm_char(body_clean)
            if len(core) < 6:
                continue

            cands = by_year.get(year, [])
            gc = grams(core)
            scored = []
            for i in cands:
                r = refs[i]
                inter = len(gc & r['grams'])
                if inter < max(3, len(gc) * 0.25):
                    continue
                s = difflib.SequenceMatcher(None, core, r['full_norm'], autojunk=False).ratio()
                if any(ch in r['src'] for ch in subs):
                    s += 0.03
                scored.append((min(1.0, s), i))
            if not scored and cands:
                # 兜底：不做 gram 门槛，直接取该年最相似
                for i in cands:
                    s = difflib.SequenceMatcher(None, core, refs[i]['full_norm'], autojunk=False).ratio()
                    scored.append((s, i))
            scored.sort(key=lambda x: -x[0])
            # 二次兜底：同年最佳仍偏低 → 全库搜索（防年份标签串行/错标）
            if (not scored or scored[0][0] < 0.8) and len(refs) > 100:
                best2 = []
                for i, r in enumerate(refs):
                    inter = len(gc & r['grams'])
                    if inter < max(3, len(gc) * 0.45):
                        continue
                    s = difflib.SequenceMatcher(None, core, r['full_norm'], autojunk=False).ratio()
                    best2.append((s, i))
                best2.sort(key=lambda x: -x[0])
                if best2 and (not scored or best2[0][0] > scored[0][0]):
                    scored = best2[:5]

            order += 1
            rec = {'page': p, 'order': order, 'tag': tag.strip(), 'source': src_tag,
                   'type': call_type(body_clean), 'body': body_clean[:300],
                   'score': None, 'ref': None, 'stem': None, 'options': None,
                   'answer': None, 'chars_ok': None, 'missing': ''}
            if scored:
                s, i = scored[0]
                r = refs[i]
                cd, cl = ms(body_clean)
                rd, rl = ms(ref_full(r))
                miss = list((cd - rd).elements()) + list((cl - rl).elements())
                extra = list((rd - cd).elements()) + list((rl - cl).elements())
                rec.update({'score': round(s, 3), 'ref': '%s/%s' % (r['ref'], r['rid']),
                            'stem': r['stem'], 'options': r['options'] or None,
                            'answer': r['answer'][:300] if r['answer'] else None,
                            'chars_ok': (not miss) and (not extra) and s >= 0.8,
                            'missing': ''.join(miss), 'extra_in_ref': ''.join(extra)})
            out.append(rec)

            if rec['chars_ok']:
                stat['✅ 双向字符一致且相似度≥0.8'] += 1
            elif rec['score'] is None:
                stat['❌ 参考库无候选'] += 1
            elif rec['score'] >= 0.8 and not rec['missing']:
                stat['🟡 仅参考多出字符（选项/注释）'] += 1
            elif rec['score'] >= 0.8:
                stat['🟠 高相似但有字符差'] += 1
            else:
                stat['❌ 低相似度需人工'] += 1

    with io.open(ROOT + '_rest_draft.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print('p91-119 共切出 %d 题' % len(out))
    for k, v in stat.most_common():
        print('  %-24s %d' % (k, v))
    print()
    print('—— 低置信 / 无候选 明细 ——')
    for r in out:
        if r['chars_ok']:
            continue
        print('[p%s #%s] %s src=%s score=%s ref=%s' %
              (r['page'], r['order'], r['tag'][:28], r['source'], r['score'], r['ref']))
        print('   PDF块: %s' % r['body'].replace('\n', ' ')[:170])
        if r['stem']:
            print('   参考 : %s' % r['stem'].replace('\n', ' ')[:170])
            print('   差异 : PDF多出=%r 参考多出=%r' % (r['missing'], r.get('extra_in_ref')))
        print()


if __name__ == '__main__':
    main()
