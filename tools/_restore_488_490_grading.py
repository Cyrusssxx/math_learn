# -*- coding: utf-8 -*-
"""恢复 no=488/490 的「评分参考」段（保持与全库其余 24+ 处一致）"""
import json, io

FP = 'pwa/data/core_bank.json'
with io.open(FP, 'r', encoding='utf-8') as f:
    core = json.load(f)

G488 = (
    '\n\n📋 **评分参考（满分 10 分）｜按考研数学阅卷通用规则估算**\n\n'
    '① 对称性去奇函数项 $x$，剩 $\\iint\\frac y{\\sqrt{x^2+y^2}}$ — **3 分**（结构分） '
    '② 极坐标定区域 $\\theta\\in[\\frac\\pi4,\\frac{3\\pi}4],\\ r\\le\\sin^2\\theta$ — **3 分**（关键推导） '
    '③ 化简为 $\\frac12\\int\\sin^5\\theta\\,d\\theta$ 计算 — **3 分**（关键推导） '
    '④ 结果 $\\frac{43\\sqrt2}{120}$ — **1 分**'
)
G490 = (
    '\n\n📋 **评分参考（满分 12 分）｜按考研数学阅卷通用规则估算**\n\n'
    '① 极坐标化区域 $r=\\sqrt{\\cos2\\theta}$、$\\theta\\in[0,\\frac\\pi4]$ — **3 分**（结构分） '
    '② 化为 $\\int_0^{\\pi/4}\\frac{\\cos^22\\theta}4\\cdot\\frac{\\sin2\\theta}2\\,d\\theta$ — **4 分**（关键推导） '
    '③ 换元 $u=\\cos2\\theta$ 积分 — **4 分**（关键推导） '
    '④ 结果 $\\dfrac1{48}$ — **1 分**'
)

for p in core:
    for s in p['sections']:
        for q in s['questions']:
            no = q.get('no')
            if no == 488 and '阅卷' not in str(q.get('answer') or ''):
                q['answer'] = str(q.get('answer') or '').rstrip() + G488
            if no == 490 and '阅卷' not in str(q.get('answer') or ''):
                q['answer'] = str(q.get('answer') or '').rstrip() + G490

with io.open(FP, 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

for p in core:
    for s in p['sections']:
        for q in s['questions']:
            if q.get('no') in (488, 490):
                a = str(q.get('answer') or '')
                print(f"no={q.get('no')}: 含评分段={'阅卷' in a} | 长度={len(a)} | $$ 数={a.count('$$')}")
