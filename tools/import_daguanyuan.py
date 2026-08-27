#!/usr/bin/env python3
"""
大观园题库导入工具：将大观园数学二题目转换为 math-note 的 practice.json。
同时扩展 exam_categories.json 以包含大观园的完整分类层级。

使用方式：python tools/import_daguanyuan.py
"""

import json
import os
import shutil
from pathlib import Path

# 路径配置
DG_BASE = Path('D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets')
MN_BASE = Path('D:/ai code/math-note/pwa')

DG_QUESTIONS = DG_BASE / 'questions.json'
DG_CATEGORIES = DG_BASE / 'categories.json'
DG_IMAGES = DG_BASE / 'question_images'

MN_CATEGORIES = MN_BASE / 'data' / 'exam_categories.json'
MN_EXAM = MN_BASE / 'data' / 'exam.json'
MN_PRACTICE = MN_BASE / 'data' / 'practice.json'
MN_IMAGES = MN_BASE / 'assets' / 'question_images'

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def expand_categories():
    """
    扩展 exam_categories.json，加入大观园的完整分类层级。
    返回：(expanded_cats, dg_to_mn_id_map)
    - expanded_cats: 扩展后的 exam_categories.json
    - dg_to_mn_id_map: 大观园ID -> math-note ID 的映射
    """
    print('=== 扩展 exam_categories.json ===')
    
    # 加载两边的分类
    dg_cats = load_json(DG_CATEGORIES)['items']
    mn_cats = load_json(MN_CATEGORIES)
    
    # 按名字查找 math-note 中已有的分类
    mn_by_name = {}
    for k, v in mn_cats.items():
        mn_by_name[v['name']] = v
    
    # 找到 math-note 中最大的 ID
    max_mn_id = max(int(k) for k in mn_cats.keys())
    print(f'  math-note 最大 ID: {max_mn_id}')
    
    # 建立大观园 ID -> math-note ID 的映射
    dg_to_mn = {}
    
    # 第一遍：处理已存在的分类（按名字匹配）
    for dg_cat in dg_cats:
        name = dg_cat['name']
        if name in mn_by_name:
            dg_to_mn[dg_cat['id']] = mn_by_name[name]['id']
    
    print(f'  已存在（按名字匹配）: {len(dg_to_mn)}')
    
    # 第二遍：处理缺失的分类（按层级顺序，先处理父节点）
    # 按 parentId 排序，确保父节点先处理
    dg_cats_sorted = sorted(dg_cats, key=lambda x: (x.get('parentId') is None, x.get('parentId', 0)))
    
    added = 0
    for dg_cat in dg_cats_sorted:
        if dg_cat['id'] in dg_to_mn:
            continue  # 已处理
        
        # 生成新 ID
        max_mn_id += 1
        new_id = max_mn_id
        
        # 确定父节点 ID
        parent_id = None
        level = 0
        if dg_cat.get('parentId') is not None:
            parent_dg_id = dg_cat['parentId']
            if parent_dg_id in dg_to_mn:
                parent_id = dg_to_mn[parent_dg_id]
                # 根据父节点确定 level
                parent_mn = mn_cats.get(str(parent_id))
                if parent_mn:
                    level = parent_mn.get('level', 0) + 1
        
        # 添加到 math-note
        mn_cats[str(new_id)] = {
            'id': new_id,
            'name': dg_cat['name'],
            'display': dg_cat['name'],
            'parentId': parent_id,
            'level': level,
            'path': dg_cat.get('path', dg_cat['name'])
        }
        
        dg_to_mn[dg_cat['id']] = new_id
        added += 1
    
    print(f'  新增: {added}')
    print(f'  总计: {len(mn_cats)}')
    
    return mn_cats, dg_to_mn

