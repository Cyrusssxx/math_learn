#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""问题②分析：25 组 linkedQid 共用 → 判定「真同题(保留)」还是「错误关联(清除)」；
并对有用户标记的 7 组，算「组内哪道题与真题题最像」以决定标记迁移目标。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def norm(s):
    s = s or ''
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    s = re.sub(r'（\s*）|\(\s*\)|_{2,}', '', s)
    return s


def bg(s):
    return set(s[i:i + 2] for i in range(len(s) - 1)) if len(s) > 1 else {s}


def jac(a, b):
    A, B = bg(a), bg(b)
    return len(A & B) / len(A | B) if (A and B) else 0.0


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    e = ann['exam']
    marked = set(json.loads(e['favs']).keys()) | set(json.loads(e['status']).keys()) | set(
        k.replace('examNote-', '') for k in e['notes'])
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = q

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    g = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            g[q['linkedQid']].append(q)
    multi = {k: v for k, v in g.items() if len(v) > 1}

    keep_link, clear_link = [], []
    for k, v in multi.items():
        same = []
        norms = collections.Counter(norm(q['stem']) for q in v)
        for q in v:
            if norms[norm(q['stem'])] > 1:
                same.append(q['no'])
        if same:
            keep_link.append((k, sorted(same)))
        clear_link.append((k, [q['no'] for q in v if q['no'] not in same]))

    total_clear = sum(len(x[1]) for x in clear_link)
    print('=== 真同题（题干相同，保留 linkedQid）===')
    for k, ns in keep_link:
        print('  %-22s no=%s' % (k, ns))
    print()
    print('=== 错误关联（题干不同，清除 linkedQid）===')
    print('组数 =', len(clear_link), ' 涉及题数 =', total_clear)
    print()
    print('=== 有用户标记的组：算「哪道与真题题最像」===')
    for k, v in sorted(multi.items(), key=lambda x: -len(x[1])):
        if k not in marked:
            continue
        z = zp.get(k)
        kinds = []
        if k in json.loads(e['favs']): kinds.append('收藏')
        if k in json.loads(e['status']): kinds.append('状态=' + json.loads(e['status'])[k])
        if k in e['notes']: kinds.append('笔记')
        print()
        print('【%s】%d 道题共用 · 你的标记: %s' % (k, len(v), '+'.join(kinds)))
        if z:
            print('   真题题(%s): %s' % (k, (z.get('stem') or '').replace('\n', ' ')[:88]))
        for q in v:
            sc = jac(norm(q.get('stem')), norm(z.get('stem'))) if z else 0
            tag = ' ★最像' if sc >= 0.6 else ''
            print('   no=%-5s 相似=%.2f%s  %s' % (q['no'], sc, tag, (q.get('stem') or '').replace('\n', ' ')[:70]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
