# -*- coding: utf-8 -*-
"""精确修复 2020 数二第15题 answer：
   ① L11 裸公式行 → 包成 $$...$$
   ② 删除其后的多余孤立 $$（它把「故/代入…」正文吞进显示块，导致 KaTeX 遇到 $ 崩溃 → 逐字裸奔）
   修完复检（无 E1/E2/E3、无裸公式行）再写盘。
"""
import json, io, re, sys
sys.path.insert(0, 'D:/ai code/math-note/tools')
from _fix_formula_safe import scan_state, bare_lines            # noqa: E402

EXAM = 'D:/ai code/math-note/pwa/data/exam.json'
ex = json.load(io.open(EXAM, encoding='utf-8'))

q15 = None
for vol in ex:
    if str(vol.get('year')) == '2020':
        for sec in vol.get('sections', []):
            for q in sec.get('questions', []):
                if q.get('no') == 15:
                    q15 = q
assert q15 is not None
v = q15['answer']
print('修复前：E=%s 裸行=%s' % (len(scan_state(v)[0]), len(bare_lines(v, scan_state(v)[2]))))

# ① 裸公式行 → 包 $$
BARE = '\\frac{y}{x}=e^{-1}\\cdot e^{\\frac t2+o(t)}=e^{-1}\\left(1+\\frac t2+o(t)\\right).'
assert BARE in v, '未找到目标裸公式行'
v2 = v.replace(BARE, '$$\n' + BARE + '\n$$', 1)

# ② 删除该行之后、下一个有内容行之前的那个「孤立 $$」（多余开块）
lines = v2.split('\n')
tgt = next(i for i, L in enumerate(lines) if L.strip() == BARE)
# 找 tgt 之后第一个非空行
j = tgt + 1
while j < len(lines) and not lines[j].strip():
    j += 1
assert lines[j].strip() == '$$', '预期位置不是孤立 $$，实际=%r' % lines[j]
lines[j] = None            # 标记删除
v3 = '\n'.join(L for L in lines if L is not None)

e, _, sp = scan_state(v3)
bl = bare_lines(v3, sp)
print('修复后：E=%s 裸行=%s' % (len(e), len(bl)))
assert not e and not bl, '复检未过，不写盘：%s %s' % (e, bl)

q15['answer'] = v3
with io.open(EXAM, 'w', encoding='utf-8', newline='') as f:
    json.dump(ex, f, ensure_ascii=False, separators=(',', ':'))

# 读回确认
ex2 = json.load(io.open(EXAM, encoding='utf-8'))
q = None
for vol in ex2:
    if str(vol.get('year')) == '2020':
        for sec in vol.get('sections', []):
            for x in sec.get('questions', []):
                if x.get('no') == 15:
                    q = x
e2, _, sp2 = scan_state(q['answer'])
print('写盘复查：E=%d 裸行=%d  单行格式=%s' % (len(e2), len(bare_lines(q['answer'], sp2)),
      io.open(EXAM, encoding='utf-8').read().count('\n') == 0))
print()
print('=== 修复后 L（含 故/代入/结果 段）===')
for i, L in enumerate(q['answer'].split('\n')):
    if 8 <= i <= 20:
        print('L%-3d (%d$) %s' % (i, L.count('$'), L[:100]))
