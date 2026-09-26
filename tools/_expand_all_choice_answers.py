# -*- coding: utf-8 -*-
import json, io, re

with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)

questions = [q for s in xd[0]['sections'] for q in s['questions']]
expanded_cnt = 0

for q in questions:
    ans = str(q.get('answer', '')).strip()
    opts = q.get('options', [])
    
    # 判断是否为纯字母选择题答案，如 "B", "A", "(C)", "$D$"
    if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', ans) and re.search(r'[A-Da-d]', ans) and opts:
        letters = re.findall(r'[A-Da-d]', ans)
        parts = []
        for L in letters:
            idx = 'abcd'.index(L.lower())
            if 0 <= idx < len(opts):
                # 剥离已有选项开头的 A. 或 (A)
                txt = re.sub(r'^\s*[（(\[]?[A-Da-d][）)\].、:：]?\s*', '', str(opts[idx])).strip()
                parts.append(f"{L.upper()}. {txt}")
        if parts:
            q['answer'] = f"（{'；'.join(parts)}）"
            expanded_cnt += 1

print(f"成功将 {expanded_cnt} 道单选/多选题答案展开为选项内容！")

# 再次保存
with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(xd, f, ensure_ascii=False, separators=(',', ':'))

print("已写回 xd_bank.json！")
