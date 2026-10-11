#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""标记同步「高维综合检测」：不只查「真题→core」一个方向，而是六个维度交叉扫描。

D1 悬空引用：core 题的 linkedQid / linkAlias 指向的键在任何题库里都不存在 → 死键
D2 关联质量：已关联的核心题 vs 其 linkedQid 真题的题干相似度 → 低分=可疑错关联
D3 反向孤岛：主键为 'core-N' 的题上有用户标记 → 只在 core 可见（正常，统计）
D4 三态一致性：收藏 / 状态 / 笔记 之间的异常组合
D5 孤儿标记键：用户标注键在任何题库里都找不到 → 完全悬空
D6 双模式可见性：core 题主键是 DG 键时，exam/core 两模式分别能否显示
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa/data', *a)
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def norm(s):
    s = (s or '')
    for _ in range(3):
        s = re.sub(r'^\s*[（(]?\s*本题满分[^）)]*分\s*[）)]?\s*', '', s)
        s = re.sub(r'^\s*【[^】]{1,24}】\s*', '', s)
        s = re.sub(r'^\s*例\s*\d+[.\-]\d+\s*', '', s)
        s = re.sub(r'^\s*[（(]\s*(?:19|20)\d\d[^）)]{0,20}[）)]\s*', '', s)
        s = re.sub(r'^\s*[（(]\s*\d{1,2}\s*[）)]\s*', '', s)
        s = re.sub(r'^\s*\d{1,2}\s*[.、]\s*', '', s)
    s = re.sub(r'\\(?:mathrm|mathbb|mathbf|operatorname)\s*\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\(?:left|right|displaystyle|limits|,|;|!|:|\s)+', '', s)
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = re.sub(r'[{}\\$\s]', '', s)
    s = re.sub(r'[，。、；：,.;:（）()]', '', s)
    return s


def bigrams(s):
    return set(s[i:i + 2] for i in range(len(s) - 1))


def sim(a, b):
    A, B = bigrams(norm(a)), bigrams(norm(b))
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def load(fn):
    p = P(fn)
    if not os.path.exists(p):
        return None
    return json.loads(io.open(p, encoding='utf-8').read())


