#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""导出「未细分题」归类清单，供人工批量标注后回填。

输出两个 CSV（UTF-8 BOM，Excel 直接打开不乱码）：
  1) 未细分题归类清单.csv
     列：题号, 来源, 题干(截断), 所属章, 当前细分, 推荐候选1(id|名), 候选2, 候选3, 目标节点id(填写)
     —— 按「所属章」排序，同章的题目在一起，可批量填同一个节点 id
  2) 分类节点字典.csv
     列：节点id, 名称, 层级, 上级路径  （填 id 时查这个）

推荐候选来源：该章根下「已细分题」挂得最多的子节点 Top3（=同类题最常去的地方）
"""
import io, json, os, sys, csv, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)
OUT1 = os.path.join(ROOT, '未细分题归类清单.csv')
OUT2 = os.path.join(ROOT, '分类节点字典.csv')


def main():
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep['nodes']
    l2root = {str(k): str(v) for k, v in deep.get('l2root', {}).items()}
    roots = set(l2root.values())

    # 父子关系
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

    def path_of(nid):
        """节点的上级路径（名称链）"""
        out = []
        cur = str(nodes.get(nid, {}).get('p') or '')
        g = 0
        while cur and g < 40:
            out.append(str(nodes.get(cur, {}).get('n') or cur))
            cur = str(nodes.get(cur, {}).get('p') or '')
            g += 1
        return ' > '.join(reversed(out))

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

    # 真正未细分 = deepCats 里**没有任何** depth>0 的节点（即全都是章根）
    # ⚠️ 不能用 min(...)==0 判定：归类时是「追加子节点并保留章根」，
    #    保留章根会让 min 恒为 0 → 已归类的题会被误判成未细分、重复出现在清单里
    def has_sub(q):
        for x in (q.get('deepCats') or []):
            d = dtr(x)
            if d is not None and d > 0:
                return True
        return False

    only_root = [q for q in qs if (q.get('deepCats') or []) and not has_sub(q)]

    # 每章：已细分题挂得最多的子节点 Top3（推荐候选）
    by_root_hot = collections.defaultdict(collections.Counter)
    for q in qs:
        dcs = [str(x) for x in (q.get('deepCats') or [])]
        subs = [d for d in dcs if dtr(d) not in (0, None)]
        # 该题所属章根
        for d in dcs:
            r = d
            g = 0
            while r and g < 40:
                if r in roots:
                    break
                r = str(nodes.get(r, {}).get('p') or '')
                g += 1
            if r in roots:
                for s in subs:
                    by_root_hot[r][s] += 1

    rows = []
    for q in only_root:
        dcs = [str(x) for x in (q.get('deepCats') or [])]
        # 章根
        root = None
        for d in dcs:
            r = d; g = 0
            while r and g < 40:
                if r in roots:
                    root = r; break
                r = str(nodes.get(r, {}).get('p') or ''); g += 1
            if root:
                break
        cur_names = '、'.join(str(nodes.get(d, {}).get('n') or d) for d in dcs)
        chap = str(nodes.get(root, {}).get('n') or root) if root else '?'
        hot = by_root_hot.get(root, collections.Counter()).most_common(3)
        cands = ['%s|%s' % (nid, str(nodes.get(nid, {}).get('n') or nid)) for nid, _ in hot]
        while len(cands) < 3:
            cands.append('')
        stem = str(q.get('stem') or '').replace('\n', ' ')[:110]
        rows.append([('core-%s' % q['no']), str(q.get('source') or '')[:60], stem, chap,
                     cur_names, cands[0], cands[1], cands[2], ''])

    # 按章排序：同章聚在一起
    rows.sort(key=lambda r: (r[3], r[0]))

    with io.open(OUT1, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['题号', '来源', '题干(截断)', '所属章', '当前细分',
                    '推荐候选1(id|名)', '推荐候选2', '推荐候选3', '目标节点id(请填写)'])
        w.writerows(rows)

    # 节点字典（只导出有细分空间的：l2root 根及其后代）
    drows = []
    for r in sorted(roots):
        for nid in sorted(subtree(r)):
            drows.append([nid, str(nodes.get(nid, {}).get('n') or ''), '', path_of(nid)])
    with io.open(OUT2, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['节点id', '名称', '', '上级路径'])
        w.writerows(drows)

    print('已导出：')
    print('  %s  （%d 道待归类，按章排序）' % (OUT1, len(rows)))
    print('  %s  （%d 个节点）' % (OUT2, len(drows)))
    print()
    print('用法：在「目标节点id(请填写)」列填节点 id（从字典查），同章可批量填同一个值；')
    print('      填完保存 CSV，我按此批量写回 core_bank.json。')
    return 0


if __name__ == '__main__':
    sys.exit(main())