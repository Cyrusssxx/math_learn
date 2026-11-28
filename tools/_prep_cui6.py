# -*- coding: utf-8 -*-
"""崔命六套卷（卷一~五）转写预处理：
1) 渲染每套试卷/解析 PDF 全部页为 PNG（供视觉转写）
2) 导出文字层（供交叉核对答案字母）
输出：
  C:/Users/cjx/AppData/Local/Temp/cui6_pages/{vol}_{exam|ans}_pNN.png
  tools/_cui6_text/vol{1..5}_{exam|ans}.txt
"""
import fitz, os, re, glob

SRC_DIR = r'E:/Desktop/做题/崔6'
OUT_IMG = r'C:/Users/cjx/AppData/Local/Temp/cui6_pages'
OUT_TXT = r'D:/ai code/math-note/tools/_cui6_text'
os.makedirs(OUT_IMG, exist_ok=True)
os.makedirs(OUT_TXT, exist_ok=True)

CN = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五'}


def find(kind, vol):
    pat = os.path.join(SRC_DIR, f'小崔说数-崔命六套卷{CN[vol]}{kind}（数二）.pdf')
    if not os.path.exists(pat):
        # 兼容卷一「终极预测卷」命名
        alt = os.path.join(SRC_DIR, f'小崔说数-崔命六套卷{CN[vol]}{kind}（数二）.pdf')
        raise FileNotFoundError(pat)
    return pat


def main():
    manifest = {}
    for vol in range(1, 6):
        for kind in ('试卷', '解析'):
            f = find(kind, vol)
            d = fitz.open(f)
            tag = 'exam' if kind == '试卷' else 'ans'
            key = f'v{vol}_{tag}'
            pages = []
            texts = []
            for i, p in enumerate(d):
                pix = p.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                fn = os.path.join(OUT_IMG, f'{key}_p{i+1:02d}.png')
                pix.save(fn)
                pages.append(fn)
                texts.append(f'===== PAGE {i+1} =====\n' + p.get_text())
            with open(os.path.join(OUT_TXT, f'{key}.txt'), 'w', encoding='utf-8') as fp:
                fp.write('\n'.join(texts))
            manifest[key] = {'pdf': f, 'pages': len(pages)}
            print(key, 'pages', len(pages))
    import json
    with open(os.path.join(OUT_TXT, 'manifest.json'), 'w', encoding='utf-8') as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=1)
    print('done')


if __name__ == '__main__':
    main()
