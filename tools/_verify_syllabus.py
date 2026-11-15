# -*- coding: utf-8 -*-
"""本轮「剔除数一/数三内容」的独立验证：字段级 diff、结构不变、结论不变、产物同步。

与修复脚本 _fix_syllabus.py 完全独立；基线取自 git HEAD（未被本轮改动）。
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from _fix_syllabus import PATCH  # noqa: E402

EXAM = os.path.join(ROOT, 'pwa', 'data', 'exam.json')


def leaves(d):
    """(卷id, 题号, 字段路径) -> 文本；选项与 tips 展开到叶子。"""
    out = {}
    for p in d:
        pid = p['id']
        for s in p['sections']:
            for q in s['questions']:
                no = q['no']
                for k, v in q.items():
                    if k in ('options', 'tips', 'categoryIds', 'deepCats'):
                        continue
                    if isinstance(v, str):
                        out[(pid, no, k)] = v
                for i, o in enumerate(q.get('options') or []):
                    out[(pid, no, f'opt{i}')] = o
                t = q.get('tips') or {}
                if isinstance(t, dict):
                    for k, v in t.items():
                        out[(pid, no, 'tips.' + k)] = v
    return out


def main():
    # 固定基线：本轮改动前的 HEAD，避免脚本随后续提交推进而失效
    base_ref = os.environ.get('SYLLABUS_BASE', 'c369048')
    base = subprocess.check_output(['git', 'show', f'{base_ref}:pwa/data/exam.json'],
                                   cwd=ROOT).decode('utf-8')
    print(f'基线: git show {base_ref}:pwa/data/exam.json')
    old_d = json.loads(base)
    new_d = json.loads(open(EXAM, encoding='utf-8').read())
    o, n = leaves(old_d), leaves(new_d)

    assert set(o) == set(n), f'字段集合变化: 新增 {set(n) - set(o)}, 丢失 {set(o) - set(n)}'
    assert len(old_d) == len(new_d) == 27, '卷数变化'
    old_q = [(p['id'], q['no']) for p in old_d for s in p['sections'] for q in s['questions']]
    new_q = [(p['id'], q['no']) for p in new_d for s in p['sections'] for q in s['questions']]
    assert old_q == new_q, '题目顺序或题号变化'

    targets = {}
    for pid, no, path, old, new in PATCH:
        targets.setdefault((pid, no, path), []).append((old, new))
    assert len(targets) >= 19, f'目标字段数异常: {len(targets)}'
    assert all(k in o for k in targets), '目标字段不在基线中'

    # 历史缺陷字段：基线含 U+000C（\frac 被 JSON 吃掉反斜杠），本轮一并还原
    ctrl_keys = {k for k, v in o.items() if isinstance(v, str) and '\x0c' in v}
    assert len(ctrl_keys) == 9, f'控制字符字段数异常: {len(ctrl_keys)}'
    assert not (ctrl_keys & set(targets)), '控制字符字段与超纲替换目标重叠'

    changed = ctrl_changed = 0
    for key in o:
        ov, nv = o[key], n[key]
        if key in ctrl_keys:
            assert nv == ov.replace('\x0c', '\\f'), f'控制字符还原不正确: {key}'
            assert '\x0c' not in nv, f'控制字符残留: {key}'
            ctrl_changed += 1
            continue
        if key in targets:
            assert ov != nv, f'目标字段未改动: {key}'
            changed += 1
            for old, new in targets[key]:
                assert old not in nv, f'旧文本残留: {key} -> {old[:50]}'
                if new:
                    assert new in nv, f'新文本缺失: {key} -> {new[:50]}'
                else:
                    assert '数一第' not in nv, f'溯源注残留: {key}'
            # LaTeX 粗配对
            assert nv.count('$$') % 2 == 0, f'$$ 不配对: {key}'
            assert (nv.count('$') - 2 * nv.count('$$')) % 2 == 0, f'$ 不配对: {key}'
        else:
            assert ov == nv, f'非目标字段被改动: {key}'
    for v in n.values():
        if isinstance(v, str):
            assert '\x0c' not in v, '全库仍有控制字符'
    print(f'字段级 diff OK：共 {len(o)} 个叶子字段，'
          f'{changed} 个超纲替换字段 + {ctrl_changed} 个控制字符还原字段改动，其余逐字节一致')

    # 结论不变：答案头 / 最终结论断言
    byq = {(p['id'], q['no']): q for p in new_d for s in p['sections'] for q in s['questions']}
    checks = [
        ('2020数二真题', 4, r'-\frac{n!}{n-2}'),
        ('2026数二真题', 21, r'-4\ln(x-2)+11'),
        ('2025数二真题', 15, r'5y^2-4xy+3x^2=4'),
        ('2024数二真题', 18, r'\frac{22}{5}\sqrt3'),
        ('2023数二真题', 5, '选 (C)'),
        ('2000数二真题', 13, r'\frac{(-1)^{n-1}n!}{n-2}'),
        ('2010数二真题', 11, r'-2^{n}(n-1)!'),
        ('2014数二真题', 20, r'\lim\limits_{n\to\infty}nS_n=1'),
        ('2024数二真题', 7, '选 (B)'),
    ]
    for pid, no, frag in checks:
        q = byq[(pid, no)]
        tips = q.get('tips', {})
        blob = q['answer'] + ' '.join(str(v) for v in tips.values())
        assert frag in blob, f'结论疑似变化: {pid} Q{no} 缺 {frag}'
    print(f'结论不变 OK：{len(checks)} 道改动题的最终答案均与基线一致')

    # mn27 产物同步（由 _build_mn27.py 重建后校验）
    m = json.load(open(os.path.join(ROOT, 'pwa', 'data', 'mn27_papers.json'), encoding='utf-8'))
    q5 = [q for p in m if p['id'] == 'mn27-07'
          for s in p['sections'] for q in s['questions'] if q['no'] == 5][0]
    blob = q5['answer'] + q5['idea'] + json.dumps(q5.get('tips', {}), ensure_ascii=False)
    for bad in ('第一类曲线积分', r'\int_L'):
        assert bad not in blob, f'mn27-07 Q5 产物仍含 {bad}'
    assert r"\sqrt{x'^2(t)+y'^2(t)}" in q5['answer'], 'mn27-07 Q5 未换成弧长微元定积分'
    assert '\u9009 (C)' in q5['answer'] or 'C' in q5['answer'][:20], 'mn27-07 Q5 答案字母变化'
    print('mn27 产物同步 OK：q07 Q5 已无曲线积分术语/记号，结论仍为 (C)')

    print('VERIFY PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
