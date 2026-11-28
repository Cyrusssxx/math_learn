# -*- coding: utf-8 -*-
"""从站点原始抓取 _zs4_raw.json 生成 mn27_zs4_papers.json（27张宇四套卷·数二）。
规则与 mn26/mn27_yt4 一致：
  - 4 卷 × 22 题，id mn27-zs4-1..4，group=mock，qid = <卷id>-<no>
  - answer = 【答案】+正确答案 + **【解】** + 清洗后的解析
  - idea  = 「思路」：从解析粗体步骤标题抽取（无则取首句），人工可读
  - 保留 siteId/siteSource 交叉引用；原图按源文件顺序写 ansImg
  - 剥掉「数三原卷对照/数二原卷对应」元话语（过大纲护栏）
  - 剥掉「### 原始参考答案（源文件顺序）」段与 asset:// 链接（原图走 ansImg）
"""
import json, re, os

ROOT = r'D:/ai code/math-note'
RAW = os.path.join(ROOT, 'tools/_zs4_raw.json')
AMAP = os.path.join(ROOT, 'tools/_zs4_asset_map.json')
OUT = os.path.join(ROOT, 'pwa/data/mn27_zs4_papers.json')
CATS = [12981, 12982, 12983, 12984]
TITLES = [
    '27 张宇四套卷·第一套', '27 张宇四套卷·第二套',
    '27 张宇四套卷·第三套', '27 张宇四套卷·第四套',
]

def clean_exp(exp):
    # 剥「原始参考答案」段（含其后的 asset 图）
    exp = re.sub(r'\n?###?\s*原始参考答案[^\n]*\n?', '\n', exp)
    exp = re.sub(r'!\[[^\]]*\]\(asset://[^)]*\)', '', exp)
    # 剥元话语段落（数三原卷对照 / 数二原卷对应）
    exp = re.sub(r'\n?\*\*数三原卷对照：\*\*[^\n]*', '', exp)
    exp = re.sub(r'\n?\*\*数二原卷对应：\*\*[^\n]*', '', exp)
    exp = re.sub(r'原始参考答案（源文件顺序）', '', exp)
    return exp.strip()

def derive_idea(exp, qt, correct):
    # 抽取解析中的粗体步骤标题（如 **先求驻点。** / **（1）...**），拼成一句
    bolds = re.findall(r'\*\*([^*\n]{2,60}?)\*\*', exp)
    steps = []
    for b in bolds:
        b = b.strip()
        if not b or b.startswith('答案') or b in ('解', '证明', '分析'):
            continue
        if b.endswith('：') or b.endswith(':'):
            continue
        steps.append(b.rstrip('。'))
    if steps:
        body = '；'.join(steps[:3])
    else:
        # 退回：取首句（到第一个句号或换行），去掉公式块
        first = re.split(r'[\n。]', exp, 1)[0].strip()
        first = re.sub(r'\$\$[\s\S]*?\$\$', '', first).strip()
        body = first[:70] or ('正确选项为 ' + correct if correct else '按题意推演')
    return '「思路」：' + body + '。'

def correct_of(it):
    a = it['answer']
    if 'option_ids' in a:
        letter = {'opt-a': 'A', 'opt-b': 'B', 'opt-c': 'C', 'opt-d': 'D'}
        return letter.get(a['option_ids'][0], a['option_ids'][0])
    return a.get('reference_answer_md', '')

def kind_of(qt):
    return {'single_choice': 'choice', 'fill': 'fill', 'essay': 'calc', 'subjective': 'calc'}[qt]

def build():
    raw = json.load(open(RAW, encoding='utf-8'))
    amap = json.load(open(AMAP, encoding='utf-8'))
    papers = []
    for idx, cat in enumerate(CATS, 1):
        items = sorted(raw[str(cat)]['items'], key=lambda x: x['serial_number'])
        questions = []
        for it in items:
            doc = it['document']
            no = it['serial_number']
            stem = doc['stem_md']
            qt = doc['question_type']
            options = []
            if qt == 'single_choice':
                letters = 'ABCD'
                for k, o in enumerate(doc['options']):
                    options.append('(%s) %s' % (letters[k], o['content_md']))
            corr = correct_of(it)
            exp = clean_exp(doc.get('explanation_md') or '')
            answer = '【答案】' + (('选 (' + corr + ')。') if qt == 'single_choice' and corr in 'ABCD' else corr)
            answer += '\n\n**【解】**\n' + exp
            idea = derive_idea(exp, qt, corr)
            q = {
                'no': no, 'kind': kind_of(qt), 'stem': stem, 'options': options,
                'answer': answer, 'idea': idea, 'tips': {}, 'categoryIds': [],
                'origin': '27张四卷·第%d套 / Q%d' % (idx, no),
                'siteId': it['id'],
                'siteSource': doc.get('source') or it.get('source') or '',
            }
            imgs = amap.get('%d-%d' % (idx, no))
            if imgs:
                q['ansImg'] = imgs['paths']
            # 视频：站点该套未抓，先不写（与 yt4 0 视频一致）
            questions.append(q)
        sections = [
            {'title': '一、选择题（1—10）', 'questions': questions[:10]},
            {'title': '二、填空题（11—16）', 'questions': questions[10:16]},
            {'title': '三、解答题（17—22）', 'questions': questions[16:]},
        ]
        papers.append({
            'id': 'mn27-zs4-%d' % idx, 'year': '27模拟', 'title': TITLES[idx-1],
            'group': 'mock',
            'source': '2027 张宇四套卷·数二·第%d套（大观园 category %d）' % (idx, cat),
            'pages': '大观园 category %d' % cat,
            'sections': sections,
        })
    json.dump(papers, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('saved', OUT, 'papers', len(papers), 'questions', sum(len(s['questions']) for p in papers for s in p['sections']))
    print('ansImg questions:', [(p['id'], q['no']) for p in papers for s in p['sections'] for q in s['questions'] if q.get('ansImg')])

if __name__ == '__main__':
    build()
