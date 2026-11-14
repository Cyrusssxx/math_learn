# -*- coding: utf-8 -*-
"""由 tools/mn27_ans/ 下的题干、答案草稿生成 pwa/data/mn27_papers.json。

用法：python tools/_build_mn27.py
结构对齐 exam.json，额外字段 group='mock' 供 exam.js 左栏分组。
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'mn27_ans')
OUT = os.path.join(HERE, '..', 'pwa', 'data', 'mn27_papers.json')

# (草稿标签, 卷 id, 卷标题, 题本页码, 答案册文件)
PAPERS = [
    ('03', 'mn27-03', '27 李林四套卷·第二套', 'p11–p14', '03_27李林四套卷数二第二套答案'),
    ('04', 'mn27-04', '27 李林四套卷·第三套', 'p15–p18', '04_27李林四套卷数二第三套答案'),
    ('05', 'mn27-05', '27 超越十套卷·第二套', 'p19–p22', '05_27超越十套卷数二第二套答案'),
    ('06', 'mn27-06', '27 超越十套卷·第四套', 'p23–p26', '06_27超越十套卷数二第四套答案'),
    ('07', 'mn27-07', '27 超越十套卷·第八套', 'p27–p30', '07_27超越十套卷数二第八套答案'),
]

# 需要裁图才能表达的题： (草稿标签, 题号) -> (src, alt)
FIGS = {
    ('04', 3): ('data/img/mn27/mn27_q04_03.png', '三条曲线示意图'),
}

SEP = re.compile(r'(?====Q(\d+)===)')
SECTIONS = [
    ('一、选择题（1—10）', range(1, 11)),
    ('二、填空题（11—16）', range(11, 17)),
    ('三、解答题（17—22）', range(17, 23)),
]


def read_blocks(path):
    s = open(path, encoding='utf-8').read()
    parts = SEP.split(s)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        out[int(parts[i])] = parts[i + 1]
    return out


def field(block, tag):
    m = re.search(r'【' + tag + r'】(.*?)(?=\n【|\Z)', block, re.S)
    return m.group(1).strip() if m else ''


def build_q(tag, no, sb, ab):
    kind = field(sb, '题型') or ('choice' if no <= 10 else ('blank' if no <= 16 else 'calc'))
    stem = field(sb, '题干')
    assert stem, f'{tag} Q{no} 缺题干'

    # 【配图】草稿标记 → 题卡图片语法（mdBlock 白名单只认 data/img/...）
    if '【配图】' in sb:
        fig = FIGS.get((tag, no))
        assert fig, f'{tag} Q{no} 声明配图但没有裁图映射'
        stem = re.sub(r'\n?【配图】[^\n]*', '', stem).strip()
        stem += '\n\n![' + fig[1] + '](' + fig[0] + ')'

    options = []
    if kind == 'choice':
        for c in 'ABCD':
            v = field(sb, c)
            assert v, f'{tag} Q{no} 缺选项 {c}'
            options.append('(' + c + ') ' + v)

    raw_ans = field(ab, '答案')
    solve = field(ab, '解')
    idea_txt = field(ab, '思路')
    yc = field(ab, '易错')
    assert raw_ans, f'{tag} Q{no} 缺答案'
    assert solve, f'{tag} Q{no} 缺解析'

    a = raw_ans.strip()
    if kind == 'choice' and re.fullmatch(r'[A-D]', a):
        head = f'【答案】选 ({a})。'
    else:
        head = f'【答案】{a}'
    answer = head + '\n\n**【解】**\n' + solve

    q = {
        'no': no,
        'kind': kind,
        'stem': stem,
        'options': options,
        'answer': answer,
        'idea': '「思路」：' + idea_txt if idea_txt else '',
        'tips': {'yc': yc} if yc else {},
        'categoryIds': [],
        'origin': f'{tag} / Q{no}',
    }
    return q


def main():
    papers = []
    for tag, pid, title, pages, ansfile in PAPERS:
        sb = read_blocks(os.path.join(SRC, f'q{tag}_stem.md'))
        ab = read_blocks(os.path.join(SRC, f'q{tag}_ans.md'))
        assert sorted(sb) == list(range(1, 23)), f'{tag} 题干题号不全'
        assert sorted(ab) == list(range(1, 23)), f'{tag} 答案题号不全'
        secs = []
        for sec_title, nos in SECTIONS:
            qs = [build_q(tag, n, sb[n], ab[n]) for n in nos]
            secs.append({'title': sec_title, 'questions': qs})
        papers.append({
            'id': pid,
            'year': '27模拟',
            'title': title,
            'group': 'mock',
            'source': ansfile,
            'pages': pages,
            'sections': secs,
        })

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(json.dumps(papers, ensure_ascii=False, indent=1) + '\n')

    total = sum(len(s['questions']) for p in papers for s in p['sections'])
    print(f'写出 {os.path.normpath(OUT)}：{len(papers)} 套 / {total} 题 / {os.path.getsize(OUT)} 字节')
    for p in papers:
        n = sum(len(s['questions']) for s in p['sections'])
        print(f"  {p['id']} {p['title']}  {n} 题")


if __name__ == '__main__':
    main()
