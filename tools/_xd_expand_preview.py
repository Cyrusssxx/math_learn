# -*- coding: utf-8 -*-
# 预览：字母答案 + options 展开后的效果（抽样 8 道）
import json, io, re

d = json.load(io.open('pwa/data/xd_bank.json', encoding='utf-8'))
qs = [q for s in d[0]['sections'] for q in s['questions']]
letter_qs = [q for q in qs if re.fullmatch(r'[\$\(\)A-Da-d\.\s、,]{1,8}', str(q.get('answer') or '').strip()) and re.search(r'[A-Da-d]', str(q.get('answer') or ''))]

# 多选?（答案含多个字母，如 "AB"）
multi = [q for q in letter_qs if len(re.findall(r'[A-Da-d]', str(q.get('answer')))) > 1]
print('多字母答案:', len(multi), [q['no'] for q in multi][:10])
print()


def expand(q):
    a = str(q.get('answer') or '').strip()
    letters = re.findall(r'[A-Da-d]', a)
    opts = q.get('options') or []
    parts = []
    for L in letters:
        i = 'abcd'.index(L.lower())
        if 0 <= i < len(opts):
            txt = str(opts[i])
            # 去掉已有的 "A." 前缀
            txt = re.sub(r'^\s*[（(\[]?[A-Da-d][）)\].、:：]?\s*', '', txt).strip()
            parts.append('%s. %s' % (L.upper(), txt))
    return '（%s）' % '；'.join(parts) if parts else a


print('=== 展开效果预览（8 道）===')
for q in letter_qs[:8]:
    print('no=%s' % q['no'])
    print('  原答案: %r' % q.get('answer'))
    print('  展开后: %s' % expand(q)[:150])
    print()