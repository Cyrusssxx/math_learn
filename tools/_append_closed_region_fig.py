from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / 'pwa' / 'data' / 'notes.json'
IMG = ROOT / 'pwa' / 'data' / 'img' / 'closed_region_max.svg'

TAIL = '  - 3️⃣ 比较：最大的为最大值，最小的为最小值'
ADD = ('\n\n> **流程速览**（点图放大）：内部驻点 → 边界最值 → 比较取值；三步缺一不可。'
       '\n![闭区域最值求解流程](data/img/closed_region_max.svg)')

with open(NOTES, encoding='utf-8', newline='') as f:
    data = json.load(f)

note = next((x for x in data if x.get('id') == '高数5-多元微分'), None)
assert note is not None, 'note not found'
md = note['md']
chapters = list(note['chapters'])

assert md.endswith(TAIL), 'md tail changed, refuse to insert'
assert 'closed_region_max.svg' not in md, 'already inserted'
assert '## 闭区域最值' in md, 'target section missing'
assert IMG.exists(), 'svg missing'

note['md'] = md + ADD
assert note['md'].startswith(md), 'prefix rule broken'
assert note['chapters'] == chapters, 'chapters changed'

with open(NOTES, 'w', encoding='utf-8', newline='') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('appended: closed_region_max.svg under 闭区域最值 (md tail), chapters unchanged')
