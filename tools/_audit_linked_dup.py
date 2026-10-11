#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""量化 linkedQid 重复共用的影响面：
  1. 有多少组「多题链同一 linkedQid」；每组里是否真的是同一道题（题干相同）
  2. 这些题经 qidOf 重定向后会共享同一主键 → 收藏/标记/笔记互相覆盖
  3. 用户标记里有多少落在这些冲突主键上
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def norm(s):
    s = re.sub(r'\s+', '', s or '')
    return re.sub(r'\\underline\{\\hspace\{[^}]*\}\}', '', s)


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    ex = ann['exam']
    fav = set(json.loads(ex['favs']).keys())
    st = set(json.loads(ex['status']).keys())
    nt = set(k.replace('examNote-', '') for k in ex['notes'])
    marked = fav | st | nt

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    groups = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            groups[q['linkedQid']].append(q)

    multi = {k: v for k, v in groups.items() if len(v) > 1}
    print('=== linkedQid 重复共用 ===')
    print('不同 linkedQid 总数 =', len(groups))
    print('被多题共用的组数 =', len(multi), ' 涉及题目 =', sum(len(v) for v in multi.values()))
    print()
    same_stem, diff_stem = 0, 0
    conflict_keys = []
    for k, v in sorted(multi.items(), key=lambda x: -len(x[1])):
        norms = collections.Counter(norm(q.get('stem')) for q in v)
        dup = sum(n - 1 for n in norms.values() if n > 1)
        same_stem += dup
        diff_stem += (len(v) - dup)
        conflict_keys.append(k)
    print('这些组里：题干真正相同的重复 =', same_stem, ' 题干不同却共用同一主键 =', diff_stem)
    print()
    print('=== 主键冲突明细（前 10 组）===')
    for k, v in sorted(multi.items(), key=lambda x: -len(x[1]))[:10]:
        norms = collections.Counter(norm(q.get('stem')) for q in v)
        uniq = len(norms)
        hit = k in marked
        print('  %-22s %2d 道题 / %2d 个不同题干   用户在此主键上有标记=%s' % (k, len(v), uniq, hit))
    print()
    print('=== 影响面 ===')
    print('用户标记落在「冲突主键」上的条数 =', sum(1 for k in conflict_keys if k in marked))
    print('（这些标记会同时作用于该组内所有题 → 出现「没做过的题显示已收藏/不熟」）')
    # 举例：2002数二真题-4 这组
    g = groups.get('2002数二真题-4', [])
    print()
    print('=== 样例：2002数二真题-4 组（%d 道）===' % len(g))
    for q in g[:6]:
        print('  no=%-5s %s' % (q['no'], (q.get('stem') or '')[:64].replace('\n', ' ')))
    print('  ...')
    return 0


if __name__ == '__main__':
    sys.exit(main())
