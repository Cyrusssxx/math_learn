#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""核心题库「目录顺序」诊断（2026-10-13 用户问：核心题库的目录顺序是不是有问题）。

方法：用大观严选题 PDF 的**书签**（1264 条，含页码与题源标注）作为「书的真值顺序」，
      把 core_bank 的题按 no 顺序与书签题目序列做**双向匹配**，得出：
        1) no 是否就是书序（匹配率）
        2) 每道题在书里的页码 → 所属章（A~F，G 级数丢掉）→ 应有节
        3) 与当前所属节对比 → 错位清单
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)

PDF = r'E:\Desktop\大观\【⚠️⚠️⚠️最重要】大观严选题\大观严选题（带答案）.pdf'

# 书签 L2 章 → core_bank 的节名（G 级数丢掉）
CH2SEC = {
    'A. 函数极限连续': '极限',
    'B. 一元微分': '一元微分',
    'C. 一元积分': '一元积分',
    'D. 多元微分': '多元微分',
    'E. 二重积分': '二重积分',
    'F. 微分方程': '微分方程',
    'G. 级数': None,          # 数二不考 → 丢弃
}


def norm_src(s):
    """归一化题源标注：统一分号/去 emoji/去题号前缀/去空格"""
    s = s or ''
    s = re.sub(r'^\(\d+\)\s*', '', s)          # (1) 前缀
    s = re.sub(r'^[ivxIVX]+[).]\s*', '', s)     # i) 前缀
    s = re.sub(r'^\([a-z]\)\s*', '', s)         # (a) 前缀
    s = s.replace('🖐️', '').replace('🖐', '').replace('✋', '')
    s = s.replace('；', ';').replace('，', ',').replace('＋', '+')
    s = re.sub(r'\s+', '', s)
    s = s.replace('>>', '')
    return s.strip(' ;,.')


def key_of_src(s):
    """取题源的主键：第一个分号前的片段"""
    return norm_src(s).split(';')[0]


def main():
    import pymupdf
    d = pymupdf.open(PDF)
    toc = d.get_toc(simple=True)
    # 只保留 L5+ 的题目条目（L4 及以前是知识点标题）
    items = []           # (页码, 章, 题源标注)
    cur_ch = None
    for l, t, pg in toc:
        if l == 2:
            cur_ch = t.replace('>>', '').strip()      # ⚠️ 书签章名带 ' >>' 后缀，必须剥
            continue
        if l >= 5 and cur_ch:
            items.append((pg, cur_ch, t.strip()))
    print('书签题目条目 = %d 条（L5+）' % len(items))
    ch_cnt = collections.Counter(c for _, c, _ in items)
    for c, n in ch_cnt.items():
        print('   %-22s %d 条' % (c, n))
    print()

    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    loc = {}
    for s in cb[0]['sections']:
        for q in s['questions']:
            loc[q['no']] = s['title']

    # 建索引：题源主键 → [(页, 章, 原文)]
    idx = collections.defaultdict(list)
    for pg, ch, t in items:
        idx[key_of_src(t)].append((pg, ch, t))

    yan = [q for q in qs if q['no'] <= 742]      # 大观严选题区间（743+ 是线代 xd）
    hit = miss = 0
    rows = []
    last_pg = 0
    for q in sorted(yan, key=lambda x: x['no']):
        k = key_of_src(q.get('source'))
        if not k:
            miss += 1
            continue
        cands = idx.get(k)
        if not cands:
            miss += 1
            continue
        # 同一题源可能出现多次（书里重复收录）→ 取「页码 >= 上一题页码」的最早候选，
        # 借助 no 递增（书序）做贪心对齐，避免匹配到书后段的同源题。
        pick = None
        for pg, ch, raw in cands:
            if pg >= last_pg:
                pick = (pg, ch, raw)
                break
        if pick is None:
            pick = cands[-1]
        hit += 1
        pg, ch, raw = pick
        last_pg = pg
        want = CH2SEC.get(ch)
        got = loc[q['no']]
        rows.append((q['no'], pg, ch, want, got, (q.get('source') or '')[:26], (q.get('stem') or '').replace('\n', ' ')[:34]))

    print('=== 匹配结果 ===')
    print('大观严选题区间（no<=742）= %d 题，题源能在书签里找到 = %d（%.0f%%），找不到 = %d'
          % (len(yan), hit, 100.0 * hit / max(1, len(yan)), miss))
    print()
    bad = [r for r in rows if r[3] and r[3] != r[4]]
    okc = [r for r in rows if r[3] and r[3] == r[4]]
    gone = [r for r in rows if r[3] is None]
    print('  ✅ 节归属正确 = %d' % len(okc))
    print('  ❌ 节归属错位 = %d' % len(bad))
    print('  ⓿ 落在 G 级数章（数二不考，本不该收）= %d' % len(gone))
    print()
    if bad:
        print('=== 错位清单（前 40）===')
        print('%-6s %-5s %-16s %-10s %-10s %s' % ('no', '页', '书章', '应有节', '现存节', '题目'))
        for no, pg, ch, want, got, src, stem in bad[:40]:
            print('%-6s %-5s %-16s %-10s %-10s %s' % (no, pg, ch[:16], want, got, stem))
        print('   …共 %d 处' % len(bad))
    if gone:
        print()
        print('=== 落在 G 级数章的题（前 20）===')
        for no, pg, ch, want, got, src, stem in gone[:20]:
            print('   no=%-5s p%-4s 现存节=%-8s %s' % (no, pg, got, stem))

    io.open(os.path.join(ROOT, 'tools/_order_diag.json'), 'w', encoding='utf-8').write(
        json.dumps({'ok': len(okc), 'bad': bad, 'gone': gone}, ensure_ascii=False, indent=1))
    print()
    print('明细已写 tools/_order_diag.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
