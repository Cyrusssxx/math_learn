# -*- coding: utf-8 -*-
"""修复 exam.json 中「连续 $$ 空块」导致的答案乱码（2020数二22题），并全库扫描同类问题。

乱码机制：`$$\n$$\n`（连续两个 $$ 行）令 mdBlock 的显示块解析错乱，
其后的 `得 $f=...$` 等被当作普通文本逐字分行显示。
"""
import json, io, re

EXAM = 'D:/ai code/math-note/pwa/data/exam.json'
ex = json.load(io.open(EXAM, encoding='utf-8'))

# 扫描全库：任意字段里出现「两行连续 $$」或「$$$$」
pat = re.compile(r'\$\$\s*\n\s*\$\$|\$\$\$\$')
hits = []
for vol in ex:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            for f in ('stem', 'answer', 'idea'):
                v = q.get(f) or ''
                for m in pat.finditer(v):
                    hits.append((vol.get('year'), q.get('no'), f, m.start()))
print('全库「连续 $$ 空块」出现 %d 处：' % len(hits))
for h in hits[:20]:
    print('  %s年 第%s题 %s @%d' % h)
print()

# 修复 2020数二 第22题 answer：连续 $$ 空块 → 单个 $$
fixed = 0
for vol in ex:
    if str(vol.get('year')) != '2020':
        continue
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            if q.get('no') != 22:
                continue
            ans = q.get('answer') or ''
            new = pat.sub('$$', ans)
            if new != ans:
                q['answer'] = new
                fixed += 1
                print('2020数二 第22题 answer 已修复 %d 处连续空块' % len(pat.findall(ans)))
                print('修复后该字段剩余连续空块:', len(pat.findall(new)))

def clean_dd(s):
    """把连续 $$ 空块折叠为单个 $$：循环替换直到无相邻 $$（处理 2 连/3 连/多连）"""
    while True:
        t = re.sub(r'\$\$\s*\n\s*\$\$', '$$', s)
        if t == s:
            return s
        s = t


# 其他年份/题目若也存在同类问题（扫描命中但不在2020q22）→ 一并修复
for vol in ex:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            for f in ('stem', 'answer', 'idea'):
                v = q.get(f) or ''
                if pat.search(v):
                    q[f] = clean_dd(v)
                    print('  同修：%s年 第%s题 %s' % (vol.get('year'), q.get('no'), f))

with io.open(EXAM, 'w', encoding='utf-8', newline='') as f:
    json.dump(ex, f, ensure_ascii=False, separators=(',', ':'))

# 复查
ex2 = json.load(io.open(EXAM, encoding='utf-8'))
left = 0
for vol in ex2:
    for sec in vol.get('sections', []):
        for q in sec.get('questions', []):
            for f in ('stem', 'answer', 'idea'):
                left += len(pat.findall(q.get(f) or ''))
print()
print('修复完成 | 修复 %d 处 | 全库剩余连续 $$ 空块: %d' % (fixed, left))
