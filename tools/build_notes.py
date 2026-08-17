# -*- coding: utf-8 -*-
"""build_notes.py — 把导图 Markdown 打包成笔记阅读站数据（math-note 阅读版构建脚本）
用法：python -X utf8 build_notes.py [源目录...]
    源目录默认 D:\\ai code\\math\\导图 与 D:\\ai code\\math\\好题（相对本脚本推导），输出 ../pwa/data/notes.json

输出结构：[{id, subject, order, name, title, chapters:[..H2标题..], md}, ...]
md 为剥离 frontmatter 后的正文原文，渲染在前端完成（js/reader.js）。
md 中 ![说明](相对路径) 引用的本地图片会被复制到 pwa/data/img/，路径改写为 data/img/文件名。
"""
import json
import re
import shutil
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DATA_DIR = TOOLS.parent / 'pwa' / 'data'
IMG_DIR = DATA_DIR / 'img'
DEFAULT_SRCS = [TOOLS.parent.parent / 'math' / '导图',
                TOOLS.parent.parent / 'math' / '好题']

SUBJECT_NAMES = {'zy': '考前21记', 'gs': '高等数学', 'xd': '线性代数', 'ht': '数学好题'}
SUBJECT_KEYS = {'高数': 'gs', '线代': 'xd', '好题': 'ht', '21记': 'zy'}


def parse_stem(stem):
    """文件名 → (学科key, 排序号)，如 高数3.1-一元积分-计算 → ('gs', 3.1)、21记1-函数极限 → ('zy', 1)"""
    m = re.match(r'^(高数|线代|好题|21记)([\d.]+)-', stem)
    if not m:
        raise ValueError(f'文件名不符合 高数N-/线代N-/好题N-/21记N- 规则: {stem}')
    return SUBJECT_KEYS[m.group(1)], float(m.group(2))


def strip_frontmatter(text):
    lines = text.splitlines()
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return '\n'.join(lines[i + 1:]).strip()
    return text.strip()


IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def localize_images(md, base_dir):
    """把 md 引用的本地图片复制进 pwa/data/img/，src 改写为 data/img/文件名"""
    def repl(m):
        alt, src = m.group(1), m.group(2).strip()
        if re.match(r'^(https?:)?//', src) or src.startswith('data/img/'):
            return m.group(0)  # 网络图片或已本地化的引用原样保留
        p = Path(src) if Path(src).is_absolute() else (base_dir / src)
        if not p.is_file():
            print(f'  ⚠ 图片不存在，保留原引用: {src}')
            return m.group(0)
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, IMG_DIR / p.name)
        return f'![{alt}](data/img/{p.name})'
    return IMG_RE.sub(repl, md)


def build(src_dirs):
    notes = []
    for src_dir in src_dirs:
        if not src_dir.is_dir():
            continue
        for path in sorted(src_dir.glob('*.md')):
            subject, order = parse_stem(path.stem)
            md = strip_frontmatter(path.read_text(encoding='utf-8'))
            md = localize_images(md, src_dir)
            title_m = re.search(r'^# (.+)$', md, re.M)
            chapters = [re.sub(r'<!--.*?-->', '', t).strip()
                        for t in re.findall(r'^## (.+)$', md, re.M)]
            notes.append({
                'id': path.stem,
                'subject': subject,
                'order': order,
                'name': path.stem,
                'title': title_m.group(1).strip() if title_m else path.stem,
                'chapters': chapters,
                'md': md,
            })
    notes.sort(key=lambda n: (n['subject'], n['order']))
    return notes


def main():
    srcs = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_SRCS
    notes = build(srcs)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # 好题(ht)独立拆出为 good.json，从笔记体系摘除（见 good.html 刷题模块）
    good = [n for n in notes if n['subject'] == 'ht']
    notes_only = [n for n in notes if n['subject'] != 'ht']
    _write(notes_only, DATA_DIR / 'notes.json')
    _write(good, DATA_DIR / 'good.json')
    for n in notes_only:
        print(f"{n['name']}: {len(n['chapters'])} 章, {len(n['md']) // 1024}KB")
    print(f"共 {len(notes_only)} 份笔记 → notes.json | {len(good)} 份好题 → good.json")


def _write(notes, out):
    out.write_text(json.dumps(notes, ensure_ascii=False), encoding='utf-8')
    print(f"  → {out} ({out.stat().st_size // 1024}KB)")


if __name__ == '__main__':
    main()