def filter_math2_questions(dg_questions, dg_cats):
    """过滤出数学二题目，排除概率统计和历年真题分类"""
    print('=== 过滤数学二题目 ===')
    
    # 建立分类查找表
    cat_map = {x['id']: x for x in dg_cats}
    
    # 找到需要排除的 L0 分类 ID（概率统计、历年真题）
    exclude_l0_ids = set()
    for cat in dg_cats:
        if cat.get('parentId') is None and cat['name'] in ['概率统计', '历年真题']:
            exclude_l0_ids.add(cat['id'])
    print(f'  排除的 L0 分类: {exclude_l0_ids}')
    
    # 建立分类的 L0 祖先查找
    def get_l0_ancestor(cat_id):
        """获取分类的 L0 祖先 ID"""
        current = cat_map.get(cat_id)
        while current and current.get('parentId') is not None:
            current = cat_map.get(current['parentId'])
        return current['id'] if current else None
    
    math2_questions = []
    excluded_prob = 0
    excluded_exam = 0
    
    for q in dg_questions:
        source = q.get('source', '')
        # 匹配 "数二" 或 "数学二"
        if '数二' not in source and '数学二' not in source:
            continue
        
        # 检查是否属于排除的分类
        category_ids = q.get('categoryIds', [])
        is_excluded = False
        
        for cat_id in category_ids:
            l0_id = get_l0_ancestor(cat_id)
            if l0_id in exclude_l0_ids:
                is_excluded = True
                # 统计排除原因
                if l0_id == next(x for x in exclude_l0_ids if cat_map[x]['name'] == '概率统计'):
                    excluded_prob += 1
                else:
                    excluded_exam += 1
                break
        
        if not is_excluded:
            math2_questions.append(q)
    
    print(f'  总题目: {len(dg_questions)}')
    print(f'  数学二（原始）: {len(math2_questions) + excluded_prob + excluded_exam}')
    print(f'  排除概率统计: {excluded_prob}')
    print(f'  排除历年真题: {excluded_exam}')
    print(f'  数学二（最终）: {len(math2_questions)}')
    
    return math2_questions

def convert_question(q, dg_to_mn, no):
    """转换单个题目格式"""
    # 映射题型
    kind_map = {
        'single_choice': 'choice',
        'multiple_choice': 'choice',
        'subjective': 'blank'
    }
    kind = kind_map.get(q.get('type', 'subjective'), 'blank')
    
    # 构建 stem（选择题把选项也放进去）
    stem = q.get('stem', '')
    if kind == 'choice' and q.get('options'):
        options_text = '\n'.join(f'{chr(65+i)}. {opt}' for i, opt in enumerate(q['options']))
        stem = stem + '\n' + options_text
    
    # 合并 answer + explanation
    answer = q.get('answer', '')
    explanation = q.get('explanation', '')
    if answer and explanation:
        combined = f'【答案】{answer}\n\n【解析】{explanation}'
    elif answer:
        combined = f'【答案】{answer}'
    elif explanation:
        combined = f'【解析】{explanation}'
    else:
        combined = ''
    
    # 映射 categoryIds
    category_ids = []
    for dg_id in q.get('categoryIds', []):
        if dg_id in dg_to_mn:
            category_ids.append(dg_to_mn[dg_id])
    
    # 处理图片引用
    img = None
    if q.get('assets'):
        # 大观园用 asset://sha256/<hash> 引用图片
        for asset in q['assets']:
            if asset.startswith('asset://sha256/'):
                hash_val = asset.split('/')[-1]
                img = f'question_images/{hash_val}.png'
                break  # 只取第一张图
    
    return {
        'no': no,
        'kind': kind,
        'stem': stem,
        'options': q.get('options', []) if kind == 'choice' else [],
        'answer': combined,
        'idea': '',
        'img': img,
        'categoryIds': category_ids,
        'source': q.get('source', ''),
        'dg_id': q['id']  # 保留原始 ID 用于去重
    }

def dedup_questions(questions, existing_exam):
    """按题干相似度去重"""
    print('=== 去重处理 ===')
    
    # 提取现有真题的题干（简化版：取前100字符）
    existing_stems = set()
    for paper in existing_exam:
        for sec in paper.get('sections', []):
            for q in sec.get('questions', []):
                stem = q.get('stem', '')[:100].strip()
                if stem:
                    existing_stems.add(stem)
    
    print(f'  现有真题题干数: {len(existing_stems)}')
    
    # 过滤重复题目
    filtered = []
    dup_count = 0
    for q in questions:
        stem = q.get('stem', '')[:100].strip()
        if stem in existing_stems:
            dup_count += 1
            continue
        filtered.append(q)
    
    print(f'  去重前: {len(questions)}')
    print(f'  去重后: {len(filtered)}')
    print(f'  去除重复: {dup_count}')
    
    return filtered

