# -*- coding: utf-8 -*-
import fitz
import re, json, io

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

dgy_path = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
with io.open(dgy_path, 'r', encoding='utf-8') as f:
    dgy = json.load(f)
    items = dgy.get('items', [])

print("检查 PDF #330~#346 各题的灰条来源和大观园候选...")

# 收集这 17 题的完整文本
pdf_tail = {}
for pno in range(175, len(doc)):
    page = doc[pno]
    blocks = page.get_text("blocks")
    for b_idx, b in enumerate(blocks):
        txt = b[4].strip().replace('\n', ' ')
        m = re.search(r'#(\d{3})', txt)
        if m:
            num = int(m.group(1))
            if num >= 330:
                # 题干文字
                c_blocks = []
                for ni in range(b_idx+1, min(b_idx+6, len(blocks))):
                    nb = blocks[ni]
                    ntxt = nb[4].strip().replace('\n', ' ')
                    if re.search(r'#\d{3}', ntxt) or '第 ' in ntxt:
                        break
                    c_blocks.append(ntxt)
                pdf_tail[num] = {
                    'num': num,
                    'bar': txt,
                    'stem': " ".join(c_blocks)
                }

def clean(s):
    return re.sub(r'[\s\$\\\{\}\(\)\_\^\+\-\=\,\.\;\:\'\"\`\(\)（）\u3000\[\]【】\/\<\>]', '', str(s)).lower()

for num in range(330, 347):
    pt = pdf_tail.get(num)
    if not pt:
        print(f"#{num}: 未找到")
        continue
    bar = pt['bar']
    stem = pt['stem']
    
    # 提取年份和 880 标记
    # 在大观园中全库搜索
    best_it = None
    best_score = 0
    pstem = clean(stem[:60])
    pbar = clean(bar)
    
    for it in items:
        isrc = clean(it.get('source', ''))
        istem = clean(it.get('stem', '')[:120])
        
        score = 0
        if pstem and istem:
            common = sum(1 for ch in pstem if ch in istem)
            ratio = common / max(len(pstem), 1)
            score += ratio * 30
            if len(pstem) >= 10 and pstem[:15] in istem:
                score += 20
        # 来源匹配
        if any(k in isrc for k in ['880', '19', '20']):
            for k in pbar.split():
                if k in isrc: score += 5
                
        if score > best_score:
            best_score = score
            best_it = it
            
    print(f"PDF #{num:03d} | Bar: {bar[:50]}")
    if best_it:
        print(f"  ==> 匹配 serial: {best_it['serial']} (score: {best_score:.1f})")
        print(f"      大观 source: {best_it.get('source')}")
        print(f"      大观 stem: {best_it.get('stem')[:60].replace(chr(10), ' ')}")
    print()
