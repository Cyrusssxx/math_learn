# -*- coding: utf-8 -*-
"""按题号边界从崔命六套卷解析 PDF 切原图，追加到 ansImg。
可重跑：先移除旧的 mn27cui6pdf-* 图与 ansImg 条目，再重新切。
"""
import fitz, json, os, re, glob

SRC_DIR = r'E:/Desktop/做题/崔6'
DATA = r'D:/ai code/math-note/pwa/data/mn27_cui6_papers.json'
IMG_DIR = r'D:/ai code/math-note/pwa/data/img/zx_site'
PREFIX = 'mn27cui6pdf-'
CN = ['一', '二', '三', '四', '五']
Y_TOP, Y_BOT = 48.0, 800.0
SCALE = 2.0
MIN_H = 16.0


def find_pdf(vol):
    f = os.path.join(SRC_DIR, f'小崔说数-崔命六套卷{CN[vol-1]}解析（数二）.pdf')
    assert os.path.exists(f), f
    return f


# 卷五 Q8/Q10 题号用半角且字体映射损坏，search_for 找不到，按题干文字人工定锚点
# (卷号, 题号) -> (0-based page, y0)
FIX = {(5, 8): (5, 580.9), (5, 10): (6, 478.0)}


def locate(doc):
    """返回 {no: [(page_idx, y0), ...]}，题号锚点（取第一个匹配）。"""
    pos = {}
    for expected in range(1, 23):
        # 卷五部分题号用半角 (8)/(10)，其余多为全角（8）
        keys = [f'（{expected}）', f'({expected})']
        hits = []
        for pi in range(len(doc)):
            found = []
            for key in keys:
                for r in doc[pi].search_for(key):
                    if Y_TOP <= r.y0 <= Y_BOT:
                        found.append((pi, r.y0))
            if found:
                hits.append(min(found, key=lambda x: x[1]))
        hits.sort()
        # 只接受排在前一题之后的锚点
        prev = pos.get(expected - 1)
        if prev:
            hits = [h for h in hits if h > prev]
        if hits:
            pos[expected] = hits[0]
    return pos


def locate_with_fix(doc, vol):
    pos = locate(doc)
    for (v, no), anchor in FIX.items():
        if v == vol:
            pos[no] = anchor
    return pos


def segments(doc, anchors):
    """按相邻题号锚点切分，返回 {no: [(page_idx, y_top, y_bot), ...]}。"""
    out = {}
    nos = sorted(anchors)
    for i, no in enumerate(nos):
        p0, y0 = anchors[no]
        nxt = anchors.get(nos[i + 1]) if i + 1 < len(nos) else None
        segs = []
        if nxt is None:
            # 最后一题：切到本题所在页页脚前；若后续页仍有正文，续到文档末
            for pi in range(p0, len(doc)):
                segs.append((pi, max(Y_TOP, y0 - 8) if pi == p0 else Y_TOP, Y_BOT))
        elif p0 == nxt[0]:
            segs.append((p0, max(Y_TOP, y0 - 8), min(Y_BOT, nxt[1] - 6)))
        else:
            segs.append((p0, max(Y_TOP, y0 - 8), Y_BOT))
            for pi in range(p0 + 1, nxt[0]):
                segs.append((pi, Y_TOP, Y_BOT))
            segs.append((nxt[0], Y_TOP, max(Y_TOP + MIN_H, nxt[1] - 6)))
        out[no] = [(p, a, b) for p, a, b in segs if b - a > MIN_H]
    return out


def main():
    # 清理旧图
    for f in glob.glob(os.path.join(IMG_DIR, PREFIX + '*.png')):
        os.remove(f)

    data = json.load(open(DATA, encoding='utf-8'))
    for p in data:
        for s in p['sections']:
            for q in s['questions']:
                q['ansImg'] = [x for x in (q.get('ansImg') or []) if PREFIX not in x]

    report = []
    for vol in range(1, 6):
        doc = fitz.open(find_pdf(vol))
        anchors = locate_with_fix(doc, vol)
        missing = [n for n in range(1, 23) if n not in anchors]
        if missing:
            print(f'卷{vol} 缺锚点: {missing}')
        segs = segments(doc, anchors)
        paper = data[vol - 1]
        for s in paper['sections']:
            for q in s['questions']:
                no = q['no']
                qa = []
                for k, (pi, a, b) in enumerate(segs.get(no, [])):
                    fn = f'{PREFIX}{vol}-{no}_{k}.png'
                    path = os.path.join(IMG_DIR, fn)
                    pix = doc[pi].get_pixmap(matrix=fitz.Matrix(SCALE, SCALE),
                                             clip=fitz.Rect(0, a, doc[pi].rect.width, b),
                                             alpha=False)
                    pix.save(path)
                    qa.append('data/img/zx_site/' + fn)
                q['ansImg'].extend(qa)
        report.append((vol, len(anchors), sum(len(v) for v in segs.values())))
        doc.close()

    with open(DATA, 'w', encoding='utf-8', newline='') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    total_imgs = sum(len(q.get('ansImg') or []) for p in data
                     for s in p['sections'] for q in s['questions'])
    print('卷/锚点/片段:', report)
    print('写出', DATA, '总 ansImg', total_imgs)


if __name__ == '__main__':
    main()
