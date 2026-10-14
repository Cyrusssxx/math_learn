#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""搜「2017 第八届全国大学生数学竞赛」题：设 f(x,y) 可微，f'_x=f，lim[f(0,y+1/n)/f(0,y)]^n=e^{cot y}，f(0,π/2)=1，求 f(x,y)。
全源搜索（exam / core / bank / dgy），输出命中题的完整归属信息（catId / deepCats / source）。
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)

KEYS = ['第八届', '全国大学生数学竞赛', '竞赛', 'cot y', '\\cot y', 'coty', 'e^{\\cot']


def blob(q):
    return '\n'.join(str(q.get(k) or '') for k in ('stem', 'answer', 'idea', 'source', 'tips') if q.get(k) is not None)


def flat(q):
    """tips 是嵌套 dict，展开"""
    parts = [str(q.get(k) or '') for k in ('stem', 'answer', 'idea', 'source')]
    tips = q.get('tips')
    if isinstance(tips, dict):
        for v in tips.values():
            if isinstance(v, list):
                parts.extend(str(x) for x in v)
            elif v:
                parts.append(str(v))
    return '\n'.join(parts)


def hits(q):
    b = flat(q)
    return [k for k in KEYS if k in b]


def main():
    targets = []
    # exam
    ex = json.loads(io.open(P('exam.json'), encoding='utf-8').read())
    papers = ex if isinstance(ex, list) else ex.get('papers', [])
    for p in papers:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                h = hits(q)
                if h:
                    targets.append(('exam', '%s-%s' % (p['id'], q['no']), p.get('id'), q, h))
    # core
    core = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    for s in core[0]['sections']:
        for q in s.get('questions', []):
            h = hits(q)
            if h:
                targets.append(('core', 'core-%s' % q['no'], s.get('title'), q, h))
    # bank
    bk = json.loads(io.open(P('bank_questions.json'), encoding='utf-8').read())
    for it in bk.get('items', []):
        h = hits(it)
        if h:
            targets.append(('bank', 'bank-%s' % it.get('id'), it.get('catId'), it, h))
    # dgy
    dgy = json.loads(io.open(P('dgy_items.json'), encoding='utf-8').read())
    papers = dgy if isinstance(dgy, list) else dgy.get('papers', [])
    for p in papers:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                h = hits(q)
                if h:
                    targets.append(('dgy', '%s-%s' % (p['id'], q['no']), p.get('id'), q, h))

    print('命中 %d 条（关键词任一命中即算，需人工甄别）' % len(targets))
    for src, qid, where, q, h in targets:
        st = (q.get('stem') or '').replace('\n', ' ')
        # 只详列含「第八届/竞赛/cot」的
        strong = any(k in h for k in ('第八届', '全国大学生数学竞赛', 'cot y', 'coty', 'e^{\\cot'))
        mark = '★' if strong else ' '
        print('%s [%s] %s ｜分类=%s ｜命中=%s' % (mark, src, qid, where, h))
        print('     %s' % st[:90])
        if src == 'core':
            print('     catId=%s categoryIds=%s deepCats=%s' % (
                q.get('catId'), q.get('categoryIds'), q.get('deepCats')))
    print()
    strongN = sum(1 for *_ , h in [(a, b, c, d, e) for a, b, c, d, e in targets] if any(k in h for k in ('第八届', '全国大学生数学竞赛', 'cot y', 'coty', 'e^{\\cot')))
    print('强命中（确为竞赛题或含 cot y）：%d 条' % strongN)
    return 0


if __name__ == '__main__':
    sys.exit(main())
