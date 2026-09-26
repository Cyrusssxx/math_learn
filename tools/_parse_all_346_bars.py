# -*- coding: utf-8 -*-
import fitz
import re, json, io

pdf_path = r"D:/cjx/下载/QQ FileRecv/线性代数重点题_346题_35天做题本_按章顺序版.pdf"
doc = fitz.open(pdf_path)

# 匹配灰条结构
# 例如: "3分钟 难度 0.89 2015数一 #001 A 行列式 具体行列式计算 · a) 么字型"
# 或者包含 #\d{3} 的 block

pdf_questions = []

for pno in range(5, len(doc)):
    page = doc[pno]
    blocks = page.get_text("blocks")
    for b_idx, b in enumerate(blocks):
        txt = b[4].strip().replace('\n', ' ')
        # 寻找形如 #001 ~ #346
        m = re.search(r'#(\d{3})', txt)
        if m:
            qnum = int(m.group(1))
            # 这是一个灰条 block！
            # 我们解析灰条的各个字段
            # 形式通常是: [时长] [难度 xx] [来源] #xxx [章] [节·考点]
            # 例如: "3分钟 难度 0.89 2015数一 #001 A 行列式 具体行列式计算 · a) 么字型"
            
            # 分割 #xxx 前后
            pre = txt[:m.start()].strip()
            post = txt[m.end():].strip()
            
            # 解析 pre
            duration = ""
            difficulty = ""
            source = ""
            
            m_dur = re.search(r'(\d+分钟)', pre)
            if m_dur:
                duration = m_dur.group(1)
                pre = pre.replace(duration, '').strip()
                
            m_diff = re.search(r'难度\s*([\d\.]+)', pre)
            if m_diff:
                difficulty = m_diff.group(1)
                pre = re.sub(r'难度\s*[\d\.]+', '', pre).strip()
                
            source = pre.strip()
            
            # 解析 post
            # post 类似于: "A 行列式 具体行列式计算 · a) 么字型"
            parts = post.split()
            chapter = parts[0] if len(parts) > 0 else ""
            if len(parts) > 1 and parts[0] in ['A', 'B', 'C', 'D', 'E', 'F']:
                chapter = parts[0] + ' ' + parts[1]
                topic = " ".join(parts[2:])
            else:
                topic = " ".join(parts[1:])
                
            pdf_questions.append({
                'num': qnum,
                'page': pno + 1,
                'block_idx': b_idx,
                'raw_bar': txt,
                'duration': duration,
                'difficulty': difficulty,
                'source': source,
                'chapter': chapter,
                'topic': topic,
                'y0': b[1],
                'y1': b[3]
            })

# 排序并去重（根据题号）
pdf_questions.sort(key=lambda x: x['num'])
print(f"找到灰条题目数: {len(pdf_questions)}")

# 检查 1~346 的覆盖
seen = {}
for q in pdf_questions:
    seen[q['num']] = q

missing = [i for i in range(1, 347) if i not in seen]
print(f"缺失的题号数量: {len(missing)}")
if missing:
    print(f"缺失的题号: {missing}")

# 打印前 10 题解析结果
print("\n=== 前 10 题元数据样本 ===")
for i in range(1, 11):
    q = seen.get(i)
    if q:
        print(f"#{q['num']:03d} | P.{q['page']} | 来源: {q['source']:<35} | 难度: {q['difficulty']:<5} | 章: {q['chapter']} | 考点: {q['topic']}")
