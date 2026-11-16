# -*- coding: utf-8 -*-
"""清理收藏池两道题答案里的 AI 套话 / 不支持的 ### 标题。数学内容一字不动。

- DG900JXB-802：删套话开头；`### 命题 X：Y` -> `**命题 X：Y**`（题卡 mdBlock 只认 **加粗**）。
- core-150：删套话开头。
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DGY = os.path.join(ROOT, 'pwa', 'data', 'dgy_items.json')
CORE = os.path.join(ROOT, 'pwa', 'data', 'core_bank.json')

DGY_LEAD = ('这种考察抽象函数导数与极限定性关系的题目，非常契合考研数学中对微积分基本定理、'
            '中值定理以及函数性态（单调性、凹凸性、渐近态）的综合考察要求。\n\n'
            '我们来逐一分析这四个命题：\n\n')
CORE_LEAD = ('这是一个典型的利用导数定义和函数方程求解的问题。为了保证逻辑的绝对严密，我们必须'
             '直接从极限与导数的定义出发，先证明 $x=1$ 处的导数存在，再计算其具体数值，'
             '绝不能在未验证域内处处可导的情况下对等式两边直接求导。\n\n')


def patch_802(ans):
    assert ans.startswith('【答案】B\n\n'), ans[:40]
    assert DGY_LEAD in ans, '套话未命中'
    ans = ans.replace('【答案】B\n\n' + DGY_LEAD, '【答案】B\n\n', 1)
    # ### 命题 ①：正确 -> **命题 ①：正确**
    ans2, n = re.subn(r'^### (命题 [①②③④][：:][^\n]+)$', r'**\1**', ans, flags=re.M)
    assert n == 4, f'### 标题命中 {n}（应为 4）'
    return ans2


def patch_150(ans):
    assert CORE_LEAD in ans, '套话未命中'
    return ans.replace(CORE_LEAD, '', 1)


def main():
    with open(DGY, encoding='utf-8') as f:
        dgy = json.load(f)
    n = 0
    for p in dgy:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                if p['id'] == 'DG900JXB' and q.get('no') == 802:
                    q['answer'] = patch_802(q['answer']); n += 1
    assert n == 1, f'dgy 命中 {n}'
    with open(DGY, 'w', encoding='utf-8', newline='') as f:
        json.dump(dgy, f, ensure_ascii=False)

    with open(CORE, encoding='utf-8') as f:
        core = json.load(f)
    m = 0
    for p in core:
        for s in p.get('sections', []):
            for q in s.get('questions', []):
                if q.get('no') == 150 and not q.get('linkedQid'):
                    q['answer'] = patch_150(q['answer']); m += 1
    assert m == 1, f'core 命中 {m}'
    with open(CORE, 'w', encoding='utf-8', newline='') as f:
        json.dump(core, f, indent=1, ensure_ascii=False)

    print(f'patched dgy-802={n}, core-150={m}')


if __name__ == '__main__':
    main()
