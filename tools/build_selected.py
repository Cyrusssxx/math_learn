# -*- coding: utf-8 -*-
"""
build_selected.py — 从「数二模拟卷选填精选.pdf」提取模拟卷选填题到 selected.json

题目源：E:/Desktop/做题/数二精选模拟题和答案/数二模拟卷选填精选.pdf（94页，有文字层）
含 31 套：余炳森五套(5) + 李林四套(4) + 张宇四套(4) + 超越十套(10) + 张宇八套(8)
每套：选择题10道(1-10) + 填空题6道(11-16)

注意：题库文字层数学符号大量乱码（f x  、积分/矩阵错乱），本脚本只做【结构提取】，
      后续须逐套渲染 PNG 视觉核对修正（同真题管线）。answer 字段在答案OCR阶段填入。
"""
import fitz, re, json, os

SRC = r"E:/Desktop/做题/数二精选模拟题和答案/数二模拟卷选填精选.pdf"
OUT = r"D:/ai code/math-note/pwa/data/selected.json"

# (选择题起始页, id前缀, 分组, 标题)  —— 页号来自扫描定位，每套间隔3页
SETS = [
    (1,  "y24-ybs", "余炳森五套卷", "24 余炳森五套卷·卷一"),
    (4,  "y24-ybs", "余炳森五套卷", "24 余炳森五套卷·卷二"),
    (7,  "y24-ybs", "余炳森五套卷", "24 余炳森五套卷·卷三"),
    (10, "y24-ybs", "余炳森五套卷", "24 余炳森五套卷·卷四"),
    (13, "y24-ybs", "余炳森五套卷", "24 余炳森五套卷·卷五"),
    (16, "y24-ll",  "李林四套卷",   "24 李林四套卷·卷一"),
    (19, "y24-ll",  "李林四套卷",   "24 李林四套卷·卷二"),
    (22, "y24-ll",  "李林四套卷",   "24 李林四套卷·卷三"),
    (25, "y24-ll",  "李林四套卷",   "24 李林四套卷·卷四"),
    (28, "y24-zy4", "张宇四套卷",   "24 张宇四套卷·卷一"),
    (31, "y24-zy4", "张宇四套卷",   "24 张宇四套卷·卷二"),
    (34, "y24-zy4", "张宇四套卷",   "24 张宇四套卷·卷三"),
    (37, "y24-zy4", "张宇四套卷",   "24 张宇四套卷·卷四"),
    (40, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷一"),
    (43, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷二"),
    (46, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷三"),
    (49, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷四"),
    (52, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷五"),
    (55, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷六"),
    (58, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷七"),
    (61, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷八"),
    (64, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷九"),
    (67, "y24-cg",  "超越十套卷",   "24 超越十套卷·卷十"),
    (70, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷一"),
    (73, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷二"),
    (76, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷三"),
    (79, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷四"),
    (82, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷五"),
    (85, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷六"),
    (88, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷七"),
    (91, "y25-zy8", "张宇八套卷",   "25 张宇八套卷·卷八"),
]

# 选项标记：A. / A． / （A） / (A)
OPT_RE = re.compile(r'(?:^|\n)\s*\(?([A-Da-d])\)?[\.．、]\s*')
NUM_RE = re.compile(r'^\s*(\d+)\s*[\.．、]\s*(.*)', re.S)


def clean(s):
    # 轻量清理：去掉常见的私有区乱码占位符
    s = re.sub(r'[\uf000-\uf0ff]', '', s)
    s = re.sub(r'', "'", s)   # 导数 '
    s = re.sub(r'', '…', s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n{2,}', '\n', s)
    return s.strip()


def split_numbered(text):
    """按行首 'N.' 切分为 (no, body) 列表"""
    parts = re.split(r'(?m)^\s*(\d+)\s*[\.．、]\s*', text)
    # parts: [pre, '1', body1, '2', body2, ...]
    out = []
    i = 1
    while i + 1 < len(parts):
        no = int(parts[i])
        body = parts[i + 1]
        out.append((no, body))
        i += 2
    return out


def parse_choice(body):
    """选择题：切出 stem + 选项 [A-D]"""
    pos = [(m.start(), m.group(1).upper()) for m in OPT_RE.finditer(body)]
    if not pos:
        return clean(body.strip()), []
    stem = clean(body[:pos[0][0]].strip())
    opts = []
    for k, (p, letter) in enumerate(pos):
        end = pos[k + 1][0] if k + 1 < len(pos) else len(body)
        o = body[p:end]
        o = re.sub(r'^\(?[A-Da-d]\)?[\.．、]\s*', '', o).strip()
        opts.append(clean(o))
    return stem, opts


def parse_set(doc, p, prefix, group, title, idx):
    raw = "\n".join(doc[i].get_text() for i in range(p, min(p + 3, doc.page_count)))
    # 切 选择题 / 填空题
    m_choice = re.search(r'一[、.．]\s*选择题', raw)
    m_fill = re.search(r'二[、.．]\s*填空题', raw)
    c_start = m_choice.end() if m_choice else 0
    c_end = m_fill.start() if m_fill else len(raw)
    fill_start = m_fill.end() if m_fill else len(raw)

    choice_block = raw[c_start:c_end]
    fill_block = raw[fill_start:]

    choices = split_numbered(choice_block)
    fills = split_numbered(fill_block)

    questions_c = []
    for no, body in choices:
        stem, opts = parse_choice(body)
        if not opts:
            continue
        questions_c.append({
            "no": no, "kind": "choice",
            "stem": stem, "options": opts, "answer": ""
        })
    questions_f = []
    for no, body in fills:
        questions_f.append({
            "no": no, "kind": "fill",
            "stem": clean(body.strip()), "answer": ""
        })

    paper = {
        "id": f"{prefix}-{idx:02d}",
        "title": title,
        "group": group,
        "sections": [
            {"type": "choice", "questions": questions_c},
            {"type": "fill", "questions": questions_f},
        ],
    }
    return paper, len(questions_c), len(questions_f)


def main():
    doc = fitz.open(SRC)
    papers = []
    counts = []
    for n, (p, prefix, group, title) in enumerate(SETS, 1):
        paper, nc, nf = parse_set(doc, p, prefix, group, title, n)
        papers.append(paper)
        counts.append((title, nc, nf))
    doc.close()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump({"papers": papers}, f, ensure_ascii=False, indent=1)

    total_q = sum(c + f for _, c, f in counts)
    print(f"已写入 {OUT}")
    print(f"套卷数={len(papers)}  题目总数≈{total_q}")
    print("每套 选择/填空 数量：")
    for t, c, f in counts:
        flag = "  ⚠选题数!=10" if c != 10 else ""
        flag2 = "  ⚠填空数!=6" if f != 6 else ""
        print(f"  {t:28} 选择{c} 填空{f}{flag}{flag2}")


if __name__ == "__main__":
    main()
