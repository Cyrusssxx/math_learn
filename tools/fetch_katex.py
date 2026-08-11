# -*- coding: utf-8 -*-
"""fetch_katex.py — 一次性下载 KaTeX 到 pwa/vendor/katex/（含字体），保证纯离线使用
用法：python -X utf8 fetch_katex.py
"""
import re
import sys
import time
import urllib.request
from pathlib import Path

VER = '0.16.11'
BASE = f'https://cdn.jsdelivr.net/npm/katex@{VER}/dist/'
OUT = Path(__file__).resolve().parent.parent / 'pwa' / 'vendor' / 'katex'

CORE = ['katex.min.css', 'katex.min.js', 'contrib/auto-render.min.js']


def fetch(rel, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size > 0 and not rel.endswith('.css'):
        print(f'跳过（已存在） {rel}')
        return dst.read_bytes()
    url = BASE + rel
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                data = r.read()
            dst.write_bytes(data)
            print(f'OK {rel}  {len(data)//1024}KB')
            return data
        except Exception as e:
            if attempt == 3:
                raise
            print(f'重试 {rel}（{e}）')
            time.sleep(2)


def main():
    css = None
    for rel in CORE:
        # auto-render 放到 vendor/katex 根目录，去掉 contrib/ 前缀
        dst = OUT / Path(rel).name
        data = fetch(rel, dst)
        if rel.endswith('.css'):
            css = data.decode('utf-8')

    # 从 css 里解析字体引用，只下 woff2（现代浏览器全部支持，css 的 src 列表会优先命中）
    fonts = sorted(set(re.findall(r'url\((fonts/[^)]+?\.woff2)\)', css)))
    print(f'字体 woff2 共 {len(fonts)} 个')
    for rel in fonts:
        fetch(rel, OUT / rel)
    print('全部完成 →', OUT)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('下载失败：', e)
        print('兜底：手动下载 https://github.com/KaTeX/KaTeX/releases 的 dist 目录，'
              '把 katex.min.css / katex.min.js / contrib/auto-render.min.js / fonts/ '
              '放到 pwa/vendor/katex/ 下即可。')
        sys.exit(1)
