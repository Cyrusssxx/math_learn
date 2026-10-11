#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ⑥：跨年同题 —— core 只收录了其中一份（以其 linkedQid 为主键），
用户把标记做在**另一年份**的同题上时，核心题库里看不到。

linkedQid 是一对一机制（一道 core 题只能占一个真题键，否则回潮到「一标记整组变」），
所以这类**不能**再补 linkedQid，改用**别名** linkAlias：
    core 题主键 = linkedQid（主）  +  linkAlias: [同题的其它年份真题键]
前端 category.js 的 migrateAliasKeys() 会把别名键上的收藏/标记/笔记**复制**到主键
（复制而非移动 —— 真题页仍以各自年份的键读标记，两边都可见，语义正确：同题）。

16 对全部人工核对过题干，确认同题。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')

# (core no, 主键=该 core 题已有 linkedQid, 别名真题键)
PAIRS = [
    (223, '2024数二真题-3', ['2025数二真题-2']),
    (189, '2016数二真题-9', ['2023数二真题-1']),
    (523, 'DG900JXB-1030', ['2010数二真题-2']),
    (170, '2010数二真题-11', ['2015数二真题-10']),
    (562, 'DG900JXB-1226', ['2016数二真题-19']),
    (560, 'DG900JXB-1115', ['2005数二真题-18']),
    (530, '2025数二真题-15', ['2024数二真题-13']),
    (451, 'DG900JXB-958', ['2015数二真题-17']),
    (536, 'DG900JXB-1095', ['2001数二真题-4']),
    (191, '2010数二真题-10', ['2025数二真题-12']),
    (341, '2011数二真题-11', ['2023数二真题-12']),
    (457, 'DG900JXB-973', ['2008数二真题-21']),
    (76, 'DG900JXB-614', ['2011数二真题-19']),
    (253, '2003数二真题-15', ['2009数二真题-16']),
    (868, 'DG900JXB-188', ['2010数二真题-7']),
    (1016, 'DG900JXB-389', ['2007数二真题-24']),
]


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    zp = set()
    for p in (ex if isinstance(ex, list) else ex.get('papers', [])):
        for s in p['sections']:
            for q in s['questions']:
                zp.add('%s-%s' % (p['id'], q['no']))
    # DG 键来自大观园题库，不在 exam.json 里；单独放宽校验
    def known(k):
        return k in zp or k.startswith('DG')

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    by_no = {q['no']: q for q in qs}

    # 别名全局唯一：同一真题键不能被两道 core 题认作别名
    owner = {}
    patched, skip = [], []
    for no, main_key, aliases in PAIRS:
        q = by_no.get(no)
        if not q:
            skip.append((no, main_key, 'core 里没有这个 no'))
            continue
        if q.get('linkedQid') != main_key:
            skip.append((no, main_key, '主键不符：实际=%s' % q.get('linkedQid')))
            continue
        ok = []
        for a in aliases:
            if not known(a):
                skip.append((no, a, '该键在真题库里不存在'))
                continue
            if a == main_key:
                skip.append((no, a, '别名等于主键'))
                continue
            if owner.get(a, no) != no:
                skip.append((no, a, '别名已被 core no=%s 占用' % owner[a]))
                continue
            owner[a] = no
            ok.append(a)
        if not ok:
            continue
        q['linkAlias'] = sorted(set(q.get('linkAlias') or []) | set(ok))
        patched.append((no, main_key, q['linkAlias']))

    print('计划 %d 对 → 实际写 %d 道' % (len(PAIRS), len(patched)))
    for no, k, al in patched:
        print('   core no=%-5s 主键=%-18s 别名=%s' % (no, k, al))
    for no, a, why in skip:
        print('   ⚠️ 跳过 no=%s %s：%s' % (no, a, why))

    # 自检 1：别名不得与任何 linkedQid 冲突（别名只能指向「没被占用的」真题键）
    all_linked = collections.Counter(q['linkedQid'] for q in qs if q.get('linkedQid'))
    conflict = [(q['no'], a) for q in qs for a in (q.get('linkAlias') or []) if all_linked.get(a, 0) > 0]
    if conflict:
        print('❌ 自检失败（别名撞主键）:', conflict)
        return 1
    # 自检 2：一个别名只能属于一道 core 题
    c2 = collections.Counter(a for q in qs for a in (q.get('linkAlias') or []))
    dup = {a: n for a, n in c2.items() if n > 1}
    if dup:
        print('❌ 自检失败（别名重复）:', dup)
        return 1
    print('✅ 自检通过：%d 道带别名，别名全局唯一且不撞主键'
          % sum(1 for q in qs if q.get('linkAlias')))

    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(
        json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
