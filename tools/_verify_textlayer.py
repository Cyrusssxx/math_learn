# -*- coding: utf-8 -*-
"""用 PDF 文字层对核心题库做全量字符级校验。

原理：该 PDF 是重排版 PDF（带文字层），文字层里的数字/字母是权威的；
子代理转写时可能的错误就是「多加/漏掉数字或字母/变量」，因此把每道题对齐到
所属页的文字层区域，双向比对数字多重集与字母多重集即可暴露绝大多数内容错误。
（文字层不保留分式/根号结构，所以只用于字符校验，不用于结构还原。）

输出：tools/_tl_report.txt  + 屏幕摘要
"""
import json, io, re, difflib
from collections import Counter

ROOT = 'D:/ai code/math-note/tools/'


def norm_tl(s):
    """文字层/题干 通用归一化：去掉格式与不可见结构，只留中文字/字母/数字"""
    if not s:
        return ''
    s = str(s)
    s = re.sub(r'【[^】]*】', '', s)
    # 整块环境与占位命令：直接删除（否则 cases/hspace 的字母数字会被误计）
    s = re.sub(r'\\(?:begin|end)\{[^{}]*\}', '', s)
    s = re.sub(r'\\(?:hspace|vspace|kern|mkern|phantom|boxed|cancel|color|'
               r'math(?:rm|bf|it|cal|bb|frak|sf|tt)|operatorname|substack|'
               r'underline|overline|overset|underset|stackrel|frac|dfrac|tfrac|'
               r'sqrt|displaystyle|textstyle|limits|nolimits|left|right|quad|qquad)'
               r'\*?(\{[^{}]*\})*', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)          # 余下的命令名一律删除
    s = re.sub(r'[${}\\]', '', s)
    # Unicode 希腊/数学符号 → 名字（与去掉命令名后的核心题侧行为一致：都不计入）
    s = re.sub(r'[^\u4e00-\u9fffa-zA-Z0-9]', '', s)
    return s


def core_text(q):
    """核心题的比对文本 = 题干 + 选项（选项带字母），与 PDF 区域口径一致"""
    parts = [q.get('stem') or '']
    opts = q.get('options')
    if isinstance(opts, dict):
        for k in 'ABCD':
            if opts.get(k):
                parts.append('%s %s' % (k, opts[k]))
    elif isinstance(opts, list):
        for i, o in enumerate(opts):
            parts.append('%s %s' % ('ABCD'[i] if i < 4 else '', o))
    return norm_tl(' '.join(parts))


def msets(s):
    digits = tuple(sorted(re.findall(r'\d', s)))
    letters = tuple(sorted(re.findall(r'[a-zA-Z]', s.lower())))
    return Counter(digits), Counter(letters)


def find_region(core, page):
    """用最长匹配块把 core 对齐到 page，返回 (region 文本, 覆盖率)"""
    sm = difflib.SequenceMatcher(None, core, page, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 2]
    if not blocks:
        return '', 0.0
    start = blocks[0].b
    end = blocks[-1].b + blocks[-1].size
    total = sum(b.size for b in blocks)
    region = page[max(0, start - 12):min(len(page), end + 12)]
    return region, total / max(1, len(core))


def clean_region(region):
    """去掉 PDF 区域两端的题号标签/章节头（如 'ii.iii2016数一4'）"""
    r = re.sub(r'^[a-z0-9.\s)]*', '', region, count=1)
    r = re.sub(r'(?:19|20)\d{2}\s*数[一二三]+', '', r)
    return norm_tl(r)


def main():
    bank = json.load(io.open(ROOT + 'yancai_bank.json', encoding='utf-8'))
    tl = json.load(io.open(ROOT + '_yancai_textlayer.json', encoding='utf-8'))
    pages = {int(k): norm_tl(v) for k, v in tl.items()}

    rows = []
    for q in bank['questions']:
        core = core_text(q)
        page = pages.get(q['page'], '')
        region, cover = find_region(core, page)
        region_n = clean_region(region)
        cd, cl = msets(core)
        rd, rl = msets(region_n)
        miss_core = list((cd - rd).elements()) + list((cl - rl).elements())
        extra_page = list((rd - cd).elements()) + list((rl - cl).elements())
        rows.append({'id': q['id'], 'page': q['page'], 'src': q.get('source'),
                     'cover': round(cover, 3),
                     'missing_in_pdf': ''.join(miss_core),
                     'missing_in_core': ''.join(extra_page),
                     'stem': q.get('stem'), 'region': region})

    with io.open(ROOT + '_tl_report.json', 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)

    hard = [r for r in rows if r['missing_in_pdf'] and r['cover'] >= 0.55]
    soft = [r for r in rows if r['missing_in_core'] and r['cover'] >= 0.55
            and not r['missing_in_pdf']]
    lowcov = [r for r in rows if r['cover'] < 0.55]

    out = []
    out.append('覆盖率分布: >=0.8: %d | 0.55-0.8: %d | <0.55: %d' % (
        sum(1 for r in rows if r['cover'] >= 0.8),
        sum(1 for r in rows if 0.55 <= r['cover'] < 0.8), len(lowcov)))
    out.append('')
    out.append('=' * 78)
    out.append('A. 核心题字符在 PDF 文字层中找不到（= 核心可能多字/写错）  共 %d 条' % len(hard))
    out.append('=' * 78)
    for r in hard:
        out.append('[%s] page=%s src=%s cover=%s 多出字符=%r' %
                   (r['id'], r['page'], r['src'], r['cover'], r['missing_in_pdf']))
        out.append('   核心: %s' % (r['stem'] or '').replace('\n', ' ')[:220])
        out.append('   PDF : %s' % (r['region'] or '')[:220])
        out.append('')
    out.append('')
    out.append('=' * 78)
    out.append('B. PDF 文字层有而核心没有（= 核心可能漏字，含邻题噪声，需人眼确认） 共 %d 条' % len(soft))
    out.append('=' * 78)
    for r in soft:
        out.append('[%s] page=%s src=%s cover=%s 疑似漏=%r' %
                   (r['id'], r['page'], r['src'], r['cover'], r['missing_in_core']))
        out.append('   核心: %s' % (r['stem'] or '').replace('\n', ' ')[:220])
        out.append('   PDF : %s' % (r['region'] or '')[:220])
        out.append('')
    out.append('')
    out.append('=' * 78)
    out.append('C. 对齐覆盖率偏低（可能整题不符/页错位）  共 %d 条' % len(lowcov))
    out.append('=' * 78)
    for r in lowcov:
        out.append('[%s] page=%s src=%s cover=%s' % (r['id'], r['page'], r['src'], r['cover']))
        out.append('   核心: %s' % (r['stem'] or '').replace('\n', ' ')[:200])
        out.append('   PDF : %s' % (r['region'] or '')[:200])
        out.append('')

    with io.open(ROOT + '_tl_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

    print(out[0])
    print('A 类(核心多字/错字): %d | B 类(核心疑漏字): %d | C 类(对齐差): %d'
          % (len(hard), len(soft), len(lowcov)))
    print('明细见 tools/_tl_report.txt')
    print()
    print('A 类前 12 条:')
    for r in hard[:12]:
        print('  [%s] p%s src=%s 多出=%r' % (r['id'], r['page'], r['src'], r['missing_in_pdf']))
        print('     核心:', (r['stem'] or '').replace('\n', ' ')[:150])
        print('     PDF :', (r['region'] or '')[:150])


if __name__ == '__main__':
    main()
