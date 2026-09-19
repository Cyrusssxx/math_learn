# -*- coding: utf-8 -*-
"""核心题库非数二题的 idea 自动分段：把单段长文拆成多行，方便观看。
   - 已有换行的保持
   - 只在 $ / $$ 公式区间之外断行
   - 断点：句号/分号/冒号/「故、因此、于是、由此、令、则、由…知、首先/其次/最后」
   - 每行尽量 30-70 字符
dry-run：只统计，不写盘。"""
import json, io, re

BASE = 'D:/ai code/math-note/pwa/data/'
DOLLAR = re.compile(r'(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)')
# 断点：后接断行（句号/分号等保留在行尾）
BREAK = re.compile(r'(?<=[。；])|(?<=[：])')
KW = ['故', '因此', '于是', '由此', '即', '令', '从而', '所以', '再由', '先求', '再求', '注意到', '关键', '注', '而', '则', '代入', '化简', '两边', '对 ', '利用', '由 ']


def segment(idea):
    if not idea or '\n' in idea:
        return idea, False
    # 分 tokens（保护公式）
    parts = DOLLAR.split(idea)
    lines, buf = [], ''
    def flush():
        nonlocal buf
        if buf.strip():
            lines.append(buf.rstrip())
        buf = ''
    for t in parts:
        if t.startswith('$'):
            buf += t
            continue
        # 文本：按断点拆
        segs = BREAK.split(t)
        for s in segs:
            if not s:
                continue
            # 若缓冲行 + s 超长且 s 含断词 → 提前断
            cand = buf + s
            if len(cand) > 72 and buf:
                # 在关键词前断开
                cut = None
                for kw in KW:
                    i = s.find(kw)
                    if 8 <= i <= 40:
                        cut = i
                        break
                if cut is not None:
                    buf += s[:cut]
                    flush()
                    buf = s[cut:]
                else:
                    # 在缓冲内找最近的断词
                    ci = None
                    for kw in KW:
                        j = buf.rfind(kw)
                        if j > 10:
                            ci = j
                            break
                    if ci is not None:
                        buf, tail = buf[:ci], buf[ci:]
                        flush()
                        buf = tail + s
                    else:
                        buf = cand
            else:
                buf = cand
    flush()
    if len(lines) <= 1:
        return idea, False
    return '\n'.join(lines), True


def main():
    d = json.load(io.open(BASE + 'core_bank.json', encoding='utf-8'))
    qs = [q for s in d[0]['sections'] for q in s['questions'] if not q.get('linkedQid')]
    done = skip = 0
    samples = []
    for q in qs:
        v = q.get('idea') or ''
        nv, ch = segment(v)
        if ch:
            q['idea'] = nv
            done += 1
            if len(samples) < 4:
                samples.append((q['no'], v, nv))
        else:
            skip += 1
    print('分段：%d 题（保持 %d 题）' % (done, skip))
    for no, old, new in samples:
        print('=' * 60)
        print('题%s 原(%d字): %s' % (no, len(old), old[:120]))
        print('题%s 新(%d行):' % (no, new.count('\n') + 1))
        for L in new.split('\n'):
            print('   | ' + L[:80])
    if '--write' in __import__('sys').argv:
        with io.open(BASE + 'core_bank.json', 'w', encoding='utf-8', newline='') as fp:
            json.dump(d, fp, ensure_ascii=False, separators=(',', ':'))
        print('\n已写盘')
    else:
        print('\n（dry-run，未写盘）')


if __name__ == '__main__':
    main()
