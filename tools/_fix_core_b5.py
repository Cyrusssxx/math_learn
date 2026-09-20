# -*- coding: utf-8 -*-
# 通用块状态机规范化：处理 core-274/283/424 的 AI 长解答字段
import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = 'pwa/data/core_bank.json'

def load():
    with open(SRC, encoding='utf-8') as f:
        return json.load(f)

def find_q(data, no):
    for s in data[0]['sections']:
        for q in s['questions']:
            if str(q['no']) == str(no):
                return q
    return None

def is_bare_math(line):
    """裸公式行：不含中文、不含 $、含 LaTeX 命令 或 以数学符号开头"""
    l = line.strip()
    if not l or '$' in l or re.search(r'[\u4e00-\u9fff]', l):
        return False
    if '\\' in l:
        return True
    return bool(re.match(r'^[=+\-0-9a-zA-Z\\{}_^,.()]+$', l)) and bool(re.search(r'[a-zA-Z0-9\\]', l))

def normalize(s):
    """块状态机：$$ 独立行开/闭块；块内行收集；块外裸公式行自动开块；空块压扁"""
    lines = s.split('\n')
    out = []
    buf = None      # None=不在块内，否则为内容list
    for raw in lines:
        l = raw.strip()
        if buf is not None:
            if l == '$$' :
                # 关闭块
                content = [x for x in buf if x.strip()]
                if content:
                    out.append('$$')
                    out.extend(buf)
                    out.append('$$')
                buf = None
                continue
            buf.append(raw)
            continue
        # 不在块内
        if l == '$$':
            buf = []
            continue
        if l.startswith('$$') and l.endswith('$$') and len(l) > 4:
            # 同行块 $$X$$
            out.append(raw)
            continue
        if is_bare_math(l):
            buf = [raw]   # 裸公式行开块
            continue
        out.append(raw)
    if buf is not None:
        content = [x for x in buf if x.strip()]
        if content:
            out.append('$$')
            out.extend(buf)
            out.append('$$')
    return '\n'.join(out)

def fix_274(s):
    s = normalize(s)
    return s

def fix_283(s):
    s = normalize(s)
    return s

def fix_424(s):
    s = normalize(s)
    return s

FIX = {
    'core-274.answer': fix_274,
    'core-283.answer': fix_283,
    'core-424.answer': fix_424,
}

if __name__ == '__main__':
    data = load()
    for k, fn in FIX.items():
        no = k.split('-')[1].split('.')[0]
        field = k.split('.')[1]
        q = find_q(data, no)
        old = q[field]
        new = fn(old)
        print(k, 'changed:', new != old, 'len', len(old), '->', len(new))
        q[field] = new
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('written.')