# -*- coding: utf-8 -*-
"""数二大纲合规护栏：扫描答案字段里的数一/数三专属内容与考纲元话语。

用法：
    python tools/_audit_syllabus.py            # 硬断言 exam + mn26/mn27_yt4/mn27_papers.json
    python tools/_audit_syllabus.py --selftest # 反向验证：注入禁用词必须被抓到

说明：core_bank.json / ys27_items.json 等其它题库存在历史遗留的超纲题，
本护栏对它们只输出 INFO，不阻塞（待用户决定是否剔除整题）。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')

# 数一/数三专属考点（数二不考）
HARD = re.compile(
    r'伯努利方程|全微分方程|欧拉方程|第一类曲线积分|第二类曲线积分'
    r'|第一类曲面积分|第二类曲面积分|三重积分|曲面积分|曲线积分'
    r'|格林公式|高斯公式|斯托克斯|方向导数|散度|旋度'
    r'|幂级数|傅里叶级数|收敛半径'
    r'|随机变量|概率密度|数学期望|大数定律|中心极限定理|假设检验|参数估计'
    r'|差分方程|边际成本|需求弹性'
)
# 考纲对比 / 溯源元话语
META = re.compile(
    r'超纲|考纲|大纲|数一第|数三第|数一/|数一真题|数三真题'
    r'|本题原是数一|不要求掌握|超出数二'
)
# 无穷级数展开式：求和号自身上/下限含 \infty 或 k\ge1。
# 有限和 \sum_{k=1}^{n} 配 \lim_{n\to\infty}（定积分定义/黎曼和，数二考）不算。
SERIES = re.compile(
    r'\\sum(?:\\limits)?[\s\S]{0,40}?[\^_](?:\{)?\\infty'
    r'|\\sum(?:\\limits)?_\{?[a-zA-Z]\\ge\s*1\}?'
)
# 仅提示、不阻塞（数二范围内的普通用语，或需人工判定的边界词）
WARN = re.compile(r'积分因子|线性变换|向量空间|过渡矩阵|势函数|逐项积分|第一类间断点')


def iter_fields(dataset):
    """产出 (卷标识, 题号, 字段名, 文本)。兼容 exam/mn27/core 的 sections 结构。"""
    papers = dataset if isinstance(dataset, list) else [dataset]
    for p in papers:
        if not isinstance(p, dict):
            continue
        pid = str(p.get('id', '?'))
        sections = p.get('sections') or [p]
        for s in sections:
            if not isinstance(s, dict):
                continue
            for q in (s.get('questions') or []):
                no = q.get('no', '?')
                for k in ('stem', 'answer', 'idea'):
                    v = q.get(k)
                    if isinstance(v, str):
                        yield pid, no, k, v
                for i, o in enumerate(q.get('options') or []):
                    if isinstance(o, str):
                        yield pid, no, 'opt' + 'ABCD'[i] if i < 4 else 'opt' + str(i), o
                t = q.get('tips')
                if isinstance(t, dict):
                    for k, v in t.items():
                        if isinstance(v, str):
                            yield pid, no, 'tips.' + k, v
                        elif isinstance(v, list):
                            for x in v:
                                if isinstance(x, str):
                                    yield pid, no, 'tips.' + k, x
                elif isinstance(t, str):
                    yield pid, no, 'tips', t


CTRL = re.compile(r'[\x00-\x08\x0b-\x1f]')  # JSON 转义吃掉 LaTeX 反斜杠会留下 C0 控制字符


def detect(text):
    hits = []
    if CTRL.search(text):
        m = CTRL.search(text)
        hits.append(('LaTeX 反斜杠丢失', '<控制字符>',
                     text[max(0, m.start() - 30):m.end() + 30].replace('\n', ' ')))
    for name, rx in (('超纲考点', HARD), ('考纲元话语', META), ('无穷级数展开', SERIES)):
        for m in rx.finditer(text):
            hits.append((name, m.group(), text[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')))
    return hits


def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return json.load(f)


def scan_dataset(name, d):
    out = []
    for pid, no, fld, txt in iter_fields(d):
        for kind, word, ctx in detect(txt):
            out.append((name, pid, no, fld, kind, word, ctx))
    return out


def main():
    selftest = '--selftest' in sys.argv
    if selftest:
        # 反向验证：注入禁用词与无穷级数式，确认 detector 不漏
        cases = [
            ('这是 $n=2$ 的伯努利方程', '伯努利方程'),
            ('$\\ln(1-x)=-\\sum\\limits_{k=1}^{\\infty}\\frac{x^k}{k}$', '无穷级数展开'),
            ('全程只用考纲内的直角坐标方法', '考纲'),
            ('方程为全微分方程，存在势函数', '全微分方程'),
            ('导数恰为 $\x0crac12$', 'LaTeX 反斜杠丢失'),
        ]
        for txt, expect in cases:
            kinds = [k for k, _, _ in detect(txt)]
            words = [w for _, w, _ in detect(txt)]
            assert kinds, f'注入未检出: {txt}'
            assert expect in kinds or expect in words, f'注入检出类型不符: {txt} -> {kinds} {words}'
        # 数二正常写法不应命中
        for txt in ('有限阶 $\\sum_{k=1}^{n}\\frac{x^k}{k}+o(x^n)$',
                    '两边同乘 $x^2$，得 $(x^2z)\'=-1$',
                    '第一类间断点共 2 个'):
            assert not detect(txt), f'误报: {txt} -> {detect(txt)}'
        print('selftest OK：5 组注入全部检出，3 组数二正常写法无误报')
        return 0

    hard_files = ('exam.json', 'mn26_papers.json', 'mn27_yt4_papers.json', 'mn27_zs4_papers.json', 'mn27_papers.json')
    info_files = ('core_bank.json', 'ys27_items.json', 'xd_bank.json',
                  'dgy_items.json', 'bank_questions.json')
    errs, infos = [], []
    for name in hard_files + info_files:
        path = os.path.join(DATA, name)
        if not os.path.exists(path):
            continue
        rows = scan_dataset(name, load(name))
        (errs if name in hard_files else infos).extend(rows)
    if errs:
        print(f'ERROR: 硬断言题库发现 {len(errs)} 处数一/数三内容')
        for r in errs[:30]:
            print(f'  {r[0]} {r[1]} Q{r[2]} [{r[3]}] {r[4]} «{r[5]}» …{r[6]}')
        return 1
    print(f'PASS: exam.json + mn26/mn27_yt4/mn27_zs4/mn27_papers.json 零数一/数三专属内容（{len(hard_files)} 个题库）')
    if infos:
        print(f'INFO: 其它题库历史遗留 {len(infos)} 处（不阻塞，待决策）')
        seen = {}
        for r in infos:
            seen.setdefault((r[0], r[1], r[2]), set()).add(r[5])
        for (f, pid, no), words in list(seen.items())[:25]:
            print(f'  {f} {pid} Q{no}: {sorted(words)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
