# -*- coding: utf-8 -*-
"""对比 exam.js 与 category.js 中重复函数的实现是否一致（为抽取公共模块做准备）"""
import re, difflib


def extract(path):
    src = open(path, encoding='utf-8').read()
    lines = src.split('\n')
    funcs = {}
    i = 0
    while i < len(lines):
        m = re.match(r'^function ([a-zA-Z0-9_]+)\s*\(', lines[i])
        if m:
            name = m.group(1)
            # 收集到单独的 '}' 结尾行
            j = i
            buf = []
            while j < len(lines):
                buf.append(lines[j])
                if lines[j] == '}':
                    break
                j += 1
            funcs[name] = '\n'.join(buf)
            i = j + 1
        else:
            i += 1
    return funcs


e = extract('pwa/js/exam.js')
c = extract('pwa/js/category.js')
dup = sorted(set(e) & set(c))
print('重复函数数:', len(dup))
print()
same, diff = [], []
for name in dup:
    if e[name].strip() == c[name].strip():
        same.append(name)
    else:
        diff.append(name)
print('=== 完全一致 (可直接抽取): %d ===' % len(same))
print('  ' + ' '.join(same))
print()
print('=== 有差异 (抽取时需决策): %d ===' % len(diff))
for name in diff:
    print('  ---', name, '(exam %d 行 / category %d 行)' % (e[name].count('\n') + 1, c[name].count('\n') + 1))
    d = list(difflib.unified_diff(e[name].split('\n'), c[name].split('\n'),
                                  fromfile='exam.js', tofile='category.js', lineterm='', n=0))
    for ln in d[:14]:
        print('     ', ln)
