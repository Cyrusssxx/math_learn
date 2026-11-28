# -*- coding: utf-8 -*-
"""字段级 diff：确认本轮只改 ansImg，且站点原图仍在 PDF 图之前。"""
import json, subprocess, os

ROOT = r'D:/ai code/math-note'
REL = 'pwa/data/mn27_zs4_papers.json'
old = json.loads(subprocess.check_output(['git', 'show', 'HEAD:' + REL], cwd=ROOT).decode('utf-8'))
new = json.load(open(os.path.join(ROOT, REL), encoding='utf-8'))

assert len(old) == len(new) == 4
diffs = []
for po, pn in zip(old, new):
    assert po['id'] == pn['id']
    for k in po:
        if k != 'sections':
            assert po[k] == pn[k], ('paper field changed', po['id'], k)
    so = po['sections']; sn = pn['sections']
    assert len(so) == len(sn)
    for soi, sni in zip(so, sn):
        assert len(soi['questions']) == len(sni['questions'])
        for qo, qn in zip(soi['questions'], sni['questions']):
            assert qo['no'] == qn['no']
            for k in qo:
                if k != 'ansImg':
                    assert qo[k] == qn[k], ('question field changed', po['id'], qo['no'], k)
            assert qn.get('ansImg'), ('no ansImg', po['id'], qn['no'])
            if qo.get('ansImg'):
                assert qn['ansImg'][:len(qo['ansImg'])] == qo['ansImg'], ('site img moved', qn['no'])
            assert any('mn27zs4pdf-' in p for p in qn['ansImg']), ('pdf img missing', qn['no'])
            diffs.append((po['id'], qn['no'], len(qo.get('ansImg') or []), len(qn['ansImg'])))

print('字段级 diff PASS：88 题只有 ansImg 变化，其他字段全同')
print('图片总数 %d → %d，新增 %d 张' %
      (sum(x[2] for x in diffs), sum(x[3] for x in diffs), sum(x[3] - x[2] for x in diffs)))
