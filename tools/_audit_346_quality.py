# -*- coding: utf-8 -*-
import json, io, os, re
from collections import Counter

with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)

questions = [q for s in xd[0]['sections'] for q in s['questions']]
print(f"新题库总题数: {len(questions)}")

# 1. 检查是否存在缺失或占位符
empty_ans = []
empty_idea = []
pure_letter_ans = []
placeholder_idea = []

for q in questions:
    no = q.get('no')
    pno = q.get('pdfNo')
    ans = str(q.get('answer', '')).strip()
    idea = str(q.get('idea', '')).strip()
    
    if not ans:
        empty_ans.append((pno, no))
    if not idea:
        empty_idea.append((pno, no))
        
    # 纯字母单选答案（如 'A' 或 '(B)' 或 '$C$' 且未展开选项内容）
    if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', ans) and re.search(r'[A-Da-d]', ans):
        pure_letter_ans.append((pno, no, ans))
        
    if re.search(r'(待补充|此处略|略$|^见解析$)', idea):
        placeholder_idea.append((pno, no, idea))

print(f"answer 为空: {len(empty_ans)}")
print(f"idea 为空: {len(empty_idea)}")
print(f"answer 为纯字母（未展开选项文字）: {len(pure_letter_ans)}")
print(f"idea 为占位符（如待补充/略）: {len(placeholder_idea)}")

# 2. 统计解析长度分布
lengths = [len(str(q.get('idea', ''))) for q in questions]
print(f"\n解析长度分布统计:")
print(f"  最短: {min(lengths)} 字")
print(f"  中位数: {sorted(lengths)[len(lengths)//2]} 字")
print(f"  最长: {max(lengths)} 字")

buckets = {'<100': 0, '100-150': 0, '150-250': 0, '250-400': 0, '>400': 0}
for l in lengths:
    if l < 100: buckets['<100'] += 1
    elif l < 150: buckets['100-150'] += 1
    elif l < 250: buckets['150-250'] += 1
    elif l < 400: buckets['250-400'] += 1
    else: buckets['>400'] += 1

for k, v in buckets.items():
    print(f"  {k:<8}: {v} 题")

# 打印一些较短解析的题目
short_list = [q for q in questions if len(str(q.get('idea', ''))) < 150]
print(f"\n解析 <150 字的题目总数: {len(short_list)}")
print("样本前 10 题:")
for q in short_list[:10]:
    print(f"  PDF #{q.get('pdfNo'):03d} (no {q.get('no')}) | 来源: {q.get('source'):<25} | 长度: {len(str(q.get('idea')))} 字")
    print(f"    answer: {repr(q.get('answer'))[:40]}")
    print(f"    idea: {repr(q.get('idea'))[:80]}")
