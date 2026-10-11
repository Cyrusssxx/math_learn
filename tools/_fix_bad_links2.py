#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ⑦：清除 37 道「假关联」—— core 题与其 linkedQid 指向的题根本不是同一道。

⚠️ 这是 tools/_audit_sync_deep.py「D2 关联质量」维度扫出来的，危害**大于漏关联**：
   一道 f(x)=|x(1-x)| 的题被链到 2022-6（数列题），用户在任一边的标记都会
   出现在另一道完全无关的题上（「标记乱跑」的另一半根因）。

逐对人工核对题干后判定：
  · CLEAR  28 道：清 linkedQid → 存 linkedQidOld（前端 migrateLinkFixKeys 会把
            旧键标记**复制**到 core-<no>，不丢用户在 core 侧做的标记）
  · PROMOTE 9 道：清 linkedQid，并把上一轮加的 linkAlias **转正**为 linkedQid
            （旧错键写进 linkedQidDead，仅留痕、不迁移 —— 它不是同题，迁移会串味）

判定依据（sim 只是线索，以题干关键内容为准）：
  数值/函数/条件不同即非同题，如
   · no=222  f(x)=|x(1-x)|        ≠ 2022-6  x_n 有界数列           sim=0.000
   · no=189  y=x·ln(e+1/(x-1))    ≠ 2016-9  y=x³/(1+x²)+arctan(...)  sim=0.429
   · no=560  x=cos t 化简 y''-xy'+y=0 ≠ DG900JXB-1115  x=sin t 化简 y''-xy'-4y=0
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
DGY = os.path.join(ROOT, 'pwa/data/dgy_items.json')

# core no -> 错误的 linkedQid（人工核对判非同题）
CLEAR = [
    (222, '2022数二真题-6'), (990, '2018数二真题-5'), (466, '2002数二真题-4'),
    (636, 'DG900JXB-90'), (674, 'DG900JXB-136'), (68, 'DG900JXB-869'),
    (178, '2009数二真题-9'), (428, '2023数二真题-13'), (781, 'DG900JXB-152'),
    (529, 'DG900JXB-1106'), (213, 'DG900JXB-964'), (583, 'DG900JXB-1027'),
    (253, '2003数二真题-15'), (310, 'DG900JXB-1281'), (221, '2008数二真题-12'),
    (416, '2019数二真题-11'), (456, 'DG900JXB-970'), (115, '2009数二真题-1'),
    (6, 'DG900JXB-480'), (566, 'DG900JXB-999'), (465, 'DG900JXB-1148'),
    (405, 'DG900JXB-939'), (451, 'DG900JXB-958'), (436, '2015数二真题-13'),
    (162, '2017数二真题-10'), (580, 'DG900JXB-1022'), (1034, 'DG900JXB-425'),
    (462, 'DG900JXB-986'),
    # 补漏（首轮整理清单时漏掉）：2yy'+2xy²=e^{-x²}sin x ≠ y'-(4/x)y=x²√y
    (693, 'DG900JXB-1092'),
]
# core no -> (错误的 linkedQid, 应转正为 linkedQid 的正确真题键, 旧 linkAlias 里的值)
PROMOTE = [
    (189, '2016数二真题-9', '2023数二真题-1'),
    (223, '2024数二真题-3', '2025数二真题-2'),
    (170, '2010数二真题-11', '2015数二真题-10'),
    (341, '2011数二真题-11', '2023数二真题-12'),
    (530, '2025数二真题-15', '2024数二真题-13'),
    (536, 'DG900JXB-1095', '2001数二真题-4'),
    (191, '2010数二真题-10', '2025数二真题-12'),
    (1016, 'DG900JXB-389', '2007数二真题-24'),
    (560, 'DG900JXB-1115', '2005数二真题-18'),
]


