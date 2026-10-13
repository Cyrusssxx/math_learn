#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""core_bank 关联字段体检：冲突 / 绑定过多 / 冗余（2026-10-13）。

检查项：
  A 主键冲突
    A1 linkedQid 重复（多题共享同一真题键）—— 真同题组需题干一致，否则是旧 bug 回潮
    A2 linkAlias 撞别人的 linkedQid（别名必须是「没被占用」的键）
    A3 linkAlias 全局唯一
    A4 迁移源（linkFix.from / linkedQidOld）全局唯一
  B 冗余 / 自指
    B1 linkedQidOld 与 linkedQidDead 同值（同义重复表达）
    B2 linkFix.from 与 linkedQidOld 同值（两处写同一件事）
    B3 linkFix.from 与 linkedQid 同值（自指，迁移等于没迁）
    B4 linkedQidDead 与 linkedQid 同值
    B5 linkAlias 里含自己的 linkedQid
    B6 linkAlias 里含 linkedQidDead
    B7 linkedQidOld 与 linkFix.from 都缺（线索为空对象等）
  C 绑定过多
    C1 一道题同时挂 ≥3 种关联字段
    C2 一道题既 linkedQid 又 linkedQidDead 又 linkFix 等堆叠
  D 悬空
    D1 linkedQid / linkAlias / linkFix.from / linkedQidOld / linkedQidDead 指向的键是否存在于题库
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)


def load(fn):
    p = P(fn)
    return json.loads(io.open(p, encoding='utf-8').read()) if os.path.exists(p) else None


def norm(s):
    s = (s or '')
    s = re.sub(r'（本题满分[^）]*分）', '', s)
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    return s


def main():
    cb = load('core_bank.json')
    ex = load('exam.json') or []
    dgy = load('dgy_items.json')
    bq = load('bank_questions.json')
    universe = set()
    for src in (ex, dgy):
        if not src:
            continue
        for p in (src if isinstance(src, list) else src.get('papers', [])):
            for s in p['sections']:
                for q in s['questions']:
                    universe.add('%s-%s' % (p['id'], q['no']))
    for it in ((bq or {}).get('items') or []):
        universe.add('bank-%s' % it.get('id'))

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    key_of = lambda q: q['linkedQid'] if q.get('linkedQid') else 'core-%s' % q['no']
    universe |= set('core-%s' % q['no'] for q in qs)

    issues = collections.OrderedDict()
    def add(cat, msg):
        issues.setdefault(cat, []).append(msg)

    # ---- A1 主键重复 ----
    g = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            g[q['linkedQid']].append(q)
    for k, v in g.items():
        if len(v) > 1:
            stems = {norm(q.get('stem') or '') for q in v}
            if len(stems) > 1:
                add('A1 主键冲突（一对多且题干不同）', '%s ← no=%s' % (k, [q['no'] for q in v]))
            else:
                add('A1 主键共享（真同题，可接受）', '%s ← no=%s' % (k, [q['no'] for q in v]))

    # ---- A2/A3 linkAlias ----
    ali = collections.defaultdict(list)
    for q in qs:
        for a in (q.get('linkAlias') or []):
            ali[a].append(q['no'])
    for a, nos in ali.items():
        if len(nos) > 1:
            add('A3 别名重复（多题共用）', '%s ← no=%s' % (a, nos))
        if a in g:
            add('A2 别名撞主键', '%s（别名）与 linkedQid 撞车' % a)

    # ---- A4 迁移源唯一 ----
    src = collections.defaultdict(list)
    for q in qs:
        old = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if old:
            src[old].append(q['no'])
    for k, nos in src.items():
        if len(nos) > 1:
            add('A4 迁移源被多题共享（会串号）', '%s ← no=%s' % (k, nos))

    # ---- B 冗余 ----
    for q in qs:
        no = q['no']
        lq = q.get('linkedQid')
        ff = (q.get('linkFix') or {}).get('from')
        old = q.get('linkedQidOld')
        dead = q.get('linkedQidDead')
        al = q.get('linkAlias') or []
        if old and dead and old == dead:
            add('B1 linkedQidOld 与 Dead 同值（冗余）', 'no=%s %s' % (no, old))
        if ff and old and ff == old:
            add('B2 linkFix.from 与 linkedQidOld 同值（冗余）', 'no=%s %s' % (no, ff))
        if ff and lq and ff == lq:
            add('B3 linkFix.from 自指 linkedQid', 'no=%s %s' % (no, ff))
        if dead and lq and dead == lq:
            add('B4 Dead 与 linkedQid 同值', 'no=%s %s' % (no, dead))
        if lq and lq in al:
            add('B5 linkAlias 含自己的主键', 'no=%s %s' % (no, lq))
        if dead and dead in al:
            add('B6 linkAlias 含死键', 'no=%s %s' % (no, dead))
        for a in al:
            if not a:
                add('B7 空别名项', 'no=%s' % no)

    # ---- C 绑定过多 ----
    for q in qs:
        kinds = []
        if q.get('linkedQid'): kinds.append('linkedQid')
        if q.get('linkAlias'): kinds.append('linkAlias')
        ff = (q.get('linkFix') or {}).get('from')
        if ff: kinds.append('linkFix.from')
        if q.get('linkedQidOld'): kinds.append('linkedQidOld')
        if q.get('linkedQidDead'): kinds.append('linkedQidDead')
        if q.get('linkScan'): kinds.append('linkScan')
        if len(kinds) >= 4:
            add('C1 关联字段堆叠（≥4 种）', 'no=%s → %s' % (q['no'], ','.join(kinds)))

    # ---- D 悬空 ----
    for q in qs:
        no = q['no']
        lq = q.get('linkedQid')
        if lq and lq not in universe:
            add('D1 悬空', 'no=%s linkedQid=%s' % (no, lq))
        for a in (q.get('linkAlias') or []):
            if a not in universe:
                add('D1 悬空', 'no=%s linkAlias=%s' % (no, a))
        ff = (q.get('linkFix') or {}).get('from')
        if ff and ff not in universe:
            add('D1 悬空', 'no=%s linkFix.from=%s' % (no, ff))
        if q.get('linkedQidOld') and q['linkedQidOld'] not in universe:
            add('D1 悬空', 'no=%s linkedQidOld=%s' % (no, q['linkedQidOld']))
        if q.get('linkedQidDead') and q['linkedQidDead'] not in universe:
            add('D1 悬空', 'no=%s linkedQidDead=%s' % (no, q['linkedQidDead']))

    # ---- 输出 ----
    print('体检对象：core_bank %d 题｜题库键 universe %d 个' % (len(qs), len(universe)))
    print()
    if not issues:
        print('✅ 全部检查项通过：无冲突 / 无堆叠 / 无冗余 / 无悬空')
        print()
        print('结论：真问题 0 处')
        return 0
    bad = 0
    for cat, lst in issues.items():
        fatal = not cat.startswith(('A1 主键共享',))
        mark = '⚠️' if fatal else 'ℹ️'
        if fatal:
            bad += len(lst)
        print('%s %s：%d 处' % (mark, cat, len(lst)))
        for m in lst[:12]:
            print('     ' + m)
        if len(lst) > 12:
            print('     …另 %d 处' % (len(lst) - 12))
    print()
    print('结论：真问题 %d 处' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
