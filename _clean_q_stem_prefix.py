# -*- coding: utf-8 -*-
"""清理 core_bank 题干开头的源书排版残留：题号「5.」「(2)」、「【例3.34】」、「【14】」，
以及两条转写备注（40 的内部编号说明、50 的不确定标注）。

规则
 1. `【…】`（例号/题号，≤14 字）→ 删；紧跟的「（2020，数三）」年份标注也删（题源已在 source 字段）。
 2. `数字.` → 删。
 3. `(n)` / `（n）` → **仅当正文里没有下一序号 (n+1)** 时删；有则为多小问结构（如 (1)…(2)…），保留。
 4. 40 题干末尾的「【注：题号为 (2)…】」→ 删。
 5. 50 题干末尾的「【不确定：…】」→ 移到 tips.gs，题干里删掉（质量标注不该出现在题面上）。
用法：python _clean_q_stem_prefix.py [--apply]
"""
import json, io, re, sys

PATH = 'pwa/data/core_bank.json'
APPLY = '--apply' in sys.argv

d = json.load(io.open(PATH, encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]

RE_HEAD = re.compile(
    r'^\s*(?P<tag>【[^】]{1,14}】)\s*(?P<year>[（(]\s*\d{4}\s*[，,][^)）]{1,12}[)）])?\s*'
    r'|^\s*(?P<num>\d+)\.\s*'
    r'|^\s*(?P<paren>[（(]\s*(?P<pn>\d+)\s*[)）])\s*'
)
RE_NOTE40 = re.compile(r'【注：题号为[^】]*】\s*$')
RE_UNSURE = re.compile(r'【不确定：[^】]*】\s*$')

changes = []
for q in qs:
    st = q.get('stem') or ''
    orig = st
    note_moved = none40 = none50 = ''

    # 4) 40 的内部编号备注
    if RE_NOTE40.search(st):
        none40 = RE_NOTE40.search(st).group(0).strip()
        st = RE_NOTE40.sub('', st)

    # 5) 50 的不确定标注 → 移到 tips
    m50 = RE_UNSURE.search(st)
    if m50:
        note_moved = m50.group(0).strip('【】')
        st = RE_UNSURE.sub('', st)

    # 1~3) 头部前缀
    m = RE_HEAD.match(st)
    if m:
        if m.group('tag'):
            st = st[m.end():]
        elif m.group('num'):
            st = st[m.end():]
        elif m.group('paren'):
            n = int(m.group('pn'))
            rest = st[m.end():]
            # 正文里是否还有下一个序号（决定是不是多小问）
            has_next = bool(re.search(r'[（(]\s*%d\s*[)）]' % (n + 1), rest))
            if not has_next:
                st = rest
    if st != orig:
        st = st.lstrip()          # 只在真的删了前缀时才去前导空格，避免纯空格改动进 diff
    if st != orig:
        changes.append((q['no'], orig, st, none40, note_moved))

print('待改动 %d 条\n' % len(changes))
for no, old, new, n40, n50 in changes:
    head_old = old[:34].replace('\n', ' ')
    head_new = new[:34].replace('\n', ' ')
    extra = ''
    if n40: extra += '  [删备注]'
    if n50: extra += '  [备注移 tips]'
    print(f'  {no:<5} {head_old!r:<40} → {head_new!r}{extra}')

if APPLY:
    for no, old, new, n40, n50 in changes:
        q = next(x for x in qs if x['no'] == no)
        q['stem'] = new
        if n50:
            tips = q.setdefault('tips', {})
            prev = tips.get('gs') or ''
            add = '⚠️ 原图 A、B 选项的极限下标可能是 $x\\to0^+$（书上加号较小），此题按 $x\\to0$ 理解需谨慎核对。'
            tips['gs'] = (prev + ('\n\n' if prev else '') + add).strip()
    io.open(PATH, 'w', encoding='utf-8', newline='').write(json.dumps(d, indent=1, ensure_ascii=False))
    print('\n已写回 core_bank.json')
else:
    print('\nDRY-RUN：未写盘，加 --apply 执行')