def norm(s):
    s = (s or '')
    s = re.sub(r'（本题满分[^）]*分）', '', s)
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    return s


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    dgy = json.loads(io.open(DGY, encoding='utf-8').read())
    zp = set()
    for src in (ex, dgy):
        for p in (src if isinstance(src, list) else src.get('papers', [])):
            for s in p['sections']:
                for q in s['questions']:
                    zp.add('%s-%s' % (p['id'], q['no']))

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    by_no = {q['no']: q for q in qs}

    # 存量修正①：上一版误给 CLEAR 类也写了 linkedQidDead（语义冲突：Dead=不迁移），清掉。
    # ⚠️ 但 451/253 后来被 PROMOTE_LATE 转正，它们的 Dead 是**需要的**（留痕且不迁移），
    #    第一版没排除它们导致误删 —— 这里一并补回。
    PROMOTE_LATE_NOS = {451, 253}
    fixed = 0
    for no, wrong in CLEAR:
        if no in PROMOTE_LATE_NOS:
            continue
        q = by_no.get(no)
        if q and q.get('linkedQidDead') is not None:
            q.pop('linkedQidDead', None)
            fixed += 1
    if fixed:
        print('（存量修正①）清掉 CLEAR 类上误写的 linkedQidDead：%d 道' % fixed)

    # 存量修正②：CLEAR 类里 no=451 / no=253 原本也带 linkAlias（真同题），
    # 上一版只删了 linkedQid，别名悬空（主键位置空着）。把别名转正。
    PROMOTE_LATE = [(451, 'DG900JXB-958', '2015数二真题-17'),
                    (253, '2003数二真题-15', '2009数二真题-16')]
    late = 0
    for no, wrong, right in PROMOTE_LATE:
        q = by_no.get(no)
        if q and not q.get('linkedQid') and right in (q.get('linkAlias') or []):
            q['linkedQid'] = right
            q['linkedQidDead'] = wrong
            q['linkFix'] = {'from': right, 'reason': 'alias-promoted'}
            al = [a for a in (q.get('linkAlias') or []) if a != right]
            if al:
                q['linkAlias'] = al
            else:
                q.pop('linkAlias', None)
            late += 1
            print('（存量修正②）no=%s 别名转正 -> %s' % (no, right))
    # 补回被①误删的 Dead 留痕（451/253）
    back = 0
    for no, wrong, right in PROMOTE_LATE:
        q = by_no.get(no)
        if q and q.get('linkedQid') == right and not q.get('linkedQidDead'):
            q['linkedQidDead'] = wrong
            back += 1
    if back:
        print('（存量修正③）补回 no=%s 的 linkedQidDead 留痕' % back)
    if not late and not back:
        print('（存量修正②③）无需处理')

    nC = nP = 0
    skip = []
    for no, wrong in CLEAR:
        q = by_no.get(no)
        if not q:
            skip.append((no, '无此题')); continue
        if q.get('linkedQid') != wrong:
            skip.append((no, '主键不符，实为 %s' % q.get('linkedQid'))); continue
        # ⚠️ CLEAR 类**必须迁移**：用户在 core 模式看到 no=222 时做的标记就存在
        #    「2022数二真题-6」这个键上（当时它是主键），不迁移 = 用户的标记凭空消失。
        #    迁移是**复制**，真题页那边照旧显示，两边都不丢。
        q['linkedQidOld'] = wrong       # 留痕 + migrateLinkFixKeys 的迁移源
        q['linkFix'] = {'from': wrong, 'reason': 'bad-link'}
        q.pop('linkedQidDead', None)    # 语义：Dead=不迁移；这批改迁移，故不能有
        del q['linkedQid']
        nC += 1

    for no, wrong, right in PROMOTE:
        q = by_no.get(no)
        if not q:
            skip.append((no, '无此题')); continue
        if q.get('linkedQid') != wrong:
            skip.append((no, '主键不符，实为 %s' % q.get('linkedQid'))); continue
        if right not in (q.get('linkAlias') or []):
            skip.append((no, 'linkAlias 里没有 %s' % right)); continue
        q['linkedQidDead'] = wrong      # 仅留痕：不同题，绝不迁移
        q['linkedQid'] = right
        q['linkFix'] = {'from': right, 'reason': 'alias-promoted'}   # 别名上的标记照样同步
        al = [a for a in (q.get('linkAlias') or []) if a != right]
        if al:
            q['linkAlias'] = al
        else:
            q.pop('linkAlias', None)
        nP += 1

    print('清除 %d 道 + 别名转正 %d 道' % (nC, nP))
    for no, w in CLEAR:
        print('   [清] no=%-5s 原 %s -> core-%s' % (no, w, no))
    for no, w, r in PROMOTE:
        print('   [正] no=%-5s 原 %s -> %s' % (no, w, r))
    for no, why in skip:
        print('   ⚠️ 跳过 no=%s：%s' % (no, why))

    # ---- 自检 ----
    linked = collections.Counter(q['linkedQid'] for q in qs if q.get('linkedQid'))
    # 1 悬空：主键必须能在题库里找到
    dangle = [q['no'] for q in qs if q.get('linkedQid') and q['linkedQid'] not in zp]
    if dangle:
        print('❌ 悬空主键:', dangle); return 1
    print('✅ 主键无悬空')
    # 2 一对多回潮
    grp = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            grp[q['linkedQid']].append(q)
    bad = {k: len(v) for k, v in grp.items()
           if len(v) > 1 and len({norm(q.get('stem')) for q in v}) > 1}
    if bad:
        print('❌ 一对多回潮:', bad); return 1
    print('✅ 无一对多回潮')
    # 3 别名不撞主键 + 全局唯一
    hit = [(q['no'], a) for q in qs for a in (q.get('linkAlias') or []) if linked.get(a, 0) > 0]
    if hit:
        print('❌ 别名撞主键:', hit); return 1
    c2 = collections.Counter(a for q in qs for a in (q.get('linkAlias') or []))
    dup = {a: n for a, n in c2.items() if n > 1}
    if dup:
        print('❌ 别名重复:', dup); return 1
    print('✅ 别名不撞主键且唯一（剩 %d 道带别名）' % sum(1 for q in qs if q.get('linkAlias')))
    # 4 死键不得被迁移（linkedQidDead 绝不能出现在 linkFix.from 里）
    dead_migrate = [q['no'] for q in qs
                    if q.get('linkedQidDead') and (q.get('linkFix') or {}).get('from') == q['linkedQidDead']]
    if dead_migrate:
        print('❌ 死键被设成了迁移源:', dead_migrate); return 1
    print('✅ 死键（linkedQidDead）不会被迁移')
    print('已关联 %d 道 / 独立键 %d 道' % (
        sum(1 for q in qs if q.get('linkedQid')), sum(1 for q in qs if not q.get('linkedQid'))))

    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
