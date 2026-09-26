# -*- coding: utf-8 -*-
import json, io, re

with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)

for s in xd[0]['sections']:
    for q in s['questions']:
        if str(q.get('no')) == '323':
            stem = q['stem']
            # 将 (A) (B) (C) (D) 拆入 options
            m = re.search(r'\(A\)\s*(.*?)\s*\(B\)\s*(.*?)\s*\(C\)\s*(.*?)\s*\(D\)\s*(.*)', stem)
            if m:
                q['stem'] = stem[:m.start()].strip()
                q['options'] = [
                    f"$a\\notin\\Omega, d\\notin\\Omega$",
                    f"$a\\notin\\Omega, d\\in\\Omega$",
                    f"$a\\in\\Omega, d\\notin\\Omega$",
                    f"$a\\in\\Omega, d\\in\\Omega$"
                ]
                q['answer'] = "（D. $a\\in\\Omega, d\\in\\Omega$）"
                print("成功修复 323 题选项与答案！")

with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(xd, f, ensure_ascii=False, separators=(',', ':'))
