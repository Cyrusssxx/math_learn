#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""可行性测试 3：验证「书签分类名」能否映射到 cat_deep 节点。

前面的测试发现「完全同名 0 个」——怀疑是书签名的编号前缀导致（如 "1.求函数表达式"）。
本测：剥离各种编号前缀（1. / a) / (1) / A. / 一、）后，再与 cat_deep 节点名比对。

并针对「未细分的 275 题」：
  - source 命中书签后，取其上级分类链（L3~L5）
  - 看能否在 cat_deep 树里找到对应子节点（供挂靠）
"""
import io, json, os, sys, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)
PDF = r'E:/Desktop/大观/【合集】大观答案/【合集】大观答案.pdf'
import pymupdf

# 各种编号前缀
PFX = [
    r'^\s*[0-9]+[.、]\s*',          # 1. 2、 
    r'^\s*[（(]\s*[0-9]+\s*[)）]\s*', # (1) （2）
    r'^\s*[a-zA-Z][).、]\s*',        # a) A. 
    r'^\s*[一二三四五六七八九十]+[、.]\s*',  # 一、
]


def strip_pfx(s):
    """剥离编号前缀，返回纯名称"""
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

    # ---- 1. 剥离前缀后与 cat_deep 节点名比对 ----
    node_names = collections.defaultdict(list)
    for nid, v in nodes.items():
        nm = str(v.get('n') or '').strip()
        if nm:
            node_names[nm].append(str(nid))
    print('=== 1. 书签分类名 vs cat_deep 节点名（剥离编号前缀后）===')
    for lv in (3, 4, 5):
        bk = [strip_pfx(t) for l, t, _ in toc if l == lv and t.strip()]
        bk = [b for b in bk if b]
        hit = [b for b in bk if b in node_names]
        print('   L%d：书签 %d 条，剥离后命中 cat_deep 节点 %d 条 (%.0f%%)' % (
            lv, len(bk), len(hit), 100.0 * len(hit) / max(1, len(bk))))
        for b in hit[:6]:
            print('        「%s」→ 节点 %s' % (b, node_names[b][:3]))
    print()

    # ---- 2. 未细分题（只挂到章根）是否能通过书签细化 ----
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
    print('=== 2. 未细分（只挂章根）的题：%d 道 ===' % len(only_root))

    # 建书签索引（题源 → 分类链），含剥离前缀的纯名
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
        k = k.split(';')[0].split('；')[0]
        return k.strip(';,')

    # 尝试细化
    can_refine, cannot = [], []
    for q in only_root:
        srcs = str(q.get('source') or '')
        cands = []
        for s in re.split(r'[;；]', srcs):
            k = norm_src(s)
            if k in src_index:
                for h in src_index[k]:
                    # 分类链里找能映射成 cat_deep 节点的
                    for name in h['path']:
                        pn = strip_pfx(name)
                        if pn in node_names:
                            cands.append((pn, node_names[pn], h['path']))
        if cands:
            can_refine.append((q, cands))
        else:
            cannot.append(q)
    print('   其中能通过书签细化：%d 道' % len(can_refine))
    print('   无法细化（无 source 命中/分类名映射不了）：%d 道' % len(cannot))
    print()
    print('=== 可细化样本 ===')
    for q, c in can_refine[:10]:
        names = [x[0] for x in c[:3]]
        print('   core-%s ｜ catId=%s 现有=%s' % (q['no'], q.get('catId'), q.get('deepCats')))
        print('        可挂候选：%s' % '、'.join(names))
        print('        书签路径：%s' % ' > '.join(c[0][2][-3:])[:70])
    doc.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())