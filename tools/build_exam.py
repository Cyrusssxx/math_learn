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
    cur_q = None        # {no, kind, stem:[], options:[], answer:[]}
    in_answer = False
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line == ':::':
            in_answer = False
            i += 1
            continue
        if line.startswith('::: answer'):
            in_answer = True
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
                     'options': [], 'answer': []}
            in_answer = False
            i += 1
            continue
        # 普通行
        if in_answer:
            cur_q['answer'].append(raw)
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
    if q['options']:
        q['kind'] = 'choice'
    if not q['answer'] and q['kind'] == 'choice':
        q['kind'] = 'choice'
    sec['questions'].append(q)


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    papers = []
    if src.is_dir():
        for path in sorted(src.glob('*.md')):
            if path.stem == '说明':
                continue
            papers.append(parse(path))
    else:
        papers.append(parse(src))
    papers.sort(key=lambda p: p['year'], reverse=True)  # 新→旧
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / 'exam.json'
    out.write_text(json.dumps(papers, ensure_ascii=False), encoding='utf-8')
    for p in papers:
        nq = sum(len(s['questions']) for s in p['sections'])
        print(f"{p['id']}: {len(p['sections'])} 大节, {nq} 题, {len(json.dumps(p, ensure_ascii=False))//1024}KB")
    print(f"共 {len(papers)} 套卷 → {out} ({out.stat().st_size // 1024}KB)")


if __name__ == '__main__':
    main()
