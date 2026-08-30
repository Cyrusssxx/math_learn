# -*- coding: utf-8 -*-
"""insert_tips_good.py — 把「好题点睛」批量写入源 Markdown（幂等、可重复运行）

用法：
    python -X utf8 tools/insert_tips_good.py tools/_tips_good_01.py [--force] [--dry]

批次文件约定（与真题 _tips_20XX.py 同风格，三引号原文避免 JSON 双重转义）：
    TIPS = {
        "好题1-函数的性质": {
            1: {"gs": "…", "yc": "…", "jq": "…", "zy": "…"},
            ...
        },
        ...
    }

写入位置：该题 `## N.` 段末尾，即 `::: fold 答案与解析` 的闭合 `:::` 之后。
幂等：段内已存在 `::: 点睛` 则跳过，除非 --force（先移除旧块再写）。
"""
import argparse
import importlib.util
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SRC_DIR = TOOLS.parent.parent / 'math' / '好题'

SEC_ORDER = [('gs', '公式'), ('yc', '易错'), ('jq', '技巧'), ('zy', '注意')]
H2_RE = re.compile(r'^##\s*(\d+)\.', re.M)
TIP_OPEN_RE = re.compile(r'^:::\s*点睛\s*$', re.M)


def load_batch(path):
    spec = importlib.util.spec_from_file_location('_tips_batch', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TIPS


def render_tip(tip):
    lines = ['::: 点睛']
    for key, label in SEC_ORDER:
        body = (tip.get(key) or '').strip()
        if body:
            lines.append(f'- **{label}**：{body}')
    if len(lines) == 1:
        return None
    lines.append(':::')
    return '\n'.join(lines)


def strip_tip(seg):
    """移除段内已有的 ::: 点睛 … ::: 块（--force 时用）"""
    m = TIP_OPEN_RE.search(seg)
    if not m:
        return seg
    start = m.start()
    end = seg.find('\n:::', m.end())
    end = len(seg) if end == -1 else end + len('\n:::')
    return (seg[:start] + seg[end:]).rstrip() + '\n'


def process(stem, tips, force, dry):
    fp = None
    for cand in SRC_DIR.glob(stem + '.md'):
        fp = cand
        break
    if fp is None:
        print(f'  ✗ 找不到源文件: {stem}.md')
        return 0
    text = fp.read_text(encoding='utf-8')

    # 按 ## N. 切段（保留前置的标题/前言部分）
    marks = [(m.start(), int(m.group(1))) for m in H2_RE.finditer(text)]
    if not marks:
        print(f'  ✗ 无 ## N. 标题: {stem}')
        return 0

    head = text[:marks[0][0]]
    segs = []
    for i, (pos, no) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        segs.append([no, text[pos:end]])

    done = skip = miss = 0
    for k, (no, seg) in enumerate(segs):
        tip = tips.get(no)
        if not tip:
            continue
        block = render_tip(tip)
        if block is None:
            miss += 1
            continue
        if TIP_OPEN_RE.search(seg):
            if not force:
                skip += 1
                continue
            seg = strip_tip(seg)
        segs[k][1] = seg.rstrip() + '\n\n' + block + '\n\n'
        done += 1

    out = head + ''.join(seg for _, seg in segs)
    if dry:
        print(f'  [dry] {stem}: 写入 {done} 题 / 跳过 {skip} / 空 {miss}')
        return done
    fp.write_text(out, encoding='utf-8')
    print(f'  ✓ {stem}: 写入 {done} 题 / 跳过(已存在) {skip} / 空 {miss}')
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('batch')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    tips_map = load_batch(args.batch)
    total = 0
    for stem, tips in tips_map.items():
        total += process(stem, tips, args.force, args.dry)
    print(f'合计写入 {total} 题点睛' + ('（dry-run，未落盘）' if args.dry else ''))
    if total == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
