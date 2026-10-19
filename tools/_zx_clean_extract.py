# -*- coding: utf-8 -*-
"""按 PDF 块坐标精确切出每道臻选题的干净题干。
版面规律：灰条「#NNN 目录 题源」与题干块在 y 轴上严格分界 ——
题干块全部落在「本条灰条底边」与「下一条灰条顶边」之间。
"""
import fitz, re, json, io

PDF = 'E:/Desktop/大观/【⚠️】大观严选题/【A4紧凑】数二线代臻选题 .pdf'
d = fitz.open(PDF)
BAR = re.compile(r'^#(\d{3})\s*$')
FOOT = re.compile(r'^第\s*\d+\s*页')

out = {}
for pi in range(len(d)):
    blocks = [b for b in d[pi].get_text('blocks') if b[4].strip()]
    bars = []
    for b in blocks:
        lines = [l.strip() for l in b[4].split('\n') if l.strip()]
        if not lines:
            continue
        m = BAR.match(lines[0])
        if m:
            bars.append((int(m.group(1)), ' / '.join(lines[1:]), b[1], b[3]))
    if not bars:
        continue
    bars.sort(key=lambda x: x[2])
    # 页脚 y（用于最后一条的右边界）
    foot_y = None
    for b in blocks:
        for line in b[4].split('\n'):
            if FOOT.match(line.strip()):
                foot_y = b[1]
    for i, (no, meta, y0, y1) in enumerate(bars):
        hi = bars[i + 1][2] if i + 1 < len(bars) else (foot_y if foot_y else 10 ** 6)
        txt = []
        for b in blocks:
            if b is None: continue
            by0, by1 = b[1], b[3]
            # 跳过页眉/章标题/灰条自身/页脚
            if by1 <= y1 - 1: continue
            if by0 >= hi - 1: continue
            for line in b[4].split('\n'):
                s = line.strip()
                if not s: continue
                if FOOT.match(s): continue
                if BAR.match(s) or re.match(r'^#\d{3}$', s): continue
                txt.append(s)
        key = str(no)
        out.setdefault(key, {'meta': meta, 'text': []})['text'].extend(txt)

for k in out:
    out[k]['text'] = ' '.join(out[k]['text'])

io.open('tools/_zx_clean_text.json', 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
print('切出题数:', len(out))
nos = sorted(int(k) for k in out)
print('范围:', nos[0], '~', nos[-1], '| 缺号:', [i for i in range(1, 356) if i not in set(nos)])
empty = [k for k in out if not out[k]['text'].strip()]
print('题干为空的:', len(empty), empty[:10])
for n in [1, 2, 3, 5, 18, 355]:
    if str(n) in out:
        print('#%03d [%s] %s' % (n, out[str(n)]['meta'][:40], out[str(n)]['text'][:110]))
