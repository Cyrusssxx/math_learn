#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""对「节归属错位」的题，输出其在书签中的**完整层级路径**（章 > 知识点 > 子知识点 > 题目），
用于人工判定错位真伪——避免只靠页码落在哪一章带来的边界噪声。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)
PDF = r'E:\Desktop\大观\【⚠️⚠️⚠️最重要】大观严选题\大观严选题（带答案）.pdf'
DIAG = os.path.join(ROOT, 'tools/_order_diag2.json')


def main():
    import pymupdf
    d = pymupdf.open(PDF)
    toc = d.get_toc(simple=True)
    # 构建「页码 → 该页所属的完整路径」（取该页最后一个 L<=4 标题）
    path_of_page = {}
    stack = {}
    for l, t, pg in toc:
        t2 = t.replace('>>', '').strip()
        if l <= 4:
            stack[l] = t2
            for k in list(stack):
                if k > l:
                    del stack[k]
            path_of_page[pg] = ' > '.join(stack[k] for k in sorted(stack))
    # 题目条目：页码 → (路径, 原文)
    item_path = []
    cur = {}
    for l, t, pg in toc:
        t2 = t.replace('>>', '').strip()
        if l <= 4:
            cur[l] = t2
            for k in list(cur):
                if k > l:
                    del cur[k]
        else:
            item_path.append((pg, ' > '.join(cur[k] for k in sorted(cur)), t2))

    diag = json.loads(io.open(DIAG, encoding='utf-8').read())
    rows = diag['rows']            # [no, pg, want, got]
    cb = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    byno = {}
    for s in cb[0]['sections']:
        for q in s['questions']:
            byno[q['no']] = q

    bad = [r for r in rows if r[2] and r[3] and r[2] != r[3]]
    print('错位题 = %d 道，按「现存节」分组列出完整书目路径' % len(bad))
    print()
    g = collections.defaultdict(list)
    for no, pg, want, got in bad:
        g[got].append((no, pg, want))
    for got in sorted(g, key=lambda k: -len(g[k])):
        print('■ 现存节【%s】共 %d 道' % (got, len(g[got])))
        for no, pg, want in g[got][:12]:
            # 找该页附近的题目条目
            cand = [x for x in item_path if abs(x[0] - pg) <= 1]
            pth = cand[0][1] if cand else '(未找到)'
            q = byno.get(no)
            print('   no=%-5s p%-4s 应为【%s】' % (no, pg, want))
            print('        书路径: %s' % pth)
            print('        题干  : %s' % (q.get('stem') or '').replace('\n', ' ')[:70])
        if len(g[got]) > 12:
            print('   …另 %d 道' % (len(g[got]) - 12))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
