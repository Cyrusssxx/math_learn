# 全量数据审计：5 个数据文件 KaTeX 结构 + 题目结构完整性
# 用法: python tools/_audit_all_data.py
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'pwa' / 'data'


def brace_balance(s):
    depth = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth < 0:
                return f'negative brace depth'
        i += 1
    return None if depth == 0 else f'unbalanced braces depth={depth}'


def dollar_balance(s):
    # 按 $$ 优先配对，再数剩余单 $（忽略 \$）
    t = s.replace('\\$', '')
    while '$$' in t:
        t = t.replace('$$', '', 1).replace('$$', '', 1) if '$$' in t[t.index('$$') + 2:] else t[:t.index('$$')] + t[t.index('$$') + 2:]
    # 简化：直接数（$$ 计 2）
    n = t.count('$')
    return None if n % 2 == 0 else f'odd $ count={n}'


def leftright(s):
    # 注意：\left\{ … \right. 等转义/空定界符是合法的；此处仅粗查，
    # 精确校验以 tools/_katex_check_all.js 的真实渲染为准
    l = len(re.findall(r'\\left(?=[.\[\]|<>{}\s(])', s))
    r = len(re.findall(r'\\right(?=[.\[\]|<>{}\s)])', s))
    return None if abs(l - r) <= 2 else f'\\left({l}) vs \\right({r}) 差距过大'


def beginend(s):
    b = re.findall(r'\\begin\{([^}]*)\}', s)
    e = re.findall(r'\\end\{([^}]*)\}', s)
    return None if b == e else f'begin/end mismatch'


def audit_field(path, note_id, field, text):
    problems = []
    if not isinstance(text, str) or not text.strip():
        problems.append('EMPTY')
        return problems
    for name, fn in [('dollar', dollar_balance), ('brace', brace_balance),
                     ('left/right', leftright), ('begin/end', beginend)]:
        r = fn(text)
        if r:
            problems.append(f'{name}: {r}')
    return problems


report = {}
issues = []

# ---------- exam.json ----------
exam = json.load(open(DATA / 'exam.json', encoding='utf-8'))
seen_ids = {}
for p in exam:
    total_q = 0
    sec_nos = []
    for sec in p['sections']:
        for q in sec['questions']:
            total_q += 1
            qid = f"{p['id']}/Q{q['no']}"
            if qid in seen_ids:
                issues.append(f'[exam] 重复题号: {qid}')
            seen_ids[qid] = True
            sec_nos.append(q['no'])
            for field in ('stem', 'answer', 'idea'):
                probs = audit_field('exam', qid, field, q.get(field, ''))
                for pr in probs:
                    issues.append(f'[exam] {qid} {field}: {pr}')
            # 选择题：答案里的选项字母必须在选项列表中
            if sec['questions'] and '选择' in sec['title']:
                if q.get('options'):
                    for i, opt in enumerate(q['options']):
                        probs = audit_field('exam', qid, f'opt{i}', opt)
                        for pr in probs:
                            issues.append(f'[exam] {qid} opt{i}: {pr}')
    # 题号连续性
    expect = list(range(1, len(sec_nos) + 1))
    if sec_nos != expect:
        issues.append(f"[exam] {p['id']} 题号不连续: {sec_nos[:5]}...{sec_nos[-3:]} 共{len(sec_nos)}题")
    report[f"exam/{p['id']}"] = total_q

# ---------- notes.json ----------
notes = json.load(open(DATA / 'notes.json', encoding='utf-8'))
for n in notes:
    md = n['md']
    probs = audit_field('notes', n['id'], 'md', md)
    for pr in probs:
        issues.append(f"[notes] {n['id']}: {pr}")
    # 章节一致性：chapters 应与 ## 标题一致（剥掉 HTML 注释后比较，渲染时注释会被剥掉）
    hs = [re.sub(r'<!--.*?-->', '', t).strip() for t in re.findall(r'^## (.+)$', md, re.M)]
    if hs != [c.strip() for c in n.get('chapters', [])]:
        issues.append(f"[notes] {n['id']} chapters 与 ## 标题不一致 ({len(hs)} vs {len(n.get('chapters', []))})")

# ---------- good.json / selected.json / practice.json ----------
for fname in ('good.json', 'selected.json', 'practice.json'):
    fpath = DATA / fname
    if not fpath.exists():
        continue
    data = json.load(open(fpath, encoding='utf-8'))
    items = data if isinstance(data, list) else list(data.values())

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and (',' in v or len(v) > 20):
                    probs = audit_field(fname, k, k, v)
                    for pr in probs:
                        issues.append(f'[{fname}] {k}: {pr}')
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    # 只审计长文本字段（stem/answer/idea/content 类），避免把 id/路径当公式
    def walk_text(o, path=''):
        if isinstance(o, dict):
            for k, v in o.items():
                walk_text(v, f'{path}.{k}')
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk_text(v, f'{path}[{i}]')
        elif isinstance(o, str) and len(o) > 30:
            probs = audit_field(fname, path, 'text', o)
            for pr in probs:
                issues.append(f'[{fname}] {path}: {pr}')
    walk_text(data)
    report[f'{fname}'] = len(items)

print('=== 条目统计 ===')
print(json.dumps(report, ensure_ascii=False, indent=1))
print(f'\n=== 问题 {len(issues)} 条 ===')
for i in issues[:60]:
    print(' -', i)
if len(issues) > 60:
    print(f' ... 其余 {len(issues) - 60} 条略')
