#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""可行性测试 2（只读）：core.source ↔ PDF 书签 的精确匹配率测算。

匹配路径（书签条目自带层级）：
  书签 L6/L7 条目 = 「题源标识」（如 880第一章基础选择2 / 26版660数一二三第1题 / 2002数二）
  其上级 L5/L4/L3 = 知识点/题型  → 这就是要补的「细分分类」

测：
  1) 归一化题源标识（去空格/版本号/「第X题」后缀差异）后，能对上多少 core 题
  2) 对能对上的题，其书签上级分类是否落在该题 catId 的现有子树内（合理）还是外部（需迁移）
  3) 列样本人工核对
"""
import io, json, os, sys, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)
PDF = r'E:/Desktop/大观/【合集】大观答案/【合集】大观答案.pdf'
import pymupdf


def norm_key(s):
    """题源标识归一化：去版本前缀/空格/标点/全半角，保留 资料名+章+类型+序号"""
    s = str(s or '')
    s = s.replace('；', ';').replace('，', ',').replace('　', ' ')
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'^(26|25|24)版', '', s)
    s = s.replace('第', '').replace('题', '')
    s = s.replace('数一二三', '数123').replace('数一二', '数12').replace('数二三', '数23')
    s = re.sub(r'[（(].*?[)）]', '', s)      # 去括号注释
    s = s.strip(';,').lower()
    return s


def split_src(s):
    """一个 source 字段可能含多条（分号分隔），拆开"""
    s = str(s or '')
    return [x for x in re.split(r'[;；]', s) if x.strip()]


def main():
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep['nodes']
    l2root = {str(k): str(v) for k, v in deep.get('l2root', {}).items()}
    roots = set(l2root.values())

    core = json.loads(io.open(P('core_bank.json'), encoding='utf-8').read())
    qs = [q for s in core[0]['sections'] for q in s['questions']]

    # ---- 建书签索引：norm_key(条目) -> [(level, title, page, 上级分类链)] ----
    doc = pymupdf.open(PDF)
    toc = doc.get_toc(simple=True)
    stack = []      # 当前路径
    index = collections.defaultdict(list)
    for lv, title, page in toc:
        while len(stack) >= lv:
            stack.pop()
        path = stack + [title]
        stack = path
        if lv >= 6:
            k = norm_key(title)
            if k:
                # 上级分类：向上找最近的非题源层（L3~L5）
                up = [t for t in path[:-1] if t.strip()]
                index[k].append({'lv': lv, 'title': title, 'page': page, 'path': up})
    print('=== 书签题源条目索引 ===')
    print('   L6+ 可归一化条目：%d 条（去重 %d）' % (
        sum(len(v) for v in index.values()), len(index)))
    print()

    # ---- 逐题匹配 ----
    matched, unmatched, multi = [], [], []
    for q in qs:
        srcs = split_src(q.get('source'))
        hits = []
        for s in srcs:
            k = norm_key(s)
            if k and k in index:
                for h in index[k]:
                    hits.append((s, h))
        if not hits:
            unmatched.append(q)
        else:
            if len(hits) > 1:
                multi.append((q, hits))
            matched.append((q, hits))
    print('=== 匹配结果（严格归一化后完全相等）===')
    print('   core 总题 %d' % len(qs))
    print('   命中 %d（其中多命中 %d）' % (len(matched), len(multi)))
    print('   未命中 %d' % len(unmatched))
    print('   命中率 %.1f%%' % (100.0 * len(matched) / len(qs)))
    print()

    # ---- 命中样本 ----
    print('=== 命中样本（题号 → 书签路径）===')
    for q, hits in matched[:8]:
        s, h = hits[0]
        print('   core-%s ｜ source=%s' % (q['no'], s[:50]))
        print('        书签: %s (p%d)' % (' > '.join(h['path'][-3:]), h['page']))
        print('        catId=%s 现有 deepCats=%s' % (q.get('catId'), q.get('deepCats')))
    print()

    print('=== 未命中样本 ===')
    for q in unmatched[:8]:
        print('   core-%s ｜ source=%s' % (q['no'], str(q.get('source'))[:60]))

    # ---- 书签上级分类是否可映射到 cat_deep 节点 ----
    print()
    print('=== 书签 L5 知识点名 与 cat_deep 节点名 重合度 ===')
    l5 = set(t.strip() for l, t, _ in toc if l == 5 and t.strip())
    node_names = set(v.get('n', '').strip() for v in nodes.values())
    inter = l5 & node_names
    print('   书签 L5 名 %d 个；cat_deep 节点名 %d 个；完全同名 %d 个' % (
        len(l5), len(node_names), len(inter)))
    print('   同名样例：%s' % '、'.join(list(inter)[:12]))
    doc.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())