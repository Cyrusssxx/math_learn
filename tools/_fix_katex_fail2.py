# -*- coding: utf-8 -*-
"""聚焦数据修复 v2（安全版）：
   R1 成对 $$...$$ 块（跨行）内部嵌套的单 $ → 删除（KaTeX 报 Can't use function '$'）
   R2 裸公式行含 \begin{env} 但缺 \end{env} → 行尾补齐（Unexpected end of input）
   R3 行内公式里的 \tag{N} → 删除（\tag works only in display mode）
   对 core_bank.json / exam.json 全字段应用（dry-run 统计）。"""
import json, io, re

BASE = 'D:/ai code/math-note/pwa/data/'
ENV = re.compile(r'\\begin\{([^}]+)\}')
TAG = re.compile(r'\\tag\{[^}]*\}')

BLOCK = re.compile(r'\$\$(.+?)\$\$', re.S)


def clean_block(m):
    return '$$' + m.group(1).replace('$', '') + '$$'


def apply_field(v):
    orig = v
    # R1：成对显示块内删除嵌套 $
    v = BLOCK.sub(clean_block, v)
    # R3：删除行内 \tag（在 $...$ 内）——整体删即可（\tag 仅在 display 有意义，删了不影响数值）
    v = TAG.sub('', v)
    # R2：裸公式行（无 $、含 \begin）补缺失 \end
    lines = v.split('\n')
    for i, L in enumerate(lines):
        if '$' in L:
            continue
        envs = ENV.findall(L)
        if not envs:
            continue
        t = L
        for env in envs:
            nb = len(re.findall(r'\\begin\{%s\}' % re.escape(env), t))
            ne = len(re.findall(r'\\end\{%s\}' % re.escape(env), t))
            if nb > ne:
                t += '\\end{%s}' % env * (nb - ne)
        lines[i] = t
    v = '\n'.join(lines)
    return v, v != orig


if __name__ == '__main__':
    import sys
    DRY = '--write' not in sys.argv
    total = 0
    for tag, path, iterate in (
        ('core', BASE + 'core_bank.json',
         lambda d: [q for s in d[0]['sections'] for q in s['questions']]),
        ('exam', BASE + 'exam.json',
         lambda d: [q for v in d for s in v.get('sections', []) for q in s.get('questions', [])]),
    ):
        d = json.load(io.open(path, encoding='utf-8'))
        changed = 0
        for q in iterate(d):
            for f in ('stem', 'answer', 'idea'):
                v = q.get(f) or ''
                if not v:
                    continue
                nv, ch = apply_field(v)
                if ch:
                    if not DRY:
                        q[f] = nv
                    changed += 1
        if not DRY:
            with io.open(path, 'w', encoding='utf-8', newline='') as fp:
                json.dump(d, fp, ensure_ascii=False, separators=(',', ':'))
        print('%s%s：修改字段 %d 个' % (tag, '(dry)' if DRY else '', changed))
        total += changed
    print('合计 %d' % total)
