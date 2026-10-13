#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""对「被保守规则跳过」的题做题源二次裁决：
   查其题源在书签中的所有候选章，若多数章 == DP 的 want → 判定为真错位，可改；
   否则保持不动（疑 DP 误判）。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)
PDF = r'E:\Desktop\大观\【⚠️⚠️⚠️最重要】大观严选题\大观严选题（带答案）.pdf'
ORDER = ['极限', '一元微分', '一元积分', '多元微分', '二重积分', '微分方程']
CH2SEC = {'A. 函数极限连续': '极限', 'B. 一元微分': '一元微分', 'C. 一元积分': '一元积分',
          'D. 多元微分': '多元微分', 'E. 二重积分': '二重积分', 'F. 微分方程': '微分方程'}


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
            items.append((pg, CH2SEC.get(cur), norm_src(t)))
    key2secs = collections.defaultdict(collections.Counter)
    for pg, sec, s in items:
        if sec:
            key2secs[s.split(';')[0]][sec] += 1

    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    loc, byno = {}, {}
    for s in cb[0]['sections']:
        for q in s['questions']:
            loc[q['no']] = s['title']
            byno[q['no']] = q
    plan = json.loads(io.open(os.path.join(ROOT, 'tools/_resec_plan.json'), encoding='utf-8').read())
    sec_of = {int(k): v for k, v in plan['plan'].items()}

    # 找出「DP 想改但当前仍不一致」的题（即被保守规则跳过的）
    pend = []
    for n in sorted(sec_of):
        if n not in loc:
            continue
        want, got = sec_of[n], loc[n]
        if want != got:
            pend.append((n, got, want, byno[n]))

    print('待裁决（DP 想改、当前未改）= %d 道' % len(pend))
    print()
    conf, doubt = [], []
    for n, got, want, q in pend:
        k = norm_src(q.get('source')).split(';')[0]
        c = key2secs.get(k)
        if not c:
            doubt.append((n, got, want, '无候选', q))
            continue
        top, topn = c.most_common(1)[0]
        tot = sum(c.values())
        ratio = topn / tot
        if top == want and ratio >= 0.6:
            conf.append((n, got, want, '%s %d/%d=%.0f%%' % (top, topn, tot, ratio * 100), q))
        else:
            doubt.append((n, got, want, '候选偏 %s %d/%d' % (top, topn, tot), q))

    print('=== 题源支持 DP 判断（可改）= %d 道 ===' % len(conf))
    for n, got, want, ev, q in conf:
        print('   no=%-4s %-10s→%-10s [%s] %s' % (n, got, want, ev, (q.get('stem') or '').replace('\n', ' ')[:46]))
    print()
    print('=== 题源不支持（保持不动）= %d 道 ===' % len(doubt))
    for n, got, want, ev, q in doubt[:20]:
        print('   no=%-4s 保持 %-10s (DP想 %-10s) [%s] %s' % (
            n, got, want, ev, (q.get('stem') or '').replace('\n', ' ')[:42]))
    out = {'confirmed': [[n, got, want] for n, got, want, ev, q in conf]}
    io.open(os.path.join(ROOT, 'tools/_resec_confirmed.json'), 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print()
    print('已写 tools/_resec_confirmed.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
