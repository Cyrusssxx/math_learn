# -*- coding: utf-8 -*-
"""彻底清除 no=432 answer/idea 中的 \\tag{...}（KaTeX 非 display 模式会报错）"""
import json, io, re

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

n = 0
for p in core:
    for s in p['sections']:
        for q in s['questions']:
            if q.get('no') != 432:
                continue
            for k in ('answer', 'idea'):
                v = str(q.get(k) or '')
                if '\\tag' in v:
                    q[k] = re.sub(r'\\tag\{[^}]*\}', '', v)
                    n += 1

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

with io.open(FP, 'r', encoding='utf-8') as f:
    chk = json.load(f)
q432 = next(q for p in chk for s in p['sections'] for q in s['questions'] if q.get('no') == 432)
assert '\\tag' not in str(q432.get('answer', '')), '仍有 tag'
print(f'no=432 已清除 \\tag（处理字段数 {n}），校验通过')
