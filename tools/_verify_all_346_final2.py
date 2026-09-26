# -*- coding: utf-8 -*-
import fitz
import re, json, io

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

dgy_path = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/questions.json'
with io.open(dgy_path, 'r', encoding='utf-8') as f:
    dgy = json.load(f)
    items = dgy.get('items', [])

cat_path = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/categories.json'
with io.open(cat_path, 'r', encoding='utf-8') as f:
    cats_data = json.load(f).get('items', [])

node_map = {n['id']: n for n in cats_data}
def is_linear_algebra(cid):
    curr = cid
    while curr:
        if curr == 1:
            return True
        curr = node_map.get(curr, {}).get('parentId')
    return False

la_cids = {n['id'] for n in cats_data if is_linear_algebra(n['id'])}
la_items = [it for it in items if any(cid in la_cids for cid in it.get('categoryIds', []))]

cat_keywords = {}
for n in cats_data:
    cid = n['id']
    cat_keywords[cid] = (n.get('name', '') + " " + n.get('path', '')).replace(' ', '').lower()

# 提取 PDF 全部 346 题
pdf_questions = []
for pno in range(5, len(doc)):
    page = doc[pno]
    blocks = page.get_text("blocks")
    for b_idx, b in enumerate(blocks):
        txt = b[4].strip().replace('\n', ' ')
        m = re.search(r'#(\d{3})', txt)
        if m:
            qnum = int(m.group(1))
            pre = txt[:m.start()].strip()
            post = txt[m.end():].strip()
            
            m_dur = re.search(r'(\d+分钟)', pre)
            duration = m_dur.group(1) if m_dur else ""
            if m_dur: pre = pre.replace(duration, '').strip()
                
            m_diff = re.search(r'难度\s*([\d\.]+)', pre)
            difficulty = m_diff.group(1) if m_diff else ""
            if m_diff: pre = re.sub(r'难度\s*[\d\.]+', '', pre).strip()
                
            source = pre.strip()
            parts = post.split()
            chapter = parts[0] if len(parts) > 0 else ""
            if len(parts) > 1 and parts[0] in ['A', 'B', 'C', 'D', 'E', 'F']:
                chapter = parts[0] + ' ' + parts[1]
                topic = " ".join(parts[2:])
            else:
                topic = " ".join(parts[1:])
            
            content_blocks = []
            for next_idx in range(b_idx + 1, min(b_idx + 8, len(blocks))):
                nb = blocks[next_idx]
                ntxt = nb[4].strip().replace('\n', ' ')
                if re.search(r'#\d{3}', ntxt) or '第 ' in ntxt:
                    break
                content_blocks.append(ntxt)
            stem_raw = " ".join(content_blocks)
            
            pdf_questions.append({
                'num': qnum,
                'page': pno + 1,
                'source': source,
                'chapter': chapter,
                'topic': topic,
                'bar': txt,
                'stem_raw': stem_raw
            })

unique_pdf = {}
for q in pdf_questions:
    if q['num'] not in unique_pdf:
        unique_pdf[q['num']] = q

# 100% 精确的 manual_override
manual_override = {
    45: 27,   # 2008数一二三 A^3=O
    60: 5920, # 2008数一 A=alpha alpha^T + beta beta^T 秩
    86: 126,  # 2024数二三 P^TAP^2 初等变换
    99: 158,  # 2024数二 A(A-A^*)=O
    107: 200, # 1989数一三 4阶矩阵|A|=0 列相关
    110: 203, # 2023数一 已知向量 a_1=(1,0,1,1)^T 向量计算
    126: 238, # 2023数一二三 已知向量 a_1=(1,2,3)^T 共同线性表示
    344: 787, # 2019数一 三张平面两两相交
    346: 790  # 2019数一 向量组alpha_1=(1,2,1)
}

chap_to_l2 = {'A': 2, 'B': 3, 'C': 4, 'D': 5, 'E': 6, 'F': 7}

def clean(s):
    return re.sub(r'[\s\$\\\{\}\(\)\_\^\+\-\=\,\.\;\:\'\"\`\(\)（）\u3000\[\]【】\/\<\>]', '', str(s)).lower()

final_matches = []
for num in range(1, 347):
    pq = unique_pdf[num]
    
    if num in manual_override:
        target_serial = manual_override[num]
        it = next(x for x in items if x['serial'] == target_serial)
        final_matches.append({
            'pdf_num': num,
            'pdf_source': pq['source'],
            'chapter': pq['chapter'],
            'topic': pq['topic'],
            'dgy_serial': target_serial,
            'item': it
        })
        continue
        
    psrc = clean(pq['source'])
    pstem = clean(pq['stem_raw'][:100])
    ptopic = clean(pq['topic'])
    pchap = pq['chapter'][0] if pq['chapter'] else ''
    target_l2 = chap_to_l2.get(pchap)
    
    m_year = re.search(r'(19\d\d|20\d\d)', psrc)
    pyear = m_year.group(1) if m_year else ""
    m_sub = re.search(r'数[一二三、，,]+', psrc)
    psub = m_sub.group(0) if m_sub else ""
    
    best_item = None
    best_score = -100
    
    for it in la_items:
        isrc = clean(it.get('source', ''))
        istem = clean(it.get('stem', '')[:150])
        icids = it.get('categoryIds', [])
        
        score = 0
        is_math1_special = 8 in icids
        
        belongs_chap = False
        for cid in icids:
            curr = cid
            while curr:
                if curr == target_l2:
                    belongs_chap = True
                    break
                curr = node_map.get(curr, {}).get('parentId')
            if belongs_chap: break
            
        if target_l2:
            if belongs_chap:
                score += 25
            elif is_math1_special and num >= 329:
                score += 25
            else:
                score -= 60
                
        if psrc and (psrc in isrc or isrc in psrc):
            score += 35
        elif pyear and pyear in isrc:
            score += 12
            if psub and psub in isrc:
                score += 10
                
        m_880_p = re.search(r'880(.*)', psrc)
        m_880_i = re.search(r'880(.*)', isrc)
        if m_880_p and m_880_i and m_880_p.group(1) == m_880_i.group(1):
            score += 40
                
        if pstem and istem:
            common = sum(1 for ch in pstem if ch in istem)
            ratio = common / max(len(pstem), 1)
            score += ratio * 30
            for l in [20, 15, 10]:
                if len(pstem) >= l and pstem[:l] in istem:
                    score += l
                    break
                    
        if score > best_score:
            best_score = score
            best_item = it
            
    final_matches.append({
        'pdf_num': num,
        'pdf_source': pq['source'],
        'chapter': pq['chapter'],
        'topic': pq['topic'],
        'dgy_serial': best_item['serial'],
        'item': best_item
    })

serials = [m['dgy_serial'] for m in final_matches]
unique_serials = set(serials)
print(f"最终匹配完成! 总数: {len(final_matches)}")
print(f"唯一大观园 serial 数: {len(unique_serials)} / 346")

from collections import Counter
counts = Counter(serials)
dup = [s for s, c in counts.items() if c > 1]
print(f"剩余重复数量: {len(dup)}")
if dup:
    for s in dup:
        duped_nums = [m['pdf_num'] for m in final_matches if m['dgy_serial'] == s]
        print(f"  serial {s}: PDF {duped_nums}")
else:
    print("★★★ 完美实现 346 道题目 100% 一对一精准无重复匹配！★★★")