def create_practice_json(questions, expanded_cats):
    """创建 practice.json，按 math-note 的 L0/L1 层级分卷"""
    print('=== 创建 practice.json ===')
    
    # 建立 math-note 分类查找表
    mn_cat_map = {int(k): v for k, v in expanded_cats.items()}
    
    # 获取 L0/L1 祖先
    def get_l0_l1(cat_id):
        """获取分类的 L0 和 L1 祖先 (name, name)"""
        cat = mn_cat_map.get(cat_id)
        if not cat:
            return None, None
        
        # 向上找 L1 和 L0
        current = cat
        l1_name = None
        l0_name = None
        
        while current:
            if current.get('level') == 1:
                l1_name = current['name']
            elif current.get('level') == 0:
                l0_name = current['name']
                break
            parent_id = current.get('parentId')
            if parent_id is None:
                break
            current = mn_cat_map.get(parent_id)
        
        return l0_name, l1_name
    
    # 按 L0 学科分组
    l0_groups = {}  # l0_name -> { l1_name -> [questions] }
    
    for q in questions:
        # 找到题目的 L0 和 L1 分类
        l0_name = None
        l1_name = None
        
        for cat_id in q.get('categoryIds', []):
            l0, l1 = get_l0_l1(cat_id)
            if l0:
                l0_name = l0
                l1_name = l1 or '未分类'
                break
        
        if not l0_name:
            # 没有找到分类，放到"其他"
            l0_name = '其他'
            l1_name = '未分类'
        
        if l0_name not in l0_groups:
            l0_groups[l0_name] = {}
        if l1_name not in l0_groups[l0_name]:
            l0_groups[l0_name][l1_name] = []
        l0_groups[l0_name][l1_name].append(q)
    
    # 构建 practice.json
    papers = []
    for l0_name, l1_groups in l0_groups.items():
        sections = []
        for l1_name, qs in l1_groups.items():
            # 重新编号
            for i, q in enumerate(qs, 1):
                q['no'] = i
            sections.append({
                'title': l1_name,
                'questions': qs
            })
        
        paper_id = f'practice-{l0_name.lower().replace(" ", "-")}'
        papers.append({
            'id': paper_id,
            'year': '0',  # 用 0 表示练习卷，排序时会排在最后
            'title': f'大观园·{l0_name}',
            'file': '',
            'sections': sections
        })
    
    print(f'  生成卷数: {len(papers)}')
    for p in papers:
        total = sum(len(s['questions']) for s in p['sections'])
        print(f'    {p["title"]}: {len(p["sections"])} 章节, {total} 题')
    
    return papers

def copy_images(questions):
    """复制题目图片"""
    print('=== 复制图片 ===')
    
    # 收集所有需要的图片
    needed_images = set()
    for q in questions:
        if q.get('img'):
            # 从路径中提取文件名
            filename = q['img'].split('/')[-1]
            needed_images.add(filename)
    
    print(f'  需要图片: {len(needed_images)}')
    
    # 创建目标目录
    MN_IMAGES.mkdir(parents=True, exist_ok=True)
    
    # 复制图片
    copied = 0
    missing = 0
    for filename in needed_images:
        src = DG_IMAGES / filename
        dst = MN_IMAGES / filename
        if src.exists():
            if not dst.exists():  # 不覆盖已存在的
                shutil.copy2(src, dst)
                copied += 1
        else:
            missing += 1
            print(f'    缺失: {filename}')
    
    print(f'  复制: {copied}')
    print(f'  缺失: {missing}')

def main():
    print('大观园题库导入工具')
    print('=' * 50)
    
    # 1. 扩展分类
    expanded_cats, dg_to_mn = expand_categories()
    
    # 2. 加载题目
    dg_data = load_json(DG_QUESTIONS)
    dg_questions = dg_data['items']
    dg_cats = load_json(DG_CATEGORIES)['items']
    
    # 3. 过滤数学二
    math2_questions = filter_math2_questions(dg_questions, dg_cats)
    
    # 4. 转换格式
    print('=== 转换题目格式 ===')
    converted = []
    for i, q in enumerate(math2_questions, 1):
        converted.append(convert_question(q, dg_to_mn, i))
    print(f'  转换完成: {len(converted)}')
    
    # 5. 去重
    existing_exam = load_json(MN_EXAM)
    deduped = dedup_questions(converted, existing_exam)
    
    # 6. 创建 practice.json
    practice = create_practice_json(deduped, expanded_cats)
    
    # 7. 复制图片
    copy_images(deduped)
    
    # 8. 保存文件
    print('=== 保存文件 ===')
    save_json(MN_CATEGORIES, expanded_cats)
    print(f'  保存: {MN_CATEGORIES}')
    
    save_json(MN_PRACTICE, practice)
    print(f'  保存: {MN_PRACTICE}')
    
    print()
    print('导入完成！')
    print(f'  新增题目: {len(deduped)}')
    print(f'  分类节点: {len(expanded_cats)}')
    print(f'  练习卷: {len(practice)}')

if __name__ == '__main__':
    main()
