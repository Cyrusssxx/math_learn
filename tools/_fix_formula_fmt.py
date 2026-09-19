# -*- coding: utf-8 -*-
"""公式格式规范化 fixer：
   规则1 删除「多余的开块 $$」——独立 $$ 行与其后最近的独立 $$ 行之间含正文行（中文且无 LaTeX 命令）时，
        该开块是多余的（正文被误吞进显示块）→ 删掉这个 $$ 行。
   规则2 裸公式行（不在 $ 区间内、含 LaTeX 命令）→ 连续段整体用 $$ 包裹（单行也可）。
   先以 2020 第15题为样例 dry-run 打印前后对比。
"""
import json, io, re

EXAM = 'D:/ai code/math-note/pwa/data/exam.json'
LATEX_CMD = re.compile(r'\\(?:frac|dfrac|tfrac|lim|left|right|begin|end|sum|int|iint|sqrt|ln|cdot|to|infty|partial|alpha|beta|gamma|theta|lambda|Delta|sigma|sin|cos|tan|cot|sec|csc|arctan|mathrm|text|quad|qquad|displaystyle|overline|vec|boldsymbol|matrix|pmatrix|cases|Bigl|Bigr|Big|big|log|max|min|exp)')
HAN = re.compile(r'[\u4e00-\u9fff]')


def is_bare_formula(line):
    s = line.strip()
    return bool(s) and '$' not in s and LATEX_CMD.search(s) and not HAN.search(s)


def fix_field(text):
    """返回 (新文本, 修复日志)"""
    lines = text.split('\n')
    logs = []
    # ---- 规则1：多余开块 $$ ----
    dd_lines = [i for i, L in enumerate(lines) if L.strip() == '$$']
    remove = set()
    for k in range(0, len(dd_lines) - 1, 2):
        i, j = dd_lines[k], dd_lines[k + 1]
        inner = lines[i + 1:j]
        # 该区间含正文行（中文且无 LaTeX 命令）→ 说明这是一对"吞正文"的错配
        if inner and any(HAN.search(x) and not LATEX_CMD.search(x) and x.strip() for x in inner):
            # 进一步：若 k 之后还有未配对的 $$（说明本 $$ 是多开的）→ 删掉
            if len(dd_lines) % 2 == 1:
                remove.add(i)
                logs.append(('删除多余开块 $$', i + 1, lines[i].strip()))
    if remove:
        lines = [L for idx, L in enumerate(lines) if idx not in remove]
    # ---- 规则2：裸公式行段包裹 $$ ----
    out, i, n = [], 0, len(lines)
    while i < n:
        if is_bare_formula(lines[i]):
            j = i
            while j < n and (is_bare_formula(lines[j]) or not lines[j].strip()):
                if not lines[j].strip() and (j + 1 >= n or not is_bare_formula(lines[j + 1])):
                    break
                j += 1
            seg = lines[i:j]
            out.append('$$')
            out.extend(seg)
            out.append('$$')
            logs.append(('包裹裸公式行段 $$', i + 1, (' / '.join(x.strip()[:40] for x in seg))[:100]))
            i = j
        else:
            out.append(lines[i])
            i += 1
    return '\n'.join(out), logs


if __name__ == '__main__':
    ex = json.load(io.open(EXAM, encoding='utf-8'))
    q15 = None
    for vol in ex:
        if str(vol.get('year')) == '2020':
            for sec in vol.get('sections', []):
                for q in sec.get('questions', []):
                    if q.get('no') == 15:
                        q15 = q
    new, logs = fix_field(q15['answer'])
    print('修复日志 %d 条：' % len(logs))
    for k, ln, s in logs:
        print('   %s @L%d | %s' % (k, ln, s))
    print()
    print('=== 修复后 L9–L22 ===')
    for i, L in enumerate(new.split('\n')):
        if 9 <= i <= 22:
            print('L%-3d (%d个$): %s' % (i, L.count('$'), L[:110]))
