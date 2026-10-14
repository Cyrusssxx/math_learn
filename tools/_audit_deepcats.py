#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""检测细分类标签（q.deepCats）的漏标 —— 用户报「偏导数的重点题在下分支找不到、上级能看到」。

机制（category.js）：细分类过滤 = catSet.has(catId) && deepCats ∩ deepSubtreeSet(curDeepCat) ≠ ∅。
所以题的 deepCats 缺失/错位 → 父级（只看 catId）能看到，子分支（看 deepCats）永远看不到。

三类问题：
  A. 缺失      —— deepCats 字段不存在 / 非数组 / 空数组
  B. 悬空      —— deepCats 里的 id 不在 cat_deep.nodes（指向已不存在的节点）
  C. 错位      —— deepCats 与「catId 对应的细分类子树」（l2root[catId] 及其后代）完全无交集
                  → 点该 L2 的任何细分支都看不到这道题（哪怕点的是它 catId 自己的根）
"""
import io, json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)


def load(name):
    d = json.loads(io.open(P(name), encoding='utf-8').read())
    return d if isinstance(d, list) else d.get('papers', d.get('items', []))


def iter_q(src, kind):
    """统一遍历：(qid物理键, catIds(list), q)"""
    if kind in ('exam', 'dgy'):
        for p in src:
            for s in p.get('sections', []):
                for q in s.get('questions', []):
                    yield '%s-%s' % (p['id'], q['no']), (q.get('categoryIds') or ([q['catId']] if q.get('catId') is not None else [])), q
    elif kind == 'core':
        for s in src[0]['sections']:
            for q in s.get('questions', []):
                yield 'core-%s' % q['no'], (q.get('categoryIds') or ([q['catId']] if q.get('catId') is not None else [])), q
    elif kind == 'bank':
        for it in src:
            yield 'bank-%s' % it.get('id'), (it.get('categoryIds') or ([it.get('catId')] if it.get('catId') is not None else [])), it


def subtree(root, ch):
    out, stack = set(), [str(root)]
    while stack:
        x = stack.pop()
        if x in out:
            continue
        out.add(x)
        stack.extend(ch.get(x, []))
    return out


def main():
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep.get('nodes', {})
    ch = collections.defaultdict(list)
    for k, v in nodes.items():
        p = str(v.get('p') or '')
        if p:
            ch[p].append(str(k))
    l2root = {str(k): str(v) for k, v in (deep.get('l2root') or {}).items()}

    cats = json.loads(io.open(P('exam_categories.json'), encoding='utf-8').read())
    cats = cats if isinstance(cats, dict) else {str(c['id']): c for c in cats}
    # L2 分类 id 集合（细分类挂载点）
    l2ids = {k for k, v in cats.items() if v.get('level') == 2}

    sources = []
    ex = json.loads(io.open(P('exam.json'), encoding='utf-8').read())
    sources.append(('exam(真题)', load('exam.json') if not isinstance(ex, list) else ex, 'exam'))
    core = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    sources.append(('core(严选+线代重点)', [core] if isinstance(core, dict) else core, 'core'))
    bk = json.loads(io.open(P('bank_questions.json'), encoding='utf-8').read())
    items = bk.get('items', bk if isinstance(bk, list) else [])
    sources.append(('bank(大观园真题)', items, 'bank'))
    dgy = json.loads(io.open(P('dgy_items.json'), encoding='utf-8').read())
    sources.append(('dgy(大观园习题)', dgy if isinstance(dgy, list) else dgy.get('papers', []), 'dgy'))

    print('=== 细分类标签（deepCats）体检 ===')
    print()
    grand = collections.Counter()
    miss_by_cat = collections.defaultdict(list)
    for name, src, kind in sources:
        stat = collections.Counter()
        samples = collections.defaultdict(list)
        for qid, catIds, q in iter_q(src, kind):
            stat['总'] += 1
            dc = q.get('deepCats')
            if not isinstance(dc, list) or not dc:
                stat['A缺失'] += 1
                if len(samples['A']) < 5:
                    samples['A'].append('%s catId=%s' % (qid, catIds[:2] if catIds else '无'))
                for c in (catIds or ['无']):
                    if str(c) in l2ids or str(c) in l2root:
                        miss_by_cat[str(c)].append(qid)
                continue
            bad = [x for x in dc if str(x) not in nodes]
            if bad:
                stat['B悬空'] += 1
                if len(samples['B']) < 3:
                    samples['B'].append('%s 悬空id=%s' % (qid, bad[:3]))
            # C 错位：与 catId 的细分类子树无交集（catId 需在 l2root 才有子树）
            hit_own = False
            own_roots = [l2root[str(c)] for c in (catIds or []) if str(c) in l2root]
            if own_roots:
                union = set()
                for r in own_roots:
                    union |= subtree(r, ch)
                hit_own = any(str(x) in union for x in dc)
            if own_roots and not hit_own:
                stat['C错位'] += 1
                if len(samples['C']) < 3:
                    samples['C'].append('%s catId=%s dc=%s' % (qid, catIds[:2], dc[:3]))
        print('【%s】' % name)
        print('   总 %d ｜缺失 %d ｜悬空 %d ｜错位 %d' % (
            stat['总'], stat['A缺失'], stat['B悬空'], stat['C错位']))
        for k in ('A', 'B', 'C'):
            for s in samples[k][:5]:
                print('     %s %s' % (k, s))
        grand['总'] += stat['总']
        grand['A'] += stat['A缺失']
        grand['B'] += stat['B悬空']
        grand['C'] += stat['C错位']
        print()
    print('=== 合计 ===')
    print('  总题数 %d ｜缺失 %d ｜悬空 %d ｜错位 %d' % (grand['总'], grand['A'], grand['B'], grand['C']))
    print()
    if miss_by_cat:
        print('=== 缺失题按 L2 分类分布（Top 15）===')
        rows = sorted(miss_by_cat.items(), key=lambda kv: -len(kv[1]))[:15]
        for cid, qids in rows:
            nm = cats.get(cid, {}).get('name') or nodes.get(cid, {}).get('n') or '?'
            print('   %-6s %-14s %d 题缺失' % (cid, nm[:14], len(qids)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