def main():
    cb = load('core_bank.json')
    ex = load('exam.json') or []
    ann = json.loads(io.open(ANN, encoding='utf-8').read())

    # ---- 全库键 universe：真题 / 大观园习题 / 大观园真题 ----
    zp = {}
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp['%s-%s' % (p['id'], q['no'])] = (q.get('stem') or '', '真题')

    # ⚠️ dgy_items.json 与 exam.json 一样是**试卷结构**（id + sections[].questions[].no），
    #    不是 items 列表。DG 键 = '<卷id>-<题no>'，如 DG900JXB-614。
    #    （第一版误当 items 读 it.id，只取到顶层 "DG900JXB"，误报 170 处悬空）
    for fn, tag in [('dgy_items.json', '大观园习题')]:
        d = load(fn)
        if not d:
            continue
        for p in (d if isinstance(d, list) else d.get('papers', [])):
            for s in p['sections']:
                for q in s['questions']:
                    zp['%s-%s' % (p['id'], q['no'])] = (q.get('stem') or '', tag)
    bq = load('bank_questions.json')
    if bq:
        for it in (bq.get('items') or []):
            if it.get('id') is not None:
                zp['bank-%s' % it['id']] = (it.get('stem') or '', '大观园真题')

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    print('core 题数 =', len(qs), '｜题库键 universe =', len(zp))
    print()

    # ================= D1 悬空引用 =================
    print('=== D1 悬空引用（linkedQid / linkAlias 指向不存在的键）===')
    dangling = []
    for q in qs:
        lq = q.get('linkedQid')
        if lq and lq not in zp:
            dangling.append((q['no'], 'linkedQid', lq))
        for a in (q.get('linkAlias') or []):
            if a not in zp:
                dangling.append((q['no'], 'linkAlias', a))
    if dangling:
        print('  ❌ %d 处悬空：' % len(dangling))
        for no, kind, k in dangling[:30]:
            print('     core no=%-5s %s -> %s' % (no, kind, k))
    else:
        print('  ✅ 0 处：所有 linkedQid / linkAlias 都能在题库里找到')
    print()

    # ================= D2 关联质量 =================
    print('=== D2 关联质量（已关联题 vs 其真题的题干相似度）===')
    pairs = [(q, q['linkedQid']) for q in qs if q.get('linkedQid') and q['linkedQid'] in zp]
    scored = []
    for q, k in pairs:
        scored.append((sim(q.get('stem') or '', zp[k][0]), q['no'], k))
    scored.sort()
    buckets = collections.Counter()
    for s, no, k in scored:
        buckets['≥0.80' if s >= 0.80 else '0.60~0.80' if s >= 0.60 else
                '0.40~0.60' if s >= 0.40 else '0.20~0.40' if s >= 0.20 else '<0.20'] += 1
    print('  已关联共 %d 道，相似度分布：' % len(scored))
    for b in ['≥0.80', '0.60~0.80', '0.40~0.60', '0.20~0.40', '<0.20']:
        print('     %-10s %d 道' % (b, buckets[b]))
    print()
    low = [(s, no, k) for s, no, k in scored if s < 0.40]
    print('  ⚠️ 相似度 <0.40 的可疑关联 = %d 道（需人工判）' % len(low))
    for s, no, k in low[:25]:
        q = next(x for x in qs if x['no'] == no)
        print('     sim=%.3f  core no=%-5s -> %s' % (s, no, k))
        print('        core: %s' % (q.get('stem') or '').replace('\n', ' ')[:66])
        print('        库  : %s' % (zp[k][0] or '').replace('\n', ' ')[:66])
    print()

    # ================= D3 反向孤岛 =================
    e = ann['exam']
    fav = json.loads(e['favs'])
    st = json.loads(e['status'])
    notes = e['notes']
    note_keys = set(k.replace('examNote-', '') for k in notes)
    allmark = set(fav) | set(st) | note_keys
    core_self = set('core-%s' % q['no'] for q in qs if not q.get('linkedQid'))
    island = sorted(k for k in allmark if k in core_self)
    print('=== D3 反向孤岛（标记挂在 core 独立键上，真题页看不到）===')
    print('  共 %d 个（属正常：这些题真题里没有同题，只在核心题库里）' % len(island))
    for k in island[:12]:
        o = []
        if k in fav: o.append('收藏')
        if k in st: o.append('状态:' + st[k])
        if k in note_keys: o.append('笔记')
        print('     %-14s %s' % (k, '+'.join(o)))
    if len(island) > 12:
        print('     … 另 %d 个' % (len(island) - 12))
    print()

    # ================= D4 三态一致性 =================
    print('=== D4 三态一致性（收藏 / 状态 / 笔记 的异常组合）===')
    only_note = sorted(k for k in note_keys if k not in fav and k not in st)
    mastered_no_fav = sorted(k for k, v in st.items() if v == 'mastered' and k not in fav)
    unk_and_unf = sorted(k for k, v in st.items() if v not in ('unknown', 'unfamiliar', 'mastered'))
    print('  只有笔记、无收藏无状态 = %d 个' % len(only_note))
    print('  状态 mastered 但未收藏 = %d 个（口径上 mastered 通常伴随收藏）' % len(mastered_no_fav))
    print('  状态取值非法 = %d 个 %s' % (len(unk_and_unf), unk_and_unf[:5]))
    empty_note = [k for k, v in notes.items() if not (v or '').strip()]
    print('  空笔记（键存在但内容为空）= %d 个 %s' % (len(empty_note), empty_note[:5]))
    print()

    # ================= D5 孤儿标记键 =================
    print('=== D5 孤儿标记键（任何题库里都找不到）===')
    known = set(zp) | core_self | set(
        (q['linkedQid'] for q in qs if q.get('linkedQid')))
    known |= set(a for q in qs for a in (q.get('linkAlias') or []))
    known |= set('xd-%s' % q['xdNo'] for q in qs if q.get('xdNo') is not None)
    orphans = sorted(k for k in allmark if k not in known)
    print('  共 %d 个：' % len(orphans))
    for k in orphans:
        o = []
        if k in fav: o.append('收藏')
        if k in st: o.append('状态:' + st[k])
        if k in note_keys: o.append('笔记')
        print('     %-22s %s' % (k, '+'.join(o)))
    print()

    # ================= D6 双模式可见性 =================
    print('=== D6 主键性质分布（决定该题在哪个模式显示）===')
    kind = collections.Counter()
    for q in qs:
        lq = q.get('linkedQid')
        if not lq:
            kind['core 独立键'] += 1
        elif re.match(r'^\d{4}数[一二三]真题-', lq):
            kind['真题键（两模式互通）'] += 1
        elif lq.startswith('DG'):
            kind['大观园键'] += 1
        else:
            kind['其他:' + lq[:12]] += 1
    for k, n in kind.most_common():
        print('     %-26s %d 道' % (k, n))
    print()
    print('  ⚠️ 大观园键的题：在 exam 模式由大观园题库渲染、core 模式由 core_bank 渲染，')
    print('     两边主键一致 → 标记互通；但若大观园侧该题被去重逻辑隐藏，标记会「看不见题」。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
