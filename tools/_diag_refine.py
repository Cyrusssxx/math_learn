#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""诊断：275 道未细分题为何细化不了 —— 逐层拆解卡点。

拆三层：
  1) source 能否命中书签条目（题源匹配）
  2) 命中后，书签上级分类链长什么样
  3) 这些分类名 vs cat_deep 子节点名 —— 精确/模糊（含子串）能匹配多少
另外给替代方案测算：用「题干文本 vs cat_deep 子节点名」的关键词匹配，能细化多少。
"""
import io, json, os, sys, re, collections

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


def main():
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep['nodes']
    l2root = {str(k): str(v) for k, v in deep.get('l2root', {}).items()}
    roots = set(l2root.values())
    doc = pymupdf.open(PDF)
    toc = doc.get_toc(simple=True)

    core = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    qs = [q for s in core[0]['sections'] for q in s['questions']]

    def depth_to_root(nid):
        cur = str(nid); d = 0
        while cur and d < 40:
            if cur in roots:
                return d
            cur = str(nodes.get(cur, {}).get('p') or '')
            d += 1
        return None

    only_root = [q for q in qs if (q.get('deepCats') or []) and
                 min([x for x in (depth_to_root(x) for x in q['deepCats']) if x is not None] or [99]) == 0]

    # 书签索引
    stack = []
    src_index = collections.defaultdict(list)
    for lv, title, page in toc:
        while len(stack) >= lv:
            stack.pop()
        path = stack + [title]
        stack = path
        if lv >= 6:
            k = re.sub(r'\s+', '', str(title)).lower().replace('第', '').replace('题', '')
            k = re.sub(r'^(26|25|24)版', '', k).strip(';,')
            if k:
                src_index[k].append({'path': path[:-1], 'page': page})

    def norm_src(s):
        k = re.sub(r'\s+', '', str(s or '')).lower().replace('第', '').replace('题', '')
        k = re.sub(r'^(26|25|24)版', '', k)
        return k.split(';')[0].split('；')[0].strip(';,')

    # ---- 逐层拆解 ----
    hit_src, no_src = [], []
    for q in only_root:
        got = False
        for s in re.split(r'[;；]', str(q.get('source') or '')):
            if norm_src(s) in src_index:
                hit_src.append((q, src_index[norm_src(s)]))
                got = True
                break
        if not got:
            no_src.append(q)
    print('=== 275 道未细分题的三层卡点 ===')
    print('  层1 source 命中书签：%d 道' % len(hit_src))
    print('  层1 未命中（书签名对不上）：%d 道' % len(no_src))
    print()

    # 命中题的分类链样例
    print('=== 命中题的书签分类链（去掉编号后）===')
    for q, hs in hit_src[:6]:
        p = hs[0]['path']
        pure = [strip_pfx(x) for x in p if strip_pfx(x)]
        print('   core-%s source=%s' % (q['no'], str(q.get('source'))[:34]))
        print('        书签链: %s' % ' > '.join(pure[-4:]))
        print('        现有: catId=%s deepCats=%s' % (q.get('catId'), q.get('deepCats')))
    print()

    # ---- 层3：分类名 vs cat_deep 子节点（精确 + 子串模糊）----
    node_names = collections.defaultdict(list)
    for nid, v in nodes.items():
        nm = str(v.get('n') or '').strip()
        if nm:
            node_names[nm].append(str(nid))
    all_names = list(node_names.keys())

    exact = fuzzy = 0
    fuzz_hits = []
    for q, hs in hit_src:
        pure = [strip_pfx(x) for x in hs[0]['path'] if strip_pfx(x)]
        ok_e = ok_f = False
        for nm in pure:
            if nm in node_names:
                ok_e = True
            else:
                for cn in all_names:
                    if len(cn) >= 2 and (cn in nm or nm in cn):
                        ok_f = True
                        fuzz_hits.append((q['no'], nm, cn))
                        break
            if ok_e or ok_f:
                break
        if ok_e:
            exact += 1
        elif ok_f:
            fuzzy += 1
    print('=== 层3：命中题的分类名能否落到 cat_deep 节点 ===')
    print('  精确同名：%d 道' % exact)
    print('  子串模糊可匹配：%d 道' % fuzzy)
    print('  完全落不了：%d 道' % (len(hit_src) - exact - fuzzy))
    print('  模糊匹配样例：')
    for no, nm, cn in fuzz_hits[:6]:
        print('     core-%s 「%s」≈ 节点「%s」' % (no, nm, cn))
    print()

    # ---- 替代方案：题干关键词 vs cat_deep 子节点名 ----
    print('=== 替代方案测算：题干文本 vs cat_deep 同层子节点名（关键词包含）===')
    # 对每道未细分题，取它 catId 下的子节点（候选细分类），看题干是否含其名
    children = collections.defaultdict(list)
    for nid, v in nodes.items():
        p = str(v.get('p') or '')
        if p:
            children[p].append(str(nid))
    refined = 0
    refine_sample = []
    for q in only_root:
        cid = str(q.get('catId'))
        # 现有 deepCats 的根
        dcs = [str(x) for x in (q.get('deepCats') or [])]
        cands = set()
        for d in dcs:
            cands |= set(children.get(d, []))
        if not cands:
            continue
        stem = str(q.get('stem') or '')
        hit = [c for c in cands if str(nodes[c].get('n') or '') and str(nodes[c].get('n')) in stem]
        if hit:
            refined += 1
            if len(refine_sample) < 6:
                refine_sample.append((q['no'], [str(nodes[c].get('n')) for c in hit[:2]]))
    print('  未细分 %d 道中，题干含子节点名的：%d 道 (%.0f%%)' % (
        len(only_root), refined, 100.0 * refined / max(1, len(only_root))))
    for no, names in refine_sample:
        print('     core-%s → 可挂 %s' % (no, '、'.join(names)))
    doc.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())