#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""干净检验：只用「在书签中唯一出现」的题源做 no → 页 映射，判断 no 是否单调（= 是否书序）。
唯一题源的匹配必然正确，可排除重复候选造成的噪声。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)
PDF = r'E:\Desktop\大观\【⚠️⚠️⚠️最重要】大观严选题\大观严选题（带答案）.pdf'


def norm_src(s):
    s = s or ''
    s = re.sub(r'^\(\d+\)\s*', '', s)
    s = re.sub(r'^[ivxIVX]+[).]\s*', '', s)
    s = re.sub(r'^\([a-z]\)\s*', '', s)
    for e in ('🖐️', '🖐', '✋', '♣'):
        s = s.replace(e, '')
    s = s.replace('；', ';').replace('，', ',').replace('＋', '+')
    s = re.sub(r'\s+', '', s)
    return s.replace('>>', '').strip(' ;,.')


def main():
    import pymupdf
    d = pymupdf.open(PDF)
    toc = d.get_toc(simple=True)
    items, cur = [], None
    for l, t, pg in toc:
        if l == 2:
            cur = t.replace('>>', '').strip()
        elif l >= 5 and cur:
            items.append((pg, cur, norm_src(t)))
    idx = collections.defaultdict(list)
    for i, (pg, ch, s) in enumerate(items):
        idx[s.split(';')[0]].append(i)
    uniq = {k: v[0] for k, v in idx.items() if len(v) == 1}
    print('书签题目条目 %d；题源唯一者 %d 个' % (len(items), len(uniq)))
    print()

    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    yan = sorted([q for q in qs if q['no'] <= 742], key=lambda x: x['no'])

    pairs = []
    for q in yan:
        k = norm_src(q.get('source')).split(';')[0]
        if k in uniq:
            i = uniq[k]
            pairs.append((q['no'], items[i][0], items[i][1], k, q))
    print('唯一命中 = %d 题' % len(pairs))
    print()
    # 单调性
    inv = [(a, b) for a, b in zip(pairs, pairs[1:]) if b[1] < a[1]]
    print('页码逆序次数 = %d / %d 次相邻比较（%.0f%% 单调）' % (
        len(inv), max(1, len(pairs) - 1), 100.0 * (len(pairs) - 1 - len(inv)) / max(1, len(pairs) - 1)))
    print()
    if inv:
        print('=== 逆序样本（前 12）===')
        for a, b in inv[:12]:
            print('   no=%s→p%s  然后 no=%s→p%s' % (a[0], a[1], b[0], b[1]))
    print()
    # 按书的章统计这些题「当前所在节」
    print('=== 唯一命中题的「书章 → 现存节」混淆矩阵 ===')
    mx = collections.defaultdict(collections.Counter)
    CH2SEC = {'A. 函数极限连续': '极限', 'B. 一元微分': '一元微分', 'C. 一元积分': '一元积分',
              'D. 多元微分': '多元微分', 'E. 二重积分': '二重积分', 'F. 微分方程': '微分方程',
              'G. 级数': '(数二不考)'}
    for no, pg, ch, k, q in pairs:
        got = next(s['title'] for s in cb[0]['sections'] if q in s['questions'])
        mx[CH2SEC.get(ch, ch)][got] += 1
    secs = [s['title'] for s in cb[0]['sections']]
    print('%-12s %s' % ('书章\\现存', ''.join('%-9s' % x[:8] for x in secs)))
    for ch in ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程', '(数二不考)']:
        row = mx.get(ch, {})
        if not row:
            continue
        print('%-12s %s' % (ch, ''.join('%-9s' % (row.get(s, '·')) for s in secs)))
    print()
    ok = sum(n for ch, r in mx.items() for s, n in r.items() if ch == s)
    tot = sum(sum(r.values()) for r in mx.values())
    print('书章与现存节一致 = %d / %d = %.0f%%' % (ok, tot, 100.0 * ok / max(1, tot)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
