#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""共享旧键组的「真同题归属」终审：
组内判定之外，再对每个旧键在**全库**反查 sim>=0.90 的题——修正「真同题不在组内」的错位。
（实例：2007数二真题-13 是 y=1/(2x+3) 高阶导数题，真同题 no=167 却被挂在 2005数二真题-1 组下）
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
DGY = os.path.join(ROOT, 'pwa/data/dgy_items.json')
PLAN = os.path.join(ROOT, 'tools/_shared_old_plan.json')


def norm(s):
    s = s or ''
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


def bg(s):
    s = norm(s)
    return set(s[i:i + 2] for i in range(len(s) - 1))


def sim(a, b):
    A, B = bg(a), bg(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def main():
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
    dgy = json.loads(io.open(DGY, encoding='utf-8').read())
    zp = {}
    for src in (ex, dgy):
        for p in (src if isinstance(src, list) else src.get('papers', [])):
            for s in p['sections']:
                for q in s['questions']:
                    zp['%s-%s' % (p['id'], q['no'])] = q.get('stem') or ''

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    groups = collections.defaultdict(list)
    for q in qs:
        old = (q.get('linkFix') or {}).get('from') or q.get('linkedQidOld')
        if old:
            groups[old].append(q)
    shared = {k: v for k, v in groups.items() if len(v) > 1}

    plan = json.loads(io.open(PLAN, encoding='utf-8').read())
    fixed = {}
    print('=== 全库反查（sim>=0.90 才算真同题）===')
    for old in sorted(shared):
        ref = zp.get(old) or ''
        if not ref:
            print('  %-20s ⚠️ 该键不存在于题库，全部不迁移' % old)
            fixed[old] = []
            continue
        # 全库找真同题
        cands = sorted(((sim(q.get('stem') or '', ref), q) for q in qs), key=lambda x: -x[0])
        best = [(s, q) for s, q in cands if s >= 0.90]
        cur = plan.get(old, [])
        if len(best) >= 1:
            # 真同题可能不止一道（同题重复收录）→ 只取最小 no，避免又串
            keep_no = [best[0][1]['no']]
            tag = '真同题' if best[0][0] >= 0.95 else '高度相似'
            moved = ''
            if cur and cur[0] != keep_no[0]:
                moved = '  （修正：原定 no=%s → 改 no=%s）' % (cur[0], keep_no[0])
            print('  %-20s %s no=%-5s sim=%.3f%s' % (old, tag, keep_no[0], best[0][0], moved))
            if len(best) > 1:
                print('       注：另有 %d 道同题（no=%s），不迁移以免重复' % (
                    len(best) - 1, ','.join(str(s and q['no']) for s, q in best[1:4])))
            fixed[old] = keep_no
        else:
            if cur:
                print('  %-20s 组内曾判 no=%s（sim 不足 0.90）→ 复核后保留' % (old, cur[0]))
                fixed[old] = cur
            else:
                print('  %-20s 全库无真同题 → 不迁移（原 sim 最高 %.3f）' % (old, cands[0][0]))
                fixed[old] = []

    out = os.path.join(ROOT, 'tools/_shared_old_plan2.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(fixed, ensure_ascii=False, indent=1))
    keep = sum(len(v) for v in fixed.values())
    print()
    print('终审：保留迁移 %d 道，改判不迁移 %d 道' % (
        keep, sum(len(v) for v in shared.values()) - keep))
    print('方案已写', out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
