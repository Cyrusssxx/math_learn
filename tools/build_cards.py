# -*- coding: utf-8 -*-
"""build_cards.py — 把导图 Markdown 拆成记忆卡片 JSON（math-cards 构建脚本）
用法：python -X utf8 build_cards.py [--only 高数4] [源目录]
    源目录默认 D:\\ai code\\math\\导图（相对本脚本推导），输出到 ../pwa/data/

解析规则（同 md2xmind.py）：剥 frontmatter；H1 忽略；H2 = 章；
缩进子弹点（2空格/级）逐级建树。保留 $...$ 原始 LaTeX 交给前端 KaTeX 渲染。

拆卡规则（按优先级，每节点一张卡）：
  1 example  行以「例：/例（」开头 → 正面=首个⇒/：之前的题干
  2 warn     含 ⚠️/⭐ → 正面=「关于X要注意什么？」
  3 term     叶子含「：」且冒号前≤15字 → 正面=「X 是什么？」
  4 list     有子节点 → 正面=「X 包含哪些要点？」
  5 fill     其余叶子 → 公式挖空填空卡
行尾 <!-- skip --> 可跳过该行不出卡（子节点照常处理）。
「## 考试大纲要点」章整体只出一张列举卡。
"""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DATA_DIR = TOOLS.parent / 'pwa' / 'data'
DEFAULT_SRC = TOOLS.parent.parent / 'math' / '导图'

SCHEMA_VERSION = 1
OUTLINE_H2 = '考试大纲要点'


def subject_of(stem):
    """文件名 → (学科key, 卡ID前缀)，如 高数3.1-一元积分-计算 → ('gs','gs3.1')"""
    m = re.match(r'^(高数|线代)([\d.]+)-', stem)
    if not m:
        raise ValueError(f'文件名不符合 高数N-/线代N- 规则: {stem}')
    key = 'gs' if m.group(1) == '高数' else 'xd'
    return key, key + m.group(2)


