# -*- coding: utf-8 -*-
# 摸清 questions.json 结构
import json, io

ROOT = 'D:/cjx/下载/Compressed/daguanyuan-for-windows-main.1.1/daguanyuan-for-windows-main/assets/'
qs = json.load(io.open(ROOT + 'questions.json', encoding='utf-8'))
print('type:', type(qs).__name__)
if isinstance(qs, dict):
    print('keys:', list(qs.keys())[:12])
    for k, v in qs.items():
        print('  %s -> %s (len=%s)' % (k, type(v).__name__, len(v) if hasattr(v, '__len__') else '-'))
    # 取一个样本
    for k, v in qs.items():
        if isinstance(v, list) and v:
            print('  样本[%s][0] type=%s' % (k, type(v[0]).__name__))
            if isinstance(v[0], dict):
                print('  字段:', list(v[0].keys()))
            break
elif isinstance(qs, list):
    print('len:', len(qs), '| 元素类型:', type(qs[0]).__name__)
    if isinstance(qs[0], dict):
        print('字段:', list(qs[0].keys()))
    else:
        print('元素样本:', str(qs[0])[:200])