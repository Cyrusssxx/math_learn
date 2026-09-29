# -*- coding: utf-8 -*-
"""把网上找到的配图挂到 core_bank 对应题目上（并要求文件存在）"""
import json, io, os

ATTACH = {
    208: 'data/img/core_fig/no208.png',
    219: 'data/img/core_fig/no219.png',
    220: 'data/img/core_fig/no220.png',
    357: 'data/img/core_fig/no357.png',
    362: 'data/img/core_fig/no362.png',
    380: 'data/img/core_fig/no380.png',
    515: 'data/img/core_fig/no515.png',
}

missing = [v for v in ATTACH.values() if not os.path.exists(os.path.join('pwa', v))]
if missing:
    raise SystemExit(f'图片缺失，中止：{missing}')

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core = json.load(f)

done = []
for p in core:
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            no = q.get('no')
            if no in ATTACH:
                q['img'] = ATTACH[no]
                done.append(no)

with io.open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(core, f, ensure_ascii=False, separators=(',', ':'))

with io.open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    chk = json.load(f)
for no, path in ATTACH.items():
    q = next(q for p in chk for s in p['sections'] for q in s['questions'] if q.get('no') == no)
    assert q.get('img') == path, no
print(f'已挂图题号: {sorted(done)}（共 {len(done)} 题，写回验证通过）')
