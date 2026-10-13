#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""终版诊断：题源「章级确定」匹配。

思路：某题源（如 "2013数三"）在书签中可能出现在多处，但只要**所有出现的章相同**，
      那这道题属于哪一章就是**确定的**（无需知道具体页码）。
      这样能把可靠样本从 33（唯一题源）扩大到几百条，得出可信的错位率。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)
PDF = r'E:\Desktop\大观\【⚠️⚠️⚠️最重要】大观严选题\大观严选题（带答案）.pdf'

CH2SEC = {'A. 函数极限连续': '极限', 'B. 一元微分': '一元微分', 'C. 一元积分': '一元积分',
          'D. 多元微分': '多元微分', 'E. 二重积分': '二重积分', 'F. 微分方程': '微分方程',
          'G. 级数': '(G级数)'}


def norm_src(s):
    s = s or ''
    s = re.sub(r'^\(\d+\)\s*', '', s)
    s = re.sub(r'^[ivxIVX]+[).]\s*', '', s)
    s = re.sub(r'^\([a-z]\)\s*', '', s)
    s = re.sub(r'^[ⅠⅡⅢ]+\)\s*', '', s)
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
    key2ch = collections.defaultdict(set)
    for pg, ch, s in items:
        key2ch[s.split(';')[0]].add(ch)

    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    secs = cb[0]['sections']
    got_of = {}
    for s in secs:
        for q in s['questions']:
            got_of[q['no']] = s['title']
    qs = [q for s in secs for q in s['questions']]
    yan = sorted([q for q in qs if q['no'] <= 742], key=lambda x: x['no'])

    rows, amb = [], 0
    for q in yan:
        k = norm_src(q.get('source')).split(';')[0]
        chs = key2ch.get(k)
        if not chs:
            continue
        if len(chs) > 1:
            amb += 1
            continue
        ch = next(iter(chs))
        want = CH2SEC.get(ch)
        rows.append((q['no'], ch, want, got_of[q['no']], q))

    print('大观严选题区间 %d 题' % len(yan))
    print('  章级确定（题源所有候选同章）= %d' % len(rows))
    print('  题源跨章（无法判定，已跳过）= %d' % amb)
    print()
    mx = collections.defaultdict(collections.Counter)
    for no, ch, want, got, q in rows:
        mx[want][got] += 1
    titles = [s['title'] for s in secs]
    print('=== 混淆矩阵（行=按书应有章，列=现存节）===')
    print('%-12s %s' % ('应有\\现存', ''.join('%-9s' % t[:8] for t in titles)))
    for ch in list(CH2SEC.values()):
        r = mx.get(ch)
        if not r:
            continue
        print('%-12s %s' % (ch, ''.join('%-9s' % (r.get(t, '·')) for t in titles)))
    tot = len(rows)
    ok = sum(n for ch, r in mx.items() for t, n in r.items() if ch == t)
    g = sum(mx.get('(G级数)', {}).values())
    print()
    print('✅ 一致 = %d（%.0f%%）' % (ok, 100.0 * ok / tot))
    print('❌ 错位 = %d（%.0f%%）' % (tot - ok - g, 100.0 * (tot - ok - g) / tot))
    print('⓿ 应在 G 级数 = %d' % g)
    print()
    # 相邻章 vs 跨章
    ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程']
    adj = far = 0
    for no, ch, want, got, q in rows:
        if want == got or want is None or want not in ORDER or got not in ORDER:
            continue
        if abs(ORDER.index(want) - ORDER.index(got)) == 1:
            adj += 1
        else:
            far += 1
    print('错位细分：相邻章之间 = %d，跨章（跳章）= %d' % (adj, far))
    print()
    print('=== 跨章错位清单（最需修，前 25）===')
    n = 0
    for no, ch, want, got, q in rows:
        if want == got or want not in ORDER or got not in ORDER:
            continue
        if abs(ORDER.index(want) - ORDER.index(got)) <= 1:
            continue
        n += 1
        if n <= 25:
            print('  no=%-5s 书=%-8s 现=%-8s %s' % (no, want, got, (q.get('stem') or '').replace('\n', ' ')[:52]))
    print('   …共 %d 道' % n)
    io.open(os.path.join(ROOT, 'tools/_order_diag3.json'), 'w', encoding='utf-8').write(
        json.dumps([[no, want, got] for no, ch, want, got, q in rows], ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
