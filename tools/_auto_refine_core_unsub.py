# -*- coding: utf-8 -*-
import json, re

# 细分类 ID 规则映射表（根据考点树节点）
# 366 (导数计算):
#   377: 参数方程求导
#   376: 隐函数求导
#   378: 复合函数求导
#   379: 高阶导
#   375: 乘积求导
# 365 (导数应用):
#   381: 切法线
#   382: 极最拐
#   383: 曲率
#   384: 渐近线
#   385: 方程根/曲线交点/函数零点
#   386: 不等式
# 328 (连续):
#   341: 间断点
#   342: 判断或讨论连续性
#   343: 已知连续确定参数
# 484 (偏导数):
#   491: 多元函数求偏导
#   492: 求全微分
#   493: 多元复合函数求偏导
#   496: 多元隐函数求偏导
# 2321 (积分计算):
#   2323: 三角相关
#   2331: 两函数相乘
#   2337: 分段函数
#   2342: 反常积分特殊题型
#   2343: 含根式
#   2369: 有理函数
#   2354: 定积分特殊题型
# 321/329 (极限):
#   330: 0/0 型
#   331: 1^\infty 型
#   332: \infty - \infty 型
#   333: \infty / \infty 型
#   334: 0 \cdot \infty 型
#   335: 数列极限
#   336: 泰勒公式求极限
#   337: 夹逼准则 / 单调有界
#   338: 确定极限中的参数

def classify_stem(root, stem):
    st = stem.lower()
    
    # 导数计算
    if root == '366':
        if '参数方程' in stem or 'cases' in stem or ('x=' in st and 'y=' in st and 't' in st):
            return '377' # 参数方程求导
        if '高阶导' in stem or 'f^{(' in st or 'y^{(' in st or "'''" in st or "^{(n)}" in st or "^{(5)}" in st:
            return '379' # 高阶导
        if '由方程' in stem and '确定' in stem:
            return '376' # 隐函数求导
        if '变上限' in stem or '\\int_' in stem:
            return '378' # 变限积分复合求导
        return '378' # 复合函数求导
        
    # 导数应用
    elif root == '365':
        if '渐近线' in stem:
            return '384'
        if '曲率' in stem:
            return '383'
        if '切线' in stem or '法线' in stem:
            return '381'
        if '极值' in stem or '拐点' in stem or '最值' in stem or '极小' in stem or '极大' in stem:
            return '382'
        if '根' in stem or '零点' in stem or '交点' in stem:
            return '385'
        if '证明' in stem or '不等式' in stem or '<' in st or '>' in st or '\\le' in st or '\\ge' in st:
            return '386'
        return '382'

    # 连续
    elif root == '328':
        if '间断点' in stem:
            return '341'
        if '反求参数' in stem or '确定参数' in stem or '常数' in stem and ('a=' in st or 'b=' in st):
            return '343'
        return '342' # 判断或讨论连续性

    # 偏导数
    elif root == '484':
        if '全微分' in stem or 'df(' in st or 'dz=' in st:
            return '492'
        if '隐函数' in stem or ('由方程' in stem and '确定' in stem):
            return '496'
        if '极值' in stem:
            return '495'
        if '复合' in stem or '具有' in stem and '偏导数' in stem:
            return '493'
        return '491'

    # 积分计算
    elif root == '2321':
        if '反常' in stem or '+\\infty' in stem or '-\\infty' in stem:
            return '2342' # 反常积分特殊题型
        if '\\sin' in st or '\\cos' in st or '\\tan' in st or '\\cot' in st or '\\sec' in st or '\\csc' in st:
            return '2323' # 三角相关
        if '\\sqrt' in st:
            return '2343' # 含根式
        if '/' in st or '\\frac' in st or '\\dfrac' in st:
            # 判断分母是否为多项式乘积
            return '2369' # 有理函数
        if '分段' in stem or 'cases' in stem or '|' in st:
            return '2337' # 分段函数
        return '2354' # 定积分特殊题型

    # 极限
    elif root == '321':
        if '渐近线' in stem:
            return '384'
        if '反常' in stem:
            return '2342'
        if '1^' in st or '^{\\cot' in st or '^{\\frac' in st or '^{\\dfrac' in st:
            return '331' # 1^\infty
        if '数列' in stem or 'a_n' in st or 'x_n' in st:
            return '335' # 数列极限
        if '确定' in stem or '常数' in stem or '参数' in stem or '等价' in stem:
            return '338' # 确定参数
        if '\\sin' in st or 'x\\to 0' in st or 'x\\to0' in st:
            return '330' # 0/0 型
        return '330'
        
    return None

# 测试对 core_bank 54 题的归类效果
with open('pwa/data/core_bank.json', 'r', encoding='utf-8') as f:
    core_papers = json.load(f)

updated_count = 0
for p in core_papers:
    for sec in p.get('sections', []):
        for q in sec.get('questions', []):
            dcs = [str(x) for x in q.get('deepCats', [])]
            for root in ['2321', '321', '366', '328', '365', '484']:
                if root in dcs and len(dcs) == 1:
                    new_sub = classify_stem(root, q.get('stem', ''))
                    if new_sub:
                        # 补充新子分类进 deepCats
                        q['deepCats'].append(new_sub)
                        updated_count += 1
                        print(f"[{root} -> {new_sub}] #{q.get('no')} | {q.get('stem')[:45].replace(chr(10), ' ')}")

print(f"\n成功智能细化分类 {updated_count} 题！")

# 保存回 core_bank.json
with open('pwa/data/core_bank.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(core_papers, f, ensure_ascii=False, separators=(',', ':'))

print("已写回 core_bank.json！")
