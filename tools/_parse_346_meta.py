# -*- coding: utf-8 -*-
import fitz
import re, json, io

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

questions = []
# 正则匹配形如 #001 或 #123
re_num = re.compile(r'#(\d{3})')

for pno in range(4, len(doc)):
    page = doc[pno]
    text = page.get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 查找所有的 #xxx 及其位置
    matches = list(re_num.finditer(text))
    if not matches:
        continue
    
    # 我们也可以按块/行来解析
    # 在每页中，灰条通常包含：
    # [用时]
    # [难度 xx]
    # [来源，如 2015数一]
    # #001
    # [章，如 A 行列式]
    # [节/考点，如 具体行列式计算 · a) 么字型]
    # 后面是题面
    for idx, m in enumerate(matches):
        qnum = int(m.group(1))
        # 截取该题的文本范围
        start_pos = m.start()
        end_pos = matches[idx+1].start() if idx + 1 < len(matches) else len(text)
        q_raw = text[start_pos:end_pos]
        
        # 向前看一点找来源、难度、用时
        pre_text = text[max(0, start_pos - 150):start_pos]
        pre_lines = [l.strip() for l in pre_text.split('\n') if l.strip()]
        
        source = ""
        difficulty = ""
        duration = ""
        for pl in pre_lines:
            if '难度' in pl:
                difficulty = pl
            elif '分钟' in pl:
                duration = pl
            elif any(k in pl for k in ['数一', '数二', '数三', '880', '19', '20']):
                source = pl
                
        questions.append({
            'num': qnum,
            'page': pno + 1,
            'source': source,
            'difficulty': difficulty,
            'duration': duration,
            'raw_snippet': q_raw[:200].replace('\n', ' ')
        })

print(f"解析到题目数量: {len(questions)}")
print("第一题:", questions[0])
print("最后一题:", questions[-1])

# 检查是否有缺失的编号
all_nums = [q['num'] for q in questions]
unique_nums = set(all_nums)
missing = [i for i in range(1, 347) if i not in unique_nums]
print(f"1~346 中缺失的题号数量: {len(missing)}, 缺失列表: {missing}")
