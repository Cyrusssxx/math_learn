# -*- coding: utf-8 -*-
"""1) 修复 no=25（截断）/ no=29（啰嗦+公式未闭合）
   2) 批量修正【答案】【答案】重复
   3) 检查题号/qid 冲突（排查"笔记串题"）
"""
import json, io, os

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)


def find(no):
    return next(q for p in core for s in p['sections'] for q in s['questions'] if q.get('no') == no)


# ============ 1. no=25：补全被截断的解析 ============
q25 = find(25)
ans25 = (
    '【答案】$2$\n'
    '对根式作有理化（分子分母同乘共轭因子）：\n'
    '$$\n'
    '\\sqrt{n+3\\sqrt n}-\\sqrt{n-\\sqrt n}\n'
    '=\\frac{(n+3\\sqrt n)-(n-\\sqrt n)}{\\sqrt{n+3\\sqrt n}+\\sqrt{n-\\sqrt n}}\n'
    '=\\frac{4\\sqrt n}{\\sqrt{n+3\\sqrt n}+\\sqrt{n-\\sqrt n}}.\n'
    '$$\n'
    '分子分母同除以 $\\sqrt n$：\n'
    '$$\n'
    '\\frac{4}{\\sqrt{1+\\frac{3}{\\sqrt n}}+\\sqrt{1-\\frac{1}{\\sqrt n}}}\n'
    '\\xrightarrow[n\\to\\infty]{}\\frac{4}{1+1}=2.\n'
    '$$\n'
    '所以极限为 $2$。'
)
idea25 = (
    '**思路**：$\\infty-\\infty$ 型根式差 → 有理化后提 $\\sqrt n$。\n'
    '① 乘共轭因子：$\\frac{4\\sqrt n}{\\sqrt{n+3\\sqrt n}+\\sqrt{n-\\sqrt n}}$。\n'
    '② 同除 $\\sqrt n$，分母 $\\to1+1=2$，分子 $=4$。\n'
    '③ 极限 $=4/2=2$。'
)
q25['answer'] = ans25
q25['idea'] = idea25

# ============ 2. no=29：单一方法、步骤完整不啰嗦、修复 $$ 未闭合 ============
q29 = find(29)
ans29 = (
    '【答案】$e^{\\frac{n+1}{2}}$\n'
    '这是 $1^{\\infty}$ 型未定式。取对数，记所求极限为 $L$，则\n'
    '$$\n'
    '\\ln L=\\lim_{x\\to0}\\frac{1}{x}\\ln\\frac{\\mathrm e^{x}+\\mathrm e^{2x}+\\cdots+\\mathrm e^{nx}}{n}.\n'
    '$$\n'
    '**第一步：底数分离出 $1$**\n'
    '$$\n'
    '\\frac{\\mathrm e^{x}+\\mathrm e^{2x}+\\cdots+\\mathrm e^{nx}}{n}\n'
    '=1+\\frac{1}{n}\\sum_{k=1}^{n}(\\mathrm e^{kx}-1),\n'
    '\\qquad \\frac{1}{n}\\sum_{k=1}^{n}(\\mathrm e^{kx}-1)\\to0\\ (x\\to0).\n'
    '$$\n'
    '**第二步：用等价无穷小代换**\n'
    '由 $\\ln(1+t)\\sim t$、$\\mathrm e^{kx}-1\\sim kx\\ (x\\to0)$：\n'
    '$$\n'
    '\\ln L=\\lim_{x\\to0}\\frac{1}{x}\\cdot\\frac{1}{n}\\sum_{k=1}^{n}(\\mathrm e^{kx}-1)\n'
    '=\\frac{1}{n}\\sum_{k=1}^{n}\\lim_{x\\to0}\\frac{kx}{x}\n'
    '=\\frac{1}{n}\\cdot\\frac{n(n+1)}{2}=\\frac{n+1}{2}.\n'
    '$$\n'
    '**第三步：还原**\n'
    '$$\n'
    'L=\\mathrm e^{\\frac{n+1}{2}}.\n'
    '$$\n'
)
idea29 = (
    '**思路**：$1^\\infty$ 型 → 取对数化为 $\\frac00$ 型，再用等价无穷小。\n'
    '① 取对数：$\\ln L=\\lim\\frac1x\\ln\\frac{\\sum_{k=1}^n e^{kx}}{n}$。\n'
    '② 底数写成 $1+\\frac1n\\sum(e^{kx}-1)$，用 $\\ln(1+t)\\sim t$、$e^{kx}-1\\sim kx$。\n'
    '③ $\\ln L=\\frac1n\\sum k=\\frac{n+1}2$，故 $L=e^{\\frac{n+1}2}$。'
)
q29['answer'] = ans29
q29['idea'] = idea29

# ============ 3. 批量修正【答案】【答案】重复（全库 core 内） ============
fixed_dup = []
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            a = q.get('answer')
            if isinstance(a, str) and '【答案】【答案】' in a:
                q['answer'] = a.replace('【答案】【答案】', '【答案】', 1)
                fixed_dup.append(q.get('no'))

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

# ============ 4. 检查题号/qid 唯一性（笔记串题排查） ============
from collections import Counter
with io.open(FP, 'r', encoding='utf-8') as f:
    chk = json.load(f)
nos = Counter()
for p in chk:
    for s in p['sections']:
        for q in s['questions']:
            nos[q.get('no')] += 1
dup_no = [n for n, c in nos.items() if c > 1]
print('core_bank 内题号重复:', dup_no if dup_no else '无')

# 与 xd_bank 的 qid 冲突（考虑 linkedQid 后）
xd_fp = 'pwa/data/xd_bank.json'
conflicts = []
if os.path.exists(xd_fp):
    with io.open(xd_fp, 'r', encoding='utf-8') as f:
        xd = json.load(f)
    core_qids = {}
    for p in chk:
        for s in p['sections']:
            for q in s['questions']:
                qid = q.get('linkedQid') or f"core-{q.get('no')}"
                core_qids.setdefault(qid, []).append(q.get('no'))
    for p in xd:
        for s in p['sections']:
            for q in s['questions']:
                qid = q.get('linkedQid') or f"xd-{q.get('no')}"
                if qid in core_qids:
                    conflicts.append((qid, core_qids[qid], q.get('no')))
    print('core 与 xd 的 qid 冲突:', conflicts[:10] if conflicts else '无')

print(f'no=25 与 no=29 已重写；批量修正【答案】重复题号: {fixed_dup}')
