# -*- coding: utf-8 -*-
"""extract_pdf.py — 从扫描版 PDF 用 OCR 提取文本，转为 Markdown"""
import fitz  # PyMuPDF
import sys
import os
import re
from rapidocr_onnxruntime import RapidOCR


def ocr_pages(pdf_path):
    engine = RapidOCR()
    doc = fitz.open(pdf_path)
    total = len(doc)
    zoom = 200 / 72
    mat = fitz.Matrix(zoom, zoom)
    results = []

    for i, page in enumerate(doc):
        print(f"  OCR {i+1}/{total} ...", end="", flush=True)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        ocr_result, _ = engine(img_bytes)
        if ocr_result:
            sorted_items = sorted(ocr_result, key=lambda x: (x[0][0][1], x[0][0][0]))
            lines = [item[1] for item in sorted_items]
            text = "\n".join(lines)
        else:
            text = ""
        results.append(text)
        print(f" {len(text)} 字")
    doc.close()
    return results


def clean_text(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+$', '', text, flags=re.M)
    return text.strip()


def format_markdown(pages, title):
    md = f"# {title}\n\n"
    for i, page in enumerate(pages):
        cleaned = clean_text(page)
        if cleaned:
            md += f"## 第{i+1}页\n\n{cleaned}\n\n"
    return md


def main():
    if len(sys.argv) < 2:
        print("用法: python -X utf8 extract_pdf.py <pdf路径> [输出目录]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else r"D:\ai code\math\导图"

    if not os.path.isfile(pdf_path):
        print(f"错误: 文件不存在 - {pdf_path}")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    title = re.sub(r'^\d{4}考研数学', '', base_name)
    title = re.sub(r'（最终版）$', '', title).strip()

    print(f"正在 OCR 提取: {pdf_path}")
    pages = ocr_pages(pdf_path)
    print(f"共 {len(pages)} 页")

    md_content = format_markdown(pages, title)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{base_name}.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"\n已保存到: {output_path}")


if __name__ == '__main__':
    main()
