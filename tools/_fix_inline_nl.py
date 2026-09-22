# -*- coding: utf-8 -*-
# 暴力修复：行内 $...$ 内的真实换行删除（显示块 $$ 不动）
import json, io, re

P = 'D:/ai code/math-note/pwa/data/exam.json'
exam = json.load(io.open(P, encoding='utf-8'))
VOLS = {'2021数二真题', '2022数二真题', '2023数二真题', '2024数二真题', '2025数二真题', '2026数二真题'}

# 行内公式：$ 开头、非 $$、内容可能跨行（换行在 $ 内）→ 去换行
INLINE = re.compile(r'(?<!\$)\$([\s\S]*?)\$(?!\$)', re.M)


def fix_inline_nl(s):
    def repl(m):
        inner = m.group(1)
        # 只处理含真实换行的（否则原样）
        if '\n' not in inner:
            return m.group(0)
        # 去换行（转空格）
        return '$' + inner.replace('\n', '') + '$'
    return INLINE.sub(repl, s)


n = 0
for v in exam:
    if v['id'] not in VOLS:
        continue
    for sec in v.get('sections', []):
        for q in sec.get('questions', []):
            for f in ('stem', 'answer', 'idea', 'tips'):
                t = q.get(f) or ''
                if isinstance(t, dict):
                    nv = {}
                    for k, val in t.items():
                        s = str(val)
                        s2 = fix_inline_nl(s)
                        nv[k] = s2
                        if s2 != s:
                            n += 1
                    q[f] = nv
                else:
                    s2 = fix_inline_nl(t)
                    if s2 != t:
                        q[f] = s2
                        n += 1

with io.open(P, 'w', encoding='utf-8', newline='') as fp:
    json.dump(exam, fp, ensure_ascii=False, separators=(',', ':'))
print('修复字段数:', n)
