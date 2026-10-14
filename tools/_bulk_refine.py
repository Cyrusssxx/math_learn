#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""大批量：把未细分题匹配到「现有细分支」（绝不新建节点），按置信度分两批。

候选约束（保证不新加分支、不跨章）：
  候选 = 该题所属章根（deepCats 上溯到的 root）的**子树内现有节点**，且必须 depth>0

打分信号（均来自已细分的题/现有体系）：
  A 同 catId 的已细分题 deepCats 分布（最可靠，权重 3）
  B 书签协同投票：同书签父分类下已细分题的 deepCats（权重 2）
  C 题干含子节点名（节点名 >=3 字，权重 2）
  D 同源（source 前 12 字）已细分题的 deepCats（权重 1）

置信度：
  高 = 命中 >=2 个不同信号，或 A 支持数 >=5
  中 = 仅 1 个信号但支持数 >=2
  低 = 其余（不归类，避免瞎猜）

--batch1 执行第一批（高置信），--batch2 执行第二批（中置信）；默认 dry-run 只报告。
"""
import io, json, os, sys, re, collections, shutil, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)
PDF = r'E:/Desktop/大观/【合集】大观答案/【合集】大观答案.pdf'
import pymupdf

PFX = [r'^\s*[0-9]+[.、]\s*', r'^\s*[（(]\s*[0-9]+\s*[)）]\s*',
       r'^\s*[a-zA-Z][).、]\s*', r'^\s*[一二三四五六七八九十]+[、.]\s*']


def strip_pfx(s):
    s = str(s or '').strip()
    for p in PFX:
        s = re.sub(p, '', s).strip()
    return s


def norm_src(s):
    s = strip_pfx(s)
    s = re.sub(r'\s+', '', s).lower()
    s = re.sub(r'^(26|25|24)版', '', s).replace('🐙', '')
    s = re.sub(r'[（(].*?[)）]', '', s).replace('第', '').replace('题', '')
    return s.strip(';,').strip()


def main():
    b1 = '--batch1' in sys.argv
    b2 = '--batch2' in sys.argv
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep['nodes']
    l2root = {str(k): str(v) for k, v in deep.get('l2root', {}).items()}
    roots = set(l2root.values())
    children = collections.defaultdict(list)
    for nid, v in nodes.items():
        p = str(v.get('p') or '')
        if p:
            children[p].append(str(nid))

    def dtr(nid):
        cur = str(nid); d = 0
        while cur and d < 40:
            if cur in roots:
                return d
            cur = str(nodes.get(cur, {}).get('p') or '')
            d += 1
        return None

    def root_of(nid):
        cur = str(nid); g = 0
        while cur and g < 40:
            if cur in roots:
                return cur
            cur = str(nodes.get(cur, {}).get('p') or '')
            g += 1
        return None

    def subtree(nid):
        out, stack = set(), [str(nid)]
        while stack:
            x = stack.pop()
            if x in out:
                continue
            out.add(x)
            stack.extend(children.get(x, []))
        return out

    core = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    qs = [q for s in core[0]['sections'] for q in s['questions']]

    def has_sub(q):
        return any((dtr(x) or 0) > 0 for x in (q.get('deepCats') or []))

    todo = [q for q in qs if (q.get('deepCats') or []) and not has_sub(q)]
    refined = [q for q in qs if has_sub(q)]
    print('真正未细分：%d 道 ｜ 已细分（可参考）：%d 道' % (len(todo), len(refined)))

    # ---- 建信号 ----
    # A: 同 catId -> Counter(deepCats 子节点)
    sigA = collections.defaultdict(collections.Counter)
    for q in refined:
        cid = str(q.get('catId'))
        for d in [str(x) for x in (q.get('deepCats') or [])]:
            if (dtr(d) or 0) > 0:
                sigA[cid][d] += 1
    # D: 同源前缀 -> Counter
    sigD = collections.defaultdict(collections.Counter)
    for q in refined:
        key = str(q.get('source') or '')[:12]
        for d in [str(x) for x in (q.get('deepCats') or [])]:
            if (dtr(d) or 0) > 0:
                sigD[key][d] += 1
    # B: 书签协同
    doc = pymupdf.open(PDF)
    toc = doc.get_toc(simple=True)
    stack = []
    src_index = collections.defaultdict(list)
    for lv, title, page in toc:
        while len(stack) >= lv:
            stack.pop()
        path = stack + [title]
        stack = path
        if lv >= 6:
            for part in re.split(r'[;；]', title):
                k = norm_src(part)
                if k:
                    src_index[k].append(tuple(path[:-1][-2:]))
    sigB = collections.defaultdict(collections.Counter)   # 书签父分类 -> Counter
    for q in refined:
        subs = [str(x) for x in (q.get('deepCats') or []) if (dtr(x) or 0) > 0]
        for s in re.split(r'[;；]', str(q.get('source') or '')):
            k = norm_src(s)
            for key in src_index.get(k, []):
                for d in subs:
                    sigB[key][d] += 1
    doc.close()

    # ---- 逐题打分 ----
    def score(q):
        qroot = None
        for d in (q.get('deepCats') or []):
            qroot = root_of(d)
            if qroot:
                break
        if not qroot:
            return None
        cands = {c for c in subtree(qroot) if (dtr(c) or 0) > 0}   # 仅现有、章内、非根
        if not cands:
            return None
        sc = collections.Counter()
        sigs = collections.defaultdict(set)     # 节点 -> 命中了哪些信号
        cid = str(q.get('catId'))
        for n, c in sigA.get(cid, collections.Counter()).items():
            if n in cands:
                sc[n] += 3 * c
                sigs[n].add('A')
        srckey = str(q.get('source') or '')[:12]
        for n, c in sigD.get(srckey, collections.Counter()).items():
            if n in cands:
                sc[n] += 1 * c
                sigs[n].add('D')
        for s in re.split(r'[;；]', str(q.get('source') or '')):
            k = norm_src(s)
            for key in src_index.get(k, []):
                for n, c in sigB.get(key, collections.Counter()).items():
                    if n in cands:
                        sc[n] += 2 * c
                        sigs[n].add('B')
        stem = str(q.get('stem') or '')
        for n in cands:
            nm = str(nodes.get(n, {}).get('n') or '')
            if len(nm) >= 3 and nm in stem:
                sc[n] += 2
                sigs[n].add('C')
        if not sc:
            return None
        top, sval = sc.most_common(1)[0]
        nsig = len(sigs.get(top, set()))
        # A 支持数（用于置信判定）
        a_cnt = sigA.get(cid, collections.Counter()).get(top, 0)
        if nsig >= 2 or a_cnt >= 5:
            conf = '高'
        elif nsig == 1 and (sval >= 2 or a_cnt >= 2):
            conf = '中'
        else:
            conf = '低'
        return {'no': q['no'], 'node': top, 'score': sval, 'conf': conf,
                'sigs': ','.join(sorted(sigs.get(top, set()))),
                'name': str(nodes.get(top, {}).get('n') or '')}

    plans = [r for r in (score(q) for q in todo) if r]
    hi = [r for r in plans if r['conf'] == '高']
    mid = [r for r in plans if r['conf'] == '中']
    low = [r for r in plans if r['conf'] == '低']
    print()
    print('=== 匹配计划（仅用现有细分支，不新建）===')
    print('  第一批 高置信：%d 道' % len(hi))
    print('  第二批 中置信：%d 道' % len(mid))
    print('  低置信（不自动归类）：%d 道' % len(low))
    print('  完全无候选/无信号：%d 道' % (len(todo) - len(plans)))
    print()
    print('  第一批样例：')
    for r in hi[:8]:
        print('    core-%s → 「%s」(%s) 信号=%s 分=%d' % (
            r['no'], r['name'][:16], r['node'], r['sigs'], r['score']))
    print('  第二批样例：')
    for r in mid[:8]:
        print('    core-%s → 「%s」(%s) 信号=%s 分=%d' % (
            r['no'], r['name'][:16], r['node'], r['sigs'], r['score']))

    target = hi if b1 else (mid if b2 else None)
    if not target:
        print('\n（dry-run：加 --batch1 或 --batch2 执行）')
        return 0

    bak = os.path.join(ROOT, 'tools', '_bak_deepcats',
                       time.strftime('%Y%m%d-%H%M%S') + ('-b1' if b1 else '-b2'))
    os.makedirs(bak, exist_ok=True)
    shutil.copy2(P('core_bank.json'), os.path.join(bak, 'core_bank.json'))
    byno = {q['no']: q for q in qs}
    done = 0
    for r in target:
        q = byno[r['no']]
        dcs = [str(x) for x in (q.get('deepCats') or [])]
        if r['node'] not in dcs:
            dcs.append(r['node'])
            q['deepCats'] = dcs
            done += 1
    out = json.dumps(core, ensure_ascii=False, separators=(',', ':'))
    assert json.loads(out) == core, '往返自检失败'
    io.open(P('core_bank.json'), 'w', encoding='utf-8', newline='\n').write(out)
    print('\n已备份 %s' % bak)
    print('已写回：第%s批 %d 道（往返自检 OK）' % ('一' if b1 else '二', done))
    return 0


if __name__ == '__main__':
    sys.exit(main())