#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 ④：给「实为真题同题却缺关联」的 core 题补 linkedQid —— 恢复标记/笔记同步。

来源：tools/_link_gap_scan.json（_scan_link_gap.py 的扫描结果）
  · auto   = 题干相似 ≥0.85 的 101 道（含用户标记的 60 道）
  · review = 0.60~0.85 的 120 道，只补「该真题上有用户标记」的 72 道
             （用户标记是强信号：他做过并标记的题，同步符合预期；
              无标记的 48 道不补 —— 可能是改编题，避免错误关联）
一对多：同一真题被多道 core 题匹配时，只有相似度最高者获得关联（已在扫描时处理，
        此处再校验一次）。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')
SCAN = os.path.join(ROOT, 'tools/_link_gap_scan.json')
ANN = r'D:\cjx\下载\download\数学笔记标注-2026-10-11.json'


def norm(s):
    s = s or ''
    s = re.sub(r'（本题满分[^）]*分）', '', s)
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'[{}$\s\\]+', '', s)
    return s


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    scan = json.loads(io.open(SCAN, encoding='utf-8').read())
    ann = json.loads(io.open(ANN, encoding='utf-8').read())
    e = ann['exam']
    marked = set(json.loads(e['favs']).keys()) | set(json.loads(e['status']).keys()) | set(
        k.replace('examNote-', '') for k in e['notes'])

    qs = [q for s in cb[0]['sections'] for q in s['questions']]
    by_no = {q['no']: q for q in qs}

    # 候选合并（去重：review 与 auto 可能重叠；同题多候选取最高分）
    cand = {}
    for k, n, s in scan['auto']:
        cand.setdefault(n, []).append((k, s))
    for k, n, s in scan['review']:
        if k in marked:
            cand.setdefault(n, []).append((k, s))
    # 每道 core 题取最高分的真题；每个真题只给一道（一对多防回潮）
    by_q = {}
    for n, lst in cand.items():
        lst.sort(key=lambda x: -x[1])
        by_q[n] = lst[0]
    occ = collections.Counter()
    for n, (k, s) in by_q.items():
        occ[k] += 1
    drop = {k for k, c in occ.items() if c > 1}
    final = {n: (k, s) for n, (k, s) in by_q.items() if k not in drop}

    print('候选 %d 道 → 一对多剔除 %d 道真题 → 最终补 %d 道' % (len(by_q), len(drop), len(final)))
    if drop:
        print('  剔除的真题（多题竞争）:', sorted(drop))

    # 占用检查：真题已被「有 linkedQid 的题」占用 → 不可再补（防一对多回潮）
    occ = collections.Counter()
    for q in qs:
        if q.get('linkedQid'):
            occ[q['linkedQid']] += 1

    patched = []
    for n, (k, s) in sorted(final.items()):
        if occ.get(k, 0) > 0:
            continue                      # 已被其他题占用
        q = by_no[n]
        if q.get('linkedQid'):
            continue                      # 修复过程中已补（不该发生，防御）
        q['linkedQid'] = k
        q['linkScan'] = round(s, 3)      # 匹配依据留痕
        occ[k] = 1
        patched.append((n, k, s))

    print('实际补 %d 道：' % len(patched))
    mk = sum(1 for n, k, s in patched if k in marked)
    print('  其中真题上有你标记的 = %d 道' % mk)

    # 自检：不得出现「题干不全同」的一对多
    g = collections.defaultdict(list)
    for q in qs:
        if q.get('linkedQid'):
            g[q['linkedQid']].append(q)
    bad = {}
    for k, v in g.items():
        if len(v) > 1 and len({norm(q.get('stem')) for q in v}) > 1:
            bad[k] = len(v)
    if bad:
        print('❌ 自检失败（一对多回潮）:', bad)
        return 1
    print('✅ 自检通过：无一对多回潮')

    if not apply:
        print('（--check 模式，未写文件）')
        return 0
    io.open(CORE, 'w', encoding='utf-8').write(json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
    print('已写回', CORE)
    mp = os.path.join(ROOT, 'tools/_fill_links_applied.json')
    io.open(mp, 'w', encoding='utf-8').write(json.dumps(
        {'patched': [[n, k, s] for n, k, s in patched], 'dropped_zhen': sorted(drop)},
        ensure_ascii=False, indent=1))
    print('清单已写', mp)
    return 0


if __name__ == '__main__':
    sys.exit(main())
