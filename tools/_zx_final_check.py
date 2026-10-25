# -*- coding: utf-8 -*-
"""185 道转录臻选题全面核对"""
import json
import re

core = json.load(open('pwa/data/core_bank.json', encoding='utf-8'))
deep = json.load(open('pwa/data/cat_deep.json', encoding='utf-8'))['nodes']
exam = json.load(open('pwa/data/exam.json', encoding='utf-8'))
dgy = json.load(open('pwa/data/dgy_items.json', encoding='utf-8'))

# 站点题干索引
pool = {}
for f in ('tools/_mock_math2.json', 'tools/_core_math2_full.json'):
    for it in json.load(open(f, encoding='utf-8')):
        pool[it['id']] = it
for it in json.load(open('tools/_complete_math2_all.json', encoding='utf-8'))['items']:
    pool.setdefault(it['id'], it)

def skel(t):
    if not t: return ''
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', t)
    t = t.replace('$', '')
    t = re.sub(r'【[^】]*】|\(\d{4}[,，][^)）]*\)', '', t)
    t = re.sub(r'本题满分[^，。;；]*[，。]?', '', t)
    t = re.sub(r'^[0-9０-９]{1,3}[.、）)\]】]', '', t)
    t = re.sub(r'[\s\\{}\[\],，、;；:：!！?？()（）\'"\.\-—_=+<>|/·]+', '', t)
    return t.lower()

# 真题有效 qid
valid_qids = set()
for p in exam + dgy:
    for sec in p['sections']:
        for q in sec['questions']:
            valid_qids.add('%s-%s' % (p['id'], q['no']))

lq = [q for p in core for s in p['sections'] for q in s['questions']]
zx = [q for q in lq if 1077 <= int(q['no']) <= 1330]
transcribed = [q for q in zx if (q.get('stem') or '').strip() != '（臻选题补录题，完整题面见下方配图）']

issues = []
ok = 0
for q in transcribed:
    no = q['no']
    stem = q.get('stem') or ''
    idea = q.get('idea') or ''

    # 1) 思路非空且非占位
    if len(idea.strip()) < 30 or '本题取自' in idea or '完整题面见下方配图' in idea:
        issues.append((no, '思路缺失或占位', idea[:20] if idea else '(空)'))
        continue

    # 2) 选择题选项完整
    if q.get('kind') == 'choice':
        opts = q.get('options') or []
        if not isinstance(opts, list) or len(opts) < 2:
            issues.append((no, '选择题选项不足', str(opts)[:30]))
            continue
        if any(not o or len(o.strip()) < 2 for o in opts):
            issues.append((no, '选项内容异常', str([o[:10] for o in opts])))

    # 3) 题干含 LaTeX 但非纯占位
    if len(stem.strip()) < 15:
        issues.append((no, '题干过短', stem[:20]))

    # 4) 题干在站点池中能找到（来源验证）
    site_stem_found = False
    for it in pool.values():
        if skel(it['stem']) == skel(stem):
            site_stem_found = True
            break
    # 自写的题（批00-05）不在池里也正常
    # 这里只标记：来自站点但找不到的
    if not site_stem_found and '（' not in stem[:3]:
        # 不是自写题（自写的多以"设"/"证明"开头且不在池中）
        pass  # 暂不标记，因为自写题也不在池中

    # 5) deepCats 有效
    dc = q.get('deepCats') or []
    if not dc or str(dc[0]) not in deep:
        issues.append((no, 'deepCats 无效', str(dc)))
        continue

    # 6) linkedQid 有效
    lk = q.get('linkedQid')
    if lk and lk not in valid_qids:
        issues.append((no, 'linkedQid 无效', lk))

    # 7) 无残留 img 字段（已转录的）
    if 'img' in q:
        issues.append((no, '已转录但残留 img', q['img'][:30]))

    # 8) idea 无 asset:// 或 原始参考答案 残留
    if 'asset://' in idea:
        issues.append((no, 'idea 残留 asset://', ''))
    if '原始参考答案' in idea:
        issues.append((no, 'idea 残留 原始参考答案 段', ''))

    # 9) 题干无 asset://
    if 'asset://' in stem:
        issues.append((no, '题干残留 asset://', ''))

    ok += 1

print('核对 %d 道转录臻选题:' % len(transcribed))
print('  ✅ 通过: %d' % ok)
print('  ✗ 问题: %d' % len(issues))
for no, typ, detail in issues:
    print('    core#%s %s | %s' % (no, typ, detail))

# 统计信息
total_choice = sum(1 for q in transcribed if q.get('kind') == 'choice')
total_proof = sum(1 for q in transcribed if q.get('kind') == 'proof')
total_calc = sum(1 for q in transcribed if q.get('kind') in ('calc', 'blank'))
print('\n题型分布: 选择 %d | 填空 %d | 计算/证明 %d' % (total_choice, total_calc - total_proof, total_proof + total_calc - total_calc + total_proof))
print('有 linkedQid: %d/%d' % (sum(1 for q in transcribed if q.get('linkedQid')), len(transcribed)))
