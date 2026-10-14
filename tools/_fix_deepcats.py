#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""修复 deepCats 漏标（2026-10-14）：
  A 缺失 / B 悬空 / C 错位 → 统一策略：
    · 剔除悬空 id（不在 cat_deep.nodes）
    · 对 catId 能在 l2root 找到细分类树的题：若 deepCats 与该树无交集 → **追加 l2root[catId]**（细分类根）
      （追加而非替换：保留可能有效的旧标签）
    · 修复后保证：deepCats 非空且与所属 L2 的细分类子树有交集 → 点「本级」一定能看到该题
  覆盖四源：exam（应无问题，跳过）/ core / bank / dgy。
  写回保持各文件原格式（core 紧凑单行；bank/dgy 按原 pretty）。
  --dry-run 只报告；默认直接写回（先自动备份到 tools/_bak_deepcats/）。
"""
import io, json, os, sys, collections, shutil, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)
DRY = '--dry-run' in sys.argv


def subtree(root, ch):
    out, stack = set(), [str(root)]
    while stack:
        x = stack.pop()
        if x in out:
            continue
        out.add(x)
        stack.extend(ch.get(x, []))
    return out


def fix_q(q, l2root, nodes, ch):
    """返回 (changed, 动作字符串)"""
    dc = q.get('deepCats')
    dc = [str(x) for x in dc] if isinstance(dc, list) else []
    catIds = [str(c) for c in (q.get('categoryIds') or ([q['catId']] if q.get('catId') is not None else []))]
    # 1) 剔悬空
    clean = [x for x in dc if x in nodes]
    removed = len(dc) - len(clean)
    # 2) 找所属 L2 的细分类根（catIds 里第一个能在 l2root 查到的）
    root = None
    for c in catIds:
        if c in l2root:
            root = l2root[c]
            break
    act = []
    if removed:
        act.append('剔悬空%d' % removed)
    # 3) catId 是 L1/无树 L2 → 在 cat_deep 树内 BFS：catId 自身或其后代中，
    #    第一个出现在 l2root.values() 的节点（例：324 多元微分 → 子树 484 偏导数）
    if not root:
        vals = set(l2root.values())
        for c in catIds:
            if c in nodes:
                stack, seen = [c], set()
                while stack and not root:
                    x = stack.pop(0)
                    if x in seen:
                        continue
                    seen.add(x)
                    if x in vals:
                        root = x
                        act.append('L1下探%s' % c)
                        break
                    stack.extend(ch.get(x, []))
                if root:
                    break
    if root:
        union = subtree(root, ch)
        if not any(x in union for x in clean):
            clean.append(root)
            act.append('补根%s' % root)
    elif not clean:
        act.append('无法补(catId无细分类树)')
    if act and clean:
        q['deepCats'] = clean
        return True, '+'.join(act)
    return False, '+'.join(act) if act else ''


def main():
    deep = json.loads(io.open(P('cat_deep.json'), encoding='utf-8').read())
    nodes = deep.get('nodes', {})
    ch = collections.defaultdict(list)
    for k, v in nodes.items():
        p = str(v.get('p') or '')
        if p:
            ch[p].append(str(k))
    l2root = {str(k): str(v) for k, v in (deep.get('l2root') or {}).items()}

    # 备份
    if not DRY:
        bak = os.path.join(ROOT, 'tools', '_bak_deepcats', time.strftime('%Y%m%d-%H%M%S'))
        os.makedirs(bak, exist_ok=True)
        for f in ('core_bank.json', 'bank_questions.json', 'dgy_items.json'):
            src = P(f)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(bak, f))
        print('已备份到', bak)

    totals = collections.Counter()
    for fname, kind in (('core_bank.json', 'core'), ('bank_questions.json', 'bank'), ('dgy_items.json', 'dgy')):
        path = P(fname)
        raw = io.open(path, encoding='utf-8').read()
        d = json.loads(raw)
        changed = collections.Counter()
        samples = []
        if kind == 'core':
            q_iters = [[q for s in d[0]['sections'] for q in s.get('questions', [])]]
        elif kind == 'bank':
            q_iters = [d.get('items', [])]          # bank 是 items 平铺，无 sections 层级
        else:
            papers = d if isinstance(d, list) else d.get('papers', [])
            q_iters = [[q for s in p.get('sections', []) for q in s.get('questions', [])] for p in papers]
        for qs in q_iters:
            for q in qs:
                    ok, act = fix_q(q, l2root, nodes, ch)
                    if ok:
                        changed['修'] += 1
                        for tag in act.split('+'):
                            if tag.startswith('剔悬空'):
                                changed['剔悬空'] += 1
                            if tag.startswith('补根'):
                                changed['补根'] += 1
                        if len(samples) < 4:
                            samples.append('core-%s %s' % (q['no'], act) if kind == 'core' else '%s' % act)
                    totals[fname] += 1 if ok else 0
        print('【%s】修改 %d 题（剔悬空 %d、补根 %d）' % (
            fname, changed['修'], changed['剔悬空'], changed['补根']))
        for s in samples:
            print('     ', s)
        if not DRY and changed['修']:
            # 保持原格式：探测 raw 是否 pretty（含缩进换行），并做 JSON 往返自检
            is_pretty = '\n  ' in raw[:800]
            compact = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
            pretty = json.dumps(d, ensure_ascii=False, indent=1)
            out = pretty if is_pretty else compact
            assert json.loads(out) == d, '往返自检失败: ' + fname
            assert len(json.loads(out)) == len(d)
            io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
            print('     已写回（格式 %s，往返自检 OK）' % ('pretty' if is_pretty else '紧凑'))
    print()
    print('合计修改题数：', sum(totals.values()), dict(totals))
    if DRY:
        print('（dry-run，未写文件）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
