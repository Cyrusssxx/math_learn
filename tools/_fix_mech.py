# -*- coding: utf-8 -*-
"""机械修复（安全三类规则），作用于 core_bank.json / exam.json 全部字段：
   R1 环境感知的行内 \\（深度 0 处）→ 真实换行（matrix/cases/aligned 等环境内的 \\ 保留）
   R2 删除行内 \tag{...}
   R3 $...$ 内的连续中文 → \text{中文}（KaTeX 中文 warn 消除）
dry-run 默认，--write 写盘。"""
import json, io, re, sys

BASE = 'D:/ai code/math-note/pwa/data/'
HAN = re.compile(r'[\u4e00-\u9fff]+')
ENV_BEGIN = re.compile(r'\\begin\{')
ENV_END = re.compile(r'\\end\{')
TAG = re.compile(r'\\tag\{[^}]*\}')


def fix_double_backslash(text):
    """深度 0 处 \\ → 换行（保留环境内的）"""
    lines = text.split('\n')
    out = []
    depth = 0
    for L in lines:
        s = L
        while True:
            b = ENV_BEGIN.search(s)
            e = ENV_END.search(s)
            # 找第一个 \begin 或 \end 或 \\ 的位置
            bi = b.start() if b else -1
            ei = e.start() if e else -1
            bs = s.find('\\\\')
            nxt = min(x for x in (bi if bi >= 0 else 10**9, ei if ei >= 0 else 10**9,
                                  bs if bs >= 0 else 10**9))
            if nxt == 10**9:
                break
            if nxt == bs and (nxt < bi or bi < 0) and (nxt < ei or ei < 0):
                if depth == 0:
                    # 行内 \\ → 换行（拆行处理）
                    head = s[:nxt]
                    s = s[nxt + 2:]
                    out.append(head)
                    # 继续处理 s 剩余部分（可能还有 \\）
                    continue
                else:
                    s = s[:nxt] + '\\\\' + s[nxt + 2:]
                    continue
            elif nxt == bi:
                depth += 1
                s = s[:bi + len('\\begin{')] + s[bi + len('\\begin{'):]  # 吃掉 \\begin{ 标记
                # 简化：直接跳过这个 begin 命令文本（保持原样），但深度已 +
                # 需要保留原文 → 恢复到完整匹配
                s = L_restore(s, b, 'begin')
                break
            else:
                depth -= 1
                break
        # 上面逻辑复杂，改为简化实现（见下方主循环）
        out.append(s)
    # 简化版其实有问题，改用第二套实现
    return _fix_dd_v2(text)


def _fix_dd_v2(text):
    lines = text.split('\n')
    out = []
    depth = 0
    disp = False
    for L in lines:
        s = L.strip()
        if s == '$$':
            disp = not disp
            out.append(L)
            continue
        if disp:
            out.append(L)      # 显示块内：\\ 是 KaTeX 换行，保留
            continue
        events = []
        for m in ENV_BEGIN.finditer(L):
            events.append(('b', m.start()))
        for m in ENV_END.finditer(L):
            events.append(('e', m.start()))
        for p in re.finditer(r'\\\\', L):
            events.append(('\\', p.start()))
        events.sort(key=lambda x: x[1])
        cur = 0
        buf = ''
        changed = False
        for typ, pos in events:
            if typ == 'b':
                depth += 1
            elif typ == 'e':
                depth -= 1
            else:
                if depth == 0:
                    buf += L[cur:pos] + '\n'
                    cur = pos + 2
                    changed = True
        buf += L[cur:]
        if changed:
            out.extend(buf.split('\n'))
        else:
            out.append(L)
    return '\n'.join(out)


def fix_cn_in_math(text):
    def repl(m):
        inner = m.group(1)
        if not HAN.search(inner):
            return m.group(0)
        # 中文连续块 → \text{...}
        fixed = HAN.sub(lambda mm: '\\text{' + mm.group(0) + '}', inner)
        return '$' + fixed + '$'
    return re.sub(r'(?<!\$)\$([^$\n]+)\$(?!\$)', repl, text)


def apply_field(v):
    orig = v
    v = _fix_dd_v2(v)
    v = TAG.sub('', v)
    v = fix_cn_in_math(v)
    return v, v != orig


if __name__ == '__main__':
    DRY = '--write' not in sys.argv
    for tag, path, iterate in (
        ('core', BASE + 'core_bank.json',
         lambda d: [q for s in d[0]['sections'] for q in s['questions']]),
        ('exam', BASE + 'exam.json',
         lambda d: [q for v in d for s in v.get('sections', []) for q in s.get('questions', [])]),
    ):
        d = json.load(io.open(path, encoding='utf-8'))
        changed = 0
        for q in iterate(d):
            for f in ('stem', 'answer', 'idea'):
                v = q.get(f) or ''
                if not v:
                    continue
                nv, ch = apply_field(v)
                if ch:
                    if not DRY:
                        q[f] = nv
                    changed += 1
        if not DRY:
            with io.open(path, 'w', encoding='utf-8', newline='') as fp:
                json.dump(d, fp, ensure_ascii=False, separators=(',', ':'))
        print('%s%s：修改字段 %d 个' % (tag, '(dry)' if DRY else '', changed))
