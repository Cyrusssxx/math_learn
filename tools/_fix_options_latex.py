#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全库扫描：options 里含裸 LaTeX（无 $ 包裹）的题。
判定：选项含 \\命令（长度≥2 的 LaTeX 命令）且不含 '$'。
输出：全部问题题清单 + 修复预览（整项包 $ 或需逐段处理）。
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, 'pwa/data/core_bank.json')

RE_LATEX = re.compile(r'\\[a-zA-Z]{2,}')
HAS_CN = re.compile(r'[\u4e00-\u9fff]')


def option_needs_fix(o):
    """选项需要修 = 含 LaTeX 命令 且 完全没有 $ 定界"""
    return bool(RE_LATEX.search(o)) and '$' not in o


def wrap(o):
    """整项包 $（仅当项内无中文）；含「【…】编者注」的拆开：LaTeX 部分包 $、注留外面；
    其余含中文的返回 None（需人工）"""
    m = re.match(r'^(.*?)(【.*)$', o, re.S)
    if m and RE_LATEX.search(m.group(1)) and not HAS_CN.search(m.group(1)):
        return '$' + m.group(1).strip() + '$' + m.group(2)
    if HAS_CN.search(o):
        return None
    return '$' + o.strip() + '$'


def main():
    apply = '--apply' in sys.argv
    cb = json.loads(io.open(CORE, encoding='utf-8').read())
    problems = []          # (section, q, auto_fixable)
    for s in cb[0]['sections']:
        for q in s['questions']:
            opts = q.get('options') or []
            bad = [o for o in opts if option_needs_fix(o)]
            if bad:
                problems.append((s['title'], q, bad))
    print('=== options 裸 LaTeX 的题：%d 道 ===' % len(problems))
    auto, manual = [], []
    for sec, q, bad in problems:
        wraps = []
        ok = True
        for o in q['options']:
            if option_needs_fix(o):
                w = wrap(o)
                if w is None:
                    ok = False
                    break
                wraps.append(w)
            else:
                wraps.append(o)
        rec = (sec, q, bad, wraps if ok else None)
        (auto if ok else manual).append(rec)
    print('可自动整项包 $：%d 道；含中文需人工：%d 道' % (len(auto), len(manual)))
    print()
    print('--- 可自动修复（前 12）---')
    for sec, q, bad, wraps in auto[:12]:
        print('  no=%-5s 节[%s] src=%s' % (q['no'], sec, str(q.get('source'))[:24]))
        print('     修前 opt0: %r' % (q['options'][0] or '')[:70])
        print('     修后 opt0: %r' % (wraps[0] or '')[:74])
    if manual:
        print()
        print('--- 需人工（含中文）---')
        for sec, q, bad, _ in manual[:10]:
            print('  no=%-5s 节[%s] opt0=%r' % (q['no'], sec, (q['options'][0] or '')[:70]))
    print()
    # 附加：stem 裸 LaTeX 检查（选项之外的题干，行内裸 \frac 等 —— 更少见，只统计）
    n_stem = 0
    for s in cb[0]['sections']:
        for q in s['questions']:
            st = q.get('stem') or ''
            # 排除已包裹的：粗查 —— $ 计数为奇数说明有未闭合，或含 \frac 且 $ 数为 0
            if RE_LATEX.search(st) and st.count('$') == 0 and not HAS_CN.search(st):
                n_stem += 1
    print('附加：题干纯 LaTeX 无 $ 的（ rare ）=', n_stem)
    if apply and auto:
        n = 0
        for sec, q, bad, wraps in auto:
            q['options'] = wraps
            n += 1
        io.open(CORE, 'w', encoding='utf-8').write(json.dumps(cb, ensure_ascii=False, separators=(',', ':')))
        print('已修复 %d 道并写回' % n)
    elif apply:
        print('无可自动修复的题')
    return 0


if __name__ == '__main__':
    sys.exit(main())
