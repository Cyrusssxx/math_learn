# -*- coding: utf-8 -*-
import json, io, os, re

# 1. 导入 346 题最终匹配表
from _verify_all_346_final2 import final_matches

# 2. 导入现有数据
with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

with io.open('pwa/data/xd_bank.json', 'r', encoding='utf-8') as f:
    xd_bank = json.load(f)
existing_xd_map = {str(q.get('no')): q for sec in xd_bank[0].get('sections', []) for q in sec.get('questions', [])}

with io.open('pwa/data/exam_categories.json', 'r', encoding='utf-8') as f:
    ecats = json.load(f)

with io.open('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/categories.json', 'r', encoding='utf-8') as f:
    dcats = json.load(f).get('items', [])
dnode = {n['id']: n for n in dcats}

def map_to_exam_cat(d_cids, default_cid):
    res = []
    for cid in d_cids:
        curr = cid
        while curr:
            if str(curr) in ecats:
                res.append(curr)
                break
            curr = dnode.get(curr, {}).get('parentId')
    if not res:
        res = [default_cid]
    return list(set(res))

# 3. 建立 2000~2026 真题套卷索引
exam_questions = []
def norm(s):
    return re.sub(r'[\s\$\\\{\}\(\)\_\^\+\-\=\,\.\;\:\'\"\`\(\)（）\u3000\[\]【】\/\<\>]', '', str(s)).lower()

for p in exam_data:
    pid = p.get('id', '')
    year = str(p.get('year', ''))
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            exam_questions.append({
                'pid': pid,
                'year': year,
                'no': str(q.get('no')),
                'qid': f"{pid}-{q.get('no')}",
                'q': q,
                'norm_stem': norm(q.get('stem', '')[:100])
            })

print(f"真题库索引构建完成: {len(exam_questions)} 题")

# 4. 构建 346 道重点线代题
chap_names = {
    'A': '一、行列式',
    'B': '二、矩阵',
    'C': '三、向量',
    'D': '四、线性方程组',
    'E': '五、特征值与特征向量',
    'F': '六、二次型'
}

sections = []
cur_chap_code = None
cur_sec_questions = []

matched_exam_cnt = 0
matched_existing_xd_cnt = 0
newly_imported_cnt = 0

for m in final_matches:
    num = m['pdf_num']
    chap_code = m['chapter'][0] if m['chapter'] else 'A'
    
    # 切章
    if chap_code != cur_chap_code:
        if cur_sec_questions:
            sections.append({
                'title': chap_names.get(cur_chap_code, cur_chap_code),
                'questions': cur_sec_questions
            })
            cur_sec_questions = []
        cur_chap_code = chap_code

    it = m['item']
    serial = str(m['dgy_serial'])
    isrc = str(it.get('source', ''))
    istem = norm(it.get('stem', '')[:100])
    
    # 查找是否有对应的数二真题
    found_eq = None
    my = re.search(r'(20\d\d|19\d\d)', isrc)
    if my and ('数二' in isrc or '数学二' in isrc):
        yr = my.group(1)
        for eq in exam_questions:
            if eq['year'] == yr:
                c = sum(1 for ch in istem[:40] if ch in eq['norm_stem'])
                if c / max(len(istem[:40]), 1) > 0.6:
                    found_eq = eq
                    break
    if not found_eq:
        for eq in exam_questions:
            if len(istem) >= 15 and len(eq['norm_stem']) >= 15:
                if istem[:20] in eq['norm_stem'] or eq['norm_stem'][:20] in istem:
                    found_eq = eq
                    break
                    
    # 构建题目对象
    # 考点映射
    raw_cids = it.get('categoryIds', [])
    # 针对第 60 题 (PDF 来源为 2008数一 矩阵的秩):
    default_cid = 27 if num == 60 else 24
    mapped_cids = map_to_exam_cat(raw_cids, default_cid)
    
    # 格式化来源前缀，例如 "2015 数一"
    source_tag = it.get('source', m['pdf_source'])
    
    if found_eq:
        matched_exam_cnt += 1
        # 最高优先级：使用本地真题卷的完整题干与解析内容，并且打上 linkedQid！
        eq_item = found_eq['q']
        q_obj = {
            'no': serial,
            'pdfNo': num,
            'linkedQid': found_eq['qid'],
            'stem': eq_item.get('stem', it.get('stem', '')),
            'options': eq_item.get('options', it.get('options', [])),
            'answer': eq_item.get('answer', it.get('answer', '')),
            'idea': eq_item.get('idea', it.get('explanation', '')),
            'source': source_tag,
            'categoryIds': mapped_cids
        }
    elif serial in existing_xd_map:
        matched_existing_xd_cnt += 1
        # 次高优先级：使用我们之前已经精细扩充、补全计算步骤与验算的 idea！
        prev_q = existing_xd_map[serial]
        q_obj = {
            'no': serial,
            'pdfNo': num,
            'stem': prev_q.get('stem', it.get('stem', '')),
            'options': prev_q.get('options', it.get('options', [])),
            'answer': prev_q.get('answer', it.get('answer', '')),
            'idea': prev_q.get('idea', it.get('explanation', '')),
            'source': source_tag,
            'categoryIds': mapped_cids
        }
    else:
        newly_imported_cnt += 1
        # 新增题目：使用大观园中的权威原版
        q_obj = {
            'no': serial,
            'pdfNo': num,
            'stem': it.get('stem', ''),
            'options': it.get('options', []),
            'answer': it.get('answer', ''),
            'idea': it.get('explanation', ''),
            'source': source_tag,
            'categoryIds': mapped_cids
        }
    cur_sec_questions.append(q_obj)

# 最后一章
if cur_sec_questions:
    sections.append({
        'title': chap_names.get(cur_chap_code, cur_chap_code),
        'questions': cur_sec_questions
    })

print(f"\n构建统计:")
print(f"  匹配真题卷 (带 linkedQid): {matched_exam_cnt}")
print(f"  保留已有详细解析 (来自原有 xd_bank): {matched_existing_xd_cnt}")
print(f"  新增导入题目 (来自大观园原库): {newly_imported_cnt}")
print(f"  总题数: {sum(len(s['questions']) for s in sections)}")

new_xd_bank = [{
    'id': 'xd',
    'title': '线性代数重点题（346题·35天做题本）',
    'sections': sections
}]

# 写入新的 xd_bank.json
with io.open('pwa/data/xd_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(new_xd_bank, f, ensure_ascii=False, separators=(',', ':'))

print("\n成功将新版 346 题写入 pwa/data/xd_bank.json！")
