#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ②：清掉 139 道「错误共用 linkedQid」的题的主键重定向。

背景：qidOf() 会把主键重定向到 linkedQid，而 25 组共 133+ 道题的 linkedQid 是与
      自己无关的真题题（如 41 道极限题都链到 2002数二真题-4）→ 这些题共享收藏/标记键，
      在一道上标记会让整组跟着变。

处置：
  · 题干相同的组（真同题，关联正确）→ 保留 linkedQid
  · 题干不同的组 → 清除 linkedQid，主键回到各自的 core-<no>
    - 对「组内存在与真题题相似度 ≥0.6 的题」的组（说明确有一道是真同题）：
      在该题上写 linkFix={from:<旧键>}，前端据此把用户在该键上的标记**复制**过来
      （复制而非移动 → 真题页的标记不受影响）
    - 其余组不写 linkFix（标记本属真题页，core 侧不该显示）

用法：python tools/_fix_bad_links.py [--apply]
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
EXAM = os.path.join(ROOT, 'pwa/data/exam.json')
MIG_SIM = 0.60          # 判定「确为同题」的相似度门槛


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
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    ex = json.loads(io.open(EXAM, encoding='utf-8').read())
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

    cleared, kept, fixes = [], [], []
    for k, v in multi.items():
        norms = collections.Counter(norm(q['stem']) for q in v)
        same = [q for q in v if norms[norm(q['stem'])] > 1]
        # 找与真题题最像的
        z = zp.get(k)
        best, best_sc = None, 0.0
        if z:
            for q in v:
                sc = jac(norm(q['stem']), norm(z['stem']))
                if sc > best_sc:
                    best, best_sc = q, sc
        for q in v:
            if q in same:
                kept.append((k, q['no']))
                continue
            q['linkedQidOld'] = k            # 留痕备查（不参与逻辑）
            del q['linkedQid']
            cleared.append((k, q['no']))
        if best is not None and best_sc >= MIG_SIM and best not in same:
            best['linkFix'] = {'from': k, 'sim': round(best_sc, 2)}
            fixes.append((k, best['no'], round(best_sc, 2)))

    print('=== 清除错误 linkedQid ===')
    print('  组数 %d，清除 %d 道；保留真同题 %d 道' % (len(multi), len(cleared), len(kept)))
    print('=== 需前端复制标记的题（组内确有一道是真同题）===')
    for k, n, sc in fixes:
        print('  %-22s → no=%-5s (相似 %.2f)' % (k, n, sc))
    print()
    # 自检：清除后，只允许「题干真相同」的组保留重复 linkedQid
    errs = []
    gg = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            gg[q['linkedQid']].append(q)
    for k, v in gg.items():
        if len(v) > 1:
            norms = collections.Counter(norm(q['stem']) for q in v)
            if max(norms.values()) < len(v):        # 并非全部题干相同 → 仍有错误关联
                errs.append('%s 仍有 %d 道（题干不全同）' % (k, len(v)))
    if len(cleared) + len(kept) != sum(len(v) for v in multi.values()):
        errs.append('数量对不上')
    if errs:
        print('❌ 自检失败:', errs)
        return 1
    print('✅ 自检通过：错误关联已清（真同题组保留）')
    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    mp = os.path.join(ROOT, 'tools/_linkfix_map.json')
    io.open(mp, 'w', encoding='utf-8').write(json.dumps(
        {'cleared': cleared, 'kept': kept, 'fixes': fixes}, ensure_ascii=False, indent=1))
    print('清单已写', mp)
    return 0


if __name__ == '__main__':
    sys.exit(main())
