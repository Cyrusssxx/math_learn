# -*- coding: utf-8 -*-
"""重建 yancai_bank.json：修正 _merge_all.py 无条件加倍反斜杠造成的 LaTeX 污染。

策略：
- p11-20 无独立批次文件，从现有 bank 中直接继承（已审计为干净）。
- p21+ 从 tools/_q_p*.json 重新解析：对每个文件尝试两种解析方式（原样 / 全加倍），
  用「污染计数 + 控制字符数」评分，取更干净的一种。
- 以 (page, order) 为唯一键去重；输出异常报告供人工复核。
"""
import json, io, glob, os, re

ROOT = 'D:/ai code/math-note/tools/'
BANK = ROOT + 'yancai_bank.json'

# 匹配「真实双反斜杠 + 字母」，即 LaTeX 命令被双写污染（json.dumps 后为 4 个反斜杠）
POLLUTE = re.compile(r'\\\\[A-Za-z]+')      # 作用于真实字符串，不是 dumps 结果


def pollute_count(obj):
    """递归统计字符串值里 '\\\\命令' 污染个数（真实字符串层面）"""
    n = 0
    if isinstance(obj, str):
        n += len(POLLUTE.findall(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            n += pollute_count(v)
    elif isinstance(obj, list):
        for v in obj:
            n += pollute_count(v)
    return n


def ctrl_count(obj):
    """统计字符串里的控制字符（\\b \\f \\t 被误解析的痕迹）"""
    n = 0
    if isinstance(obj, str):
        n += len(re.findall(r'[\x08\x0c\x07\x0b]', obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            n += ctrl_count(v)
    elif isinstance(obj, list):
        for v in obj:
            n += ctrl_count(v)
    return n


def load_best(path):
    """返回 (arr, mode, score)"""
    raw = io.open(path, encoding='utf-8').read()
    cands = []
    for mode, text in (('as-is', raw), ('doubled', raw.replace('\\', '\\\\'))):
        try:
            arr = json.loads(text)
        except Exception as e:
            continue
        score = pollute_count(arr) + ctrl_count(arr) * 5
        cands.append((score, mode, arr))
    if not cands:
        return None, 'FAIL', 10 ** 9
    cands.sort(key=lambda x: (x[0], 0 if x[1] == 'as-is' else 1))
    score, mode, arr = cands[0]
    return arr, mode, score


def main():
    bank = json.load(io.open(BANK, encoding='utf-8'))
    old = bank['questions']
    # 1) 保留 p11-20（无批次文件，且已审计干净）
    keep = [q for q in old if q['page'] <= 20]
    print('继承 p11-20：%d 题（污染 %d）' % (len(keep), pollute_count(keep)))

    questions = list(keep)
    seen = {q['id'] for q in questions}
    pages = set(q['page'] for q in questions)
    report = []

    files = sorted(glob.glob(ROOT + '_q_p*.json'))
    dup_in_file = []
    for f in files:
        arr, mode, score = load_best(f)
        base = os.path.basename(f)
        if arr is None:
            report.append((base, 'PARSE-FAIL', mode, -1, -1))
            print('!! 解析失败', base)
            continue
        added = 0
        local = set()
        for q in arr:
            qid = 'yc-%s-%s' % (q['page'], q['order'])
            if qid in local:
                dup_in_file.append((base, qid, q.get('source'), q.get('stem', '')[:40]))
            local.add(qid)
            if qid in seen:
                continue
            q['id'] = qid
            q['catId'] = None
            q['status'] = 'transcribed'
            questions.append(q)
            seen.add(qid)
            pages.add(q['page'])
            added += 1
        report.append((base, mode, score, len(arr), added))

    print()
    print('%-20s %-9s %-7s %-6s %s' % ('文件', '解析模式', '异常分', '题数', '新增'))
    for r in report:
        print('%-20s %-9s %-7s %-6s %s' % r)

    if dup_in_file:
        print()
        print('!! 同一文件内 (page,order) 重复（子代理编号错误，需人工看）:')
        for d in dup_in_file:
            print('  ', d)

    questions.sort(key=lambda q: (q['page'], q['order']))
    bank['questions'] = questions
    bank['meta']['transcribed_pages'] = sorted(pages)
    bank['meta']['question_count'] = len(questions)

    with io.open(BANK, 'w', encoding='utf-8', newline='') as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)

    print()
    print('重建完成：总题数 %d | 有题页数 %d | 残留污染 %d | 控制字符 %d'
          % (len(questions), len(pages), pollute_count(questions), ctrl_count(questions)))


if __name__ == '__main__':
    main()
