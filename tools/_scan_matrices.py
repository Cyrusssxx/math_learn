# -*- coding: utf-8 -*-
import json, io

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

for pid in ['2022数二真题', '2024数二真题']:
    paper = next(p for p in exam_data if p['id'] == pid)
    print(f"\n==================== 扫描 {pid} 的所有题干中的 LaTeX 矩阵格式 ====================")
    for sec in paper.get('sections', []):
        for q in sec.get('questions', []):
            stem = q.get('stem', '')
            no = q.get('no')
            # 检查是否有缺少换行 \\ 的情况，比如 \begin{pmatrix}1\lambda... 或 1\\1\lambda 等
            # 或者 pmatrix 中只有单斜杠或者反斜杠被吞的情况
            if 'begin{pmatrix}' in stem or 'begin{bmatrix}' in stem:
                print(f"[{no}] {stem}")
