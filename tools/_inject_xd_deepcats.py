import json

with open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd = json.load(f)

with open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json', 'r', encoding='utf-8') as f:
    dgy = json.load(f).get('items', [])
dgy_map = {str(it['serial']): it for it in dgy}

mapped = 0
for s in xd[0]['sections']:
    for q in s['questions']:
        it = dgy_map.get(str(q.get('no')))
        if it and it.get('categoryIds'):
            # 将原始大观园 categoryIds 作为 deepCats
            q['deepCats'] = [str(x) for x in it['categoryIds']]
            mapped += 1

print(f"成功为 {mapped} 道线代重点题注入 deepCats！")

with open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(xd, f, ensure_ascii=False, separators=(',', ':'))

print("已写回 xd_bank.json！")
