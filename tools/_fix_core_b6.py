# -*- coding: utf-8 -*-
# 批次6：压缩连续 $$ 行 + 中文混合公式行包 $ + 渲染验证循环
import json, io, sys, re, subprocess, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = 'pwa/data/core_bank.json'
NODE = r'C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe'
LOCATE = r'C:/Users/cjx/.workbuddy/binaries/node/workspace/_t_locate_core.js'

def load():
    with open(SRC, encoding='utf-8') as f:
        return json.load(f)

def find_q(data, no):
    for s in data[0]['sections']:
        for q in s['questions']:
            if str(q['no']) == str(no):
                return q
    return None

def compress_blocks(s):
    """把连续两行都是 $$ 的合并为一行 $$；并清理累计影响"""
    lines = s.split('\n')
    out = []
    for l in lines:
        if l.strip() == '$$' and len(out) > 0 and out[-1].strip() == '$$':
            continue  # 跳过连续重复的 $$ 行
        out.append(l)
    s = '\n'.join(out)
    # 再做一次：被压缩后可能出现“$$(空)$$”同行或空块对，二次清理 `\n$$\n\n$$\n`
    s = re.sub(r'\n\$\$\n\n\$\$\n', '\n$$\n', s)
    return s

def chop_mixed(s):
    """中文+公式混合行：把行内裸公式段包 $（针对 故 4\dfrac... 这类）"""
    # 模式：中文 后跟 裸LaTeX（含 \ 命令）直至行尾 → 中文留外，公式包 $
    # 如 "故 4\dfrac{a}{b}+12\dfrac{c}{d}" → "故 $4\dfrac{a}{b}+12\dfrac{c}{d}$"
    def repl(m):
        pre = m.group(1)          # 中文前缀（含空格）
        body = m.group(2)         # 公式体
        return pre + '$' + body.strip() + '$'
    s = re.sub(r'([\u4e00-\u9fff][^$\n]{0,12}?)\s*(\\[a-zA-Z]+\{[^\n]*?(?:=[^\n]*)?)', repl, s)
    return s

def fix_283(s):
    s = compress_blocks(s)
    return s

def fix_424(s):
    s = compress_blocks(s)
    # “故 4\dfrac{...}+...” 中文混合行 —— compress 后该行可能是独立行
    lines = s.split('\n')
    out = []
    for l in lines:
        t = l.strip()
        if t.startswith('故 ') and '\\dfrac' in t and not t.startswith('$$'):
            body = t[2:].strip()
            if not body.startswith('$'):
                out.append('故 $' + body + '$')
                continue
        if not l.startswith('$$') and not t.startswith('$$'):
            # 中文绘同行内裸公式（非 $ 起的 \partial 长链行）
            if re.search(r'[\u4e00-\u9fff]', t) and t.count('$') == 0 and '\\' in t:
                # 如 "由复合函数链式法则得\qquad ..." 之类，暂不自动包，交给验证
                pass
        out.append(l)
    return '\n'.join(out)

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
    # 渲染自检
    env = dict(os.environ, NODE_PATH=r'C:/Users/cjx/.workbuddy/binaries/node/workspace/node_modules')
    r = subprocess.run([NODE, LOCATE], capture_output=True, text=True, encoding='utf-8', env=env, cwd='D:/ai code/math-note')
    for line in r.stdout.splitlines():
        if '###' in line and '已无残留' not in line:
            print('BAD:', line)
    print('--- done ---')