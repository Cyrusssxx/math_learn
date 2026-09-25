# -*- coding: utf-8 -*-
import json, io, os

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

src = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
with io.open(src, 'r', encoding='utf-8') as f:
    dgy = json.load(f)
    items = dgy if isinstance(dgy, list) else dgy.get('items', [])

# 抽取 2022 和 2024
dgy_map = {'2022': {}, '2024': {}}
# 2022 数二真题 serial: 4992 ~ 5013 (正好 22 道题！1~10 选择，11~16 填空，17~22 解答)
# 2024 数二真题 serial: 4957 ~ 4978 (正好 22 道题！1~10 选择，11~16 填空，17~22 解答)

for it in items:
    s = str(it.get('source', ''))
    serial = it.get('serial')
    if 4992 <= serial <= 5013:
        qno = serial - 4992 + 1
        dgy_map['2022'][str(qno)] = it
    elif 4957 <= serial <= 4978:
        qno = serial - 4957 + 1
        dgy_map['2024'][str(qno)] = it

print("2022 抓取题数:", len(dgy_map['2022']))
print("2024 抓取题数:", len(dgy_map['2024']))

# 对比 exam.json 中的 2022 和 2024
for year in ['2022', '2024']:
    paper_id = f'{year}数二真题'
    paper = next((p for p in exam_data if p.get('id') == paper_id), None)
    if not paper:
        print(f"未找到试卷: {paper_id}")
        continue
    
    print(f"\n==================== 对比 {year} 年数二真题 ====================")
    for sec in paper.get('sections', []):
        for q in sec.get('questions', []):
            no = str(q.get('no'))
            dgy_q = dgy_map[year].get(no)
            if not dgy_q:
                print(f"[{no}] 大观园无对应题")
                continue
            
            # 对比 stem, options, answer
            our_stem = q.get('stem', '')
            dgy_stem = dgy_q.get('stem', '')
            our_opts = q.get('options', [])
            dgy_opts = dgy_q.get('options', [])
            our_ans = q.get('answer', '')
            dgy_ans = dgy_q.get('answer', '')
            
            # 简单清洗空格和格式
            def norm(s):
                return str(s).replace(' ', '').replace('$', '').replace('\n', '').replace('\\displaystyle', '').replace('，', ',')
            
            stem_diff = norm(our_stem) != norm(dgy_stem)
            opt_diff = norm(our_opts) != norm(dgy_opts)
            
            print(f"--- 题号 {no} ---")
            if stem_diff:
                print("  [Stem 差异]")
                print("    本库:", repr(our_stem))
                print("    大观:", repr(dgy_stem))
            else:
                print("  [Stem 一致]")
                
            if opt_diff:
                print("  [Options 差异]")
                print("    本库:", repr(our_opts))
                print("    大观:", repr(dgy_opts))
            
            # 打印答案情况
            print("    本库答案:", repr(our_ans)[:60])
            print("    大观答案:", repr(dgy_ans)[:60])
