#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""笔记主页排版体检：目录匹配度 / 锚点死链 / 结构规范 / 数学与图片完整性

用法: python tools/_audit_notes_layout.py [--json 输出.json]
"""
import io, json, re, sys, os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES = os.path.join(ROOT, 'pwa', 'data', 'notes.json')
PWA = os.path.join(ROOT, 'pwa')

R = io.open(NOTES, encoding='utf-8').read()
notes = json.loads(R)

def strip_cmt(s):
    return re.sub(r'<!--.*?-->', '', s)

# ---------------- 每篇体检 ----------------
issues = defaultdict(list)      # id -> [(级别, 分类, 说明)]
def add(nid, lvl, cat, msg):
    issues[nid].append((lvl, cat, msg))

for n in notes:
    nid = n['id']
    md = n['md']
    chaps = n.get('chapters') or []
    raw_lines = md.split('\n')

    # 1) 正文 ## 标题（去注释、去尾空白）
    h2 = []
    for i, l in enumerate(raw_lines):
        ll = strip_cmt(l).rstrip()
        if ll.startswith('## '):
            h2.append((i + 1, ll[3:].strip()))

    # ---- A. 目录匹配度 ----
    if len(h2) != len(chaps):
        add(nid, 'P0', '目录', f'章节数不符：正文 ## {len(h2)} 个 / chapters {len(chaps)} 项')
    for k in range(min(len(h2), len(chaps))):
        if h2[k][1] != chaps[k]:
            add(nid, 'P1', '目录', f'第 {k+1} 项文案不一致：正文「{h2[k][1]}」(L{h2[k][0]}) vs chapters「{chaps[k]}」')
    # 顺序整体错位检测（去掉编号前缀后比对集合）
    def norm(s):
        return re.sub(r'^[（(【\[]?\s*[0-9一二三四五六七八九十]+\s*[、.．)）】\]]\s*', '', s).strip()
    if len(h2) == len(chaps) and h2 and [x[1] for x in h2] != chaps:
        a, b = [norm(x[1]) for x in h2], [norm(x) for x in chaps]
        if a == b:
            add(nid, 'P2', '目录', '仅编号前缀差异（标题带「一、」而 chapters 不带），渲染出的目录少编号')
        elif sorted(a) == sorted(b):
            add(nid, 'P1', '目录', '章节顺序与 chapters 不一致（内容会跳错章）')

    # ---- B. 锚点 ----
    anchors = set()
    figids = set()          # figure 的 id 是渲染时按图片名自动生成的，不是 {#id}，也算合法跳转目标
    for i, l in enumerate(raw_lines):
        s = strip_cmt(l).rstrip()
        m = re.match(r'\s*\{#([A-Za-z0-9_\-]+)\}\s*$', s)
        if m: anchors.add(m.group(1))
        m2 = re.match(r'\s*- \{#([A-Za-z0-9_\-]+)\}\s', s)
        if m2: anchors.add(m2.group(1))
        m3 = re.match(r'^!\[(.*?)\]\((.+?)\)$', s.strip())
        if m3:
            base = os.path.basename(m3.group(2))
            base = re.sub(r'\.[^.]+$', '', base)
            figids.add('fig-' + re.sub(r'[^A-Za-z0-9_\-]', '_', base))
    anchors |= figids
    dup = [k for k, v in Counter(re.findall(r'\{#([A-Za-z0-9_\-]+)\}', strip_cmt(md))).items() if v > 1]
    if dup:
        add(nid, 'P1', '锚点', f'锚点 id 重复 {len(dup)} 个：{dup[:6]}')
    links = re.findall(r'\[[^\]]*\]\(#([A-Za-z0-9_\-]+)\)', strip_cmt(md))
    dead = sorted(set(l for l in links if l not in anchors))
    if dead:
        add(nid, 'P0', '锚点', f'死链 {len(dead)} 个（跳转目标不存在）：{dead[:8]}')
    orphan = sorted(a for a in anchors if a not in links)
    if orphan:
        add(nid, 'P2', '锚点', f'孤儿锚点 {len(orphan)} 个（无人跳转）：{orphan[:8]}')

    # ---- C. 结构 ----
    # ::: 配对
    stack = []
    for i, l in enumerate(raw_lines):
        t = strip_cmt(l).strip()
        if re.match(r'^:::\s*(fold|nav|点睛)', t): stack.append((i + 1, t[:14]))
        elif t == ':::':
            if not stack: add(nid, 'P0', '结构', f'L{i+1} 出现多余的 :: 闭合（无对应开标签）')
            else: stack.pop()
    for ln, t in stack:
        add(nid, 'P0', '结构', f'L{ln} 「:::{t}」未闭合（整块内容会被吞掉）')

    # 列表缩进
    li_lv = defaultdict(int)
    for i, l in enumerate(raw_lines):
        m = re.match(r'^(\s*)- (.*)$', strip_cmt(l))
        if m:
            if len(m.group(1)) % 2: add(nid, 'P2', '结构', f'L{i+1} 列表缩进 {len(m.group(1))} 空格（非 2 的倍数）')
            li_lv[len(m.group(1))] += 1
        elif re.match(r'^\s*-\S', strip_cmt(l)) and not re.match(r'^\s*-{3,}\s*$', strip_cmt(l)):
            add(nid, 'P2', '结构', f'L{i+1} 「-」后缺空格：{strip_cmt(l).strip()[:40]}')

    # 表格列数
    i = 0
    while i < len(raw_lines):
        if strip_cmt(raw_lines[i]).strip().startswith('|'):
            cols, start = [], i + 1
            while i < len(raw_lines) and strip_cmt(raw_lines[i]).strip().startswith('|'):
                s = strip_cmt(raw_lines[i]).strip()
                # 忽略 $...$ 里的 |
                cells, cur, inm = [], '', False
                body = s.strip('|')
                for ch in body:
                    if ch == '$': inm = not inm
                    if ch == '|' and not inm: cells.append(cur.strip()); cur = ''
                    else: cur += ch
                cells.append(cur.strip())
                cols.append(len(cells)); i += 1
            uniq = set(cols)
            if len(uniq) > 1:
                add(nid, 'P1', '表格', f'L{start} 起表格列数不一致：{[ (start+k, c) for k,c in enumerate(cols)]}')
            elif len(uniq) == 1 and cols and cols[0] < 2:
                add(nid, 'P2', '表格', f'L{start} 表格只有 1 列')
        else:
            i += 1

    # ---- D. 数学 / 图片 / 其它 ----
    # 行内 $ 配平（按行）
    for i, l in enumerate(raw_lines):
        s = strip_cmt(l)
        # 去掉 $$ 块标记后统计单 $
        t = s.replace('$$', '')
        if t.count('$') % 2:
            add(nid, 'P1', '公式', f'L{i+1} 行内 $ 不配平（奇数个）：{s.strip()[:60]}')
    if md.count('$$') % 2:
        add(nid, 'P0', '公式', f'$$ 总数为奇数（{md.count("$$")}），显示块未配平')

    # 图片路径
    for i, l in enumerate(raw_lines):
        for alt, src in re.findall(r'!\[(.*?)\]\((.+?)\)', strip_cmt(l)):
            p = src if src.startswith('http') else os.path.join(PWA, src.lstrip('./'))
            if not src.startswith('http') and not os.path.exists(p):
                add(nid, 'P0', '图片', f'L{i+1} 图片不存在：{src}')

    # 行尾空格 / 连续空行
    trail = sum(1 for l in raw_lines if l != l.rstrip())
    if trail: add(nid, 'P2', '排版', f'{trail} 行有行尾空格')
    blank3 = len(re.findall(r'\n\n\n+', md))
    if blank3: add(nid, 'P2', '排版', f'{blank3} 处连续 3+ 空行')

    # 空章节（## 后紧接 ##）
    for k in range(len(h2) - 1):
        if h2[k + 1][0] - h2[k][0] <= 1:
            add(nid, 'P1', '内容', f'空章节：L{h2[k][0]}「{h2[k][1]}」后面紧接下一个 ##')
    # 末章是否为空
    if h2 and len(raw_lines) - h2[-1][0] < 1:
        add(nid, 'P1', '内容', f'空章节：最后一章「{h2[-1][1]}」无内容')

# ---------------- 汇总输出 ----------------
LEVEL_ORDER = {'P0': 0, 'P1': 1, 'P2': 2}
total = Counter()
by_cat = Counter()
for nid, lst in issues.items():
    for lv, cat, _ in lst:
        total[lv] += 1; by_cat[cat] += 1

print('=' * 70)
print(f'笔记排版体检：{len(notes)} 篇')
print(f'  P0 严重 = {total["P0"]}    P1 需修 = {total["P1"]}    P2 建议 = {total["P2"]}')
print(f'  按分类：{dict(by_cat.most_common())}')
print('=' * 70)

order = sorted(issues.items(), key=lambda kv: (-sum(1 for x in kv[1] if x[0] == 'P0'),
                                               -sum(1 for x in kv[1] if x[0] == 'P1'),
                                               -len(kv[1])))
for nid, lst in order:
    lst = sorted(lst, key=lambda x: LEVEL_ORDER[x[0]])
    print(f'\n### {nid}   ({len(lst)} 项)')
    for lv, cat, msg in lst:
        print(f'   [{lv}][{cat}] {msg}')

if '--json' in sys.argv:
    out = sys.argv[sys.argv.index('--json') + 1]
    io.open(out, 'w', encoding='utf-8').write(
        json.dumps({k: v for k, v in issues.items()}, ensure_ascii=False, indent=1))
    print(f'\n已写出 {out}')
