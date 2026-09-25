# -*- coding: utf-8 -*-
import json, io, re

with io.open('pwa/data/exam.json', 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

print("=== 扫描全库 exam.json 所有年份题干中缺少换行 \\\\ 的矩阵 ===")
# 匹配类似 \begin{pmatrix} 或 \begin{bmatrix} 中出现数字紧贴字母且无 \\ 的情况，比如 1\lambda 或 1\\1\lambda 等
bad_matrix = []
for paper in exam_data:
    pid = paper.get('id', '')
    for sec in paper.get('sections', []):
        for q in sec.get('questions', []):
            stem = q.get('stem', '')
            no = q.get('no')
            # 搜索 pmatrix 或 bmatrix
            matrices = re.findall(r'\\begin\{(?:p|b|v|V)matrix\}(.*?)\\end\{(?:p|b|v|V)matrix\}', stem, re.DOTALL)
            for mat in matrices:
                # 检查是否有形如 1\lambda, \lambda\lambda, a\lambda, 数字\lambda, \lambda^2 紧贴数字等缺失 \\ 的特征
                if re.search(r'[0-9a-zA-Z]\\[a-zA-Z]', mat) or re.search(r'\\[a-zA-Z]+[0-9a-zA-Z]', mat):
                    # 排除合法的像 2a, 3b, \lambda^2 等
                    # 查找具体的异常：紧随 \lambda 没有空格也没有操作符的数字或字母，如 1\lambda 或 \lambda\lambda
                    if re.search(r'\d\\lambda', mat) or re.search(r'\\lambda[a-zA-Z0-9]', mat):
                        bad_matrix.append((pid, no, mat))

print(f"扫描发现疑似损坏矩阵: {len(bad_matrix)} 处")
for item in bad_matrix:
    print(item[0], "题号:", item[1], "矩阵体:", repr(item[2]))
