from pathlib import Path
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / 'pwa' / 'data' / 'notes.json'
IMG = ROOT / 'pwa' / 'data' / 'img' / 'closed_region_max.svg'
SW = ROOT / 'pwa' / 'sw.js'

TAIL = '  - 3️⃣ 比较：最大的为最大值，最小的为最小值'
ADD = ('\n\n> **流程速览**（点图放大）：内部驻点 → 边界最值 → 比较取值；三步缺一不可。'
       '\n![闭区域最值求解流程](data/img/closed_region_max.svg)')

with open(NOTES, encoding='utf-8', newline='') as f:
    data = json.load(f)
note = next(x for x in data if x.get('id') == '高数5-多元微分')
md = note['md']

assert note['chapters'][-1] == '闭区域最值', 'last chapter changed'
assert len(note['chapters']) == 10, 'chapter count changed'
assert md.count('## 闭区域最值') == 1, 'section duplicated'
assert md.endswith(ADD), 'figure text not at md tail'
assert md[:-len(ADD)].endswith(TAIL), 'original tail disturbed'
assert md.count('closed_region_max.svg') == 1, 'figure link duplicated'

svg = IMG.read_text(encoding='utf-8')
root = ET.fromstring(svg)
assert root.attrib['viewBox'] == '0 0 680 432', 'viewBox changed'
assert 'fill="#FCEBEB"' in svg and 'stroke="#A32D2D"' in svg, 'red warning strip missing'
assert 'AC−B²&lt;0' in svg, 'saddle-point caution missing'
assert not any(ord(ch) < 32 and ch not in '\n\t' for ch in svg), 'C0 control char in svg'
assert "'data/img/closed_region_max.svg'," in SW.read_text(encoding='utf-8'), 'not precached'

print('verify ok: 闭区域最值 section + svg + precache')
