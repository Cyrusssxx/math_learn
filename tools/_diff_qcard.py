# -*- coding: utf-8 -*-
"""对比真题页 qCard() 与分类页 catCard() 的结构差异：class 集合 / data-act / onclick 函数"""
import io, re

def seg_of(path, fname):
    s = io.open(path, encoding='utf-8').read()
    i = s.find('function ' + fname)
    j = s.find('\nfunction ', i + 10)
    return s[i:j if j > 0 else len(s)]

ex = seg_of('D:/ai code/math-note/pwa/js/exam.js', 'qCard')
ca = seg_of('D:/ai code/math-note/pwa/js/category.js', 'catCard')
print('exam.js qCard 段长 %d | category.js catCard 段长 %d' % (len(ex), len(ca)))

def classes(seg):
    out = set()
    for m in re.finditer(r'class="([^"$]*)"', seg):
        for c in m.group(1).split():
            if c and '$' not in c:
                out.add(c)
    return out


def acts(seg):
    return set(re.findall(r'data-act="([^"$]+)"', seg))


def fns(seg):
    return set(re.findall(r'onclick="([a-zA-Z_$][\w$]*)\(', seg))


ce, cc = classes(ex), classes(ca)
print('\n=== class 差异 ===')
print('仅真题页:', sorted(ce - cc))
print('仅分类页:', sorted(cc - ce))
print('\n=== data-act 差异 ===')
print('仅真题页:', sorted(acts(ex) - acts(ca)))
print('仅分类页:', sorted(acts(ca) - acts(ex)))
print('\n=== onclick 函数差异 ===')
print('仅真题页:', sorted(fns(ex) - fns(ca)))
print('仅分类页:', sorted(fns(ca) - fns(ex)))
print('\n两页共有 class 数:', len(ce & cc))
