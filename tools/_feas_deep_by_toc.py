#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""可行性测试（只读）：用大观答案 PDF 书签给 core 库「未细分」的题补细分。

思路与前提验证：
  A. core 库 deepCats 的「细分深度」分布 —— 有多少题只挂到 l2root 根（=未细分）
  B. PDF 书签的层级/命名结构 —— L6/L7 是否为「题源+来源」可匹配格式
  C. 匹配率测算 —— 用 source 字段（如「26版660数一二三第1题」）能否对上书签条目
不写任何数据文件。
"""
import io, json, os, sys, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)
PDF = r'E:/Desktop/大观/【合集】大观答案/【合集】大观答案.pdf'

import pymupdf


def depth_to_root(node_id, nodes, roots, limit=40):
    """节点到 l2root 的距离（0 = 本身就是根）"""
    cur = str(node_id)
    d = 0
    while cur and d < limit:
        if cur in roots:
            return d
        cur = str(nodes.get(cur, {}).get('p') or '')
        d += 1
    return None


def main():
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep['nodes']
    l2root = {str(k): str(v) for k, v in deep.get('l2root', {}).items()}
    roots = set(l2root.values())

    core = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    qs = [q for s in core[0]['sections'] for q in s['questions']]

    # ---------- A. 细分深度分布 ----------
    print('=== A. core 库 deepCats 细分深度分布 ===')
    print('   core 总题数：%d' % len(qs))
    dist = collections.Counter()
    only_root, no_dc, deep_ok = [], [], []
    for q in qs:
        dc = [str(x) for x in (q.get('deepCats') or [])]
        if not dc:
            no_dc.append(q['no']); dist['无 deepCats'] += 1; continue
        ds = [depth_to_root(x, nodes, roots) for x in dc]
        ds = [d for d in ds if d is not None]
        if not ds:
            dist['无法上溯'] += 1; continue
        mn = min(ds)
        dist['最深精度=%d' % mn] += 1
        if mn == 0:
            only_root.append(q['no'])
        else:
            deep_ok.append(q['no'])
    for k in sorted(dist):
        print('   %-14s %d' % (k, dist[k]))
    print('   → 只挂到「章根」（未细分）：%d 题' % len(only_root))
    print('   → 已细分到子节点：%d 题' % len(deep_ok))
    print('   → 无标签：%d 题' % len(no_dc))
    print()

    # 未细分题按 catId 分布
    bycat = collections.defaultdict(list)
    for q in qs:
        if q['no'] in only_root:
            bycat[str(q.get('catId'))].append(q['no'])
    print('   未细分题的 catId 分布（Top 12）：')
    for cid, nos in sorted(bycat.items(), key=lambda kv: -len(kv[1]))[:12]:
        nm = nodes.get(cid, {}).get('n', '?')
        print('      catId=%-6s %-16s %d 题' % (cid, nm[:16], len(nos)))
    print()

    # ---------- B. PDF 书签结构 ----------
    print('=== B. PDF 书签结构与命名可匹配性 ===')
    doc = pymupdf.open(PDF)
    toc = doc.get_toc(simple=True)
    lv = collections.Counter(l for l, _, _ in toc)
    print('   总条数 %d ｜ 层级分布 %s' % (len(toc), dict(sorted(lv.items()))))
    # L6/L7 条目命名样例
    for target in (6, 7):
        ex = [t for l, t, _ in toc if l == target]
        print('   L%d 共 %d 条，样例：' % (target, len(ex)))
        for t in ex[:5]:
            print('      %s' % t)
    # 能否解析出「来源+编号」
    pat = re.compile(r'(660|1000|880|900|姜晓千|真题同源|数[一二三])')
    l67 = [t for l, t, _ in toc if l >= 6]
    hit = [t for t in l67 if pat.search(t)]
    print('   L6+ 中带「题源关键词」的：%d / %d (%.0f%%)' % (
        len(hit), len(l67), 100.0 * len(hit) / max(1, len(l67))))
    print()

    # ---------- C. source 匹配率粗测 ----------
    print('=== C. core.source 与书签条目匹配粗测 ===')
    srcs = [str(q.get('source') or '') for q in qs]
    with_src = [s for s in srcs if s.strip()]
    print('   core 有 source 的题：%d / %d' % (len(with_src), len(qs)))
    print('   source 样例：')
    for s in with_src[:6]:
        print('      %s' % s[:70])
    # 抽取 source 里的核心标识（如 660第1题 / 880第一章基础填空1）
    def core_key(s):
        m = re.findall(r'((?:26版|25版|24版)?\s*(?:660|1000|880|900|🐙1000)[^;；,，。]*?第?\d+[题]?)', s)
        return m
    keys = [k for s in with_src for k in core_key(s)]
    print('   能从 source 抽出「资料+题号」的：%d 个（去重 %d）' % (len(keys), len(set(keys))))
    for k in list(dict.fromkeys(keys))[:8]:
        print('      %s' % k)
    doc.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())