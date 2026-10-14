#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""用「大观答案书签」归类核心题库未细分题（只挂到章根的 275 道）。

方法（协同归类，不引入新分类体系）：
  1. 书签条目剥离编号前缀后建题源索引（修掉之前 a) 前缀导致的 0 命中 bug）
  2. 未细分题用 source 命中书签条目 → 得到它在书签里的「最细父分类」(L5/L4)
  3. 统计该书签分类下**其他已细分的 core 题**的 deepCats → 投票得票数最多的子节点
  4. 把未细分题挂到投票出的子节点（追加，保留原章根不动，保证不丢可见性）
  5. 无命中/无邻居投票 → 不动（宁缺勿错）

--apply 才写回；默认 dry-run 只报告。
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


def norm(s):
    """题源标识归一化：剥离编号前缀 + 去空格/版本/第题/括号"""
    s = strip_pfx(s)
    s = re.sub(r'\s+', '', s).lower()
    s = re.sub(r'^(26|25|24)版', '', s)
    s = s.replace('🐙', '')
    s = re.sub(r'[（(].*?[)）]', '', s)      # 去括号注释（含「重点」）
    s = s.replace('第', '').replace('题', '')
    return s.strip(';,').strip()


def main():
    apply = '--apply' in sys.argv
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep['nodes']
    l2root = {str(k): str(v) for k, v in deep.get('l2root', {}).items()}
    roots = set(l2root.values())

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
    print('未细分（只挂章根）：%d 道' % len(only_root))

    # ---- 建书签索引：norm(条目) -> [最细父分类路径] ----
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
            # 条目可能含多条题源（分号分隔）
            for part in re.split(r'[;；]', title):
                k = norm(part)
                if k:
                    src_index[k].append({'parents': path[:-1], 'page': page})
    print('书签题源索引：%d 条（剥离前缀后）' % len(src_index))

    # ---- 已细分题按「书签父分类」统计 deepCats 投票 ----
    # 先给所有 core 题算：它命中哪些书签父分类（用于建投票表和找邻居）
    def qid_key(q):
        return 'core-%s' % q['no']

    def hit_toc(q):
        out = []
        for s in re.split(r'[;；]', str(q.get('source') or '')):
            k = norm(s)
            if k and k in src_index:
                for h in src_index[k]:
                    # 最细父分类 = 路径里最后 2 层（L5 知识点 / L4 组）
                    out.append(tuple(h['parents'][-2:]))
        return out

    refined = [q for q in qs if q not in only_root]
    # 投票表：书签父分类 -> Counter(deepCats 子节点)
    vote = collections.defaultdict(collections.Counter)
    for q in refined:
        dcs = [str(x) for x in (q.get('deepCats') or [])]
        # 只投「非根节点」的子节点（才是细分）
        subs = [d for d in dcs if depth_to_root(d) not in (0, None)]
        for key in hit_toc(q):
            for s in subs:
                vote[key][s] += 1
    print('已细分题里，能命中书签并建立投票的：%d 个父分类' % len(vote))

    # ---- 逐题归类 ----
    plan = []
    nohit, novote = [], []
    for q in only_root:
        keys = hit_toc(q)
        if not keys:
            nohit.append(q['no']); continue
        # 汇总该题命中的父分类的投票
        agg = collections.Counter()
        for k in keys:
            agg.update(vote.get(k, collections.Counter()))
        if not agg:
            novote.append(q['no']); continue
        # 取得票最多的子节点；要求票数 >= 2 或唯一最高（避免噪声）
        top, cnt = agg.most_common(1)[0]
        if cnt < 2 and len(agg) > 1:
            novote.append(q['no']); continue
        # 该子节点必须属于本题 catId 的章（避免跨章错挂）
        qroots = set()
        for d in [str(x) for x in (q.get('deepCats') or [])]:
            # 上溯到根
            cur = d; g = 0
            while cur and g < 40:
                if cur in roots:
                    qroots.add(cur); break
                cur = str(nodes.get(cur, {}).get('p') or ''); g += 1
        tcur = top; troots = set(); g = 0
        while tcur and g < 40:
            if tcur in roots:
                troots.add(tcur); break
            tcur = str(nodes.get(tcur, {}).get('p') or ''); g += 1
        if not (qroots & troots):
            novote.append(q['no']); continue   # 跨章，拒绝
        plan.append((q['no'], top, cnt, str(nodes[top].get('n') or '')))
    print()
    print('=== 归类计划 ===')
    print('  可归类（有邻居投票且同章）：%d 道' % len(plan))
    print('  source 未命中书签：%d 道' % len(nohit))
    print('  命中但无有效投票（邻居少/跨章）：%d 道' % len(novote))
    print()
    print('  样例：')
    for no, nid, cnt, nm in plan[:12]:
        print('    core-%s → 挂「%s」(节点%s，票数%d)' % (no, nm, nid, cnt))

    if not apply:
        print('\n（dry-run，未写库。加 --apply 执行）')
        doc.close()
        return 0

    # ---- 写回：追加子节点（保留原章根，不丢可见性）----
    bak = os.path.join(ROOT, 'tools', '_bak_deepcats', time.strftime('%Y%m%d-%H%M%S') + '-refine')
    os.makedirs(bak, exist_ok=True)
    shutil.copy2(P('core_bank.json'), os.path.join(bak, 'core_bank.json'))
    print('\n已备份', bak)

    byno = {q['no']: q for q in qs}
    done = 0
    for no, nid, cnt, nm in plan:
        q = byno[no]
        dcs = [str(x) for x in (q.get('deepCats') or [])]
        if nid not in dcs:
            dcs.append(nid)
            q['deepCats'] = dcs
            done += 1
    out = json.dumps(core, ensure_ascii=False, separators=(',', ':'))
    assert json.loads(out) == core, '往返自检失败'
    io.open(P('core_bank.json'), 'w', encoding='utf-8', newline='\n').write(out)
    print('已写回 core_bank.json，新增细分挂靠 %d 道（往返自检 OK）' % done)
    doc.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())