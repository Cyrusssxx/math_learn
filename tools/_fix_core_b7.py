# -*- coding: utf-8 -*-
# 批次7：块重构器——对 283/424 把「$$ 配对 + 裸公式行独立成块」规范化
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

def is_math_line(l):
    """裸公式行：不含中文、不含 $、长度>3、含任意 LaTeX 命令或数学符号"""
    t = l.strip()
    if not t or '$' in t or re.search(r'[\u4e00-\u9fff]', t):
        return False
    if '\\' in t and len(t) > 3:
        return True
    # 全是纯数学符号（如 = a + b ^2 等，无 \ 命令）——少见，不强行包
    return False

def rebuild(s):
    """产出规范文本：所有公式一律成对 $$ 独立块；中文/段落行原样保留"""
    lines = s.split('\n')
    out = []
    i = 0
    n = len(lines)
    while i < n:
        l = lines[i]
        t = l.strip()
        if t == '$$':
            # 找配对的下一个 $$（跳过中间；若中间有中文也保留为块内容？mdBlock 会把块内行都当公式）
            j = i + 1
            buf = []
            while j < n and lines[j].strip() != '$$':
                buf.append(lines[j])
                j += 1
            if j >= n:
                # 无配对 → 当作普通文本行处理（删除孤立的 $$）
                out.append(l)
                i += 1
                continue
            # 块内有内容则输出块；空块跳过
            content = [x for x in buf if x.strip()]
            if content:
                out.append('$$')
                out.extend(buf)
                out.append('$$')
            # 若块内全是中文（误配）→ 拆开
            i = j + 1
            continue
        if is_math_line(l):
            # 该裸公式行若是「跟在 $$ 块后/前」，包成独立块
            out.append('$$')
            out.append(l)
            out.append('$$')
            i += 1
            continue
        out.append(l)
        i += 1
    return '\n'.join(out)

def chop_424(s):
    """424 特例：中文行与公式同一行（如 「故 4\dfrac{...}」）→ 公式包 $"""
    s = re.sub(r'^故 ([^$\n]*)$', lambda m: '故 $' + m.group(1).strip() + '$', s)
    # 行内 纯公式段前接中文（如 得\n$$ 已处理）；这里处理 “=X\n$$” 缺开块形式
    return s

def fix_283(s):
    return rebuild(s)

def fix_424(s):
    return chop_424(rebuild(s))

if __name__ == '__main__':
    data = load()
    for k, fn in [('core-283.answer', fix_283), ('core-424.answer', fix_424)]:
        no = k.split('-')[1].split('.')[0]
        field = k.split('.')[1]
        q = find_q(data, no)
        old = q[field]
        new = fn(old)
        print(k, 'changed:', new != old, 'len', len(old), '->', len(new))
        q[field] = new
    json.dump(data, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('written.')