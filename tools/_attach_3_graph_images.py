# -*- coding: utf-8 -*-
"""给 3 道有真题图的配图题挂题干图"""
import json, io, os

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

ATTACH = {
    379: 'data/img/exam_fig/2007_q03.png',
    356: 'data/img/exam_fig/2010_q18.png',
    605: 'data/img/exam_fig/2003_q19.png',
}

missing = [rel for rel in ATTACH.values() if not os.path.exists(os.path.join('pwa', rel))]
if missing:
    raise SystemExit(f'文件缺失，中止: {missing}')

attached = []
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            if q.get('no') in ATTACH:
                q['img'] = ATTACH[q['no']]
                attached.append(q['no'])

with io.open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

# 验证
with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    chk = json.load(f)
for no in ATTACH:
    q = next(q for p in chk for s in p['sections'] for q in s['questions'] if q.get('no') == no)
    assert q.get('img') == ATTACH[no], no
print(f'已挂题干图题号: {sorted(attached)}（文件均存在，写回验证通过）')
