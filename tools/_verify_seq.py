#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""验证 core_bank 的 no 是否就是「大观严选题」的书序。
方法：把每题的题源标注与书签题目条目做「单调匹配」（页码必须单调不减），
      统计单调命中率与逆序次数。若几乎全单调 → no 即书序。
另：对「落在 G 级数章」的题做人工复核清单（那是最关键的结论）。
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
    s = re.sub(r'^[ⅠⅡⅢ]+\)\s*', '', s)
    for e in ('🖐️', '🖐', '✋', '♣'):
        s = s.replace(e, '')
    s = s.replace('；', ';').replace('，', ',').replace('＋', '+')
    s = re.sub(r'\s+', '', s)
    s = s.replace('>>', '')
    return s.strip(' ;,.')


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
    # 建：题源主键 -> 该书签条目在 items 中的下标
    idx = collections.defaultdict(list)
    for i, (pg, ch, s) in enumerate(items):
        idx[s.split(';')[0]].append(i)

    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    yan = sorted([q for q in qs if q['no'] <= 742], key=lambda x: x['no'])

    # 单调匹配：用 item 下标做指针，只往后走
    ptr = 0
    mono = back = nomatch = 0
    seg = []
    for q in yan:
        k = norm_src(q.get('source')).split(';')[0]
        cands = [i for i in idx.get(k, []) if i >= ptr]
        if not cands:
            # 允许回退一次（书里同源题可能被重复收录）
            allc = idx.get(k, [])
            if allc:
                back += 1
                i = allc[-1]
            else:
                nomatch += 1
                continue
        else:
            i = cands[0]
            mono += 1
        ptr = max(ptr, i)
        seg.append((q['no'], items[i][0], items[i][1]))

    print('大观严选题区间 %d 题：单调命中 %d，回退 %d，无匹配 %d' % (
        len(yan), mono, back, nomatch))
    print('  单调命中率 = %.0f%%' % (100.0 * mono / len(yan)))
    print()
    # 记录 no -> 页 的映射，检查是否单调
    pg_seq = [(no, pg) for no, pg, ch in seg]
    inv = sum(1 for a, b in zip(pg_seq, pg_seq[1:]) if b[1] < a[1])
    print('页码序列逆序次数 = %d' % inv)
    print()
    # 每章对应多少题
    ch_cnt = collections.Counter(ch for _, _, ch in seg)
    print('=== 按书签章统计（匹配到的题）===')
    for c, n in ch_cnt.most_common():
        print('   %-22s %d 题' % (c, n))
    print()
    # G 级数章的题（最需要复核）
    gone = [(no, pg, q) for (no, pg, ch), q in zip(seg, [x for x in yan]) if ch.startswith('G')]
    real_gone = []
    for no, pg, ch in seg:
        if ch.startswith('G'):
            real_gone.append((no, pg))
    print('=== 匹配到 G 级数章的题（%d 道）===' % len(real_gone))
    byno = {q['no']: q for q in qs}
    for no, pg in real_gone[:30]:
        q = byno[no]
        print('   no=%-5s p%-4s src=%-24s %s' % (
            no, pg, (q.get('source') or '')[:24], (q.get('stem') or '').replace('\n', ' ')[:46]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
