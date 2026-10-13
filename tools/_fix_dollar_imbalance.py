#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""修复 exam.json 中 15 处 `$$` 不平衡（2026-10-13 用户确认要改）。

根因：答案文本由多次编辑累积，`$$` 块的位置在改写中被打乱。实测 15 处：
  · 14 处是「末尾多一个孤立 `$$`」或「块内插入了多余的 `$$`」
  ·  1 处（2003 Q8）是 `$$` 开了未闭合，需要补
  ·  1 处（2023 Q11）是 `$-2$` 与 `$\ln` 连体成 `$$`，需要插入空格拆开

实现：逐字符扫描定位每个 `$$`（跳过 \\$ 转义），按**序号**精确增删，
      不用正则（避免转义地狱），改完立即全量复验。
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')


def scan_pos(v):
    """返回每个 `$$` 的起始下标（跳过 \\ 转义）"""
    out, i, n = [], 0, len(v)
    while i < n:
        ch = v[i]
        if ch == '\\':
            i += 2
            continue
        if ch == '$' and i + 1 < n and v[i + 1] == '$':
            out.append(i)
            i += 2
            continue
        i += 1
    return out


# (卷id, 题号, 字段, 操作, 参数)
#   操作 del  = 删除第 k 个 `$$`（1-based）
#   操作 space= 在第 k 个 `$$` 的第二个 $ 前插入空格（拆连体）
#   操作 add  = 在「含 anchor 的那一行」之后另起一行插入 `$$`（补闭合）
PLAN = [
    ('2023数二真题', 11, 'answer', 'space', 1),
    ('2019数二真题', 13, 'answer', 'del', 6),
    ('2019数二真题', 22, 'answer', 'del', 7),
    ('2018数二真题', 13, 'answer', 'del', 3),
    ('2017数二真题', 9,  'answer', 'del', 3),
    ('2015数二真题', 5,  'answer', 'del', 3),
    ('2015数二真题', 7,  'answer', 'del', 3),
    ('2015数二真题', 11, 'answer', 'del', 3),
    ('2014数二真题', 7,  'answer', 'del', 3),
    ('2014数二真题', 17, 'answer', 'del', 7),
    ('2013数二真题', 17, 'answer', 'del', 3),
    ('2013数二真题', 23, 'answer', 'del', 5),
    ('2009数二真题', 11, 'answer', 'del', 4),
    ('2005数二真题', 5,  'answer', 'del', 3),
    ('2003数二真题', 8,  'answer', 'add', '（重要极限）'),
]


def main():
    apply = '--apply' in sys.argv
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    papers = ex if isinstance(ex, list) else ex.get('papers', [])
    by = {}
    for p in papers:
        for s in p['sections']:
            for q in s['questions']:
                by[(p['id'], q['no'])] = q

    done = []
    for pid, no, field, op, arg in PLAN:
        q = by.get((pid, no))
        if not q:
            print('⚠️ 找不到 %s Q%s' % (pid, no))
            continue
        v = q.get(field) or ''
        before = v.count('$$')
        if op == 'del':
            pos = scan_pos(v)
            if len(pos) < arg:
                print('⚠️ %s Q%s：只有 %d 个 $$，取不到第 %d 个' % (pid, no, len(pos), arg))
                continue
            i = pos[arg - 1]
            v = v[:i] + v[i + 2:]
        elif op == 'space':
            pos = scan_pos(v)
            i = pos[arg - 1] + 1          # 第二个 $ 之前
            v = v[:i] + ' ' + v[i:]
        elif op == 'add':
            anchor = arg
            lines = v.split('\n')
            idx = next((k for k, ln in enumerate(lines) if anchor in ln), None)
            if idx is None:
                print('⚠️ %s Q%s：找不到锚点 %s' % (pid, no, anchor))
                continue
            lines.insert(idx + 1, '$$')
            v = '\n'.join(lines)
        after = v.count('$$')
        if after % 2 != 0:
            print('❌ %s Q%s：修复后仍为奇数（%d），已跳过' % (pid, no, after))
            continue
        q[field] = v
        done.append((pid, no, op, before, after))

    print('修复 %d 处：' % len(done))
    for pid, no, op, b, a in done:
        print('   %-14s Q%-3s %-6s $$ 计数 %d → %d' % (pid, no, op, b, a))

    # 全量复验
    bad = 0
    for p in papers:
        for s in p['sections']:
            for q in s['questions']:
                for fld in ('stem', 'answer', 'idea'):
                    v = q.get(fld)
                    if v and v.count('$$') % 2 == 1:
                        bad += 1
                        print('❌ 仍不平衡：%s Q%s [%s]' % (p['id'], q['no'], fld))
    print()
    print('✅ 全量复验：$$ 不平衡 = %d 处' % bad)
    if bad:
        return 1

    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(EXAM, 'w', encoding='utf-8').write(
        json.dumps(ex, ensure_ascii=False, separators=(',', ':')))
    print('已写回', EXAM)
    return 0


if __name__ == '__main__':
    sys.exit(main())
