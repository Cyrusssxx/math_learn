# -*- coding: utf-8 -*-
"""第二轮逐题修正：把「标签与归属不同树」的 9 题归位。
   - 极坐标计算二重积分（标签在 585=二重积分/计算/极坐标/其他）→ 归 **562 二重积分/计算**
   - 以二重积分形式给出的函数（标签在 563 子树）→ 归 **563 二重积分/其他**
   （exam 2003数二真题-22 标签是大观园归档类「数学一专项」，无对应细分类，保持现状）
"""
import json, io

TOOLS = 'D:/ai code/math-note/tools/'
FIX = json.load(io.open(TOOLS + '_catid_fix.json', encoding='utf-8'))

CALC = '562'    # 二重积分 / 计算
OTHER = '563'   # 二重积分 / 其他

core_calc = ['471', '480', '484', '485']
exam_calc = ['2025数二真题-20', '2022数二真题-19', '2020数二真题-19']
core_other = ['519']
exam_other = ['2021数二真题-14']

for no in core_calc:
    FIX['core'][no] = CALC
for k in exam_calc:
    FIX['exam'][k] = CALC
for no in core_other:
    FIX['core'][no] = OTHER
for k in exam_other:
    FIX['exam'][k] = OTHER

json.dump(FIX, io.open(TOOLS + '_catid_fix.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1, sort_keys=True)
print('修正表更新：core %d 条 / exam %d 条' % (len(FIX['core']), len(FIX['exam'])))
print('  极坐标二重积分 → 562：core %s / exam %s' % (core_calc, exam_calc))
print('  二重积分形式函数 → 563：core %s / exam %s' % (core_other, exam_other))