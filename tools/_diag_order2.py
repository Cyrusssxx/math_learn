#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""核心题库目录诊断（终版）：迭代式锚点扩充 + 章边界反推。

已知：no 是「大观严选题」的书序（唯一题源检验 97% 单调）。
做法：
  1) 用「题源在书签中唯一」的题做种子锚点（匹配必对）
  2) 线性拟合 no → 页，得到初始章边界
  3) 对每道题，在其题源的所有候选书签条目里选「章与当前估计相符」的那个 → 扩充锚点
  4) 迭代收敛后输出：no 的章边界、每题应有章、与现存节的错位清单
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)
PDF = r'E:\Desktop\大观\【⚠️⚠️⚠️最重要】大观严选题\大观严选题（带答案）.pdf'

CH2SEC = {'A. 函数极限连续': '极限', 'B. 一元微分': '一元微分', 'C. 一元积分': '一元积分',
          'D. 多元微分': '多元微分', 'E. 二重积分': '二重积分', 'F. 微分方程': '微分方程',
          'G. 级数': '(G级数·数二不考)'}
CHAPTERS = [(1, 75, 'A. 函数极限连续'), (76, 163, 'B. 一元微分'), (164, 264, 'C. 一元积分'),
            (265, 319, 'D. 多元微分'), (320, 360, 'E. 二重积分'), (361, 439, 'F. 微分方程'),
            (440, 536, 'G. 级数')]


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


def ch_of(pg):
    for a, b, c in CHAPTERS:
        if a <= pg <= b:
            return c
    return None


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

    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    secs = cb[0]['sections']
    qs = [q for s in secs for q in s['questions']]
    got_of = {}
    for s in secs:
        for q in s['questions']:
            got_of[q['no']] = s['title']
    yan = sorted([q for q in qs if q['no'] <= 742], key=lambda x: x['no'])

    # 种子锚点
    anchor = {}
    for q in yan:
        k = norm_src(q.get('source')).split(';')[0]
        if k in uniq:
            anchor[q['no']] = items[uniq[k]][0]
    print('种子锚点 = %d 个' % len(anchor))

    # 迭代
    for it in range(6):
        if len(anchor) >= 2:
            ks = sorted(anchor)
            # 用「页码/题号」比值的中位数做尺度（近似线性）
            ratios = [anchor[k] / k for k in ks if k > 20]
            scale = sorted(ratios)[len(ratios) // 2] if ratios else 0.884
        else:
            scale = 0.884
        added = 0
        for q in yan:
            if q['no'] in anchor:
                continue
            k = norm_src(q.get('source')).split(';')[0]
            cands = idx.get(k)
            if not cands:
                continue
            est = q['no'] * scale
            # 选页码最接近估计值的候选（允许 ±60 页容差）
            best = min(cands, key=lambda i: abs(items[i][0] - est))
            if abs(items[best][0] - est) <= 60:
                anchor[q['no']] = items[best][0]
                added += 1
        print('  迭代 %d：新增 %d，累计 %d' % (it + 1, added, len(anchor)))
        if added == 0:
            break
    print()

    # 输出：每题的应有章 vs 现存节
    rows = []
    for q in yan:
        if q['no'] not in anchor:
            continue
        pg = anchor[q['no']]
        ch = ch_of(pg)
        rows.append((q['no'], pg, ch, CH2SEC.get(ch), got_of[q['no']], q))
    print('可判定题数 = %d / %d' % (len(rows), len(yan)))
    mx = collections.defaultdict(collections.Counter)
    for no, pg, ch, want, got, q in rows:
        mx[want][got] += 1
    titles = [s['title'] for s in secs]
    print()
    print('=== 混淆矩阵（行=按书应有的章，列=现存节）===')
    print('%-18s %s' % ('应有 \\ 现存', ''.join('%-10s' % t[:9] for t in titles)))
    for ch in [v for v in CH2SEC.values()] + ['(G级数·数二不考)']:
        r = mx.get(ch, {})
        if not r:
            continue
        print('%-18s %s' % (ch, ''.join('%-10s' % (r.get(t, '·')) for t in titles)))
    print()
    tot = len(rows)
    okn = sum(n for ch, r in mx.items() for t, n in r.items() if ch == t)
    gone = sum(mx.get('(G级数·数二不考)', {}).values())
    print('✅ 归属一致 = %d（%.0f%%）' % (okn, 100.0 * okn / tot))
    print('❌ 归属错位 = %d（%.0f%%）' % (tot - okn - gone, 100.0 * (tot - okn - gone) / tot))
    print('⓿ 落在 G 级数章（数二不考）= %d' % gone)
    print()
    # 错位明细
    bad = [(no, pg, want, got, q) for no, pg, ch, want, got, q in rows if want and got and want != got]
    print('=== 错位明细（前 30 / 共 %d）===' % len(bad))
    for no, pg, want, got, q in bad[:30]:
        print('  no=%-5s p%-4s 应=%-10s 现=%-10s %s' % (
            no, pg, want, got, (q.get('stem') or '').replace('\n', ' ')[:44]))
    gs = [(no, pg, q) for no, pg, ch, want, got, q in rows if want == '(G级数·数二不考)']
    if gs:
        print()
        print('=== 落在 G 级数章的题（前 20 / 共 %d）===' % len(gs))
        for no, pg, q in gs[:20]:
            print('  no=%-5s p%-4s 现存=%-8s %s' % (no, pg, got_of[no], (q.get('stem') or '').replace('\n', ' ')[:44]))
    io.open(os.path.join(ROOT, 'tools/_order_diag2.json'), 'w', encoding='utf-8').write(
        json.dumps({'anchor': anchor,
                    'rows': [[no, pg, want, got] for no, pg, ch, want, got, q in rows]},
                   ensure_ascii=False, indent=1))
    print()
    print('已写 tools/_order_diag2.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
