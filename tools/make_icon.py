# -*- coding: utf-8 -*-
"""make_icon.py — 生成便签风格 PWA 图标（icons/icon-192.png、icon-512.png）
用法：python -X utf8 tools/make_icon.py
设计：主题蓝圆角底 + 黄色便签纸（右下折角 + 阴影 + 三行笔记线）
"""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / 'pwa' / 'icons'

BG = (74, 144, 217)        # 主题蓝（同 theme-color #4a90d9）
PAPER = (255, 232, 132)    # 便签黄（同荧光色 --mk-y #ffe884）
FOLD = (230, 201, 92)      # 折角深黄
LINE = (176, 138, 32)      # 笔记线
SHADOW = (0, 0, 0, 60)     # 便签投影


def draw_icon(size):
    s = size / 512  # 以 512 为基准等比缩放
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 圆角背景
    r = int(110 * s)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)

    # 便签纸区域（居中略偏上）
    x0, y0 = int(118 * s), int(100 * s)
    x1, y1 = int(394 * s), int(412 * s)
    fold = int(78 * s)  # 折角边长

    # 投影
    off = int(14 * s)
    sh = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon(
        [(x0 + off, y0 + off), (x1 + off, y0 + off),
         (x1 + off, y1 - fold + off), (x1 - fold + off, y1 + off),
         (x0 + off, y1 + off)], fill=SHADOW)
    img = Image.alpha_composite(img, sh)
    d = ImageDraw.Draw(img)

    # 纸面（右下切角的五边形）
    d.polygon([(x0, y0), (x1, y0), (x1, y1 - fold), (x1 - fold, y1), (x0, y1)],
              fill=PAPER)
    # 折角（翻起的小三角）
    d.polygon([(x1 - fold, y1), (x1, y1 - fold), (x1 - fold, y1 - fold)],
              fill=FOLD)

    # 三行笔记线（圆头短线，长短不一更像手写便签）
    lw = int(26 * s)
    lx = x0 + int(42 * s)
    for i, w in enumerate([200, 200, 130]):
        ly = y0 + int((72 + i * 78) * s)
        d.rounded_rectangle([lx, ly, lx + int(w * s), ly + lw],
                            radius=lw // 2, fill=LINE)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for size in (192, 512):
        # 4 倍超采样抗锯齿
        big = draw_icon(size * 4)
        big.resize((size, size), Image.LANCZOS).save(OUT / f'icon-{size}.png')
        print(f'icon-{size}.png 已生成')


if __name__ == '__main__':
    main()
