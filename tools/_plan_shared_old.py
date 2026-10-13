#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""对 22 个「共享旧键组」逐组判定：组内哪一道（如果有）才是与旧键真题真同题的。
判据：题干相似度（归一化 + 剥排版前缀 + 保留公式内容）。
输出每组结论，供修复脚本使用。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
DGY = os.path.join(ROOT, 'pwa/data/dgy_items.json')


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
    plan = {}
    print('共享组 %d 个：' % len(shared))
    for old, lst in sorted(shared.items(), key=lambda x: -len(x[1])):
        ref = zp.get(old)
        print('=' * 78)
        print('旧键 %s （%d 道题共享）' % (old, len(lst)))
        print('  该键真题: %s' % ((ref or '⚠️ 键不存在于题库').replace('\n', ' ')[:88]))
        scored = sorted(((sim(q.get('stem') or '', ref or ''), q) for q in lst), key=lambda x: -x[0])
        best = scored[0]
        print('  组内相似度排序：')
        for s, q in scored[:6]:
            flag = ' ← 真同题' if s >= 0.75 else ('  (疑似)' if s >= 0.55 else '')
            print('     sim=%.3f no=%-5s %s%s' % (s, q['no'], (q.get('stem') or '').replace('\n', ' ')[:52], flag))
        print('  ⇒ 结论: %s' % (
            'no=%s 迁移，其余不迁移' % best[1]['no'] if best[0] >= 0.75
            else '⚠️ 组内无真同题 → 全部不迁移'))
        plan[old] = [best[1]['no']] if best[0] >= 0.75 else []
    # 存档供修复脚本使用
    out = os.path.join(ROOT, 'tools/_shared_old_plan.json')
    io.open(out, 'w', encoding='utf-8').write(json.dumps(plan, ensure_ascii=False, indent=1))
    print()
    print('迁移方案已写', out)
    keep = sum(len(v) for v in plan.values())
    print('保留迁移 %d 道；改判「不迁移」%d 道' % (
        keep, sum(len(v) for v in shared.values()) - keep))
    return 0


if __name__ == '__main__':
    sys.exit(main())
