# -*- coding: utf-8 -*-
"""逐题人工判定的修正：把「无法判定」的题按大观园标签正确落位（二重积分/其他 = 563）。
   追加进 tools/_catid_fix.json 后由 _apply_catid_fix.py 统一应用。"""
import json, io

TOOLS = 'D:/ai code/math-note/tools/'
FIX = json.load(io.open(TOOLS + '_catid_fix.json', encoding='utf-8'))

TARGET = '563'          # 本库 L2「二重积分 / 其他」

# core：题号 → 563（人工逐题判定）
core_add = ['60', '510', '511', '509', '506', '513', '514', '515', '517', '520', '521', '604']
for no in core_add:
    FIX['core'][no] = TARGET

# exam：卷-题号 → 563
exam_add = ['2015数二真题-6', '2010数二真题-6', '2006数二真题-11']
for k in exam_add:
    FIX['exam'][k] = TARGET

json.dump(FIX, io.open(TOOLS + '_catid_fix.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1, sort_keys=True)
print('修正表已更新：core %d 条 / exam %d 条' % (len(FIX['core']), len(FIX['exam'])))
print('  本次人工追加：core %s' % core_add)
print('              exam %s' % exam_add)