def clean(text):
    """去 HTML 注释与加粗星号，保留 $...$ LaTeX 原文"""
    text = re.sub(r'<!--.*?-->', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    return text.strip()


class Node:
    __slots__ = ('text', 'children', 'skip')

    def __init__(self, text, skip=False):
        self.text = text
        self.children = []
        self.skip = skip


def parse_md(path):
    """返回 [(章标题, [Node,...]), ...]"""
    lines = path.read_text(encoding='utf-8').splitlines()
    if lines and lines[0].strip() == '---':  # 剥离 frontmatter
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                lines = lines[i + 1:]
                break
    chapters = []
    nodes = None
    stack = []  # [(level, Node)]
    for line in lines:
        if not line.strip():
            continue
        if line.startswith('# ') and not line.startswith('## '):
            continue  # H1 = 文件主题，卡片里用文件名字段表达
        if line.startswith('## '):
            nodes = []
            chapters.append((clean(line[3:]), nodes))
            stack = []
            continue
        m = re.match(r'^(\s*)- (.*)$', line)
        if m and nodes is not None:
            level = len(m.group(1)) // 2
            skip = '<!-- skip -->' in m.group(2)
            node = Node(clean(m.group(2)), skip)
            while stack and stack[-1][0] >= level:
                stack.pop()
            if stack:
                stack[-1][1].children.append(node)
            else:
                nodes.append(node)
            stack.append((level, node))
    return chapters


# ---------------- 拆卡 ----------------

FORMULA_RE = re.compile(r'\$[^$]+\$')


def strip_markers(s):
    return s.replace('⚠️', '').replace('⭐', '').strip()


def visible_len(s):
    """去掉公式后的可见文本长度（用于术语卡冒号前长度判断）"""
    return len(FORMULA_RE.sub('', s))


def split_example(text):
    """例题行 → (题干正面, 是否成功)。切在首个 ⇒（数学链条），否则首个中文冒号之后的下一个「：」"""
    body = re.sub(r'^例[：:（(]?\s*', '', text)
    for sep in ('⇒', '⟹'):
        if sep in body:
            return body.split(sep, 1)[0].strip(), True
    # 无推导箭头：尝试「题干：解法」结构（跳过公式内部不存在中文冒号的问题）
    if '：' in body:
        head = body.split('：', 1)[0].strip()
        if visible_len(head) >= 2:
            return head, True
    return body, False  # 整行当题干（背面还有子节点兜底）


def make_card(node, chapter, path):
    """按优先级生成 (type, front, back)；返回 None 表示过滤"""
    text = node.text
    if not text or visible_len(text) < 4 and not FORMULA_RE.search(text):
        return None  # 纯标点/过短且无公式

    children_titles = [c.text for c in node.children]
    back_lines = lambda: '\n'.join('· ' + t for t in children_titles)

    if re.match(r'^例[：:（(]', text):
        stem, ok = split_example(text)
        back = text + ('\n' + back_lines() if children_titles else '')
        front = stem + '\n（例题，回忆解法）'
        return 'example', front, back

    if '⚠️' in text or '⭐' in text:
        plain = strip_markers(text)
        for sep in ('：', '——'):
            if sep in plain:
                head = plain.split(sep, 1)[0].strip()
                if 0 < visible_len(head) <= 20:
                    front = f'⚠️ 关于「{head}」要注意什么？'
                    break
        else:
            front = f'⚠️ 易错点：{plain[:12]}……后面是什么？'
        back = text + ('\n' + back_lines() if children_titles else '')
        return 'warn', front, back

    if '：' in text:
        head, tail = text.split('：', 1)
        if (tail.strip() and 0 < visible_len(head) <= 15 and not head.startswith('$')
                and '；' not in head and '。' not in head):
            back = tail.strip() + ('\n' + back_lines() if children_titles else '')
            return 'term', f'{head.strip()} 是什么？', back

    if node.children:
        return 'list', f'「{text}」包含哪些要点？', back_lines()

    # 兜底填空卡：挖掉最后一个公式；整行皆公式/无公式时退化为「后面是什么」
    spans = list(FORMULA_RE.finditer(text))
    if spans:
        last = spans[-1]
        front = (text[:last.start()] + ' ____ ' + text[last.end():]).strip()
        if front != '____' and visible_len(front) >= 2:
            return 'fill', front, text
    plain = strip_markers(FORMULA_RE.sub('', text)).strip('，。；、 ')
    head = plain[:12] if plain else text[:20]
    return 'fill', f'{head}……完整内容是什么？', text


def cards_from_file(path, id_prefix, subject):
    stem = path.stem
    chapters = parse_md(path)
    cards = []

    def walk(node, chapter, path_titles):
        if not node.skip:
            made = make_card(node, chapter, path_titles)
            if made:
                ctype, front, back = made
                cards.append({
                    'subject': subject, 'file': stem, 'chapter': chapter,
                    'path': path_titles, 'type': ctype,
                    'front': front, 'back': back,
                })
        for c in node.children:
            walk(c, chapter, path_titles + [node.text])

    for chapter, nodes in chapters:
        if chapter == OUTLINE_H2:  # 大纲章整体一张列举卡
            leaves = [n.text for n in nodes]
            cards.append({
                'subject': subject, 'file': stem, 'chapter': chapter,
                'path': [], 'type': 'list',
                'front': f'《{stem}》考试大纲要点有哪些？',
                'back': '\n'.join('· ' + t for t in leaves),
            })
            continue
        for n in nodes:
            walk(n, chapter, [])

    # 稳定 ID：前缀 + sha1(文件stem + 章 + 归一化正面)；碰撞时纳入 path 重算
    seen = {}
    result = []
    for c in cards:
        norm = re.sub(r'\s+', '', c['file'] + c['chapter'] + c['front'])
        cid = id_prefix + '-' + hashlib.sha1(norm.encode('utf-8')).hexdigest()[:8]
        if cid in seen:
            norm2 = re.sub(r'\s+', '', ''.join(c['path'])) + norm
            cid = id_prefix + '-' + hashlib.sha1(norm2.encode('utf-8')).hexdigest()[:8]
            if cid in seen:
                print(f'  ! 重复卡跳过: {cid} 「{c["front"][:30]}」')
                continue
        seen[cid] = True
        result.append({'id': cid, **c})
    return result


def main():
    args = sys.argv[1:]
    only = None
    if '--only' in args:
        i = args.index('--only')
        only = args[i + 1]
        args = args[:i] + args[i + 2:]
    src = Path(args[0]) if args else DEFAULT_SRC

    files = sorted(src.glob('*.md'))
    if only:
        files = [f for f in files if only in f.stem]
    if not files:
        print('未找到 md 文件:', src)
        sys.exit(1)

    by_subject = {}
    meta_files = {}
    for f in files:
        subject, prefix = subject_of(f.stem)
        cards = cards_from_file(f, prefix, subject)
        by_subject.setdefault(subject, []).extend(cards)
        by_chapter = {}
        for c in cards:
            by_chapter[c['chapter']] = by_chapter.get(c['chapter'], 0) + 1
        meta_files[f.stem] = len(cards)
        print(f'{f.stem}: {len(cards)} 张')
        for ch, n in by_chapter.items():
            print(f'    {ch}: {n}')

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    all_ids = set()
    for subject, cards in by_subject.items():
        ids = {c['id'] for c in cards}
        assert len(ids) == len(cards), f'{subject} 存在重复 ID'
        # ID 增删报告（对比上次构建）
        out = DATA_DIR / f'{subject}.json'
        if out.exists():
            old_ids = {c['id'] for c in json.loads(out.read_text(encoding='utf-8'))}
            added, removed = ids - old_ids, old_ids - ids
            if added or removed:
                print(f'[{subject}] 新增 {len(added)} 张，删除 {len(removed)} 张（对应进度将重置）')
        out.write_text(json.dumps(cards, ensure_ascii=False), encoding='utf-8')
        print(f'→ {out.name}: {len(cards)} 张, {out.stat().st_size // 1024}KB')
        total += len(cards)
        all_ids |= ids

    assert len(all_ids) == total, '跨学科重复 ID'
    meta = {
        'schemaVersion': SCHEMA_VERSION,
        'buildTime': time.strftime('%Y-%m-%d %H:%M:%S'),
        'files': meta_files,
        'total': total,
    }
    (DATA_DIR / 'meta.json').write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'共 {total} 张卡 → {DATA_DIR}')


if __name__ == '__main__':
    main()
