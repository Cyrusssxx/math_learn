# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)

# 329~346 全部属于 PDF 第六章 F 二次型「正定 · c) 其他」
# 映射到考点 210 (正定)
updated = 0
for s in xd[0]['sections']:
    for q in s['questions']:
        pno = q.get('pdfNo')
        if pno and 329 <= pno <= 346:
            q['categoryIds'] = [210]
            updated += 1

print(f"成功将 {updated} 道题的 categoryIds 更新为 [210] (正定)！")

with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(xd, f, ensure_ascii=False, separators=(',', ':'))

print("已写回 xd_bank.json！")
