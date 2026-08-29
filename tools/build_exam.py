# -*- coding: utf-8 -*-
"""build_exam.py — 把真题 Markdown 打包成语料数据（math-note 真题页面构建脚本）
用法：python -X utf8 build_exam.py [源目录...]
    源目录默认 D:\\ai code\\数学二真题（相对本脚本推导），输出 ../pwa/data/exam.json

源文件格式（每套卷一个 md）：
    # 2023年数学（二）真题
    ## 一、选择题
    ### 1. 题干…（可多行，含 $KaTeX$）
    (A) 选项1
    (B) 选项2
    (C) 选项3
    (D) 选项4
    ::: answer
    答案与解析…（可多行）
    :::
    ### 2. …

输出结构：
    [{
      id, year, title, file,
      sections: [{
        title,  // 一、选择题
        questions: [{
          no, kind: 'choice'|'blank'|'solve',
          stem,       // 题干（含选项内联到题干尾，纯文本带 $...$）
          options,    // 选择题才有：['(A) …', …]
          answer,     // ::: answer 块内容
        }]
      }]
    }]
"""
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DATA_DIR = TOOLS.parent / 'pwa' / 'data'
DEFAULT_SRC = TOOLS.parent.parent / '数学二真题'


def parse(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    year_m = re.search(r'(\d{4})', path.stem)
    year = year_m.group(1) if year_m else path.stem

    title = ''
    if lines and lines[0].startswith('# '):
        title = lines[0][2:].strip()
        lines = lines[1:]

    paper = {'id': path.stem, 'year': year, 'title': title or path.stem,
             'file': path.stem + '.md', 'sections': []}

    cur_sec = None      # {title, questions:[]}
    cur_q = None        # {no, kind, stem:[], options:[], answer:[], idea:[], tips:{}}
    in_answer = False
    in_idea = False
    in_tips = False
    tip_key = None      # 当前点睛段位：gs公式/yc易错/jq技巧/zy注意
    TIP_KEYS = {'公式': 'gs', '易错': 'yc', '技巧': 'jq', '注意': 'zy', '坑': 'yc'}
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line == ':::':
            in_answer = False
            in_idea = False
            in_tips = False
            tip_key = None
            i += 1
            continue
        if line.startswith('::: answer'):
            in_answer = True
            in_idea = False
            in_tips = False
            i += 1
            continue
        if line.startswith('::: idea'):
            in_idea = True
            in_answer = False
            in_tips = False
            i += 1
            continue
        if line.startswith('::: 点睛'):
            in_tips = True
            in_answer = False
            in_idea = False
            tip_key = None
            if cur_q is not None and 'tips' not in cur_q:
                cur_q['tips'] = {}
            i += 1
            continue
        if line.startswith('## '):
            if cur_sec and cur_q:
                finalize_q(cur_sec, cur_q)
            cur_sec = {'title': line[3:].strip(), 'questions': []}
            cur_q = None
            paper['sections'].append(cur_sec)
            i += 1
            continue
        if line.startswith('### '):
            if cur_sec is None:
                cur_sec = {'title': '', 'questions': []}
                paper['sections'].append(cur_sec)
            if cur_q:
                finalize_q(cur_sec, cur_q)
            head = line[4:].strip()
            no_m = re.match(r'^(\d+)', head)
            no = int(no_m.group(1)) if no_m else (len(cur_sec['questions']) + 1)
            kind = 'choice' if head.endswith('C') else 'blank'  # 占位，随后按选项修正
            # 去掉题号后的分隔符（点、空格、顿号等），避免 "." 混入题干
            stem_head = re.sub(r'^[\s.、，,;；:：\-]+', '', head[no_m.end():])
            cur_q = {'no': no, 'kind': kind, 'stem': [stem_head],
                     'options': [], 'answer': [], 'idea': []}
            in_answer = False
            in_idea = False
            in_tips = False
            tip_key = None
            i += 1
            continue
        # 普通行
        if in_answer:
            cur_q['answer'].append(raw)
        elif in_idea:
            cur_q['idea'].append(raw)
        elif in_tips:
            m = re.match(r'^【([^】]+)】\s*(.*)$', line)
            if m and m.group(1) in TIP_KEYS:
                tip_key = TIP_KEYS[m.group(1)]
                cur_q['tips'].setdefault(tip_key, [])
                if m.group(2):
                    cur_q['tips'][tip_key].append(m.group(2))
            elif tip_key:
                cur_q['tips'][tip_key].append(raw)
        elif cur_q is not None and re.match(r'^\((A|B|C|D)\)', line):
            cur_q['options'].append(line)
        elif cur_q is not None:
            cur_q['stem'].append(raw)
        i += 1
    if cur_sec and cur_q:
        finalize_q(cur_sec, cur_q)

    # 补充分类：有选项→choice
    for sec in paper['sections']:
        for q in sec['questions']:
            if q['options']:
                q['kind'] = 'choice'
    return paper


def finalize_q(sec, q):
    q['stem'] = '\n'.join(x for x in q['stem'] if x).strip()
    q['answer'] = '\n'.join(x for x in q['answer'] if x).strip()
    if q['idea']:
        q['idea'] = '\n'.join(x for x in q['idea'] if x).strip()
    else:
        q.pop('idea', None)
    if q.get('tips'):
        tips = {k: '\n'.join(x for x in v if x).strip() for k, v in q['tips'].items()}
        q['tips'] = {k: v for k, v in tips.items() if v}   # 空段位丢弃
        if not q['tips']:
            del q['tips']
    if q['options']:
        q['kind'] = 'choice'
    if not q['answer'] and q['kind'] == 'choice':
        q['kind'] = 'choice'
    sec['questions'].append(q)


def check_math_balance(paper):
    """构建期预警：某题题干/答案的 $$ 不配对会导致 KaTeX 渲染失败。"""
    for sec in paper['sections']:
        for q in sec['questions']:
            for key in ('stem', 'answer', 'idea'):
                v = q.get(key, '')
                if v.count('$$') % 2 != 0:
                    print(f"  [WARN] {paper['id']} {sec['title']} Q{q['no']} {key}: "
                          f"$$ 不配对({v.count('$$')}个)，KaTeX 可能渲染失败")


def preserve_category_ids(papers, out):
    """重建会把分类脚本后处理写入的 categoryIds 抹掉——从现有 exam.json 按
    「套卷id + 题目顺序」原样搬回（顺序由源 md 决定，重建不会改变）。"""
    if not out.exists():
        return
    try:
        old = json.loads(out.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        print('  [WARN] 旧 exam.json 读取失败，跳过 categoryIds 保留')
        return
    old_map = {p['id']: [q for s in p['sections'] for q in s['questions']] for p in old}
    kept = 0
    for p in papers:
        oqs = old_map.get(p['id'])
        if not oqs:
            continue
        nqs = [q for s in p['sections'] for q in s['questions']]
        if len(oqs) != len(nqs):
            print(f"  [WARN] {p['id']} 题数变化({len(oqs)}→{len(nqs)})，categoryIds 不搬运，需重跑分类")
            continue
        for oq, nq in zip(oqs, nqs):
            if oq.get('categoryIds'):
                nq['categoryIds'] = oq['categoryIds']
                kept += 1
    print(f"  categoryIds 保留: {kept} 题")


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    papers = []
    if src.is_dir():
        for path in sorted(src.glob('*.md')):
            if path.stem == '说明':
                continue
            p = parse(path)
            check_math_balance(p)
            papers.append(p)
    else:
        papers.append(parse(src))
    papers.sort(key=lambda p: p['year'], reverse=True)  # 新→旧
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / 'exam.json'
    preserve_category_ids(papers, out)
    out.write_text(json.dumps(papers, ensure_ascii=False), encoding='utf-8')
    for p in papers:
        nq = sum(len(s['questions']) for s in p['sections'])
        print(f"{p['id']}: {len(p['sections'])} 大节, {nq} 题, {len(json.dumps(p, ensure_ascii=False))//1024}KB")
    print(f"共 {len(papers)} 套卷 → {out} ({out.stat().st_size // 1024}KB)")


if __name__ == '__main__':
    main()
